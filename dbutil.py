import cx_Oracle


class DB:
    conn = None
    cursor = None

    def __init__(self, username="guozhi", password="wf8211521", address="oracle.cise.ufl.edu/orcl"):
        self.conn = cx_Oracle.connect(username, password, address, encoding="utf-8")

    def executeSingleResult(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        toReturn = cursor.fetchone()[0]
        cursor.close()
        return toReturn

    def executeMultiResult(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        toReturn = cursor.fetchall()
        cursor.close()
        return toReturn

    def executeInsert(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        cursor.close()

    def save(self):
        self.conn.commit()

    def close(self):
        self.conn.close()
