__all__ = ['DailyActivity']


class DailyActivity:
    def __init__(self):
        self._key = None
        self._data = None

    def get_key(self):
        return self._key

    def set_key(self, key):
        if not (isinstance(key[0], int) and 
                isinstance(key[1], str)):
            error = 'The date-seccode key must be in int-str format'
            raise ValueError(error)
        self._key = key

    def get_data(self):
        return self._data

    def set_data(self, data):
        self._data = data
