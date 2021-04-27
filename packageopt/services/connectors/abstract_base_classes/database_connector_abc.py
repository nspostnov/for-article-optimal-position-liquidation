from abc import ABC, abstractmethod


__all__ = ['DataBaseConnectorABC']


class DataBaseConnectorABC(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, value, traceback):
        pass
