from abc import ABC, abstractmethod


__all__ = ['Agent']


class Agent(ABC):
    @abstractmethod
    def get(self, key):
        pass
