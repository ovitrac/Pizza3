#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Workshop 0 - main file
    
        Write a LAMMPS code directy from Python from codelets (Python script templates)
        Typical section code with variables (strings, expressions, vectors, lists)
        are coded with "codelets" (dynamics scripts of the class pizza.script())
        Variables values can be overidden.
        
        
        Each codelet (pizza.script object) set two main variables
        
            DEFINITIONS coding for the variables, some examples follows:
                strings: "$ this is a string # comment"
                 vector: [1,0,1]
                   list: ["p","f","p"] or [500, 0.9, "rcb"]
                 tupple: (-10,2)
             expression: '50*${c0}^2*${rho}' with variables and mathematical operators or functions
             
                   
            TEMPLATE the python code with variable names:
                ${variable} will be replaced by its value (possibly after evaluation)
                ${expression}

             NOTE1: Indexing is authorized in DEFINITIONS but not in TEMPLATES
                   Vectors and lists are expanded/flattened as strings when evaluated
                 run = [500,1000]
                 run0 = "${run[0]}"
                 run1 = "${run[1]}"
                 
             NOTE2: Vectors and lists are expanded with " " as separator
                    Tuples are expanded with "," as separator

        Values of definitions and new variables can be set at runtime
            mycodelet = codelet()
            mycodelet.USER.var1 = 1
            mycodelet.USER.var2 = 2
            
        Several instances may be run with different values
            mycodelet1 = codelet(var=1)
            mycodelet2 = codelet(var=2)
            mycodelet1.USER.var1 = 10
            mycodelet1.USER.var2 = 20

        Codelets can be multievaluated with the operator "&" (and)
            mycodelet = codelet(var=1) & codelet(var=2) & ...
            with all variables defined in each instance of codelet
            
        Codelets can be combined with the operator "+" (plus)
            mycodelet = codelet_1(var1=1) + codelet_2(var2=2)
            with the definition of variable var1 passed to codelet_2
            note: in the example above, codelet_2 can a function of var1, var2
            note: if the same variable is defined in two codelets, the last 
                  definition is used
            note: mycodelet can be also multievaluated:
                  mycodelet(var1=1,var2=2) & mycodelet(var1=10,var2=20)
                  
        Codelets can be displayed, converted to stings, written in a file
            mycodelet + ENTER to display it
            mycodelet.DEFINITIONS to see the definitions
            mycodelet.USER to see user definitions
            mycodelet.TEMPLATE shows the TEMPLATE
            note: It is not recommended to change TEMPLATE in instances
                  (all instances will be affected)
           
            mycodelet.do() evaluates the codelet as string
            
            mycodelet.write("inp.mylammpsscript") write a LAMMPS script
            
            
        Creating your codelets (beyond the scope of the workshop).
            All codelets should be of or derived from the class pizza.script()
            class newcodelet(oldcodelet)
                description = "blah, blah"
                useid = "newcodelet()"
                version = 0
                DEFINTIONS = scriptdata(
                    var1 = 1,
                    var2 = 2
                    )
                TEMPLATE = "" "
                # LAMMPS code
                "" "
                
    USAGE:
        from workshop0 import *
        
        use name_of_the_codelet.description to see the syntax
        
        codelet = name_of_the_codelet(var1,var2)
        fullscript = codelet1 + codelet2 + codelet3
        fullscript.write("mylammpsscript.inp")
    
    
    LIST OF CODELETS:
        
        -- initialization --
        
            initialization()    ---> initialize the framework
            load()              ---> load input data (examples from data() and raster() objects)
            group()             ---> group beads
            gravity()           ---> set gravity
            interactions()      ---> set forcefield
            
            note: load() and groups() are designed to be multievaluated
            
        -- equilibration --
        
            thermo()            ---> pseudo thermostat initialization, and computes
            equilibration()     ---> equilibration steps
            
            note: equilibration() is designed to be multievaluated
            
        -- dump --
            
            smddump()
            
            note: dump are framework depended, set all outputs for SMD
            
        -- displacements --
        
            translation()       ---> translation of rigid objects
            rampforce()         ---> set forces
            


