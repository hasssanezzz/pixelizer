# Pixelizer (POC)

This repository contains a Python script that allows you to encode any kind of file into a series of black and white images representing the file's bits. It also provides functionality to decode these images back into the original data.

## Introduction


The Pixelizer provides a way to transform the binary data of a file by converting the bits into black and white pixels. The resulting sequence of images can then be converted into a video file.

Furthermore, the script also allows you to decode a video file back into the original data, reconstructing the bits from the black and white images.

## Installation


1. Clone this repository to your local machine:
```bash
$ git clone https://github.com/hasssanezzz/pixelizer
```
2. Navigate into the cloned directory:
```bash
$ cd pixelizer
```
3. Install the required dependencies. You can use pip to install them automatically:
```bash
$ pip install -r requirements.txt
```

## Usage

To encode a file, provide the input file path and the desired output file path. The script will convert the file's bits into a series of black and white images and save them as a video file.

```bash
python3 pixelizer.py -i '<your_file>' -o  '<generated_mp4>'
```

Example:
```bash
python3 pixelizer.py -i data.txt -o output_video.mp4
```

To decode a video file, provide the `-d` flag, the path of the video file, and the desired output file path. The script will extract the black and white images from the video and decode them back into the original data.

```bash
python3 pixelizer.py -d -i '<mp4_file_path>' -o  '<decoded_file>'
```

Example:
```bash
python3 pixelizer.py -i video.mp4 -o data.txt
```

## Contributing

Contributions are welcome! If you'd like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b my-feature`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin my-feature`.
5. Submit a pull request.
