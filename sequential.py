"""
Copyright 2022 Simona Richterova.
Licensed to MIT https://spdx.org/licenses/MIT.html

This module converts 3 color images to black and white
using the GPU and the numba library. This version of the program 
demonstrates the operations in sequence in a single stream.
"""


from numba import cuda
import cv2
import math
from time import perf_counter


@cuda.jit
def color_to_grey(color):
    """
    Convert color image to grey using cuda.
    Args:
        color(numpy array): color image with 3 dimensions (RGB colors)
    """
    x, y = cuda.grid(2)
    x_max, y_max, _ = color.shape
    if x < x_max and y < y_max:
        colors_sum = color[x][y][0] + color[x][y][1] + color[x][y][2]
        color[x][y] = colors_sum // 3


def main():
    pass


if __name__ == "__main__":
    main()
