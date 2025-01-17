from flask_socketio import SocketIO
from flask import request
from flask_socketio import emit

socket = SocketIO()

users = {}

@socket.on("connect")
def connectHandler():
    print("Client Connected!")


@socket.on("user_join")
def handleUserJoin(username):
    print(f"User {username} joined!")
    users[request.sid] = username
    emit("user_connected", {"user": username}, broadcast=True)

@socket.on("message")
def handleSendMessage(message):
    emit("chat", {"message": message, "user": users[request.sid]}, broadcast=True)
