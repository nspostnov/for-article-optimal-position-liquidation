from ..abstract_base_classes import RepoABC
from ...models.vola import Vola


__all__ = ['VolaRepo']


class VolaRepo(RepoABC):
    def __init__(self, volatablecruder):
        self._volatablecruder = volatablecruder

    def get(self, key):
        vola = Vola()
        vola.set_key(key)

        return self._volatablecruder.get(vola)
    
    def set(self, vola):
        self._volatablecruder.update(vola)
