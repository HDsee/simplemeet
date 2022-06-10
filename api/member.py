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
friendApi = Blueprint( 'friendApi', __name__)

# 會員資料修改
@memberApi.route('/member', methods=['POST'])
def memberupdate():
    try:
        data = request.json
        name = data['name']
        email = data['email']
        password = data['password']
        db=connection_pool.get_connection()
        cursor = db.cursor()
        cursor.execute('select * from `member` where name=%s',(name,))
        userName = cursor.fetchone()

        #驗證資料
        if (not userName ) and (password != None) and (name != None):
            cursor.execute('UPDATE `member` SET name =%s, password=%s WHERE email = %s',(name,password,email))
            cursor.execute('UPDATE `friends` SET name =%s WHERE email = %s',(name,email)) 
            cursor.execute('UPDATE `friends` SET friendname =%s WHERE friendemail = %s',(name,email))
            data = {"ok": True}
            session['user'] = name
            return jsonify(data), 200
            
        # email重複
        else:
            data = {
                "error": True,
                "message": "修改失敗，重複的姓名"
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


# 會員資料比對
@memberApi.route('/member', methods=['PATCH'])
def memberget():
    try:
        data = request.json
        email = data['email']
        db=connection_pool.get_connection()
        cursor = db.cursor()
        if (email != session['email']):
            cursor.execute('select * from `member` where email=%s',(email,))
            user = cursor.fetchone()
            if ( user ):
                print(user[1])
                data = {
                    "user": user[1],
                    "email": email
                }
                return jsonify(data)
            else:
                data = {
                    "error": True,
                    "message": "未註冊的email"
                }
                return jsonify(data), 400
        else:
            data = {
                "error": True,
                "message": "Dont enter your email !!"
            }
            return jsonify(data), 400
    # 伺服器錯誤
    except Exception as e:
        print(e)
        data = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        return jsonify(data), 500
    finally:
        cursor.close()
        db.close()

    

# 好友資料增加
@friendApi.route('/member', methods=['POST'])
def joinfiend():
    try:
        data = request.json
        name = session['user']
        email = session['email']
        friendname = data['name']
        friendemail = data['email']
        db=connection_pool.get_connection()
        cursor = db.cursor()
        cursor.execute('select frinedname from `friends` where email=%s and friendemail=%s',(email,friendemail))
        friend = cursor.fetchone()

        #驗證資料
        if (friend != friendname ):
            print(friend)
            data = {"ok": True}
            session['user'] = name
            return jsonify(data), 200
            
        # 好友重複
        else:
            data = {
                "error": True,
                "message": "好友添加失敗，已經成為好友"
            }
            return jsonify(data), 400

    # 伺服器錯誤
    except:
        data = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        return jsonify(data), 500
    finally:
        db.commit()
        cursor.close()
        db.close()