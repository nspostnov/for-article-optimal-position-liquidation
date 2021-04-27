from ..abstract_base_classes.agent import Agent


__all__ = ['PriceAgent']


class PriceAgent(Agent):
    def __init__(self, pricerepo, pricesolver):
        self._pricerepo = pricerepo
        self._pricesolver = pricesolver

    def get(self, key):
        price = self._pricerepo.get(key)
        if price is None:
            price = self._pricesolver.calculate(key)
            self._pricerepo.set(price)
            price = self._pricerepo.get(key)

        return price
