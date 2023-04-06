from sqlalchemy import create_engine
import json 
import pandas as pd
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
        result = self.connection.execute(query.get_ngay_filter_orders_vegan_day_tbl)
        df = pd.DataFrame(result.fetchall())
        ngay_filter_list = df['ngay_filter'].tolist()
        return ngay_filter_list

    def get_total_order_orders_vegan_day_tbl_with(self, ngay_filter_list):
        ngay_filter_list = tuple(ngay_filter_list)
        if len(ngay_filter_list) == 1:
            result = self.connection.execute(query.get_total_order_orders_vegan_day_tbl_with['single_day'] % (ngay_filter_list[0]))
        else:
            result = self.connection.execute(query.get_total_order_orders_vegan_day_tbl_with['multi_days'] % (ngay_filter_list,))
        total_order_orders_vegan_day_tbl_with_df = pd.DataFrame(result.fetchall())
        return total_order_orders_vegan_day_tbl_with_df

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