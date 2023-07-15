# __init__.py
# Pizza library for Python 3.x
#   It is back compatible with original Pizza with more features
#   INRAE\olivier.vitrac@agroparistech.fr

# For the end-user:
#    1) add pizza/ to your PYTHONPATH
#    export PYTHONPATH="${PYTHONPATH}:/home/me/python/pizza"
#    2) in your Python code
#    import pizza *

# list of public classes: data, dump, raster, script, forcefield, struct, param

# $ last revision - 2023-07-12 $

# Revision history
# 2022-05-16 RC
# 2023-01-03 workaround to have raster working on Windows without restrictions
# 2023-07-12 add paramauto

# to test system (isPC)
from platform import system

# check system
def check_PIL():
    if system().startswith("darwin") or system().startswith("win"):
        try:
            from PIL import Image
            print("pizza.private.PIL.Image not compiled on Darwin or Windows\n\t>>try the default Pillow (installed v. %s)"
                  % Image.__version__)
        except ImportError:
            print("please add Pillow to your Python 3.x\n\t>> https://pillow.readthedocs.io/en/latest/installation.html")
        else:
            raise Exception("PIL is not compatible with Darwin or Windows systems")
    else:
        from pizza.private.PIL.Image import Image

# input data objects and methods
from pizza.data3 import data
# dump objects and methods
from pizza.dump3 import dump
# 2D sketching methods (3D pending)
from pizza.raster import raster,emulsion,coreshell
# script engine and methods
from pizza.script import *
# forcefield objects and derived classes
from pizza.forcefield import *
from pizza.generic import *
# script objects and derived classes
from pizza.script import *
# basic tools à la Matlab
# including a feature similar to MS/alias() from INRAE/MS Toolbox
from pizza.private.struct import struct,param,paramauto
# region objects and methods
from pizza.region import *
# Image
check_PIL()


# other libraries will be added there
from workshop0 import *
