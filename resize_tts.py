from mpl_toolkits import mplot3d
from tts_read import read_tts_file
import numpy as np
import matplotlib.pyplot as plt
from voxels import Voxels
import math
from tts_utils import draw_prefab, layers_to_array
import sys

def resize_prefab(prefab, new_size):
    # calculate dim scalars
    x_s = prefab["size_x"] / new_size[0]
    y_s = prefab["size_y"] / new_size[1]
    z_s = prefab["size_z"] / new_size[2]

    # create fresh blank array of new size
    resized_voxel_data = np.zeros((new_size[2], new_size[1], new_size[0]))

    # iterate through each block of new array and 
    # scale by sampling values using the dim scalars
    for z_i in range(new_size[2]):
        for y_i in range(new_size[1]):
            for x_i in range(new_size[0]):
                x_d = math.floor(x_i * x_s)
                y_d = math.floor(y_i * y_s)
                z_d = math.floor(z_i * z_s)
                try:
                    resized_voxel_data[z_i][y_i][x_i] = prefab["layers"][z_d][y_d][x_d]
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    print("i: {} {} {}".format(x_i, y_i, z_i))
                    print("d: {} {} {}".format(x_d, y_d, z_d))

    # create new prefab and return it
    new_prefab = prefab
    new_prefab["size_x"] = new_size[0]
    new_prefab["size_y"] = new_size[1]
    new_prefab["size_z"] = new_size[2]
    print("type: {} {} {}".format(type(new_prefab["size_x"]), type(new_prefab["size_y"]), type(new_prefab["size_z"])))
    new_prefab["layers"] = resized_voxel_data
    return new_prefab

if __name__ == '__main__':
    tts_data = read_tts_file("prefabs/all/trailer_03.tts")
    original_size = (tts_data["size_x"], tts_data["size_y"], tts_data["size_z"])
    print(original_size)
    resized_prefab = resize_prefab(tts_data, (16, 16, 30))
    draw_prefab(resized_prefab)