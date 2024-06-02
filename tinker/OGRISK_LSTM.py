import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM

# Load data from JSON file
with open('/content/drive/MyDrive/features_and_labels.json', 'r') as f:
    data = json.load(f)

# Find the maximum length of flow vectors
max_length = max(len(entry['flow_vector']) for entry in data)

# Extract features and labels
X = []
y = []

for entry in data:
    flow_vectors = entry['flow_vector']

    # Convert flow vectors to a matrix
    matrix = np.array(flow_vectors)

    # Append to lists
    X.append(matrix)
    y.append(entry['label'])

print("Maximum length of flow vectors:", max_length)

# Number of features in each flow vector
num_features = 3

# Number of rows (sequences or time steps)
num_rows = max_length

# Number of columns (features)
num_columns = num_features

print("Size of the matrix:", num_rows, "x", num_columns)

# Extract labels
labels = [entry['label'] for entry in data]

# Count unique labels
unique_labels = set(labels)
num_unique_labels = len(unique_labels)

print("Unique labels:", unique_labels)
print("Number of unique labels:", num_unique_labels)

# Pad sequences to ensure uniform length (optional)
X = tf.keras.preprocessing.sequence.pad_sequences(X, maxlen=max_length, padding='post')

# Convert labels to numpy array and shift to range [0, num_classes - 1]
y = np.array(y) - 1

# Split data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the model
model = Sequential([
    LSTM(32, activation='tanh', input_shape=(max_length, X_train.shape[2])),
    Dense(16, activation='tanh'),
    Dense(8, activation='tanh'),
    Dense(3, activation='softmax') # Final dense layer with 3 units for 3 classes
])

# Compile the model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
history = model.fit(X_train, y_train, epochs=10, batch_size=16, validation_data=(X_val, y_val))

# Predict labels for validation set
y_pred = model.predict(X_val)
y_pred_classes = np.argmax(y_pred, axis=1)

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
