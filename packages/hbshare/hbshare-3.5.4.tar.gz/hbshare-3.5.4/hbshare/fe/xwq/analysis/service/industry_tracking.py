# -*- coding: utf-8 -*-

from hbshare.fe.xwq.analysis.orm.hbdb import HBDB
from datetime import datetime, timedelta
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style('white', {'font.sans-serif': ['simhei', 'Arial']})


def to_percent(temp, position):
    return '%1.0f'%(temp) + '%'

def get_cal_and_trade_cal(start, end):
    """
    获取交易日期
    """
    cal = HBDB().read_cal(start, end)
    cal = cal.rename(columns={'JYRQ': 'TRADE_DATE', 'SFJJ': 'IS_OPEN', 'SFZM': 'IS_WEEK_END', 'SFYM': 'IS_MONTH_END'})
    cal['IS_OPEN'] = cal['IS_OPEN'].astype(int).replace({0: 1, 1: 0})
    cal['IS_WEEK_END'] = cal['IS_WEEK_END'].fillna(0).astype(int)
    cal['IS_MONTH_END'] = cal['IS_MONTH_END'].fillna(0).astype(int)
    cal = cal.sort_values('TRADE_DATE')
    trade_cal = cal[cal['IS_OPEN'] == 1]
    trade_cal['RECENT_TRADE_DATE'] = trade_cal['TRADE_DATE']
    trade_cal['PREV_TRADE_DATE'] = trade_cal['TRADE_DATE'].shift(1)
    trade_cal = trade_cal[['TRADE_DATE', 'RECENT_TRADE_DATE', 'PREV_TRADE_DATE', 'IS_OPEN', 'IS_WEEK_END', 'IS_MONTH_END']]
    cal = cal.merge(trade_cal[['TRADE_DATE', 'RECENT_TRADE_DATE']], on=['TRADE_DATE'], how='left')
    cal['RECENT_TRADE_DATE'] = cal['RECENT_TRADE_DATE'].fillna(method='ffill')
    cal = cal.merge(trade_cal[['TRADE_DATE', 'PREV_TRADE_DATE']], on=['TRADE_DATE'], how='left')
    cal['PREV_TRADE_DATE'] = cal['PREV_TRADE_DATE'].fillna(method='bfill')
    cal = cal[['TRADE_DATE', 'RECENT_TRADE_DATE', 'PREV_TRADE_DATE', 'IS_OPEN', 'IS_WEEK_END', 'IS_MONTH_END']]
    return cal, trade_cal

