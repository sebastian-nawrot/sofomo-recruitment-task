from pymongo import MongoClient

from app.config import settings


client = MongoClient(f"mongodb://{settings.mongo_username}:"
                     f"{settings.mongo_password}@{settings.mongo_host}",
                     connectTimeoutMS=4000,
                     serverSelectionTimeoutMS=4000)
