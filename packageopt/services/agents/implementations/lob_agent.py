from ..abstract_base_classes.agent import Agent


__all__ = ['LOBAgent']


class LOBAgent(Agent):
    def __init__(self, lobrepo, lobsolver):
        self._lobrepo = lobrepo
        self._lobsolver = lobsolver

    def get(self, key):
        lob = self._lobrepo.get(key)
        if lob is None:
            lob = self._lobsolver.calculate(key)
            self._lobrepo.set(lob)
            lob = self._lobrepo.get(key)

        return lob    
