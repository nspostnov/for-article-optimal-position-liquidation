import numpy as np
import pandas as pd 
from ..abstract_base_classes.solver_abc import SolverABC
from scipy.optimize import Bounds, LinearConstraint, basinhopping, minimize
from ....models.strategy_optimal import StrategyOptimal


__all__ = ['StrategyOptimalSolver']
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


class StrategyOptimalSolver(SolverABC):
    def __init__(self, volaagent, transactioncostsagent, strategyoptimaltable):
        self._volaagent = volaagent
        self._transactioncostsagent = transactioncostsagent
        self._strategyoptimaltable = strategyoptimaltable

    @staticmethod
    def _expected_costs(v, params):
        #return params[0] * v + params[1] * v**2
        return params[0] * v + params[1] * v**2 + params[2] * v**3 + params[3] * v**4

    @staticmethod
    def _expected_costs_d(v, params):
        #return params[0] + 2 * params[1] * v
        return params[0] + 2 * params[1] * v + 3 * params[2] * v**2 +\
                4 * params[3] * v**3

    @staticmethod
    def _expected_costs_dd(v, params):
        #return 2 * params[1]
        return 2 * params[1] + 6 * params[2] * v + 12 * params[3] * v**2

    @staticmethod
    def _var_costs(v, cov_params):
        var_b1 = cov_params[0, 0]
        var_b2 = cov_params[1, 1]
        var_b3 = cov_params[2, 2] # 
        var_b4 = cov_params[3, 3] # 
        cov_b1b2 = cov_params[0, 1]
        cov_b1b3 = cov_params[0, 2] # 
        cov_b1b4 = cov_params[0, 3] # 
        cov_b2b3 = cov_params[1, 2] #
        cov_b2b4 = cov_params[1, 3] # 
        cov_b3b4 = cov_params[2, 3] # 

        #var = v**2 * var_b1 + v**4 * var_b2 + 2 * cov_b1b2 * v**3
        var = v**2 * var_b1 + v**4 * var_b2 + v**6 * var_b3 + v**8 * var_b4 +\
                2*v**3 * cov_b1b2 + 2*v**4 * cov_b1b3 + 2*v**5 * cov_b1b4 +\
                2*v**5 * cov_b2b3 + 2*v**6 * cov_b2b4 + 2*v**7 * cov_b3b4

        return var

    @staticmethod
    def _var_costs_d(v, cov_params):
        var_b1 = cov_params[0, 0]
        var_b2 = cov_params[1, 1]
        var_b3 = cov_params[2, 2] # 
        var_b4 = cov_params[3, 3] # 
        cov_b1b2 = cov_params[0, 1]
        cov_b1b3 = cov_params[0, 2] # 
        cov_b1b4 = cov_params[0, 3] # 
        cov_b2b3 = cov_params[1, 2] #
        cov_b2b4 = cov_params[1, 3] # 
        cov_b3b4 = cov_params[2, 3] # 
    
        #var = 2 * v * var_b1 + 4 * v**3 * var_b2 + 6 * cov_b1b2 * v**2
        var = 2*v * var_b1 + 4*v**3 * var_b2 + 6*v**5 * var_b3 + 8*v**7 * var_b4 +\
                6*v**2 * cov_b1b2 + 8*v**3 * cov_b1b3 + 10*v**4 * cov_b1b4 +\
                10*v**4 * cov_b2b3 + 12*v**5 * cov_b2b4 + 14*v**6 * cov_b3b4
        
        return var

    @staticmethod
    def _var_costs_dd(v, cov_params):
        var_b1 = cov_params[0, 0]
        var_b2 = cov_params[1, 1]
        var_b3 = cov_params[2, 2] # 
        var_b4 = cov_params[3, 3] # 
        cov_b1b2 = cov_params[0, 1]
        cov_b1b3 = cov_params[0, 2] # 
        cov_b1b4 = cov_params[0, 3] # 
        cov_b2b3 = cov_params[1, 2] #
        cov_b2b4 = cov_params[1, 3] # 
        cov_b3b4 = cov_params[2, 3] # 

        #var = 2 * var_b1 + 12 * v**2 * var_b2 + 12 * cov_b1b2 * v
        var = 2 * var_b1 + 12*v**2 * var_b2 + 30*v**4 * var_b3 + 56*v**6 * var_b4 +\
                12*v * cov_b1b2 + 24*v**2 * cov_b1b3 + 40*v**3 * cov_b1b4 +\
                40*v**3 * cov_b2b3 + 60*v**4 * cov_b2b4 + 84*v**5 * cov_b3b4

        return var

    def calculate(self, key):
        date = key[0]
        seccode = key[1]
        time = key[2]
        step_vola_length = key[3]	
        backward_num_steps = key[4]
        num_steps = key[5]
        step_length = key[6]
        try:
            DIV = DIVIDER[seccode]
        except KeyError:
            DIV = 1
        volume_to_liquidate = key[7] / DIV
        lam = key[8]

        key_tc = [date, seccode, time]
        key_vola = [date, seccode, time, step_vola_length, backward_num_steps, 
                num_steps, step_length]

        transactioncosts = self._transactioncostsagent.get(key_tc)
        vola = self._volaagent.get(key_vola)

        tc_params = np.array(transactioncosts.get_data().params[0][0])
        tc_covparams = np.array(transactioncosts.get_data().cov_params[0])
        vola_estimates = np.array(vola.get_data().vola_estimates[0]) *\
                DIV**2

        atol = 0.000000000001

        x0 = np.array([volume_to_liquidate / num_steps] * num_steps)
        bounds = Bounds(0, volume_to_liquidate, keep_feasible=True)
        linear_constraint = LinearConstraint([[1] * num_steps], 
                [volume_to_liquidate - atol], [volume_to_liquidate + atol], keep_feasible=True)

        print(np.sum(x0))
        print(volume_to_liquidate - atol, volume_to_liquidate + atol)

        V = volume_to_liquidate
        s2 = vola_estimates

        def functional(v):
            v2_new = np.cumsum(v[::-1])[::-1] ** 2
            square = np.sqrt(np.sum(s2 * v2_new) + 
                    np.sum(self._var_costs(v, tc_covparams)))
            first = lam * square 
            second = np.sum(self._expected_costs(v, tc_params))
            func = first + second
            
            return func

        def functional_jac(v):
            coeff = lam / 2
            v_new = np.cumsum(v[::-1])[::-1]
            v2_new = v_new ** 2
            denumerator = np.sqrt(np.sum(s2 * v2_new) + 
                    np.sum(self._var_costs(v, tc_covparams)))
            jac = np.empty(shape=len(v))
            for i in range(len(v)):
                v_i = v[i]
                sl = (s2 * v_new)[:i+1]
                numerator_i = (self._var_costs_dd(v_i, tc_covparams) + 2 * np.sum(sl))
                additional_i = self._expected_costs_d(v_i, tc_params)
                jac_i = coeff * numerator_i / denumerator + additional_i
                jac[i] = jac_i

            return jac

        def functional_hess(v):
            coeff = lam / 2
            v_new = np.cumsum(v[::-1])[::-1]
            v2_new = v_new**2
            g = (np.sqrt(np.sum(s2 * v2_new) + 
                np.sum(self._var_costs(v, tc_covparams))))
            hess = np.zeros(shape=(len(v), len(v)))
            for i in range(len(v)):
                for j in range(len(v)):
                    f_i = (self._var_costs_d(v[i], tc_covparams) + 
                            2 * np.sum((s2 * v_new)[:i]))
                    f_ij = (self._var_costs_dd(v[j], tc_covparams) * (i == j) +
                            2 * np.sum(s2[:np.min([i, j])]))
                    g_j = (0.5 * (self._var_costs_d(v[j], tc_covparams) + 
                        2 * np.sum((s2 * v_new)[:j])) / np.sqrt(np.sum(s2 * v2_new) + 
                            np.sum(self._var_costs(v, tc_covparams))))
                    brackets = f_ij * g - g_j * f_i
                    hess_ij = (coeff * brackets / g**2 +
                            self._expected_costs_dd(v[j], tc_params) * (i == j))
                    hess[i, j] = hess_ij

            return hess

        minimizer_kwargs = {
                'method': 'trust-constr',
                'jac': functional_jac,
                'hess': functional_hess,
                'constraints':[linear_constraint],
                'bounds': bounds}

        #result = basinhopping(functional, x0, minimizer_kwargs=minimizer_kwargs)
        result = minimize(functional, x0, method='trust-constr', jac=functional_jac,
                hess=functional_hess, constraints=minimizer_kwargs['constraints'], 
                bounds=minimizer_kwargs['bounds'])

        print(result)

        strategy = result.x * DIV

        strategy_left = np.round(key[7] - np.cumsum(strategy), 0)
        strategy = key[7] - strategy_left
        for j in range(len(strategy) - 1, 0, -1):
            strategy[j] = strategy[j] - strategy[j - 1]
        
        strategy = np.array(list(map(int, strategy)))

        row = pd.DataFrame(columns=self._strategyoptimaltable.get_column_names())
        key_names = self._strategyoptimaltable.get_key()

        row[key_names[0]] = [key[0]]
        row[key_names[1]] = [key[1]]
        row[key_names[2]] = [key[2]]
        row[key_names[3]] = [key[3]]
        row[key_names[4]] = [key[4]]
        row[key_names[5]] = [key[5]]
        row[key_names[6]] = [key[6]]
        row[key_names[7]] = [key[7]]
        row[key_names[8]] = [key[8]]
        row['strategy'] = [strategy.tolist()]

        optimal_strategy = StrategyOptimal()
        optimal_strategy.set_key(key)
        optimal_strategy.set_data(row)

        return optimal_strategy
