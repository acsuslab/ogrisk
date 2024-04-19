import json
import numpy as np
import tensorflow as tf
from sklearn.model_selection import KFold
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import matplotlib.pyplot as plt

# Load data from JSON file
with open('/home/nick/acsus/out-of-gas-ml/features_and_labels.json', 'r') as f:
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

# Pad sequences to ensure uniform length (optional)
X = tf.keras.preprocessing.sequence.pad_sequences(X, maxlen=max_length, padding='post')

# Convert labels to numpy array and shift to range [0, num_classes - 1]
y = np.array(y) - 1

# Define the model
model = Sequential([
    LSTM(32, activation='tanh', input_shape=(max_length, X.shape[2])),
    Dense(16, activation='tanh'),
    Dense(8, activation='tanh'),
    Dense(3, activation='softmax') # Final dense layer with 3 units for 3 classes
])

# Compile the model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Perform k-fold cross-validation
kf = KFold(n_splits=5, shuffle=True, random_state=42)
f1_scores = []
precision_scores = []
recall_scores = []
accuracy_scores = []
training_accuracies = []
validation_accuracies = []

for train_index, val_index in kf.split(X):
    X_train, X_val = X[train_index], X[val_index]
    y_train, y_val = y[train_index], y[val_index]

    # Train the model
    history = model.fit(X_train, y_train, epochs=10, batch_size=16, verbose=0, validation_data=(X_val, y_val))

    # Predict labels for validation set
    y_pred = model.predict(X_val)
    y_pred_classes = np.argmax(y_pred, axis=1)

    # Calculate performance metrics
    f1 = f1_score(y_val, y_pred_classes, average='weighted')
    precision = precision_score(y_val, y_pred_classes, average='weighted')
    recall = recall_score(y_val, y_pred_classes, average='weighted')
    accuracy = accuracy_score(y_val, y_pred_classes)

    f1_scores.append(f1)
    precision_scores.append(precision)
    recall_scores.append(recall)
    accuracy_scores.append(accuracy)

    # Store training and validation accuracies
    training_accuracies.append(history.history['accuracy'])
    validation_accuracies.append(history.history['val_accuracy'])

# Calculate mean scores
mean_f1 = np.mean(f1_scores)
mean_precision = np.mean(precision_scores)
mean_recall = np.mean(recall_scores)
mean_accuracy = np.mean(accuracy_scores)

print("Mean F1 Score:", mean_f1)
print("Mean Precision:", mean_precision)
print("Mean Recall:", mean_recall)
print("Mean Accuracy:", mean_accuracy)

# Plot mean scores
metrics = ['F1 Score', 'Precision', 'Recall', 'Accuracy']
mean_scores = [mean_f1, mean_precision, mean_recall, mean_accuracy]

plt.bar(metrics, mean_scores, color=['blue', 'green', 'red', 'orange'])
plt.title('Mean Performance Metrics Across Folds')
plt.xlabel('Metric')
plt.ylabel('Mean Score')
plt.show()

# Plot training and validation accuracies
plt.plot(np.mean(training_accuracies, axis=0), label='Training Accuracy')
plt.plot(np.mean(validation_accuracies, axis=0), label='Validation Accuracy')
plt.title('Mean Training and Validation Accuracies Across Folds')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()
