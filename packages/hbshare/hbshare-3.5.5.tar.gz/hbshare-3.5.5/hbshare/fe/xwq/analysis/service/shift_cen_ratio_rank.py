# -*- coding: utf-8 -*-

from hbshare.fe.xwq.analysis.orm.fedb import FEDB
import numpy as np

df1 = FEDB().read_hbs_his_data('hbs_cen_shift_ratio_his_style')
df2 = FEDB().read_hbs_his_data('hbs_cen_shift_ratio_his_industry1')
df3 = FEDB().read_hbs_his_data('hbs_stock_cenlv_his')
df = df1.merge(df2, on=['jjdm', 'jsrq'], how='outer').merge(df3, on=['jjdm', 'jsrq'], how='outer')
df = df[['jjdm', 'jsrq', 'shift_ratio_size', 'c_level_size', 'shift_ratio_style', 'c_level_style', 'shift_ratio_theme', 'c_level_theme', 'shift_ratio', 'c_level', 'cenlv']]
df.columns = ['jjdm', 'jsrq', 'shift_ratio_size', 'c_level_size', 'shift_ratio_style', 'c_level_style', 'shift_ratio_theme', 'c_level_theme', 'shift_ratio_ind', 'c_level_ind', 'c_level_stock']
df_count = df[['jsrq', 'jjdm']].groupby('jsrq').count().reset_index().rename(columns={'jjdm': 'count'})
df = df.merge(df_count, on=['jsrq'], how='left')
for col in list(df.columns)[2:-1]:
    df[col] = df[['jsrq', col]].groupby('jsrq').rank(method='min')
    df[col] = df[col] / df['count']
    df[col] = df[col].replace(np.nan, None)
df = df.drop('count', axis=1)
FEDB().insert_hbs_rank_his_df(df)