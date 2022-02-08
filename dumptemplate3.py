#!/usr/bin/env python3

# dumptemplate3.py
# Generic script to test the new dump3.py (pizza for Python 3.x)
# load a dump file and plot it

# INRAE\Olivier Vitrac, INRAE\William Jenkinson - rev. 2022/02/03
# contacts: olivier.vitrac@agroparistech.fr

# Minimum dependencies: os, sys, time, pizza, numpy

"""
Note that this script works only in Python 3.x
The following file structure is assumed
    |--- host directory (on my PC, it is '/home/olivi/billy/python)
    |------------- this file (initially dumptemplate3.py)
    |-------------  pizza\                      (mandatory)
    |-------------------------- dump3.py        (mandatory)

    Do not forget chmod +x dumptemplate3.py to run it directly from bash

    Depending on the kind of simulation plot it in 2D or 3D
"""


# %% Dependencies
import time
import numpy as np
#from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from pizza.dump3 import dump


# %% Full example based on the last implementation of dump
# this very short code uses the new class frame
tic = time.time(); # timer
dmp = "data/play_data/dump.play.50frames"

X = dump(dmp)
print(X)

frame = X.frame(50) # extract the 50th frame (first=0)
frame.v = np.sqrt(frame.vx**2+frame.vy**2) # add a field
print(frame)

fig = plt.figure(); ax = plt.axes()
ax.scatter(frame.x,frame.y,c=frame.v,cmap="viridis")
plt.show()

toc1 = time.time() # first timer
print("elapsed time for loading and plotting data=%0.4f s"  % (toc1-tic))

# %% Easter : frame objects can be compared and sorted
f0 = X.frame(0)
f10 = X.frame(10)
f30 = X.frame(30)
flast = X.frame(-1) # use -1 for the last
fbeforethelast = X.frame(-2) # use -2 for for the last before the last
print("f0>f30?",f0>f30,"f10<=f30?",f10<=f30,sep="\n")
fselect = [f10,f30,flast,f0,fbeforethelast]
fselect.sort()
tselect = [fselect[k].time for k in range(len(fselect))]
print("the frames are now sorted correctly as:",tselect,sep="\n")

# %% OLD FASHION - basic code to extract dump properties (as print(X) does)
# preread data and display some information
# use fields["name"] to get the data matching one column
times = X.time();
ntimes = len(times)
lastime = times[-1];
fields = X.names;
print("dump file: %s\ncontains %d frames (tend=%d)\nwith fields" % (X.flist[0],ntimes,lastime) )
for k  in sorted(fields,key=fields.get,reverse=False):
    print("\t%02d: %s" % (fields[k],k) )

# %% OLD FASHION - snap: selection of the last frame and all atoms (other frames are discarded)
#X.aselect.all(lastime)
#X.tselect.one(lastime)
#X.delete()
snap = X.snaps[ntimes-1] # snap = X.snaps[-1] does the same
natoms = len(snap.atoms)
print("box %s \n\t%f %f \n\t%f %f \n\t%f %f" % (snap.boxstr, snap.xlo,snap.xhi, snap.ylo,snap.yhi, snap.zlo,snap.zhi))
print("number of atoms: %d" % (natoms))
toc1 = time.time() # first timer
print("elapsed time for loading data=%0.4f s"  % (toc1-tic))

# %% OLD FASHION -  post-treatment: plot all particles with a color matching the velocity module
plt.close('all')
fig = plt.figure()
#ax = plt.axes(projection='3d')
ax = plt.axes()
x = snap.atoms[:,fields["x"]];
y = snap.atoms[:,fields["y"]];
z = snap.atoms[:,fields["z"]];
vx = snap.atoms[:,fields["vx"]];
vy = snap.atoms[:,fields["vy"]];
vz = snap.atoms[:,fields["vz"]];
v = np.sqrt(vx**2+vy**2+vz**2)
#ax.scatter3D(x, y,z, c=v, cmap='viridis')
ax.scatter(x,y,c=v,cmap="viridis")
toc2 = time.time()
print("elapsed time for feeding the plot=%0.4f s"  % (toc2-toc1))
plt.show()

# end of the template
print("end of the template")

# %% Extra test (added OV on 2022-01-25)
# skip data, save them, reload them and plot them
X.tselect.all()
X.tselect.skip(5)
X.write('tmp/testOV.dump')
X1 = dump('tmp/testOV.dump')
snap0 = X1.snaps[0]     # first snap
snap1 = X1.snaps[-1]    # last snap
X1.tselect.test("$t >= 20000 and $t < 1000000")

plt.figure(); plt.axes()
plt.plot(X1.snaps[0].atoms[:,fields["x"]],
                X1.snaps[0].atoms[:,fields["y"]],
                'bo'); plt.show()
plt.plot(X1.snaps[-1].atoms[:,fields["x"]],
                X1.snaps[-1].atoms[:,fields["y"]],
                'rx'); plt.show()
# %% print figure
plt.savefig('tmp/testOV.pdf')
plt.savefig('tmp/testOV.png',dpi=300)