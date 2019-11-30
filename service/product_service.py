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
    resulsts = db.executeMultiResult(sql)
    db.close()
    return resulsts


def draw_line_product(start_date, end_date, product_id):
    db = DB()
    sql = '''
    SELECT COUNT(*) AS cnt, TO_CHAR(ORDERR.PURCHASE_TIME, 'YYYY-MM') AS time1
    FROM ORDERR,
         ORDER_ITEM,
         PRODUCT
    WHERE ORDERR.ORDER_ID = ORDER_ITEM.ORDER_ID
      AND ORDER_ITEM.PRODUCT_ID = PRODUCT.PRODUCT_ID
      AND PRODUCT.PRODUCT_ID = '%s'
      AND ORDERR.PURCHASE_TIME < TO_DATE('%s', 'YYYY-MM')
      AND ORDERR.PURCHASE_TIME > TO_DATE('%s', 'YYYY-MM')
    GROUP BY TO_CHAR(ORDERR.PURCHASE_TIME, 'YYYY-MM')
    ORDER BY TO_DATE(time1, 'YYYY-MM') ASC''' % (product_id, end_date, start_date)
    print(sql)
    results = db.executeMultiResult(sql)
    db.close()
    return results


def draw_line_all_product():
    db = DB()
    sql = '''
    SELECT *
    FROM (SELECT COUNT(*) cnt, TO_CHAR(PURCHASE_TIME, 'YYYY-MM') timee
          FROM ORDERR
          GROUP BY TO_CHAR(PURCHASE_TIME, 'YYYY-MM'))
    ORDER BY timee'''
    print(sql)
    result = db.executeMultiResult(sql)
    db.close()
    return result


def search_product_selector_by_id(keyword):
    db = DB()
    sql = "SELECT * FROM PRODUCT_SELECTOR WHERE PRODUCT_ID LIKE '%%%s%%'" % keyword
    results = db.executeMultiResult(sql)
    db.close()
    return results


def get_selector_schema():
    db = DB()
    sql = "SELECT COLUMN_NAME FROM USER_TAB_COLUMNS WHERE TABLE_NAME='PRODUCT_SELECTOR'"
    result = db.executeMultiResult(sql)
    db.close()
    return result

    return results

def draw_stacked_map(category_list, start_date, end_date):
    db = DB()
    sql = '''                                                                                                                                                                             
                 SELECT COUNT(DISTINCT ORDERR.ORDER_ID)             SALES,                                                                                                                   
                        PRODUCT.CATEGORY                            CATEGORY,                                                                                                                
                        TO_CHAR(ORDERR.PURCHASE_TIME, 'YYYY-MM')    TIMEE                                                                                                                    
                 FROM ORDERR,                                                                                                                                                                
                      ORDER_ITEM,                                                                                                                                                            
                      PRODUCT                                                                                                                                                                                                                                                                                                                             
                 WHERE ORDERR.ORDER_ID = ORDER_ITEM.ORDER_ID                                                                                                                                 
                   AND ORDER_ITEM.PRODUCT_ID = PRODUCT.PRODUCT_ID                                                                                                                            
                   AND PRODUCT.CATEGORY IN (%s)                                                                                                              
                   AND ORDERR.PURCHASE_TIME > TO_DATE('%s', 'YYYY-MM')                                                                                                            
                   AND ORDERR.PURCHASE_TIME < TO_DATE('%s', 'YYYY-MM')                                                                                                            
                 GROUP BY PRODUCT.CATEGORY, TO_CHAR(ORDERR.PURCHASE_TIME, 'YYYY-MM')                                                                                                      
                 ORDER BY TO_DATE(TIMEE, 'YYYY-MM')   ''' %(category_list, start_date, end_date)
    print(sql)
    results = db.executeMultiResult(sql)
    db.close()
    return results


def draw_satisfactory_histogram(product_id):
    db = DB()
    sql = '''
        SELECT AVG(SCORE), TO_CHAR(REVIEW.CREATION_DATE, 'YYYY-MM') AS TIMEE                                                                                                                 
        FROM ORDERR,                                                                                                                                                                         
             ORDER_ITEM,                                                                                                                                                                     
             PRODUCT,                                                                                                                                                                        
             REVIEW                                                                                                                                                                          
        WHERE ORDERR.ORDER_ID = ORDER_ITEM.ORDER_ID                                                                                                                                          
          AND ORDER_ITEM.PRODUCT_ID = PRODUCT.PRODUCT_ID                                                                                                                                     
          AND PRODUCT.PRODUCT_ID = '%s'                                                                                                                        
          AND ORDERR.ORDER_ID = REVIEW.ORDER_ID                                                                                                                                                                                                                                                                                           
        GROUP BY TO_CHAR(REVIEW.CREATION_DATE, 'YYYY-MM')                                                                                                                                    
        ORDER BY TO_DATE(TIMEE, 'YYYY-MM') ASC  ''' %(product_id)
    results = db.executeMultiResult(sql)
    db.close()
    return results

def see_if_fake_order():
    db = DB()
    sql = '''
        SELECT digit,
               ROUND(COUNT(digit) / (
                   SELECT COUNT(DISTINCT PRODUCT_ID)
                   FROM ORDER_ITEM
               ) * 100, 2) cnt
        FROM (
                 SELECT PRODUCT_ID, substr(COUNT(PRODUCT_ID), 0, 1) digit
                 FROM ORDER_ITEM
                 GROUP BY PRODUCT_ID
             )
        GROUP BY digit
        ORDER BY cnt DESC'''
    results = db.executeMultiResult(sql)
    db.close()
    return results

def see_if_fake_price():
    db = DB()
    sql = '''
        SELECT digit,
           ROUND(COUNT(digit) / (
               SELECT COUNT(*)
               FROM ORDER_ITEM
           ) * 100, 2) cnt
        FROM (
                 SELECT PRODUCT_ID, substr(PRICE, 0, 1) digit
                 FROM ORDER_ITEM
             )
        GROUP BY digit
        ORDER BY digit ASC'''
    results = db.executeMultiResult(sql)
    db.close()
    return results

def see_if_fake_weight():
    db = DB()
    sql = '''
        SELECT digit,
           ROUND(COUNT(digit) / (
               SELECT COUNT(*)
               FROM PRODUCT
           ) * 100, 2) cnt
        FROM (
                 SELECT PRODUCT_ID, substr(WEIGHT, 0, 1) digit
                 FROM PRODUCT
             )
        GROUP BY digit
        ORDER BY digit ASC'''
    results = db.executeMultiResult(sql)
    db.close()
    return results