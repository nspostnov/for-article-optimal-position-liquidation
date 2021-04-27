__all__ = ['LiquidationValueTable', 'LiquidationValueTruncatedTable']


class LiquidationValueTable:
    def __init__(self):
        self._column_names = ['date', 'seccode', 'time', 'step_vola_length', 
                'backward_num_steps', 'num_steps', 'step_length', 
                'volume_to_liquidate', 'lambda', 'optimal', 'equal']
        self._column_types = ['bigint not null', 'varchar(20) not null', 
                'bigint not null', 'smallint not null', 'smallint not null', 
                'smallint not null', 'smallint not null', 'bigint not null', 
                'double precision not null', 'double precision', 'double precision']
        
        self._primary_key = ['date', 'seccode', 'time', 'step_vola_length', 
                'backward_num_steps', 'num_steps', 'step_length', 
                'volume_to_liquidate', 'lambda']
        self._table_name = 'liquidationvalue'
        self._constraints = None
        
        self._key = ['date', 'seccode', 'time', 'step_vola_length', 
                'backward_num_steps', 'num_steps', 'step_length', 
                'volume_to_liquidate', 'lambda']

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


class LiquidationValueTruncatedTable:
    def __init__(self, date=None, seccode=None):
        self._column_names = ['date', 'seccode', 'time', 'step_vola_length', 
                'backward_num_steps', 'num_steps', 'step_length', 
                'volume_to_liquidate', 'lambda', 'optimal', 'equal']
        self._column_types = ['bigint not null', 'varchar(20) not null', 
                'bigint not null', 'smallint not null', 'smallint not null', 
                'smallint not null', 'smallint not null', 'bigint not null', 
                'double precision not null', 'double precision', 'double precision']
        
        self._primary_key = ['date', 'seccode', 'time', 'step_vola_length', 
                'backward_num_steps', 'num_steps', 'step_length', 
                'volume_to_liquidate', 'lambda']
        if date is None and seccode is None:
            self._table_name = 'liquidationvalue'
        elif date is not None and seccode is None:
            self._table_name = 'liquidationvalue' + '_' + str(date)
        elif date is not None and seccode is not None:
            self._table_name = 'liquidationvalue' + '_' + str(date) + '_' + str(seccode)
        else:
            raise ValueError('Liquidation value table naming, something went wrong')

        self._constraints = None
        
        self._key = ['date', 'seccode', 'time', 'step_vola_length', 
                'backward_num_steps', 'num_steps', 'step_length', 
                'volume_to_liquidate', 'lambda']

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
