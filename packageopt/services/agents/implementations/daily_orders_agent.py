from ..abstract_base_classes.agent import Agent


__all__ = ['DailyOrdersAgent']


class DailyOrdersAgent(Agent):
    def __init__(self, dailyordersrepo, dailyorderssolver):
        self._dailyordersrepo = dailyordersrepo
        self._dailyorderssolver = dailyorderssolver

    def get(self, key):
        dailyorders = self._dailyordersrepo.get(key)
        if dailyorders is None:
            dailyorders = self._dailyorderssolver.calculate(key)
            self._dailyordersrepo.set(dailyorders)
            dailyorders = self._dailyordersrepo.get(key)

        return dailyorders
