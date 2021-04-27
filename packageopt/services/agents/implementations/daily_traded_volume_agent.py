from ..abstract_base_classes.agent import Agent


__all__ = ['DailyTradedVolumeAgent']


class DailyTradedVolumeAgent(Agent):
    def __init__(self, dailytradedvolumerepo, dailytradedvolumesolver):
        self._dailytradedvolumerepo = dailytradedvolumerepo
        self._dailytradedvolumesolver = dailytradedvolumesolver

    def get(self, key):
        dailytradedvolume = self._dailytradedvolumerepo.get(key)
        if dailytradedvolume is None:
            dailytradedvolume = self._dailytradedvolumesolver.calculate(key)
            self._dailytradedvolumerepo.set(dailytradedvolume)
            dailytradedvolume = self._dailytradedvolumerepo.get(key)

        return dailytradedvolume
