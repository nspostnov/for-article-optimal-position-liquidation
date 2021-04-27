from ..abstract_base_classes import RepoABC
from ...models.transaction_costs import TransactionCosts


__all__ = ['TransactionCostsRepo']


class TransactionCostsRepo(RepoABC):
    def __init__(self, transactioncoststablecruder):
        self._transactioncoststablecruder = transactioncoststablecruder

    def get(self, key):
        transactioncosts = TransactionCosts()
        transactioncosts.set_key(key)

        return self._transactioncoststablecruder.get(transactioncosts)

    def set(self, transactioncosts):
        self._transactioncoststablecruder.update(transactioncosts)
