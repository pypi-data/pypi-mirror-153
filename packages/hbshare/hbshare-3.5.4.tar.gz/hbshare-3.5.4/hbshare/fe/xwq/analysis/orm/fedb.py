# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Insert
import pandas as pd
import pymysql
import sqlalchemy
import sys
import time
import traceback
import warnings
warnings.filterwarnings('ignore', category=pymysql.Warning)


class FEDB:
    def __init__(self):
        self.fedb_engine = None
        self.fedb_connection = None
        self.create_connection()

    def create_connection(self):
        vaild = False
        while not vaild:
            try:
                self.fedb_engine = create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(
                                                 'admin', 'mysql', '192.168.223.152', '3306', 'fe_temp_data'),
                                   connect_args={'charset': 'utf8'}, pool_recycle=360,
                                   pool_size=2, max_overflow=10, pool_timeout=360)
                self.fedb_connection = self.fedb_engine.connect()
                vaild = True
            except Exception as e:
                self.close_connection()
                print('[FEDB] mysql connect error')
                time.sleep(5)
        return

    def close_connection(self):
        # 1) close connection
        try:
            if self.fedb_connection is not None:
                self.fedb_connection.close()
        except Exception as e:
            print('[FEDB] close connect error')
        # 2) dispose engine
        try:
            if self.fedb_engine is not None:
                self.fedb_engine.dispose()
        except Exception as e:
            print('[FEDB] dispose engine error')
        return

    def get_df(self, sql):
        valid = False
        df = None
        while not valid:
            try:
                df = pd.read_sql_query(sql, self.fedb_engine)
                self.close_connection()
                valid = True
            except Exception as e:
                self.close_connection()
                self.create_connection()
                print('[FEDB] sql error:{0}'.format(sql))
                time.sleep(5)
        return df

    def create_metadata(self, metadata):
        valid = False
        while not valid:
            try:
                metadata.create_all(self.fedb_engine)
                valid = True
            except Exception as e:
                self.close_connection()
                self.create_connection()
                exc_type, exc_value, exc_trackback = sys.exc_info()
                print(repr(traceback.format_exception(exc_type, exc_value, exc_trackback)))
                print('[FEDB] create metadata error')
            return metadata

    def insert_data(self, table, params):
        try:
            self.fedb_connection.execute(table.insert(), params)
        except Exception as e:
            conn = self.fedb_engine.connect()
            conn.execute(table.insert(), params)
            self.fedb_connection = conn
            exc_type, exc_value, exc_trackback = sys.exc_info()
            print(repr(traceback.format_exception(exc_type, exc_value, exc_trackback)))
            print('[FEDB] insert data error')
        return

    def replace_data(self, table, params):
        # @compiles(Insert)
        def replace_string(insert, compiler, **kw):
            s = compiler.visit_insert(insert, **kw)
            s = s.replace("INSERT INTO", "REPLACE INTO")
            return s

        valid = False
        times = 0
        while not valid and times < 5:
            try:
                times += 1
                self.fedb_connection.execute(table.insert(replace_string=""), params)
                valid = True
            except Exception as e:
                self.close_connection()
                self.create_connection()
                time.sleep(2)
                exc_type, exc_value, exc_trackback = sys.exc_info()
                print(repr(traceback.format_exception(exc_type, exc_value, exc_trackback)))
                print('[FEDB] replace data error')
            return

    def update_data(self, table, params):
        # @compiles(Insert)
        def append_string(insert, compiler, **kw):
            s = compiler.visit_insert(insert, **kw)
            if insert.kwards.get('on_duplicates_key_update'):
                fields = s[s.find("(") + 1:s.find(")")].replace(" ", "").split(",")
                generated_directive = ["{0}=VALUES({0})".format(field) for field in fields]
                return s + " ON DUPLICATES KEY UPDATE " + ",".join(generated_directive)
            return s

        valid = False
        times = 0
        while not valid and times < 5:
            try:
                times += 1
                self.fedb_connection.execute(table.insert(on_duplicates_key_update=True), params)
                valid = True
            except Exception as e:
                self.close_connection()
                self.create_connection()
                time.sleep(2)
                exc_type, exc_value, exc_trackback = sys.exc_info()
                print(repr(traceback.format_exception(exc_type, exc_value, exc_trackback)))
                print('[FEDB] update data error')
            return

    def insert_df(self, factor_df):
        table_name = 'mutual_fund_holding_label'
        metadata = sqlalchemy.MetaData()
        table = sqlalchemy.Table(
            table_name, metadata,
            sqlalchemy.Column('REPORT_DATE'),
            sqlalchemy.Column('REPORT_HISTORY_DATE'),
            sqlalchemy.Column('FUND_UNIVERSE'),
            sqlalchemy.Column('IS_ZC'),
            sqlalchemy.Column('LABEL_TYPE'),
            sqlalchemy.Column('LABEL_NAME'),
            sqlalchemy.Column('LABEL_VALUE'),
            sqlalchemy.Column('LABEL_VALUE_STRING')
        )
        metadata = self.create_metadata(metadata)
        params = []
        for idx in range(len(factor_df)):
            rows = factor_df.iloc[idx]
            param = dict()
            param['REPORT_DATE'] = rows['REPORT_DATE']
            param['REPORT_HISTORY_DATE'] = rows['REPORT_HISTORY_DATE']
            param['FUND_UNIVERSE'] = rows['FUND_UNIVERSE']
            param['IS_ZC'] = rows['IS_ZC']
            param['LABEL_TYPE'] = rows['LABEL_TYPE']
            param['LABEL_NAME'] = rows['LABEL_NAME']
            param['LABEL_VALUE'] = rows['LABEL_VALUE']
            param['LABEL_VALUE_STRING'] = rows['LABEL_VALUE_STRING']
            params.append(param)
            if len(params) > 1000:
                self.update_data(table, params)
                del params
                params = []
        if len(params) > 0:
            self.update_data(table, params)
        self.close_connection()
        return

    def insert_hbs_rank_his_df(self, factor_df):
        table_name = 'hbs_rank_his'
        metadata = sqlalchemy.MetaData()
        table = sqlalchemy.Table(
            table_name, metadata,
            sqlalchemy.Column('jjdm'),
            sqlalchemy.Column('jsrq'),
            sqlalchemy.Column('shift_ratio_size'),
            sqlalchemy.Column('c_level_size'),
            sqlalchemy.Column('shift_ratio_style'),
            sqlalchemy.Column('c_level_style'),
            sqlalchemy.Column('shift_ratio_theme'),
            sqlalchemy.Column('c_level_theme'),
            sqlalchemy.Column('shift_ratio_ind'),
            sqlalchemy.Column('c_level_ind'),
            sqlalchemy.Column('c_level_stock'),
        )
        metadata = self.create_metadata(metadata)
        params = []
        for idx in range(len(factor_df)):
            rows = factor_df.iloc[idx]
            param = dict()
            param['jjdm'] = rows['jjdm']
            param['jsrq'] = rows['jsrq']
            param['shift_ratio_size'] = rows['shift_ratio_size']
            param['c_level_size'] = rows['c_level_size']
            param['shift_ratio_style'] = rows['shift_ratio_style']
            param['c_level_style'] = rows['c_level_style']
            param['shift_ratio_theme'] = rows['shift_ratio_theme']
            param['c_level_theme'] = rows['c_level_theme']
            param['shift_ratio_ind'] = rows['shift_ratio_ind']
            param['c_level_ind'] = rows['c_level_ind']
            param['c_level_stock'] = rows['c_level_stock']
            params.append(param)
            if len(params) > 1000:
                self.update_data(table, params)
                del params
                params = []
        if len(params) > 0:
            self.update_data(table, params)
        self.close_connection()
        return

    def insert_fund_index(self, factor_df):
        table_name = 'fund_index'
        metadata = sqlalchemy.MetaData()
        table = sqlalchemy.Table(
            table_name, metadata,
            sqlalchemy.Column('TRADE_DATE'),
            sqlalchemy.Column('INDEX_SYMBOL'),
            sqlalchemy.Column('INDEX_NAME'),
            sqlalchemy.Column('INDEX_POINT')
        )
        metadata = self.create_metadata(metadata)
        params = []
        for idx in range(len(factor_df)):
            rows = factor_df.iloc[idx]
            param = dict()
            param['TRADE_DATE'] = rows['TRADE_DATE']
            param['INDEX_SYMBOL'] = rows['INDEX_SYMBOL']
            param['INDEX_NAME'] = rows['INDEX_NAME']
            param['INDEX_POINT'] = rows['INDEX_POINT']
            params.append(param)
            if len(params) > 1000:
                self.update_data(table, params)
                del params
                params = []
        if len(params) > 0:
            self.update_data(table, params)
        self.close_connection()
        return

    def read_fund_index_latest_date(self):
        sql = "SELECT max(TRADE_DATE) FROM fe_temp_data.fund_index GROUP BY INDEX_NAME"
        df = self.get_df(sql)
        latest_date = min(df['max(TRADE_DATE)'])
        return latest_date

    def read_fund_index_given_date(self, date):
        sql = "SELECT TRADE_DATE, INDEX_SYMBOL, INDEX_NAME, INDEX_POINT FROM fe_temp_data.fund_index WHERE TRADE_DATE = '{0}'".format(date)
        df = self.get_df(sql)
        return df

    def read_fund_index_gt_date(self, date):
        sql = "SELECT TRADE_DATE, INDEX_SYMBOL, INDEX_NAME, INDEX_POINT FROM fe_temp_data.fund_index WHERE TRADE_DATE >= '{0}'".format(date)
        df = self.get_df(sql)
        return df

    def read_data(self, date, label_type):
        sql = "SELECT REPORT_DATE, REPORT_HISTORY_DATE, FUND_UNIVERSE, IS_ZC, LABEL_TYPE, LABEL_NAME, LABEL_VALUE, LABEL_VALUE_STRING FROM fe_temp_data.mutual_fund_holding_label where REPORT_DATE='{0}' AND LABEL_TYPE='{1}' AND FUND_UNIVERSE='FOCUS_MUTUAL_FUND_UNIVERSE' AND IS_ZC=1".format(date, label_type)
        df = self.get_df(sql)
        df['REPORT_DATE'] = df['REPORT_DATE'].astype(str)
        df['REPORT_HISTORY_DATE'] = df['REPORT_HISTORY_DATE'].astype(str)
        df['IS_ZC'] = df['IS_ZC'].astype(int)
        return df

    def read_hbs_size_property_given_code(self, code):
        size_list = ['大盘', '中盘', '小盘']
        size = ','.join(size_list)
        size_rank_list = ['大盘_rank', '中盘_rank', '小盘_rank']
        size_rank = ','.join(size_rank_list)
        sql = "select jjdm, asofdate, shift_lv, cen_lv, {0}, shift_lv_rank, cen_lv_rank, {1} from fe_temp_data.hbs_size_property where jjdm='{2}' and asofdate=(SELECT max(asofdate) FROM fe_temp_data.hbs_size_property)".format(size, size_rank, code)
        df = self.get_df(sql)
        return df

    def read_size_exposure_given_code(self, code):
        sql = "select jjdm, jsrq, size_type, zjbl from fe_temp_data.hbs_size_exp where jjdm='{0}'".format(code)
        df = self.get_df(sql)
        return df

    def read_hbs_style_property_given_code(self, code):
        style_list = ['成长', '价值']
        style = ','.join(style_list)
        style_rank_list = ['成长_rank', '价值_rank']
        style_rank = ','.join(style_rank_list)
        sql = "select jjdm, asofdate, shift_lv, cen_lv, {0}, shift_lv_rank, cen_lv_rank, {1} from fe_temp_data.hbs_style_property where jjdm='{2}' and asofdate=(SELECT max(asofdate) FROM fe_temp_data.hbs_style_property)".format(style, style_rank, code)
        df = self.get_df(sql)
        return df

    def read_style_exposure_given_code(self, code):
        sql = "select jjdm, jsrq, style_type, zjbl from fe_temp_data.hbs_style_exp where jjdm='{0}'".format(code)
        df = self.get_df(sql)
        return df

    def read_hbs_size_style_property_history_given_code(self, code):
        sql = "select jjdm, jsrq, shift_ratio_size, c_level_size, shift_ratio_style, c_level_style from fe_temp_data.hbs_cen_shift_ratio_his_style where jjdm='{0}'".format(code)
        df = self.get_df(sql)
        return df

    def read_hbs_theme_industry_property_given_code(self, code):
        sql = "select jjdm, asofdate, ratio_theme, cen_theme, ratio_theme_rank, cen_theme_rank, ratio_ind_1 as ratio_ind, cen_ind_1 as cen_ind, ratio_ind_1_rank as ratio_ind_rank, cen_ind_1_rank as cen_ind_rank, industry_num, top5 from fe_temp_data.hbs_industry_property_new where jjdm='{0}' and asofdate=(SELECT max(asofdate) FROM fe_temp_data.hbs_industry_property_new)".format(code)
        df = self.get_df(sql)
        return df

    def read_hbs_theme_property_given_code(self, code):
        theme_list = ['大金融', '消费', 'TMT', '制造', '周期']
        theme = ','.join(theme_list)
        sql = "select jjdm, asofdate, {0} from fe_temp_data.jjpic_theme_p where jjdm='{1}' and asofdate=(SELECT max(asofdate) FROM fe_temp_data.jjpic_theme_p)".format(theme, code)
        df = self.get_df(sql)
        return df

    def read_hbs_industry_property_given_code(self, code):
        sql = "select jjdm, asofdate, yjxymc, zsbl_mean, zsbl_med, zsbl_mean_rank, zsbl_med_rank from fe_temp_data.hbs_industry_property_1_industry_level where jjdm='{0}' and asofdate=(SELECT max(asofdate) FROM fe_temp_data.hbs_industry_property_1_industry_level)".format(code)
        df = self.get_df(sql)
        return df

    def read_theme_exposure_given_code(self, code):
        theme_list = ['大金融', '消费', 'TMT', '制造', '周期']
        theme = ','.join(theme_list)
        sql = "select jjdm, jsrq, {0} from fe_temp_data.hbs_theme_exp where jjdm='{1}'".format(theme, code)
        df = self.get_df(sql)
        return df

    def read_industry_exposure_given_code(self, code):
        sql = "select jjdm, jsrq, yjxymc, zjbl from fe_temp_data.hbs_industry_class1_exp where jjdm='{0}'".format(code)
        df = self.get_df(sql)
        return df

    def read_hbs_theme_industry_property_history_given_code(self, code):
        sql = "select jjdm, jsrq, shift_ratio_theme, c_level_theme, shift_ratio as shift_ratio_ind, c_level as c_level_ind from fe_temp_data.hbs_cen_shift_ratio_his_industry1 where jjdm='{0}'".format(code)
        df = self.get_df(sql)
        return df

    def read_hbs_holding_property_given_code(self, code):
        sql = "select jjdm, asofdate, 个股集中度 from fe_temp_data.hbs_holding_property where jjdm='{0}' and asofdate=(SELECT max(asofdate) FROM fe_temp_data.hbs_holding_property)".format(code)
        df = self.get_df(sql)
        return df

    def read_hbs_holding_property_history_given_code(self, code):
        sql = "select jjdm, jsrq, cenlv as c_level_stock from fe_temp_data.hbs_stock_cenlv_his where jjdm='{0}'".format(code)
        df = self.get_df(sql)
        return df

    def read_hbs_stock_trading_property_given_code(self, code):
        sql = "select * from fe_temp_data.hbs_stock_trading_property where jjdm='{0}' and asofdate=(SELECT max(asofdate) FROM fe_temp_data.hbs_stock_trading_property)".format(code)
        df = self.get_df(sql)
        return df

    def read_hbs_rank_history_given_code(self, code):
        sql = "select jjdm, jsrq, shift_ratio_size, c_level_size, shift_ratio_style, c_level_style, shift_ratio_theme, c_level_theme, shift_ratio_ind, c_level_ind, c_level_stock from fe_temp_data.hbs_rank_his where jjdm='{0}'".format(code)
        df = self.get_df(sql)
        return df

    def read_hbs_his_data(self, table_name):
        sql = "select * from fe_temp_data.{0}".format(table_name)
        df = self.get_df(sql)
        return df