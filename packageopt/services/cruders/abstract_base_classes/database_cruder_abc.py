from abc import ABC, abstractmethod


__all__ = ['DataBaseCRUDerABC']


class DataBaseCRUDerABC(ABC):
    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def check_existance(self):
        pass

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, value, traceback):
        pass
