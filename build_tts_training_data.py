import os
import time
import random
from file_utils import unpack
from tts_read import read_tts_file
from config import Config
from pathlib import Path
import ntpath
import struct
from voxels import Voxels
import numpy as np

def print_tts_details(prefab):
    print("Prefab version: " + str(prefab["version"]))
    print("Dimensions: " + str(prefab["size_x"]) + "x" + str(prefab["size_y"]) + "x" + str(prefab["size_z"]))
    print("total block: {}".format(prefab["total_blocks"]))
    print("footer size: {}".format(len(prefab["footer"])))
    print("ratio: {}".format(len(prefab["footer"]) / prefab["total_blocks"]))

def resize_voxels():
    pad = np.zeros((3,1))
    pad[0,0] = max(Input.shape) - Input.shape[0]
    pad[1,0] = max(Input.shape) - Input.shape[1]
    pad[2,0] = max(Input.shape) - Input.shape[2]
    paddedInput = np.zeros((max(Input.shape),max(Input.shape),max(Input.shape)))
    paddedInput = np.pad(Input, ((int(math.ceil(pad[0,0]/2)),
        int(math.floor(pad[0,0]/2))),(int(math.ceil(pad[1,0]/2)),
        int(math.floor(pad[1,0]/2))),(int(math.ceil(pad[2,0]/2)),
        int(math.floor(pad[2,0]/2)))), 'constant', constant_values=0)
    paddedInput.resize((16,16,16))

def read_tts_footer(file_name):
    bin_file = open(file_name, "rb")
    prefab = {}

    # get properties not from tts file
    prefab["name"] = ntpath.basename(file_name)

    # get tts header properties from file (header is first 14 bytes of file)
    prefab["header"] = unpack(bin_file, "s", 4) # 4 byte header is always the string: "tts "
    prefab["version"] = unpack(bin_file, "I")   # next 4 bytes are version, but only the first byte matters
    prefab["size_x"] = unpack(bin_file, "H")    # each size value is 2 bytes, but again only the first byte matters
    prefab["size_y"] = unpack(bin_file, "H")    # each size value is 2 bytes, but again only the first byte matters
    prefab["size_z"] = unpack(bin_file, "H")    # each size value is 2 bytes, but again only the first byte matters
    prefab["total_blocks"] = prefab["size_x"]*prefab["size_y"]*prefab["size_z"]

    prefab["layers"] = []
    for layer_index in range(prefab["size_z"]):
        prefab["layers"].append([])
        for row_index in range(prefab["size_y"]):
            prefab["layers"][layer_index].append([])
            for block_index in range(prefab["size_x"]):
                prefab["layers"][layer_index][row_index].append(None)
                value = unpack(bin_file, "I")
                prefab["layers"][layer_index][row_index][block_index] = value

    footer_bytes = []
    byte = bin_file.read(1)
    while byte:
        footer_bytes.append(byte[0])
        byte = bin_file.read(1)
    prefab["footer"] = footer_bytes
    return prefab
    # for b in footer_bytes:
    #     print('{:4d}'.format(b), end='')

def layers_to_array(prefab):
    result = []
    for layer_index in range(prefab["size_z"]):
        for row_index in range(prefab["size_y"]):
            for block_index in range(prefab["size_x"]):
                result.append(prefab["layers"][layer_index][row_index][block_index])
    return np.asarray(result)

if __name__ == '__main__':
    conf = Config.getInstance()
    totalPrefabs = 0
    rootdir = conf.get("gamePrefabsFolder")
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file.endswith(".tts") and "house" in file:
                totalPrefabs += 1
                filename = os.path.join(subdir, file)
                print("reading tts file: {}".format(file))
                tts_data = read_tts_file(filename)
                block_data = layers_to_array(tts_data)
                v = Voxels(file, (tts_data["size_x"], tts_data["size_y"], tts_data["size_z"]), block_data)
                v.as_training_image()
    print("total prefabs: " + str(totalPrefabs))