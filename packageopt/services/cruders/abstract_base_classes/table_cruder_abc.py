from abc import ABC, abstractmethod


__all__ = ['TableCRUDerABC']


class TableCRUDerABC(ABC):
    @abstractmethod
    def check_existance(self):
        pass

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def check_key(self, key):
        pass

    @abstractmethod
    def update(self, obj, separator, null):
        pass

    @abstractmethod
    def get(self, obj):
        pass
