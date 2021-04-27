from ..abstract_base_classes.agent import Agent


__all__ = ['DailyTradedVolumeMoneyAgent']


class DailyTradedVolumeMoneyAgent(Agent):
    def __init__(self, dailytradedvolumemoneyrepo, dailytradedvolumemoneysolver):
        self._dailytradedvolumemoneyrepo = dailytradedvolumemoneyrepo
        self._dailytradedvolumemoneysolver = dailytradedvolumemoneysolver

    def get(self, key):
        dailytradedvolumemoney = self._dailytradedvolumemoneyrepo.get(key)
        if dailytradedvolumemoney is None:
            dailytradedvolumemoney = self._dailytradedvolumemoneysolver.calculate(key)
            self._dailytradedvolumemoneyrepo.set(dailytradedvolumemoney)
            dailytradedvolumemoney = self._dailytradedvolumemoneyrepo.get(key)

        return dailytradedvolumemoney
