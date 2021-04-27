import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import config

from packageopt import * 


STEP_VOLA_LENGTH = 5
BACKWARD_NUM_STEPS = 720

SECCODE = 'SBER'
DATE = 20190605
TIME = 110500000000
VOLUME_TO_LIQUIDATE = 983556

DIVIDER = 10**3


PATH_ABS = config.PATH_TO_SAVE_1
PATH_FROM_ABS = config.PATH_TO_SAVE_2
PATH_LOGS = config.PATH_INITIAL
DB_USER = config.USER
DB_PASSWORD = config.PASSWORD
DB_HOST = config.HOST
DB_PORT = config.PORT
DB_NAME = config.DB_NAME


def main():
    strats_lam = []
    lam_list = [0.1, 1, 5, 100]
    for lam in lam_list:
        strategy = calculate_strategy_reverse(15, 60, lam)
        strats_lam.append(strategy)

    strats_num = []
    num_list = [3, 5, 10, 15]
    for num in num_list:
        strategy = calculate_strategy_reverse(num, 60, 5)
        strats_num.append(strategy)

    figure, (ax1, ax2) = plt.subplots(2, 1, sharey=True)
    colors = ['#000000', '#303030', '#888888', '#D3D3D3']
    for j in range(len(strats_lam)):
        ax1.plot(strats_lam[j] / DIVIDER, color=colors[j])

    for j in range(len(strats_num)):
        ax2.plot(strats_num[j] / DIVIDER, color=colors[j])

    datetime = transpose_datetime(DATE, TIME)

    ax1.title.set_text('Ликвидация ' + SECCODE + ', начиная с ' + datetime)
    ax1.set_ylabel('Остаток позиции, тыс. шт.')
    ax2.set_ylabel('Остаток позиции, тыс. шт.')
    ax2.set_xlabel('Номер шага ликвидации')
    ax1.legend([r'$\lambda = {}$'.format(x) for x in lam_list])
    ax2.legend([r'$N = {}$'.format(x) for x in num_list])
    figure.set_size_inches(w=6, h=8)
    
    path_name = 'optimization_solution.pgf'
    path = os.path.join(PATH_ABS, PATH_FROM_ABS, path_name)
    plt.savefig(path, bbox_inches='tight')
    plt.show()


def calculate_strategy_reverse(num_steps, step_length, lam):
    process = Main(DB_USER, DB_PASSWORD, DB_HOST, 
            DB_PORT, DB_NAME, PATH_LOGS)
    key = [
            DATE,
            SECCODE,
            TIME,
            STEP_VOLA_LENGTH,
            BACKWARD_NUM_STEPS,
            num_steps,
            step_length,
            VOLUME_TO_LIQUIDATE, 
            lam]
    print(key)
    result = process.run(key).get_data()

    volume = int(result['volume_to_liquidate'][0])
    strategy = np.array(list(map(int, result['strategy'][0])))

    strategy = np.array([volume] + list(volume - np.cumsum(strategy)))

    return strategy


def transpose_datetime(date, time):
    str_date_base = str(date)
    str_date = '-'.join([str_date_base[:4], str_date_base[4:6], str_date_base[6:]])

    str_time_base = str(time)
    str_time = ':'.join([str_time_base[:2], str_time_base[2:4], str_time_base[4:6]])

    datetime = ' '.join([str_date, str_time])

    return datetime


class Main:
    def __init__(self, user, password, host, port, dbname, path_to_logs):
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._dbname = dbname
        self._path = path_to_logs

    def _calculate(self, key):
        db = DataBase(dbname=self._dbname, user=self._user, password=self._password,
                host=self._host, port=self._port)
        dbcruder = DataBaseCRUDer(db)
        connector = DataBaseConnector(dbcruder)

        date, seccode = key[0], key[1]

        orderlogtable_date = OrderLogTable(date=date)
        orderlogtablecruder_date = OrderLogTableCRUDer(orderlogtable_date, connector)
        orderlogrepo_date = OrderLogRepo(orderlogtablecruder_date)
        orderlogsolver_date = OrderLogSolver(self._path)
        orderlogagent_date = OrderLogAgent(orderlogrepo_date, orderlogsolver_date)

        orderlogtable = OrderLogTruncatedTable(date=date, seccode=seccode)
        orderlogtablecruder = OrderLogTableTruncatedCRUDer(orderlogtable, orderlogtable_date, connector)
        orderlogrepo = OrderLogTruncatedRepo(orderlogtablecruder)
        orderlogsolver = OrderLogTruncatedSolver(self._path)
        orderlogagent = OrderLogTruncatedAgent(orderlogrepo, orderlogsolver)

        lobtable = LOBTruncatedTable(date=date, seccode=seccode)
        lobtablecruder = LOBTableCRUDer(lobtable, connector)
        lobrepo = LOBRepo(lobtablecruder)
        lobsolver = LOBSolver(orderlogagent, orderlogtable, lobtable, connector)
        lobagent = LOBAgent(lobrepo, lobsolver)

        pricetable = PriceTruncatedTable(date=date, seccode=seccode)
        pricetablecruder = PriceTableCRUDer(pricetable, connector)
        pricerepo = PriceRepo(pricetablecruder)
        pricesolver = PriceSolver(lobagent, pricetable)
        priceagent = PriceAgent(pricerepo, pricesolver)

        transactioncoststable = TransactionCostsTruncatedTable(date=date, seccode=seccode)
        transactioncoststablecruder = TransactionCostsTableCRUDer(
                transactioncoststable, connector)
        transactioncostsrepo = TransactionCostsRepo(transactioncoststablecruder)
        transactioncostssolver = TransactionCostsSolver(lobagent,
                priceagent, transactioncoststable)
        transactioncostsagent = TransactionCostsAgent(transactioncostsrepo,
                transactioncostssolver)

        volatable = VolaTruncatedTable(date=date, seccode=seccode)
        volatablecruder = VolaTableCRUDer(volatable, connector)
        volarepo = VolaRepo(volatablecruder)
        volasolver = VolaSolver(volatable, priceagent, TimeGenerator)
        volaagent = VolaAgent(volarepo, volasolver)

        strategyoptimaltable = StrategyOptimalTruncatedTable(date=date, seccode=seccode)
        strategyoptimaltablecruder = StrategyOptimalTableCRUDer(strategyoptimaltable,
                connector)
        strategyoptimalrepo = StrategyOptimalRepo(strategyoptimaltablecruder)
        strategyoptimalsolver = StrategyOptimalSolver(volaagent,
                transactioncostsagent, strategyoptimaltable)
        strategyoptimalagent = StrategyOptimalAgent(strategyoptimalrepo,
                strategyoptimalsolver)

        return strategyoptimalagent.get(key)

    def run(self, key):
        strategy = self._calculate(key)

        return strategy


if __name__ == '__main__':
    main()
