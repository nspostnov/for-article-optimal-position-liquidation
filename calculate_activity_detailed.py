'''This script calculates the money order volume (action = 1) for time in (t1, t2)
(for the time of liquidation)
'''
import config

from packageopt import * 


HYPERPARAMS = {
        'USER': config.USER, # the user of database
        'PASSWORD': config.PASSWORD, # the password from user 
        'HOST': config.HOST, # the host for connection
        'PORT': config.PORT, # the port of server
        'DB_NAME': config.DB_NAME, # the name of database to create and work with
        'PATH_INITIAL': config.PATH_INITIAL, # the path to initial .txt files with orderlogs
        'SECCODES': ['SBER', 'VTBR', 
            'GAZP', 'LKOH', 'GMKN', 'ROSN', 'SBERP',
            'ALRS', 'IRAO', 'TATN', 'MGNT'], # the seccodes of top traded equities
        'DATES': [20190603, 20190604, 20190605, 20190606, 20190607, 
            20190610, 20190611, 20190613, 20190614, 20190617, 
            20190618, 20190619, 20190620, 20190621, 20190624, 
            20190625, 20190626, 20190627, 20190628], # list of dates
        'TIME_INTERVAL_LIQUIDATION': 600, # time interval of one liquidation process
        'TIME_INITIAL': 110000000000, # the time for start
        'TIME_END': 180000000000, # the time for end
        'STEP_TIME_CHANGE': 300, # time between liquidations
        'NUM_STEPS': 12*7, # number of steps of changing times 
        }


def main():
    process = Main(
        HYPERPARAMS['USER'], 
        HYPERPARAMS['PASSWORD'], 
        HYPERPARAMS['HOST'], 
        HYPERPARAMS['PORT'],
        HYPERPARAMS['DB_NAME'], 
        HYPERPARAMS['PATH_INITIAL'], 
        HYPERPARAMS['SECCODES'], 
        HYPERPARAMS['DATES'],
        HYPERPARAMS['TIME_INTERVAL_LIQUIDATION'],
        HYPERPARAMS['TIME_INITIAL'], 
        HYPERPARAMS['TIME_END'],
        HYPERPARAMS['STEP_TIME_CHANGE'],
        HYPERPARAMS['NUM_STEPS'])
    process.run()


class Main:
    def __init__(self, user, password, host, port, dbname, path_to_logs, seccodes, 
            dates, time_interval, time_start, time_end, step_length, num_steps):
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._dbname = dbname
        self._path = path_to_logs
        self._seccodes = seccodes
        self._dates = dates
        self._time_interval = time_interval
        self._time_start = time_start
        self._time_end = time_end
        self._step_length = step_length
        self._num_steps = num_steps

    def _calculate(self, key):
        db = DataBase(dbname=self._dbname, user=self._user, password=self._password,
                host=self._host, port=self._port)
        dbcruder = DataBaseCRUDer(db)
        connector = DataBaseConnector(dbcruder)

        orderlogtable = OrderLogTable()
        orderlogtablecruder = OrderLogTableCRUDer(orderlogtable, connector)
        orderlogrepo = OrderLogRepo(orderlogtablecruder)
        orderlogsolver = OrderLogSolver(self._path)
        orderlogagent = OrderLogAgent(orderlogrepo, orderlogsolver)

        tradedvolumefromtotable = TradedVolumeFromToTable()
        tradedvolumefromtotablecruder = TradedVolumeFromToTableCRUDer(
                tradedvolumefromtotable, connector) 
        tradedvolumefromtorepo = TradedVolumeFromToRepo(tradedvolumefromtotablecruder)
        tradedvolumefromtosolver = TradedVolumeFromToSolver(
                orderlogagent, orderlogtable, tradedvolumefromtotable, connector, 
                TimeGenerator)
        tradedvolumefromtoagent = TradedVolumeFromToAgent(
                tradedvolumefromtorepo, tradedvolumefromtosolver)

        return tradedvolumefromtoagent.get(key)

    def _key_creation(self):
        dates = self._dates
        seccodes = self._seccodes
        time_interval = self._time_interval

        time_start = self._time_start
        time_end = self._time_end
        step_length = self._step_length
        num_steps = self._num_steps

        time_initial = Time()
        time_initial.set_date(dates[0])
        time_initial.set_time(time_start)

        times = TimeGenerator(time_initial, 
                step_length, num_steps, include_initial=True, 
                direction='up').generate()
        times = list(map(lambda x: x.get_time(), times))

        keys = []
        for date in dates:
            for seccode in seccodes:
                for time in times:
                    keys.append([date, seccode, time, time_interval])
        return keys

    def run(self):
        keys = self._key_creation()
        for key in keys:
            print(key)
            self._calculate(key)


if __name__ == '__main__':
    main()
