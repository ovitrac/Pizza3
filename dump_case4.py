#!/usr/bin/env python3

# dump_case4.py
# Script to load and minpulate case 4 dump simulations

# INRAE\Olivier Vitrac, INRAE\William Jenkinson - rev. 2022/01/25
# contacts: olivier.vitrac@agroparistech.fr

# Minimum dependencies: os, sys, pizza, numpy

"""
The following file structure is assumed
    |--- host directory 
    |------------- dump_csae4.py
    |-------------  pizza\                      (mandatory)
    |-------------------------- dump3.py        (mandatory)

"""

# %% import dump from pizza.dump3
from pizza.dump3 import dump
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

# %% Tait Equation for this simulation (read the LAMMPS code)
c0 = 10
rho0 = 1000
gamma = 7
def Tait(rho):
    B = (c0**2) * rho0
    return B * ( (rho/rho0)**gamma -1 )

# %% load data
dmp = "data/play_data/dump.play.50frames"
X = dump(dmp)
# extract fields --> fields["id"] gives the column index of "id"
fields = X.names;
for k  in sorted(fields,key=fields.get,reverse=False):
    print("\t%02d: %s" % (fields[k],k) )
    
# %% overview of system definition from first frame
# type 1: bottom tooth bead
# type 2: top tooth bead
# type 3: shell bead
# type 4: core bead
# General syntax for aselect method
# X.aselect.test("$id > 100 and $type == 2")    select match atoms in all steps
# X.aselect.test("$id > 100 and $type == 2",N)  select matching atoms in one step

# select for type 4
#   17015 atoms of 34057 selected in first step 0
#   6419 atoms of 23391 selected in last step 130000
X.aselect.test("$type == 4")
X.write('tmp/case4core.dump')
typ1,typ2 = X.minmax("type") # for the selection ONLY (here type)
c_row1,c_row2 = X.minmax("c_rho") # for the selection ONLY (here type)

#   viz() returns info for selected atoms for specified timestep index
#     can also call as viz(time,1) and will find index of preceding snapshot
#     time = timestep value
#     box = \[xlo,ylo,zlo,xhi,yhi,zhi\]
#     atoms = id,type,x,y,z for each atom as 2d array
#     bonds = id,type,x1,y1,z1,x2,y2,z2,t1,t2 for each bond as 2d array
X.atype = "c_rho"
rawselection = X.viz(25)
xyzselection = np.array(rawselection[2])
rhoselection = xyzselection[:,1];
xyzselection = xyzselection[:,2:5]
plt.figure(); plt.axes(); plt.plot(xyzselection[:,0],xyzselection[:,1],'ro'); 
plt.figure(); plt.axes(); plt.hist(rhoselection)

# without slection
snap = X.snaps[0]
typ = snap.atoms[:,fields["type"]]
typu = np.unique(typ)

# %% extract the average pressure from all frames and plot them
times = X.time();
ntimes = len(times)
pavg = np.zeros(ntimes)
for iframe in range(0,ntimes):
    print("average frame %d of %d" % (iframe+1,ntimes) )
    rawselection = X.viz(iframe)
    xyzselection = np.array(rawselection[2])
    pavg[iframe] = np.average(Tait(xyzselection[:,1]));
    
plt.figure(); plt.axes(); plt.plot(times,pavg,'b-'); 
plt.savefig('tmp/corepressure_method1.pdf')
plt.savefig('tmp/corepressure_method1.png',dpi=300)

# %% alternative code using snap instead of viz
snap = X.snaps[25] # snap = X.snaps[-1] does the same
natoms = len(snap.atoms)
typ = snap.atoms[:,fields["type"]]
x = snap.atoms[typ==4,fields["x"]];
y = snap.atoms[typ==4,fields["y"]];
p4 = Tait(snap.atoms[typ==4,fields["c_rho"]]);
plt.figure(); plt.axes(); plt.hist(p4); plt.show()
