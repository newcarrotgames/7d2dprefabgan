import struct
import time
import random
import ntpath
import numpy as np
import math

def unpack(bin_file, data_type, length_arg=0):
    #integer or unsigned integer
    if data_type == "i" or data_type == "I":
        return int(struct.unpack(data_type, bin_file.read(4))[0])
    #short or unsigned short
    elif data_type == "h" or data_type == "H":
        return int(struct.unpack(data_type, bin_file.read(2))[0])
    #string
    elif data_type == "s":
        return struct.unpack(str(length_arg) + data_type, bin_file.read(length_arg))[0].decode("utf-8")
    #char
    elif data_type == "c":
        return struct.unpack(data_type, bin_file.read(1))[0]
    #byte or unsigned byte
    elif data_type == "b" or data_type == "B":
        return int(struct.unpack(data_type, bin_file.read(1))[0])

def read_tts_file(file_name):
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
    prefab["num_blocks"] = prefab["size_x"] * prefab["size_y"] * prefab["size_z"]
    prefab["layers"] = []
    
    # todo: read as sequential array
    for layer_index in range(prefab["size_z"]):
        prefab["layers"].append([])
        for row_index in range(prefab["size_y"]):
            prefab["layers"][layer_index].append([])
            for block_index in range(prefab["size_x"]):
                prefab["layers"][layer_index][row_index].append(None)
                value = unpack(bin_file, "I")
                #get rid of flags, block id can only be less than 2048
                block_id = value & 2047
                flags = value >> 11
                prefab["layers"][layer_index][row_index][block_index] = block_id

    # read density
    prefab["density"] = []
    for x in range(prefab["num_blocks"]):
        value = unpack(bin_file, "b")
        prefab["density"].append(value)

    # read damage
    prefab["damage"] = []
    for x in range(prefab["num_blocks"]):
        value = unpack(bin_file, "h")
        prefab["damage"].append(value)

    # read textures (empty?)
    prefab["num_textures"] = unpack(bin_file, "h")
    prefab["textures"] = []

    # read tile entities (empty?)
    prefab["num_tile_entities"] = unpack(bin_file, "h")
    prefab["tile_entities"] = []
    return prefab

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
    new_prefab["layers"] = resized_voxel_data
    return new_prefab

def layers_to_array(prefab):
    result = []
    for layer_index in range(prefab["size_z"]):
        for row_index in range(prefab["size_y"]):
            for block_index in range(prefab["size_x"]):
                result.append(prefab["layers"][layer_index][row_index][block_index])
    return np.asarray(result)