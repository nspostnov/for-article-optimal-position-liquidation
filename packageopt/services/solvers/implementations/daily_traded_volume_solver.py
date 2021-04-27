import pandas as pd
from ..abstract_base_classes.solver_abc import SolverABC
from ....models.daily_traded_volume import DailyTradedVolume


__all__ = ['DailyTradedVolumeSolver']


class DailyTradedVolumeSolver(SolverABC):
    def __init__(self, orderlogagent, orderlogtable, 
            dailytradedvolumetable, db_connection):
        self._orderlogagent = orderlogagent
        self._table_name = orderlogtable.get_table_name()
        self._column_names = dailytradedvolumetable.get_column_names()
        self._db_connection = db_connection

    def calculate(self, key):
        date, seccode = key
        if not self._orderlogagent.get(date):
            print('Something went wrong')

        query = '''
        SELECT "date", "seccode", SUM("volume")
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

        dailytradedvolume = DailyTradedVolume()
        dailytradedvolume.set_key(key)
        dailytradedvolume.set_data(data)

        return dailytradedvolume
