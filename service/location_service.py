from dbutil import DB


def draw_thermal_location (city_name, state_name):
    db = DB()
    sql = '''
        SELECT GEOLOC.LATITUDE, GEOLOC.LONGITUDE, COUNT(ORDERR.ORDER_ID)                                                                                                                   
        FROM ORDERR,                                                                                                                                                                   
             CUSTOMER,                                                                                                                                                                 
             GEOLOC                                                                                                                                                                    
        WHERE GEOLOC.CITY = '%s'                                                                                                                                                       
          AND GEOLOC.STATE = '%s'                                                                                                                                                      
          AND GEOLOC.ZIPCODE = CUSTOMER.ZIPCODE                                                                                                                                        
          AND CUSTOMER.CUSTOMER_ID = ORDERR.CUSTOMER_ID                                                                                                                                
        GROUP BY GEOLOC.LATITUDE, GEOLOC.LONGITUDE''' % (city_name, state_name)
    print(sql)
    results = db.executeMultiResult(sql)
    db.close()
    return results
