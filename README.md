# @Simona735/PPDS-assignments - 10
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3102/)
[![License](https://img.shields.io/npm/l/@tandil/diffparse?color=%23007ec6)](https://github.com/Simona735/PPDS-assignments/blob/main/LICENSE)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-blue.svg)](https://conventionalcommits.org)

# About
Simple python application that converts a color image to black and white using the GPU and the numba library. In this branch 3 versions of the program are introduced, a sequential one, one with the use of streams and a third one with the use of both streams and events. 

# Assignment

Modify last week's program to 1) make optimal use of the equipment and 2) use streams as part of the solution. Use events to time the calculations. Produce supporting documentation: what problem you solved, how you looked for optimal computation parameters (use of profilers, GPU occupancy calculator, dynamic device occupancy detection using API), what speedup you achieved, and what guaranteed it.

# Solution

The solution followed the steps from the lecture (sequential -> streams -> streams and events). Each version of file has it's own dedicated file.

Firstly, we modified the version from branch 09 by using 3 images instead of one.

Sources:
- [Golden Retriever puppy](https://en.wikipedia.org/wiki/Puppy#/media/File:Golde33443.jpg)
- [Cat](https://en.wikipedia.org/wiki/File:Felis_silvestris_catus_lying_on_rice_straw.jpg)
- [Kittens](https://en.wikipedia.org/wiki/File:Kitten_Sibling_Pair.jpg)

The purpose of the implemented application remains the same as in branch 09. That is to load an images, convert it to black and white using the GPU. For GPU operations we used the numba library and its methods as presented at the lecture. 

For future reference, I have an NVIDIA GeForce RTX 2070 Max-Q graphics card. This graphics card is based on the Turing architecture, i.e. version 7.5.

## Sequential 

In this part of the assignment we did not modify the functionality of the code itself, but we focused on its optimization. The goal was to check the existing code and optimize it to use the device at 100%.

As mentioned in previous documentation, we have used threads_per_block = (16, 16). Maximum number of threads per block for all versions of graphics cards is 1024. So we have modified the parameter to (32, 32).

## Streams

In the second modification of the program we have added streams. We created one stream for each image. Thus the streams will be independent of each other, so no manual synchronization is needed between them. This action will speed up the program. 

Another optimization step that we have done is that we have added correct data transfer between the device and the host and vice versa. 

**Preview:**

```python
for k in range(len(data)):
    streams.append(cuda.stream())

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
```

The order of operations is such that first we create a stream for each image, then we transfer the data (images) to the device and assign a stream to each image. Based on the image, we calculate blocks per grid and start the kernel execution. When finished, copy the data back to the host. 

## Streams and events

In the third version of the program we have created two events for each stream, which in our case are used to find the time difference between them. 

# Results

Let's take a look at the resulting execution times of the programs.

**Sequential:**
Total time: 2.74 seconds

**Streams:**
Total time: 0.32 seconds

We can see major improvement here.

**Streams and events:**
Total time: 0.32 seconds
Mean kernel duration (milliseconds): 100.315591
Mean kernel standard deviation (milliseconds): 128.678776

In total time there is no improvement as there was no made from second version. 

We have also used the CUDA Occupancy Calculator excel sheet. The result was that the occupancy is 100%. This was decided on the basis of the number of threads per block. 

