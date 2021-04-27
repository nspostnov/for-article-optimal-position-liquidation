from ..abstract_base_classes.agent import Agent


__all__ = ['VolaAgent']


class VolaAgent(Agent):
    def __init__(self, volarepo, volasolver):
        self._volarepo = volarepo
        self._volasolver = volasolver

    def get(self, key):
        vola = self._volarepo.get(key)
        if vola is None:
            vola = self._volasolver.calculate(key)
            self._volarepo.set(vola)
            vola = self._volarepo.get(key)

        return vola
