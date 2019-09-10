from .CoIntCheckerBase import CoIntCheckerBase
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint


class CoIntCheckerEG(CoIntCheckerBase):
    def __init__(self, prices_a, prices_b):
        super().__init__(prices_a, prices_b)

    def check(self):
        _log_price_a = np.log(self._prices_a)
        _log_price_b = np.log(self._prices_b)

        independent = sm.add_constant(_log_price_a)
        ols_result = sm.OLS(_log_price_b, independent).fit()
        alpha, beta = ols_result.params

        rst = coint(_log_price_b, _log_price_a, maxlag=1, trend='c', autolag=None, return_results=False)
        self._p_value = rst[1]
        self._t_stats = rst[0]

        self._beta = beta
        self._spread = _log_price_b - beta * _log_price_a
