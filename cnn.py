import pandas as pd
import numpy as np
import tensorflow as tf

# Load datasets
deadlift_df = pd.read_csv('deadlift.csv')
squat_df = pd.read_csv('squat.csv')
bench_df = pd.read_csv('bench.csv')

# Define windows
deadlift_window1 = deadlift_df[(deadlift_df['Time'] > 7233) & (deadlift_df['Time'] < 9733)]
deadlift_window2 = deadlift_df[(deadlift_df['Time'] > 11873) & (deadlift_df['Time'] < 11873 + 2500)]
deadlift_window3 = deadlift_df[(deadlift_df['Time'] > 16397) & (deadlift_df['Time'] < 16397 + 2500)]
deadlift_window4 = deadlift_df[(deadlift_df['Time'] > 21153) & (deadlift_df['Time'] < 21153 + 2500)]
deadlift_window5 = deadlift_df[(deadlift_df['Time'] > 26000) & (deadlift_df['Time'] < 26000 + 2500)]

squat_window1 = squat_df[(squat_df['Time'] > 23626) & (squat_df['Time'] < 23626 + 2500)]
squat_window2 = squat_df[(squat_df['Time'] > 26648) & (squat_df['Time'] < 26648 + 2500)]
squat_window3 = squat_df[(squat_df['Time'] > 30800) & (squat_df['Time'] < 30800 + 2500)]
squat_window4 = squat_df[(squat_df['Time'] > 35000) & (squat_df['Time'] < 35000 + 2500)]
squat_window5 = squat_df[(squat_df['Time'] > 39000) & (squat_df['Time'] < 39000 + 2500)]

bench_window1 = bench_df[(bench_df['Time'] > 14000) & (bench_df['Time'] < 14000 + 2500)]
bench_window2 = bench_df[(bench_df['Time'] > 18700) & (bench_df['Time'] < 18700 + 2500)]
bench_window3 = bench_df[(bench_df['Time'] > 23000) & (bench_df['Time'] < 23000 + 2500)]
bench_window4 = bench_df[(bench_df['Time'] > 27000) & (bench_df['Time'] < 27000 + 2500)]
bench_window5 = bench_df[(bench_df['Time'] > 33000) & (bench_df['Time'] < 33000 + 2500)]

# Organize windows
deadlift_windows = [deadlift_window1, deadlift_window2, deadlift_window3, deadlift_window4, deadlift_window5]
squat_windows = [squat_window1, squat_window2, squat_window3, squat_window4, squat_window5]
bench_windows = [bench_window1, bench_window2, bench_window3, bench_window4, bench_window5]

# Extract sequences and labels
X = []
y = []
for window in deadlift_windows:
    accel_x = window["Accel_X"].values
    accel_y = window["Accel_Y"].values
    accel_z = window["Accel_Z"].values
    X.append(np.stack([accel_x, accel_y, accel_z], axis=-1))  # Shape: (time_steps, 3)
    y.append(0)
for window in squat_windows:
    accel_x = window["Accel_X"].values
    accel_y = window["Accel_Y"].values
    accel_z = window["Accel_Z"].values
    X.append(np.stack([accel_x, accel_y, accel_z], axis=-1))
    y.append(1)
for window in bench_windows:
    accel_x = window["Accel_X"].values
    accel_y = window["Accel_Y"].values
    accel_z = window["Accel_Z"].values
    X.append(np.stack([accel_x, accel_y, accel_z], axis=-1))
    y.append(2)

# Find minimum sequence length and truncate
min_length = min([len(seq) for seq in X])
X = [seq[:min_length] for seq in X]

# Convert to numpy arrays
X = np.array(X)  # Shape: (15, min_length, 3)
y = np.array(y)  # Shape: (15,)

# Split into train and test
X_train = np.concatenate([X[0:4], X[5:9], X[10:14]])  # Shape: (12, min_length, 3)
y_train = np.concatenate([y[0:4], y[5:9], y[10:14]])   # Shape: (12,)
X_test = np.array([X[4], X[9], X[14]])                # Shape: (3, min_length, 3)
y_test = np.array([y[4], y[9], y[14]])                # Shape: (3,)

# One-hot encode labels
y_train = tf.keras.utils.to_categorical(y_train, num_classes=3)  # Shape: (12, 3)
y_test = tf.keras.utils.to_categorical(y_test, num_classes=3)    # Shape: (3, 3)

# Build the model
model = tf.keras.Sequential([
    tf.keras.layers.Conv1D(32, kernel_size=3, activation='relu', input_shape=(min_length, 3)),
    tf.keras.layers.MaxPooling1D(pool_size=2),
    tf.keras.layers.Conv1D(64, kernel_size=3, activation='relu'),
    tf.keras.layers.MaxPooling1D(pool_size=2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=1, validation_data=(X_test, y_test))

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test accuracy: {accuracy}")

# Step 1: Define representative dataset generator
def representative_data_gen():
    for i in range(len(X_train)):
        # Yield 1 sample at a time in a list
        yield [X_train[i:i+1].astype(np.float32)]

# Step 2: Convert to TFLite model with full integer (int8) quantization
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_data_gen
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.int8   # Force input to int8
converter.inference_output_type = tf.int8  # Force output to int8

tflite_model = converter.convert()

# Step 3: Save to 'clf.tflite'
with open("clf.tflite", "wb") as f:
    f.write(tflite_model)
