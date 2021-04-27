import numpy as np
import pandas as pd
from ..abstract_base_classes.solver_abc import SolverABC
from ....models.price import Price


__all__ = ['PriceSolver']


class PriceSolver(SolverABC):
    def __init__(self, lobagent, pricetable):
        self._lobagent = lobagent
        self._pricetable = pricetable

    def calculate(self, key):
        date, seccode, time = key
        lob = self._lobagent.get(key)
        if lob is None:
            print('Something went wrong')

        data = lob.get_data()
        data = data[['buysell', 'price', 'volume']]
        
        ask = np.min(data.loc[data.buysell == 'S', 'price'])
        bid = np.max(data.loc[data.buysell == 'B', 'price'])

        if np.isnan(ask) and not np.isnan(bid):
            price_point = [bid]
        elif not np.isnan(ask) and np.isnan(bid):
            price_point = [ask]
        elif not np.isnan(ask) and not np.isnan(bid):
            price_point = [(bid + ask) / 2]
        else:
            print('Calculation price. Something went wrong.')

        row = [key + price_point]
        row = pd.DataFrame(row, 
                columns=self._pricetable.get_column_names())

        price = Price()
        price.set_key(key)
        price.set_data(row)

        return price
