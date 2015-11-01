from huffman import HuffmanTree, LEFT, RIGHT
from utilities import unpack_data, scan
import sys


TREE_SIZE_BITS = 16
BIT = 1
BYTE = 8


# TODO: Get this working, it doesn't now:
def resurrect_tree(bit_string):
    # Algorithm for storing and resurrecting came from this SO answer:
    # http://stackoverflow.com/a/759766/3199099
    bits = scan(bit_string)

    def _interpret_bit():
        next_bit = next(bits)

        if next_bit == '1':
            next_byte = ''.join([next(bits) for _ in range(BYTE)])
            char = chr(int(next_byte, 2))
            new_node = HuffmanTree(char=char)
        elif next_bit == '0':
            left = _interpret_bit()
            right = _interpret_bit()
            new_node = HuffmanTree(left_child=left, right_child=right)
        return new_node

    return _interpret_bit()


def decode(data):
    encoded_bit_string = unpack_data(data)
    encoded_tree_size = int(encoded_bit_string[0:TREE_SIZE_BITS], 2)
    end_of_tree = TREE_SIZE_BITS + encoded_tree_size
    encoded_tree = encoded_bit_string[TREE_SIZE_BITS:end_of_tree]
    tree = resurrect_tree(encoded_tree)

    current_node = tree
    decoded_data = []
    for i in encoded_bit_string[end_of_tree:]:
        if i == LEFT:
            current_node = current_node.left_child
        elif i == RIGHT:
            current_node = current_node.right_child
        if current_node.is_leaf:
            decoded_data.append(current_node.char)
            current_node = tree
    return ''.join(decoded_data)


def dehuffman(inputfile, outputfile):
    with open(inputfile, 'rb') as f:
        encoded_data = f.read()

    decoded_data = decode(encoded_data)
    with open(outputfile, 'wb') as f:
        f.write(decoded_data)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        dehuffman(sys.argv[1], sys.argv[2])
    else:
        print 'Usage:\ndehuffman.py inputfile outputfile'
