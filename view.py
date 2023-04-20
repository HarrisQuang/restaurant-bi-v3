import streamlit as st
import altair as alt
import os, sys
import numpy as np
import json 
path = os.path.abspath('.')
sys.path.append(path)
import controller.data_warehouse as dw
import controller.utils as utils

with open('config.json', "r", encoding='utf-8') as f:
    data = json.loads(f.read())

st.set_page_config(
    page_title="Rau Cu Nam report",
    page_icon="✅",
    layout="wide",
)


dw_qrdb = dw.QueryDB()
dw_wd = dw.WranglingData()
dw_qrdb.begin()

tab1, tab2, tab3 = st.tabs(["NGÀY CHAY", "NGÀY", "THÁNG"])

with tab1:
    st.title("XEM BÁO CÁO THEO NGÀY CHAY")

    placeholder = st.empty()

    label_colors = {'condition': [], 'value': 'white'}  # The default value if no condition is met
        
    with placeholder.container():
        ngay_filter_list = dw_qrdb.get_ngay_filter_orders_vegan_day_tbl()
        with st.form(key='form-chon-ngay-chay'):
            col1, col2 = st.columns(2)
            with col1:
                selected_day = st.multiselect('Chọn ngày chay', ngay_filter_list)
            submitted = st.form_submit_button('Thực hiện')
        if not selected_day:
            selected_day = [ngay_filter_list[-1]]
        
        st.markdown("### Số đơn hàng đã bán")
        
        total_order_orders_vegan_day_tbl_with_df = dw_qrdb.get_total_order_orders_vegan_day_tbl_with(selected_day)
        total_order_orders_vegan_day_tbl_final_df, measure_delta = dw_wd.generate_total_order_orders_vegan_day_tbl_final_df(total_order_orders_vegan_day_tbl_with_df)
        
        if len(selected_day) == 1:
            total_order_orders_vegan_day_tbl_final_df = total_order_orders_vegan_day_tbl_final_df.iloc[:,:-1]
            st.table(total_order_orders_vegan_day_tbl_final_df)
        else:
            fig = utils.create_line_chart(data = total_order_orders_vegan_day_tbl_final_df, x = 'Ngày', y = 'Số đơn hàng', measure_delta = measure_delta, sorting = True)
            st.altair_chart(fig, use_container_width=True)
       
        st.markdown("### Số phần đã bán của mỗi loại món ăn")
        
        dish_list = dw_qrdb.get_distinct_dish_quantity_sales_dishes_vegan_day_tbl()
        dish_list.append('...')
        selected_dish_list = []
        with st.form(key='form-chon-nhieu-mon-an'):
            cols = st.columns(5)
            for i, col in enumerate(cols):
                selected_dish = col.selectbox('Chọn món', dish_list, key=i, index=len(dish_list)-1)
                selected_dish_list.append(selected_dish)
            submitted = st.form_submit_button('Thực hiện')
        final_selected_dish_list = []
        for i in selected_dish_list:
            if i != '...':
                final_selected_dish_list.append(i)
        if len(final_selected_dish_list) == 0:
            final_selected_dish_list.append('Bún Thái')  
        
        sell_quantity_sales_dishes_vegan_day_tbl_with_df = dw_qrdb.get_sell_quantity_sales_dishes_vegan_day_tbl_with(selected_day, final_selected_dish_list)
        sell_quantity_sales_dishes_vegan_day_tbl_final_df, measure_delta = dw_wd.generate_sell_quantity_sales_dishes_vegan_day_tbl_final_df(sell_quantity_sales_dishes_vegan_day_tbl_with_df)
        
        if len(selected_day) == 1:
            sell_quantity_sales_dishes_vegan_day_tbl_final_df = sell_quantity_sales_dishes_vegan_day_tbl_final_df.iloc[:,1:-1]
            st.table(sell_quantity_sales_dishes_vegan_day_tbl_final_df.style.format({'Số phần bán': '{:,.0f}'}))
        else:
            fig = utils.create_line_chart(data = sell_quantity_sales_dishes_vegan_day_tbl_final_df, x = 'Ngày', y = 'Số phần bán', measure_delta = measure_delta, cate = 'Tên món')
            st.altair_chart(fig, use_container_width=True)
        
        st.markdown("### Số lượng được khuyến mãi")
        
        with st.form(key='form-chon-1-mon-an'):
            col1, col2 = st.columns(2)
            with col1:
                sltd_dish = st.selectbox("Chọn món", dish_list, index=len(dish_list)-1)
            submitted = st.form_submit_button('Thực hiện')
            
        if sltd_dish == '...':
            sltd_dish = 'Bún Thái'
            
        sale_off_quantity_sales_dishes_vegan_day_tbl_with_single_day_df = dw_qrdb.get_sale_off_quantity_sales_dishes_vegan_day_tbl_with_single_day(selected_day, sltd_dish)
        sale_off_quantity_sales_dishes_vegan_day_tbl_with_single_day_df = dw_wd.generate_sale_off_quantity_sales_dishes_vegan_day_tbl_single_day_df(sale_off_quantity_sales_dishes_vegan_day_tbl_with_single_day_df)
        
        if len(selected_day) == 1:
            st.table(sale_off_quantity_sales_dishes_vegan_day_tbl_with_single_day_df.style.format({'Số lượng': '{:.0f}', 'Doanh thu': '{:,.0f}'}))
        else:
            pass
        
        st.markdown("### Xếp hạng món bán chạy")
        
        col1, col2 = st.columns(2)
        with col1:
            top_quantity = st.slider("Top SL:", 1, 20, 3)
        ranking_quantity_sales_dishes_vegan_day_tbl_with_df = dw_qrdb.get_ranking_quantity_sales_dishes_vegan_day_tbl_with(selected_day, top_quantity)
        ranking_quantity_sales_dishes_vegan_day_tbl_pivot_df = dw_wd.generate_ranking_quantity_sales_dishes_vegan_day_tbl_pivot_df(ranking_quantity_sales_dishes_vegan_day_tbl_with_df)
        st.table(ranking_quantity_sales_dishes_vegan_day_tbl_pivot_df)
        
        col3, col4 = st.columns(2)
        with col3:
            top_revenue = st.slider("Top Doanh thu:", 1, 20, 3)
        ranking_revenue_sales_dishes_vegan_day_tbl_with_df = dw_qrdb.get_ranking_quantity_sales_dishes_vegan_day_tbl_with(selected_day, None, top_revenue)
        ranking_revenue_sales_dishes_vegan_day_tbl_pivot_df = dw_wd.generate_ranking_revenue_sales_dishes_vegan_day_tbl_pivot_df(ranking_revenue_sales_dishes_vegan_day_tbl_with_df)        
        st.table(ranking_revenue_sales_dishes_vegan_day_tbl_pivot_df)

with tab2:
    st.title("XEM BÁO CÁO THEO NGÀY")

    placeholder = st.empty()

    label_colors = {'condition': [], 'value': 'white'}  # The default value if no condition is met
        
    with placeholder.container():
        st.markdown("### ...")

with tab3:
    st.title("XEM BÁO CÁO THEO THÁNG")

    placeholder = st.empty()

    label_colors = {'condition': [], 'value': 'white'}  # The default value if no condition is met
        
    with placeholder.container():
        st.markdown("### ...")
        