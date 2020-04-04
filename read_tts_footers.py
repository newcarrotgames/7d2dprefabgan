import os
import time
import random
from file_utils import unpack
from config import Config
from pathlib import Path
import ntpath
import struct

def print_tts_details(prefab):
    print("Prefab version: " + str(prefab["version"]))
    print("Dimensions: " + str(prefab["size_x"]) + "x" + str(prefab["size_y"]) + "x" + str(prefab["size_z"]))
    print("total block: {}".format(prefab["total_blocks"]))
    print("footer size: {}".format(len(prefab["footer"])))
    print("ratio: {}".format(len(prefab["footer"]) / prefab["total_blocks"]))


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

if __name__ == '__main__':
    conf = Config.getInstance()
    totalPrefabs = 0
    rootdir = conf.get("gamePrefabsFolder")
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file.endswith(".tts"):
                totalPrefabs += 1
                filename = os.path.join(subdir, file)
                print("reading tts file (len: {}): {}".format(Path(filename).stat().st_size, file))
                prefab = read_tts_footer(filename)
                print_tts_details(prefab)
    print("total prefabs: " + str(totalPrefabs))