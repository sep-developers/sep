import os
import re
import sys
from glob import glob

from setuptools import Extension, setup

# from setuptools import setup
from setuptools.dist import Distribution

# Detect if setup.py is being run with an argument that doesn't require
# building anything. (egg info, help commands, etc)
options = Distribution.display_option_names + ["help-commands", "help"]
is_non_build = (
    any("--" + opt in sys.argv for opt in options)
    or len(sys.argv) == 1
    or sys.argv[1] in ("egg_info", "clean", "help")
)

# extension module(s): only add if we actually need to build, because we need
# to import numpy and cython to build, and we'd rather non-build commands
# work when those dependencies are not installed.
if is_non_build:
    extensions = None
else:
    import numpy
    from Cython.Build import cythonize

    sourcefiles = ["sep_pjw.pyx"] + glob(os.path.join("src", "*.c"))
    headerfiles = glob(os.path.join("src", "*.h"))
    include_dirs = [numpy.get_include(), "src"]
    extensions = [
        Extension(
            "sep_pjw",
            sourcefiles,
            include_dirs=include_dirs,
            depends=headerfiles,
            define_macros=[("_USE_MATH_DEFINES", "1")],
        )
    ]
    extensions = cythonize(extensions)

setup(ext_modules=extensions)