Created on Fri Feb 25 13:52:08 2022 - revised on 2022-03-02

@author: olivi,billy
"""

# Revision history
# 2022-02-28 early version, almost functional (dump and run missing)
# 2022-03-01 release candidate, full documentation, better style
# 2022-03-02 full documentation for the workshop
# 2022-03-02 fix neighbor in initialization() and example

# generic dependencies
import datetime, os, socket, getpass

# import script, forcefield and struct classes
from pizza.script import *
from pizza.forcefield import *
from pizza.private.struct import struct


# %% Initialization template
class initialization(globalsection):
    """ 
    workshop0.initialization()
    workshop0.initialization(param1=value1,param2=value2)
    
        Initialize LAMMPS core-shell model of workshop0
        
        Example
        -------
        init = initialization(boundary=["p","f","p"],dimension=2)
        init.USER.boundary=["p","f","p"] # works also
        init.do()                       # shows the script
        bead_kernel_radius = put the value of the kernel radius of the bead
        init.USER.neighbor = [bead_kernel_radius,"bin"]
        
        Comments:
            Set parameters at during the first call or use the USER atrribute to do it
            The method do() shows the content of the script
            type init +ENTER to see all accessible DEFINITIONS and TEMPLATE
            
        How to generate a complex script
        ---------------------------------
          fullscript = init+geom+groups+physgravity+forcefield+\
              initthermo+equilsteps+dump+moves
          fullscript.write("tmp/myscript.inp")
          
          Comments:
              Several scripts can be combined with the operator +
              As a result, values set in DEFINITIONS are shared between all scripts
              Use: fullscript.write("tmp/myscript.inp") to generate a LAMMPS file
              Use: fullscript.do() to show the script
              type fullscript +ENTER to see all details
            
        Previous step/class: none
        Next step/class: load()
        
    """
    description = "initialization(var1=val1,var2=val2,...)"
    userid = "initialization"               # user name
    version = 1.0                           # version
    
    # SMD Scheme (these variables are available everywhere)
    DEFINITIONS = scriptdata(
                units= "$ si",
            dimension= 2,
             boundary= ["p","f","p"], # simulation box boundaries
          comm_modify= ["vel","yes"],
           comm_style= "$ tiled",
          atom_modify= ["map","array"],
               newton= "$ off",
              neighbor= [1,"bin"],
    neigh_modify_every= 5, 
    neigh_modify_delay= 0,
    neigh_modify_check= "$ yes",
            atom_style= "$ smd"
            )
    
    # header
    HEADER = f"# Automatic LAMMPS script (version {script.version})\n" + \
             f"# {getpass.getuser()}@{socket.gethostname()}:{os.getcwd()}\n" + \
             f'# {datetime.datetime.now().strftime("%c")}'
    
    # Template
    TEMPLATE = HEADER + "\n\n# " + "\n# ".join(script._contact) + "\n"*3 + """
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
    """ 
    workshop0.load(local="$workingdir",file="$filename")
    
        Load geometry models and assign bead indices (first digits)
        
        Example
        -------
        wdir = "$ ../datafile"
        geom = load(local=wdir,file="$ 2_Top_mod.lmp",mode="") & \
               load(local=wdir,file="$ 1_Bottom_mod.lmp") & \
               load(local=wdir,file="$ 3_thin_shell_outer_mod.lmp") & \
               load(local=wdir,file="$ 4_thin_shell_inner_mod.lmp")       
               
        Comments:
            Use "$" to define a chain without evaluation
            Use "&" (and) to link several actions (same script with different values)
            mode = "" is used to avoid "add append"
            
        Previous step/class: initialization()
        Next step/class: group()        
        
    """
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


