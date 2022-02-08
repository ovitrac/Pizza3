#!/usr/bin/env python

# dumptemplate.py
# Generic script template to use pizza.dump without any environment
# load a dump file and plot it

# INRAE\Olivier Vitrac, INRAE\William Jenkinson - rev. 2022/01/16
# contacts: olivier.vitrac@agroparistech.fr

# Minimum dependencies: os, sys, time, pizza, numpy

"""
Note that this script works only in Python 2.7 (pizza issues)
The following file structure is assumed
    |--- host directory (on my PC, it is '/home/olivi/billy/python)
    |------------- this file (initially dumptemplate.py)
    |-------------  pizza\                          (mandatory)
    |-------------------------- dump.py        (mandatory)

    Do not forget chmod +x dumptemplate.py to run it directly from bash

    Comments: Development with eric6 (confortable), bpython (funny)
"""

# retrieve path and add it if needed
# the location of this file is used as working directory
import os,  sys,  time
try:
    pwd = os.path.dirname(os.path.abspath(__file__))
except NameError:
    pwd = os.getcwd() # os.chdir('/home/olivi/billy/python')
# modify path (PYTHONPATH) if neded
try:
    sys.path.index(pwd)
except ValueError:
    sys.path.append(pwd) # sys.path.insert(0, pwd)
# print current path
print("working directory: "+pwd)

"""
    main script
"""
# timer
tic = time.time();
# data file
dmp = "/home/olivi/billy/production_backextrusion/dump.backextrusion_v3_less"

# preread data and display some information
# use fields["name"] to get the data matching one column
from pizza.dump import dump
X = dump(dmp)
times = X.time();
ntimes = len(times)
lastime = times[-1];
fields = X.names;
print("dump file: %s\ncontains %d frames (tend=%d)\nwith fields" % (X.flist[0],ntimes,lastime) )
for k  in sorted(fields,key=fields.get,reverse=False):
    print("\t%02d: %s" % (fields[k],k) )

# snap: selection of the last frame and all atoms (other frames are discarded)
#X.aselect.all(lastime)
#X.tselect.one(lastime)
#X.delete()
snap = X.snaps[ntimes-1];
natoms = len(snap.atoms)
print("box %s \n\t%f %f \n\t%f %f \n\t%f %f" % (snap.boxstr, snap.xlo,snap.xhi, snap.ylo,snap.yhi, snap.zlo,snap.zhi))
print("number of atoms: %d" % (natoms))
toc1 = time.time() # first timer
print("elapsed time for loading data=%0.4f s"  % (toc1-tic))

# post-treatment: plot all particles with a color matching the velocity module
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
fig = plt.figure()
ax = plt.axes(projection='3d')
x = snap.atoms[:,fields["x"]];
y = snap.atoms[:,fields["y"]];
z = snap.atoms[:,fields["z"]];
vx = snap.atoms[:,fields["vx"]];
vy = snap.atoms[:,fields["vy"]];
vz = snap.atoms[:,fields["vz"]];
v = np.sqrt(vx**2+vy**2+vz**2)
ax.scatter3D(x, y,z, c=v, cmap='viridis');
toc2 = time.time()
print("elapsed time for feeding the plot=%0.4f s"  % (toc2-toc1))
plt.show()

# end of the template
print("end of the template")
