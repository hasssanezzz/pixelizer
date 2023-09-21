from cv2 import imread
import numpy as np

from .constants import CHUNK_SIZE


class Decoder:

    def __init__(self, img_path: str, output_path: str):
        self.img_path = img_path
        self.output_path = output_path

        self.read_img()

    def read_img(self):
        img = imread(self.img_path)
        width, height, _ = img.shape

        if width != CHUNK_SIZE or height != CHUNK_SIZE:
            raise ValueError('File shape doesn\'t match')

        self.img = img

    def img_to_binary(self):
        self.binary_stream = np.zeros(CHUNK_SIZE ** 2, dtype='b')
        idx = 0

        for col in self.img:
            for pixel in col:
                psum = sum(pixel)
                self.binary_stream[idx] = not (psum // 3 > 255 // 2)
                idx += 1

    def decode_binary_stream(self):
        end_idx = -1

        # find the last 0 bit
        for i in range(CHUNK_SIZE ** 2):
            if self.binary_stream[(CHUNK_SIZE ** 2) - i - 1]:
                end_idx = (CHUNK_SIZE ** 2) - i - 1
                break
        
        self.binary_stream = self.binary_stream[:end_idx]

        # TODO this is super slow and need to be optimized
        bit_chunks = [list(self.binary_stream[i:i+8]) for i in range(0, end_idx-1, 8)]
        bit_chunks_str = [''.join(str(i) for i in x) for x in bit_chunks]
        byte_sequence = bytes(int(chunk, 2) for chunk in bit_chunks_str)
        
        return byte_sequence

    def write_bytes(self):
        open(self.output_path, 'wb').write(self.decode_binary_stream())

def decode(img_path: str, output_path: str):
    d = Decoder(img_path, output_path)
    d.read_img()
    d.img_to_binary()
    d.write_bytes()