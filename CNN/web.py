import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

# Load models
model1_path = 'animal_species_model1.h5'
model2_path = 'animal_species_model4.h5'
model3_path = 'animal_species_model5.h5'
model1 = load_model(model1_path)
model2 = load_model(model2_path)
model3 = load_model(model3_path) 

# Function to predict the image class
def load_and_predict_image(img, model):
    img = image.load_img(img, target_size=(128, 128))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)
    class_labels = ['Beetle', 'Butterfly', 'Cat', 'Cow', 'Dog', 'Elephant', 'Gorilla', 
                    'Hippo', 'Lizard', 'Monkey', 'Mouse', 'Panda', 'Spider', 'Tiger', 'Zebra']
    return class_labels[predicted_class[0]]

def load_and_predict_image2(img, model):
    img = image.load_img(img, target_size=(100, 100))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)
    class_labels = ['Beetle', 'Butterfly', 'Cat', 'Cow', 'Dog', 'Elephant', 'Gorilla', 
                    'Hippo', 'Lizard', 'Monkey', 'Mouse', 'Panda', 'Spider', 'Tiger', 'Zebra']
    return class_labels[predicted_class[0]]

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page:", ["Home", "Predict", "Learn about CNN"])

# Page 1: Home Page
if page == "Home":
    st.title("Welcome to the Animal Species Prediction App!")
    st.write("""
        This application uses deep learning to predict the species of animals in images. 
        Upload an image on the 'Predict' page and select a model to see predictions.
    """)

# Page 2: Prediction Page
elif page == "Predict":
    st.title('Animal Species Prediction')
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        img = image.load_img(uploaded_file, target_size=(128, 128))
        st.image(img, caption='Uploaded Image', use_column_width=True)
        if st.button('Predict with Model 1'):
            prediction = load_and_predict_image(uploaded_file, model1)
            st.write(f"Predicted class: {prediction}")
        if st.button('Predict with Model 2  '):
            prediction = load_and_predict_image(uploaded_file, model2)
            st.write(f"Predicted class: {prediction}")
        if st.button('Predict with Model 3'):
            prediction = load_and_predict_image2(uploaded_file, model3)
            st.write(f"Predicted class: {prediction}")


# Page 3: Learn about CNN
elif page == "Learn about CNN":
    st.title("Understanding Convolutional Neural Networks (CNN)")
    st.write("""
        Convolutional Neural Networks (CNNs) are a class of deep neural networks, most commonly applied to analyzing visual imagery.
        They are particularly powerful in tasks like image classification, object detection, and more.
    """)
    st.image("path_to_cnn_explanation_image.png", caption="CNN Architecture")
    st.write("""
        The basic building blocks of CNNs are convolutional layers that apply filters to an image to create feature maps.
        These highlight important features of the image for further analysis by the network.
    """)

