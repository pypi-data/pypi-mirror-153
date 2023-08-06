from . import _ResourceGroup

from .capabilities import _HasTeamsMixin, _HasSportingEventsMixin, _HasVideosMixin, _HasResourceGroupsMixin


class ClubResourceGroup(_ResourceGroup, _HasTeamsMixin, _HasSportingEventsMixin, _HasVideosMixin, _HasResourceGroupsMixin):
    pass
