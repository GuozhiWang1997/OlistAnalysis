from dbutil import DB


def search_customer_by_keyword(keyword):
    db = DB()
    sql = "SELECT * FROM CUSTOMER WHERE CUSTOMER_ID LIKE '%%%s%%'" % keyword
    results = db.executeMultiResult(sql)
    db.close()
    return results


def get_schema():
    db = DB()
    sql = "SELECT COLUMN_NAME FROM USER_TAB_COLUMNS WHERE TABLE_NAME='CUSTOMER'"
    result = db.executeMultiResult(sql)
    db.close()
    return result
