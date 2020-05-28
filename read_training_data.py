import os
import cv2
import numpy as np
import glob

def read_training_data():
    training_images = []
    training_labels = []
    image_num = 1
    for image_file in glob.iglob('datasets\\training\\padded\\*.png'):
        # filename = os.path.join('datasets/training', image_filename)
        image_data = cv2.imread(image_file, 0)
        image_data = np.reshape(image_data, (-1, 64))
        training_images.append(image_data)
        # doesn't seem to be used but here just in case
        # eventually this should have the prefab's label
        training_labels.append(1)
        image_num += 1
        if image_num % 1000 == 0:
            print("image number: {}".format(image_num))
    training_images = np.asarray(training_images)
    training_labels = np.asarray(training_labels)
    return training_images, training_labels