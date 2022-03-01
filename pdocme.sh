# Generate documentation of main classes
# INRAE\olivier.vitrac@agroparistech.fr

# revision history 2022-03-01 $


export PYTHONPATH='/home/olivi/billy/python':'/home/olivi/billy/python/pizza':'/home/olivi/anaconda3/lib/python3.9':'/home/olivi/anaconda3/lib/python3.9/lib-dynload':'/home/olivi/anaconda3/lib/python3.9/site-packages':'/home/olivi/anaconda3/lib/python3.9/site-packages/locket-0.2.1-py3.9.egg':'/home/olivi/anaconda3/lib/python3.9/site-packages/IPython/extensions':'/home/olivi/.ipython'

pdoc -f --html -o ./html/ ./pizza/raster.py
pdoc -f --html -o ./html/ ./pizza/data3.py
pdoc -f --html -o ./html/ ./pizza/dump3.py
pdoc -f --html -o ./html/ ./pizza/forcefield.py
pdoc -f --html -o ./html/ ./pizza/private/struct.py
pdoc -f --html -o ./html/ ./pizza/__init__.py
pdoc -f --html -o ./html/ ./pizza/script.py
pdoc -f --html -o ./html/ ./workshop0.py
