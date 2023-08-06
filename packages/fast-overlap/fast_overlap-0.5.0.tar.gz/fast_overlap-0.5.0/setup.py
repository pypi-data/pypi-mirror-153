import os

import numpy
from Cython.Build import cythonize
from setuptools import Extension, setup

# os.environ["CC"] = "C:/Program Files/LLCM/bin/clang-cl.exe"
# os.environ["CXX"] = "C:/Program Files/LLCM/bin/clang-cl.exe"
if os.name == "nt":
    compile_args = ["/fopenmp", "/Ox"]
    extra_link_args = []
else:
    compile_args = [
        "-fopenmp",
        "-O3",
    ]
    extra_link_args = ["-fopenmp"]
# if os.name == "darwin":
#     compile_args.append("-lomp")
setup(
    name="fast_overlap",
    use_scm_version={"write_to": "fast_overlap/_version.py"},
    ext_modules=cythonize(
        [
            Extension(
                "fast_overlap._engine",
                ["fast_overlap/fast_overlap.pyx"],
                include_dirs=[numpy.get_include()],
                extra_compile_args=compile_args,
                extra_link_args=extra_link_args,
            )
        ],
        language_level="3",
    ),
)
