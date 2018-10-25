#!/usr/bin/env python
""" pygama setup script.
run from containing folder with:
$ pip install -e pygama
re-runs cythonize function on a list of extensions.
"""
from setuptools import setup, Extension, find_packages
import sys, os

do_cython = False
try:
    from Cython.Build import cythonize
    do_cython = True
except ImportError:
    do_cython = False

if __name__ == "__main__":

    try:
        import numpy as np
        include_dirs = [np.get_include(),]
    except ImportError:
        do_cython = False

    src = []
    fext = ".pyx" if do_cython else ".c"
    exts = [
        Extension(
            "pygama.processing.tier0",
            sources=[os.path.join("pygama", "processing", "tier0" + fext)],
            language="c",
            include_dirs=include_dirs),
    #     Extension(
    #         "pygama.processing._tier1",
    #         sources=[os.path.join("pygama", "processing", "tier1" + fext)],
    #         language="c",
    #         include_dirs=include_dirs),
    #     Extension(
    #         "pygama.processing.transforms",
    #         sources=[os.path.join("pygama", "processing", "transforms" + fext)],
    #         language="c"),
    #     Extension(
    #         "pygama.processing.calculators",
    #         sources=[
    #             os.path.join("pygama", "processing", "calculators" + fext)
    #         ],
    #         language="c")
    ]
    if do_cython:
        exts = cythonize(exts)
    # exts = []

    setup(
        name="pygama",
        version="0.1.0",
        author="Ben Shanks",
        author_email="benjamin.shanks@gmail.com",
        packages=find_packages(),
        ext_modules=exts,
        install_requires=[
            "numpy", "scipy", "pandas", "tables", "future", "cython"
        ])