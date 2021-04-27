from abc import abstractmethod
from .table_cruder_abc import TableCRUDerABC


__all__ = ['TableCRUDer']


class TableCRUDer(TableCRUDerABC):
    def check_existance(self):
        query = '''
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_name = '{}' AND
            table_schema = 'public'
        )
        '''.format(self._table_name)
        query = ' '.join(query.split())
        with self._db_connection as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            existance = cursor.fetchone()[0]

        return existance

    def create(self):
        if self.check_existance():
            print('Table {} already exists'.format(self._table_name))
            return

        query = '''
        CREATE TABLE "{}"."{}" (
        '''.format('public', self._table_name)
        query_all_columns = ''
        for j in range(len(self._column_names)):
            query_all_columns += '''
            "{}" {},
            '''.format(self._column_names[j], self._column_types[j])
            query_all_columns += '\n'
        query += query_all_columns

        if isinstance(self._primary_key, list):
            p_key = list(map(lambda x: '"' + x + '"', self._primary_key))
            p_key = ','.join(p_key)
        else:
            p_key = '"' + self._primary_key + '"'
        query += '''
        PRIMARY KEY ({})
        '''.format(p_key)

        if self._constraints is not None:
            constraint_name = self._constraints[0]
            foreign_key = self._constraints[1]
            references = self._constraints[2]

            query_constraint = '''
            , \n
            CONSTRAINT {}
                FOREIGN KEY ({})
                    REFERENCES {}
            '''.format(constraint_name, foreign_key, references)
        else:
            query_constraint = ''
        query += query_constraint
        
        query += ');'
        query = ' '.join(query.split())

        with self._db_connection as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
        print('Table {} created'.format(self._table_name))

    def delete(self):
        if not self.check_existance():
            print('Table {} does not exist'.format(self._table_name))
            return

        query = 'DROP TABLE "{}"'.format(self._table_name)
        with self._db_connection as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
        print('Table {} is deleted'.format(self._table_name))

    def check_key(self, key):
        if not self.check_existance():
            print('Table {} does not exist'.format(self._table_name))
            return False

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
                    "'"*isinstance(x[1], str) +  str(x[1]) + "'"*isinstance(x[1], str), 
                    zip(key_names, key_values)))
        condition = ' AND '.join(condition)

        query = '''
        SELECT EXISTS (
            SELECT 1 FROM "{}"
                WHERE {}
        )
        '''.format(self._table_name, condition)
        query = ' '.join(query.split())
        with self._db_connection as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            existance = cursor.fetchone()[0]

        return existance

    @abstractmethod
    def update(self, obj, separator, null):
        pass

    @abstractmethod
    def get(self, obj):
        pass
