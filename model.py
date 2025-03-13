import tensorflow as tf
import numpy as np

class Model(tf.keras.Model):
    def __init__(self):
        super(Model, self).__init__()
        self.values = tf.constant([0], dtype=tf.float32)

    def heaviside_custom(self, x, values):
        ones = tf.ones_like(x)
        zeros = tf.zeros_like(x)
        return tf.where(x > 0, ones, tf.where(x < 0, zeros, values))

    def call(self, tens):
        t = self.heaviside_custom(tens, self.values)
        b = t[1:] - t[:-1]
        mask = tf.reduce_any(tf.not_equal(b, 0), axis=1)
        b = tf.boolean_mask(b, mask)
        b = tf.where(tf.equal(b, -1), tf.zeros_like(b), b)
        return tf.reduce_sum(b, axis=0)

    def preprocessing(self, dummy_input):
        padding = np.zeros((128 - dummy_input.shape[0] % 128, dummy_input.shape[1]))
        dummy_input = np.concatenate([dummy_input, padding], axis=0)
        t = np.mean(dummy_input, axis=0) 
        dummy_input = dummy_input - t
        dummy_input_2 = np.reshape(dummy_input, (-1, 128, 3))
        dummy_input_3 = tf.constant(dummy_input_2, dtype=tf.float32)
        return dummy_input_3
