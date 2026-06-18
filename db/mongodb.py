from pymongo import MongoClient
import os


# client = MongoClient("mongodb://mongo:27017")

client = MongoClient(
    os.getenv("MONGO_URL")
)

db = client["auth_db"]

user_collection = db["users"]
refresh_tokens_collection = db["refresh_tokens"]

user_collection.create_index(
    "email",
    unique=True
)

user_collection.create_index(
    "username",
    unique=True
)