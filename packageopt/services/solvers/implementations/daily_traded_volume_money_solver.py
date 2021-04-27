import pandas as pd
from ..abstract_base_classes.solver_abc import SolverABC
from ....models.daily_traded_volume_money import DailyTradedVolumeMoney


__all__ = ['DailyTradedVolumeMoneySolver']


class DailyTradedVolumeMoneySolver(SolverABC):
    def __init__(self, orderlogagent, orderlogtable, 
            dailytradedvolumemoneytable, db_connection):
        self._orderlogagent = orderlogagent
        self._table_name = orderlogtable.get_table_name()
        self._column_names = dailytradedvolumemoneytable.get_column_names()
        self._db_connection = db_connection

    def calculate(self, key):
        date, seccode = key
        if not self._orderlogagent.get(date):
            print('Something went wrong')

        query = '''
        SELECT "date", "seccode", SUM("volume" * "tradeprice")
        FROM "{}"
        WHERE 
            "date" = {} AND 
            "seccode" = '{}' AND 
            "action" = 2 AND 
            "buysell" = 'B'
        GROUP BY
            "date",
            "seccode"
        '''.format(self._table_name, date, seccode)
        query = ' '.join(query.split())

        with self._db_connection as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            data = pd.DataFrame(cursor.fetchall(), columns=self._column_names)

        dailytradedvolumemoney = DailyTradedVolumeMoney()
        dailytradedvolumemoney.set_key(key),
        dailytradedvolumemoney.set_data(data)

        return dailytradedvolumemoney
