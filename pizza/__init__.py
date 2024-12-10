# __init__.py
# Pizza library for Python 3.x
#   Backward compatible with the original Pizza with additional features
#   INRAE\olivier.vitrac@agroparistech.fr

# For the end-user:
#    1) Add pizza/ to your PYTHONPATH
#       export PYTHONPATH="${PYTHONPATH}:/home/me/python/pizza"
#    2) In your Python code, use:
#       import pizza.*

# List of public classes: data, dump, raster, script, forcefield, struct, param

# $ Last revision: 2024-12-08 $

# Revision history
# 2022-05-16: Initial Release Candidate (RC)
# 2023-01-03: Workaround for raster on Windows without restrictions
# 2023-07-12: Added paramauto
# 2023-04-14: Fixed issues for Python 3.11 on Windows
# 2024-10-11 add global flag
# 2024-12-08 add all pizza classes

import os
from platform import system
from warnings import warn

# Define a flag to check if initialization has already been done
if not globals().get('_PIZZA_INITIALIZED', False):
    print("\n"+" "*10+"*"*10)
    _PIZZA_INITIALIZED = True

    # Function to check PIL compatibility
    def check_PIL():
        system_name = system().lower()
        if system_name.startswith("darwin") or system_name.startswith("win"):
            try:
                from PIL import Image
                print(f"pizza.private.PIL.Image not compiled on {system_name.capitalize()}\n"
                      f"\t>> Using default Pillow (installed v. {Image.__version__})")
            except ImportError:
                print("Please install Pillow for Python 3.x\n\t>> https://pillow.readthedocs.io/en/latest/installation.html")
            else:
                print("\n -- [ Your installation of Pizza3 ]")
                print("\nYour installed PIL may not be fully compatible with pizza3 on Darwin and Windows systems.")
        else:
            from pizza.private.PIL.Image import Image

    # Check PIL compatibility once during initialization
    check_PIL()

    # Import data objects and methods
    from pizza.data3 import data

    # Import dump objects and methods
    from pizza.dump3 import dump

    # Import 2D sketching methods (3D support pending)
    from pizza.raster import raster, emulsion, coreshell

    # Import script engine and methods
    from pizza.script import *
    from pizza.dscript import *

    # Import forcefield objects and derived classes
    from pizza.forcefield import *
    from pizza.dforcefield import *
    from pizza.generic import *

    # Import struct and param utilities with Matlab-like features
    from pizza.private.mstruct import struct, param, paramauto

    # Import region and group objects and methods
    from pizza.region import *
    from pizza.group import *

    # Import additional libraries for the workshop
    from workshop0 import *

    print("Pizza library initialized successfully.")
else:
    print("Pizza library was already initialized. Skipping repeated initialization.")
print(" "*10+"*"*10)