# group beads together
class group(geometrysection):
    """ 
    workshop0.group(name="$groupname",type=1 or [1,2,3..])
    
        Set group of beads based on their types
        
        Example
        -------
        groups = group(name="$ solid",type=[1,2,3]) & \
                 group(name="$ tlsph",type=[1,2,3]) & \
                 group(name="$ fluid",type=4) & \
                 group(name="$ ulsph",type=4) & \
                 group(name="$ moving1",type=1) & \
                 group(name="$ moving2",type=2)    
               
        Comments:
            Use "$" to define a chain without evaluation
            Use "&" (and) to link several actions (same script with different values)
            type can be either int or list
            
        Previous step/class: load()
        Next step/class: gravity()        
        
    """
    description = 'group(name="$mygroup",type=[1,2,3])'
    userid = "group()"
    version = 1.0
    
    # group definition
    DEFINITIONS = scriptdata(
        name = "$ solid",
        type = [1,2,3]
        )
    #template
    TEMPLATE = """group ${name} ${type}"""


# Set gravity in simulation
class gravity(initializesection):
    """ 
    workshop0.gravity(g=9.81,vector=[0,1,0])
    
        Set gravity for simulation (intensity and orientation)
        
        Example
        -------
        physgravity = gravity(g=0)  
               
        Comments:
            In 2D, gravity should be along y (i.e., [0,1,0])
            Use "&" (and) to link several actions (same script with different values)
            type can be either int or list
            
        Previous step/class: group()
        Next step/class: interactions()        
        
    """
    description = 'gravity(g=9.81,vector=[0,1,0])'
    userid = "gravity()"
    version = 1.0
    
    # group definition
    DEFINITIONS = scriptdata(
             g = 9.81,
        vector = [0,1,0]
        )
    #template
    TEMPLATE = """fix gfix all gravity ${g} vector ${vector}"""
    
    
# set interactions
class interactions(initialization,interactionsection):
    """ 
    workshop0.interactions(top=1,bottom=2,solid=3,fluid=4)
    
        Set forcefields for workshop
        
        Example
        -------
        forcefield = interactions(top=1,bottom=2,solid=3,fluid=4)
        forcefield.FLUID.rho = 951
        forcefield.refresh() # mandatory after a value modification
               
        Comments:
            Assign bead types to the four labels "top","bottom","solid","fluid"
            Use  forcefield.FLUID to set a fluid properties
            Idem with forcefield.SOLID, forcefield.WALL
            Note1: update the all definitions with forcefield.refresh()
            Note2: forcefields have complex defitions, please refer to the code
                   and the class forcefield()
            
        Previous step/class: gravity()
        Next step/class: thermo()        
        
    """
    description = 'interactions(top=1,bottom=2,solid=3,fluid=4)'
    userid = "interactions()"
    version = 1.0
    
    # Properties (used in LAMMPS) - they are interpreted by the proper forcefield
    FLUID = scriptdata(
            rho = 950,
            c0 = 10.0,
            q1 = 1.0,
            Cp = 1.0,
            # hertz contacts
            contact_scale = 1.5,
            contact_stiffness = '10*${c0}^2*${rho}'
        )    
    SOLID = scriptdata(
            rho = 1100,
            c0 = 10.0,
            E = '50*${c0}^2*${rho}',
            nu = 0.3, # Poisson ratio for solid objects
            q1 = 1.0,
            q2 = 0.0,
            Hg = 10,
            Cp = 1.0,
            sigma_yield = '0.1*${E}',
            hardening = 0,
            # hertz contacts
            contact_scale = 1.5,
            contact_stiffness = '50*${c0}^2*${rho}'
        )
    WALL = scriptdata(
            rho = 3000,
            c0 = 10.0,
            contact_stiffness = '50*${c0}^2*${rho}',
            contact_scale = 1.5
        )
       
    # Bead id set at construction
    def __init__(self,top=1,bottom=2,solid=3,fluid=4):
        """ set bead id with interactions(top=1,bottom=2,solid=3,fluid=4) """
        super().__init__() # required to initialize interactions
        self.beadid = scriptdata(top=top,bottom=bottom,solid=solid,fluid=fluid)
        self.forcefield = struct(
            fluid = water(beadtype=fluid, userid="fluid", USER=self.FLUID),
            solid = solidfood(beadtype=solid, userid="solid",USER=self.SOLID),
            top = rigidwall(beadtype=top, userid="top", USER=self.WALL),
            bottom = rigidwall(beadtype=bottom, userid="bottom", USER=self.WALL)
                   )
        self.TEMPLATE = "\n# ===== [ BEGIN FORCEFIELD SECTION ] "+"="*80 +\
                   self.forcefield[0].pair_style() + \
                   self.forcefield.fluid.pair_diagcoeff() + \
                   self.forcefield.solid.pair_diagcoeff() + \
                   self.forcefield.top.pair_diagcoeff() + \
                   self.forcefield.bottom.pair_diagcoeff() + \
                   self.forcefield.bottom.pair_offdiagcoeff(self.forcefield.top) + \
                   self.forcefield.bottom.pair_offdiagcoeff(self.forcefield.fluid) + \
                   self.forcefield.bottom.pair_offdiagcoeff(self.forcefield.solid) + \
                   self.forcefield.top.pair_offdiagcoeff(self.forcefield.fluid) + \
                   self.forcefield.top.pair_offdiagcoeff(self.forcefield.solid) + \
                   self.forcefield.solid.pair_offdiagcoeff(self.forcefield.fluid) + \
                   "\n# ===== [ END FORCEFIELD SECTION ] "+"="*82+"\n"
        self.DEFINTIONS = scriptdata() # no definitions
        
    # Refresh data
    def refresh(self):
        """ refresh values """
        self.__init__(top=self.beadid.top,
                    bottom=self.beadid.bottom,
                    solid=self.beadid.solid,
                    fluid=self.beadid.fluid)
        


