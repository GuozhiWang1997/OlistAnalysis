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
    results = db.executeMultiResult(sql)
    db.close()
    return results


def get_cities_by_state(state):
    db = DB()
    sql = '''
    SELECT DISTINCT (UTL_RAW.CAST_TO_VARCHAR2(NLSSORT(CITY, 'nls_sort=binary_ai'))) city FROM GEOLOC
    WHERE STATE = '%s'
    ORDER BY city
    ''' % (state)
    results = db.executeMultiResult(sql)
    db.close()

    return results


def draw_delivery_histogram(state1,city1, state2, city2):
    db = DB()
    sql = '''
        SELECT ROUND(AVG(ORDERR.DELIVERING_TIME                                                                                                                                                    
            - ORDERR.PURCHASE_TIME), 2)                    AS PREP_TIME,                                                                                                                     
               ROUND(AVG(ORDERR.RECEIVING_TIME                                                                                                                                                     
                   - ORDERR.DELIVERING_TIME), 2)           AS DELI_TIME,                                                                                                                     
               TO_CHAR(ORDERR.PURCHASE_TIME, 'YYYY-MM') AS TIME1                                                                                                                          
        FROM ORDERR,                                                                                                                                                                         
             CUSTOMER,                                                                                                                                                                       
             ORDER_ITEM,                                                                                                                                                                     
             SELLER                                                                                                                                                                          
        WHERE CUSTOMER.CUSTOMER_ID = ORDERR.CUSTOMER_ID                                                                                                                                      
          AND CUSTOMER.ZIPCODE IN                                                                                                                                                            
              (SELECT ZIPCODE                                                                                                                                                                
               FROM GEOLOC                                                                                                                                                                   
               WHERE GEOLOC.STATE = '%s' 
               AND GEOLOC.CITY = '%s'                                                                                                                                                    
              )                                                                                                                                                                              
          AND SELLER.ZIPCODE IN                                                                                                                                                              
              (SELECT ZIPCODE                                                                                                                                                                
               FROM GEOLOC                                                                                                                                                                   
               WHERE GEOLOC.STATE = '%s'
               AND GEOLOC.CITY = '%s'     )                                                                                                                                                    
          AND ORDERR.STATUS = 'delivered'                                                                                                                                                    
          AND ORDER_ITEM.SELLER_ID = SELLER.SELLER_ID                                                                                                                                        
          AND ORDERR.ORDER_ID = ORDER_ITEM.ORDER_ID                                                                                                                                          
        GROUP BY TO_CHAR(ORDERR.PURCHASE_TIME, 'YYYY-MM')                                                                                                                                 
        ORDER BY TO_DATE(TIME1, 'YYYY-MM') ASC''' % (state1,city1, state2, city2)
    results = db.executeMultiResult(sql)
    db.close()
    return results