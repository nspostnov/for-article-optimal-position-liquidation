from ..abstract_base_classes import RepoABC
from ...models.daily_activity import DailyActivity


__all__ = ['DailyActivityRepo']


class DailyActivityRepo(RepoABC):
    def __init__(self, dailyactivitytablecruder):
        self._dailyactivitytablecruder = dailyactivitytablecruder

    def get(self, key):
        dailyactivity = DailyActivity()
        dailyactivity.set_key(key)

        return self._dailyactivitytablecruder.get(dailyactivity)

    def set(self, dailyactivity):
        self._dailyactivitytablecruder.update(dailyactivity)
