import os
import numpy as np
import matplotlib.pyplot as plt

import config 

from packageopt import * 
from statsmodels.regression import linear_model
from sklearn.metrics import mean_squared_error as mse


SECCODE = 'SBER'
DATE = 20190603
TIME = 114035000000
PATH_ABS = config.PATH_TO_SAVE_1
PATH_FROM_ABS = config.PATH_TO_SAVE_2
PATH_LOGS = config.PATH_INITIAL
DB_USER = config.USER
DB_PASSWORD = config.PASSWORD
DB_HOST = config.HOST
DB_PORT = config.PORT
DB_NAME = config.DB_NAME


def main(seccode, date, time):
    process = Main(
            user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT,
            dbname=DB_NAME, path_to_logs=PATH_LOGS)

    DIV = 10**6

    key = [date, seccode, time] 
    result = process.calculate(key)

    volume, costs = result.volume/DIV, result.costs

    y = costs
    X = np.stack([volume, volume**2, volume**3, volume**4, volume**5], axis=1)
    model_full_5 = linear_model.OLS(y, X)
    results_full_5 = model_full_5.fit()
    y_full_5 = results_full_5.predict(X)
    #mse_full_5 = '{:.2e}'.format(mse(y, y_full_5))
    mse_full_5 = '{:.2}'.format(mse(y/DIV, y_full_5/DIV))

    y = costs
    X = np.stack([volume, volume**2, volume**3, volume**4], axis=1)
    model_full_4 = linear_model.OLS(y, X)
    results_full_4 = model_full_4.fit()
    y_full_4 = results_full_4.predict(X)
    #mse_full_4 = '{:.2e}'.format(mse(y, y_full_4))
    mse_full_4 = '{:.2}'.format(mse(y/DIV, y_full_4/DIV))

    y = costs
    X = np.stack([volume, volume**2, volume**3], axis=1)
    model_full = linear_model.OLS(y, X)
    results_full = model_full.fit()
    y_full = results_full.predict(X)
    #mse_full = '{:.2e}'.format(mse(y, y_full))
    mse_full = '{:.2}'.format(mse(y/DIV, y_full/DIV))

    X = np.stack([volume, volume**2], axis=1)
    model_squared = linear_model.OLS(y, X)
    results_squared = model_squared.fit()
    y_squared = results_squared.predict(X)
    #mse_squared = '{:.2e}'.format(mse(y, y_squared))
    mse_squared = '{:.2}'.format(mse(y/DIV, y_squared/DIV))

    figure, ax = plt.subplots(1, 1, sharey=True)
    ax.plot(volume, costs/DIV, color='#000000')
    ax.ticklabel_format(axis='x', style='plain', scilimits=(0, 0))
    ax.ticklabel_format(axis='y', style='plain', scilimits=(0, 0))
    datetime = transpose_datetime(DATE, TIME)
    ax.title.set_text(SECCODE + ', ' + datetime)
    ax.set_ylabel('Трансакционные издержки,\n млн руб.')
    ax.set_xlabel('Объем исполнения, млн шт.')
    ax.grid(color='#DCDCDC')
    figure.set_size_inches(w=4, h=2.5)

    path_name = 'empirical_transaction_costs.pgf'
    path = os.path.join(PATH_ABS, PATH_FROM_ABS, path_name)
    plt.savefig(path, bbox_inches='tight')

    figure, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharey=True)
    ax3.title.set_text(SECCODE + ', ' + datetime)
    ax1.plot(volume, y/DIV, color='#C0C0C0')
    ax2.plot(volume, y/DIV, color='#C0C0C0')
    ax3.plot(volume, y/DIV, color='#C0C0C0')
    ax4.plot(volume, y/DIV, color='#C0C0C0')

    ax1.plot(volume, y_full_5/DIV, color='#000000')
    ax2.plot(volume, y_full_4/DIV, color='#000000')
    ax3.plot(volume, y_full/DIV, color='#000000')
    ax4.plot(volume, y_squared/DIV, color='#000000')

    ax4.set_xlabel('Объем исполнения, млн шт.')
    ax1.ticklabel_format(axis='x', style='plain', scilimits=(0, 0))
    ax2.ticklabel_format(axis='x', style='plain', scilimits=(0, 0))
    ax3.ticklabel_format(axis='x', style='plain', scilimits=(0, 0))
    ax4.ticklabel_format(axis='x', style='plain', scilimits=(0, 0))
    ax1.set_ylabel('Трансакционные\nиздержки,\n млн руб.')
    ax2.set_ylabel('Трансакционные\nиздержки,\nмлн руб.')
    ax3.set_ylabel('Трансакционные\nиздержки,\nмлн руб.')
    ax4.set_ylabel('Трансакционные\nиздержки,\nмлн руб.')
    ax1.legend(['эмпирическая функция', 
        r'$\beta_1v_t + \beta_2v_t^2 + \beta_3v_t^3 + \beta_4v_t^4+\beta_5v_t^5$' +\
                '\nMSE = ' + mse_full_5])
    ax2.legend(['эмпирическая функция', 
        r'$\beta_1v_t + \beta_2v_t^2 + \beta_3v_t^3 + \beta_4v_t^4$' +\
                '\nMSE = ' + mse_full_4])
    
    ax3.legend(['эмпирическая функция', 
        r'$\beta_1v_t + \beta_2v_t^2 + \beta_3v_t^3$' + '\nMSE = ' + mse_full])
    ax4.legend(['эмпирическая функция', 
        r'$\beta_1v_t + \beta_2v_t^2$' + '\nMSE = ' + mse_squared])
    
    ax1.grid(color='#DCDCDC')
    ax2.grid(color='#DCDCDC')
    ax3.grid(color='#DCDCDC')
    ax4.grid(color='#DCDCDC')

    figure.set_size_inches(w=5, h=6.5)
    plt.tight_layout(pad=0.4)
    
    path_name = 'parametrization_transaction_costs.pgf'
    path = os.path.join(PATH_ABS, PATH_FROM_ABS, path_name)
    plt.savefig(path, bbox_inches='tight')
    plt.show()

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

    def calculate(self, key):
        db = DataBase(dbname=self._dbname, user=self._user, password=self._password,
                host = self._host, port=self._port)
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
        
        tc_data = transactioncostssolver.calculate(key, return_data=True)

        return tc_data


if __name__ == '__main__':
    main(seccode=SECCODE, date=DATE, time=TIME)
