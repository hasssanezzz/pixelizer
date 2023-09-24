import os
from math import ceil
import cv2

from .coders.encoder import encode_chunk_to_img_array
from .coders.decoder import Decoder
from .constants import CHUNK_SIZE_B, IMG_DIM, FPS

class FSCoder:

    def __init__(self):
        pass

    def split_file(self, file_path: str):
        with open(file_path, 'rb') as file:
            chunk_counter = 0
            while True:
                chunk = file.read(CHUNK_SIZE_B)
                if not chunk:
                    break  # End of file
                chunk_counter += 1
                yield chunk, chunk_counter

    def chunks_to_images(self, file_path: str):
        file_size = os.path.getsize(file_path)
        print(f'Splitting and encoding {ceil(file_size/ CHUNK_SIZE_B)}')
        for chunk, chunk_index in self.split_file(file_path):
            print(f'Encoding chunk {chunk_index} size: {len(chunk) / 1024} KB')

            yield encode_chunk_to_img_array(chunk)

    def mp4_encode(self, file_path: str, out_mp4: str):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(
            out_mp4, fourcc, FPS, (IMG_DIM, IMG_DIM))

        i = 1
        for img_array in self.chunks_to_images(file_path):
            print(f'Writing frame {i} to video')
            i += 1
            video_writer.write(img_array)

        video_writer.release()

        return out_mp4

    def read_video_frames(self, in_mp4: str):
        video_reader = cv2.VideoCapture(in_mp4)
        frame_count = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(video_reader.get(cv2.CAP_PROP_FPS))

        print('Frame count', frame_count / fps)

        for idx in range(frame_count):
            if idx % fps == 0:
                success, frame = video_reader.read()
                if success:
                    yield frame

    def mp4_decode(self, in_mp4: str, out_file: str):
        with open(out_file, 'ab') as file:
            i = 1
            for frame in self.read_video_frames(in_mp4):
                print(f'Decoding frame {i}')
                i += 1
                d = Decoder()
                d.read_frame(frame)
                bytes_to_write = d.decode_binary_stream()
                file.write(bytes_to_write)

