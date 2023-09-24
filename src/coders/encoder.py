import numpy as np
from cv2 import imwrite

from ..constants import IMG_DIM


class Encoder:

    def __init__(self):
        pass

    def file_to_binary_string(self, file_path: str):
        rb = open(file_path, 'rb').read()
        return ''.join(format(byte, '08b') for byte in rb) + '1'

    def chunk_to_binary_string(self, chunk: bytes):
        return ''.join(format(byte, '08b') for byte in chunk) + '1'

    def encode_binary_string(slef, binary_string: str):
        chunk_2d = np.zeros((IMG_DIM, IMG_DIM), dtype='b')

        if len(binary_string) > IMG_DIM ** 2:
            raise ValueError(
                f'Big chunk, received: {len(binary_string)} bits, capability: {IMG_DIM ** 2} bits')

        column_index = 0
        for idx, bit in enumerate(binary_string):
            if idx != 0 and idx % IMG_DIM == 0:
                column_index += 1
            if bit == '1':
                chunk_2d[column_index, (idx + IMG_DIM) % IMG_DIM] = 1
                
        return chunk_2d

    def to_img_array(self, chunk_2d):
        arr = np.empty((IMG_DIM, IMG_DIM, 3), dtype=np.uint8)

        for col_index, col in enumerate(chunk_2d):
            for pixel_index, pixel in enumerate(col):
                value = 0 if pixel == 1 else 255
                arr[col_index, pixel_index, 0] = value
                arr[col_index, pixel_index, 1] = value
                arr[col_index, pixel_index, 2] = value

        return arr

    def write_image(self, binary_string, img_path):
        imwrite(img_path, self.to_img_array(self.encode_binary_string(binary_string)))


def encode(file_path: str, img_path: str):
    e = Encoder()
    binary_string = e.file_to_binary_string(file_path)
    e.write_image(binary_string, img_path)


def encode_chunk_to_img_array(chunk: bytes):
    e = Encoder()
    binary_string = e.chunk_to_binary_string(chunk)
    chunk_2d = e.encode_binary_string(binary_string)
    
    # return image array from bytes
    return e.to_img_array(chunk_2d)
