import os
import time
import pygame
import random
from file_utils import unpack

def getTTSHeader(filename):
    bin_file = open(filename, "rb")
    prefab = {}
    prefab["header"] = unpack(bin_file, "s", 4)
    prefab["version"] = unpack(bin_file, "I")
    prefab["size_x"] = unpack(bin_file, "H")
    prefab["size_y"] = unpack(bin_file, "H")
    prefab["size_z"] = unpack(bin_file, "H")
    return prefab

def printHeaderInfo(prefab):
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
                prefab = getTTSHeader(filename)
                printHeaderInfo(prefab)
    print("total prefabs: " + str(totalPrefabs))

main()