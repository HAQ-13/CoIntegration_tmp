from .CoIntCheckerBase import CoIntCheckerBase
import numpy as np

from statsmodels.tsa.vector_ar.vecm import coint_johansen
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.adfvalues import mackinnonp
import ipdb


class CoIntCheckerECM(CoIntCheckerBase):
    def __init__(self, prices_a, prices_b):
        super().__init__(prices_a, prices_b)

    def check(self):
        _log_price_a = np.log(self._prices_a)
        _log_price_b = np.log(self._prices_b)

        _values = np.stack((_log_price_b, _log_price_a), axis=-1)

        rst = coint_johansen(_values, det_order=0, k_ar_diff=1)

        beta_b, beta_a = rst.evec[0]
        # self._spread = _log_price_b * beta_b + _log_price_a * beta_a
        # res_adf = adfuller(self._spread, maxlag=1, regression='c', autolag=None)
        # print(res_adf)

        self._beta_b = beta_b
        self._beta_a = beta_a

        self._beta = beta_a / beta_b
        self._spread = _log_price_b + _log_price_a * beta_a / beta_b
        res_adf = adfuller(self._spread, maxlag=1, regression='c', autolag=None)
        # ipdb.set_trace()

        self._p_value = mackinnonp(res_adf[0], regression='c', N=2)
        self._t_stats = res_adf[0]

    # @property
    # def Beta(self):
    #     return self._beta_b, self._beta_a
