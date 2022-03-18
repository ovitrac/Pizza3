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
        Cp = 1.0,
        taitexponent = 7,
        # hertz contacts
        contact_scale = 1.5,
        contact_stiffness = '100*${c0}^2*${rho}'
    )    
SOLID = scriptdata(
        rho = 2000,
        c0 = 200.0,
        E = '5*${c0}^2*${rho}',
        nu = 0.3,
        q1 = 1.0,
        q2 = 0.0,
        Hg = 10,
        Cp = 1.0,
        sigma_yield = '0.1*${E}',
        hardening = 0,
        # hertz contacts
        contact_scale = 1.5,
        contact_stiffness = '100*${c0}^2*${rho}'
    )
WALL = scriptdata(
        rho = 3000,
        c0 = 200.0,
        contact_stiffness = '10*${c0}^2*${rho}',
        contact_scale = 1.5
    )


# %% Building LAMMPS script using script.py

init = initialization(neighbor =[0.0015,"bin"])
     
b1 = scriptobject(name="bead 1",group = ["rigid", "solid"],filename='./raster_2_types.lmp',forcefield=rigidwall(USER=WALL))
b2 = scriptobject(name="bead 2", group = ["fluid", "ulsph"],filename = './raster_2_types.lmp',forcefield=water())
b3 = scriptobject(name="bead 3", group = ["oscillating", "solid","tlsph"],filename = './raster_4_types.lmp',forcefield=solidfood(USER=SOLID))
b4 = scriptobject(name="bead 4", group = ["solid", "tlsph"],filename = './raster_4_types.lmp',forcefield=solidfood())
  
inte = integration()

thermo = thermo_print()

hold_obj =   translation(vx = ["0"],vy = ["0"],vz = ["0"],group =["oscillating"])

equilsteps =   equilibration(it=1,re=0.6)

dmp = smddump(outstep=100,outputfile=["dump.workshop1"],)

moves = translation(eq_vx=["0.1*exp(-step/100)"],group=["oscillating"]) & \
        run() & \
        translation() & \
        force() & \
        run()



# %% Final assempbly
collection = b1+b2+b3+b4

fullscript = init + collection.script + inte + thermo + hold_obj + equilsteps + dmp + moves

fullscript.write("./tmp/in.swimmingpool")



