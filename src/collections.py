from pymongo import MongoClient

client = MongoClient("localhost:27017")

db = client["testMessaging"]

userCollection = db["users"]
communityCollection = db["communities"]