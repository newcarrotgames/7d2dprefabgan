import pygame
import random

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