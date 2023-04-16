from sqlalchemy import create_engine, text
import json 
import pandas as pd
import numpy as np
import os, sys
path = os.path.abspath('.')
sys.path.append(path)

import query
import controller.utils as ut
query = query.Query()

with open('config.json', "r", encoding='utf-8') as f:
    config = json.loads(f.read())

class QueryDB:
    def __init__(self, conn_str = config['dev_db_connection']):
        self.engine = create_engine(conn_str)
        self.connection = self.engine.connect()
    
    def begin(self):
        self.trans = self.connection.begin()
    
    def commit(self):
        self.trans.commit()
    
    def rollback(self):
        self.trans.rollback()
        
    def get_ngay_filter_orders_vegan_day_tbl(self):
        result = self.connection.execute(text(query.get_ngay_filter_orders_vegan_day_tbl))
        df = pd.DataFrame(result.fetchall())
        ngay_filter_list = df['ngay_filter'].tolist()
        return ngay_filter_list

    def get_distinct_dish_quantity_sales_dishes_vegan_day_tbl(self):
        result = self.connection.execute(text(query.get_distinct_dish_quantity_sales_dishes_vegan_day_tbl))
        df = pd.DataFrame(result.fetchall())
        dish_list = df['ten_mon'].tolist()
        return dish_list
    
    def get_total_order_orders_vegan_day_tbl_with(self, ngay_filter_list):
        ngay_filter_list = tuple(ngay_filter_list)
        if len(ngay_filter_list) == 1:
            result = self.connection.execute(text(query.get_total_order_orders_vegan_day_tbl_with['single_day'] % (ngay_filter_list[0])))
        else:
            result = self.connection.execute(text(query.get_total_order_orders_vegan_day_tbl_with['multi_days'] % (ngay_filter_list,)))
        total_order_orders_vegan_day_tbl_with_df = pd.DataFrame(result.fetchall())
        return total_order_orders_vegan_day_tbl_with_df
    
    def get_sell_quantity_sales_dishes_vegan_day_tbl_with(self, ngay_filter_list, final_selected_dish_list):
        ngay_filter_list = tuple(ngay_filter_list)
        final_selected_dish_list = tuple(final_selected_dish_list)
        if len(ngay_filter_list) == 1 and len(final_selected_dish_list) == 1:
            result = self.connection.execute(text(query.get_sell_quantity_sales_dishes_vegan_day_tbl_with['single_day_single_dish'] % (ngay_filter_list[0], final_selected_dish_list[0])))
        elif len(ngay_filter_list) == 1 and len(final_selected_dish_list) > 1:
            result = self.connection.execute(text(query.get_sell_quantity_sales_dishes_vegan_day_tbl_with['single_day_multi_dishes'] % (ngay_filter_list[0], final_selected_dish_list)))
        elif len(ngay_filter_list) > 1 and len(final_selected_dish_list) == 1:
            result = self.connection.execute(text(query.get_sell_quantity_sales_dishes_vegan_day_tbl_with['multi_days_single_dish'] % (ngay_filter_list, final_selected_dish_list[0])))
        elif len(ngay_filter_list) > 1 and len(final_selected_dish_list) > 1:
            result = self.connection.execute(text(query.get_sell_quantity_sales_dishes_vegan_day_tbl_with['multi_days_multi_dishes'] % (ngay_filter_list, final_selected_dish_list)))
        sell_quantity_sales_dishes_vegan_day_tbl_with_df = pd.DataFrame(result.fetchall())
        return sell_quantity_sales_dishes_vegan_day_tbl_with_df
    
    def get_ranking_sales_dishes_vegan_day_tbl_with(self, ngay_filter_list, top_quantity = None, top_revenue = None):
        ngay_filter_list = tuple(ngay_filter_list)
        if len(ngay_filter_list) == 1 and top_quantity != None:
            result = self.connection.execute(text(query.get_ranking_sales_dishes_vegan_day_tbl_with['single_day_with_xep_hang_sl_ban'] % (ngay_filter_list[0], top_quantity)))
        elif len(ngay_filter_list) > 1 and top_quantity != None:
            result = self.connection.execute(text(query.get_ranking_sales_dishes_vegan_day_tbl_with['multi_days_with_xep_hang_sl_ban'] % (ngay_filter_list, top_quantity)))
        elif len(ngay_filter_list) == 1 and top_revenue != None:
            result = self.connection.execute(text(query.get_ranking_sales_dishes_vegan_day_tbl_with['single_day_with_xep_hang_tong'] % (ngay_filter_list[0], top_revenue)))
        elif len(ngay_filter_list) > 1 and top_revenue != None:
            result = self.connection.execute(text(query.get_ranking_sales_dishes_vegan_day_tbl_with['multi_days_with_xep_hang_tong'] % (ngay_filter_list, top_revenue)))
        ranking_sales_dishes_vegan_day_tbl_with_df = pd.DataFrame(result.fetchall())
        return ranking_sales_dishes_vegan_day_tbl_with_df
    
class WranglingData:
    def calculate_percentage_change(self, df, orgin, criteria, grouping = True):
        temp = []
        if grouping == True:
            for i, val in enumerate(df[orgin]):
                if i == 0:
                    temp.append(0)
                else:
                    if df[orgin][i] != df[orgin][i-1]:
                        temp.append(0)
                    else:
                        temp.append(1)
        else:
            for i, val in enumerate(df[orgin]):
                if i == 0:
                    temp.append(0)
                else:
                    temp.append(1)
        df['flag'] = temp
        for el in criteria.keys():
            temp = []
            for i, el1 in enumerate(df[el]):
                if df['flag'][i] == 0:
                    temp.append('0')
                else:
                    delta = round((df[el][i] - df[el][i-1])/df[el][i-1]*100, 2)
                    temp.append(delta)
            df[criteria[el]] = temp
        df = df.drop('flag', axis = 1)
        return df
    
    def generate_ranking_quantity_sales_dishes_vegan_day_tbl_pivot_df(self, df):
        df['xep_hang_sl_ban'] = df['xep_hang_sl_ban'].astype('int')
        df = df.groupby(['ngay_filter', 'xep_hang_sl_ban'], as_index=False).agg({'ten_mon': ', '.join, 'sl_ban': np.max})
        df['value_pivot'] = df['ten_mon'] + ' (' + df['sl_ban'].astype('str') + ')'
        df = df.pivot_table(values='value_pivot', index='xep_hang_sl_ban', columns='ngay_filter', aggfunc = np.max)
        return df
    
    def generate_ranking_revenue_sales_dishes_vegan_day_tbl_pivot_df(self, df):
        df['xep_hang_tong'] = df['xep_hang_tong'].astype('int')
        df['tong'] = df['tong'].apply(lambda x: '{:,.0f}'.format(x))
        df = df.groupby(['ngay_filter', 'xep_hang_tong'], as_index=False).agg({'ten_mon': ', '.join, 'tong': np.max})
        df['value_pivot'] = df['ten_mon'] + ' (' + df['tong'].astype('str') + ')'
        df = df.pivot_table(values='value_pivot', index='xep_hang_tong', columns='ngay_filter', aggfunc = np.max)
        return df