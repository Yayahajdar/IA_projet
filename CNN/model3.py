import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt

# Constants
IMAGE_WIDTH = 100
IMAGE_HEIGHT = 100
BATCH_SIZE = 32
NUM_EPOCHS = 50
NUM_CLASSES = 5   

# Paths to your dataset
train_data_dir = 'dataset/animal/Training Data/Training Data'
val_data_dir = 'dataset/animal/Validation Data/Validation Data'
test_data_dir = 'dataset/animal/Testing Data/Testing Data'

# Data generators with augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

val_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

# Load and preprocess data
train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(IMAGE_WIDTH, IMAGE_HEIGHT),
    batch_size=BATCH_SIZE,
    class_mode='categorical')

val_generator = val_datagen.flow_from_directory(
    val_data_dir,
    target_size=(IMAGE_WIDTH, IMAGE_HEIGHT),
    batch_size=BATCH_SIZE,
    class_mode='categorical')

test_generator = test_datagen.flow_from_directory(
    test_data_dir,
    target_size=(IMAGE_WIDTH, IMAGE_HEIGHT),
    batch_size=1,  
    class_mode='categorical')

# Build the model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(IMAGE_WIDTH, IMAGE_HEIGHT, 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(NUM_CLASSES, activation='softmax')  
])



# Compile the model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
model.fit(
    train_generator,
    epochs=NUM_EPOCHS,
    validation_data=val_generator,
)

# Evaluate and print test accuracy
test_loss, test_acc = model.evaluate(test_generator, steps=test_generator.samples)
print(f'Test accuracy: {test_acc}')

# Save the model
model.save('animal_species_model5.h5')

# Display and predict a few images
for i in range(5):
    plt.figure(figsize=(5, 5))
    batch = next(test_generator)
    img, label = batch[0], batch[1]
    true_label = np.argmax(label[0])
    predicted_label = np.argmax(model.predict(img)[0])
    plt.imshow(img[0] * 255)  # Rescale back the image to display correctly
    plt.title(f'Predicted: {predicted_label}, True: {true_label}')
    plt.show()

# Evaluate and print test accuracy
test_loss, test_acc = model.evaluate(test_generator, steps=test_generator.samples)

model.save('animal_species_model5.h5')
print(f'Test accuracy: {test_acc}')
