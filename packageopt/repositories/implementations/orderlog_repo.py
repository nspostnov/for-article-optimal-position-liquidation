from ..abstract_base_classes import RepoABC
from ...models.orderlog import OrderLog, OrderLogTruncated


__all__ = ['OrderLogRepo', 'OrderLogTruncatedRepo']


class OrderLogRepo(RepoABC):
    def __init__(self, orderlogtablecruder):
        self._orderlogtablecruder = orderlogtablecruder

    def get(self, key):
        orderlog = OrderLog()
        orderlog.set_key(key)

        return self._orderlogtablecruder.get(orderlog)

    def set(self, orderlog):
        self._orderlogtablecruder.update(orderlog)


class OrderLogTruncatedRepo(RepoABC):
    def __init__(self, orderlogtablecruder):
        self._orderlogtablecruder = orderlogtablecruder

    def get(self, key):
        orderlog = OrderLogTruncated()
        orderlog.set_key(key)

        return self._orderlogtablecruder.get(orderlog)

    def set(self, orderlog):
        self._orderlogtablecruder.update(orderlog)
