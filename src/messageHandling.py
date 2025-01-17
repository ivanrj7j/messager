from flask_socketio import SocketIO
from flask import request
from flask_socketio import emit, join_room, disconnect
from .models import Community
from .collections import communityCollection, userCollection

socket = SocketIO()


@socket.on("connect")
def connectHandler():
    print("Client Connected!")


@socket.on("user_join")
def handleUserJoin(data):
    username = data["username"]
    community = Community(data["community"], communityCollection, userCollection)
    community.validate()

    if not community.validated:
        print("Invalid Community!")
        emit("invalid_community", {"community": community.name}, to=request.sid)
        # disconnect()
        return
    
    if not community.validateUser(username):
        print("Invalid User!")
        emit("invalid_user", {"user": username}, to=request.sid)
        # disconnect()
        return

    join_room(community)
    print(f"User {username} joined!")
    
    emit("user_connected", {"user": username}, to=community)

@socket.on("message")
def handleSendMessage(data):
    message = data["message"]
    join_room(data["community"])
    user = data["user"]
    emit("chat", {"message": message, "user": user}, to=data["community"])
