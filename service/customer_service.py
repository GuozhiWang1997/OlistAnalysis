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

def draw_customer_histogram(start_date, end_date):
    db = DB()
    sql = '''
        SELECT COUNT(DISTINCT CUSTOMER.CUSTOMER_ID)       AS CNT, 
               TO_CHAR(ORDERR.PURCHASE_TIME, 'YYYY-MM')   AS TIME1                                                                                
        FROM ORDERR,                                                                                                                                                                         
             CUSTOMER                                                                                                                                                                        
        WHERE CUSTOMER.CUSTOMER_ID = ORDERR.CUSTOMER_ID                                                                                                                                      
          AND ORDERR.PURCHASE_TIME < TO_DATE('%s', 'YYYY-MM')                                                                                                                     
          AND ORDERR.PURCHASE_TIME > TO_DATE('%s', 'YYYY-MM')                                                                                                                     
        GROUP BY TO_CHAR(ORDERR.PURCHASE_TIME, 'YYYY-MM')                                                                                                                                    
        ORDER BY TO_DATE(TIME1, 'YYYY-MM') ASC''' % (end_date, start_date)
    results = db.executeMultiResult(sql)
    db.close()
    return results