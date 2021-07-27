from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

clients = []

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@socketio.on('connect')
def connected(auth):
    print(f'Client {request.sid} connected')
    clients.append(request.sid)

@socketio.on('disconnect')
def disconnected():
    print(f'Client {request.sid} disconnected')

@socketio.on('message')
def handle_message(data):
    print(f'Received message: {data}')

    send("server sending the message!")

@socketio.on('heard')
def handle_heard(data):
    print(f'Received heard: {data}')

    emit('say', f'{data}')

def broadcast():
    socketio.emit('say', 'hello everyone')

def send_message(client_id, data):
    socketio.emit('output', data, room=clients[-1])

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)