"""
Copyright 2022 Simona Richterova.
Licensed to MIT https://spdx.org/licenses/MIT.html

This module converts 3 color images to black and white
using the GPU and the numba library. In addition, the program
is optimised with the use of multiple streams.
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


def load_images_preset():
    """
    Load predefined set of images as numpy array each.

    Returns:
        list: list of images
    """
    images = [cv2.imread("dog.jpg"),
              cv2.imread("cat.jpg"),
              cv2.imread("kittens.jpg")]
    return images


def main():
    data = load_images_preset()
    data_gpu = []
    gpu_out = []
    streams = []

    for k in range(len(data)):
        streams.append(cuda.stream())

    time_start = perf_counter()

    for k in range(len(data)):
        data_gpu.append(cuda.to_device(data[k], stream=streams[k]))

    for k in range(len(data)):
        threads_per_block = (32, 32)
        blocks_per_grid_x = math.ceil(data[k].shape[0] / threads_per_block[0])
        blocks_per_grid_y = math.ceil(data[k].shape[1] / threads_per_block[1])
        blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)
        color_to_grey[blocks_per_grid, threads_per_block, streams[k]](data_gpu[k])

    for k in range(len(data)):
        gpu_out.append(data_gpu[k].copy_to_host(stream=streams[k]))

    time_end = perf_counter()

    print(f'Total time: {time_end - time_start:.2f} seconds')


if __name__ == "__main__":
    main()
