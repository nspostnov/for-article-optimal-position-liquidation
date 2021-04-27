import numpy as np
import sys

import config
from packageopt import *

ARGS = sys.argv[1:]  # ticker date
_SECCODES = list(np.unique(ARGS[::2]))
_DATES = list(np.unique([int(x) for x in ARGS[1::2]]))


HYPERPARAMS = {
        'DATE_INITIAL': 20190603, # initial date of start calculation
        'TIME_INITIAL': 110000000000, # initial time of start calculation 
        'STEP_VOLA_LENGTH': 5, # time in seconds for step calculation the vola estimates
        'BACKWARD_NUM_STEPS': 720, # the number of steps for vola estimates (for 5 second step for 1 hour it's 720)
        'NUM_STEPS': 20, # the number of steps of liquidation procedure
        'STEP_LENGTH': 30, # time in seconds in the step's length of liquidation
        'LAMBDA': 1, # the lambda parameter of the optimization task
        'DATES': [int(x) for x in _DATES], # the list of dates to calculate
        'SECCODES': _SECCODES, # the list of tickers to calculate
        'TASK_STEP_LENGTH': 300, # the step between tasks to calculate (5 minutes is 300)
        'TASK_STEPS_NUMBER': 84, # the number of steps for task (84 steps for 5 minutes length calculates the timerange from 11.00 to 18.00)
        'USER': config.USER, # the user of database
        'PASSWORD': config.PASSWORD, # the password from user 
        'HOST': config.HOST, # the host for connection
        'PORT': config.PORT, # the port of server
        'DB_NAME': config.DB_NAME, # the name of database to create and work with
        'PATH_INITIAL': config.PATH_INITIAL, # the path to initial .txt files with orderlogs
        }


def main():
    Main(
        HYPERPARAMS['USER'], 
        HYPERPARAMS['PASSWORD'], 
        HYPERPARAMS['HOST'], 
        HYPERPARAMS['PORT'],
        HYPERPARAMS['DB_NAME'], 
        HYPERPARAMS['PATH_INITIAL']).run()


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

        liquidationvaluetable = LiquidationValueTruncatedTable(date=date, seccode=seccode)
        liquidationvaluetablecruder = LiquidationValueTableCRUDer(
                liquidationvaluetable, connector)
        liquidationvaluerepo = LiquidationValueRepo(liquidationvaluetablecruder)
        liquidationvaluesolver = LiquidationValueSolver(
                lobagent, strategyoptimalagent, liquidationvaluetable, 
                TimeGenerator)
        liquidationvalueagent = LiquidationValueAgent(liquidationvaluerepo, 
                liquidationvaluesolver)

        liquidationvalueagent.get(key)

    def _calculate_key(self):
        step_vola_length = HYPERPARAMS['STEP_VOLA_LENGTH']
        backward_num_steps = HYPERPARAMS['BACKWARD_NUM_STEPS']
        num_steps = HYPERPARAMS['NUM_STEPS']
        step_length = HYPERPARAMS['STEP_LENGTH']
        lam = HYPERPARAMS['LAMBDA']
        date_initial = HYPERPARAMS['DATE_INITIAL']
        time_initial = HYPERPARAMS['TIME_INITIAL']
        dates = HYPERPARAMS['DATES']
        seccodes = HYPERPARAMS['SECCODES']

        time_obj = Time()
        time_obj.set_date(date_initial)
        time_obj.set_time(time_initial)
        times = TimeGenerator(
                time_obj, 
                step_length=HYPERPARAMS['TASK_STEP_LENGTH'], 
                num_steps=HYPERPARAMS['TASK_STEPS_NUMBER'], 
                include_initial=True,
                direction='up').generate()
        times = list(map(lambda x: x.get_time(), times))
        
        keys = []
        for seccode in seccodes:
            for date in dates:
                db = DataBase(dbname=self._dbname, user=self._user,
                        password=self._password, host=self._host,
                        port=self._port)
                dbcruder = DataBaseCRUDer(db)
                connector = DataBaseConnector(dbcruder)

                orderlogtable = OrderLogTable(date=date)
                orderlogtablecruder = OrderLogTableCRUDer(orderlogtable, 
                        connector)
                orderlogrepo = OrderLogRepo(orderlogtablecruder)
                orderlogsolver = OrderLogSolver(self._path)
                orderlogagent = OrderLogAgent(orderlogrepo, orderlogsolver)
                
                dailytradedvolumetable = DailyTradedVolumeTable()
                dailytradedvolumetablecruder = DailyTradedVolumeTableCRUDer(
                        dailytradedvolumetable, connector)
                dailytradedvolumerepo = DailyTradedVolumeRepo(
                        dailytradedvolumetablecruder)
                dailytradedvolumesolver = DailyTradedVolumeSolver(
                        orderlogagent, orderlogtable, 
                        dailytradedvolumetable, connector)
                dailytradedvolumeagent = DailyTradedVolumeAgent(
                        dailytradedvolumerepo, dailytradedvolumesolver)


                volume_to_liquidate = int(dailytradedvolumeagent.get(
                        [date, seccode]).get_data().volume[0] * (
                                num_steps * step_length / ((8*60 + 45)*60)))
                
                for time in times:
                    key = [date, seccode, time, 
                            step_vola_length, backward_num_steps,
                            num_steps, step_length, volume_to_liquidate, 
                            lam]
                    keys.append(key)
        return keys

    def run(self):
        keys = self._calculate_key()
        for key in keys:
            print(key[:3])
            self._calculate(key)


if __name__ == '__main__':
    main()
