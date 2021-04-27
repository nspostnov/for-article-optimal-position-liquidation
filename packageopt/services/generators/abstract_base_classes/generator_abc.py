from abc import ABC, abstractmethod


__all__ = ['GeneratorABC']


class GeneratorABC(ABC):
    @abstractmethod
    def generate(self):
        pass
