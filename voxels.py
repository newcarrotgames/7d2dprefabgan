import math

class Voxels:
    def __init__(self, name, dim, data):
        self.name = name
        self.width = dim[0]
        self.height = dim[1]
        self.depth = dim[2]
        self.data = data

    def get_cross_section(self, n):
        cross_section_size = self.width * self.depth
        offset = cross_section_size * n
        return self.data[offset:offset+cross_section_size]

    def as_training_image(self):
        sqr_height = math.sqrt(self.height)
        grid_width = math.ceil(sqr_height)
        grid_depth = math.floor(sqr_height)
        img_w = grid_width * self.width
        img_h = grid_depth * self.depth
        img_data = np.zeros((img_h, img_w, 3), dtype=np.uint8)
        training_image = Image.fromarray(img_data, 'RGB')
        for i in self.height:
            cross_section = self.get_cross_section(i)
            x = i % grid_width * width
            y = i / grid_width * height
            sub_image = Image.fromarray(cross_section, 'RGB')
            training_image.paste(sub_image, (x, y))
        image.save("dataset\\train\\prefab_{}.png".format(self.name))