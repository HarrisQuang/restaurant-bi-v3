# imports
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import os, sys
path = os.path.abspath('.')
sys.path.append(path)
import controller.data_warehouse as dw

dw_qrdb = dw.QueryDB()

selected_day = ['01/04/2022(01/03)', '29/04/2022(29/03)', '27/07/2022(29/06)']
sltd_dish = 'Bún Thái'
df = dw_qrdb.get_sale_off_quantity_sales_dishes_vegan_day_tbl_with_multi_days(selected_day, sltd_dish)
print(df)

fig = px.bar(df, x='ngay_filter', y='sl_ban_cate', color='main_cate', hover_data=['tong_cate', 'percent_sl', 'percent_tong'], barmode = 'group')
fig.show()

# data
# df = pd.DataFrame({'Index': {0: 1.0,
#                               1: 2.0,
#                               2: 3.0,
#                               3: 4.0,
#                               4: 5.0,
#                               5: 6.0,
#                               6: 7.0,
#                               7: 8.0,
#                               8: 9.0,
#                               9: 10.0},
#                              'A': {0: 15.0,
#                               1: 6.0,
#                               2: 5.0,
#                               3: 4.0,
#                               4: 3.0,
#                               5: 2.0,
#                               6: 1.0,
#                               7: 0.5,
#                               8: 0.3,
#                               9: 0.1},
#                              'B': {0: 1.0,
#                               1: 4.0,
#                               2: 2.0,
#                               3: 5.0,
#                               4: 4.0,
#                               5: 6.0,
#                               6: 7.0,
#                               7: 2.0,
#                               8: 8.0,
#                               9: 1.0},
#                              'C': {0: 12.0,
#                               1: 6.0,
#                               2: 5.0,
#                               3: 4.0,
#                               4: 3.0,
#                               5: 2.0,
#                               6: 1.0,
#                               7: 0.5,
#                               8: 0.2,
#                               9: 0.1}})
# # set up plotly figure
# fig = make_subplots(1,2)

# # add first bar trace at row = 1, col = 1
# fig.add_trace(go.Bar(x=df['Index'], y=df['A'],
#                      name='A',
#                      marker_color = 'green',
#                      opacity=0.4,
#                      marker_line_color='rgb(8,48,107)',
#                      marker_line_width=2),
#               row = 1, col = 1)

# # add first scatter trace at row = 1, col = 1
# fig.add_trace(go.Scatter(x=df['Index'], y=df['B'], line=dict(color='red'), name='B'),
#               row = 1, col = 1)

# # add first bar trace at row = 1, col = 2
# fig.add_trace(go.Bar(x=df['Index'], y=df['C'],
#                      name='C',
#                      marker_color = 'green',
#                      opacity=0.4,
#                      marker_line_color='rgb(8,48,107)',
#                     marker_line_width=2),
#               row = 1, col = 2)
# fig.show()