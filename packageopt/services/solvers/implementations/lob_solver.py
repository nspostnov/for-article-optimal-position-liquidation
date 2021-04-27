import pandas as pd
from ..abstract_base_classes.solver_abc import SolverABC
from ....models.lob import LOB


__all__ = ['LOBSolver']


class LOBSolver(SolverABC):
    def __init__(self, orderlogagent, orderlogtable, lobtable, db_connection):
        self._orderlogagent = orderlogagent
        self._table_name = orderlogtable.get_table_name()
        self._column_names = lobtable.get_column_names()
        self._db_connection = db_connection

    def calculate(self, key):
        date, seccode, time = key
        if not self._orderlogagent.get([date, seccode]):
            print('Something went wrong')

        query = '''
        SELECT
            {} as "date",
            '{}' as "seccode",
            {} as "time",
            tt."price" as "price",
            tt."volume" as "volume",
            tt."buysell" as "buysell"
        FROM
            (SELECT
                t."buysell" as "buysell",
                t."price" as "price",
                SUM(t."volume") as "volume"
            FROM
                (SELECT 
                    "buysell", "orderno", "price",                   
                    CASE "action"
                        WHEN 1 THEN "volume"
                        WHEN 0 THEN -"volume"
                        WHEN 2 THEN -"volume"
                    END as "volume"
                FROM
                    "{}"
                WHERE
                    "date" = {} AND
                    "seccode" = '{}' AND
                    "time" <= {} AND
                    "price" != 0) t
            GROUP BY
                t."buysell",
                t."price") tt
        WHERE
            tt."volume" > 0
        ORDER BY
            tt."buysell" DESC,
            tt."price" DESC
        '''.format(
                date,
                seccode,
                time,
                self._table_name,
                date, 
                seccode,
                time)
        query = ' '.join(query.split())

        with self._db_connection as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            data = pd.DataFrame(cursor.fetchall(), columns=self._column_names)

        lob = LOB()
        lob.set_key(key)
        lob.set_data(data)

        return lob
