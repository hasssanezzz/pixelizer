#!/usr/bin/python3

import argparse

from src import FSCoder

def main(file_path: str, out_file: str, decode_mode: bool):
    f = FSCoder()
    
    if decode_mode:
        f.mp4_decode(file_path, out_file)
    else:
        f.mp4_encode(file_path, out_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--decode', dest='decode', type=bool, help='Decode mode', default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument('-i', '--i', dest="inp", type=str, help='Provide input file', required=True)
    parser.add_argument('-o', '--o', dest="out", type=str, help='Provide output file', required=True)
    
    args = parser.parse_args()
    
    main(args.inp, args.out, args.decode)