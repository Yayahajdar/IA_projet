from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Connexion à MongoDB
mongo_uri = os.getenv('MONGO_URI')
client = MongoClient(mongo_uri)
db = client['mooc']
collection1 = db['fourm']
collection2 = db['user']