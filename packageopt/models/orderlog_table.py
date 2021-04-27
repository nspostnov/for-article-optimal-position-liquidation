__all__ = ['OrderLogTable', 'OrderLogTruncatedTable']


class OrderLogTable:
    def __init__(self, date=None, seccode=None):
        self._column_names = ['no', 'date', 'seccode', 'buysell', 'time', 
                'orderno', 'action', 'price', 'volume', 'tradeno', 
                'tradeprice']
        self._column_types = ['bigint not null', 'bigint not null', 
                'varchar(20) not null', 'char(1) not null', 'bigint not null', 
                'bigint not null', 'smallint not null', 'double precision not null', 
                'bigint not null', 'bigint', 'double precision']
        self._primary_key = ['date', 'no']
        if date is not None and seccode is None:
            self._table_name = 'orderlog' + '_' + str(date)
        elif date is not None and seccode is not None:
            self._table_name = 'orderlog' + '_' + str(date) + '_' + str(seccode)
        else:
            self._table_name = 'orderlog'
        self._constraints = None
        self._key = 'date'

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


class OrderLogTruncatedTable:
    def __init__(self, date=None, seccode=None):
        self._column_names = ['no', 'date', 'seccode', 'buysell', 'time', 
                'orderno', 'action', 'price', 'volume', 'tradeno', 
                'tradeprice']
        self._column_types = ['bigint not null', 'bigint not null', 
                'varchar(20) not null', 'char(1) not null', 'bigint not null', 
                'bigint not null', 'smallint not null', 'double precision not null', 
                'bigint not null', 'bigint', 'double precision']
        self._primary_key = ['date', 'no']
        if date is not None and seccode is None:
            self._table_name = 'orderlog' + '_' + str(date)
        elif date is not None and seccode is not None:
            self._table_name = 'orderlog' + '_' + str(date) + '_' + str(seccode)
        else:
            self._table_name = 'orderlog'
 
        self._constraints = None
        self._key = ['date', 'seccode']

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
