from tensorflow.keras import layers
import numpy as np
import matplotlib.pyplot as plt

import tensorflow as tf

tf.__version__

# base voxel model size
SIZE = (16, 16, 16)
KERNEL_SIZE = (5, 5, 5)
STRIDES = (1, 1, 1)

def build_discriminator():
    model = tf.keras.Sequential()
    model.add(layers.Conv3D(64, KERNEL_SIZE, strides=STRIDES, padding='same', input_shape=SIZE))
    model.add(layers.LeakyReLU())
    model.add(layers.Dropout(0.3))
    model.add(layers.Conv3D(128, KERNEL_SIZE, strides=STRIDES, padding='same'))
    model.add(layers.LeakyReLU())
    model.add(layers.Dropout(0.3))
    model.add(layers.Flatten())
    model.add(layers.Dense(1))
    return model

def build_generator():
    model = tf.keras.Sequential()
    model.add(layers.Dense(4*3*256, use_bias=False, input_shape=(100,)))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())
    model.add(layers.Reshape((4, 4, 4, 256)))
    # Note: None is the batch size
    assert model.output_shape == (None, 4, 4, 4, 256)
    model.add(layers.Conv3DTranspose(
        128, KERNEL_SIZE, strides=STRIDES, padding='same', use_bias=False))
    assert model.output_shape == (None, 4, 4, 4, 128)
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())
    model.add(layers.Conv3DTranspose(
        64, KERNEL_SIZE, strides=STRIDES, padding='same', use_bias=False))
    assert model.output_shape == (None, 8, 8, 8, 64)
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())
    model.add(layers.Conv3DTranspose(1, KERNEL_SIZE, strides=STRIDES,
                                     padding='same', use_bias=False, activation='tanh'))
    assert model.output_shape == (None, 16, 16, 16, 1)
    return model