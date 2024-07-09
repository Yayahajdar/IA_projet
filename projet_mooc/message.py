from pymongo import MongoClient
import dotenv, re, os
import pandas as pd 

# Requires the PyMongo package.
# https://api.mongodb.com/python/current
dotenv.load_dotenv()

# Les collections
client = MongoClient('mongodb://localhost:27017')
forum = client['mooc']['fourm']
user = client['mooc']['user']
message = client['mooc']['Message']

# # Filter pour université 'CNAM'
# filter={
#     'content.course_id': re.compile(r"^MinesTelecom")
# }

# # Fonction (récursive) qui traite un MESSAGE
# def analyse(doc, niv):
#     print(f"{'  '*niv}{doc['id']} (niv{niv}) par {doc['anonymous']} {'???' if doc['anonymous'] else doc['username']}, {doc['course_id']}")
#     if 'children' in doc:
#         for resp in doc['children']:
#             analyse(resp, niv+1)
#     if 'non_endorsed_response' in doc:
#         for resp in doc['non_endorsed_response']:
#             analyse(resp, niv+1)
#     # Enregistrement dans collection
#     doc['niv']=niv
#     doc['children']=None
#     doc['non_endorsed_response']=None
#     #client['MOOC']['Message'].insert_one(doc)
#     client['mooc']['Message'].update_one({'id': doc['id']}, {'$set': doc}, upsert=True)

# # Boucle sur tous les fils de discution du CNAM
# for doc in forum.find(filter):
#     analyse(doc['content'], 1)
 
# Filter pour université 'CNAM'
filter={
    'content.course_id': re.compile(r"^MinesTelecom")
}

# Fonction (récursive) qui traite un MESSAGE
def analyse(doc, niv):
    # Récupération et split du course_id -> univ, course, session
    course_id = doc['course_id']
    course_id=course_id.replace('course-v1:', '')
    info = course_id.split('/' if '/' in course_id else '+')
    print(f"{'  '*niv}{doc['id']} (niv{niv}) par {doc['anonymous']} {'???' if doc['anonymous'] else doc['username']}, {info}")
    if 'children' in doc:
        for resp in doc['children']:
            analyse(resp, niv+1)
    if 'non_endorsed_response' in doc:
        for resp in doc['non_endorsed_response']:
            analyse(resp, niv+1)
    # Enregistrement dans collection, après avoir mis a jour les champs
    doc['niv']=niv
    doc['univ']=info[0]
    doc['course']=info[1]
    doc['session']=info[2]
    doc['children']=None
    doc['non_endorsed_response']=None
    #client['MOOC']['Message'].insert_one(doc)
    client['mooc']['Message'].update_one({'id': doc['id']}, {'$set': doc}, upsert=True)
    return doc

# Boucle sur tous les fils de discution du CNAM
processed_docs = []
for doc in forum.find(filter):
    processed_doc = analyse(doc['content'], 1)
    processed_docs.append(processed_doc)

# Convert output to DataFrame
df = pd.DataFrame(processed_docs)
print(df)

# Optionally, save DataFrame to CSV
df.to_csv('messages.csv', index=False)
 
