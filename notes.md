# Using A Generative Adversarial Network To Create 7D2D Points Of Interest
This outline seeks to design a process for using GANs to procedurally create logical groups of 3D Voxel data that mimic existing POI structures. The process described in this document only serves as a proof of concept to explore the generation of voxel based content using machine learning. The main concern I have with this approach is that the adversarial network used in this example may not understand that the 2D data it is presented represents a 3D structure, therefore the relationships between points on the “substrate” images need to be precise, but hopefully the pipeline created can be reused by a different system capable of working with 3D data natively.

GAN code is here: 

- [Deep Convolutional Generative Adversarial Network](https://www.tensorflow.org/tutorials/generative/dcgan)
- [docs/dcgan.ipynb at master · tensorflow/docs](https://github.com/tensorflow/docs/blob/master/site/en/tutorials/generative/dcgan.ipynb)

7D2D Prefab Technical Info:

- [Prefabs](https://7daystodie.gamepedia.com/Prefabs)
- https://forums.7daystodie.com/forum/-7-days-to-die-pc/game-modification/prefabs/73952-getting-started-prefabbing-complete-poi-creation

variable name conventions

w = width (x)
h = height (y)
d = depth (z)
r = rotation (quaternion?)
n = integer (amount or count or number of)
dir = specific axis (x y or z)

non-primitive types

vec3 = (x, y, z)

classes

The voxel class was my first idea for storing the block data for the prefab, but I decided not to use it because it would always require an extra step when converted to and from array structures that the GAN code, which was just copied from another project, understands. The only value I can see in having it is providing some helper methods when dealing with the block flags particularly the bits that represent physical orientation (rotation) which can be handled by either a decorator class or a static helper method. This does present another problem of representing the blocks rotation within the training image but this could also be done using something similar to marching cubes.

Voxel {
blockId int16
flags int16

Voxel(blockid, flags)
Voxel(blockid)
// flags by name?
getFlag(flagId int) bool // id is bit position?
setFlag(flagId int, value bool)
getRotation() // just return value of rot flag?
setRotation() // this wont be part of poc
// other flags are? loot/zomb spawns
// do some air blocks have these flags?
}

Voxels {
// fields
Dimensions Vector3
Data Voxel[]

// methods
getVoxel(Vector3) (Voxel)
getYLevel(int y) (Voxels)
getPlane(wdOrH, n)
getRun(x, y, z, d, n)

Voxels(Dimension, data)
Voxels(Dimension)
ToImage()
FromImage()
FromTTS()
ToTTS()
}

getVoxel(vec3) {
i = y*this.h + z*this.d + x
return this.data[i]
}

// static methods from another class
coordIndex(vec3){
return y*this.h + z*this.d + x
}

coordIndex(vec2) {
}

// don’t want to call getVoxel every time 
getYPlane(dir, n) {
level = []
for w,d { 
level += getVoxel(i)
}
}

other notes

models could be trained to augment existing structures and then called in succession to prevent random “blobs”.

restate above

floors? could pick a random number or keep stats of existing prefabs and then manually pick sizes from biome label

how to divide?


Convert voxels to flattened 2d image

use numpy reshape to convert voxels array data to image data?
toIntArray()

Does python image have a paste into method?
yes

convert layer to image to call paste method?
no, toImage() after calling getPlane works for this use cases

how to represent enemy and loot locations so the same neural network can be used? or any gan for that matter?

create regions for placing items or mobs 

scan for regions afterwards? partial region found and hollowed out. etc

plot?

whats even possible? tripwire reveals but pathing could drive prefab structure.
gan will need to be able to add to an existing structure
new plots?

names will be fun!
labels should come from names?
biome?

layers of abstraction from general concept or name to voxel data

// these classes are dependent on the gans interface
LayerConfig {

}

Layer {
Config LayerConfig
Pipeline PipelineConfig
Data *Voxels
Run()
Next *Layer
Prev *Layer
Input()
Output()
}

what are gans inputs and outputs?
better requirements?





GAN CODE

from __future__ import absolute_import, division, print_function, unicode_literals
 
try:
    # %tensorflow_version only exists in Colab.
    %tensorflow_version 2.x
except Exception:
    pass
 
import tensorflow as tf
 
tf.__version__
 
# To generate GIFs
!pip install imageio
 
import glob
import imageio
import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
from tensorflow.keras import layers
import time
 
from IPython import display
 
# why toss the test set out?
(train_images, train_labels), (_, _) = tf.keras.datasets.mnist.load_data()
 
train_images = train_images.reshape(train_images.shape[0], 28, 28, 1).astype('float32')
train_images = (train_images - 127.5) / 127.5 # Normalize the images to [-1, 1]
 
BUFFER_SIZE = 60000
BATCH_SIZE = 256
 
# Batch and shuffle the data
train_dataset = tf.data.Dataset.from_tensor_slices(train_images).shuffle(BUFFER_SIZE).batch(BATCH_SIZE)
 
 
def make_generator_model():
        model = tf.keras.Sequential()
        model.add(layers.Dense(7*7*256, use_bias=False, input_shape=(100,)))
        model.add(layers.BatchNormalization())
        model.add(layers.LeakyReLU())
 
        model.add(layers.Reshape((7, 7, 256)))
        assert model.output_shape == (None, 7, 7, 256) # Note: None is the batch size
 
        model.add(layers.Conv2DTranspose(128, (5, 5), strides=(1, 1), padding='same', use_bias=False))
        assert model.output_shape == (None, 7, 7, 128)
        model.add(layers.BatchNormalization())
        model.add(layers.LeakyReLU())
 
        model.add(layers.Conv2DTranspose(64, (5, 5), strides=(2, 2), padding='same', use_bias=False))
        assert model.output_shape == (None, 14, 14, 64)
        model.add(layers.BatchNormalization())
        model.add(layers.LeakyReLU())
 
        model.add(layers.Conv2DTranspose(1, (5, 5), strides=(2, 2), padding='same', use_bias=False, activation='tanh'))
        assert model.output_shape == (None, 28, 28, 1)
 
        return model
 
generator = make_generator_model()
 
noise = tf.random.normal([1, 100])
generated_image = generator(noise, training=False)
 
plt.imshow(generated_image[0, :, :, 0], cmap='gray')
 
def make_discriminator_model():
        model = tf.keras.Sequential()
        model.add(layers.Conv2D(64, (5, 5), strides=(2, 2), padding='same',
                                                                         input_shape=[28, 28, 1]))
        model.add(layers.LeakyReLU())
        model.add(layers.Dropout(0.3))
 
        model.add(layers.Conv2D(128, (5, 5), strides=(2, 2), padding='same'))
        model.add(layers.LeakyReLU())
        model.add(layers.Dropout(0.3))
 
        model.add(layers.Flatten())
        model.add(layers.Dense(1))
 
        return model
 
discriminator = make_discriminator_model()
decision = discriminator(generated_image)
print (decision)
 
# This method returns a helper function to compute cross entropy loss
cross_entropy = tf.keras.losses.BinaryCrossentropy(from_logits=True)
 
 
def discriminator_loss(real_output, fake_output):
        real_loss = cross_entropy(tf.ones_like(real_output), real_output)
        fake_loss = cross_entropy(tf.zeros_like(fake_output), fake_output)
        total_loss = real_loss + fake_loss
        return total_loss
 
def generator_loss(fake_output):
        return cross_entropy(tf.ones_like(fake_output), fake_output)
 
generator_optimizer = tf.keras.optimizers.Adam(1e-4)
discriminator_optimizer = tf.keras.optimizers.Adam(1e-4)
 
checkpoint_dir = './training_checkpoints'
checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
checkpoint = tf.train.Checkpoint(generator_optimizer=generator_optimizer,
                                                                 discriminator_optimizer=discriminator_optimizer,
                                                                 generator=generator,
                                                                 discriminator=discriminator)
 
 
EPOCHS = 50
noise_dim = 100
num_examples_to_generate = 16
 
# We will reuse this seed overtime (so it's easier)
# to visualize progress in the animated GIF)
seed = tf.random.normal([num_examples_to_generate, noise_dim])
 
# Notice the use of `tf.function`
# This annotation causes the function to be "compiled".
@tf.function
def train_step(images):
        noise = tf.random.normal([BATCH_SIZE, noise_dim])
 
        with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
            generated_images = generator(noise, training=True)
 
            real_output = discriminator(images, training=True)
            fake_output = discriminator(generated_images, training=True)
 
            gen_loss = generator_loss(fake_output)
            disc_loss = discriminator_loss(real_output, fake_output)
 
        gradients_of_generator = gen_tape.gradient(gen_loss, generator.trainable_variables)
        gradients_of_discriminator = disc_tape.gradient(disc_loss, discriminator.trainable_variables)
 
        generator_optimizer.apply_gradients(zip(gradients_of_generator, generator.trainable_variables))
        discriminator_optimizer.apply_gradients(zip(gradients_of_discriminator, discriminator.trainable_variables))
 
def train(dataset, epochs):
    for epoch in range(epochs):
        start = time.time()
 
        for image_batch in dataset:
            train_step(image_batch)
 
        # Produce images for the GIF as we go
        display.clear_output(wait=True)
        generate_and_save_images(generator,
                                                         epoch + 1,
                                                         seed)
 
        # Save the model every 15 epochs
        if (epoch + 1) % 15 == 0:
            checkpoint.save(file_prefix = checkpoint_prefix)
 
        print ('Time for epoch {} is {} sec'.format(epoch + 1, time.time()-start))
 
    # Generate after the final epoch
    display.clear_output(wait=True)
    generate_and_save_images(generator,
                                                     epochs,
                                                     seed)
 
def generate_and_save_images(model, epoch, test_input):
    # Notice `training` is set to False.
    # This is so all layers run in inference mode (batchnorm).
    predictions = model(test_input, training=False)
 
    fig = plt.figure(figsize=(4,4))
 
    for i in range(predictions.shape[0]):
            plt.subplot(4, 4, i+1)
            plt.imshow(predictions[i, :, :, 0] * 127.5 + 127.5, cmap='gray')
            plt.axis('off')
 
    plt.savefig('image_at_epoch_{:04d}.png'.format(epoch))
    plt.show()
 
train(train_dataset, EPOCHS)
 
checkpoint.restore(tf.train.latest_checkpoint(checkpoint_dir))
 
 
# Display a single image using the epoch number
def display_image(epoch_no):
    return PIL.Image.open('image_at_epoch_{:04d}.png'.format(epoch_no))
 
display_image(EPOCHS)
 
 
anim_file = 'dcgan.gif'
 
with imageio.get_writer(anim_file, mode='I') as writer:
    filenames = glob.glob('image*.png')
    filenames = sorted(filenames)
    last = -1
    for i,filename in enumerate(filenames):
        frame = 2*(i**0.5)
        if round(frame) > round(last):
            last = frame
        else:
            continue
        image = imageio.imread(filename)
        writer.append_data(image)
    image = imageio.imread(filename)
    writer.append_data(image)
 
import IPython
if IPython.version_info > (6,2,0,''):
    display.Image(filename=anim_file)

Error:

2020-02-29 12:00:20.694694: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cudart64_101.dll
Traceback (most recent call last):
  File "g:/7d2d/tts_decode/tts_train.py", line 20, in <module>
    (train_images, train_labels), (_, _) = get_fake_training_data()
  File "g:\7d2d\tts_decode\training_data.py", line 11, in get_fake_training_data
    training_images = np.asarray(training_images).reshape(-1, 512, 512, 1)
ValueError: cannot reshape array of size 15625 into shape (512,512,1)





12x16x8

grid_width = round(sqrt(height), R_UP)
grid_depth = round(sqrt(height), R_DOWN)
voxelsImage = Image(grid_width * width, grid_depth * depth)

for (i=0;i<height;i++) {
run = voxels.getHorizontalCrossSection(i)
xsImage=Image((w,d), run.toIntArray())
x = i % grid_width * width
y = i / grid_width * height

}

forget data as array of voxels create a voxel class that takes int32 if needed

fromImage

how can we know what these values are from the image? 

how to know what the gan produces? 

that must be why these networks always deal with images of the same size, so generated prefabs will always be the same size?
Could scale results and somehow feed them back into gan?

create a large enough grid to handle most cases?

generate synthetic data from basic shapes

grid_width 
grid_height

starting size?

16x16x16 = 2^4 * 2^4 * 2^4 = 2^12

64x64 = 8 * 8 * 8 * 8 = (2^3)^4 = 2^12

4096

Block value from single block prefab:

1100001100000010000000100000000
 098765432109876543210987654321