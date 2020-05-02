import os
import cv2
import numpy as np

def read_training_data():
    files = os.listdir('datasets/training')
    training_images = []
    training_labels = []
    for _, image_filename in enumerate(files):
        image_data = cv2.imread(os.path.join('datasets/training', image_filename), 0)
        image_data = np.reshape(image_data, (-1, 28))
        training_images.append(image_data)
        # doesn't seem to be used but here just in case
        # eventually this should have the prefab's label
        training_labels.append(1)
    training_images = np.asarray(training_images)
    training_labels = np.asarray(training_labels)
    return training_images, training_labels