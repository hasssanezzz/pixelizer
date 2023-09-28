import os
import cv2
from math import ceil

from ..constants import CHUNK_SIZE_B, IMG_DIM, FPS
from ..coders.encoder import Encoder


class MP4_Encoder:
    encoded_chunks = []

    @staticmethod
    def split_file(file_path: str):
        with open(file_path, 'rb') as file:
            chunk_counter = 0
            while True:
                chunk = file.read(CHUNK_SIZE_B)
                if not chunk:
                    break
                chunk_counter += 1
                yield chunk_counter, chunk

    @staticmethod
    def encode_chunks_from_file(file_path: str):
        file_size = os.path.getsize(file_path)

        print(
            f'File of size {file_size // (1024 * 8)}KB will be splitted into {ceil(file_size / CHUNK_SIZE_B)}')

        for idx, chunk in MP4_Encoder.split_file(file_path):
            print(f'Encoding chunk {idx}')
            yield Encoder.encode_bytes_to_img(chunk)

    @staticmethod
    def to_mp4(file_path: str, out_mp4: str):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(
            out_mp4, fourcc, FPS, (IMG_DIM, IMG_DIM))

        i = 1
        for img_array in MP4_Encoder.encode_chunks_from_file(file_path):
            print(f'Writing frame {i} to video')
            video_writer.write(img_array)
            i += 1

        video_writer.release()

        return out_mp4


if __name__ == '__main__':
    MP4_Encoder.to_mp4('debug/in.mkv', 'touch.mp4')
