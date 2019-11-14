from dbutil import DB


def search_seller_by_id(keyword):
    db = DB()
    sql = "SELECT * FROM SELLER WHERE SELLER_ID LIKE '%%%s%%'" % keyword
    results = db.executeMultiResult(sql)
    db.close()
    return results


def get_schema():
    db = DB()
    sql = "SELECT COLUMN_NAME FROM USER_TAB_COLUMNS WHERE TABLE_NAME='SELLER'"
    result = db.executeMultiResult(sql)
    db.close()
    return result
