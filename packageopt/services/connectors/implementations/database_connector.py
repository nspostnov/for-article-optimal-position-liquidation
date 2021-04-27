from ..abstract_base_classes.database_connector_abc import DataBaseConnectorABC


__all__ = ['DataBaseConnector']


class DataBaseConnector(DataBaseConnectorABC):
    def __init__(self, database_cruder):
        self._dbcruder = database_cruder

        self._connection = None

    def connect(self):
        connection = self._dbcruder.connect()
        if connection is None:
            self._dbcruder.create()
            connection = self._dbcruder.connect()

        self._connection = connection
        return self._connection

    def close(self):
        if self._connection is not None:
            self._dbcruder.close()
            self._connection = None

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, value, traceback):
        self.close()
