import streamlit as st
from textblob import TextBlob
from pymongo import MongoClient
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv

load_dotenv()
mongo_uri = os.getenv('MONGO_URI')
client = MongoClient(mongo_uri)
language_key = os.environ.get('A_k')
language_endpoint = os.environ.get('ENDPOINT')

def authenticate_client():
    ta_credential = AzureKeyCredential(language_key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=language_endpoint, 
            credential=ta_credential)
    return text_analytics_client




# Database et collections
db = client['mooc']
collectionUser = db['user']
collectionForum = db['fourm']

# Les cours
courses_sessions = [
    'MinesTelecom/04017/session01',
    'MinesTelecom/04017S02/session02',
    'MinesTelecom/04018/session01',
    'MinesTelecom/04018S02/session02',
    'MinesTelecom/04021/session01',
    'MinesTelecom/04021S02/session02',
    'course-v1:MinesTelecom+04017+session03',
    'course-v1:MinesTelecom+04021+session03',
    'course-v1:MinesTelecom+04018+session03',
    'course-v1:MinesTelecom+04017+session04'
]

def language_extraction(client, message_input):
    try :
        documents = [message_input]
        response = client.detect_language(documents = documents, country_hint = 'fr')[0]
        return response.primary_language.name

    except Exception as err:
        print("Encountered exception. {}".format(err))



def main():
    client = authenticate_client()
    st.title('Forum')

    with st.form(key='message_form'):
        selected_course = st.selectbox("Choisissez un cours", courses_sessions)
        message_input = st.text_area("Entrez votre message ici:")
        goal_input = st.text_input("But de l'utilisateur (Goals):")
        education_level_input = st.text_input("Niveau d'études:")
        submit_button = st.form_submit_button(label='Analyser')

        if submit_button:

            # Analyse de sentiment
            documents = [message_input]

            # Affichage des résultats
            
            result = client.analyze_sentiment(documents, show_opinion_mining=True)
            docs = [doc for doc in result if not doc.is_error]

            # Affichage des informations supplémentaires
            st.write(f"Objectifs de l'utilisateur: {goal_input}")
            st.write(f"Niveau d'études: {education_level_input}")
            st.write(f"Langue détectée : {language_extraction(client, message_input)}")
            for idx, doc in enumerate(docs):
                st.write(f"Document text: {documents[idx]}")
                st.write(f"Overall sentiment: {doc.sentiment}")



if __name__ == '__main__':
    main()
