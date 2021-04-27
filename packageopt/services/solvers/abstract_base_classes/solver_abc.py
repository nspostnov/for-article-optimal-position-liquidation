from abc import ABC, abstractmethod


__all__ = ['SolverABC']


class SolverABC(ABC):
    @abstractmethod
    def calculate(self, key):
        pass
