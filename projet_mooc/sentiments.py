import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import streamlit as st
from textblob import TextBlob
from pymongo import MongoClient

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key and endpoint from environment variables
api_key = os.getenv('A_S')
endpoint = os.getenv('ENDPOINT')

# Authenticate the client
credential = AzureKeyCredential(api_key)
text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=credential)

print("Connection established successfully.")

def authenticate_client():
    ta_credential = AzureKeyCredential(api_key)
    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=ta_credential)
    return text_analytics_client

# MongoDB connection (Ensure MongoDB is running and replace <your_connection_string>)
client = MongoClient("<your_connection_string>")

# Database and collections
db = client['mooc']
collectionUser = db['user']
collectionForum = db['forum']

# Courses
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
    try:
        documents = [message_input]
        response = client.detect_language(documents=documents, country_hint='fr')[0]
        return response.primary_language.name
    except Exception as err:
        print("Encountered exception. {}".format(err))

def main():
    client = authenticate_client()
    st.title('Analyse de Sentiment des Messages du Forum')

    with st.form(key='message_form'):
        selected_course = st.selectbox("Choisissez un cours", courses_sessions)
        message_input = st.text_area("Entrez votre message ici:")
        goal_input = st.text_input("But de l'utilisateur (Goals):")
        education_level_input = st.text_input("Niveau d'études:")
        submit_button = st.form_submit_button(label='Analyser')

        if submit_button:
            # Sentiment analysis
            documents = [message_input]
            response = client.analyze_sentiment(documents=documents)[0]

            # Display sentiment analysis results
            st.write("Polarité : {:.2f} (de -1 à 1)".format(response.confidence_scores.positive - response.confidence_scores.negative))
            st.write("Subjectivité : {:.2f} (de 0 à 1)".format(TextBlob(message_input).sentiment.subjectivity))

            if response.confidence_scores.positive > response.confidence_scores.negative:
                st.success("Le sentiment global est positif pour le cours sélectionné : {}".format(selected_course))
            elif response.confidence_scores.negative > response.confidence_scores.positive:
                st.error("Le sentiment global est négatif pour le cours sélectionné : {}".format(selected_course))
            else:
                st.info("Le sentiment global est neutre pour le cours sélectionné : {}".format(selected_course))

            # Display additional information
            st.write(f"Objectifs de l'utilisateur: {goal_input}")
            st.write(f"Niveau d'études: {education_level_input}")
            st.write(f"Langue détectée : {language_extraction(client, message_input)}")

if __name__ == '__main__':
    main()
