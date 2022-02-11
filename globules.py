#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 10:44:13 2022

@author: INRAE\olivier.vitrac@agroparistech.fr
"""

# %% Example 3D
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

xmin, ymin, zmin = -1, -1, -1
xmax, ymax, zmax = 1, 1, 1


def globule(x=0,y=0,z=0,r=1,color='b'):
    global xmin, ymin, zmin, xmax, ymax, zmax
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    xs = x + r * np.outer(np.cos(u), np.sin(v))
    ys = y + r * np.outer(np.sin(u), np.sin(v))
    zs = z + r * np.outer(np.ones(np.size(u)), np.cos(v))
    xmin, ymin, zmin = min(xmin,min(xs.flatten())), min(ymin,min(ys.flatten())), min(zmin,min(zs.flatten()))
    xmax, ymax, zmax = max(xmax,max(xs.flatten())), max(ymax,max(ys.flatten())), max(zmin,max(zs.flatten()))
    # Plot the surface
    ax.plot_surface(xs, ys, zs, color=color)
 
def axistight():
    max_range = np.array([xmax-xmin, ymax-ymin, zmax-zmin]).max()
    Xbox = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(xmin+xmax)
    Ybox = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(ymin+ymax)
    Zbox = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(zmin+zmax)
    for xb, yb, zb in zip(Xbox, Ybox, Zbox):  ax.plot([xb], [yb], [zb], 'k')



# %%
fig = plt.figure()
ax = plt.axes(projection='3d')
rsmall = 20
rbig = 40
globule(x=-150,y=-100,z=0,r=rsmall,color='g')
globule(x=-100,y=-50,z=-10,r=rsmall,color='b')
globule(x=-50,y=-20,z=-10,r=rsmall,color='r')

globule(x=0,y=0,z=0,r=rbig,color='g')
globule(x=-120,y=80,z=-15,r=rbig,color='b')
globule(x=120,y=70,z=15,r=rbig,color='r')


globule(x=50,y=-50,z=0,r=rsmall,color='r')
globule(x=-50,y=50,z=-20,r=rsmall,color='b')
globule(x=25,y=70,z=-20,r=rsmall,color='b')

# Make data
axistight()
plt.show()