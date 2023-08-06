# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from hbshare.fe.common.util.verifier import verify_type
from hbshare.fe.common.util.exception import PreprocessError
from hbshare.fe.common.util.logger import logger
from hbshare.fe.xwq.analysis.orm.fedb import FEDB
from hbshare.fe.xwq.analysis.orm.hbdb import HBDB


class IndexConstruction:
    def __init__(self, index_name, date, data_path, update_all):
        """
        :param index_name: 指数名称
        :param start_date: 归因的起始时间
        :param end_date: 归因的结束时间
        :param frequency: 归因频率
        """
        self.index_name = index_name
        self.index_symbol_dic = {'主动股票型基金指数': 'zdgj', '偏股混合型基金指数': 'pgjj'}
        self.index_symbol = self.index_symbol_dic[self.index_name]
        self.index_fund_type_dic = {'主动股票型基金指数': ['13', '37', '34'], '偏股混合型基金指数': ['37']}
        self.fund_type = self.index_fund_type_dic[self.index_name]
        self.start_date = '20071231'
        self.end_date = date
        self.data_path = data_path
        self.update_all = update_all
        self.exist_limit = 90
        self._verify_input_param()
        self._load_data()
        self._init_data()

    def _verify_input_param(self):
        verify_type(self.index_name, 'index_name', str)
        verify_type(self.start_date, 'start_date', str)
        verify_type(self.end_date, 'end_date', str)
        verify_type(self.data_path, 'data_path', str)

    def preload_fund_cumret(self, start_date, end_date, data_path):
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        fund_cumret_path = data_path + 'fund_cumret.hdf'
        if os.path.isfile(fund_cumret_path):
            existed_fund_cumret = pd.read_hdf(fund_cumret_path, key='table')
            max_date = max(existed_fund_cumret['JZRQ'])
            start_date = max(str(max_date), start_date)
        else:
            existed_fund_cumret = pd.DataFrame()
        trade_df = self.trade_df[(self.trade_df['TRADE_DATE'] > start_date) & (self.trade_df['TRADE_DATE'] <= end_date)]
        data = []
        for idx, td in enumerate(trade_df['TRADE_DATE'].unique().tolist()):
            fund_cumret_date = HBDB().read_fund_cumret_given_date(td)
            data.append(fund_cumret_date)
            print('[PreloadFundCumret][{0}/{1}]'.format(idx, len(trade_df['TRADE_DATE'])))
        fund_cumret = pd.concat([existed_fund_cumret] + data, ignore_index=True)
        # fund_cumret = fund_cumret.drop_duplicates(['JJDM', 'JZRQ'])
        fund_cumret.to_hdf(fund_cumret_path, key='table', mode='w')
        return

    def _load_data(self):
        self.calendar_df = HBDB().read_cal((datetime.strptime(self.start_date, '%Y%m%d') - timedelta(15)).strftime('%Y%m%d'), self.end_date)
        self.calendar_df = self.calendar_df.rename(columns={'JYRQ': 'CALENDAR_DATE', 'SFJJ': 'IS_OPEN', 'SFZM': 'IS_WEEK_END', 'SFYM': 'IS_MONTH_END'})
        self.calendar_df['CALENDAR_DATE'] = self.calendar_df['CALENDAR_DATE'].astype(str)
        self.calendar_df = self.calendar_df.sort_values('CALENDAR_DATE')
        self.calendar_df['IS_OPEN'] = self.calendar_df['IS_OPEN'].astype(int).replace({0: 1, 1: 0})
        self.calendar_df['YEAR_MONTH'] = self.calendar_df['CALENDAR_DATE'].apply(lambda x: x[:6])
        self.calendar_df['MONTH_DAY'] = self.calendar_df['CALENDAR_DATE'].apply(lambda x: x[-4:])
        self.report_df = self.calendar_df.drop_duplicates('YEAR_MONTH', keep='last').rename(columns={'CALENDAR_DATE': 'REPORT_DATE'})
        self.report_df = self.report_df[self.report_df['MONTH_DAY'].isin(['0331', '0630', '0930', '1231'])]
        self.report_df = self.report_df[(self.report_df['REPORT_DATE'] >= self.start_date) & (self.report_df['REPORT_DATE'] <= self.end_date)]
        self.trade_df = self.calendar_df[self.calendar_df['IS_OPEN'] == 1].rename(columns={'CALENDAR_DATE': 'TRADE_DATE'})
        self.first_trade_date = self.trade_df[self.trade_df['TRADE_DATE'] <= self.start_date]['TRADE_DATE'].iloc[-1]
        self.trade_df = self.trade_df[(self.trade_df['TRADE_DATE'] >= self.start_date) & (self.trade_df['TRADE_DATE'] <= self.end_date)]

        self.fund_info = HBDB().read_fund_info()
        self.fund_info = self.fund_info.rename(columns={'jjdm': 'FUND_CODE', 'jjmc': 'FUND_FULL_NAME', 'jjjc': 'FUND_SHORT_NAME', 'clrq': 'ESTABLISH_DATE', 'zzrq': 'EXPIRE_DATE', 'cpfl': 'PRODUCT_TYPE', 'kffb': 'OPEN_CLOSE', 'jjfl': 'FUND_TYPE_1ST', 'ejfl': 'FUND_TYPE_2ND'})
        self.fund_info = self.fund_info.dropna(subset=['ESTABLISH_DATE'])
        self.fund_info['EXPIRE_DATE'] = self.fund_info['EXPIRE_DATE'].fillna(20990101)
        self.fund_info['ESTABLISH_DATE'] = self.fund_info['ESTABLISH_DATE'].astype(int).astype(str)
        self.fund_info['EXPIRE_DATE'] = self.fund_info['EXPIRE_DATE'].astype(int).astype(str)
        self.fund_info = self.fund_info[(self.fund_info['PRODUCT_TYPE'] == '2') & (self.fund_info['OPEN_CLOSE'] == '0')]
        self.fund_info = self.fund_info[self.fund_info['FUND_TYPE_2ND'].isin(self.fund_type)]

        self.preload_fund_cumret(self.start_date, self.end_date, self.data_path)
        self.fund_cumret = pd.read_hdf(self.data_path + 'fund_cumret.hdf', key='table')
        self.fund_cumret = self.fund_cumret.rename(columns={'JJDM': 'FUND_CODE', 'JZRQ': 'TRADE_DATE', 'HBCL': 'CUM_RET'})
        self.fund_cumret['TRADE_DATE'] = self.fund_cumret['TRADE_DATE'].astype(str)
        self.first_fund_cumret = HBDB().read_fund_cumret_given_date(self.first_trade_date)
        self.first_fund_cumret = self.first_fund_cumret.rename(columns={'JJDM': 'FUND_CODE', 'JZRQ': 'TRADE_DATE', 'HBCL': 'CUM_RET'})
        self.first_fund_cumret['TRADE_DATE'] = self.first_fund_cumret['TRADE_DATE'].astype(str)
        self.fund_cumret = pd.concat([self.first_fund_cumret, self.fund_cumret])
        self.fund_cumret = self.fund_cumret.pivot(index='TRADE_DATE', columns='FUND_CODE', values='CUM_RET')
        self.fund_cumret = self.fund_cumret.sort_index()
        self.fund_nav = 0.01 * self.fund_cumret + 1

        fund_aum_list = []
        for idx, td in enumerate(self.report_df['REPORT_DATE'].unique().tolist()):
            fund_aum_date = HBDB().read_fund_scale_given_date(td)
            fund_aum_date = fund_aum_date[fund_aum_date['BBLB1'] == 13]
            fund_aum_date = fund_aum_date.sort_values(['JJDM', 'JSRQ', 'GGRQ']).drop_duplicates(['JJDM', 'JSRQ'], keep='last')
            fund_aum_list.append(fund_aum_date)
            print('[PreloadFundAum][{0}/{1}]'.format(idx, len(self.report_df['REPORT_DATE'])))
        fund_aum = pd.concat(fund_aum_list, ignore_index=True)
        # fund_aum = fund_aum.drop_duplicates(['JJDM', 'JSRQ'])
        fund_aum.to_hdf(data_path + 'fund_aum.hdf', key='table', mode='w')
        self.fund_aum = pd.read_hdf(self.data_path + 'fund_aum.hdf', key='table')
        self.fund_aum = self.fund_aum.rename(columns={'JJDM': 'FUND_CODE', 'JSRQ': 'REPORT_DATE', 'ZCJZ': 'AUM'})
        self.fund_aum['REPORT_DATE'] = self.fund_aum['REPORT_DATE'].astype(str)
        self.fund_aum = self.fund_aum.pivot(index='REPORT_DATE', columns='FUND_CODE', values='AUM')
        self.fund_aum = self.fund_aum.sort_index()

    def _init_data(self):
        date_list = sorted(list(set([self.first_trade_date] + self.trade_df['TRADE_DATE'].unique().tolist())))
        if not self.update_all:
            latest_date = FEDB().read_fund_index_latest_date()
            date_list = [date for date in date_list if date >= latest_date]
        if not (self.fund_nav.empty or self.fund_aum.empty):
                self.fund_nav = self.fund_nav.reindex(date_list).interpolate().sort_index()
                self.fund_aum = self.calendar_df[['CALENDAR_DATE']].set_index('CALENDAR_DATE').sort_index().merge(self.fund_aum, left_index=True, right_index=True, how='left')
                self.fund_aum = self.fund_aum.fillna(method='ffill').reindex(date_list)
                assert (self.fund_nav.shape[0] == self.fund_aum.shape[0])

                self.fund_info['INTO_DATE'] = self.fund_info['ESTABLISH_DATE'].apply(lambda x: (datetime.strptime(x, '%Y%m%d') + timedelta(self.exist_limit)).strftime('%Y%m%d'))
                self.fund_info['OUT_DATE'] = self.fund_info['EXPIRE_DATE']
                fund_nav_unstack = self.fund_nav.unstack().reset_index().rename(columns={0: 'NAV_ADJ'})
                fund_nav_unstack = fund_nav_unstack.merge(self.fund_info[['FUND_CODE', 'INTO_DATE', 'OUT_DATE']], on=['FUND_CODE'], how='left')
                fund_nav_unstack['INTO_DATE'] = fund_nav_unstack['INTO_DATE'].fillna('20990101')
                fund_nav_unstack['OUT_DATE'] = fund_nav_unstack['OUT_DATE'].fillna('19000101')
                fund_nav_unstack['INTO_SAMPLE'] = (fund_nav_unstack['INTO_DATE'] <= fund_nav_unstack['TRADE_DATE']) & (fund_nav_unstack['OUT_DATE'] > fund_nav_unstack['TRADE_DATE'])
                fund_nav_unstack['INTO_SAMPLE'] = fund_nav_unstack['INTO_SAMPLE'].astype(int)
                self.into_sample = fund_nav_unstack.pivot(index='TRADE_DATE', columns='FUND_CODE', values='INTO_SAMPLE')
                self.into_sample = self.into_sample.reindex(date_list).fillna(0.0)
                assert (self.fund_nav.shape[0] == self.into_sample.shape[0])
        else:
            msg = "Data empty occurred, check your input"
            logger.error(msg)
            raise PreprocessError(message=msg)

    def get_index(self):
        fund_ret = self.fund_nav / self.fund_nav.shift()
        fund_total_weight = pd.DataFrame((self.fund_aum * self.into_sample).sum(axis=1)).rename(columns={0: 'TOTAL_AUM'})
        fund_total_weight['TOTAL_AUM'] = fund_total_weight['TOTAL_AUM'].replace(0.0, np.nan)
        fund_weight = (self.fund_aum * self.into_sample).merge(fund_total_weight, left_index=True, right_index=True, how='left')
        fund_weight = fund_weight.apply(lambda x: x[:-1] / x[-1], axis=1)
        fund_index_adj = (fund_ret * fund_weight).sum(axis=1)
        if self.update_all:
            fund_index_adj.iloc[0] = 1000
            fund_index_adj = fund_index_adj.rename(index={fund_index_adj.index[0]: self.start_date})
            index = fund_index_adj.cumprod()
            index_df = pd.DataFrame(index).reset_index()
        else:
            latest_date = FEDB().read_fund_index_latest_date()
            latest_index = FEDB().read_fund_index_given_date(latest_date)
            latest_index = latest_index[latest_index['INDEX_NAME'] == self.index_name]['INDEX_POINT'].values[0]
            fund_index_adj.iloc[0] = latest_index
            index = fund_index_adj.cumprod()
            index_df = pd.DataFrame(index).reset_index().iloc[1:]
        index_df.columns = ['TRADE_DATE', 'INDEX_POINT']
        index_df['INDEX_SYMBOL'] = self.index_symbol
        index_df['INDEX_NAME'] = self.index_name
        index_df = index_df[['TRADE_DATE', 'INDEX_SYMBOL', 'INDEX_NAME', 'INDEX_POINT']]
        FEDB().insert_fund_index(index_df)
        return


