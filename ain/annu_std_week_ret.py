# %%
import pandas as pd
import numpy as np

# load & clean data
raw_data = pd.read_csv('data/sheet2.csv', index_col=0)
data = raw_data[['StockCode', 'WeeklyClosingDate', 'WeeklyClosingPrice']]
data.columns = ['code', 'date', 'close']
data['year'] = data.date.str[:4]
data.code = data.code.apply(str).str.zfill(6)
# data.set_index(['code'], inplace=True)
try:
    data.close = pd.to_numeric(data.close)
except Exception as e:
    data.close = pd.to_numeric(data[:-1].close)
# %%
data
# %%

# get weekly returns


def get_ret(group):
    group = (group - group.shift(1)) / group.shift(1)
    return group


ret = pd.DataFrame()

ret['code'] = data['code']
ret['year'] = data['year']
ret['ret'] = pd.DataFrame(data.groupby('code').close.apply(get_ret))
ret

# %%

# get std of weekly returns
 
ret_std = pd.DataFrame(ret.groupby(['code', 'year']).ret.std())
ret_std

# %%

# Annualized
# For weekly returns, Annualized Standard Deviation = Standard Deviation of Weekly Returns * Sqrt(52).
annu_ret_std = ret_std * np.sqrt(52)
annu_ret_std.columns = ['anu_ret_std']
annu_ret_std

# %%
annu_ret_std.to_csv('sheet2.csv')

# %%

# %%
