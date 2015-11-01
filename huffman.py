from utilities import pack_data, pad_to_full_byte, bit_string_for
from collections import defaultdict
from bisect import bisect_left
import sys


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


def preserve_tree(node):
    # TODO: this could be a method on HuffmanTree, but I don't know if it should be
    preserved = []

    def _preserve(node=node):
        if node.is_leaf:
            preserved.append('1')
            preserved.append(pad_to_full_byte(bit_string_for(node.char)))
        else:
            preserved.append('0')
            _preserve(node.left_child)
            _preserve(node.right_child)

    _preserve()
    preserved = ''.join(preserved)
    encoded_tree_size = pad_to_full_byte(bit_string_for(len(preserved)), byte_length=16)
    print int(encoded_tree_size,2)
    return encoded_tree_size + preserved


def huffman(inputfile, outputfile):
    counts = count_chars(inputfile)
    tree = build_tree(counts)
    encoded_data = preserve_tree(tree) + tree.encode_data(inputfile)

    with open(outputfile, 'wb') as f:
        f.write(pack_data(encoded_data))


if __name__ == '__main__':
    if len(sys.argv) == 3:
        huffman(sys.argv[1], sys.argv[2])
    else:
        print 'Usage:\nhuffman.py inputfile outputfile'
