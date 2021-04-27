from ..abstract_base_classes.repo_abc import RepoABC
from ...models.strategy_optimal import StrategyOptimal


__all__ = ['StrategyOptimalRepo']


class StrategyOptimalRepo(RepoABC):
    def __init__(self, strategyoptimaltablecruder):
        self._strategyoptimaltablecruder = strategyoptimaltablecruder

    def get(self, key):
        strategyoptimal = StrategyOptimal()
        strategyoptimal.set_key(key)

        return self._strategyoptimaltablecruder.get(strategyoptimal)

    def set(self, strategyoptimal):
        self._strategyoptimaltablecruder.update(strategyoptimal)
