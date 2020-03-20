"""
7 Days to Die TTS encoder
Copyright (C) 2020 David Harris <newcarrotgames@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import struct
import time
import pygame
import random
from file_utils import pack
from tts_utils import draw_prefab

def random_prefab():
    # create random prefab, size = 16x16x16 blocks
    prefab = {}
    prefab["version"] = 13
    prefab["size_x"] = 16
    prefab["size_y"] = 16
    prefab["size_z"] = 16

    # create random voxel data for prefab
    prefab["layers"] = []
    for layer_index in range(prefab["size_z"]):
        prefab["layers"].append([])
        for row_index in range(prefab["size_y"]):
            prefab["layers"][layer_index].append([])
            for block_index in range(prefab["size_x"]):
                prefab["layers"][layer_index][row_index].append(None)
                block_id = 0
                if random.randint(0, 8) == 0:
                    block_id = random.randint(0, 2048)
                prefab["layers"][layer_index][row_index][block_index] = block_id

    return prefab

def encode(prefab, filename):
    # open the above binary file for writing
    bin_file = open(filename, "wb")

    # write header and supported game version
    pack(bin_file, "s", "tts ")
    pack(bin_file, "i", prefab["version"])

    # write prefab dimensions
    pack(bin_file, "h", prefab["size_x"])
    pack(bin_file, "h", prefab["size_y"])
    pack(bin_file, "h", prefab["size_z"])

    # output prefab header info
    print("Prefab version: " + str(prefab["version"]))
    print("Dimensions: " + str(prefab["size_x"]) + "x" + str(prefab["size_y"]) + "x" + str(prefab["size_z"]))

    # write prefab voxel data
    for layer_index in range(prefab["size_z"]):
        for row_index in range(prefab["size_y"]):
            for block_index in range(prefab["size_x"]):
                pack(bin_file, "i", prefab["layers"][layer_index][row_index][block_index])

    # render image of random prefab
    draw_prefab(prefab)

    # remaining files?
    # nim
    # mesh
    # ins
    # xml

def main():
    bin_file = open("test.dat", "wb")
    i = 128
    bin_file.write(struct.pack(">i", i))

main()
