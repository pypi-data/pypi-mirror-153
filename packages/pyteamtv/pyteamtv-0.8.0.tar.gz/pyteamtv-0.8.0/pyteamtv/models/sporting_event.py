import logging
import os
from datetime import datetime
from typing import Optional, Union

from .list import List
from .observation import Observation
from .observation_log import ObservationLog
from .teamtv_object import TeamTVObject
from .video import Video

from tusclient.uploader import Uploader


class Clock(TeamTVObject):
    @property
    def clock_id(self):
        return self._clock_id

    @property
    def synchronization_points(self):
        return self._synchronization_points

    def add_synchronization_point(self, type_: str, key: str, time: Union[float, datetime]):
        if self.clock_id == 'U1':
            formatted_time = datetime.isoformat(time).replace("+00:00", "Z")
        else:
            formatted_time = float(time)

        self._requester.request(
            "POST",
            f"/sportingEvents/{self._sporting_event_id}/addSynchronizationPoint",
            {
                'clockId': self._clock_id,
                'type': type_,
                'key': key,
                'time': formatted_time
            }
        )

        # TODO: maybe get this one from backend
        self._synchronization_points.append(
            {
                "type": type_,
                "key": str(key),
                "time": time
            }
        )

    def remove_synchronization_point(self, type_: str, key: str):
        self._requester.request(
            "POST",
            f"/sportingEvents/{self._sporting_event_id}/removeSynchronizationPoint",
            {
                'clockId': self._clock_id,
                'type': type_,
                'key': key
            }
        )

        # TODO: maybe get this one from backend
        for i, synchronization_point in enumerate(self._synchronization_points):
            if synchronization_point['type'] == type_ and synchronization_point['key'] == str(key):
                self._synchronization_points.pop(i)
                break

    def _use_attributes(self, attributes: dict):
        self._sporting_event_id = attributes['sportingEventId']
        self._clock_id = attributes['clockId']
        self._synchronization_points = [
            {
                'type': synchronization_point['type'],
                'key': synchronization_point['key'],
                'time': (
                    float(synchronization_point['time'])
                    if self._clock_id != 'U1' else
                    datetime.fromisoformat(synchronization_point['time'].replace("Z", "+00:00"))
                )
            }
            for synchronization_point in
            attributes['synchronizationPoints']
        ]

    def __repr__(self):
        return f"<Clock id={self._clock_id} synchronization_points={self._synchronization_points}>"

class SportingEvent(TeamTVObject):
    @property
    def scheduled_at(self) -> datetime:
        return self._scheduled_at

    @property
    def sporting_event_id(self) -> str:
        return self._sporting_event_id

    @property
    def name(self):
        return self._name

    @property
    def tags(self):
        return self._tags

    @property
    def main_video_id(self) -> Optional[str]:
        if self._video_ids:
            return self._video_ids[0]
        return None

    @property
    def is_local(self):
        return self._is_local

    def get_clock(self, id_: str) -> Optional[Clock]:
        if id_ not in self._clocks:
            for key, clock in self._clocks.items():
                if clock['clockId'] == id_:
                    id_ = key
                    break
            else:
                return None

        return Clock(
            self._requester,
            {
                "sportingEventId": self.sporting_event_id,
                **self._clocks[id_]
            }
        )

    def get_observation_log(self) -> ObservationLog:
        video_id = self.main_video_id
        if video_id:
            clock_id = self._clocks[video_id]['clockId']
        else:
            clock_id = 'U1'

        return ObservationLog(
            Observation,
            self._requester,
            "GET",
            f"/sportingEvents/{self.sporting_event_id}/observations/{clock_id}",
            clock_id,
            self
        )

    def get_videos(self) -> List[Video]:
        def _filter(video: Video) -> bool:
            return video.video_id in self._video_ids

        return List(
            Video,
            self._requester,
            "GET",
            "/videos",
            item_filter=_filter
        )

    def upload_video(self, *file_paths: str, chunks_per_request: int = 1, tags: Optional[dict] = None) -> Video:
        chunks_per_request = int(chunks_per_request)
        if chunks_per_request < 1:
            chunks_per_request = 1

        files = []
        for filename in file_paths:
            files.append({
                'name': os.path.basename(filename),
                'size': os.path.getsize(filename)
            })

        video_id = self._requester.request(
            "POST",
            f"/sportingEvents/{self.sporting_event_id}/initVideoUpload",
            {
                "files": files,
                "tags": tags or {}
            }
        )

        video = Video(
            self._requester,
            self._requester.request(
                "GET",
                f"/videos/{video_id}"
            )
        )
        for i, part in enumerate(video.parts):
            uploader = Uploader(
                file_paths[i],
                url=part['tusUploadUrl'],
                chunk_size=chunks_per_request * 25 * 1024 * 1024,
                log_func=lambda msg: logging.info(f"Uploading: {msg}"),

                retries=5,
                retry_delay=5
            )

            uploader.upload()

        return Video(
            self._requester,
            self._requester.request(
                "GET",
                f"/videos/{video_id}"
            )
        )

    def _use_attributes(self, attributes: dict):
        self._name = attributes['name']
        self._sporting_event_id = attributes['sportingEventId']
        self._tags = attributes.get('tags', {})
        self._video_ids = attributes.get('videoIds', [])
        self._clocks = attributes['clocks']
        self._scheduled_at = datetime.fromisoformat(attributes['scheduledAt'].replace("Z", "+00:00"))
        self._is_local = attributes['_metadata']['source']['type'] == 'ResourceGroup'

    def __str__(self):
        return f"{self._scheduled_at.strftime('%d/%m/%y')} {self._name}"
