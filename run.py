"""
1. 1000条数据进行测试
2. EG和ECM两种算法
3. pp和MA文件
"""

import pandas as pd
from CointCheck.CoIntCheckerECM import CoIntCheckerECM
from CointCheck.CoIntCheckerEG import CoIntCheckerEG
import ipdb

# 第一层循环的列表
keys = [('AskPrice1_Cur_x', 'BidPrice1_Cur_y'), ('BidPrice1_Cur_x', 'AskPrice1_Cur_y'), ('Close_x', 'Close_y')]
# 第二层循环的列表
Ns = [100, 200, 300, 400, 500, 600]
# 字典存放循环次数
values = range(len(keys))
dict_loop = dict(zip(keys, values))

# 读取文件
in1 = 'data/bars_DCE_pp.csv'
in2 = 'data/bars_CZCE_MA.csv'
in1_df = pd.read_csv(in1)
in2_df = pd.read_csv(in2)
# inner merge
allin_df = pd.merge(in1_df, in2_df, how='inner', on='UpdateTime', sort=True, suffixes=('_x', '_y'))
# 选取前一千条数据
allin_df = allin_df[:1000]

for key in keys:
    for N in Ns:
        # 创建空dataframe
        objs_EG = pd.DataFrame(columns=['TradingTime', 'Beta', 'PValue', 'Sigma', 'Mu', 'MuEMA(0.1)', 'MuEMA(0.2)',
                                        'MuEMA(0.3)', 'MuEMA(0.4)', 'MuEMA(0.5)'])
        objs_ECM = pd.DataFrame(columns=['TradingTime', 'Beta', 'PValue', 'Sigma', 'Mu', 'MuEMA(0.1)', 'MuEMA(0.2)',
                                         'MuEMA(0.3)', 'MuEMA(0.4)', 'MuEMA(0.5)'])
        for i in range(N + 1, 1000):
            _in_df = allin_df[i - N:i]
            prices_a = _in_df[key[0]].values
            prices_b = _in_df[key[1]].values
            _out1_df = pd.DataFrame()
            _out2_df = pd.DataFrame()

            # EG算法
            obj_EG = CoIntCheckerEG(prices_a, prices_b)
            obj_EG.check()
            _out1_df = pd.DataFrame()
            _out1_df.loc[i - N - 1, 'TradingTime'] = allin_df.loc[i, 'UpdateTime']
            _out1_df.loc[i - N - 1, 'Beta'] = obj_EG.Beta
            _out1_df.loc[i - N - 1, 'PValue'] = obj_EG.PValue
            _out1_df.loc[i - N - 1, 'Sigma'] = obj_EG.Sigma
            _out1_df.loc[i - N - 1, 'Mu'] = obj_EG.Mu
            _out1_df.loc[i - N - 1, 'MuEMA(0.1)'] = obj_EG.MuEMA(0.1)
            _out1_df.loc[i - N - 1, 'MuEMA(0.2)'] = obj_EG.MuEMA(0.2)
            _out1_df.loc[i - N - 1, 'MuEMA(0.3)'] = obj_EG.MuEMA(0.3)
            _out1_df.loc[i - N - 1, 'MuEMA(0.4)'] = obj_EG.MuEMA(0.4)
            _out1_df.loc[i - N - 1, 'MuEMA(0.5)'] = obj_EG.MuEMA(0.5)
            objs_EG = objs_EG.append(_out1_df)

            # ECM算法
            obj_ECM = CoIntCheckerECM(prices_a, prices_b)
            obj_ECM.check()
            _out2_df = pd.DataFrame()
            _out2_df.loc[i - N - 1, 'TradingTime'] = allin_df.loc[i, 'UpdateTime']
            _out2_df.loc[i - N - 1, 'Beta'] = obj_ECM.Beta
            _out2_df.loc[i - N - 1, 'PValue'] = obj_ECM.PValue
            _out2_df.loc[i - N - 1, 'Sigma'] = obj_ECM.Sigma
            _out2_df.loc[i - N - 1, 'Mu'] = obj_ECM.Mu
            _out2_df.loc[i - N - 1, 'MuEMA(0.1)'] = obj_ECM.MuEMA(0.1)
            _out2_df.loc[i - N - 1, 'MuEMA(0.2)'] = obj_ECM.MuEMA(0.2)
            _out2_df.loc[i - N - 1, 'MuEMA(0.3)'] = obj_ECM.MuEMA(0.3)
            _out2_df.loc[i - N - 1, 'MuEMA(0.4)'] = obj_ECM.MuEMA(0.4)
            _out2_df.loc[i - N - 1, 'MuEMA(0.5)'] = obj_ECM.MuEMA(0.5)
            objs_ECM = objs_ECM.append(_out2_df)
            # ipdb.set_trace()

        names_prefix = ['PPAsk_MABid', 'PPBid_MAAsk', 'PPClose_MAClose']
        names_suffix = ['EG', 'ECM']
        out1_file = 'output/{0}_N{1}_{2}.csv'.format(names_prefix[dict_loop[key]], N, names_suffix[0])
        out2_file = 'output/{0}_N{1}_{2}.csv'.format(names_prefix[dict_loop[key]], N, names_suffix[1])
        objs_EG.to_csv(out1_file, index=False)
        objs_ECM.to_csv(out2_file, index=False)
