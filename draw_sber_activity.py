import matplotlib.pyplot as plt
import pandas as pd
import os 
import config

from psycopg2 import connect as cnct 
from datetime import datetime as dt
from packageopt import *


PATH_ABS = config.PATH_TO_SAVE_1
PATH_FROM_ABS = config.PATH_TO_SAVE_2
SECCODE = 'SBER'

HYPERPARAMS = {
        'DATE_INITIAL': 20190603, # initial date of start calculation
        'TIME_INITIAL': 110000000000, # initial time of start calculation 
        'USER': config.USER, # the user of database
        'PASSWORD': config.PASSWORD, # the password from user 
        'HOST': config.HOST, # the host for connection
        'PORT': config.PORT, # the port of server
        'DB_NAME': config.DB_NAME, # the name of database to create and work with
        'PATH_INITIAL': config.PATH_INITIAL, # the path to initial .txt files with orderlogs
        'DATES': [20190603, 20190604, 20190605, 20190607, 20190610, 20190611, 20190613, 20190614, 
            20190617, 20190618, 20190619, 20190620, 20190621, 20190624, 20190625, 20190626, 20190627, 
            20190628]
        }

DIV = 10**9

if DIV == 10**6:
    TEXT_DIV = 'млн'
elif DIV == 10**3:
    TEXT_DIV = 'тыс.'
elif DIV == 10**9:
    TEXT_DIV = 'млрд'
else:
    TEXT_DIV = ''


def main():
    ticker = SECCODE
    Main(
        HYPERPARAMS['USER'], 
        HYPERPARAMS['PASSWORD'], 
        HYPERPARAMS['HOST'], 
        HYPERPARAMS['PORT'],
        HYPERPARAMS['DB_NAME'], 
        HYPERPARAMS['PATH_INITIAL']).run()

    data = data_get(ticker)

    figure, ax = plt.subplots(1, 1, sharey=False)
    ax.plot(data['date'], data['volume'] / DIV, color='#000000')
    ax.title.set_text(ticker)
    ax.set_ylabel('Объем торгов, ' + TEXT_DIV + ' руб.')
    ax.set_xlabel('Дата')

    figure.autofmt_xdate()
    figure.set_size_inches(w=5, h=4)
    path_name = 'sber_activity.pgf'
    path = os.path.join(PATH_ABS, PATH_FROM_ABS, path_name)

    plt.savefig(path, bbox_inches='tight')
    plt.show()


class Main:
    def __init__(self, user, password, host, port, dbname, path_to_logs):
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._dbname = dbname
        self._path = path_to_logs

    def _calculate_key(self):
        date_initial = HYPERPARAMS['DATE_INITIAL']
        time_initial = HYPERPARAMS['TIME_INITIAL']
        dates = HYPERPARAMS['DATES']

        seccode = SECCODE
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
           
            dailytradedvolumemoneytable = DailyTradedVolumeMoneyTable()
            dailytradedvolumemoneytablecruder = DailyTradedVolumeMoneyTableCRUDer(
                    dailytradedvolumemoneytable, connector)
            dailytradedvolumemoneyrepo = DailyTradedVolumeMoneyRepo(
                    dailytradedvolumemoneytablecruder)
            dailytradedvolumemoneysolver = DailyTradedVolumeMoneySolver(
                    orderlogagent, orderlogtable, dailytradedvolumemoneytable, 
                    connector)
            dailytradedvolumemoneyagent = DailyTradedVolumeMoneyAgent(
                    dailytradedvolumemoneyrepo, dailytradedvolumemoneysolver)

            dailytradedvolumemoneyagent.get([date, seccode])


    def run(self):
        self._calculate_key()


def data_get(seccode):
    with cnct(
            dbname=HYPERPARAMS['DB_NAME'], 
            host=HYPERPARAMS['HOST'], 
            user=HYPERPARAMS['USER'], 
            password=HYPERPARAMS['PASSWORD'], 
            port=HYPERPARAMS['PORT']) as connect:
        cursor = connect.cursor()
        query = f'''
        SELECT date, volume
        FROM 
            dailytradedvolumemoney
        WHERE
            seccode = '{seccode}'
        ORDER BY 
            date
        '''
        query = ' '.join(query.split())
        cursor.execute(query)
        data = pd.DataFrame(cursor.fetchall(), columns=['date', 'volume'])

    data['date'] = list(map(lambda x: datetime_convert(x), data['date']))

    return data


def datetime_convert(date):
    date_str = str(date)

    year = int(date_str[:4])
    month = int(date_str[4:6])
    day = int(date_str[6:])

    datetime = dt(year=year, month=month, day=day)

    return datetime


if __name__ == '__main__':
    main()
