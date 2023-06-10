import streamlit as st
import altair as alt
import os, sys
import numpy as np
import json 
path = os.path.abspath('.')
sys.path.append(path)
import controller.data_warehouse as dw
import controller.utils as utils
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
                
        st.markdown("### Doanh thu, chi phí bán hàng")
        unpivot_finance_vegan_day_tbl_with_df = dw_qrdb.get_unpivot_finance_vegan_day_tbl_with(selected_day)
        if unpivot_finance_vegan_day_tbl_with_df.empty:
            st.warning('Không có dữ liệu với ngày được chọn', icon="⚠️")
        else:
            fig = go.Figure()
            fig.update_layout(
                template="simple_white",
                xaxis=dict(title_text="Ngày"),
                yaxis=dict(title_text="Loại"),
                barmode="stack",
            )
            colors = ["#01A84B", "#01A84B", "#E24A2C", "#E24A2C", "#4BC8C4", "#4BC8C4", "#939496"]
            for r, c in zip(['Grab', 'Ck Grab', 'Sp Food', 'Ck Sp Food', 'Ck Baemin', 'Baemin', 'Tai Quan'], colors):
                plot_df = unpivot_finance_vegan_day_tbl_with_df[unpivot_finance_vegan_day_tbl_with_df.sub_cate == r]
                # fig.add_trace(
                #     go.Bar(x=[plot_df.ngay_filter, plot_df.main_cate], y=plot_df.value, name=r, marker_color=c, hovertext = plot_df.pct.values.astype('str') + plot_df.main_cate.values, hoverinfo='y+text+name'),
                # )
                fig.add_trace(
                    go.Bar(x=[plot_df.ngay_filter, plot_df.main_cate], y=plot_df.value, name=r, marker_color=c, customdata = np.stack((plot_df.main_cate, plot_df.pct), axis=-1), 
                        hovertemplate='<b> Ngày: %{x[0]} <b> <br> Giá trị: %{y:,.0f}đ <br> Phần trăm: %{customdata[1]}%'),
                )
            for annotation in ['Tong doanh thu', 'Chi chiet khau']:
                plot_df = unpivot_finance_vegan_day_tbl_with_df[unpivot_finance_vegan_day_tbl_with_df.sub_cate == annotation]
                for i, val in enumerate(plot_df.value):
                    fig.add_annotation(x=[plot_df.ngay_filter.iloc[i], plot_df.main_cate.iloc[i]], y=val,
                        text='{:,.0f} đ'.format(val), showarrow=False,
                        yshift=10)
                    
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        
        st.markdown("### Doanh thu thành phần")
        component_list = data['revenue_component_list']
        with st.form(key='form-chon-1-dthu-thanh-phan'):
            col1, col2 = st.columns(2)
            with col1:
                sltd_component= st.selectbox("Chọn loại doanh thu", component_list, index=len(component_list)-1)
            submitted = st.form_submit_button('Thực hiện')
        
        value_pct_THU_unpivot_finance_vegan_day_tbl_with_df = dw_qrdb.get_value_pct_THU_unpivot_finance_vegan_day_tbl_with(selected_day, sltd_component)
        if value_pct_THU_unpivot_finance_vegan_day_tbl_with_df.empty:
            st.warning('Không có dữ liệu với ngày được chọn', icon="⚠️")
        else:
            value_pct_THU_unpivot_finance_vegan_day_tbl_with_df = dw_wd.generate_value_pct_THU_unpivot_finance_vegan_day_tbl_final_df(value_pct_THU_unpivot_finance_vegan_day_tbl_with_df)
            plot_df = value_pct_THU_unpivot_finance_vegan_day_tbl_with_df
            st.info(f'Bạn đã chọn: {sltd_component}', icon="ℹ️")
            if len(selected_day) == 1:
                st.table(plot_df.style.format({'Giá trị': '{:,.0f} đ', 'Phần trăm': '{:,.2f} %'}))
            else:
                fig = make_subplots(specs=[[{"secondary_y": True}]])
                fig.update_layout(
                    template="simple_white",
                )
                fig.update_yaxes(title_text="<b>Giá trị</b>", secondary_y=False)
                fig.update_yaxes(title_text="<b>Phần trăm</b>", secondary_y=True)
                fig.add_trace(
                    go.Bar(x=plot_df['Ngày'], y=plot_df['Giá trị'], name=sltd_component, 
                        hovertemplate='<b> Ngày: %{x} <b> <br> Giá trị: %{y:,.0f}đ'),
                    secondary_y=False,
                )
                fig.add_trace(
                    go.Scatter(x=plot_df['Ngày'], y=plot_df['Phần trăm'], name=sltd_component, 
                        hovertemplate='<b> Ngày: %{x} <b> <br> Phần trăm: %{y:,.2f}%'),
                    secondary_y=True,
                )
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        
        st.markdown("### Doanh thu các thành phần")
        value_type = ['Giá trị', 'Phần trăm']
        with st.form(key='form-chon-dthu-cac-thanh-phan'):
            col1, col2 = st.columns(2)
            with col1:
                sltd_component = st.multiselect('Chọn loại doanh thu', component_list)
            with col2:
                sltd_type = st.selectbox('Chọn kiểu hiển thị', value_type, index=0)
            submitted = st.form_submit_button('Thực hiện')
        if not sltd_component:
            sltd_component = [component_list[-1]]
        value_pct_THU_unpivot_finance_vegan_day_tbl_with_many_df = dw_qrdb.get_value_pct_THU_unpivot_finance_vegan_day_tbl_with_many(selected_day, sltd_component, sltd_type)
        if value_pct_THU_unpivot_finance_vegan_day_tbl_with_many_df.empty:
            st.warning('Không có dữ liệu với ngày được chọn', icon="⚠️")
        else:
            plot_df = value_pct_THU_unpivot_finance_vegan_day_tbl_with_many_df
            st.info(f'Bạn đã chọn: {sltd_component}', icon="ℹ️")
            if len(selected_day) == 1:
                plot_df = dw_wd.generate_value_pct_THU_unpivot_finance_vegan_day_tbl_with_value_type_final_df(plot_df, sltd_type)
                st.table(plot_df)
            else:
                fig = go.Figure()
                fig.update_layout(
                    template="simple_white",
                    xaxis=dict(title_text="Ngày"),
                    yaxis=dict(title_text=sltd_type)
                )
                name_color = []
                if len(sltd_component) == 1:
                    for r, c in zip(data['revenue_component_list'], data['revenue_component_colors']):
                        if r == sltd_component[0]:
                            name_color.append((r, c))
                else:
                    for r, c in zip(data['revenue_component_list'], data['revenue_component_colors']):
                        if r in sltd_component:
                            name_color.append((r, c))       
                for r, c in name_color:
                    plot_df_loop = plot_df[plot_df.sub_cate == r]
                    if sltd_type == 'Giá trị':
                        fig.add_trace(
                            go.Scatter(x=plot_df_loop['ngay_filter'], y=plot_df_loop['value'], name=r, marker_color=c, 
                            hovertemplate='<b> Ngày: %{x} <b> <br> Giá trị: %{y:,.0f}đ'),
                        )
                    else:
                        fig.add_trace(
                            go.Scatter(x=plot_df_loop['ngay_filter'], y=plot_df_loop['pct'], name=r, marker_color=c, 
                            hovertemplate='<b> Ngày: %{x} <b> <br> Phần trăm: %{y:,.2f}%'),
                        )
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)
                

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
        
        st.markdown("### Số phần đã bán trên app (chiết khấu)")
        
        with st.form(key='form-chon-1-mon-an'):
            col1, col2 = st.columns(2)
            with col1:
                sltd_dish = st.selectbox("Chọn món", dish_list, index=len(dish_list)-1)
            submitted = st.form_submit_button('Thực hiện')
            
        if sltd_dish == '...':
            sltd_dish = 'Bún Thái'
            
        if len(selected_day) == 1:
            sale_off_quantity_sales_dishes_vegan_day_tbl_with_single_day_df = dw_qrdb.get_sale_off_quantity_sales_dishes_vegan_day_tbl_with_single_day(selected_day, sltd_dish)
            sale_off_quantity_sales_dishes_vegan_day_tbl_with_single_day_df = dw_wd.generate_sale_off_quantity_sales_dishes_vegan_day_tbl_single_day_df(sale_off_quantity_sales_dishes_vegan_day_tbl_with_single_day_df)
            st.table(sale_off_quantity_sales_dishes_vegan_day_tbl_with_single_day_df.style.format({'Số lượng': '{:.0f}', 'Doanh thu': '{:,.0f}'}))
        else:
            sale_off_quantity_sales_dishes_vegan_day_tbl_with_multi_days_df = dw_qrdb.get_sale_off_quantity_sales_dishes_vegan_day_tbl_with_multi_days(selected_day, sltd_dish)
            sale_off_quantity_sales_dishes_vegan_day_tbl_with_multi_days_df = dw_wd.generate_sale_off_quantity_sales_dishes_vegan_day_tbl_with_multi_days_final_df(sale_off_quantity_sales_dishes_vegan_day_tbl_with_multi_days_df)
            fig = px.bar(sale_off_quantity_sales_dishes_vegan_day_tbl_with_multi_days_df, x='Ngày', y='Số lượng bán', 
                         color='Phân loại', hover_data=['Tên món', 'Doanh thu', 'Phần trăm số lượng', 'Phần trăm doanh thu'], barmode = 'group').update_xaxes(tickangle=90).add_traces(
                        px.line(sale_off_quantity_sales_dishes_vegan_day_tbl_with_multi_days_df, x="Ngày", y="Tổng số lượng bán", hover_data=['Doanh thu', 'Tên món']).update_traces(showlegend=True, name="Tổng").update_layout(bargap=0.1).data
                        )
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)
                       
        st.markdown("### Xếp hạng món bán chạy")
        col1, col2 = st.columns(2)
        with col1:
            top_quantity = st.slider("Top SL:", 1, 20, 3, key='top_best_quantity')
            ranking_quantity_sales_dishes_vegan_day_tbl_with_df = dw_qrdb.get_best_ranking_quantity_sales_dishes_vegan_day_tbl_with(selected_day, top_quantity)
            ranking_quantity_sales_dishes_vegan_day_tbl_pivot_df = dw_wd.generate_best_ranking_quantity_sales_dishes_vegan_day_tbl_pivot_df(ranking_quantity_sales_dishes_vegan_day_tbl_with_df)
            st.table(ranking_quantity_sales_dishes_vegan_day_tbl_pivot_df)
        
        with col2:
            top_revenue = st.slider("Top Doanh thu:", 1, 20, 3, key='top_best_revenue')
            ranking_revenue_sales_dishes_vegan_day_tbl_with_df = dw_qrdb.get_best_ranking_quantity_sales_dishes_vegan_day_tbl_with(selected_day, None, top_revenue)
            ranking_revenue_sales_dishes_vegan_day_tbl_pivot_df = dw_wd.generate_best_ranking_revenue_sales_dishes_vegan_day_tbl_pivot_df(ranking_revenue_sales_dishes_vegan_day_tbl_with_df)        
            st.table(ranking_revenue_sales_dishes_vegan_day_tbl_pivot_df)
        
        st.markdown("### Xếp hạng món bán chậm")
        col1, col2 = st.columns(2)
        with col1:
            top_quantity = st.slider("Top SL:", 1, 20, 3, key='top_worst_quantity')
            ranking_quantity_sales_dishes_vegan_day_tbl_with_df = dw_qrdb.get_worst_ranking_quantity_sales_dishes_vegan_day_tbl_with(selected_day, top_quantity)
            ranking_quantity_sales_dishes_vegan_day_tbl_pivot_df = dw_wd.generate_worst_ranking_quantity_sales_dishes_vegan_day_tbl_pivot_df(ranking_quantity_sales_dishes_vegan_day_tbl_with_df)
            st.table(ranking_quantity_sales_dishes_vegan_day_tbl_pivot_df)
        
        with col2:
            top_revenue = st.slider("Top Doanh thu:", 1, 20, 3, key='top_worst_revenue')
            ranking_revenue_sales_dishes_vegan_day_tbl_with_df = dw_qrdb.get_worst_ranking_quantity_sales_dishes_vegan_day_tbl_with(selected_day, None, top_revenue)
            ranking_revenue_sales_dishes_vegan_day_tbl_pivot_df = dw_wd.generate_worst_ranking_revenue_sales_dishes_vegan_day_tbl_pivot_df(ranking_revenue_sales_dishes_vegan_day_tbl_with_df)        
            st.table(ranking_revenue_sales_dishes_vegan_day_tbl_pivot_df)
    
        st.markdown("### Tổng quan các món")
        with st.form(key='form-chon-tieu-chi-cac-mon'):
            col1, col2 = st.columns(2)
            with col1:
                sltd_criteria = st.selectbox("Chọn tiêu chí", ['Doanh số', 'Doanh thu'], index=0)
            with col2:
                sltd_measure = st.selectbox("Chọn đo lường", ['Tổng cộng', 'Trung bình cộng'], index=0)
            submitted = st.form_submit_button('Thực hiện')
        
        st.info(f'Bạn đã chọn: {selected_day}, {sltd_criteria}, {sltd_measure}', icon="ℹ️") 
        statistics_dishes_quantity_sales_dishes_vegan_tbl_with_df = dw_qrdb.get_statistics_dishes_quantity_sales_dishes_vegan_tbl_with(selected_day, sltd_criteria, sltd_measure)
        statistics_dishes_quantity_sales_dishes_vegan_tbl_with_df = dw_wd.generate_statistics_dishes_quantity_sales_dishes_vegan_tbl_with_df(statistics_dishes_quantity_sales_dishes_vegan_tbl_with_df, sltd_criteria)
        st.table(statistics_dishes_quantity_sales_dishes_vegan_tbl_with_df)
        fig = px.treemap(statistics_dishes_quantity_sales_dishes_vegan_tbl_with_df, path=['Tên món'],values=sltd_criteria, hover_data=["Tỷ trọng"],
                 )
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
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
        