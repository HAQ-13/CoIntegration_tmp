import unittest
import os
import pandas as pd

from CointCheck.CoIntCheckerECM import CoIntCheckerECM
from CointCheck.CoIntCheckerEG import CoIntCheckerEG
import ipdb


class TestCoInt(unittest.TestCase):
    def test_0010(self):
        df = pd.read_csv('./data/Y_P_5min.csv')
        # _df = df[86:386]
        _df = df[1957:2257]
        prices_a = _df['close_1'].values
        prices_b = _df['close_2'].values

        obj = CoIntCheckerEG(prices_a, prices_b)
        obj.check()
        print('----- EG -----')
        print(obj.TStats, obj.PValue, obj.Beta, obj.Mu, obj.MuEMA(0.5), obj.Sigma)

    def test_0011(self):
        df = pd.read_csv('./data/Y_P_5min.csv')
        _df = df[1957:2257]
        prices_a = _df['close_1'].values
        prices_b = _df['close_2'].values

        obj = CoIntCheckerECM(prices_a, prices_b)
        obj.check()
        print('----- ECM -----')
        print(obj.TStats, obj.PValue, obj.Beta, obj.Mu, obj.MuEMA(0.5), obj.Sigma)

    def test_0020(self):
        df = pd.read_csv('./data/Y_P_5min.csv')
        window_len = 300
        for i in range(window_len + 1, 1000):
            # for i in range(950, 1000):
            _df = df[i - 300:i]
            prices_a = _df['close_1'].values
            prices_b = _df['close_2'].values

            obj = CoIntCheckerEG(prices_a, prices_b)
            obj.check()
            if obj.PValue < 0.2:
                ipdb.set_trace()
                print('----- {0} -----'.format(i))

                print('----- EG -----')
                print(obj.TStats, obj.PValue, obj.Beta, obj.Mu, obj.MuEMA(0.5), obj.Sigma)

                obj = CoIntCheckerECM(prices_a, prices_b)
                obj.check()
                print('----- ECM -----')
                print(obj.TStats, obj.PValue, obj.Beta, obj.Mu, obj.MuEMA(0.5), obj.Sigma)
