import glob
from PIL import Image, ImageOps

for image_file in glob.iglob('datasets\\training\\*.png'):
    print(image_file)
    image = Image.open(image_file)
    image = ImageOps.mirror(image)
    image.save(image_file.replace(".png", ".pad.png"))