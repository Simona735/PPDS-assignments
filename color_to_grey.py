"""
Copyright 2022 Simona Richterova.
Licensed to MIT https://spdx.org/licenses/MIT.html

This module converts a color image to black and white
using the GPU and the numba library.
"""


from numba import cuda
import numpy as np
import cv2
import math


@cuda.jit
def color_to_grey(color, grey):
    """
    Convert color image to grey using cuda.

    Args:
        color(numpy array): color image with 3 dimensions (RGB colors)
        grey(numpy array): resulting grey image with 2 dimensions
    """
    x, y = cuda.grid(2)
    x_max, y_max, _ = color.shape
    if x < x_max and y < y_max:
        colors_sum = color[x][y][0] + color[x][y][1] + color[x][y][2]
        grey[x][y] = colors_sum // 3


def main():
    print(cuda.gpus)


if __name__ == "__main__":
    main()
