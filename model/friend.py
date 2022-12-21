from flask import *
from flask import session
from connector import connection_pool

import re


class friend:
    #好友資料取得
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
    def friendJoin():
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