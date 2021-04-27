from ..abstract_base_classes.agent import Agent


__all__ = ['DailyActivityAgent']


class DailyActivityAgent(Agent):
    def __init__(self, dailyactivityrepo, dailyactivitysolver):
        self._dailyactivityrepo = dailyactivityrepo
        self._dailyactivitysolver = dailyactivitysolver

    def get(self, key):
        dailyactivity = self._dailyactivityrepo.get(key)
        if dailyactivity is None:
            dailyactivity = self._dailyactivitysolver.calculate(key)
            self._dailyactivityrepo.set(dailyactivity)
            dailyactivity = self._dailyactivityrepo.get(key)

        return dailyactivity
