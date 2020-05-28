import os
from util import read_tts_file, resize_prefab, layers_to_array
from config import Config
from pathlib import Path
import numpy as np

def load():
    conf = Config.getInstance()
    totalPrefabs = 0
    rootdir = conf.get("gamePrefabsFolder")
    prefabs = np.zeros(0)
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file.endswith(".tts"):
                totalPrefabs += 1
                filename = os.path.join(subdir, file)
                print("reading tts file: {}".format(file))
                tts_data = read_tts_file(filename)
                resized_prefab = resize_prefab(tts_data, (16, 16, 16))
                block_data = layers_to_array(resized_prefab)
                np.append(prefabs, block_data)
    return prefabs, []