from collections import defaultdict
from bisect import bisect_left
import sys


BYTE_LENGTH = 8
LEFT = '0'
RIGHT = '1'


class HuffmanTree(object):
    def __init__(self, count=0, left_child=None, right_child=None, char=None):
        self.char = char
        self.count = count
        self.left_child = left_child
        self.right_child = right_child

    def encode_data(self, filepath):
        self.build_encoding()
        with open(filepath, 'rb') as infile:
            encoded_data = [self.encoding[ch] for ch in infile.read()]
            return ''.join(encoded_data)

    def build_encoding(self, encoding=None, bit_array=None):
        if encoding is None:
            encoding = {}
        if bit_array is None:
            bit_array = []

        if self.left_child is not None:
            self.left_child.build_encoding(encoding, bit_array + [LEFT])
        if self.right_child is not None:
            self.right_child.build_encoding(encoding, bit_array + [RIGHT])
        if self.char is not None:
            bit_string = ''.join(bit_array)
            encoding[self.char] = bit_string
        self.encoding = encoding
        return encoding

    @property
    def is_leaf(self):
        return self.char is not None

    def __repr__(self):
        return 'HuffmanTree(count=%s, char=%s)' % (self.count, self.char)

    def __cmp__(self, other):
        return cmp(self.count, other)


def count_chars(filepath):
    with open(filepath, 'rb') as f:
        chars = f.read()

    counts = defaultdict(int)
    for ch in chars:
        counts[ch] += 1
    return counts


def build_tree(counts):
    tree = [HuffmanTree(counts[ch], char=ch) for ch in counts]
    tree.sort()

    while len(tree) > 1:
        left, right = tree.pop(0), tree.pop(0)
        new_node = HuffmanTree(left.count + right.count, left, right)
        insertion_point = bisect_left(tree, new_node)
        tree.insert(insertion_point, new_node)
    return tree[0]


def encode_data(filepath, encoding):
    with open(filepath, 'rb') as infile:
        encoded_data = [encoding[ch] for ch in infile.read()]
    return ''.join(encoded_data)


def pack_data(data):
    """
    Data should be a string of 1's and 0's.  As it stands now, this function will produce some junk on the last byte if
    the length of data is not divisible by 8.
    TODO: Find a way to deal with that junk data at the end
    """
    packed_data = []
    for i in range(0, len(data), 8):
        bit_string = data[i:i+8]
        next_char = chr(int(bit_string, 2))
        packed_data.append(next_char)
    return ''.join(packed_data)


def pad_to_full_byte(incomplete_byte):
    # Add leading 0's to make it a full byte
    full_byte = '0' * (BYTE_LENGTH - len(incomplete_byte)) + incomplete_byte
    return full_byte


def binary_for(char):
    return str(bin(ord(char)))[2:]


def preserve_tree(node):
    # TODO: this could probably be a method on HuffmanTree, but I don't know if it should be
    preserved = []
    if node.is_leaf:
        preserved.append('1')
        preserved.append(pad_to_full_byte(binary_for(node.char)))
    else:
        preserved.append('0')
        preserved.append(preserve_tree(node.left_child))
        preserved.append(preserve_tree(node.right_child))
    return ''.join(preserved)


def huffman(inputfile, outputfile):
    counts = count_chars(inputfile)
    tree = build_tree(counts)
    encoded_data = tree.encode_data(inputfile)

    with open(outputfile, 'wb') as f:
        f.write(pack_data(preserve_tree(tree)))
        f.write(pack_data(encoded_data))


if __name__ == '__main__':
    if len(sys.argv) == 3:
        huffman(sys.argv[1], sys.argv[2])
    else:
        print 'Usage:\nhuffman.py inputfile outputfile'
