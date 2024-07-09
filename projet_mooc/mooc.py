'''from connexionBdd import client
import pymongo

conn = pymongo.MongoClient()
db = conn.test
col = db.mooc

filter={
    'username': 'jirasrideslis'
}
result = client['mooc']['user'].find(
  filter=filter
)
for doc in result :
   print(doc)
'''

from pymongo import MongoClient
import os
from dotenv import load_dotenv
import os
import re

load_dotenv()

# Connexion à MongoDB
mongo_uri = os.getenv('MONGO_URI')
client = MongoClient(mongo_uri)
db = client['mooc']
forum = db['fourm']
user = db['user']

# Filter pour université 'CNAM'
filter={
    'content.course_id': re.compile(r"^CNAM")
}

# Fonction (récursive) qui traite un MESSAGE
def analyse(doc, niv):
    print(f"{doc['id']} (niv{niv}) par {doc['anonymous']} {'???' if doc['anonymous'] else doc['username']}")

# Boucle sur tous les fils de discution du CNAM
for doc in forum.find(filter):
    analyse(doc['content'], 1)