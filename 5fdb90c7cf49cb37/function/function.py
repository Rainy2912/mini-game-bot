from ntpath import join
import sqlite3

def join_sql():
    try:
        sql = sqlite3.connect('user.db')
        woogi = sql.cursor()
        return sql, woogi
    except:
        return False, False

def check_data_user(id):
    sql, woogi = join_sql()
    if sql:
        woogi.execute(f"SELECT * FROM user_info WHERE user_id = {id}")
        sql.commit()
        result = woogi.fetchone()
        sql.close()
        if result is None:
            return False
        else:
            return result
    else:
        return False