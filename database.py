import pymongo
import utility

client = pymongo.MongoClient("mongodb://localhost:27017")

def add_account(account):
    serialized = utility.serialize_account(account)
    if(username_in_db(account.username)):
        return -1
    else:
        db = client["accounts"]
        col = db["users"]
        col.insert_one(serialized)
        return 0

def get_account(username, password):
    col = client["accounts"]["users"]
    if(len(list(col.find({"username" : username, "password" : password}))) == 0):
        return -1
    else:
        return list(col.find({"username" : username, "password" : password}))[0]

def username_in_db(username):
    col = client["accounts"]["users"]
    if len(list(col.find({"username" : username}))) == 0:
        return False
    else:
        return True
