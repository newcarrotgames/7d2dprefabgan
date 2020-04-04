import os
import time
import random
from file_utils import unpack
from config import Config
from pathlib import Path

# nim file notes:
#
# the first four bytes always seem to be:
#
# 1 0 0 0
# 
# next four bytes:
#
# 42 0 0 0
#
# I _think_ the first byte in this sequence is the number of unique block types in the file.
#
# 2 0 0 0
#
# not sure what this means yet
#
# 

def getNIMHeader(filename):
    bin_file = open(filename, "rb")
    header = []
    for i in range(12):
        b = unpack(bin_file, "B")
        header.append(b)
    return header

def printHeaderInfo(header):
    for b in header:
        print('{:3d}|'.format(b), end='')
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


if __name__ == '__main__':
    main()