import numpy as np
from cv2 import imwrite

from .constants import CHUNK_SIZE

class Encoder:
    
    CHUNK_SIZE = CHUNK_SIZE
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        
    def read_file(self):
        rb = open(self.file_path, 'rb').read()        
        self.binary_string = ''.join(format(byte, '08b') for byte in rb) + '1'

    def chunkize(self):
        self.chunk_2d = np.zeros((self.CHUNK_SIZE, self.CHUNK_SIZE), dtype='b')
        
        if len(self.binary_string) > self.CHUNK_SIZE ** 2:
            raise ValueError('Big chunk')
        
        column_index = 0
        for idx, bit in enumerate(self.binary_string):
            if idx != 0 and idx % self.CHUNK_SIZE == 0:
                column_index += 1
            if bit == '1':
                self.chunk_2d[column_index, (idx + self.CHUNK_SIZE) % self.CHUNK_SIZE] = 1
            
    def chunk_to_img_array(self):
        arr = np.empty((self.CHUNK_SIZE, self.CHUNK_SIZE, 3), dtype=np.uint8)
        
        for col_index, col in enumerate(self.chunk_2d):
            for pixel_index, pixel in enumerate(col):
                value = 0 if pixel == 1 else 255
                arr[col_index, pixel_index, 0] = value
                arr[col_index, pixel_index, 1] = value
                arr[col_index, pixel_index, 2] = value
                
        return arr
    
    def write_image(self, img_path):
        imwrite(img_path, self.chunk_to_img_array())
        
def encode(file_path: str, img_path):
    e = Encoder(file_path)
    e.read_file()
    e.chunkize()
    e.write_image(img_path)