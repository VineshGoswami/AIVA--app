import pymongo
from datetime import datetime

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['AivaDB']
user_collection = db['users']
chat_collection = db['chats']


def savechat(username, message, aiva_response):
    chat_data = {
        "username": username,
        "message": message,
        "aiva_response": aiva_response,
        "time": datetime.now()
    }
    chat_collection.insert_one(chat_data)
    print("Chat saved successfully.")


def getchathistory(username):
    return list(chat_collection.find({"username": username}, {"_id": 0}))


if __name__ == "__main__":
    print("Welcome to PyMongo")
