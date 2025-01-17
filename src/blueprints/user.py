from flask import Blueprint, session
from ..models import User
from flask import request
from src.collections import userCollection
from .utils import newUserRequired, loginRequired

userBlueprint = Blueprint("user", __name__)

@newUserRequired
@userBlueprint.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    user = User(username, userCollection)
    try:
        user.register(password)
    except ValueError:
        return {"error": "Username already exists"}, 406
    
    session["username"] = username
    return {"message": "User registered successfully"}, 201


@newUserRequired
@userBlueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    user = User(username, userCollection)
    try:
        user.login(password)
    except ValueError:
        return {"error": "Invalid username or password"}, 401
    
    session["username"] = username    
    return {"message": "User logged in successfully"}, 200

@loginRequired
@userBlueprint.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    return {"message": "User logged out successfully"}, 200