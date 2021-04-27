__all__ = ['LOB']


class LOB:
    def __init__(self):
        self._key = None
        self._data = None

    def get_key(self):
        return self._key

    def set_key(self, key):
        if not (isinstance(key[0], int) and 
                isinstance(key[1], str) and 
                isinstance(key[2], int)):
            error = 'The date-seccode-time key must be in int-str-int format'
            raise ValueError(error)
        self._key = key

    def get_data(self):
        return self._data

    def set_data(self, data):
        self._data = data
