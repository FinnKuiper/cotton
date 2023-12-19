from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

# load environment variables
load_dotenv()


# create mongodb client
def get_database():
    CONNECTION_STRING = os.getenv('MONGODB_CONNECTION_STRING')
    client = MongoClient(CONNECTION_STRING, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
    except Exception as e:
        print(e)
        
    return client["discord-bot"]

if __name__ == "__main__":
    dbname = get_database()
    collection_name = dbname["guild"]
    print(collection_name.find_one())