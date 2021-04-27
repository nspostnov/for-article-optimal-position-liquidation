__all__ = ['StrategyOptimal']


class StrategyOptimal:
    def __init__(self):
        self._key = None
        self._data = None

    def get_key(self):
        return self._key

    def set_key(self, key):
        if not (isinstance(key[0], int) and 
                isinstance(key[1], str) and 
                isinstance(key[2], int) and

                isinstance(key[3], int) and
                isinstance(key[4], int) and
                isinstance(key[5], int) and
                isinstance(key[6], int) and
                isinstance(key[7], int) and 
                isinstance(key[8], (int, float))):
            error = 'You must set correct type for key of StrategyOptimal'
            raise ValueError(error)
        self._key = key

    def get_data(self):
        return self._data

    def set_data(self, data):
        self._data = data
