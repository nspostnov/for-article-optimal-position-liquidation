from ..abstract_base_classes.agent import Agent


__all__ = ['StrategyOptimalAgent']


class StrategyOptimalAgent(Agent):
    def __init__(self, strategyoptimalrepo, strategyoptimalsolver):
        self._strategyoptimalrepo = strategyoptimalrepo
        self._strategyoptimalsolver = strategyoptimalsolver

    def get(self, key):
        strategyoptimal = self._strategyoptimalrepo.get(key)
        if strategyoptimal is None:
            strategyoptimal = self._strategyoptimalsolver.calculate(key)
            self._strategyoptimalrepo.set(strategyoptimal)
            strategyoptimal = self._strategyoptimalrepo.get(key)

        return strategyoptimal
