from ..abstract_base_classes.agent import Agent


__all__ = ['OrderLogAgent', 'OrderLogTruncatedAgent']


class OrderLogAgent(Agent):
    def __init__(self, orderlogrepo, orderlogsolver):
        self._orderlogrepo = orderlogrepo
        self._orderlogsolver = orderlogsolver

    def get(self, key):
        if not self._orderlogrepo.get(key):
            orderlog = self._orderlogsolver.calculate(key)
            self._orderlogrepo.set(orderlog)
        return True


class OrderLogTruncatedAgent(OrderLogAgent):
    pass
