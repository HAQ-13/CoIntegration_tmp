import abc
import numpy as np
import pandas as pd
import ipdb


class CoIntCheckerBase(abc.ABC):

    def __init__(self, prices_a, prices_b):
        """
        :param prices_a: price series a
        :param prices_b: price series b
        """

        if not isinstance(prices_a, np.ndarray):
            raise Exception("Expect Numpy Array")
        if not isinstance(prices_b, np.ndarray):
            raise Exception("Expect Numpy Array")

        if len(prices_a) != len(prices_b):
            raise Exception("Expect Same Length")
        if not (prices_a.ndim == 1 and prices_b.ndim == 1):
            raise Exception("Expect N-dim is 1")

        self._prices_a = prices_a
        self._prices_b = prices_b

        self._p_value = None
        self._beta = None
        self._t_stats = None

        self._spread = np.zeros(len(self._prices_a))

    @abc.abstractmethod
    def check(self):
        """
        check the series a and b is coint
        :return:
        """
        pass

    @property
    def PValue(self):
        return self._p_value

    @property
    def Beta(self):
        return self._beta

    @property
    def Sigma(self):
        return np.std(self._spread)

    @property
    def Mu(self):
        return np.mean(self._spread)

    def MuEMA(self, com):
        """
        Mu With EMA
        :param com:
        :return:
        """

        df = pd.DataFrame({"spread": self._spread})
        return df['spread'].ewm(com).mean().iloc[-1]

    @property
    def TStats(self):
        return self._t_stats
