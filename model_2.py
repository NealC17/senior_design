import tensorflow as tf
import numpy as np

class Model_2(tf.keras.Model):
    def __init__(self):
        super(Model, self).__init__()
        self.model = tf.keras.Sequential([
                                    tf.keras.layers.Conv1D(32, kernel_size=3, activation='relu', input_shape=(min_length, 3)),
                                    tf.keras.layers.MaxPooling1D(pool_size=2),
                                    tf.keras.layers.Conv1D(64, kernel_size=3, activation='relu'),
                                    tf.keras.layers.MaxPooling1D(pool_size=2),
                                    tf.keras.layers.Flatten(),
                                    tf.keras.layers.Dense(64, activation='relu'),
                                    tf.keras.layers.Dense(3, activation='softmax')
                                    ])

    def heaviside_custom(self, x, values):
        ones = tf.ones_like(x)
        zeros = tf.zeros_like(x)
        return tf.where(x > 0, ones, tf.where(x < 0, zeros, values))

    def call(self, tens):
        return self.model(tens)

    def preprocessing(self, dummy_input):
        padding = np.zeros((128 - dummy_input.shape[0] % 128, dummy_input.shape[1]))
        dummy_input = np.concatenate([dummy_input, padding], axis=0)
        t = np.mean(dummy_input, axis=0) 
        dummy_input = dummy_input - t
        dummy_input_2 = np.reshape(dummy_input, (-1, 128, 3))
        dummy_input_3 = tf.constant(dummy_input_2, dtype=tf.float32)
        return dummy_input_3