if __name__ == '__main__':
    update_all = False
    index_name = '主动股票型基金指数'  # 主动股票型基金指数，偏股混合型基金指数
    date = (datetime.today() - timedelta(1)).strftime('%Y%m%d')
    data_path = 'D:/Git/hbshare/hbshare/fe/xwq/data/index_construction/'
    IndexConstruction(index_name, date, data_path, update_all).get_index()

    # index_aum = FEDB().read_fund_index_gt_date('20071231')
    # index_aum = index_aum[['TRADE_DATE', 'INDEX_NAME', 'INDEX_POINT']]
    # index_zz = HBDB().read_index_daily_k_given_date_and_indexs('20071231', ['930890', '930950'])
    # index_zz = index_zz[['zqmc', 'jyrq', 'spjg']].rename(columns={'zqmc': 'INDEX_NAME', 'jyrq': 'TRADE_DATE', 'spjg': 'INDEX_POINT'})
    # index = pd.concat([index_aum, index_zz])
    # index['TRADE_DATE'] = index['TRADE_DATE'].astype(str)
    # index = index.pivot(index='TRADE_DATE', columns='INDEX_NAME', values='INDEX_POINT').fillna(1000).sort_index()
    # index = index.rename(columns={'偏股基金': '中证偏股型基金指数', '主动股基': '中证主动股票型基金指数', '偏股混合型基金指数': '基于AUM的偏股混合型基金指数', '主动股票型基金指数': '基于AUM的主动股票型基金指数'})
    # index.index = map(lambda x: datetime.strptime(x, '%Y%m%d'), index.index)
    #
    # import matplotlib.pyplot as plt
    # plt.rcParams['font.sans-serif'] = ['SimHei']
    # plt.rcParams['axes.unicode_minus'] = False
    #
    # fig, ax = plt.subplots()
    # ax.plot(index.index, index['基于AUM的偏股混合型基金指数'].values, label='基于AUM的偏股混合型基金指数', color='#F04950')
    # ax.plot(index.index, index['中证偏股型基金指数'].values, label='中证偏股型基金指数', color='#6268A2')
    # plt.legend(loc=2)
    # plt.xticks(rotation=90)
    # plt.tight_layout()
    # plt.savefig('D:/Git/hbshare/hbshare/fe/xwq/data/index_construction/偏股型基金指数.png')
    #
    # fig, ax = plt.subplots()
    # ax.plot(index.index, index['基于AUM的主动股票型基金指数'].values, label='基于AUM的主动股票型基金指数', color='#F04950')
    # ax.plot(index.index, index['中证主动股票型基金指数'].values, label='中证主动股票型基金指数', color='#6268A2')
    # plt.legend(loc=2)
    # plt.xticks(rotation=90)
    # plt.tight_layout()
    # plt.savefig('D:/Git/hbshare/hbshare/fe/xwq/data/index_construction/主动股票型基金指数.png')
