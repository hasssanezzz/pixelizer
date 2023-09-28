import numpy as np
import cv2

from ..constants import IMG_DIM

class Encoder:
    @staticmethod
    def unpack_bytes(chunk) -> list[bool]:
        bool_array = np.unpackbits(np.frombuffer(chunk, dtype=np.uint8))
        extra_bit = np.array([True], dtype=bool)
        return np.concatenate((bool_array, extra_bit))

    @staticmethod
    def reshape_bits(bits):
        sqr = IMG_DIM ** 2

        if len(bits) > sqr:
            raise ValueError(
                f'Big chunk, received: {len(bits)} bits, capability: {IMG_DIM ** 2} bits')

        to_pad = sqr - len(bits)
        padded = np.pad(bits, (0, to_pad), mode='constant')

        return np.reshape(padded, (IMG_DIM, IMG_DIM)).astype(np.uint8) * 255

    @staticmethod
    def make_img(image_data):
        return cv2.cvtColor(image_data, cv2.COLOR_GRAY2BGR)

    @staticmethod
    def encode_bytes_to_img(chunk):
        return Encoder.make_img(Encoder.reshape_bits(Encoder.unpack_bytes(chunk)))
