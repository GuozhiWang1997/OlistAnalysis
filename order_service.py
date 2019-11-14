from dbutil import DB


def search_order_by_customer_id(keyword):
    db = DB()
    sql = "SELECT * FROM ORDERR WHERE CUSTOMER_ID LIKE '%%%s%%'" % keyword
    results = db.executeMultiResult(sql)
    db.close()
    return results


def search_order_by_order_id(keyword):
    db = DB()
    sql = "SELECT * FROM ORDERR WHERE ORDER_ID LIKE '%%%s%%'" % keyword
    results = db.executeMultiResult(sql)
    db.close()
    return results


def get_schema():
    db = DB()
    sql = "SELECT COLUMN_NAME FROM USER_TAB_COLUMNS WHERE TABLE_NAME='ORDERR'"
    result = db.executeMultiResult(sql)
    db.close()
    return result
