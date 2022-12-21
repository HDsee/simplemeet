from flask import *
from flask_socketio import SocketIO, join_room, leave_room,emit,send

#import api
from api.user import userApi 
from api.joinroom import joinroomApi
from api.member import memberApi
from api.member import friendApi
from api.member import messageApi
from api.member import imgApi

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["JSON_SORT_KEYS"] = False #阻止json按照字母排序

#註冊blueprint
app.register_blueprint(userApi, url_prefix='/api')
app.register_blueprint(joinroomApi, url_prefix='/api')
app.register_blueprint(memberApi, url_prefix='/api')
app.register_blueprint(friendApi, url_prefix='/api')
app.register_blueprint(messageApi, url_prefix='/api')
app.register_blueprint(imgApi, url_prefix='/api')

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

# @socketio.on('send_message' )
# def handle_send_message_event(data):
#     app.logger.info("{} has sent message to the room {}: {}".format(data['username'],data['room'],data['message']))
#     socketio.emit('receive_message', data, room=data['room'])

# @socketio.on('join_room')
# def handle_join_room_event(data):
#     app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
#     join_room(data['room'])
#     users[session['user']] = request.sid
#     print(users)
    # socketio.emit('join_room_announcement', data, room=data['room'])

# @socketio.on('leave_room')
# def handle_leave_room_event(data):
#     app.logger.info("{} has left the room {}".format(data['username'], data['room']))
#     leave_room(data['room'])
#     socketio.emit('leave_room_announcement', data, room=data['room']) 

# @socketio.on('disconnect')
# def disconnect():
#     del users[session['user']]
#     print(users,'OK')
# 	app.logger.info("{} has disconnect {}".format(session['user'], session['room']))
#     disconnect(data)
#     socketio.emit('leave_room_announcement', data, room=session['room'])

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
