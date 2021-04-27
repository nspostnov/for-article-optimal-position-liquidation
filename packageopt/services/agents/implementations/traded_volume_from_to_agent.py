from ..abstract_base_classes.agent import Agent


__all__ = ['TradedVolumeFromToAgent']


class TradedVolumeFromToAgent(Agent):
    def __init__(self, tradedvolumefromtorepo, tradedvolumefromtosolver):
        self._tradedvolumefromtorepo = tradedvolumefromtorepo
        self._tradedvolumefromtosolver = tradedvolumefromtosolver

    def get(self, key):
        tradedvolumefromto = self._tradedvolumefromtorepo.get(key)
        if tradedvolumefromto is None:
            tradedvolumefromto = self._tradedvolumefromtosolver.calculate(key)
            self._tradedvolumefromtorepo.set(tradedvolumefromto)
            tradedvolumefromto = self._tradedvolumefromtorepo.get(key)

        return tradedvolumefromto
