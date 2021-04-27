import pandas as pd
from abc import abstractmethod
from .table_cruder import TableCRUDer
from io import StringIO


__all__ = ['TableCRUDerDefault']


class TableCRUDerDefault(TableCRUDer):
    @abstractmethod
    def __init__(self, table, db_connection, modelclass):
        self._db_connection = db_connection

        self._table_name = table.get_table_name()
        self._column_names = table.get_column_names()
        self._column_types = table.get_column_types()
        self._primary_key = table.get_primary_key()
        self._constraints = table.get_constraints()

        self._key = table.get_key()
        self._class = modelclass

    def get(self, obj):
        key = obj.get_key()
        if not self.check_key(key):
            return None

        if not isinstance(self._key, (list, tuple)):
            key_names = [self._key]
        else:
            key_names = self._key

        if not isinstance(key, (list, tuple)):
            key_values = [key]
        else:
            key_values = key

        condition = list(
                map(lambda x: '"' + str(x[0]) + '"' + ' = ' + 
                    "'"*isinstance(x[1], str) + str(x[1]) + "'"*isinstance(x[1], str), 
                    zip(key_names, key_values)))
        condition = ' AND '.join(condition)

        query = '''
        SELECT * 
            FROM "{}"
                WHERE {}
        '''.format(self._table_name, condition)
        query = ' '.join(query.split())
        with self._db_connection as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            data = pd.DataFrame(cursor.fetchall(), 
                    columns=self._column_names)

        obj_return = self._class()
        obj_return.set_key(key)
        obj_return.set_data(data)

        return obj_return

    def update(self, obj, separator=',', null=''):
        key = obj.get_key()
        data = obj.get_data()
        if self.check_key(key):
            print('This key in the table {} already exist'.format(key))
            return
        if not self.check_existance():
            print('The table {} does not exist'.format(self._table_name))
            self.create()
            print('The table {} is created'.format(self._table_name))

        with StringIO() as file_:
            file_.write(data.to_csv(index=None, header=None, sep='\t',  float_format='%.15f'))
            file_.seek(0)
            tmp = file_.getvalue()
            tmp = tmp.replace('[', '{').replace(']', '}')
            file_.seek(0)
            file_.write(tmp)
            file_.seek(0)
            with self._db_connection as connection:
                cursor = connection.cursor()
                cursor.copy_from(file_, '"{}"'.format(self._table_name), sep='\t',
                        columns=self._column_names, null=null)
                connection.commit()
