from ..abstract_base_classes.repo_abc import RepoABC
from ...models.lob import LOB


__all__ = ['LOBRepo']


class LOBRepo(RepoABC):
    def __init__(self, lobtablecruder):
        self._lobtablecruder = lobtablecruder

    def get(self, key):
        lob = LOB()
        lob.set_key(key)

        return self._lobtablecruder.get(lob)

    def set(self, lob):
        self._lobtablecruder.update(lob)
