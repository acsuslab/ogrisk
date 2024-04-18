import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM

# Load data from JSON file
with open('/home/ahmedm89/small_features_and_labels.json', 'r') as f:
    data = json.load(f)


# Find the maximum length of flow vectors
max_length = max(len(entry['flow_vector']) for entry in data)

def pad_flow_vectors(flow_vectors, max_length):
    padded_vectors = []
    for vector in flow_vectors:
        # Calculate the number of elements to pad
        padding_length = max_length - len(vector)
        if padding_length > 0:
            # Pad the flow vector with zeros
            padded_vector = vector + [[0, 0, 0]] * padding_length
        else:
            # If the vector is already at max length, keep it unchanged
            padded_vector = vector[:]
        padded_vectors.append(padded_vector)
    return padded_vectors

# Extract features and labels
# Convert flow vectors to Python lists
X = []
y = []

for entry in data:
    flow_vectors = entry['flow_vector']

    # Pad the flow vectors to ensure uniform length
    padded_vectors = pad_flow_vectors(flow_vectors, max_length)

    # Append to lists
    X.append(padded_vectors)
    y.append(entry['label'])

# Split data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)



# Define the model
model = Sequential([
    LSTM(64, activation='tanh', input_shape=(max_length, 3)),
    Dense(32, activation='tanh'),
    Dense(16, activation='tanh'),
    Dense(3, activation='softmax') # Final dense layer with 3 units for 3 classes
])

# Compile the model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_val, y_val))

# Predict labels for validation set
y_pred = model.predict(X_val)
y_pred_classes = [np.argmax(pred) for pred in y_pred]

# Calculate performance metrics
f1 = f1_score(y_val, y_pred_classes, average='weighted')
precision = precision_score(y_val, y_pred_classes, average='weighted')
recall = recall_score(y_val, y_pred_classes, average='weighted')
accuracy = accuracy_score(y_val, y_pred_classes)

print("F1 Score:", f1)
print("Precision:", precision)
print("Recall:", recall)
print("Accuracy:", accuracy)

import matplotlib.pyplot as plt

# Plot training and validation errors
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Training and Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()

