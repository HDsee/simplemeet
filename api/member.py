from flask import *
from flask import session
import mysql.connector
from mysql.connector import pooling
import re
import boto3

# 讀取.env的隱藏資料
from dotenv import load_dotenv
import os


load_dotenv()
rdsHost = os.getenv("rdsHost")
rdsDatabease = os.getenv("rdsDatabase")
rdsUser = os.getenv("rdsUser")
rdsPassword = os.getenv("rdsPassword")
s3ID = os.getenv("s3ID")
s3Key = os.getenv("s3Key")

connection_pool = pooling.MySQLConnectionPool(pool_name="db",
                                            pool_size=10,
                                            pool_reset_session=True,
                                            host=rdsHost,
                                            database=rdsDatabease,
                                            user=rdsUser,
                                            password=rdsPassword,
                                            port=3306)


memberApi = Blueprint( 'memberApi', __name__)




# 註冊功能
@memberApi.route('/member', methods=['POST'])
def memberupdate():
    try:
        data = request.json
        name = data['name']
        email = data['email']
        password = data['password']
        db=connection_pool.get_connection()
        cursor = db.cursor()
        cursor.execute('select * from `member` where name=%s',(email,))
        email = cursor.fetchone()

        #驗證資料
        if (name != None) and (password != None):
            cursor.execute('UPDATE `member` SET name =%s, password=%s WHERE email = %s',(name,password,email))
            data = {"ok": True}
            session['user'] = name
            return jsonify(data), 200
            
        # email重複
        else:
            data = {
                "error": True,
                "message": "修改失敗，請輸入姓名、密碼"
            }
            db.rollback()
            return jsonify(data), 400

    # 伺服器錯誤
    except:
        data = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        db.rollback()
        return jsonify(data), 500
    finally:
        db.commit()
        cursor.close()
        db.close()
    

