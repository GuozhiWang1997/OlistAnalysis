from dbutil import DB


def get_customers_page(start=0, end=500):
    db = DB()
    sql = "SELECT * FROM (" \
          "     SELECT ROWNUM AS ROWNUMM, t.*  FROM CUSTOMER t" \
          ") WHERE ROWNUMM < " + str(end) + " AND ROWNUMM >= " + str(start)
    results = db.executeMultiResult(sql)
    db.close()
    return results

def get_schema():
    db = DB()
    sql = "SELECT COLUMN_NAME FROM USER_TAB_COLUMNS WHERE TABLE_NAME='CUSTOMER'"
    result = db.executeMultiResult(sql)
    db.close()
    return result