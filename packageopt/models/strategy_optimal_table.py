__all__ = ['StrategyOptimalTable', 'StrategyOptimalTruncatedTable']


class StrategyOptimalTable:
    def __init__(self):
        self._column_names = ['date', 'seccode', 'time', 'step_vola_length', 
                'backward_num_steps', 'num_steps', 'step_length', 
                'volume_to_liquidate', 'lambda', 'strategy']
        self._column_types = ['bigint not null', 'varchar(20) not null', 
                'bigint not null', 'smallint not null', 'smallint not null', 
                'smallint not null', 'smallint not null', 'bigint not null', 
                'double precision not null', 'bigint[]']
        
        self._primary_key = ['date', 'seccode', 'time', 'step_vola_length', 
                'backward_num_steps', 'num_steps', 'step_length', 
                'volume_to_liquidate', 'lambda']
        self._table_name = 'strategyoptimal'
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


class StrategyOptimalTruncatedTable:
    def __init__(self, date=None, seccode=None):
        self._column_names = ['date', 'seccode', 'time', 'step_vola_length', 
                'backward_num_steps', 'num_steps', 'step_length', 
                'volume_to_liquidate', 'lambda', 'strategy']
        self._column_types = ['bigint not null', 'varchar(20) not null', 
                'bigint not null', 'smallint not null', 'smallint not null', 
                'smallint not null', 'smallint not null', 'bigint not null', 
                'double precision not null', 'bigint[]']
        
        self._primary_key = ['date', 'seccode', 'time', 'step_vola_length', 
                'backward_num_steps', 'num_steps', 'step_length', 
                'volume_to_liquidate', 'lambda']
        if date is None and seccode is None:
            self._table_name = 'strategyoptimal'
        elif date is not None and seccode is None:
            self._table_name = 'strategyoptimal' + '_' + str(date)
        elif date is not None and seccode is not None:
            self._table_name = 'strategyoptimal' + '_' + str(date) + '_' + str(seccode)
        else:
            raise ValueError('Strategy optimal table naming problem occured')
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
