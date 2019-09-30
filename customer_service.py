from dbutil import DB


def get_all_customers():
    db = DB()
    sql = "SELECT * FROM CUSTOMER"
    results = db.executeMultiResult(sql)
    db.close()
    return results

def get_schema():
    db = DB()
    sql = "SELECT COLUMN_NAME FROM USER_TAB_COLUMNS WHERE TABLE_NAME='CUSTOMER';"
    result = db.executeSingleResult(sql)
    db.close()
    return result