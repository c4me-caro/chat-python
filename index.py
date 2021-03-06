import json
from flask import Flask, redirect, render_template, request, redirect, make_response
from flask_socketio import SocketIO, emit, join_room, leave_room
import random

app = Flask(__name__)
app.config['secret_key'] = '7h1si5s3cr3t'
socketio = SocketIO(app)

randhex = lambda: random.randint(150,255)

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/join', methods = ['POST'])
def join():
   if request.method == 'POST':
        name = request.form["name"]
        room = request.form["room"]
        font = '<font color="#%02X%02X%02X">' % (randhex(),randhex(),randhex())
        resp = make_response(redirect("/chat?room=" + room))
        resp.set_cookie('user', json.dumps({'name':name, 'font':font}))
        return resp

@app.route('/chat', methods=['GET'])
def chat():
    name = json.loads(request.cookies.get('user'))["name"]
    room = request.args.get('room')
    return render_template("chat.html", name=name, room=room)

@socketio.on('chat')
def handle_message(msg):
    user = json.loads(request.cookies.get('user'))
    name = user["name"]
    font = user["font"]
    emit('chat', font + name + ": " + msg["message"] + "</font>", broadcast=True, to=msg["room"])

@socketio.on('join')
def assign(data):
    join_room(data["room"])
    name = json.loads(request.cookies.get('user'))["name"]
    font = json.loads(request.cookies.get('user'))["font"]
    emit('chat', font + name + ": has join the chat</font>", broadcast=True, to=data["room"])

@socketio.on('leave')
def unset(data):
    leave_room(data["room"])
    name = json.loads(request.cookies.get('user'))["name"]
    font = json.loads(request.cookies.get('user'))["font"]
    emit('chat', font + name + ": has leaved the chat</font>", broadcast=True, to=data["room"])

if __name__ == '__main__':
    socketio.run(app)