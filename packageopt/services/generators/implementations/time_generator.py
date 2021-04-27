import numpy as np
from datetime import datetime, timedelta
from ..abstract_base_classes.generator_abc import GeneratorABC
from ....models.time_ import Time


__all__ = ['TimeGenerator']


class TimeGenerator(GeneratorABC):
    def __init__(self, time_initial, step_length, num_steps, include_initial, direction):
        self._time_initial = time_initial
        self._step_length = step_length
        self._num_steps = num_steps
        self._include_initial = include_initial
        self._direction = direction

    @staticmethod
    def _to_datetime(date, time):
        date_str = str(date)
        year = int(date_str[:4])
        month = int(date_str[4:6])
        day = int(date_str[6:])

        time_str = str(time)
        hours = int(time_str[:2])
        minutes = int(time_str[2:4])
        seconds = int(time_str[4:6])
        microseconds = int(time_str[6:])

        date_time = datetime(year, month, day, hours, 
                minutes, seconds, microseconds)

        return date_time

    @staticmethod
    def _to_initial_format(date_time):
        year = str(date_time.year)
        month = str(date_time.month)
        day = str(date_time.day)

        hours = str(date_time.hour)
        minutes = str(date_time.minute)
        seconds = str(date_time.second)
        microseconds = str(date_time.microsecond)

        date = year + month.zfill(2) + day.zfill(2)
        time = (hours.zfill(2) + minutes.zfill(2) + 
                seconds.zfill(2) + microseconds.zfill(6))

        return int(date), int(time)

    @staticmethod
    def _step_calculation(seconds):
        return seconds*(10**6)

    @staticmethod
    def _timedelta(step):
        return timedelta(microseconds=step)

    def generate(self):
        date = self._time_initial.get_date()
        time = self._time_initial.get_time()
        date_time = TimeGenerator._to_datetime(date, time)
        step = TimeGenerator._step_calculation(self._step_length)

        if self._direction == 'up':
            direction = 1
        elif self._direction == 'down':
            direction = -1
        else:
            raise ValueError('Direction must be set as \'up\' or \'down\'')

        lst = list(date_time + direction * np.cumsum(np.array(
            [TimeGenerator._timedelta(step)] * self._num_steps)))
        if self._include_initial:
            lst.append(date_time)
        lst.sort()

        def func_convertion(date_time):
            date, time = TimeGenerator._to_initial_format(date_time)
            time_object = Time()
            time_object.set_date(date)
            time_object.set_time(time)

            return time_object

        lst = list(map(func_convertion, lst))

        return lst
