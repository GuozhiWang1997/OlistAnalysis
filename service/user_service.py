from dbutil import DB


def check_if_user_existed(username, email):
    db = DB()
    sql = "SELECT COUNT(*) FROM USERR WHERE USERNAME='%s' OR EMAIL='%s'" % (username, email)
    result = db.executeSingleResult(sql)
    db.close()
    if result > 0:
        return True
    else:
        return False


def register_new_user(username, email, password):
    try:
        db = DB()
        sql = "INSERT INTO USERR VALUES ('%s', '%s', '%s')" % (email, username, password)
        db.executeNoResult(sql)
        db.save()
        db.close()
        return True
    except:
        return False


def check_email_password(email, password):
    db = DB()
    sql = "SELECT PASSWORD FROM USERR WHERE email='%s'" % (email)
    result = db.executeSingleResult(sql)
    db.close()
    if result == password:
        return True
    else:
        return False


def get_name_by_email(email):
    db = DB()
    sql = "SELECT USERNAME FROM USERR WHERE EMAIL='%s'" % (email)
    result = db.executeSingleResult(sql)
    db.close()
    return result