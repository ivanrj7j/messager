from pymongo.collection import Collection
from .user import User

class Community:
    def __init__(self, name:str, collection:Collection, userCollection:Collection):
        self.name = name
        self.collection = collection
        self.validated = False
        self.userCollection = userCollection

    @property
    def members(self):
        if not self.validated:
            raise ValueError("Community not validated yet")
        
        return self.collection.find_one({
            "name": self.name
        }, {
            "members": 1
        })
    
    def validate(self):
        check = self.collection.find_one({
            "name": self.name
        })

        self.validated = check is not None

    
    def create(self, admin:str):
        check = self.collection.find_one({
            "name": self.name
        })

        userExists = self.userCollection.find_one({
            "username": admin
        })

        if userExists is None:
            raise ValueError("Admin user not found")

        if check is not None:
            raise NameError("Community already exists")
        
        result = self.collection.insert_one({
            "name": self.name,
            "members": [
                admin
            ],
            "admin": admin
        })

        self.validated = result.acknowledged

    def remove(self, admin:str):
        if not self.validated:
            raise ValueError("Community not validated yet")
        
        result = self.collection.delete_one({
            "name": self.name,
            "admin": admin
        })

        if result.deleted_count == 0:
            raise ValueError("Community not found")
        

    def addUser(self, username:str):
        if not self.validated:
            raise ValueError("Community not validated yet")
        
        user = User(username, self.userCollection)
        exists = user.exists()

        if exists:
            userExistsInCommunity = self.collection.find_one({
                "name": self.name,
                "members": {"$in": [username]}
            })

            if userExistsInCommunity is not None:
                raise FileExistsError("The user already exists in the community")
            
            self.collection.update_one({
                "name": self.name
            }, {
                "$push": {
                    "members": username
                }
            })
        else:
            raise NameError("User not found")
        
    def removeUser(self, username:str):
        if not self.validated:
            raise ValueError("Community not validated yet")
        
        result = self.collection.update_one({
            "name": self.name
        }, {
            "$pull": {
                "members": username
            }
        })

        if result.modified_count == 0:
            raise ValueError("User not found in the community")