from ..abstract_base_classes.agent import Agent


__all__ = ['TransactionCostsAgent']


class TransactionCostsAgent(Agent):
    def __init__(self, transactioncostsrepo, transactioncostssolver):
        self._transactioncostsrepo = transactioncostsrepo
        self._transactioncostssolver = transactioncostssolver

    def get(self, key):
        transactioncosts = self._transactioncostsrepo.get(key)
        if transactioncosts is None:
            transactioncosts = self._transactioncostssolver.calculate(key)
            self._transactioncostsrepo.set(transactioncosts)
            transactioncosts = self._transactioncostsrepo.get(key)

        return transactioncosts
