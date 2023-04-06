class Query:
    get_ngay_filter_orders_vegan_day_tbl = "SELECT ngay_filter FROM orders_vegan_day order by ngay_number"
    get_total_order_orders_vegan_day_tbl_with = {
        "single_day": "SELECT ngay_filter, total_order FROM orders_vegan_day where ngay_filter = '%s' order by ngay_number ",
        "multi_days": "SELECT ngay_filter, total_order FROM orders_vegan_day where ngay_filter in %s order by ngay_number "
    }