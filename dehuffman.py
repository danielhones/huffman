from huffman import build_tree, LEFT, RIGHT, DECODING_FILE, binary_for, pad_to_full_byte, BYTE_LENGTH
import pickle
import sys


# TODO: put utility functions like get_next_byte, pad_to_full_byte, pack_data, etc in separate file

def get_next_byte(ch):
    next_byte = pad_to_full_byte(binary_for(ch))
    return next_byte


def unpack_data(data):
    binary_data = [get_next_byte(ch) for ch in data]
    bit_string = ''.join(binary_data)
    return bit_string


def decode(data, tree):
    encoded_bit_string = unpack_data(data)
    current_node = tree
    decoded_data = []
    for i in encoded_bit_string:
        if i == LEFT:
            current_node = current_node.left_child
        elif i == RIGHT:
            current_node = current_node.right_child
        if current_node.is_leaf:
            decoded_data.append(current_node.char)
            current_node = tree
    return ''.join(decoded_data)


def resurrect_tree(inputfile):
    pass


def dehuffman(inputfile, outputfile):
    tree = resurrect_tree(inputfile)

    with open(inputfile, 'rb') as f:
        encoded_data = f.read()

    decoded_data = decode(encoded_data, tree)
    with open(outputfile, 'wb') as f:
        f.write(decoded_data)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        dehuffman(sys.argv[1], sys.argv[2])
    else:
        print 'Usage:\ndehuffman.py inputfile outputfile'
