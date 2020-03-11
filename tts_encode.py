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

def pack(bin_file, data_type, data):
    data_type = data_type.lower()
    # integer or unsigned integer
    if data_type == "i":
        bin_file.write(struct.pack(">i", data))
    # short or unsigned short
    elif data_type == "h":
        bin_file.write(struct.pack(">h", data))
    # string
    elif data_type == "s":
        data = bytes(data, 'utf-8')
        bin_file.write(struct.pack("I%ds" % (len(data),), len(data), data))
    # char
    elif data_type == "c":
        bin_file.write(struct.pack(">c", data))
    # byte or unsigned byte
    elif data_type == "b":
        bin_file.write(struct.pack(">b", data))

def draw_prefab(prefab):
    colors = {}

    block_size = (10, 10, 3)

    image_size_x = ( (1*prefab["size_x"]*block_size[0]) + (prefab["size_z"]*block_size[2]) + block_size[0])
    image_size_y = ( (1*prefab["size_y"]*block_size[1]) + (prefab["size_z"]*block_size[2]) + block_size[1])
    image = pygame.surface.Surface((image_size_x, image_size_y))

    z = 0
    for each_layer in prefab["layers"]:
        y = 0
        for each_row in each_layer:
            x = 0
            for each_block in each_row:
                if each_block != 0:
                    if each_block not in colors:
                        colors[each_block] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    draw_color = colors[each_block]
                    draw_x = (x*block_size[0]) + (z*block_size[2])
                    draw_y = (-y*block_size[1]) + (z*block_size[2]) + prefab["size_y"]*block_size[1]
                    draw_rect = (draw_x, draw_y, block_size[0], block_size[1])

                    pygame.draw.rect(image, draw_color, draw_rect, 0)
                    pygame.draw.rect(image, (0, 0, 0), draw_rect, 1)
                x += 1
            y += 1
        z += 1

    print("Block ids and colors: " + str(colors))
    pygame.image.save(image, "output.png")

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

def encode():
    # make a random prefab for testing output
    prefab = random_prefab()

    # change the output file name here
    file_name = "test.tts"

    # open the above binary file for writing
    bin_file = open(file_name, "wb")

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
