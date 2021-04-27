import psycopg2
from ..abstract_base_classes.database_cruder_abc import DataBaseCRUDerABC
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


__all__ = ['DataBaseCRUDer']


class DataBaseCRUDer(DataBaseCRUDerABC):
    def __init__(self, database):
        self._user = database.get_user()
        self._password = database.get_password()
        self._host = database.get_host()
        self._port = database.get_port()
        self._dbname = database.get_dbname()

        self._connection = None

    def check_existance(self):
        query = 'SELECT datname FROM pg_database'
        with psycopg2.connect(
                user=self._user, 
                password=self._password, 
                host=self._host,
                port=self._port,
                dbname='postgres') as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            lst_databases = cursor.fetchall()
        
        if (self._dbname, ) in lst_databases:
            return True
        else:
            return False

    def create(self):
        query = '''
        CREATE DATABASE "{}" WITH OWNER = {} TEMPLATE = template0
            ENCODING = UTF8
        '''.format(self._dbname, self._user)
        query = ' '.join(query.split())

        existance = self.check_existance()
        if existance:
            print('Database {} already exists'.format(self._dbname))
        else:
            print('Creation database {}'.format(self._dbname))
            with psycopg2.connect(
                    user=self._user, 
                    password=self._password,
                    host=self._host,
                    port=self._port,
                    dbname='postgres') as connection:
                connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                cursor = connection.cursor()
                cursor.execute(query)
                connection.commit()
                print('Database {} is created'.format(self._dbname))

    def delete(self):
        existance = self.check_existance()
        if not existance:
            print('Database {} does not exist'.format(self._dbname))
            return

        query_drop = 'DROP DATABASE {}'.format(self._dbname)
        query_drop_connections = '''
            SELECT pg_terminate_backend(pid) from pg_stat_activity WHERE
                datname = '{}'
        '''.format(self._dbname)
        query_drop_connections = ' '.join(query_drop_connections.split())

        with psycopg2.connect(
                user=self._user, 
                password=self._password,
                host=self._host,
                port=self._port,
                dbname='postgres') as connection:
            
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = connection.cursor()
            cursor.execute(query_drop_connections)
            connection.commit()
            self._connection = None

            cursor.execute(query_drop)
            connection.commit()
            print('Database {} is deleted'.format(self._dbname))

    def connect(self):
        existance = self.check_existance()
        if not existance:
            print('There is no database {}'.format(self._dbname))
            return self._connection 

        if self._connection is None:
            self._connection = psycopg2.connect(
                    user=self._user,
                    password=self._password,
                    dbname=self._dbname,
                    host=self._host,
                    port=self._port)

        return self._connection
        
    def close(self):
        if self._connection is not None:
            self._connection.close()
            self._connection = None
        else:
            print('There is no connection to close')
    
    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, value, traceback):
        self.close()