def get_industry_index(date, stock_industry):
    trade_cal = get_cal_and_trade_cal('20000101', datetime.today().strftime('%Y%m%d'))[1]
    trade_cal['TRADE_DATE'] = trade_cal['TRADE_DATE'].astype(str)
    trade_cal = trade_cal.sort_values('TRADE_DATE')
    recent_trade_date = trade_cal[trade_cal['TRADE_DATE'] <= date]['TRADE_DATE'].iloc[-1]

    stock_finance = HBDB().read_finance_data_given_date(date)
    stock_finance.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_tracking/stock_finance_{0}.hdf'.format(date), key='table', mode='w')
    stock_finance = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_tracking/stock_finance_{0}.hdf'.format(date), key='table')
    stock_finance = stock_finance[['TICKER_SYMBOL', 'END_DATE', 'PUBLISH_DATE', 'ROE_TTM', 'GROSS_INCOME_RATIO_TTM', 'NET_PROFIT', 'INCOME_PS']]
    stock_finance = stock_finance.sort_values(['TICKER_SYMBOL', 'END_DATE', 'PUBLISH_DATE']).drop_duplicates(['TICKER_SYMBOL', 'END_DATE'], keep='last')
    stock_mv = HBDB().read_stock_market_value_given_date(recent_trade_date)
    stock_mv.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_tracking/stock_mv_{0}.hdf'.format(date), key='table', mode='w')
    stock_mv = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_tracking/stock_mv_{0}.hdf'.format(date), key='table')
    stock_mv = stock_mv[['TICKER_SYMBOL', 'MARKET_VALUE']]
    stock_price = HBDB().read_stock_daily_k_given_date(recent_trade_date)
    stock_price.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_tracking/stock_price_{0}.hdf'.format(date), key='table', mode='w')
    stock_price = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_tracking/stock_price_{0}.hdf'.format(date), key='table')
    stock_price = stock_price[['TICKER_SYMBOL', 'CLOSE_PRICE']]
    stock_finance = stock_finance.merge(stock_mv, on=['TICKER_SYMBOL'], how='left').merge(stock_price, on=['TICKER_SYMBOL'], how='left')
    stock_finance['TOTAL_SHARES'] = stock_finance['MARKET_VALUE'] / stock_finance['CLOSE_PRICE']
    stock_finance['INCOME'] = stock_finance['INCOME_PS'] * stock_finance['TOTAL_SHARES']
    stock_finance = stock_finance[['TICKER_SYMBOL', 'END_DATE', 'PUBLISH_DATE', 'ROE_TTM', 'GROSS_INCOME_RATIO_TTM', 'NET_PROFIT', 'INCOME', 'MARKET_VALUE']]
    stock_finance = stock_finance[stock_finance['TICKER_SYMBOL'].isin(stock_industry['TICKER_SYMBOL'].unique().tolist())]
    stock_finance = stock_finance.sort_values('TICKER_SYMBOL')
    stock_finance = stock_finance.merge(stock_industry[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='left')
    stock_finance = stock_finance.dropna(subset=['TICKER_SYMBOL', 'END_DATE', 'PUBLISH_DATE', 'MARKET_VALUE', 'INDUSTRY_NAME'])

    income = stock_finance[['TICKER_SYMBOL', 'END_DATE', 'PUBLISH_DATE', 'INCOME', 'MARKET_VALUE', 'INDUSTRY_NAME']]
    income = income.dropna(subset=['INCOME'])
    income = income[['INDUSTRY_NAME', 'INCOME']].groupby('INDUSTRY_NAME').sum()

    net_profit = stock_finance[['TICKER_SYMBOL', 'END_DATE', 'PUBLISH_DATE', 'NET_PROFIT', 'MARKET_VALUE', 'INDUSTRY_NAME']]
    net_profit = net_profit.dropna(subset=['NET_PROFIT'])
    net_profit = net_profit[['INDUSTRY_NAME', 'NET_PROFIT']].groupby('INDUSTRY_NAME').sum()

    gross_ttm = stock_finance[['TICKER_SYMBOL', 'END_DATE', 'PUBLISH_DATE', 'GROSS_INCOME_RATIO_TTM', 'MARKET_VALUE', 'INDUSTRY_NAME']]
    gross_ttm = gross_ttm.dropna(subset=['GROSS_INCOME_RATIO_TTM'])
    gross_ttm = gross_ttm[(gross_ttm['GROSS_INCOME_RATIO_TTM'] <= gross_ttm['GROSS_INCOME_RATIO_TTM'].quantile(0.95)) & (gross_ttm['GROSS_INCOME_RATIO_TTM'] >= gross_ttm['GROSS_INCOME_RATIO_TTM'].quantile(0.05))]
    gross_ttm_mv = gross_ttm[['INDUSTRY_NAME', 'MARKET_VALUE']].groupby('INDUSTRY_NAME').sum().reset_index().rename(columns={'MARKET_VALUE': 'TOTAL_MARKET_VALUE'})
    gross_ttm = gross_ttm.merge(gross_ttm_mv, on=['INDUSTRY_NAME'], how='left')
    gross_ttm['GROSS_INCOME_RATIO_TTM'] = gross_ttm['GROSS_INCOME_RATIO_TTM'] * gross_ttm['MARKET_VALUE'] / gross_ttm['TOTAL_MARKET_VALUE']
    gross_ttm = gross_ttm[['INDUSTRY_NAME', 'GROSS_INCOME_RATIO_TTM']].groupby('INDUSTRY_NAME').sum()

    roe_ttm = stock_finance[['TICKER_SYMBOL', 'END_DATE', 'PUBLISH_DATE', 'ROE_TTM', 'MARKET_VALUE', 'INDUSTRY_NAME']]
    roe_ttm = roe_ttm.dropna(subset=['ROE_TTM'])
    roe_ttm = roe_ttm[(roe_ttm['ROE_TTM'] <= roe_ttm['ROE_TTM'].quantile(0.95)) & (roe_ttm['ROE_TTM'] >= roe_ttm['ROE_TTM'].quantile(0.05))]
    roe_ttm_mv = roe_ttm[['INDUSTRY_NAME', 'MARKET_VALUE']].groupby('INDUSTRY_NAME').sum().reset_index().rename(columns={'MARKET_VALUE': 'TOTAL_MARKET_VALUE'})
    roe_ttm = roe_ttm.merge(roe_ttm_mv, on=['INDUSTRY_NAME'], how='left')
    roe_ttm['ROE_TTM'] = roe_ttm['ROE_TTM'] * roe_ttm['MARKET_VALUE'] / roe_ttm['TOTAL_MARKET_VALUE']
    roe_ttm = roe_ttm[['INDUSTRY_NAME', 'ROE_TTM']].groupby('INDUSTRY_NAME').sum()

    industry_finance = income.merge(net_profit, left_index=True, right_index=True, how='outer').merge(gross_ttm, left_index=True, right_index=True, how='outer').merge(roe_ttm, left_index=True, right_index=True, how='outer')
    return industry_finance

def get_industry_tracking(report_date, sw_type):
    stock_info = HBDB().read_stock_info()
    stock_info.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_tracking/stock_info.hdf', key='table', mode='w')
    stock_info = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_tracking/stock_info.hdf', key='table')
    stock_info = stock_info.rename(columns={'zqdm': 'TICKER_SYMBOL', 'zqmc': 'SEC_SHORT_NAME', 'ssrq': 'ESTABLISH_DATE'})
    stock_info['ESTABLISH_DATE'] = stock_info['ESTABLISH_DATE'].astype(int).astype(str)
    stock_info = stock_info.loc[stock_info['TICKER_SYMBOL'].str.len() == 6]
    stock_info = stock_info.loc[stock_info['TICKER_SYMBOL'].astype(str).str.slice(0, 1).isin(['0', '3', '6'])]
    stock_info = stock_info[stock_info['ESTABLISH_DATE'] <= (datetime.strptime(report_date, '%Y%m%d') - timedelta(365)).strftime('%Y%m%d')]

    stock_industry = HBDB().read_stock_industry()
    stock_industry.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_tracking/stock_industry.hdf', key='table', mode='w')
    stock_industry = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_tracking/stock_industry.hdf', key='table')
    stock_industry = stock_industry.rename(columns={'zqdm': 'TICKER_SYMBOL', 'fldm': 'INDUSTRY_ID', 'flmc': 'INDUSTRY_NAME', 'hyhfbz': 'INDUSTRY_VERSION', 'fljb': 'INDUSTRY_TYPE', 'qsrq': 'BEGIN_DATE', 'jsrq': 'END_DATE', 'sfyx': 'IS_NEW', 'credt_etl': 'CREDT_ETL'})
    stock_industry['IS_NEW'] = stock_industry['IS_NEW'].astype(int)
    stock_industry['INDUSTRY_VERSION'] = stock_industry['INDUSTRY_VERSION'].astype(int)
    stock_industry['INDUSTRY_TYPE'] = stock_industry['INDUSTRY_TYPE'].astype(int)
    stock_industry = stock_industry[stock_industry['IS_NEW'] == 1]
    stock_industry = stock_industry[stock_industry['INDUSTRY_VERSION'] == 2]
    stock_industry = stock_industry[stock_industry['INDUSTRY_TYPE'] == sw_type]
    if sw_type == 1:
        stock_industry = stock_industry[~stock_industry['INDUSTRY_NAME'].isin(['综合', '社会服务'])]
    if sw_type == 3:
        stock_industry = stock_industry[stock_industry['INDUSTRY_NAME'].isin(['钴', '锂', '铝', '锂电池', '电池化学品', '硅料硅片', '光伏电池组件', '逆变器', '航空装备', '军工电子', '电动乘用车', '车身附件及饰件', '底盘与发动机系统', '空调', '冰洗', '酒店', '白酒', '数字芯片设计', '模拟芯片设计', '半导体设备', '医疗研发外包'])]
    stock_industry = stock_industry[stock_industry['TICKER_SYMBOL'].isin(stock_info['TICKER_SYMBOL'].unique().tolist())]

    last_report_date = '{0}{1}'.format(str(int(report_date[:4]) - 1), report_date[4:])
    industry_finance = get_industry_index(report_date, stock_industry)
    industry_finance_cols = list(industry_finance.columns)
    industry_finance.columns = [col + '_' + report_date for col in industry_finance_cols]
    last_industry_finance = get_industry_index(last_report_date, stock_industry)
    last_industry_finance_cols = list(last_industry_finance.columns)
    last_industry_finance.columns = [col + '_' + last_report_date for col in last_industry_finance_cols]
    industry_finance = pd.concat([industry_finance, last_industry_finance], axis=1)
    for col in ['INCOME', 'NET_PROFIT']:
        industry_finance[col + '_YOY_' + report_date] = (industry_finance[col + '_' + report_date] - industry_finance[col + '_' + last_report_date]) / abs(industry_finance[col + '_' + last_report_date]) * 100.0
    for col in ['GROSS_INCOME_RATIO_TTM', 'ROE_TTM']:
        industry_finance[col + '_YOY_' + report_date] = industry_finance[col + '_' + report_date] - industry_finance[col + '_' + last_report_date]
    return industry_finance

def get_result(report_date_list, sw_type_list):
    for sw_type in sw_type_list:
        industry_finance_list = []
        for report_date in report_date_list:
            industry_finance_list.append(get_industry_tracking(report_date, sw_type))
        industry_finance_all = pd.concat(industry_finance_list, axis=1)

        index_cn_dic = {'INCOME': '营业收入', 'NET_PROFIT': '归母净利润', 'GROSS_INCOME_RATIO_TTM': '毛利率（TTM）', 'ROE_TTM': 'ROE（TTM）'}
        fig_size_dic = {1: (12, 6), 2: (20, 8), 3: (12, 6)}

        for index in ['INCOME', 'NET_PROFIT', 'GROSS_INCOME_RATIO_TTM', 'ROE_TTM']:
            for report_date in report_date_list:
                data = industry_finance_all[[index + '_YOY_' + report_date]]
                data = data.sort_values(index + '_YOY_' + report_date, ascending=False)

                fig, ax = plt.subplots(figsize=fig_size_dic[sw_type])
                ax.bar(range(len(data.index)), data[index + '_YOY_' + report_date], color='#C94649', tick_label=data.index, label=index_cn_dic[index] + '_' + report_date)
                plt.legend(loc=1)
                plt.xticks(rotation=90)
                plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))
                if index in ['INCOME', 'NET_PROFIT']:
                    plt.ylabel('同比增速')
                if index in ['GROSS_INCOME_RATIO_TTM', 'ROE_TTM']:
                    plt.ylabel('同比绝对变化')
                plt.tight_layout()
                plt.savefig('{0}{1}{2}'.format('D:/Git/hbshare/hbshare/fe/xwq/data/industry_tracking/', 'sw{0}/'.format(str(sw_type)), index_cn_dic[index] + '_' + report_date))

        report_date_disp_list = [report_date_list[len(report_date_list) - i - 1] for i in range(len(report_date_list))]
        for index in ['GROSS_INCOME_RATIO_TTM', 'ROE_TTM']:
            data_list = []
            for report_date in report_date_disp_list:
                data = industry_finance_all[[index + '_' + report_date]].rename(columns={index + '_' + report_date: index}).reset_index()
                data['REPORT_DATE'] = report_date
                data = data.sort_values(index, ascending=False)
                data_list.append(data)
            data = pd.concat(data_list)

            fig, ax = plt.subplots(figsize=fig_size_dic[sw_type])
            sns.barplot(x='INDUSTRY_NAME', y=index, data=data, hue='REPORT_DATE', hue_order=report_date_disp_list, palette=['#C94649', '#8588B7'])
            plt.legend(loc=1)
            plt.xticks(rotation=90)
            plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))
            plt.xlabel('')
            plt.ylabel(index_cn_dic[index])
            plt.tight_layout()
            plt.savefig('{0}{1}{2}'.format('D:/Git/hbshare/hbshare/fe/xwq/data/industry_tracking/', 'sw{0}/'.format(str(sw_type)), index_cn_dic[index]))
    return


if __name__ == '__main__':
    report_date_list = ['20211231', '20220331']
    sw_type_list = [1, 2, 3]
    get_result(report_date_list, sw_type_list)