# %% Equilibration and dynamics
class thermo(integrationsection):
    """ 
    workshop0.thermo(adjust_radius = [1.01,10,15],limit_velocity=1000)
    
        Set default parameters for time integration
        
        Example
        -------
        initthermo = thermo()
               
        Comments:
            Do not change the parameters without reading the "style" manual
            
            
        Previous step/class: interactions()
        Next step/class: equilibration()        
        
    """
    description = 'thermo(param=value...)'
    userid = "thermo()"
    version = 1.0
    
    DEFINITIONS = scriptdata(
              dt = 0.1,
   adjust_radius = [1.01,10,15],
  limit_velocity = 1000,
         thermo = 50,
  thermo_modify = ["lost","ignore"],
        balance = [500, 0.9, "rcb"] # load balancing for MPI
        )
    
    TEMPLATE = """
#   Time integration conditions
fix             dtfix fluid smd/adjust_dt ${dt} # dynamically adjust time increment every step
fix             integration_fix fluid smd/integrate_ulsph adjust_radius ${adjust_radius}
fix             integration_fix_solid solid smd/integrate_tlsph limit_velocity ${limit_velocity}
fix             integration_fix_moving1 moving1 smd/integrate_tlsph limit_velocity ${limit_velocity}
fix             integration_fix_moving2 moving2 smd/integrate_tlsph limit_velocity ${limit_velocity}
#   thermo
thermo		   ${thermo}
thermo_modify  ${thermo_modify}
#   balancing
fix             balance_fix all balance ${balance}
"""

