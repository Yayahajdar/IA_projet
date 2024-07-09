from pymongo import MongoClient
import dotenv, re, os

# Requires the PyMongo package.
# https://api.mongodb.com/python/current
dotenv.load_dotenv()

# Les collections
client = MongoClient(os.environ["MONGO_URI"])
forum = client['mooc']['fourm']
user = client['mooc']['User']

# Filter pour université 'CNAM'
filter={
    'content.course_id': re.compile(r"^CNAM")
}

# Fonction (récursive) qui traite un MESSAGE
def analyse(doc, niv):
    print(f"{'  '*niv}{doc['id']} (niv{niv}) par {doc['anonymous']} {'???' if doc['anonymous'] else doc['username']}")
    if 'children' in doc:
        for resp in doc['children']:
            analyse(resp, niv+1)
    if 'non_endorsed_response' in doc:
        for resp in doc['non_endorsed_response']:
            analyse(resp, niv+1)

# Boucle sur tous les fils de discution du CNAM
for doc in forum.find(filter):
    analyse(doc['content'], 1)
    
