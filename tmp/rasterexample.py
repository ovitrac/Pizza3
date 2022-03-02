#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 13:48:46 2022

@author: olivi
"""

from pizza.raster import raster
from workshop0 import *

# %% input geometry
S = raster(width=200,height=200) #domain

#geometries
top, bottom, solid, fluid = 1, 2, 3, 4
S.rectangle(0,200,0,200,name="edge",beadtype=top)
S.rectangle(10,190,10,190,name="pool",beadtype=fluid)
S.circle(100, 50, 20, name="floater",beadtype=bottom)
S.triangle(100,50,15,name="mask",ismask=True,)
S.hexagon(100, 150, 20,name="dingy",beadtype=solid)
S.plot()
S.show(extra="label",contour=False)


# create object data
X = S.data(scale=(0.1,0.1))

X.write("./swimmingpool.lmp")

# %% Lammps script

# Building LAMMPS script using script.py
init = initialization()
ld = load(local="$ .",file="$ swimmingpool.lmp")

groups = group(name="$ moving1",type=top) & \
         group(name="$ moving2",type=bottom) & \
         group(name="$ solid",type=solid) & \
         group(name="$ fluid",type=fluid) & \
         group(name="$ tlsph",type=solid) & \
         group(name="$ ulsph",type=fluid)
         
grav = gravity(g=9.81,vector=[0,1,0])

FF = interactions(top=top,bottom=bottom,solid=solid,fluid=fluid)

initthermo = thermo()

equilsteps = equilibration(mode="init",run=[1000,2000]) & \
               equilibration(mode="fast",limit_velocity=1000,run=1000) & \
               equilibration(mode="slow",limit_velocity=0.01,run=1000) & \
               equilibration(mode="fast",limit_velocity=1000,run=1000)


dmp = smddump(outstep=2000,outputfile=["dump.workshop0"])

moves = translation(velocity1 = [0,-1,0], velocity2 = [0,1,0],run=5000) & \
        translation(velocity1 = [0,-0.1,0], velocity2 = [0,0.1,0],run=2000) & \
        translation(force=[0,-1,0], velocity1 = [0,0,0], velocity2 = [0,0,0],run=21000) & \
        rampforce(ramp=(-1,-10), velocity1 = [0,0,0], velocity2 = [0,0,0],run=21000)


fullscript = init + ld + groups + grav + FF + initthermo + equilsteps + dmp + moves