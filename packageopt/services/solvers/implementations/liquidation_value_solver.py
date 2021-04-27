import copy
import numpy as np
import pandas as pd
from ..abstract_base_classes.solver_abc import SolverABC
from ....models.liquidation_value import LiquidationValue
from ....models.time_ import Time


__all__ = ['LiquidationValueSolver']


class LiquidationValueSolver(SolverABC):
    def __init__(self, lobagent, strategyoptimalagent, liquidationvaluetable, 
            classtimegenerator):
        self._lobagent = lobagent
        self._strategyoptimalagent = strategyoptimalagent
        self._liquidationvaluetable = liquidationvaluetable
        self._classtimegenerator = classtimegenerator

    @staticmethod
    def _calculation(strategy_liquidation, lobs):
        liquidation_values = []
        try:
            for step in range(len(strategy_liquidation)):
                liquidate_volume_onestep = strategy_liquidation[step]
                if liquidate_volume_onestep <= int(lobs[step].volume[0]):
                    liq_value = (liquidate_volume_onestep * 
                            float(lobs[step].price[0]))
                else:
                    tmp_lob = copy.deepcopy(lobs[step])
                    tmp_lob['volume_cum'] = np.cumsum(tmp_lob['volume'])
                    tmp_less = tmp_lob.loc[tmp_lob['volume_cum'] < 
                            liquidate_volume_onestep]
                    liq_value = np.sum(tmp_less['volume'] * tmp_less['price'])

                    price_more = tmp_lob.loc[tmp_lob['volume_cum'] >= 
                            liquidate_volume_onestep,
                            'price'].reset_index(drop=True)[0]
                    left_volume = liquidate_volume_onestep - np.sum(
                    tmp_less['volume'])
                    liq_value += price_more * left_volume

                liquidation_values.append(liq_value)
        except:
            print('Something went wrong')
            liquidation_values = np.nan

        return np.sum(liquidation_values)

    def calculate(self, key):
        date = key[0]
        seccode = key[1]
        time = key[2]
        step_vola_length = key[3]
        backward_num_steps = key[4]
        num_steps = key[5]
        step_length = key[6]
        volume_to_liquidate = key[7]	
        lam = key[8]

        optimal_strategy = np.array(self._strategyoptimalagent.get(key).get_data().strategy[0])
        
        equal_strategy = np.array([volume_to_liquidate / num_steps] * num_steps)
        equal_strategy = np.round(volume_to_liquidate - np.cumsum(equal_strategy), 0)
        equal_strategy = volume_to_liquidate - equal_strategy
        for j in range(len(equal_strategy) - 1, 0, -1):
            equal_strategy[j] = equal_strategy[j] - equal_strategy[j - 1]

        equal_strategy = np.array(list(map(int, equal_strategy)))

        time_initial = Time()
        time_initial.set_date(date)
        time_initial.set_time(time)

        generator = self._classtimegenerator
        times = generator(time_initial=time_initial,
                step_length=step_length, 
                num_steps=num_steps,
                include_initial=False,
                direction='up').generate()
        lst_times = list(map(lambda x: x.get_time(), times))
        keys = [[date, seccode, time_output] for time_output in lst_times]

        lobs = [self._lobagent.get(key_lob).get_data() for key_lob in keys]
        lobs = list(map(lambda x: (x.loc[x.buysell=='B']).sort_values(
            by='price', ascending=False).reset_index(drop=True), lobs))

        optimal_value = LiquidationValueSolver._calculation(optimal_strategy, lobs)
        equal_value = LiquidationValueSolver._calculation(equal_strategy, lobs)

        data = np.array([key + [optimal_value, equal_value]])
        data = pd.DataFrame(data, columns=self._liquidationvaluetable.get_column_names())
        liquidationvalue = LiquidationValue()
        liquidationvalue.set_key(key)
        liquidationvalue.set_data(data)

        return liquidationvalue
