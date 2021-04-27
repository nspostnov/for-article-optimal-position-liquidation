from abc import ABC, abstractmethod


__all__ = ['RepoABC']


class RepoABC(ABC):
    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def set(self, obj):
        pass
