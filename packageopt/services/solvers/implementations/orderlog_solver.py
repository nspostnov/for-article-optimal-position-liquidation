import os
from ..abstract_base_classes.solver_abc import SolverABC
from ....models.orderlog import OrderLog, OrderLogTruncated


__all__ = ['OrderLogSolver', 'OrderLogTruncatedSolver']


class OrderLogSolver(SolverABC):
    def __init__(self, path_to_logs):
        self._path_to_logs = path_to_logs

    def calculate(self, key):
        '''here key is date (int)
        '''
        path = os.path.join(self._path_to_logs, 
                'OrderLog' + str(key) + '.txt')
        file_ = open(path, 'r')
        orderlog = OrderLog()
        orderlog.set_key(key)
        orderlog.set_data(file_)

        return orderlog


class OrderLogTruncatedSolver(SolverABC):
    def __init__(self, path_to_logs):
        self._path_to_logs = path_to_logs

    def calculate(self, key):
        '''here key is list(int, str): date and seccode
        '''
        path = os.path.join(self._path_to_logs, 'OrderLog' + str(key[0]) + '.txt')
        file_ = open(path, 'r')
        parent_orderlog = OrderLog()
        parent_orderlog.set_key(key[0])
        parent_orderlog.set_data(file_)

        orderlog = OrderLogTruncated()
        orderlog.set_key(key)
        orderlog.set_data(parent_orderlog)

        return orderlog
