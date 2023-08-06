# Fast Overlap

A tiny cython library to calculate the pairwise overlap of all cell
masks between two time points. Created for use in https://github.com/Hekstra-Lab/microutil/

## Install

```
pip install fast-overlap
```


## Development

### Installation
```
python setup.py build_ext -i
```

To really remove stuff and build + test:
```
rm *.so build/ fast_overlap.cpp -rf && python setup.py build_ext -i && python test_speedup.py
```


### On Mac
You need to compile python extensions with the same compiler used to compile python. So on mac you should use `clang`. However the apple distributed clang doesn't include openmp so you should either use g++ locally (which seems to work for some reason, but doesn't for built wheels) or use homebrew clang as in the github workflows.
