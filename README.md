# Using A Generative Adversarial Network To Create 7D2D Points Of Interest
This outline seeks to design a process for using GANs to procedurally create logical groups of 3D Voxel data that mimic existing POI structures. The process described in this document only serves as a proof of concept to explore the generation of voxel based content using machine learning. The main concern I have with this approach is that the adversarial network used in this example may not understand that the 2D data it is presented represents a 3D structure, therefore the relationships between points on the “substrate” images need to be precise, but hopefully the pipeline created can be reused by a different system capable of working with 3D data natively.

GAN code is here: 

- [Deep Convolutional Generative Adversarial Network](https://www.tensorflow.org/tutorials/generative/dcgan)
- [docs/dcgan.ipynb at master · tensorflow/docs](https://github.com/tensorflow/docs/blob/master/site/en/tutorials/generative/dcgan.ipynb)

7D2D Prefab Technical Info:

- [Prefabs](https://7daystodie.gamepedia.com/Prefabs)
- https://forums.7daystodie.com/forum/-7-days-to-die-pc/game-modification/prefabs/73952-getting-started-prefabbing-complete-poi-creation