from pymongo import MongoClient


MONGO_URI = "mongodb+srv://parthdesai635:parth1@ewd.azvnj.mongodb.net/?retryWrites=true&w=majority&appName=EWD"

client = MongoClient(MONGO_URI)

db = client["EWD"]

events_collection = db["MainEvents"]
articles_collection = db["MainArticles"]

def get_db():
    return db
