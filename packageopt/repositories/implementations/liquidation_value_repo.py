from ..abstract_base_classes.repo_abc import RepoABC
from ...models.liquidation_value import LiquidationValue


__all__ = ['LiquidationValueRepo']


class LiquidationValueRepo(RepoABC):
    def __init__(self, liquidationvaluetablecruder):
        self._liquidationvaluetablecruder = liquidationvaluetablecruder

    def get(self, key):
        liquidationvalue = LiquidationValue()
        liquidationvalue.set_key(key)

        return self._liquidationvaluetablecruder.get(liquidationvalue)

    def set(self, liquidationvalue):
        self._liquidationvaluetablecruder.update(liquidationvalue)
