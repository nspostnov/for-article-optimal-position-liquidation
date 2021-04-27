import pandas as pd
from ..abstract_base_classes.solver_abc import SolverABC
from ....models.daily_orders import DailyOrders


__all__ = ['DailyOrdersSolver']


class DailyOrdersSolver(SolverABC):
    def __init__(self, orderlogagent, orderlogtable, 
            dailyorderstable, db_connection):
        self._orderlogagent = orderlogagent
        self._table_name = orderlogtable.get_table_name()
        self._column_names = dailyorderstable.get_column_names()
        self._db_connection = db_connection

    def calculate(self, key):
        date, seccode = key
        if not self._orderlogagent.get(date):
            print('Something went wrong')

        query = '''
        SELECT "date", "seccode", count("no") as "orders", (max("price") + min("price")) / 2 as "av_price"
        FROM "{}"
        WHERE 
            "date" = {} AND 
            "seccode" = '{}' AND
            "time" >= 110000000000 AND 
            "time" <= 180000000000 AND
            "action" != 2
        GROUP BY
            "date",
            "seccode"
        '''.format(self._table_name, date, seccode)
        query = ' '.join(query.split())

        with self._db_connection as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            data = pd.DataFrame(cursor.fetchall(), columns=self._column_names)

        dailyorders = DailyOrders()
        dailyorders.set_key(key),
        dailyorders.set_data(data)

        return dailyorders
