from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)

users = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    username = request.args.get('username')
    if not username or username not in users:
        return redirect(url_for('index'))
    return render_template('chat.html', username=username)

@socketio.on('set_username')
def handle_set_username(username):
    if username not in users:
        users[username] = request.sid
        emit('user_joined', {'username': username}, broadcast=True)

@socketio.on('send_message')
def handle_send_message(message):
    emit('receive_message', {'message': message}, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    username = next((u for u, s in users.items() if s == request.sid), None)
    if username:
        del users[username]
        emit('user_left', {'username': username}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
