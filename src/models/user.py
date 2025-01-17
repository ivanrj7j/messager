from pymongo.collection import Collection
import time

class User:
    def __init__(self, username:str, collection:Collection):
        self.username = username
        self.loggedIn = False
        self.collection = collection

    def register(self, password:str) -> None:
        data = {
            "username": self.username,
            "pasword": password,
            "joinedOn": time.time(),
            "communities": []
        }

        self.collection.insert_one(data)
        self.loggedIn = True

    def loginCheck(self):
        if not self.loggedIn:
            raise ValueError("User is not logged in")

    def login(self, password:str) -> None:
        result = self.collection.find_one({
            "username": self.username,
            "pasword": password
        })

        if result is not None:
            self.loggedIn = True

        raise ValueError("The given username and passwords do not match")

    @property
    def details(self) -> dict:
        self.loginCheck()
        
        result = self.collection.find({
            "username": self.username
        })

        return dict(result)

    @property
    def joinedCommunites(self) -> list[dict]:
        self.loginCheck()

        result = self.collection.find_one({
            "username": self.username
        }, {
            "communities": 1
        })

        return 
    
