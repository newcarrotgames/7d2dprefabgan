"""
7 Days to Die TTS decoder
Copyright (C) 2017 Liam Brandt <brandt.liam@gmail.com>

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
from file_utils import unpack
import ntpath

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

if __name__ == '__main__':
    read_tts_file("output/aifab_01.tts")