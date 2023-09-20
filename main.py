import argparse

from src.encoder import encode

def main(file_path: str, out_file: str):
    encode(file_path, out_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--i', dest="inp", type=str, help='Provide input file', required=True)
    parser.add_argument('-o', '--o', dest="out", type=str, help='Provide output file', required=True)
    
    args = parser.parse_args()
    
    main(args.inp, args.out)