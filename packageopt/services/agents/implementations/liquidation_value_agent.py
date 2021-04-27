from ..abstract_base_classes.agent import Agent


__all__ = ['LiquidationValueAgent']


class LiquidationValueAgent(Agent):
    def __init__(self, liquidationvaluerepo, liquidationvaluesolver):
        self._liquidationvaluerepo = liquidationvaluerepo
        self._liquidationvaluesolver = liquidationvaluesolver

    def get(self, key):
        liquidationvalue = self._liquidationvaluerepo.get(key)
        if liquidationvalue is None:
            liquidationvalue = self._liquidationvaluesolver.calculate(key)
            self._liquidationvaluerepo.set(liquidationvalue)
            liquidationvalue = self._liquidationvaluerepo.get(key)

        return liquidationvalue
