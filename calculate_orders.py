'''This script calculates the number of daily orders (action = 1, 0)
'''
import contextlib
import config
from packageopt import * 


PATH_DATES = config.PATH_DATES_FILE
PATH_SECCODES = config.PATH_SECCODES_FILE
PATH_LOGS = config.PATH_INITIAL
DB_USER = config.USER
DB_PASSWORD = config.PASSWORD
DB_HOST = config.HOST
DB_PORT = config.PORT
DB_NAME = config.DB_NAME


def main():
    code_main = Main(
            user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT, 
            dbname=DB_NAME, path_to_logs=PATH_LOGS)
    
    dates = list(map(lambda x: int(x.rstrip()), 
        open(PATH_DATES, 'r').readlines()))
    seccodes = list(map(lambda x: x.rstrip(), 
        open(PATH_SECCODES, 'r').readlines()))

    keys = list(map(lambda x: list(zip(dates, [x] * len(dates))), seccodes))
    keys = list(map(list, [item for sublist in keys for item in sublist]))

    num = 1
    for key in keys:
        print([num] + key)
        num += 1
        code_main.calculate(key)


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

        orderlogtable = OrderLogTable()
        orderlogtablecruder = OrderLogTableCRUDer(orderlogtable, connector)
        orderlogrepo = OrderLogRepo(orderlogtablecruder)
        orderlogsolver =OrderLogSolver(self._path)
        orderlogagent = OrderLogAgent(orderlogrepo, orderlogsolver)

        dailyorderstable = DailyOrdersTable()
        dailyorderstablecruder = DailyOrdersTableCRUDer(
                dailyorderstable, connector)
        dailyordersrepo = DailyOrdersRepo(
                dailyorderstablecruder)
        dailyorderssolver = DailyOrdersSolver(
                orderlogagent, orderlogtable, dailyorderstable, 
                connector)
        dailyordersagent = DailyOrdersAgent(
                dailyordersrepo, dailyorderssolver)

        return dailyordersagent.get(key)


if __name__ == '__main__':
    main()
