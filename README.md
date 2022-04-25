# @Simona735/PPDS-assignments - 09
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3102/)
[![License](https://img.shields.io/npm/l/@tandil/diffparse?color=%23007ec6)](https://github.com/Simona735/PPDS-assignments/blob/main/LICENSE)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-blue.svg)](https://conventionalcommits.org)

# About
Simple python application that converts a color image to black and white using the GPU and the numba library.

# Assignment

Write your own application that uses GPU and library numba.

# Solution
 
The purpose of the implemented application is to load an image, convert it to black and white using the GPU and display the converted image. For GPU operations we used the numba library and its methods as presented at the lecture. 

For demonstration purposes we have used an image from wikipedia - [Golden Retriever puppy](https://en.wikipedia.org/wiki/Puppy#/media/File:Golde33443.jpg).

**Input image**: 

![Golden Retriever puppy](dog.jpg?raw=true "Golden Retriever puppy")

**Output image**: 

The output will be displayed on screen but we have provided a peview.

![Grey image](grey.jpg?raw=true "Grey image")

The position of computed pixel is given by a numba method cuda.grid(2), then it is checked for boundaries of image and lastly the black and white value is computed. The conversion is done as an average of RGB values on a given pixel position. 

We have launech the kernel with threads_per_block = (16, 16) and blocks per grid are computed based on image size.

