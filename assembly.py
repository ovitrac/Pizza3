#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 13:48:46 2022

@author: billy
"""

from workshop1 import *

# %% State material properties different to default
FLUID = scriptdata(
        rho = 1000,
        c0 = 100.0,
        q1 = 1.0,
        contact_stiffness = '10000000'
    )    
SOLID = scriptdata(
        rho = 2000,
        c0 = 200.0,
        sigma_yield = '0.1*${E}',
        contact_stiffness = '10000000'
    )
WALL = scriptdata(
        rho = 3000,
        c0 = 200.0,
        contact_stiffness = '10000000',
        contact_scale = 1.5
    )


# %% Building LAMMPS script using script.py

init = initialization(neighbor =[0.0015,"bin"])
     
b1 = scriptobject(name="bead 1",group = ["rigid", "solid"],filename='./raster_2_types.lmp',forcefield=rigidwall(USER=WALL))
b2 = scriptobject(name="bead 2", group = ["fluid", "ulsph"],filename = './raster_2_types.lmp',forcefield=water(USER=FLUID))
b3 = scriptobject(name="bead 3", group = ["oscillating", "solid","tlsph"],filename = './raster_4_types.lmp',forcefield=solidfood(USER=SOLID))
b4 = scriptobject(name="bead 4", group = ["solid", "tlsph"],filename = './raster_4_types.lmp',forcefield=solidfood(USER=SOLID))

inte = integration()

thermo = thermo_print()

# hold_obj =   translation(vx = ["0"],vy = ["0"],vz = ["0"],group =["oscillating"])

equilsteps =   equilibration(it=10,re=0.6)

dmp = smddump(outstep=100,outputfile=["dump.workshop1"],)

moves = translation(eqvy=["1"],group=["oscillating"]) & \
        run() & \
        force() & \
        run()



# %% Final assempbly
collection = b1+b2+b3+b4

fullscript = init + collection.script + inte + thermo + equilsteps + dmp + moves

fullscript.write("./tmp/in.swimmingpool")



