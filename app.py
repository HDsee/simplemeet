from flask import *
from flask_socketio import SocketIO, join_room, leave_room,emit,send

#import api
from controller.user_route import userApi
from controller.joinroom_route import joinroomApi
from controller.friend_route import friendApi
from controller.message_route import messageApi
from controller.member_route import memberApi
from controller.member_route import imgApi

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["JSON_SORT_KEYS"] = False #阻止json按照字母排序

#註冊blueprint
app.register_blueprint(userApi)
app.register_blueprint(joinroomApi)
app.register_blueprint(memberApi)
app.register_blueprint(friendApi)
app.register_blueprint(messageApi)
app.register_blueprint(imgApi)

app.secret_key="HD"
# Pages
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/member")
def member():
	return render_template("member.html")

@app.route('/video')
def video():
    return render_template("video.html")	

@app.route('/chat')
def chat():
    return render_template('chat.html')

users = {}

@socketio.on('message from user', namespace='/messages')
def receive_message_from_user(message):
    print(request.sid,message)
    emit('from flask',message, broadcast=True)

@socketio.on('username', namespace='/private')
def receive_username(username):
    users[username] = request.sid
    print('online users:',users)

@socketio.on('private_message', namespace='/private')
def private_message(payLoad):
    recipient_session_id = users[payLoad['username']]
    message = payLoad['message']
    emit('new_private_message', message, room=recipient_session_id)

@socketio.on('disconnect', namespace='/private')
def disconnect():
    del users[session['user']]
    print(session['user'],'has left')
    print('online users:',users)




if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', port=3020, debug=True)
