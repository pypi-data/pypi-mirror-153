# pyteamtv

## Upload a video

```python
import pyteamtv

# Make sure TEAMTV_API_TOKEN environment variable is set
team = pyteamtv.get_team('Koenstest 1')

sporting_event = team.get_sporting_event('123213-123123-123123-123')
sporting_event.upload_video('/home/koen/Wedstrijd_zaterdag.mp4')
```
