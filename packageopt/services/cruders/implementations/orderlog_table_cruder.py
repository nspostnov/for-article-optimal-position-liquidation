import os
import subprocess
from ..abstract_base_classes.table_cruder import TableCRUDer


__all__ = ['OrderLogTableCRUDer', 'OrderLogTableTruncatedCRUDer']


class OrderLogTableCRUDer(TableCRUDer):
    def __init__(self, orderlog_table, db_connection):
        self._db_connection = db_connection

        self._table_name = orderlog_table.get_table_name()
        self._column_names = orderlog_table.get_column_names()
        self._column_types = orderlog_table.get_column_types()
        self._primary_key = orderlog_table.get_primary_key()
        self._constraints = orderlog_table.get_constraints()

        self._key = orderlog_table.get_key()

    def get(self, obj):
        key = obj.get_key()
        if self.check_key(key):
            return True
        return False

    def update(self, obj, separator=',', null=''):
        key = obj.get_key()
        file_ = obj.get_data()

        query_index_check = '''
        SELECT EXISTS 
            (SELECT indexname 
                FROM pg_indexes 
            WHERE indexname = 'idx_{}_dateseccodetimeprice') 
        '''.format(self._table_name)
        query_index_check = ' '.join(query_index_check.split())
        with self._db_connection as connection:
            cursor = connection.cursor()
            cursor.execute(query_index_check)
            existance_index = cursor.fetchone()[0]

        if self.check_key(key):
            print('Orderlog with key: {} - is already filled'.format(key))
            file_.close()
            return
        if not self.check_existance():
            print('The table {} does not exist'.format(self._table_name))
            self.create()
            print('The table {} is created'.format(self._table_name))

        if not existance_index:
            query_index_create = '''
            CREATE INDEX "idx_{}_dateseccodetimeprice" 
                ON "{}" ("date", "seccode", "time", "price");
            '''.format(self._table_name, self._table_name)
            query_index_create = ' '.join(query_index_create.split())
            with self._db_connection as connection:
                cursor = connection.cursor()
                cursor.execute(query_index_create)
                connection.commit()

        path = file_.name
        path_tmp = os.path.join(os.path.split(path)[0], 'tmp.csv')

        script = '''
        awk -F, '{FS=","; OFS=","; $1 = $1 OFS (NR==1?"DATE":
        '''
        script = ' '.join(script.split()) + '"' + str(key) + '"'
        script = ' '.join(script.split()) + " )} NR>1'"
        script = script + ' {} > {}'.format(path, path_tmp)
        print(script)
        subprocess.run(script, shell=True)
        file_.close()

        with self._db_connection as connection:
            with open(path_tmp, 'r') as file_:
                cursor = connection.cursor()
                cursor.copy_from(file_, self._table_name, sep=separator, 
                        columns=self._column_names, null=null)
                connection.commit()


class OrderLogTableTruncatedCRUDer(TableCRUDer):
    def __init__(self, orderlog_table, parent_orderlog_table, db_connection):
        self._db_connection = db_connection

        self._table = orderlog_table
        self._table_name = orderlog_table.get_table_name()
        self._parent_table = parent_orderlog_table
        self._column_names = orderlog_table.get_column_names()
        self._column_types = orderlog_table.get_column_types()
        self._primary_key = orderlog_table.get_primary_key()
        self._constraints = orderlog_table.get_constraints()

        self._key = orderlog_table.get_key()

    def get(self, obj):
        key = obj.get_key()
        if self.check_key(key):
            return True
        return False

    def update(self, obj, separator=',', null=''):
        key = obj.get_key()
        parent_orderlog = obj.get_data()

        query_index_check = '''
        SELECT EXISTS 
            (SELECT indexname 
                FROM pg_indexes 
            WHERE indexname = 'idx_{}_dateseccodetimeprice') 
        '''.format(self._table_name)
        query_index_check = ' '.join(query_index_check.split())
        with self._db_connection as connection:
            cursor = connection.cursor()
            cursor.execute(query_index_check)
            existance_index = cursor.fetchone()[0]

        if self.check_key(key):
            print('Orderlog with key: {} - is already filled'.format(key))
            return
        if not self.check_existance():
            print('The table {} does not exist'.format(self._table_name))
            self.create()
            print('The table {} is created'.format(self._table_name))

        if not existance_index:
            query_index_create = '''
            CREATE INDEX "idx_{}_dateseccodetimeprice" 
                ON "{}" ("date", "seccode", "time", "price");
            '''.format(self._table_name, self._table_name)
            query_index_create = ' '.join(query_index_create.split())
            with self._db_connection as connection:
                cursor = connection.cursor()
                cursor.execute(query_index_create)
                connection.commit()

        parent_cruder = OrderLogTableCRUDer(self._parent_table, self._db_connection)
        parent_cruder.update(parent_orderlog)

        key_names = self._table.get_key()
        key_values = key

        conditions = list(
                map(lambda x: '"' + str(x[0]) + '"' + ' = ' + 
                    "'"*isinstance(x[1], str) + str(x[1]) + "'"*isinstance(x[1], str), 
                    zip(key_names, key_values)))
        conditions = ' AND '.join(conditions)

        query = '''
        INSERT INTO "{}"
        SELECT 
            * 
        FROM {}
        WHERE
            {}
        '''.format(self._table_name, self._parent_table.get_table_name(), conditions)

        with self._db_connection as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
