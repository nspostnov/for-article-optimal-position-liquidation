__all__ = ['Time']


class Time:
    def __init__(self):
        self._date = None
        self._time = None

    def get_date(self):
        return self._date

    def set_date(self, date):
        if not isinstance(date, int):
            raise ValueError('Date must be in int format')
        self._date = date

    def get_time(self):
        return self._time

    def set_time(self, time):
        if not isinstance(time, int):
            raise ValueError('Time must be in int format')
        self._time = time
