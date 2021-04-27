from ..abstract_base_classes.repo_abc import RepoABC
from ...models.price import Price


__all__ = ['PriceRepo']


class PriceRepo(RepoABC):
    def __init__(self, pricetablecruder):
        self._pricetablecruder = pricetablecruder

    def get(self, key):
        price = Price()
        price.set_key(key)

        return self._pricetablecruder.get(price)

    def set(self, price):
        self._pricetablecruder.update(price)
