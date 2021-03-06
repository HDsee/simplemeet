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
                                            pool_size=5,
                                            pool_reset_session=True,
                                            host=rdsHost,
                                            database=rdsDatabease,
                                            user=rdsUser,
                                            password=rdsPassword,
                                            port=3306)


userApi = Blueprint( 'userApi', __name__)


#取得當前使用者資訊
@userApi.route('/user', methods=['GET'])
def api_user():
    # 登入中
    if "user" in session:
        id = session['id']
        user = session['user']
        email = session['email']
        data = {
            "data":{
                "id":id,
                "user":user,
                "email":email
            }
        }
        return jsonify(data)

    # 沒登入
    data = {"data": None}
    return jsonify(data)

# 註冊功能
@userApi.route('/user', methods=['POST'])
def signup():
    try:
        data = request.json
        name = data['name']
        email = data['email']
        password = data['password']
        db=connection_pool.get_connection()
        cursor = db.cursor()
        cursor.execute('select * from `member` where email=%s',(email,))
        user = cursor.fetchone()
        #驗證資料
        if (not user) and (name != None) and (password != None):
            pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if re.fullmatch(pattern, email):
                cursor.execute('select * from `member` where name=%s',(name,))
                userName = cursor.fetchone()
                print(name,email,password)
                if(not userName):
                    cursor.execute('INSERT INTO `member` (name,email,password) VALUES (%s,%s,%s)',(name,email,password))
                    data = {"ok": True}
                    return jsonify(data), 200
                else:
                    data = {
                    "error": True,
                    "message": "註冊失敗，重複的姓名"
                }
                db.rollback()
                return jsonify(data), 400
            else:
                data = {
                    "error": True,
                    "message": "註冊失敗，email、帳號、密碼格式錯誤"
                }
                db.rollback()
                return jsonify(data), 400
        # email重複
        else: 
            data = {
                "error": True,
                "message": "註冊失敗，重複的email"
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
    

# 登入功能
@userApi.route('/user', methods=['PATCH'])
def signin():
    try:
        data = request.json
        email = data['email']
        password = data['password']
        db=connection_pool.get_connection()
        cursor = db.cursor()
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if (re.fullmatch(pattern, email)) and (password != None):
            cursor.execute('select * from `member` where email=%s and password=%s',(email,password))
            user = cursor.fetchone()
            # 登入成功
            if user:
                session['id'] = user[0]
                session['user'] = user[1]
                session['email'] = user[2]
                data = {"ok": True}
                return jsonify(data)
            # 登入失敗
            else:
                data = {
                    "error": True,
                    "message": "信箱或密碼輸入錯誤"
                }
                return jsonify(data), 400
        else:
            data = {
                "error": True,
                "message": "登入失敗，email或密碼格式錯誤"
            }
            db.rollback()
            return jsonify(data), 400

    # 伺服器錯誤
    except:
        data = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        cursor.close()
        db.close()
        return jsonify(data), 500
    finally:
        cursor.close()
        db.close()

# 登出功能
@userApi.route('/user', methods=['DELETE'])
def singout():
    # 登出
    data = {"ok": True}
    session.pop('user')
    return jsonify(data)