class equilibration(integrationsection):
    """ 
    workshop0.equilibration(mode="init|slow|fast",limit_velocity=1000,run=1000)
    
        Equilibrate the simulation with various limit_velocities
        
        Example
        -------
        equilsteps = equilibration(mode="init",run=[1000,2000]) & \
                     equilibration(mode="fast",limit_velocity=1000,run=1000) & \
                     equilibration(mode="slow",limit_velocity=0.01,run=1000) & \
                     equilibration(mode="fast",limit_velocity=1000,run=1000)
               
        Comments:
            Heuristic, please update the flavor to your case
            
            
        Previous step/class: thermo()
        Next step/class: smddump()        
        
    """
    description = 'equilibration(mode="init",limit_velocity=1000,run=1000)'
    userid = "equilibration()"
    version = 1.0
    
    DEFINITIONS = scriptdata(
        velocity = [0,0,0],
        limit_velocity = 0.01,
        run = [1000,1000]
        )
    
    def __init__(self,mode="init",**args):
        if mode=="init":
            self.TEMPLATE = f"#   Equilibration {mode}" + """
fix             movement1 moving1 smd/setvel ${velocity}
fix             movement2 moving2 smd/setvel ${velocity}
run		${run_0_}
fix             integration_fix_solid solid smd/integrate_tlsph limit_velocity ${limit_velocity}
fix             integration_fix_moving1 moving1 smd/integrate_tlsph limit_velocity ${limit_velocity}
fix             integration_fix_moving2 moving2 smd/integrate_tlsph limit_velocity ${limit_velocity}
run		${run_1_}
"""
        else:
            self.TEMPLATE = f"#   Equilibration {mode}" + """
fix             integration_fix_solid solid smd/integrate_tlsph limit_velocity ${limit_velocity}
fix             integration_fix_moving1 moving1 smd/integrate_tlsph limit_velocity ${limit_velocity}
fix             integration_fix_moving2 moving2 smd/integrate_tlsph limit_velocity ${limit_velocity}
run		${run_0_}
"""
        # populate run values and create run_0_,run_1_
        self.USER = scriptdata(**args)
        tmp = self.DEFINITIONS + self.USER
        if 'run' in tmp:
            if isinstance(tmp.run,(int,float)): tmp.run = [tmp.run]
            for irun in range(len(tmp.run)):
                self.USER.setattr(f"run_{irun}_",tmp.run[irun])
        
        


# %% DUMP SECTION
class smddump(dumpsection):
    """ 
    workshop0.smddump(outstep=1000,outputfile="$myfile")
    
        Dump file format for SMD
        
        Example
        -------
        dump = smddump(outstep=5000,outputfile="$ dump.workshop0")
               
        Comments:
            outstep = dump every outstep
            outputfile = dump filename
            
        Previous step/class: equilibration()
        Next step/class: translation()        
    """
    
    description = 'smddump(outstep=1000,outputfile="$myfile")'
    userid = "smddump()"
    version = 1.0
    
    DEFINITIONS = scriptdata(
        outstep = 7000,
     outputfile = "$ dump.file"
        )

    TEMPLATE = """
#   Computes
compute         eint all smd/internal/energy
compute         contact_radius all smd/contact/radius
compute         S solid smd/tlsph/stress
compute         nn fluid smd/ulsph/num/neighs
compute         epl solid smd/plastic/strain
compute         vol all smd/vol
compute         rho all smd/rho

#   Dump file
dump            dump_id all custom ${outstep} ${outputfile} id type x y z &
                fx fy fz vx vy vz c_eint c_contact_radius mol &
                c_S[1] c_S[2] c_S[3] c_S[4] mass c_epl c_vol c_rho c_nn proc
dump_modify     dump_id first yes
"""

# %% DISPLACEMENTS and integration
class translation(runsection):
    """ 
    workshop0.translation(velocity1=[],velocity2=[],force=[],run=5000)
    
        Translates top and bottom according to set velocities or forces
        
        Example
        -------
        moves = translation(velocity1 = [0,-1,0], velocity2 = [0,1,0],run=5000) & \
                translation(velocity1 = [0,-0.1,0], velocity2 = [0,0.1,0],run=2000) & \
                translation(force=[0,-1,0], velocity1 = [0,0,0], velocity2 = [0,0,0],run=21000) & \
                rampforce(ramp=(-1,-10), velocity1 = [0,0,0], velocity2 = [0,0,0],run=21000)
               
        Comments:
            Refer to TEMPLATE for details
           
        Previous step/class: smddump()
        Next step/class: rampforce()        
    """
    
    description = 'translation(velocity1=[],velocity2=[],force=[],run=5000)'
    userid = "smddump()"
    version = 1.0
    
    DEFINITIONS = scriptdata(
        velocity1 = [0,-1,0],
        velocity2 = [0,1,0],
        force = [0,0,0],
        run = 5000
        )
    TEMPLATE = """
#   Translation
fix             movement1 moving1 smd/setvel ${velocity1}
fix             movement2 moving2 smd/setvel ${velocity2}
fix             force1 moving1 setforce ${force}
run		${run}
"""

