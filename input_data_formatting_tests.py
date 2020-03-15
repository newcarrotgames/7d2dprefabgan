from __future__ import absolute_import, division, print_function, unicode_literals
 
import tensorflow as tf
 
tf.__version__
  
import glob
import imageio
import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
from tensorflow.keras import layers
import time
from read_training_data import read_training_data
from IPython import display

def normalize_dataset(dataset):
    dataset = dataset.reshape(dataset.shape[0], 28, 28, 1).astype('float32')
    dataset = (dataset - 127.5) / 127.5 # Normalize the images to [-1, 1]
    return dataset

def print_dataset_shape(dataset):
    print("shape: {}\n".format(dataset.shape))

# clear terminal
print(chr(27) + "[2J")

# load minst data and print shape
print("loading minst dataset")
(mnist_training_dataset, mnist_train_labels), (_, _) = tf.keras.datasets.mnist.load_data()
print_dataset_shape(mnist_training_dataset)

# load our "fake" data and print shape
print("loading my local dataset")
(my_training_dataset, my_train_labels) = read_training_data()
print_dataset_shape(my_training_dataset)

# attempt to normalize minst data set
minst_normalized_dataset = normalize_dataset(mnist_training_dataset)

# attempt to normalize my data set
my_normalized_dataset = normalize_dataset(my_training_dataset)