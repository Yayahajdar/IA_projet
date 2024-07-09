from keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt

def load_and_predict_image(image_path, model_path):
    # Load the pre-trained model
    model = load_model(model_path)
    
    # Load and process the image
    img = image.load_img(image_path, target_size=(100, 100))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Create a batch
    img_array /= 255.0  # Rescale the image

    # Make predictions
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)

    # Get class labels from the generator or a predefined list
    class_labels = ['Beetle', 'Butterfly', 'Cat', 'Cow', 'Dog']

    # Display the image and prediction
    plt.imshow(img)
    plt.title(f"Predicted class: {class_labels[predicted_class[0]]}")
    plt.axis('off')
    plt.show()

    return class_labels[predicted_class[0]]

# Example usage
image_path = 'imges/Lane-Cats.webp'
model_path = 'animal_species_model5.h5'
predicted_class = load_and_predict_image(image_path, model_path)
print(f"The image was predicted as: {predicted_class}")