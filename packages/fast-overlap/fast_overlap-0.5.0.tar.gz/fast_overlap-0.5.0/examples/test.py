import numpy as np
from skimage.draw import random_shapes
from skimage.segmentation import relabel_sequential

from fast_overlap import overlap, overlap_parallel

im_shape = (1024, 1024)
min_shapes = 5
im1 = random_shapes(im_shape, 20, min_shapes=min_shapes, random_seed=0)[0]
im1 = relabel_sequential(im1.sum(axis=-1))[0]
im2 = random_shapes(im_shape, 20, min_shapes=min_shapes, random_seed=1995)[0]
im2 = relabel_sequential(im2.sum(axis=-1))[0]
shape = (int(np.max(im1) + 1), int(np.max(im2) + 1))
out = overlap_parallel(im1.astype(np.int32), im2.astype(np.int32), shape)
print(out.sum())
# out_serial = overlap(im1.astype(np.int32), im2.astype(np.int32), shape)
out_serial = overlap(im1.astype(np.uint16), im2.astype(np.uint16), shape)

# from IPython import embed
# embed(colors="Linux")
assert np.all(out == out_serial)
