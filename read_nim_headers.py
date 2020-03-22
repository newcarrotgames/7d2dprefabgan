import os
import time
import random
from file_utils import unpack
from config import Config
from pathlib import Path

def getNIMHeader(filename):
    bin_file = open(filename, "rb")
    header = []
    for i in range(8):
        b = unpack(bin_file, "B")
        header.append(b)
    return header

def printHeaderInfo(header):
    for b in header:
        print('{} '.format(b), end='')
    print('')

def main():
    conf = Config.getInstance()
    totalPrefabs = 0 
    rootdir = conf.get("gamePrefabsFolder")
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file.endswith(".nim"):
                totalPrefabs += 1
                filename = os.path.join(subdir, file)
                print("reading nim file (len: {}): {}".format(Path(filename).stat().st_size, file))
                header = getNIMHeader(filename)
                printHeaderInfo(header)
    print("total prefabs: " + str(totalPrefabs))

main()