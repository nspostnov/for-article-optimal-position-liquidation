__all__ = ['DataBase']


class DataBase:
    def __init__(self, dbname,
            user='postnov', password='password', host='localhost', port=5432):
        self._dbname = dbname
        self._user = user
        self._password = password
        self._host = host
        self._port = port

    def get_dbname(self):
        return self._dbname

    def set_dbname(self, name):
        self._dbname = name

    def get_user(self):
        return self._user

    def set_user(self, user):
        self._user = user

    def get_password(self):
        return self._password

    def set_password(self, password):
        self._password = password

    def get_host(self):
        return self._host

    def set_host(self, host):
        self._host = host

    def get_port(self):
        return self._port

    def set_port(self, port):
        self._port = port
