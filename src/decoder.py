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
        self.binary_stream = np.zeros(CHUNK_SIZE, dtype='b')
        