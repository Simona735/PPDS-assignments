"""
Copyright 2022 Simona Richterova.
Licensed to MIT https://spdx.org/licenses/MIT.html

This module converts a color image to black and white
using the GPU and the numba library.
"""


from numba import cuda


def main():
    print(cuda.gpus)


if __name__ == "__main__":
    main()
