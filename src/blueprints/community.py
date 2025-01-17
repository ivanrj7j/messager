from flask import Blueprint, request, session
from .utils import loginRequired
from src.collections import communityCollection, userCollection
from ..models.community import Community

communityBlueprint = Blueprint("community", __name__)

@loginRequired
@communityBlueprint.route("/createCommunity", methods=["POST"])
def createCommunity():
    data = request.get_json()
    admin = data["username"]
    communityName = data["name"]

    community = Community(communityName, communityCollection, userCollection)
    try:
        community.create(admin)
    except ValueError:
        return {"error": "Admin Not found"}, 404
    except NameError:
        return {"error": "Community already exists"}, 400

    return {"message": "Community created successfully"}

@loginRequired
@communityBlueprint.route("/removeCommunity", methods=["POST"])
def removeCommunity():
    data = request.get_json()
    user = data["username"]
    name = data["name"]

    community = Community(name, communityCollection, userCollection)
    community.validate()

    try:
        community.remove(user)
    except ValueError:
        return {"message": "Community not found in the community"}, 404
    
    return {"message": "Community removed successfully"}

@loginRequired
@communityBlueprint.route("/addUserToCommunity", methods=["POST"])
def addUserToCommunity():
    data = request.get_json()
    user = data["username"]
    communityName = data["name"]

    community = Community(communityName, communityCollection, userCollection)
    community.validate()

    try:
        community.addUser(user)
    except FileExistsError:
        return {"message": "User already exists in the community"}, 409
    except NameError:
        return {"message": "User not found in the database"}, 404
    except ValueError:
        return {"message": "Community not found in the database"}, 404
    
    return {"message": "User added successfully"}

@loginRequired
@communityBlueprint.route("/removeUserFromCommunity", methods=["POST"])
def removeUserFromCommunity():
    data = request.get_json()
    user = data["username"]
    communityName = data["name"]

    community = Community(communityName, communityCollection, userCollection)
    community.validate()

    try:
        community.removeUser(user)
    except ValueError:
        return {"message": "User not found in the community"}, 404
    
    return {"message": "User removed successfully"}

