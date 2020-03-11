import os
import cv2
import numpy as np

def get_fake_training_data():
    files = os.listdir('dataset/train')
    training_images = []
    training_labels = []
    for _, image_filename in enumerate(files):
        training_images.append(cv2.imread(os.path.join('dataset/train', image_filename), 0))
        training_images = np.asarray(training_images).reshape(-1, 512, 512, 1)
        # doesn't seem to be used but here just in case
        training_labels.append(1)
    return training_images, training_labels