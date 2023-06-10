class Query:
    get_ngay_filter_orders_vegan_day_tbl = "SELECT ngay_filter FROM orders_vegan_day order by ngay_number"
    get_total_order_orders_vegan_day_tbl_with = {
        "single_day": "SELECT ngay_filter, total_order FROM orders_vegan_day where ngay_filter = '%s' order by ngay_number ",
        "multi_days": "SELECT ngay_filter, total_order FROM orders_vegan_day where ngay_filter in %s order by ngay_number "
    }
    get_unpivot_finance_vegan_day_tbl_with = {
        "single_day": "SELECT ngay_filter, main_cate, sub_cate, value, pct from unpivot_finance_vegan_day where ngay_filter = '%s' order by ngay_number ",
        "multi_days": "SELECT ngay_filter, main_cate, sub_cate, value, pct from unpivot_finance_vegan_day where ngay_filter in %s order by ngay_number "
    }
    get_distinct_dish_quantity_sales_dishes_vegan_day_tbl = "SELECT distinct ten_mon FROM quantity_sales_dishes_vegan_day order by ten_mon"
    get_sell_quantity_sales_dishes_vegan_day_tbl_with = {
        "single_day_single_dish": "SELECT ngay_number, ngay_filter, ten_mon, sl_ban FROM quantity_sales_dishes_vegan_day where ngay_filter = '%s' and ten_mon = '%s' order by ten_mon, ngay_number",
        "multi_days_multi_dishes": "SELECT ngay_number, ngay_filter, ten_mon, sl_ban FROM quantity_sales_dishes_vegan_day where ngay_filter in %s and ten_mon in %s order by ten_mon, ngay_number",
        "single_day_multi_dishes": "SELECT ngay_number, ngay_filter, ten_mon, sl_ban FROM quantity_sales_dishes_vegan_day where ngay_filter = '%s' and ten_mon in %s order by ten_mon, ngay_number",
        "multi_days_single_dish": "SELECT ngay_number, ngay_filter, ten_mon, sl_ban FROM quantity_sales_dishes_vegan_day where ngay_filter in %s and ten_mon = '%s' order by ten_mon, ngay_number"
    }
    get_best_ranking_quantity_sales_dishes_vegan_day_tbl_with = {
        "single_day_with_xep_hang_sl_ban_chay": "SELECT ngay_filter, ten_mon, sl_ban, xep_hang_sl_ban_chay FROM quantity_sales_dishes_vegan_day where ngay_filter = '%s' and xep_hang_sl_ban_chay <= %s order by xep_hang_sl_ban_chay",
        "multi_days_with_xep_hang_sl_ban_chay": "SELECT ngay_filter, ten_mon, sl_ban, xep_hang_sl_ban_chay FROM quantity_sales_dishes_vegan_day where ngay_filter in %s and xep_hang_sl_ban_chay <= %s order by xep_hang_sl_ban_chay",
        "single_day_with_xep_hang_tong_ban_chay": "SELECT ngay_filter, ten_mon, tong, xep_hang_tong_ban_chay FROM quantity_sales_dishes_vegan_day where ngay_filter = '%s' and xep_hang_tong_ban_chay <= %s order by xep_hang_tong_ban_chay",
        "multi_days_with_xep_hang_tong_ban_chay": "SELECT ngay_filter, ten_mon, tong, xep_hang_tong_ban_chay FROM quantity_sales_dishes_vegan_day where ngay_filter in %s and xep_hang_tong_ban_chay <= %s order by xep_hang_tong_ban_chay"
    }
    get_worst_ranking_quantity_sales_dishes_vegan_day_tbl_with = {
        "single_day_with_xep_hang_sl_ban_cham": "SELECT ngay_filter, ten_mon, sl_ban, xep_hang_sl_ban_cham FROM quantity_sales_dishes_vegan_day where ngay_filter = '%s' and xep_hang_sl_ban_cham <= %s order by xep_hang_sl_ban_cham",
        "multi_days_with_xep_hang_sl_ban_cham": "SELECT ngay_filter, ten_mon, sl_ban, xep_hang_sl_ban_cham FROM quantity_sales_dishes_vegan_day where ngay_filter in %s and xep_hang_sl_ban_cham <= %s order by xep_hang_sl_ban_cham",
        "single_day_with_xep_hang_tong_ban_cham": "SELECT ngay_filter, ten_mon, tong, xep_hang_tong_ban_cham FROM quantity_sales_dishes_vegan_day where ngay_filter = '%s' and xep_hang_tong_ban_cham <= %s order by xep_hang_tong_ban_cham",
        "multi_days_with_xep_hang_tong_ban_cham": "SELECT ngay_filter, ten_mon, tong, xep_hang_tong_ban_cham FROM quantity_sales_dishes_vegan_day where ngay_filter in %s and xep_hang_tong_ban_cham <= %s order by xep_hang_tong_ban_cham"
    }
    get_sale_off_quantity_sales_dishes_vegan_day_tbl_with_multi_days = '''
                                                                        select *
                                                                        from (SELECT ngay_number, ngay_filter, ngay, ten_mon, sl_ban, float8(tong) tong, 'KM' main_cate,
                                                                        sl_ban_km sl_ban_cate, float8(tong_km) tong_cate, percent_sl_ban_km percent_sl, percent_tong_km percent_tong
                                                                        FROM quantity_sales_dishes_vegan_day
                                                                        union all
                                                                        SELECT ngay_number, ngay_filter, ngay, ten_mon, sl_ban, float8(tong) tong, 'Not KM' main_cate,
                                                                        sl_ban_ko_km sl_ban_cate, float8(tong_ko_km) tong_cate, percent_sl_ban_ko_km percent_sl, percent_tong_ko_km percent_tong
                                                                        FROM quantity_sales_dishes_vegan_day) tbl
                                                                        where tbl.ngay_filter in %s and tbl.ten_mon = '%s' order by ngay_number
                                                                        '''
    get_sale_off_quantity_sales_dishes_vegan_day_tbl_with_single_day = "SELECT ngay_filter, ten_mon, sl_ban, tong, sl_ban_km_display, sl_ban_ko_km_display, tong_km_display, tong_ko_km_display FROM quantity_sales_dishes_vegan_day where ngay_filter = '%s' and ten_mon = '%s' order by ngay_number"
    get_value_pct_THU_unpivot_finance_vegan_day_tbl_with = {
        "single_day_with_sub_cate": "select ngay_filter, value, pct from unpivot_finance_vegan_day where ngay_filter = '%s' and sub_cate = '%s' order by ngay_number",
        "multi_days_with_sub_cate": "select ngay_filter, value, pct from unpivot_finance_vegan_day where ngay_filter in %s and sub_cate = '%s' order by ngay_number"
    }
    get_value_pct_THU_unpivot_finance_vegan_day_tbl_with_many = {
        "single_day_single_component": "select ngay_filter, sub_cate, value, pct from unpivot_finance_vegan_day where ngay_filter = '%s' and sub_cate = '%s' order by ngay_number",
        "single_day_multi_components": "select ngay_filter, sub_cate, value, pct from unpivot_finance_vegan_day where ngay_filter = '%s' and sub_cate in %s order by ngay_number",
        "multi_days_single_component": "select ngay_filter, sub_cate, value, pct from unpivot_finance_vegan_day where ngay_filter in %s and sub_cate = '%s' order by ngay_number",
        "multi_days_multi_components": "select ngay_filter, sub_cate, value, pct from unpivot_finance_vegan_day where ngay_filter in %s and sub_cate in %s order by ngay_number"
    }
    get_statistics_dishes_quantity_sales_dishes_vegan_tbl_with = {
        "single_day": "SELECT ten_mon, %s(%s) FROM quantity_sales_dishes_vegan_day where ngay_filter = '%s' group by ten_mon",
        "multi_days": "SELECT ten_mon, %s(%s) FROM quantity_sales_dishes_vegan_day where ngay_filter in %s group by ten_mon"
    }