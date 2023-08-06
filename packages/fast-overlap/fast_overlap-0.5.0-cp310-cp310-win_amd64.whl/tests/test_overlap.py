# noqa: E402
import os
import sys

if os.environ.get("CI", False):
    # remove the local version from sys.path so that we use the version
    # we installed from the wheel
    sys.path = sys.path[1:]

from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pytest  # noqa: E402

import fast_overlap  # noqa: E402

ims = np.load(str(Path(__file__).parent / "test-ims.npy")).astype(np.int64)
expected = np.load(str(Path(__file__).parent / "expected-overlap.npy"))
shape = (int(np.max(ims[0]) + 1), int(np.max(ims[1]) + 1))


# test a few different types but not all
@pytest.mark.parametrize("type", [np.uint16, np.uint64, np.int32, np.int64])
def test_overlap(type):
    out = fast_overlap.overlap(ims[0].astype(type), ims[1].astype(type), shape)
    assert np.all(out == expected)


def test_overlap_no_shape():
    out = fast_overlap.overlap(ims[0], ims[1])
    assert np.all(out == expected)


def test_parallel_overlap():
    out = fast_overlap.overlap_parallel(
        ims[0].astype(np.int32), ims[1].astype(np.int32), shape
    )
    assert np.all(out == expected)
