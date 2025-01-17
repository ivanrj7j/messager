from flask_socketio import SocketIO
from flask import request
from flask_socketio import emit, join_room

socket = SocketIO()


@socket.on("connect")
def connectHandler():
    print("Client Connected!")


@socket.on("user_join")
def handleUserJoin(data):
    username = data["username"]
    community = data["community"]
    join_room(community)
    print(f"User {username} joined!")
    
    emit("user_connected", {"user": username}, to=community)

@socket.on("message")
def handleSendMessage(data):
    message = data["message"]
    join_room(data["community"])
    user = data["user"]
    emit("chat", {"message": message, "user": user}, to=data["community"])
