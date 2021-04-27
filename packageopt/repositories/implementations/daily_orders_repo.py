from ..abstract_base_classes import RepoABC
from ...models.daily_orders import DailyOrders


__all__ = ['DailyOrdersRepo']


class DailyOrdersRepo(RepoABC):
    def __init__(self, dailyorderstablecruder):
        self._dailyorderstablecruder = dailyorderstablecruder

    def get(self, key):
        dailyorders = DailyOrders()
        dailyorders.set_key(key)

        return self._dailyorderstablecruder.get(dailyorders)

    def set(self, dailyorders):
        self._dailyorderstablecruder.update(dailyorders)
