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

# _reader.ReadInt32();
# lock (this)
# {
#     Array.Clear(idsToNames, 0, idsToNames.Length);
#     namesToIds.Clear();
#     int num = _reader.ReadInt32();
#     for (int i = 0; i < num; i++)
#     {
#         int num2 = _reader.ReadInt32();
#         string text = _reader.ReadString();
#         idsToNames[num2] = text;
#         namesToIds[text] = num2;
#     }
#     isDirty = false;
# }

def read_nim(filename):
    # open file in binary mode
    bin_file = open(filename, "rb")

    # skip first four bytes
    unpack(bin_file, "I")

    # create map var
    map = {}

    # read number of maps
    num = unpack(bin_file, "I")
    for i in range(num):
        num2 = unpack(bin_file, "I")
        slen = unpack(bin_file, "B")
        name = unpack(bin_file, "s", slen)
        map[num2] = name
    return map

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

def read_nim_headers():
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

structural_phrases = ['wood', 'concrete']

def is_structural_block(block_id, block_type_map):
    block_type = block_type_map[block_id]
    for phrase in structural_phrases:
        if phrase in block_type.lower():
            return True
    return False

def main():
    read_nim("prefabs/trailer_03/trailer_03.blocks.nim")

if __name__ == '__main__':
    main()