import math
from PIL import Image
import numpy as np
from tts_write import encode

class Voxels:
    def __init__(self, name, dim, data):
        self.name = name
        self.width = dim[0]
        self.height = dim[1]
        self.depth = dim[2]

        sqr_height = math.sqrt(self.height)
        self.grid_width = math.ceil(sqr_height)
        self.grid_depth = math.floor(sqr_height)
        self.grid_cell_size = self.width * self.depth

        self.data = data

    def get_cross_section(self, n):
        cross_section_size = self.width * self.depth
        offset = cross_section_size * n
        run = self.data[offset:offset+cross_section_size]
        xs = []
        for y in range(self.depth):
            line = run[y * self.width:y * self.width + self.width]
            xs.append(line)
        return np.asarray(xs, dtype=np.uint8)

    def set_value_with_image_coords(self, x, z, val):
        grid_col = math.floor(x / self.width)
        grid_row = math.floor(z / self.depth)
        cell_x = x % self.width
        cell_z = z % self.depth
        index = (grid_row * self.grid_cell_size * self.grid_width) + (grid_col * self.grid_cell_size) + cell_z * self.width + cell_x
        self.data[index] = val

    def get_value_at(self, layer_index, row_index, block_index):
        return self.data[self.grid_cell_size * layer_index + row_index * self.width + block_index]

    def to_tts_file(self, filename):
        prefab = {}
        prefab["version"] = 13
        prefab["size_x"] = self.width
        prefab["size_y"] = self.height
        prefab["size_z"] = self.depth
        prefab["layers"] = []
        for layer_index in range(prefab["size_z"]):
            prefab["layers"].append([])
            for row_index in range(prefab["size_y"]):
                prefab["layers"][layer_index].append([])
                for block_index in range(prefab["size_x"]):
                    prefab["layers"][layer_index][row_index].append(None)
                    #prefab["layers"][layer_index][row_index][block_index] = self.get_value_at(layer_index, row_index, block_index)
                    val = self.get_value_at(layer_index, row_index, block_index)
                    if val > 0:
                        val = 98657 # 61 81 01 00 = wood block from test3.tts
                    prefab["layers"][layer_index][row_index][block_index] = val
        encode(prefab, filename)

    def from_training_image(self, filename):
        # Open the image form working directory
        image = Image.open(filename)
        # summarize some details about the image
        print(image.format)
        print(image.size)
        print(image.mode)
        data = np.array(image)
        self.data = np.zeros(image.size[0] * image.size[1], dtype=np.uint8)
        for row_index, row in enumerate(data):
            for pixel_index, pixel in enumerate(row):
                self.set_value_with_image_coords(pixel_index, row_index, pixel[0])
                # print('pixel at {}, {}: {}'.format(pixel_index, row_index, pixel))

    def as_training_image(self):
        sqr_height = math.sqrt(self.height)
        grid_width = math.ceil(sqr_height)
        grid_depth = math.floor(sqr_height)
        img_w = grid_width * self.width
        img_h = grid_depth * self.depth
        img_data = np.zeros((img_h, img_w, 3), dtype=np.uint8)
        print("grid_width: {}, grid_depth: {}".format(grid_width, grid_depth))
        print("img_w: {}, img_h: {}".format(img_w, img_h))
        training_image = Image.fromarray(img_data)
        for i in range(self.height):
            cross_section = self.get_cross_section(i)
            x = i % grid_width * self.width
            y = math.ceil(i / grid_width) * self.height
            sub_image = Image.fromarray(cross_section)
            training_image.paste(sub_image, (x, y))
        training_image.save("datasets\\training\\prefab_{}.png".format(self.name))


if __name__ == '__main__':
    v = Voxels("prefab1", (7,16,7), [])
    v.from_training_image('generated_prefab_100.png')
    v.to_tts_file('output\\aifab_02.tts')