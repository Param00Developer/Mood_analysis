from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()
def connect(collection_name):
    try:
        db_name=os.getenv("DB_NAME","CSV_DEMO")
        mongo_uri=os.getenv("DB_URI")
        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]
        return (client,collection)
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")