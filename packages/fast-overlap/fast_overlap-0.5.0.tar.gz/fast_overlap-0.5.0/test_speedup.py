from timeit import timeit

setup = """
from fast_overlap import overlap_parallel, overlap

from skimage.draw import random_shapes
from skimage.segmentation import relabel_sequential
import numpy as np

im_shape=(1024,1024)
min_shapes = 5
im1 =random_shapes(im_shape, 20, min_shapes=min_shapes, random_seed=0)[0]
im1 = relabel_sequential(im1.sum(axis=-1))[0]
im2 =random_shapes(im_shape, 20, min_shapes=min_shapes, random_seed=1995)[0]
im2 = relabel_sequential(im2.sum(axis=-1))[0]
shape = (int(np.max(im1)+1), int(np.max(im2)+1))

from numba import int32, jit

@jit((int32[:,:], int32[:,:], int32, int32), nopython=True)
def overlap_numba(prev, curr, shape1, shape2):
    arr = np.zeros((shape1, shape2), dtype=np.dtype("i"))
    for i in range(prev.shape[0]):
        for j in range(prev.shape[1]):
            arr[prev[i,j],curr[i,j]] += 1
    return arr
"""

# import matplotlib.pyplot as plt
# fig, axs = plt.subplots(1,2)
# axs[0].imshow(im1)
# axs[1].imshow(im2)
# plt.show()
times = {}
times["serial_cpp"] = timeit(
    "overlap(im1.astype(np.int32), im2.astype(np.int32), shape)", setup=setup, number=10
)
times["parallel_cpp"] = timeit(
    "overlap_parallel(im1.astype(np.int32), im2.astype(np.int32), shape)",
    setup=setup,
    number=10,
)
times["serial_numba"] = timeit(
    "overlap_numba(im1.astype(np.int32), im2.astype(np.int32), *shape)",
    setup=setup,
    number=10,
)
print(times)
