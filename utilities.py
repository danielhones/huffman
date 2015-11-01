BYTE_LENGTH = 8


# Had a problem getting this to work right, not sure why:
'''
def scan(string):
    """
    Return a generator that yields 'size' characters at a time from the string until the string is exhausted
    """
    index = 0
    sub_string = None
    while index < len(string):
        size = yield sub_string
        sub_string = string[index:index + size]
        index += size
'''


# So we'll do it a simple way instead
def scan(string):
    return (i for i in string)


def pack_data(data):
    """
    Data should be a string of 1's and 0's.  As it stands now, this function will produce some junk on the last byte if
    the length of data is not divisible by 8.  So it seems I need to add to the file a count of how many junk bits
    should be truncated when reading it back in for decompression.
    TODO: Find a way to deal with that junk data at the end
    """
    packed_data = []
    for i in range(0, len(data), 8):
        bit_string = data[i:i+8]
        next_char = chr(int(bit_string, 2))
        packed_data.append(next_char)
    return ''.join(packed_data)


def pad_to_full_byte(incomplete_byte, byte_length=BYTE_LENGTH):
    # Add leading 0's to make it a full 'byte' although byte_length can be specified to
    # something other than 8.
    full_byte = '0' * (byte_length - len(incomplete_byte)) + incomplete_byte
    return full_byte


def bit_string_for(char_or_num):
    if type(char_or_num) is str:
        return str(bin(ord(char_or_num)))[2:]
    elif type(char_or_num) in (int, float):
        return str(bin(char_or_num))[2:]


def get_next_byte(ch):
    next_byte = pad_to_full_byte(bit_string_for(ch))
    return next_byte


def unpack_data(data):
    binary_data = [get_next_byte(ch) for ch in data]
    bit_string = ''.join(binary_data)
    return bit_string
