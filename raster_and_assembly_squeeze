#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 13:48:46 2022

@author: billy, pei
"""
# Revision hisotry
# 2022-04-01 add maxtype=4 for raster data outputs
# 2022-04-13 change density of S (continuous phase) to 1000 from 1
# 2022-04-20 BRANCH Pei Sun initial branch of geometry.py used in workshop1
#               and being adapted into a visco(si)meter
# 2022-04-21 WJ - Basic viscosimeter design template
# 2022-04-28 BRANCH WJ - modified to be compatible with viscosimeter
# 2022-05-02 BRANCH WJ - modified for the numerical experiments: reference shear with sweep of vwall values
# 2022-05-05 organised ahead of productions

import os, importlib
from pizza.raster import raster
from workshop2 import *


root = os.path.dirname(importlib.util.find_spec("workshop2").origin)
wdir = os.path.join(root,"Production/") # wdir = $root/Production/
#fullfile = $root/Production/$filename
fullfile = lambda filename: os.path.join(root,filename) #related to the Final assempbly

# %% Parameters
# raster parameters
# simulation geometry
Sensor_w = 20
Substance_w = 10
Top_w = 10
Sensor_h = 1
Substance_h = 1
Top_h = 1
res = 20  #number of particles lined up between sensor and plate

# particle-wise parameters (size, scaling, mass)
mm = 1E-3   #Convert units to millimeters
scale_factor = Substance_h*mm/res
rho = 1000

# simulation-wise parameters
k_radius = 2*scale_factor
contact_stiffness = 1e9# contact stiffness between two different species
Y_modulus = 2000     # Youngs modulus for solids
rho0= 999          # reference density (rho0<rho, system initiate in compressed state)
nu  = 1E-6
c0 = 0.1            # speed of sound
q1 = 8*nu/(c0*k_radius)           # coefficient of artifical viscosity
sigma_yield = 0.1*Y_modulus     # yield stress
timestep = k_radius**2/(8*nu)

neigh_search = k_radius # ~2 times particle the particle size

# external forces/actuations
v_plate = -0.0001

# %% Raster files names
output_destination = "squeeze_apparatus" # e.g. "visco_h_hertzbc"
output_name = "squeeze_salted_resolution_%s" %(format(res)) # e.g. "h_%s" % (format(h))

# %% Create Rasters
# create raster objects
SEN = raster(name="sensor", width=max(Sensor_w*res, Substance_w*res, Top_w*res)+5,height=(Sensor_h+Substance_h+Top_h+2)*res, mass=rho,radius = 1)
SUB = raster(name="substance", width=max(Sensor_w*res, Substance_w*res, Top_w*res)+5,height=(Sensor_h+Substance_h+Top_h+2)*res, mass=rho,radius = 1)

# create geometries inside the objects
Bottom_plate, Top_plate, Substance, Salt = 1, 2, 3, 4
SEN.rectangle(0, Sensor_w*res, 0, 2+Sensor_h*res,name="sensor",beadtype=Bottom_plate)
SUB.rectangle(0.5*(Sensor_w-Substance_w)*res, 0.5*(Sensor_w+Substance_w)*res, 2+Sensor_h*res, 2+(Sensor_h+Substance_h)*res,name="substance",beadtype=Substance,beadtype2=(4,0.1),)
SEN.rectangle(0.5*(Sensor_w-Top_w)*res, 0.5*(Sensor_w+Top_w)*res, 2+(Sensor_h+Substance_h)*res, 2+(Sensor_h+Substance_h+Top_h)*res,name="top plate",beadtype=Top_plate)

# preview rasters
SEN.plot()
#SEN.show(extra="label", contour=True, what="beadtype") 
SUB.plot()
#SUB.show(extra="label", contour=True, what="beadtype") 

# scale the data spacing
SEN_scaled = SEN.data(scale=(scale_factor,scale_factor),maxtype=4)
SUB_scaled = SUB.data(scale=(scale_factor,scale_factor),maxtype=4)


# %% Print Rasters
destination0 = wdir+output_destination+"/data.%s_%dtypes_" % (SEN.name,4)+output_name+".lmp"
destination1 = wdir+output_destination+"/data.%s_%dtypes_" % (SUB.name,4)+output_name+".lmp"
SEN_scaled.write(destination0)
SUB_scaled.write(destination1)

# %% Set Material Properties
FLUID = scriptdata(
        rho = rho0, # kg/m3
        c0 = c0, # m/s
        q1 = q1,
        contact_stiffness = contact_stiffness, # Pa
        contact_scale = 1.0 # dimensionless
    )
SOLID = scriptdata(
        rho = rho0, # kg/m3
        c0 = c0, # m/s
        q1 = q1,
        E = 2000,
        sigma_yield = sigma_yield, # with E defined by default as '5*${c0}^2*${rho}' (see forcefield.py:395)
        contact_stiffness = contact_stiffness, # Pa
        contact_scale = 1.0 # dimensionless
    )

# %% LAMMPS script generator

# LAMMPS initiation section
init = initialization(neighbor =[neigh_search,"bin"]) # neigh search within 1 kernel radius

#read in files section
files = file(file_name=["./data.%s_%dtypes_" % (SEN.name,4)+output_name+".lmp"],group=True,group_name=["sensor"]) & \
        file(file_name=["./data.%s_%dtypes_" % (SUB.name,4)+output_name+".lmp"],group=True,group_name=["substance"], append = True)
        
groups = group(groupID = ['fixed_bottom'], y=['EDGE',0.0002])

# particles interaction section        
b1 = scriptobject(name="bottom plate",group = ["tlsph", "bottom_plate"],forcefield=solidfood(USER=SOLID), beadtype=Bottom_plate)
b2 = scriptobject(name="top plate", group = ["tlsph", "top_plate"],forcefield=solidfood(USER=SOLID),beadtype=Top_plate)
b3 = scriptobject(name="substance", group = ["ulsph"],forcefield=water(USER=FLUID),beadtype=Substance)
b4 = scriptobject(name="salt",group = ["tlsph"],forcefield=solidfood(USER=SOLID), beadtype=Salt)

# Integration section
inte = integration(g=0,timestep=False, dt = timestep)

# Thermo data section
thermo = thermo_print(print_freq=10000)

# Equilibration step (relaxes the system)
equilsteps =   equilibration(static = "$ tlsph")

# Initiate Production dump file
dmp = smddump(dump_freq=10000,outputfile=["dump."+output_name],mechanical=True)

# squeeze step
moves = translation(group=["fixed_bottom"],fixIDv = "$ fixplate") & \
        translation(vy=v_plate,group=["top_plate"],fixIDv = "$ translatetopplate") & \
        run(runs=2000000)


interactions = b1+b2+b3+b4 # define interaction between particle types
fullscript = init + files + groups + interactions.script + inte + thermo + equilsteps + dmp + moves
fullscript.write(fullfile("Production/"+output_destination+"/in."+output_name))
