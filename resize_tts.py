from mpl_toolkits import mplot3d
from tts_read import read_tts_file
import numpy as np
import matplotlib.pyplot as plt
from voxels import Voxels
from build_tts_training_data import layers_to_array
import math

tts_data = read_tts_file("prefabs/trailer3/trailer_03.tts")
original_size = (tts_data["size_x"], tts_data["size_y"], tts_data["size_z"])
print(original_size)
block_data = layers_to_array(tts_data).reshape(original_size)
print(block_data.shape)

pad = np.zeros((3,1))
pad[0,0] = max(block_data.shape) - block_data.shape[0]
pad[1,0] = max(block_data.shape) - block_data.shape[1]
pad[2,0] = max(block_data.shape) - block_data.shape[2]

padded_block_data = np.zeros((max(block_data.shape),max(block_data.shape),max(block_data.shape)))

padded_block_data = np.pad(block_data, ((int(math.ceil(pad[0,0]/2)),
    int(math.floor(pad[0,0]/2))),(int(math.ceil(pad[1,0]/2)),
    int(math.floor(pad[1,0]/2))),(int(math.ceil(pad[2,0]/2)),
    int(math.floor(pad[2,0]/2)))), 'constant', constant_values=0)

new_size = (16,16,16)
padded_block_data.resize(new_size)

# fig = plt.figure()
# ax = plt.axes(projection='3d')

# for z in range(new_size[2]):
#     for y in range(new_size[1]):
#         for x in range(new_size[0]):
#             print (padded_block_data.shape)
#             print (x, y, z)
#             if padded_block_data[z][y][x] != 0:
#                 ax.scatter3D(x, y, z)

prefab_block_data = padded_block_data.flatten()
print(prefab_block_data.shape)
name = "trailer_03_resized.tts"
v = Voxels(name, new_size, prefab_block_data)
v.to_tts_file(name)