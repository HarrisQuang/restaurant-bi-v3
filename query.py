class Query:
    get_ngay_filter_orders_vegan_day_tbl = "SELECT ngay_filter FROM orders_vegan_day order by ngay_number"
    get_total_order_orders_vegan_day_tbl_with = {
        "single_day": "SELECT ngay_filter, total_order FROM orders_vegan_day where ngay_filter = '%s' order by ngay_number ",
        "multi_days": "SELECT ngay_filter, total_order FROM orders_vegan_day where ngay_filter in %s order by ngay_number "
    }
    get_distinct_dish_sell_quantity_dishes_vegan_day_tbl = "SELECT distinct ten_mon FROM sell_quantity_dishes_vegan_day order by ten_mon"
    get_sell_quantity_dishes_vegan_day_tbl_with = {
        "single_day_single_dish": "SELECT ngay_number, ngay_filter, ten_mon, sl_ban FROM sell_quantity_dishes_vegan_day where ngay_filter = '%s' and ten_mon = '%s' order by ten_mon, ngay_number",
        "multi_days_multi_dishes": "SELECT ngay_number, ngay_filter, ten_mon, sl_ban FROM sell_quantity_dishes_vegan_day where ngay_filter in %s and ten_mon in %s order by ten_mon, ngay_number",
        "single_day_multi_dishes": "SELECT ngay_number, ngay_filter, ten_mon, sl_ban FROM sell_quantity_dishes_vegan_day where ngay_filter = '%s' and ten_mon in %s order by ten_mon, ngay_number",
        "multi_days_single_dish": "SELECT ngay_number, ngay_filter, ten_mon, sl_ban FROM sell_quantity_dishes_vegan_day where ngay_filter in %s and ten_mon = '%s' order by ten_mon, ngay_number"
    }