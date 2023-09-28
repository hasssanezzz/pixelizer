import cv2

from ..coders.decoder import Decoder


class MP4_Deocer:
    
    frames: int

    @staticmethod
    def read_video_frames(in_mp4: str):
        video_reader = cv2.VideoCapture(in_mp4)
        frame_count = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(video_reader.get(cv2.CAP_PROP_FPS))

        MP4_Deocer.frames = frame_count / fps
        print('[*] Frame count', MP4_Deocer.frames)

        for idx in range(frame_count):
            if idx % fps == 0:
                success, frame = video_reader.read()
                if success:
                    yield frame

    @staticmethod
    def mp4_decode(in_mp4: str, out_file: str):
        with open(out_file, 'ab') as file:
            i = 1
            for frame in MP4_Deocer.read_video_frames(in_mp4):
                print(f'Decoding frame {i}')
                i += 1
                file.write(Decoder.decode_img(frame))

if __name__ == '__main__':
    MP4_Deocer.mp4_decode(out_file='out.touch.mkv', in_mp4='touch.mp4')
