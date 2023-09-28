import numpy as np


class Decoder:
    
    @staticmethod
    def flatten_img(img_arr):
        flattened = np.ravel(np.mean(img_arr, axis=2))
        return np.vectorize(lambda x: x > 255 // 2)(flattened)

    @staticmethod
    def last_bit_index(bit_arr):
        n = len(bit_arr)
        for i in range(n):
            idx = n - i - 1
            if bit_arr[idx]:
                return idx

    @staticmethod
    def nearest_bigger_multiple_of_8(number):
        remainder = number % 8
        if remainder == 0:
            return number
        else:
            return number + (8 - remainder)

    @staticmethod
    def decode_bits(bit_arr):
        last_one_index = Decoder.last_bit_index(bit_arr)
        bit_arr = bit_arr[:last_one_index]

        n = len(bit_arr)
        nearest = Decoder.nearest_bigger_multiple_of_8(n)
        bit_arr = np.concatenate((bit_arr, np.zeros(nearest - n)))
        return np.packbits(bit_arr.astype(bool), axis=-1).tobytes()

    @staticmethod
    def decode_img(img_arr):
        bit_arr = Decoder.flatten_img(img_arr)
        return Decoder.decode_bits(bit_arr)
