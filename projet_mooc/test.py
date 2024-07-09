import streamlit as st
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

def language_extraction(client, message_input):
    try:
        documents = [message_input]
        response = client.detect_language(documents=documents, country_hint='fr')[0]
        return response.primary_language.name
    except Exception as err:
        print("Encountered exception. {}".format(err))
        return None

def calculate_grade(education_level, goals):
    # Custom grading logic based on education level and goals
    if education_level == "PhD" or "doctorate" in goals.lower():
        return 'A'
    elif education_level == "Masters" or "master" in goals.lower():
        return 'B'
    elif education_level == "Bachelors" or "bachelor" in goals.lower():
        return 'C'
    elif education_level == "High School" or "high school" in goals.lower():
        return 'D'
    else:
        return 'F'

def sentiment_from_grade(grade):
    # Assign sentiment based on the grade
    if grade == 'A':
        return 'positive'
    elif grade == 'B':
        return 'positive'
    elif grade == 'C':
        return 'neutral'
    else:
        return 'negative'

def main():
    client = authenticate_client()
    st.title('Forum')

    with st.form(key='message_form'):
        forum_name = st.text_input("Nom du forum:")
        education_level_input = st.text_input("Niveau d'études:")
        goal_input = st.text_input("Objectifs de l'utilisateur (Goals):")
        message_input = st.text_area("Entrez votre message ici:")
        submit_button = st.form_submit_button(label='Soumettre')

        if submit_button:
            # Detect language
            language = language_extraction(client, message_input)
            if not language:
                language = "Unknown"

            # Calculate grade
            grade = calculate_grade(education_level_input, goal_input)

            # Determine sentiment based on grade
            sentiment = sentiment_from_grade(grade)
            sentiment_score = {"positive": 0.9, "neutral": 0.5, "negative": 0.1}[sentiment]

            # Display the results
            st.write(f"Nom du forum: {forum_name}")
            st.write(f"Niveau d'études: {education_level_input}")
            st.write(f"Objectifs de l'utilisateur: {goal_input}")
            st.write(f"Langue détectée : {language}")
            st.write(f"Texte du document: {message_input}")
            st.write(f"Sentiment global: {sentiment.capitalize()}")
            st.write(f"Score de positivité: {sentiment_score:.2f}")
            st.write(f"Score de neutralité: {(1 - sentiment_score):.2f}")
            st.write(f"Score de négativité: {0.0 if sentiment == 'positive' else (1 - sentiment_score):.2f}")
            st.write(f"Grade: {grade}")

if __name__ == '__main__':
    main()


    # In this programme when i write the forum names it give me result in behalf of my function information which is not ready yet
    # and and when i write the message it also detects the language or sentiments in behalf of grades for example if the grade is good it gives a
    # positive sentiments or if the result is not good the sentiments will be negative