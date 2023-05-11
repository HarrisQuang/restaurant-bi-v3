class Query:
    get_ngay_filter_orders_vegan_day_tbl = "SELECT ngay_filter FROM orders_vegan_day order by ngay_number"
    get_total_order_orders_vegan_day_tbl_with = {
        "single_day": "SELECT ngay_filter, total_order FROM orders_vegan_day where ngay_filter = '%s' order by ngay_number ",
        "multi_days": "SELECT ngay_filter, total_order FROM orders_vegan_day where ngay_filter in %s order by ngay_number "
    }
    get_all_finance_vegan_day_tbl_with = {
        "single_day": "SELECT ngay_filter, doanh_thu, grab, baemin, sp_food, tai_quan, chi_phi, ck_grab, ck_baemin, ck_sp_food, pct_baemin, pct_grab, pct_sp_food, pct_tai_quan FROM finance_vegan_day where ngay_filter = '%s' order by ngay_number ",
        "multi_days": "SELECT ngay_filter, doanh_thu, grab, baemin, sp_food, tai_quan, chi_phi, ck_grab, ck_baemin, ck_sp_food, pct_baemin, pct_grab, pct_sp_food, pct_tai_quan FROM finance_vegan_day where ngay_filter in %s order by ngay_number "
    }
    get_distinct_dish_quantity_sales_dishes_vegan_day_tbl = "SELECT distinct ten_mon FROM quantity_sales_dishes_vegan_day order by ten_mon"
    get_sell_quantity_sales_dishes_vegan_day_tbl_with = {
        "single_day_single_dish": "SELECT ngay_number, ngay_filter, ten_mon, sl_ban FROM quantity_sales_dishes_vegan_day where ngay_filter = '%s' and ten_mon = '%s' order by ten_mon, ngay_number",
        "multi_days_multi_dishes": "SELECT ngay_number, ngay_filter, ten_mon, sl_ban FROM quantity_sales_dishes_vegan_day where ngay_filter in %s and ten_mon in %s order by ten_mon, ngay_number",
        "single_day_multi_dishes": "SELECT ngay_number, ngay_filter, ten_mon, sl_ban FROM quantity_sales_dishes_vegan_day where ngay_filter = '%s' and ten_mon in %s order by ten_mon, ngay_number",
        "multi_days_single_dish": "SELECT ngay_number, ngay_filter, ten_mon, sl_ban FROM quantity_sales_dishes_vegan_day where ngay_filter in %s and ten_mon = '%s' order by ten_mon, ngay_number"
    }
    get_ranking_quantity_sales_dishes_vegan_day_tbl_with = {
        "single_day_with_xep_hang_sl_ban": "SELECT ngay_filter, ten_mon, sl_ban, xep_hang_sl_ban FROM quantity_sales_dishes_vegan_day where ngay_filter = '%s' and xep_hang_sl_ban <= %s order by xep_hang_sl_ban",
        "multi_days_with_xep_hang_sl_ban": "SELECT ngay_filter, ten_mon, sl_ban, xep_hang_sl_ban FROM quantity_sales_dishes_vegan_day where ngay_filter in %s and xep_hang_sl_ban <= %s order by xep_hang_sl_ban",
        "single_day_with_xep_hang_tong": "SELECT ngay_filter, ten_mon, tong, xep_hang_tong FROM quantity_sales_dishes_vegan_day where ngay_filter = '%s' and xep_hang_tong <= %s order by xep_hang_tong",
        "multi_days_with_xep_hang_tong": "SELECT ngay_filter, ten_mon, tong, xep_hang_tong FROM quantity_sales_dishes_vegan_day where ngay_filter in %s and xep_hang_tong <= %s order by xep_hang_tong"
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
