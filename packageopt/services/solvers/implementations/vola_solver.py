import numpy as np
import pandas as pd
#import pyflux as pf
import arch as pf
from ..abstract_base_classes import SolverABC
from ....models.time_ import Time
from ....models.vola import Vola


__all__ = ['VolaSolver']


class VolaSolver(SolverABC):
    def __init__(self, volatable, priceagent, classtimegenerator):
        self._volatable = volatable
        self._priceagent = priceagent
        self._classtimegenerator = classtimegenerator

    def calculate(self, key):
        date = key[0]
        seccode = key[1]
        time = key[2]
        step_vola_length = key[3]
        backward_num_steps = key[4]
        num_steps = key[5]
        step_length = key[6]

        time_initial = Time()
        time_initial.set_date(date)
        time_initial.set_time(time)

        generator = self._classtimegenerator
        times = generator(time_initial=time_initial, 
                step_length=step_vola_length, 
                num_steps=backward_num_steps, 
                include_initial=True, 
                direction='down').generate()

        lst_times = list(map(lambda x: x.get_time(), times))
        keys = [[date, seccode, time_output] for time_output in lst_times]
        prices = [self._priceagent.get(key).get_data() for key in keys]
        price_table = pd.concat(prices).reset_index(drop=True)
        
        price = price_table.price
        dprice = np.log(price) - np.log(price.shift(1))
        dprice = pd.DataFrame(dprice.dropna().reset_index(drop=True))

        #model = pf.GARCH(dprice, p=1, q=1)
        #model.fit()
        a = 1
        b = 950
        drift = np.float64(a - np.min(dprice) * 
                (b - a) / (np.max(dprice) - np.min(dprice)))
        scale = np.float64((b - a) / (np.max(dprice) - np.min(dprice)))
        dprice_adj = drift + dprice * scale

        model = pf.arch_model(dprice_adj, p=1, q=1)
        fitted = model.fit()


        time_multiplier = int(step_length / step_vola_length)
        if np.abs(time_multiplier - step_length/step_vola_length) > 0.0000000001:
            error = 'Liquidation step length can not be divided on vola length'
            raise ValueError(error)
        #forecast_initial = model.predict(h=num_steps*time_multiplier)
        forecast_initial = np.array(fitted.forecast(
            horizon=num_steps*time_multiplier).variance.dropna())[0]
        
        forecast_initial = forecast_initial / scale**2
        
        j = 0 
        forecast_for_liquidation = []
        while j < len(forecast_initial):
            forecast_for_liquidation.append(np.sum(forecast_initial[j:j+time_multiplier]))
            j += time_multiplier


        #forecast_for_liquidation = np.array(forecast_for_liquidation).transpose()[0]
        forecast_for_liquidation = np.array(forecast_for_liquidation)

        column_names = self._volatable.get_column_names()
        key_names = self._volatable.get_key()

        row = pd.DataFrame(columns=column_names)
        row[key_names[0]] = [key[0]]
        row[key_names[1]] = [key[1]]
        row[key_names[2]] = [key[2]]
        row[key_names[3]] = [key[3]]
        row[key_names[4]] = [key[4]]
        row[key_names[5]] = [key[5]]
        row[key_names[6]] = [key[6]]
        row['vola_estimates'] = [forecast_for_liquidation.tolist()]


        vola = Vola()
        vola.set_key(key)
        vola.set_data(row)

        return vola
