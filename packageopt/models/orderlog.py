__all__ = ['OrderLog', 'OrderLogTruncated']


class OrderLog:
    def __init__(self):
        self._key = None
        self._data = None

    def get_key(self):
        return self._key

    def set_key(self, key):
        if not isinstance(key, int):
            raise ValueError('Date must be in int format')
        self._key = key

    def get_data(self):
        return self._data

    def set_data(self, data):
        self._data = data


class OrderLogTruncated:
    def __init__(self):
        self._key = None
        self._data = None

    def get_key(self):
        return self._key

    def set_key(self, key):
        if not isinstance(key, list):
            raise ValueError('OrderLogTruncated has a key of list type!')
        if not len(key) == 2:
            raise ValueError('The length of key for OrderLogTruncated must be equal to 2')
        if not isinstance(key[0], int) or not isinstance(key[1], str):
            raise ValueError('First key part must be int (date), the second must be str (seccode)')
        self._key = key

    def get_data(self):
        return self._data

    def set_data(self, data):
        self._data = data
