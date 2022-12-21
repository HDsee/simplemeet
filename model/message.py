from flask import *
from flask import session
from connector import connection_pool
from datetime import date, datetime

import re



class message:
    # 歷史訊息取得
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