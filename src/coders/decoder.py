import numpy as np


class Decoder:
    """
    The Decoder class provides methods for decoding binary data from images.

    Methods:
    --------
    flatten_img(img_arr: np.ndarray) -> np.ndarray:
        Flatten and threshold an image array.

    last_bit_index(bit_arr: np.ndarray) -> int:
        Find the index of the last '1' in a binary array.

    decode_bits(bit_arr: np.ndarray) -> bytes:
        Decode bits into bytes.

    decode_img(img_arr: np.ndarray) -> bytes:
        Decode binary data from an image array.
    """

    @staticmethod
    def flatten_img(img_arr: np.ndarray) -> np.ndarray:
        """
        Flatten and threshold an image array.

        Parameters:
        -----------
        img_arr : np.ndarray
            The input image array.

        Returns:
        --------
        np.ndarray
            The flattened and thresholded binary array.
        """
        flattened = np.ravel(np.mean(img_arr, axis=2))
        return np.vectorize(lambda x: x > 255 // 2)(flattened)

    @staticmethod
    def last_bit_index(bit_arr: np.ndarray) -> int:
        """
        Find the index of the last '1' in a binary array.

        Parameters:
        -----------
        bit_arr : np.ndarray
            The input binary array.

        Returns:
        --------
        int
            The index of the last '1'.
        """
        n = len(bit_arr)
        for i in range(n):
            idx = n - i - 1
            if bit_arr[idx]:
                return idx

    @staticmethod
    def decode_bits(bit_arr: np.ndarray) -> bytes:
        """
        Decode bits into bytes.

        Parameters:
        -----------
        bit_arr : np.ndarray
            The input binary array.

        Returns:
        --------
        bytes
            The decoded byte data.
        """
        last_one_index = Decoder.last_bit_index(bit_arr)
        bit_arr = bit_arr[:last_one_index]

        n = len(bit_arr)
        nearest = n + (8 - n % 8) if n % 8 else n
        bit_arr = np.concatenate((bit_arr, np.zeros(nearest - n)))
        return np.packbits(bit_arr.astype(bool), axis=-1).tobytes()

    @staticmethod
    def decode_img(img_arr: np.ndarray) -> bytes:
        """
        Decode binary data from an image array.

        Parameters:
        -----------
        img_arr : np.ndarray
            The input image array.

        Returns:
        --------
        bytes
            The decoded byte data.
        """
        bit_arr = Decoder.flatten_img(img_arr)
        return Decoder.decode_bits(bit_arr)
