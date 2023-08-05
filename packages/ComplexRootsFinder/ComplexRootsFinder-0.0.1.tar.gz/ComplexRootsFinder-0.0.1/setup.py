import sys, os

from pybind11 import get_cmake_dir
# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

__version__ = "0.0.1"

# The main interface is through Pybind11Extension.
# * You can add cxx_std=11/14/17, and then build_ext can be removed.
# * You can set include_pybind11=false to add the include directory yourself,
#   say from a submodule.
#
# Note:
#   Sort input source files if you glob sources to ensure bit-for-bit
#   reproducible builds (https://github.com/pybind/python_example/pull/53)

# These are my includes...
# note that /clib/include only exists after calling clib_install.sh
cwd = os.path.dirname(os.path.abspath(__file__))
include_dirs = [
    cwd,
    cwd + '/src',
    cwd + '/src/fparser',
]

ext_modules = [
    Pybind11Extension("ComplexRootsFinder",
        ["src/main.cpp", "src/fparser/fparser.cc", "src/fparser/fpoptimizer.cc"],
        include_dirs=include_dirs,
        # Example: passing in the version to the compiled code
        define_macros = [('VERSION_INFO', __version__)],
        cxx_std=17
        ),
]

setup(
    name="ComplexRootsFinder",
    version=__version__,
    author="Andrey Kuzmin, Ladygin Stanislav, Karachurin Raul",
    author_email="ankuzme@yandex.ru",
    url="https://github.com/ut0xxia",
    description="Cross-platform Python wrapper for ComplexRootsFinder С++ library. Developed at MEPhI in 2022.",
    long_description="",
    ext_modules=ext_modules,
    extras_require={"test": "pytest"},
    # Currently, build_ext only provides an optional "highest supported C++
    # level" feature, but in the future it may provide more features.
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.6",
    install_requires=[
        'pybind11',
    ],
)
