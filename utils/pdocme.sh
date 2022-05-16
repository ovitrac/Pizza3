#!/usr/bin/env bash

# Generate documentation of main classes
# INRAE\olivier.vitrac@agroparistech.fr

# revision history 2022-05-16 $


export PYTHONPATH='/home/olivi/billy/python':'/home/olivi/billy/python/pizza':'/home/olivi/anaconda3/lib/python3.9':'/home/olivi/anaconda3/lib/python3.9/lib-dynload':'/home/olivi/anaconda3/lib/python3.9/site-packages':'/home/olivi/anaconda3/lib/python3.9/site-packages/locket-0.2.1-py3.9.egg':'/home/olivi/anaconda3/lib/python3.9/site-packages/IPython/extensions':'/home/olivi/.ipython'

mainfolder="./.."

pdoc -f --html -o $mainfolder/html/ $mainfolder/pizza/raster.py
pdoc -f --html -o $mainfolder/html/ $mainfolder/pizza/data3.py
pdoc -f --html -o $mainfolder/html/ $mainfolder/pizza/dump3.py
pdoc -f --html -o $mainfolder/html/ $mainfolder/pizza/forcefield.py
pdoc -f --html -o $mainfolder/html/ $mainfolder/pizza/generic.py
pdoc -f --html -o $mainfolder/html/ $mainfolder/pizza/private/struct.py
pdoc -f --html -o $mainfolder/html/ $mainfolder/pizza/private/PIL/Image.py
pdoc -f --html -o $mainfolder/html/ $mainfolder/pizza/__init__.py
pdoc -f --html -o $mainfolder/html/ $mainfolder/pizza/script.py
pdoc -f --html -o $mainfolder/html/ $mainfolder/workshop0.py
pdoc -f --html -o $mainfolder/html/ $mainfolder/workshop1.py
pdoc -f --html -o $mainfolder/html/ $mainfolder/geometry.py
pdoc -f --html -o $mainfolder/html/ $mainfolder/assembly.py
