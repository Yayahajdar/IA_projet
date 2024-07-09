import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
from sklearn.metrics import confusion_matrix, classification_report

# Load the trained model
model = load_model('animal_species_model.h5')

# Prepare the testing data with ImageDataGenerator
test_datagen = ImageDataGenerator(rescale=1./255)
test_generator = test_datagen.flow_from_directory(
    'dataset/animal/Testing Data/Testing Data',
    target_size=(128, 128),
    batch_size=20,
    class_mode='categorical',
    shuffle=False
)

# Reset the test_generator before making predictions
test_generator.reset()
predictions = model.predict(test_generator, steps=int(np.ceil(test_generator.samples / test_generator.batch_size)))
predicted_classes = np.argmax(predictions, axis=1)

# Retrieve true class labels
true_classes = test_generator.classes
class_labels = list(test_generator.class_indices.keys())

# Calculate the confusion matrix
cm = confusion_matrix(true_classes, predicted_classes)

# Plotting the confusion matrix
plt.figure(figsize=(12, 10))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_labels, yticklabels=class_labels)
plt.title('Confusion Matrix')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.show()

# Generate a classification report
report = classification_report(true_classes, predicted_classes, target_names=class_labels)
print(report)
