#!/usr/bin/env python3

# datatemplate.py
# Generic script template to use pizza.data without any environment
# load a data file and plot it

# INRAE\Olivier Vitrac, INRAE\William Jenkinson - rev. 2022/02/04
# contacts: olivier.vitrac@agroparistech.fr

# Minimum dependencies: os, sys, numpy, pizza, numpy

"""
Note that this script works only in Python 2.7 (pizza issues)
The following file structure is assumed
    |--- host directory (on my PC, it is '/home/olivi/billy/python)
    |------------- this file
    |-------------  pizza\                          (mandatory)
    |-------------------------- data3.py            (mandatory)
"""

# %% Dependences
import numpy as np
import matplotlib.pyplot as plt
from pizza.data3 import data

# %% load data file
# data file
datafile = "./data/play_data/data.play.lmp"
X = data(datafile)
print(X)

# %% input file operation
# columns can be reordered and modified
# note that the column are numbered from 1 to the number of columns
X.dispsection("Atoms")
typ = X.get("Atoms",2)
X.append("Atoms",6) # append a column of 6
X.append("Atoms",9) # append a column of 9
X.append("Atoms",8) # append a column of 8
X.append("Atoms",7) # append a column of 7
X.replace("Atoms",6,typ) # replace the column 7 with typ
X.reorder("Atoms",1,2,4,3,5,6,9,8,7) # swap the x nd y axis, reorder the three lasts
X.write("tmp/data.modified.lmp")

Xtst = data("tmp/data.modified.lmp") # check that the new file can be read

# %% plot 3D with equal axis
fig = plt.figure()
ax = plt.axes(projection='3d')
x = X.get("Atoms",3)
y = X.get("Atoms",4)
z = X.get("Atoms",5)
ax.scatter3D(x, y, z);
# Create cubic bounding box to simulate equal aspect ratio
xmin = min(x); ymin=min(y); zmin=min(z);
xmax = max(x); ymax=max(y); zmax=max(z);
max_range = np.array([xmax-xmin, ymax-ymin, zmax-zmin]).max()
Xbox = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(xmin+xmax)
Ybox = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(ymin+ymax)
Zbox = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(zmin+zmax)
for xb, yb, zb in zip(Xbox, Ybox, Zbox):  ax.plot([xb], [yb], [zb], 'k')
ax.view_init(90,-90)
plt.show()
plt.title(X.flist[0])


# %% plot 2D
fig = plt.figure()
ax = plt.axes()
x = X.get("Atoms",3)
y = X.get("Atoms",4)
plt.plot(x,y,'bo',markersize=3)
plt.axis("equal")
plt.title(X.flist[0])
plt.show()

