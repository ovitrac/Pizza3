#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 13:48:46 2022

@author: billy
"""

# Revision hisotry
# 2022-04-01 add maxtype=4 for raster data outputs

from pizza.raster import raster

# %% input geometry
wdir = "./tmp"
S = raster(width=100,height=100) #domain
O = raster(width=100,height=100) #domain
#geometries
rigid, fluid, oscillating, solid, solid2= 1, 2, 3, 4, 5
S.rectangle(0,100,0,100,name="edge",beadtype=rigid)
S.rectangle(5,95,5,95,name="pool",beadtype=fluid)
S.circle(50, 25, 10, name="mask0",ismask=True)
S.hexagon(50, 75, 10,name="mask1",ismask=True)
O.circle(50, 25, 10, name="floater",beadtype=oscillating)
O.triangle(50,25,7,name="mask2",ismask=True)
O.hexagon(50, 75, 10,name="dingy",beadtype=solid)
O.mass = 2000
#S.hexagon(50, 150, 20,name="dingy2",beadtype=solid2)

S.plot()
O.plot()
S.show(extra="label",contour=False)
O.show(extra="label",contour=False)

# create object data
num_type0 = max(S.count())[0]
num_type1 = max(O.count())[0]
X = S.data(scale=(0.001,0.001),maxtype=4)
Y = O.data(scale=(0.001,0.001),maxtype=4)

destination0 = "%s/raster_%d_types.lmp" % (wdir,num_type0)
destination1 = "%s/raster_%d_types.lmp" % (wdir,num_type1)
X.write(destination0)
Y.write(destination1)