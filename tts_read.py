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
    pygame.image.save(image, "output/output_{}.png".format(prefab["name"]))


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

    print("Prefab version: " + str(prefab["version"]))
    print("Dimensions: " + str(prefab["size_x"]) + "x" + str(prefab["size_y"]) + "x" + str(prefab["size_z"]))

    prefab["layers"] = []

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

    draw_prefab(prefab)


if __name__ == '__main__':
    read_tts_file("prefabs/test2/test2.tts")