from pymongo import MongoClient
import os

MONGO_HOST = os.environ.get("MONGO_HOST", "mongodb")
MONGO_PORT = os.environ.get("MONGO_PORT", "27017")
MONGO_USER = os.environ.get("MONGO_INITDB_ROOT_USERNAME", "root")
MONGO_PASS = os.environ.get("MONGO_INITDB_ROOT_PASSWORD", "rootpassword")

DATABASE_NAME = "spotilike_db"

client = MongoClient(
    host=MONGO_HOST,
    port=int(MONGO_PORT),
    username=MONGO_USER,
    password=MONGO_PASS
)

db = client[DATABASE_NAME]
