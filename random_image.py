from PIL import Image
import numpy as np
import cv2
import random

w, h = 125, 125
grid_size = 5
cell_size = 25
numer_of_images_to_generate = 100
for image_index in range(numer_of_images_to_generate):
    data = np.zeros((h, w, 3), dtype=np.uint8)
    for grid_x in range(grid_size):
        for grid_y in range(grid_size):
            top_left_offset = random.randint(1, 10)
            left = grid_x*cell_size + top_left_offset
            top = grid_y*cell_size + top_left_offset
            bottom_right_offset = random.randint(1, 10)
            right = grid_x*cell_size+cell_size - bottom_right_offset
            bottom = grid_y*cell_size+cell_size - bottom_right_offset
            cv2.rectangle(data, (top, left), (bottom, right), (0, 0, 255), 1)
    image = Image.fromarray(data, 'RGB')
    image.save("dataset\\train\\test_image_{}.png".format(image_index))