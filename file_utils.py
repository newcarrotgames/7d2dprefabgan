import struct

def unpack(bin_file, data_type, length_arg=0):
    #integer or unsigned integer
    if data_type == "i" or data_type == "I":
        return int(struct.unpack(data_type, bin_file.read(4))[0])
    #short or unsigned short
    elif data_type == "h" or data_type == "H":
        return int(struct.unpack(data_type, bin_file.read(2))[0])
    #string
    elif data_type == "s":
        return struct.unpack(str(length_arg) + data_type, bin_file.read(length_arg))[0].decode("utf-8")
    #char
    elif data_type == "c":
        return struct.unpack(data_type, bin_file.read(1))[0]
    #byte or unsigned byte
    elif data_type == "b" or data_type == "B":
        return int(struct.unpack(data_type, bin_file.read(1))[0])

def pack(bin_file, data_type, data):
    data_type = data_type.lower()
    # integer or unsigned integer
    if data_type == "i":
        bin_file.write(struct.pack("<i", data))
    # short or unsigned short
    elif data_type == "h":
        bin_file.write(struct.pack("<h", data))
    # string
    elif data_type == "s":
        bin_file.write(data.encode('ascii'))
    # char
    elif data_type == "c":
        bin_file.write(struct.pack("<c", data))
    # byte or unsigned byte
    elif data_type == "b":
        bin_file.write(struct.pack("<b", data))