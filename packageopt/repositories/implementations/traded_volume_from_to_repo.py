from ..abstract_base_classes import RepoABC
from ...models.traded_volume_from_to import TradedVolumeFromTo


__all__ = ['TradedVolumeFromToRepo']


class TradedVolumeFromToRepo(RepoABC):
    def __init__(self, tradedvolumefromtotablecruder):
        self._tradedvolumefromtotablecruder = tradedvolumefromtotablecruder

    def get(self, key):
        tradedvolumefromto = TradedVolumeFromTo()
        tradedvolumefromto.set_key(key)

        return self._tradedvolumefromtotablecruder.get(tradedvolumefromto)

    def set(self, tradedvolumefromto):
        self._tradedvolumefromtotablecruder.update(tradedvolumefromto)
