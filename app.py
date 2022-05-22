from flask import *
from flask_socketio import SocketIO, join_room, leave_room

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/video')
def video():
    return render_template("video.html")

@app.route('/chat')
def chat():
    username = request.args.get('username')
    room = request.args.get('room')
    if username and room:
        return render_template('chat.html', username=username, room=room)
    else:
        return redirect(url_for('home'))

@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} has sent message to the room {}: {}".format(data['username'],data['room'],data['message']))

    socketio.emit('receive_message', data, room=data['room'])

@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])

@socketio.on('disconnect')
def disconnect():
	print("Client disconnected")
	# socketio.stop() 

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', port=3020, debug=True)
