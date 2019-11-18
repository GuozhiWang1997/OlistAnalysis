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
        SELECT COUNT(*) AS CNT, TO_CHAR(ORDERR.PURCHASE_TIME, 'YYYY-MM') AS TIME1                                                                                                            
        FROM ORDERR,                                                                                                                                                                         
             ORDER_ITEM,                                                                                                                                                                     
             PRODUCT                                                                                                                                                                         
        WHERE ORDERR.ORDER_ID = ORDER_ITEM.ORDER_ID                                                                                                                                          
          AND ORDER_ITEM.PRODUCT_ID = PRODUCT.PRODUCT_ID                                                                                                                                     
          AND PRODUCT.PRODUCT_ID = '%s'                                                                                                                                                      
          AND ORDERR.PURCHASE_TIME < TO_DATE('%s', 'YYYY-MM')                                                                                                                                
          AND ORDERR.PURCHASE_TIME > TO_DATE('%s', 'YYYY-MM')                                                                                                                                
        GROUP BY TO_CHAR(ORDERR.PURCHASE_TIME, 'YYYY-MM')                                                                                                                                    
        ORDER BY TO_DATE(TIME1, 'YYYY-MM') ASC ''' % (product_id, end_date, start_date)
    print(sql)
    results = db.executeMultiResult(sql)
    db.close()
    return results

def draw_stacked_map(category_list, start_date, end_date):
    db = DB()
    sql = '''                                                                                                                                                                             
                 SELECT COUNT(DISTINCT ORDERR.ORDER_ID)             SALES,                                                                                                                   
                        PRODUCT.CATEGORY                            CATEGORY,                                                                                                                
                        TO_CHAR(ORDERR.PURCHASE_TIME, 'YYYY-MM') TIMEE                                                                                                                    
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