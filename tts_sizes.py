import os
import struct
import time
import pygame
import random


def unpack(bin_file, data_type, length_arg=0):
    # integer or unsigned integer
    if data_type == "i" or data_type == "I":
        return int(struct.unpack(data_type, bin_file.read(4))[0])
    # short or unsigned short
    elif data_type == "h" or data_type == "H":
        return int(struct.unpack(data_type, bin_file.read(2))[0])
    # string
    elif data_type == "s":
        return struct.unpack(str(length_arg) + data_type, bin_file.read(length_arg))[0]
    # char
    elif data_type == "c":
        return struct.unpack(data_type, bin_file.read(1))[0]
    # byte or unsigned byte
    elif data_type == "b" or data_type == "B":
        return int(struct.unpack(data_type, bin_file.read(1))[0])

def getTTSHeader(filename):
    bin_file = open(filename, "rb")
    prefab = {}
    prefab["header"] = unpack(bin_file, "s", 4)
    prefab["version"] = unpack(bin_file, "I")
    prefab["size_x"] = unpack(bin_file, "H")
    prefab["size_y"] = unpack(bin_file, "H")
    prefab["size_z"] = unpack(bin_file, "H")
    print("\tPrefab version: " + str(prefab["version"]))
    print("\tDimensions: " + str(prefab["size_x"]) + "x" + str(prefab["size_y"]) + "x" + str(prefab["size_z"]))
    print("\tTotal size: " + str(prefab["size_x"]*prefab["size_y"]*prefab["size_z"]) + " blocks")

def main():
    totalPrefabs = 0
    rootdir = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\7 Days To Die\\Data\\Prefabs"
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file.endswith(".tts"):
                totalPrefabs += 1
                filename = os.path.join(subdir, file)
                print(file)
                getTTSHeader(filename)
    print("total prefabs: " + str(totalPrefabs))
    
main()