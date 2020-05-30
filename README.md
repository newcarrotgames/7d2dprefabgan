# Using A Generative Adversarial Network To Create 7D2D Points Of Interest
## **Please note**: This is a work in progress. You're welcome to clone anything here, just don't expect it to work :).
This outline seeks to design a process for using GANs to procedurally create logical groups of 3D Voxel data that mimic existing POI structures. The process described in this document only serves as a proof of concept to explore the generation of voxel based content using machine learning. The adversarial network used in this example may not understand that the 2D data it is presented represents a 3D structure, but hopefully the pipeline created here can be reused by a different system specifically created to work with 3D data.

Track the progress of this project here: http://newcarrots.games/

GAN code is here: 

- [Deep Convolutional Generative Adversarial Network](https://www.tensorflow.org/tutorials/generative/dcgan)
- [docs/dcgan.ipynb at master · tensorflow/docs](https://github.com/tensorflow/docs/blob/master/site/en/tutorials/generative/dcgan.ipynb)

7D2D Prefab Technical Info:

- [Prefabs](https://7daystodie.gamepedia.com/Prefabs)
- https://forums.7daystodie.com/forum/-7-days-to-die-pc/game-modification/prefabs/73952-getting-started-prefabbing-complete-poi-creation

To run some of the examples, you'll need to create a config.ini file that looks like this:

    [DEFAULT]
    gamePrefabsFolder = [7D2D STEAM FOLDER CONTAINING PREFABS]

On Windows, the folder is usually (_escape as needed_):

    C:\Program Files (x86)\Steam\steamapps\common\7 Days To Die\Data\Prefabs

