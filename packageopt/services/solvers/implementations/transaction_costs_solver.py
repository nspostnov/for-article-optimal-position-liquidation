import copy
import numpy as np
import pandas as pd
from ..abstract_base_classes.solver_abc import SolverABC
from ....models.transaction_costs import TransactionCosts
from statsmodels.regression import linear_model


__all__ = ['TransactionCostsSolver']
#DIVIDER = 10**6
DIVIDER = {
    'SBER':  10**6,
    'GAZP':  10**6,
    'LKOH':  10**3,
    'GMKN':  10**3,
    'ROSN':  10**6,
    'SBERP': 10**6,
    'ALRS':  10**6,
    'IRAO':  10**6,
    'TATN':  10**6,
    'VTBR':  10**9,
    'MGNT':  10**3,
}


class TransactionCostsSolver(SolverABC):
    def __init__(self, lobagent, priceagent, transactioncoststable):
        self._lobagent = lobagent
        self._priceagent = priceagent
        self._transactioncoststable = transactioncoststable

    def calculate(self, key, return_data=False):
        lob = self._lobagent.get(key).get_data()
        price = self._priceagent.get(key).get_data().price[0]

        lob_buy = lob.loc[lob.buysell == 'B', ['price', 'volume']].sort_values(
                by='price', ascending=False)
        lob_sell = lob.loc[lob.buysell == 'S', ['price', 'volume']].sort_values(
                by='price', ascending=True)

        tr_costs_sell = copy.copy(lob_buy)
        tr_costs_buy = copy.copy(lob_sell)

        tr_costs_sell['costs'] = np.cumsum(np.abs(tr_costs_sell.price - price) * 
                tr_costs_sell.volume)
        tr_costs_sell.volume = np.cumsum(tr_costs_sell.volume)

        tr_costs_buy['costs'] = np.cumsum(np.abs(tr_costs_buy.price - price) * 
                tr_costs_buy.volume)
        tr_costs_buy.volume = -np.cumsum(tr_costs_buy.volume)

        tr_costs = pd.concat((tr_costs_buy, tr_costs_sell)).sort_values(
                by='volume').reset_index(drop=True)
        tr_costs = tr_costs[['volume', 'costs']]
        if return_data:
            return tr_costs
        
        try:
            DIV = DIVIDER[key[1]]
        except KeyError:
            DIV = 1
        V = np.array(tr_costs.volume) / DIV
        costs = np.array(tr_costs.costs)

        y = costs
        X = np.stack([V, V**2, V**3, V**4], axis=1)

        model = linear_model.OLS(y, X)
        results = model.fit()
        
        params = np.array([results.params])
        covparams = results.cov_params()

        column_names = self._transactioncoststable.get_column_names()
        key_names = self._transactioncoststable.get_key()

        row = pd.DataFrame(columns=column_names)
        row[key_names[0]] = [key[0]]
        row[key_names[1]] = [key[1]]
        row[key_names[2]] = [key[2]]
        row['params'] = [params.tolist()]
        row['cov_params'] = [covparams.tolist()]

        transactioncosts = TransactionCosts()
        transactioncosts.set_key(key)
        transactioncosts.set_data(row)

        return transactioncosts
