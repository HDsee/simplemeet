from flask import *
from flask import session
from connector import connection_pool
from datetime import date, datetime
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


memberApi = Blueprint( 'memberApi', __name__)
friendApi = Blueprint( 'friendApi', __name__)
messageApi = Blueprint( 'messageApi', __name__)
imgApi = Blueprint( 'imgApi', __name__)

# 會員資料修改
@memberApi.route('/member', methods=['POST'])
def memberUpdate():
    try:
        data = request.json
        name = data['name']
        email = data['email']
        password = data['password']
        db = connection_pool.get_connection()
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
def memberGet():
    try:
        data = request.json
        email = data['email']
        db = connection_pool.get_connection()
        cursor = db.cursor()
        if (email != session['email']):
            cursor.execute('select * from `member` where email=%s',(email,))
            user = cursor.fetchone()
            if ( user ):
                print(user[1])
                data = {
                    "user": user[1],
                    "email": email,
                    "img": user[4]
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
    except :
        data = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        return jsonify(data), 500
    finally:
        cursor.close()
        db.close()

# 會員圖片修改
@imgApi.route('/img', methods=['POST'])
def memberImgUpdate():

    image = request.files['file'] 
    rdsUrl = "https://d2xfotk02kb3rl.cloudfront.net/"+ session['user'] + image.filename
    imgName = session['user'] + image.filename

    s3 = boto3.client('s3', 
        aws_access_key_id=s3ID,
        aws_secret_access_key=s3Key
    )

    try:
        s3.upload_fileobj(image, "hdts3", imgName)
    except:
        return {"error": True, "message": "s3伺服器內部錯誤"}

    try:
        db = connection_pool.get_connection()
        cursor = db.cursor(buffered = True, dictionary = True)
        cursor.execute('UPDATE `member` SET img =%s WHERE name = %s',(rdsUrl,session['user']))
        cursor.execute('UPDATE `friends` SET friendimg =%s WHERE friendname = %s',(rdsUrl,session['user']))
        session['img'] = rdsUrl
    except Exception as e:
        print(e)
        db.rollback()
        return {"error": True, "message": "rds伺服器內部錯誤"}
    finally:
        cursor.close()
        db.commit()
        db.close()

    return {'ok': True}, 200

    
#好友資料取得
@friendApi.route('/friend', methods=['GET'])
def friendGet():
    try:
        email = session['email']
        db = connection_pool.get_connection()
        cursor = db.cursor()
        cursor.execute('select friendname,friendimg from `friends` where email=%s ',(email,))
        friend = cursor.fetchall()
        # 好友資料查詢
        if friend :
            data = {
            "data":{"frined":friend}
            }
            return jsonify(data)
        # 沒有好友
        data = {"data": None}
        return jsonify(data)

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
@friendApi.route('/friend', methods=['POST'])
def joinFiend():
    try:
        data = request.json
        name = session['user']
        email = session['email']
        friendname = data['name']
        friendemail = data['email']
        friendimg = data['img']
        db = connection_pool.get_connection()
        cursor = db.cursor()
        cursor.execute('select friendname from `friends` where email=%s and friendemail=%s',(email,friendemail))
        friend = cursor.fetchone()
        # 添加好友
        if (not friend  ):
            cursor.execute('INSERT INTO `friends` (email,name,friendemail,friendname,friendimg) VALUES (%s,%s,%s,%s,%s)',(email,name,friendemail,friendname,friendimg))
            data = {"ok": True}
            return jsonify(data), 200
        # 好友重複
        elif (friend[0] == friendname):
            data = {
                "error": True,
                "message": "好友添加失敗，已經成為好友"
            }
            db.rollback()
            return jsonify(data), 400

    # 伺服器錯誤
    except Exception as e:
        print(e)
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


# 歷史訊息取得
@messageApi.route('/message', methods=['PATCH'])
def messageGet():
    try:
        data = request.json
        search = data['sender'] + data['receiver']
        research = data['receiver'] + data['sender']
        db = connection_pool.get_connection()
        cursor = db.cursor()
        cursor.execute('select img from `member` where name=%s  ',(data['receiver'],))
        img = cursor.fetchone()
        #有歷史訊息
        if  img:
            cursor.execute('select sender,receiver,message,time from `message` where search=%s or search=%s  ',(search,research))
            history = cursor.fetchall()
            data = {
                "data": history,
                "img": img
            }
            return jsonify(data),200
        # #沒有歷史訊息
        else:
            data = {"data": None}
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

# 訊息儲存
@messageApi.route('/message', methods=['POST'])
def messageStore():
    try:
        data = request.json
        date = datetime.now().strftime('%Y%m%d%H%M%S')
        sender = data['sender']
        receiver = data['receiver']
        message = data['message']
        search = sender+receiver
        db = connection_pool.get_connection()
        cursor = db.cursor()
        cursor.execute('INSERT INTO `message` (search,sender,receiver,message,time) VALUES (%s,%s,%s,%s,%s)',(search,sender,receiver,message,date))
        data = {"ok": True}
        return jsonify(data), 200

    # 伺服器錯誤
    except Exception as e:
        print(e)
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