class rampforce(runsection):
    """ 
    workshop0.rampforec(ramp=(-1,10),run=5000)
    
        Applies a force ramp
        
        Example
        -------
        moves = translation(velocity1 = [0,-1,0], velocity2 = [0,1,0],run=5000) & \
                translation(velocity1 = [0,-0.1,0], velocity2 = [0,0.1,0],run=2000) & \
                translation(force=[0,-1,0], velocity1 = [0,0,0], velocity2 = [0,0,0],run=21000) & \
                rampforce(ramp=(-1,-10), velocity1 = [0,0,0], velocity2 = [0,0,0],run=21000)
               
        Comments:
            Refer to TEMPLATE for details
            The ramp must be defined with a Tuple (mandatory)
           
        Previous step/class: translation()
        Next step/class: none        
    """
    
    description = "rampforec(ramp=(-1,10),run=5000)"
    userid = "smddump()"
    version = 1.0
    
    DEFINITIONS = scriptdata(
        ramp = (-1,10),
        run = 5000
        )
    TEMPLATE = """
#   Force ramp
variable        ramp equal ramp(${ramp})
fix             movement1 moving1 smd/setvel 0 NULL 0
fix             movement2 moving2 smd/setvel 0 0 0
fix             force1 moving1 setforce 0 v_ramp 0
run		${run}
"""


# %% DEBUG  
# ===================================================   
# main()
# ===================================================   
# for debugging purposes (code called as a script)
# the code is called from here
# ===================================================
if __name__ == '__main__':
    
    # initizalization of the scheme (note that c0 is note used in DEFINITIONS)
    bead_kernel_radius = 1.5
    init = initialization(neighbor =[bead_kernel_radius,"bin"])
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
    groups = group(name="$ solid",type=[1,2,3]) & \
             group(name="$ tlsph",type=[1,2,3]) & \
             group(name="$ fluid",type=4) & \
             group(name="$ ulsph",type=4) & \
             group(name="$ moving1",type=1) & \
             group(name="$ moving2",type=2)
    # add gravity
    # help with physgravity.description
    physgravity = gravity(g=0)
    
    # interactions (do not forget to refresh)
    forcefield = interactions(top=1,bottom=2,solid=3,fluid=4)
    forcefield.FLUID.rho = 951
    forcefield.refresh() # mandatory after a value modification
    
    
    # equilibration
    initthermo = thermo()
    equilsteps = equilibration(mode="init",run=[1000,2000]) & \
                 equilibration(mode="fast",limit_velocity=1000,run=1000) & \
                 equilibration(mode="slow",limit_velocity=0.01,run=1000) & \
                 equilibration(mode="fast",limit_velocity=1000,run=1000)
  
    # dump
    dump = smddump(outstep=5000,outputfile="$ dump.workshop0")
    
    # displacements
    moves = translation(velocity1 = [0,-1,0], velocity2 = [0,1,0],run=5000) & \
            translation(velocity1 = [0,-0.1,0], velocity2 = [0,0.1,0],run=2000) & \
            translation(force=[0,-1,0], velocity1 = [0,0,0], velocity2 = [0,0,0],run=21000) & \
            rampforce(ramp=(-1,-10), velocity1 = [0,0,0], velocity2 = [0,0,0],run=21000)
  
    # full script
    fullscript = init+geom+groups+physgravity+forcefield+\
        initthermo+equilsteps+dump+moves
    fullscript.write("tmp/myscript.inp")
