from dbutil import DB


def draw_thermal_location (date):
    db = DB()
    sql = '''
       SELECT ROUND(AVG(GEOLOC.LATITUDE), 2)  AS LATITUDE,
              ROUND(AVG(GEOLOC.LONGITUDE), 2) AS LONGITUDE,
              COUNT(ORDERR.ORDER_ID)          AS ORDER_NUNBER,
              UTL_RAW.CAST_TO_VARCHAR2(NLSSORT(CITY, 'nls_sort=binary_ai')) AS CITY
        FROM ORDERR,
             CUSTOMER,
             GEOLOC
        WHERE GEOLOC.ZIPCODE = CUSTOMER.ZIPCODE
          AND CUSTOMER.CUSTOMER_ID = ORDERR.CUSTOMER_ID
          AND ORDERR.PURCHASE_TIME < TO_DATE('%s', 'YYYY-MM-DD')
        GROUP BY UTL_RAW.CAST_TO_VARCHAR2(NLSSORT(CITY, 'nls_sort=binary_ai'))''' % date
    print(sql)
    results = db.executeMultiResult(sql)
    db.close()
    return results
