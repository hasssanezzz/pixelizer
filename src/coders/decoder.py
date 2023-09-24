from cv2 import imread
import numpy as np

from ..constants import IMG_DIM


class Decoder:

    def __init__(self):
        pass

    def read_img_file(self, img_path: str):
        img = imread(img_path)
        width, height, _ = img.shape

        if width != IMG_DIM or height != IMG_DIM:
            raise ValueError('File shape doesn\'t match')

        self.img = img
        
    def read_frame(self, frame):
        self.img = frame

    def img_to_binary(self):
        # TODO need to be optimized
        binary_stream = np.zeros(IMG_DIM ** 2, dtype='b')
        idx = 0

        for col in self.img:
            for pixel in col:
                psum = sum(pixel)
                binary_stream[idx] = not (psum // 3 > 255 // 2)
                idx += 1
                
        return binary_stream

    def decode_binary_stream(self):
        binary_stream = self.img_to_binary()
        
        end_idx = -1

        # find the last 0 bit
        for i in range(IMG_DIM ** 2):
            if binary_stream[(IMG_DIM ** 2) - i - 1]:
                end_idx = (IMG_DIM ** 2) - i - 1
                break
        
        binary_stream = binary_stream[:end_idx]

        # TODO this is super slow and need to be optimized
        bit_chunks = [list(binary_stream[i:i+8]) for i in range(0, end_idx-1, 8)]
        bit_chunks_str = [''.join(str(i) for i in x) for x in bit_chunks]
        byte_sequence = bytes(int(chunk, 2) for chunk in bit_chunks_str)
        
        return byte_sequence

    def write_bytes(self, output_path: str):
        open(output_path, 'wb').write(self.decode_binary_stream())

def decode(img_path: str, output_path: str):
    d = Decoder()
    d.read_img_file(img_path)
    d.img_to_binary()
    d.write_bytes(output_path)