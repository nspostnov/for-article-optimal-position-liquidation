import pandas as pd
from ....models.time_ import Time
from ..abstract_base_classes.solver_abc import SolverABC
from ....models.traded_volume_from_to import TradedVolumeFromTo


__all__ = ['TradedVolumeFromToSolver']


class TradedVolumeFromToSolver(SolverABC):
    def __init__(self, orderlogagent, orderlogtable, tradedvolumefromtotable,
            db_connection, classtimegenerator):
        self._orderlogagent = orderlogagent
        self._table_name = orderlogtable.get_table_name()
        self._column_names = tradedvolumefromtotable.get_column_names()
        self._db_connection = db_connection
        self._classtimegenerator = classtimegenerator

    def calculate(self, key):
        date, seccode, time, time_interval = key
        
        time_initial = Time()
        time_initial.set_date(date)
        time_initial.set_time(time)
        generator = self._classtimegenerator
        times = generator(time_initial=time_initial,
                step_length=time_interval,
                num_steps=1,
                include_initial=True,
                direction='up').generate()
        lst_times = list(map(lambda x: x.get_time(), times))

        time_right = lst_times[-1]

        if not self._orderlogagent.get(date):
            print('Something went wrong')

        query = '''
        SELECT 
            {} as "date", '{}' as "seccode", {} as "time", {} as "time_interval",
            sum("price"*"volume") as "volume"
        FROM
            "{}"
        WHERE
            "date" = {} AND
            "seccode" = '{}' AND 
            "time" >= {} AND
            "time" <= {} AND
            "buysell" = 'S' AND
            "action" = 1
        '''.format(date, seccode, time, time_interval, self._table_name, date, seccode, time, time_right)
        query = ' '.join(query.split())

        with self._db_connection as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            data = pd.DataFrame(cursor.fetchall(), columns=self._column_names)

        tradedvolumefromto = TradedVolumeFromTo()
        tradedvolumefromto.set_key(key)
        tradedvolumefromto.set_data(data)

        return tradedvolumefromto
