from flask import *
from flask import session

# 讀取.env的隱藏資料
from dotenv import load_dotenv
import os


load_dotenv()


class joinroom:
    #取得當前房間資訊
    def roomStatus():
        # 房間登入中
        if "room" in session:
            room = session['room']
            data = {
                "data":{
                    "room":room
                }
            }
            return jsonify(data)

        # 房間沒登入
        data = {"data": None}
        return jsonify(data)



    # 房間登入功能
    def roomIn():
        try:
            data = request.json
            room = data['room']
            if room != None:
                session['room'] = room
                data = {"ok": True}
                return jsonify(data)
            else:
                data = {
                    "error": True,
                    "message": "未輸入房間名稱"
                }
                return jsonify(data), 400

        # 伺服器錯誤
        except:
            data = {
                "error": True,
                "message": "伺服器內部錯誤"
            }
            return jsonify(data), 500

    # 房間登出功能
    def roomOut():
        # 登出
        data = {"ok": True}
        session['room'] = ""
        return jsonify(data)