from ..abstract_base_classes import RepoABC
from ...models.daily_traded_volume import DailyTradedVolume


__all__ = ['DailyTradedVolumeRepo']


class DailyTradedVolumeRepo(RepoABC):
    def __init__(self, dailytradedvolumetablecruder):
        self._dailytradedvolumetablecruder = dailytradedvolumetablecruder

    def get(self, key):
        dailytradedvolume = DailyTradedVolume()
        dailytradedvolume.set_key(key)

        return self._dailytradedvolumetablecruder.get(dailytradedvolume)

    def set(self, dailytradedvolume):
        self._dailytradedvolumetablecruder.update(dailytradedvolume)
