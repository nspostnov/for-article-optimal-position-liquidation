__all__ = ['TradedVolumeFromToTable']


class TradedVolumeFromToTable:
    def __init__(self):
        self._column_names = ['date', 'seccode', 'time', 'time_interval', 'volume']
        self._column_types = ['bigint not null', 'varchar(20) not null', 
                'bigint not null', 'bigint not null',
                'double precision']
        self._primary_key = ['date', 'seccode', 'time', 'time_interval']
        self._table_name = 'tradedvolumefromto'
        self._constraints = None
        self._key = ['date', 'seccode', 'time', 'time_interval']

    def get_column_names(self):
        return self._column_names

    def set_column_names(self, names):
        self._column_names = names

    def get_column_types(self):
        return self._column_types

    def set_column_types(self, types):
        self._column_types = types

    def get_primary_key(self):
        return self._primary_key

    def set_primary_key(self, key):
        self._primary_key = key

    def get_table_name(self):
        return self._table_name

    def set_table_name(self, name):
        self._table_name = name

    def get_constraints(self):
        return self._constraints

    def set_constraints(self, params):
        self._constraints = params

    def get_key(self):
        return self._key

    def set_key(self, key):
        self._key = key
