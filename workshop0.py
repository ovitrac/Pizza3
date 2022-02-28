#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Workshop 1 - main file

Created on Fri Feb 25 13:52:08 2022

@author: olivi
"""

# import script
from pizza.script import *


# %% Initialization template
class initialization(globalsection):
    """ initialize LAMMPS core-shell model"""
    description = "syntax: init(var1=val1,var2=val2,...)"
    userid = "initialization"               # user name
    version = 1.0                           # version
    
    # Properties (used in LAMMPS)
    PROPERTIES = scriptdata(
            rho_fluid= 950,     # mass density water
            rho_solid= 1100,    # mass density solid objects
                   c0= 10.0,    # speed of sound for water    
                    E= "50*${c0}*${c0}*${rho_fluid}",   # Young's modulus for droplets objects
             E_tongue= "500*${c0}*${c0}*${rho_fluid}",  # Poisson ratio for solid objects
                   nu= 0.3,     # Poisson ratio for solid objects
          sigma_yield= "0.9*${E}",  # plastic yield stress for solid objects
  hardening_parameter= 0,           # plastic hardening parameter for solid objects
    contact_stiffness= "10*${c0}^2*${rho_fluid}",       # contact force amplitude
                   q1= 1.0,     # artificial viscosity
                   q2= 0.0,     # artificial viscosity
                   Hg= 10,      # Hourglass control coefficient for solid objects
                   Cp= 1.0      # heat capacity -- not used here
        )
    
    # SMD Scheme
    SCHEME = scriptdata(
                units= "$ si",
            dimension= 2,
             boundary= "$ p f p", # simulation box boundaries
          comm_modify= "$ vel yes",
           comm_style= "$ tiled",
          atom_modify= "$ map array",
               newton= "$ off",
              neighbor= "$ 1 bin",
    neigh_modify_every= 5, 
    neigh_modify_delay= 0,
    neigh_modify_check= "$ yes",
            atom_style= "$ smd"
            )
    
    # Merge all definitions
    DEFINITIONS = PROPERTIES + SCHEME
    
    # Template
    TEMPLATE = """
# SCHEME INITIALIZATION
units       ${units}
dimension	${dimension}
boundary    ${boundary}
comm_modify ${comm_modify}
comm_style  ${comm_style}
atom_modify ${atom_modify}
newton ${newton}
neighbor	${neighbor}
neigh_modify    every ${neigh_modify_every} delay ${neigh_modify_delay} check ${neigh_modify_check}

atom_style	${atom_style}
 """
    

# %% Initialization template
class load(geometrysection):
    """ load geometry """
    description = 'syntax: load(local="$ /my/folder/",file="$ my file")'
    userid = "load()"
    version = 1.0
    
    # file to load
    DEFINITIONS = scriptdata(
            local = "$ ../datafiles",  # remove the trailing /
             file = "$ 2_Top_mod.lmp",
             mode = "$ add append"
            )
    # Template
    TEMPLATE = \
    """read_data ${local}/${file} ${mode}"""
  
class group(geometrysection):
    """ create groups """
    description = 'group(name="$ mygroup",type="$ 1 2 3")'
    userid = "group()"
    version = 1.0
    
    # group definition
    DEFINITIONS = scriptdata(
        name = "$ solid",
        type = "$ 1 2 3"
        )
    #template
    TEMPLATE = """group ${name} ${type}"""

class gravity(initializesection):
    """ apply gravity """
    description = 'gravity(g=9.81,vector="$ 0 1 0")'
    userid = "gravity()"
    version = 1.0
    
    # group definition
    DEFINITIONS = scriptdata(
             g = 9.81,
        vector = "$ 0 1 0"
        )
    #template
    TEMPLATE = """fix gfix all gravity ${g} vector ${vector} """
    
class interactions(interactionsection):
    """ set forcefield """
    description = 'interactions(top=1,bottom=2,solid=3,fluid=4)'
    userid = "interactions()"
    version = 1.0
    
    # Bead id set at construction
    def __init__(self,top=1,bottom=2,solid=3,fluid=4):
        """ set bead id with interactions(top=1,bottom=2,solid=3,fluid=4) """
        super().__init__() # required to initialize interactions
        self.beadid = scriptdata(top=top,bottom=bottom,solid=solid,fluid=fluid)
    
    # DEFINITIONS
    
    

# %% DEBUG  
# ===================================================   
# main()
# ===================================================   
# for debugging purposes (code called as a script)
# the code is called from here
# ===================================================
if __name__ == '__main__':
    
    # initizalization of the scheme
    init = initialization(c0=12) # 12 to see how to change sound velocity
    init.c0 = 13                 # works also
    init.do()                    # shows the script
    
    # read input data
    # help with load.description
    wdir = "$ ../datafile"
    geom = load(local=wdir,file="$ 2_Top_mod.lmp",mode="") & \
           load(local=wdir,file="$ 1_Bottom_mod.lmp") & \
           load(local=wdir,file="$ 3_thin_shell_outer_mod.lmp") & \
           load(local=wdir,file="$ 4_thin_shell_inner_mod.lmp")
    # create groups
    # help with groups.description
    groups = group(name="$ solid",type="$ 1 2 3") & \
             group(name="$ tlsph",type="$ 1 2 3") & \
             group(name="$ fluid",type="$ 4") & \
             group(name="$ ulsph",type="$ 4") & \
             group(name="$ moving1",type="$ 1") & \
             group(name="$ moving2",type="$ 2")
    # add gravity
    # help with physgravity.description
    physgravity = gravity(g=0)
    
    # interactions
    FF = interactions(top=1,bottom=2,solid=3,fluid=4)
    
    # full script
    fullscript = init+geom+groups+physgravity
    fullscript.write("tmp/myscript.inp")