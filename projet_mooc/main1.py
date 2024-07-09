import joblib
from scipy.sparse import hstack, csr_matrix
import numpy as np
import pandas as pd
import streamlit as st
from pymongo import MongoClient
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
mongo_uri = os.getenv('MONGO_URI')
client = MongoClient(mongo_uri)
language_key = os.getenv('A_K')
language_endpoint = os.getenv('ENDPOINT')

# Load the trained model
model = joblib.load('random_forest_regressor_model.pkl')

# Load the TF-IDF vectorizers used for text data
vectorizer = joblib.load('vectorizer.pkl')
vectorizer_goals = joblib.load('vectorizer_goals.pkl')
vectorizer_children = joblib.load('vectorizer_children.pkl')

# Load the additional preprocessing components
preprocessor = joblib.load('preprocessor.pkl')

# Database and collections
db = client['mooc']
collectionUser = db['user']
collectionForum = db['forum']

def authenticate_client():
    ta_credential = AzureKeyCredential(language_key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=language_endpoint, 
            credential=ta_credential)
    return text_analytics_client

def language_extraction(client, message_input):
    try:
        documents = [message_input]
        response = client.detect_language(documents=documents, country_hint='fr')[0]
        return response.primary_language.name
    except Exception as err:
        print(f"Encountered exception: {err}")
        return "Unknown"

def preprocess_message(message, goals='', children='', count=0, down_count=0, point=0, up_count=0, forum_level_of_education='unknown'):
    # Transform the text data
    text_features = vectorizer.transform([message])
    goals_features = vectorizer_goals.transform([goals])
    children_features = vectorizer_children.transform([children])
    
    # Create a DataFrame for additional features
    additional_features = pd.DataFrame({
        'count': [count],
        'down_count': [down_count],
        'point': [point],
        'up_count': [up_count],
        'forum_level_of_education': [forum_level_of_education]
    })

    # Apply preprocessing
    additional_features_transformed = preprocessor.transform(additional_features)

    # Convert to sparse matrix
    additional_features_transformed = csr_matrix(additional_features_transformed)

    return hstack([text_features, goals_features, children_features, additional_features_transformed])

def test_model(message, goals='', children='', count=0, down_count=0, point=0, up_count=0, forum_level_of_education='unknown'):
    # Preprocess the input message
    X = preprocess_message(message, goals, children, count, down_count, point, up_count, forum_level_of_education)

    # Make prediction
    prediction = model.predict(X)

    return prediction

def main():
    client = authenticate_client()
    st.title('Message Analyst')

    with st.form(key='message_form'):
        message_input = st.text_area("Entrez votre message ici:")
        goal_input = st.text_input("But de l'utilisateur (Goals):")
        education_level_input = st.text_input("Niveau d'études:")
        submit_button = st.form_submit_button(label='Analyser')

        if submit_button:
            # Language detection
            detected_language = language_extraction(client, message_input)
            
            # Sentiment analysis
            documents = [message_input]
            sentiment_result = client.analyze_sentiment(documents, show_opinion_mining=True)
            docs = [doc for doc in sentiment_result if not doc.is_error]

            # Prediction using the pre-trained model
            predicted_value = test_model(
                message=message_input, 
                goals=goal_input, 
                forum_level_of_education=education_level_input
            )

            # Displaying results
            st.write(f"Objectifs de l'utilisateur: {goal_input}")
            st.write(f"Niveau d'études: {education_level_input}")
            st.write(f"Langue détectée : {detected_language}")
            for idx, doc in enumerate(docs):
                st.write(f"Document text: {documents[idx]}")
                st.write(f"Overall sentiment: {doc.sentiment}")
                st.write(f"Positive score: {doc.confidence_scores.positive}")
                st.write(f"Neutral score: {doc.confidence_scores.neutral}")
                st.write(f"Negative score: {doc.confidence_scores.negative}")

            st.write(f"Predicted value: {predicted_value}")

if __name__ == '__main__':
    main()
