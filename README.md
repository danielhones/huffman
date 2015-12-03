# Huffman Coding
A little implementation of Huffman coding that I wrote for fun and as an exercise.  Needs Python 2.x.  There is still a tiny problem where it will sometimes add on a few junk bits to the end of the compressed file, depending on how the length of the encoding works out.

## Usage
To compress:<br>
`python huffman.py input_file compressed_file`

To decompress:<br>
`python dehuffman.py compressed_file output_file`
