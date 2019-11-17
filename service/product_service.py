from dbutil import DB


def search_product_by_id(keyword):
    db = DB()
    sql = "SELECT * FROM PRODUCT WHERE PRODUCT_ID LIKE '%%%s%%'" % keyword
    results = db.executeMultiResult(sql)
    db.close()
    return results


def get_schema():
    db = DB()
    sql = "SELECT COLUMN_NAME FROM USER_TAB_COLUMNS WHERE TABLE_NAME='PRODUCT'"
    result = db.executeMultiResult(sql)
    db.close()
    return result


def draw_line_product(start_date, end_date, product_id):
    db = DB()
    sql = "select count(*) as cnt,to_char(orderr.purchase_time,'YYYY-MM') as time1 \
    from orderr,order_item,product \
    where orderr.order_id=order_item.order_id \
    and order_item.product_id = product.product_id \
    and product.product_id='%s' \
    and orderr.purchase_time<TO_DATE('%s', 'YYYY-MM') \
    and orderr.purchase_time>TO_DATE('%s', 'YYYY-MM')\
    group by to_char(orderr.purchase_time,'YYYY-MM')\
    order by TO_DATE(time1,'YYYY-MM') asc" % (product_id, end_date, start_date)
    print(sql)
    result = db.executeMultiResult(sql)
    db.close()
    return result