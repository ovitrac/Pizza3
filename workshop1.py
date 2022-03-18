#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Workshop 1 - main file
    
        Write a LAMMPS code directy from Python from codelets (Python script templates)
        Typical section LAMMPS code with variables (strings, expressions, vectors, lists)
        are coded with "codelets" (dynamics scripts of the class pizza.script())
        Variables values can be defined from placeholders and subsequently overidden.
        
        
        Each codelet (pizza.script object) sets two main variables
        
            DEFINITIONS coding for the variables, some examples follows:
                strings: "$ this is a string # comment"
                 vector: [1,0,1]
                   list: ["p","f","p"] or [500, 0.9, "rcb"]
                 tupple: (-10,2)
             expression: '50*${c0}^2*${rho}' with variables and mathematical operators or functions
             
                   
            TEMPLATE is a string with placeholders/variables:
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
                  
        Codelets can be displayed, converted to stings, written to a file
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
            
        -- thermo --
            
            integration()       ---> set integration parameters
            thermo_print()      ---> pseudo thermostat initialization, and computes
            
        -- equilibration --
        
            equilibration()     ---> equilibration steps
            
            note: equilibration() is designed to be multievaluated
            
        -- dump --
            
            smddump()
            
            note: dump are framework depended, set all outputs for SMD
            
        -- displacements --
        
            translation()       ---> translation of rigid objects
            force()             ---> set forces
            


Created on Fri Feb 25 13:52:08 2022 - revised on 2022-03-18

@author: olivi,billy
"""

# Revision history
# 2022-02-28 early version, almost functional (dump and run missing)
# 2022-03-01 release candidate, full documentation, better style
# 2022-03-02 full documentation for the workshop
# 2022-03-02 fix neighbor in initialization() and example
# 2022-03-02 first post-workshop0 fixes (others are coming before forking as workshop1)
# 2022-03-17 [FORK] workshop1: load, group, and interactions classes removed from
#            workshop (replaced with script.scriptobject)
#            thermo class broken into integrate and thermo_print
#            integration class created with time integration, gravity and balancing
#            thermo_printclass created with print/log screen options
#            equilibration class streamlined
#            dump class upgraded, option to chose dump information by catagories
#            translation and force classes created, can now apply equations directly
#            run class created
#            

# generic dependencies
import datetime, os, socket, getpass

# import script, forcefield and struct classes
from pizza.script import *
from pizza.forcefield import *
from pizza.private.struct import struct


# %% INITIALIZATION
class initialization(globalsection):
    """ 
    workshop1.initialization()
    workshop1.initialization(param1=value1,param2=value2)
    
        Initialize LAMMPS script of workshop1
        
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
        Next step/class: integration()
        
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
    
    # Template
    TEMPLATE = "\n\n# " + "\n# ".join(script._contact) + "\n"*3 + """
#   Scheme initialization
units       ${units}
dimension	${dimension} 
boundary    ${boundary}         # f = fixed, p = periodic
comm_modify ${comm_modify}
comm_style  ${comm_style}
atom_modify ${atom_modify}
newton ${newton}
neighbor	${neighbor}            # search radius for neighbor list (=kernel radius)
neigh_modify    every ${neigh_modify_every} delay ${neigh_modify_delay} check ${neigh_modify_check}

atom_style	${atom_style}
 """
 

# %% THERMO
class integration(integrationsection):
    """ 
    workshop1.integration( g = 9.81,g_vector = [0,1,0],dt = 0.1,adjust_radius = [1.01,10,15],
                          balance = [500, 0.9, "rcb"])
    
        Set default parameters for time integration
        
        Example
        -------
        inte = integration()
        inte = integration(g_vector = [1,-1,0]) # change direction of gravity
        
        Comments:
            refer to TEMPLATE for details
            gravity is intuitive to adjust
            integration parameters:
            dt sets the initial timestep, smd then dynamically modifies dt
            adjust_radius lets smd dynamically modify the kernel radius to optimize num. neighbors
            balance allows LAMMPS to dynamically modify the domain and processor loading
            
        Previous step/class: initialization()
        Next step/class: thermo_print()        
        
    """
    description = 'thermo(param=value...)'
    userid = "thermo()"
    version = 1.0
    
    DEFINITIONS = scriptdata(
            g = 9.81,
            g_vector = [0,1,0],
              dt = 0.1,
   adjust_radius = [1.01,10,15],
        balance = [500, 0.9, "rcb"] # load balancing for MPI
        )
    
    TEMPLATE = """
#   Gravity
fix             gfix all gravity ${g} vector ${g_vector}
#   Time integration conditions
fix             dtfix fluid smd/adjust_dt ${dt} # dynamically adjust time increment every step
fix             integration_fix_ulsph ulsph smd/integrate_ulsph adjust_radius ${adjust_radius}
fix             integration_fix_tlsph tlsph smd/integrate_tlsph
#   balancing
fix             balance_fix all balance ${balance}
"""

class thermo_print(integrationsection):
    """ 
    workshop1.thermo_print()
    
        Set frequency and parameters of terminal output
        
        Example
        -------
        thermo = thermo_print()
        thermo = thermo_print(outstep = 1000) # less terminal output
        
        Comments:
            refer to TEMPLATE for details
            default thermo_style prints number of steps and timestep (which is dynamic)
            
            
            
        Previous step/class: interactions()
        Next step/class: equilibration()        
        
    """
    description = 'thermo(param=value...)'
    userid = "thermo_print()"
    version = 1.0
    
    DEFINITIONS = scriptdata(
         outstep = 100,
         thermo_modify = ["lost","ignore"],
         thermo_style = ["custom","step","dt"]
        )
    
    TEMPLATE = """
#   thermodynamic information
thermo		   ${outstep}
thermo_modify  ${thermo_modify}
thermo_style   ${thermo_style}
"""
# %% EQUILIBRATION

class equilibration(integrationsection):
    """ 
    workshop1.equilibration()
    
        Relax and equilibrate the simulation with limit_velocities
        It performs 50 iterations where limit_velocities(n) = 0.9*maxvel(n-1) 
        where n is the iteration step: 0.9^50 = 0.005
        i.e. final_velocity =< 0.005*inital_velocity
        
        Example
        -------
        equilsteps = equilibration(iterations=10)       
        
        Comments:
            Heuristic, based on rapidly destroying kinetic energy in the system
            iterations can be modified
            rule of thumb: velocity halved every 7 iterations
            
        Previous step/class: thermo_print()
        Next step/class: smddump()        
        
    """
    description = 'equilibration()'
    userid = "equilibration()"
    version = 1.0
    
    DEFINITIONS = scriptdata(
        it = 50,
        re = 0.9
        )
    
    TEMPLATE = """
#   Equilibration
dump            dump_equilibrate all custom 100 dump.equilibrate id type x y z &
                fx fy fz vx vy vz radius
dump_modify     dump_equilibrate first yes

variable vmag atom sqrt(vx^2+vy^2+vz^2)
compute         maxvel all reduce max v_vmag
variable        maxvelre equal ${re}*c_maxvel
run     ${it}000 every 1000 &
    "print \${maxvelre}" &
    "fix             ulsph_equilibration ulsph smd/integrate_ulsph limit_velocity \${maxvelre}" &
    "fix             tlsph_equilibration tlsph smd/integrate_tlsph limit_velocity \${maxvelre}"

dump_modify     dump_equilibrate every 1000000

fix             ulsph_equilibration ulsph smd/integrate_ulsph
fix             tlsph_equilibration tlsph smd/integrate_tlsph

"""   


# %% DUMP SECTION
class smddump(dumpsection):
    """ 
    workshop1.smddump(outstep=1000,outputfile="$myfile")
    
        Dump file format for SMD
        
        Example
        -------
        dump = smddump(outstep=5000,outputfile="$ dump.workshop0")
        dump = smddump(machanical = True) # computes and dumps mechanical data        
        
        Comments:
            lots of flexibility to manage dumpfiles so several options:
            outstep = dump every outstep
            outputfile = dump filename
            
            set these to True or False to choose what to dump [DefaultValue]:
            particle_data  [True]  = id,type,x,y,z,mol,mass,volume,radius,contact_radius,density
            velocity_force [True]  = vx,vy,vz,fx,fy,fz
            mechanical     [False] = stress, strain and strain rate tensors
            thermo         [False] = internal energy
            calc_data      [False] = nn number of neighbors, processor number, hourglass error
            
        Previous step/class: equilibration()
        Next step/class: translation()        
    """
    
    description = 'smddump(outstep=1000,outputfile="$myfile")'
    userid = "smddump()"
    version = 1.0
    
    DEFINITIONS = scriptdata(
            outstep = 1000,
         outputfile = "$ dump.file",
      particle_data = ["id","type","x","y","z","mol","mass","c_rho","c_vol","radius","c_contact_radius"],
              v_xyz = ["vx","vy","vz"],
              f_xyz = ["fx","fy","fz"],
      stress_tensor = ["c_S[1]","c_S[2]"],
      strain_tensor = ["c_E[1]","c_E[2]"],
 strain_rate_tensor = ["c_L[1]","c_L[2]"],
  thermo_properties = ["c_epl"],
          calc_data = ["c_nn","proc","c_HGe"]
  
            )
    def __init__(self,particle_data=True,velocity_force=True,mechanical=False,thermo=False,calc_data=False,**args):
        COMPUTE = """
#   Additional computed values
        """
        DUMP = """

#   dump command
dump            dump_id all custom ${outstep} ${outputfile} """
        if particle_data:
            COMPUTE += """
#   Compute supp particle data
compute         contact_radius all smd/contact/radius
compute         vol all smd/vol
compute         rho all smd/rho
"""
            DUMP += """&
${particle_data} """
        if velocity_force:
            DUMP += """&
${v_xyz} ${f_xyz} """
        if mechanical:
            COMPUTE += """
#   Compute mechanical data
compute         S tlsph smd/tlsph/stress
compute         E tlsph smd/tlsph/stress
compute         L tlsph smd/tlsph/stress
compute         P ulpsh smd/ulsph/stress
"""
            DUMP += """&
${stress_tensor} ${strain_tensor} ${strain_rate_tensor}"""
        if thermo:
            COMPUTE +=  """
#   Compute thermo data
compute         e_int all smd/internal_energy"""
            DUMP += """&
${thermo_properties} """
        if calc_data:
            COMPUTE += """
#   Compute calculation data
compute         nn ulsph smd/ulsph/num/neighs
computer        HGE all smd/hourglass_error"""
            DUMP += """&
${calc_data}"""
        self.TEMPLATE = COMPUTE + DUMP + """
dump_modify     dump_id first yes #every/time 0.001
"""
        self.USER = scriptdata(**args)
        
# %% DISPLACEMENTS AND FORCES
class translation(runsection):
    """ 
    workshop1.translation(eq_vx = ["NULL"],eq_vy = ["NULL"],eq_vz = ["NULL"],
                          fix_ID = ["setvelocities"],group = "all")
    
        Translates top and bottom according to set velocities or forces
        
        Example
        -------
        moves = translation(eq_vx = ["NULL"],eq_vy = ["0"],eq_vz = ["sin(temp)",group="object1"])
               
        Comments:
            Refer to TEMPLATE for details
            =0 sets velocity to 0 whereas =NULL means do not alter
           
        Previous step/class: smddump()
        Next step/class: force()
    """
    
    description = 'translation(velocity1=[],velocity2=[],force=[],run=5000)'
    userid = "smddump()"
    version = 1.0
    
    DEFINITIONS = scriptdata(
        eqvx = ["0"],
        eqvy = ["0"],
        eqvz = ["0"],
        fixIDv = ["setvelocities"],
        group = ["all"]
        )
    TEMPLATE = """
#   Translation
variable        vx equal ${eqvx}
variable        vy equal ${eqvy}
variable        vz equal ${eqvz}
fix             ${fixIDv} ${group} smd/setvel v_vx v_vy v_vz
"""

class force(runsection):
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
        eqfx = ["0"],
        eqfy = ["0"],
        eqfz = ["0"],
        fixIDf = ["setforces"],
        group = ["all"]
        )
    TEMPLATE = """
#   Force
variable        fx equal ${eqfx}/count(${group})
variable        fy equal ${eqfy}/count(${group})
variable        fz equal ${eqfz}/count(${group})
fix             ${fixIDf} ${group} smd/setvel v_fx v_fy v_fz
"""
# %% RUN

class run(runsection):
    """ 
    workshop1.run(runs=50000)
    
        Performs a run of N steps
        
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
    
    description = 'number of runs'
    userid = "run()"
    version = 1.0
    
    DEFINITIONS = scriptdata(
        runs = 50000
        )
    TEMPLATE = """
#   run section
run ${runs}
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
    bead_kernel_radius = 0.0015
    init = initialization(neighbor =[bead_kernel_radius,"bin"])
    init.do()                    # shows the script
    
    # scriptobject handles bead interactions and sets material properties from library (rigidwall, water, solid food)
    b1 = scriptobject(name="bead 1",group = ["rigid", "solid"],filename='./raster_4_types.lmp',forcefield=rigidwall())
    b2 = scriptobject(name="bead 2", group = ["fluid", "ulsph"],filename = './raster_4_types.lmp',forcefield=water())
    b3 = scriptobject(name="bead 3", group = ["oscillating", "solid","tlsph"],filename = './raster_4_types.lmp',forcefield=solidfood())
    b4 = scriptobject(name="bead 4", group = ["solid", "tlsph"],filename = './raster_4_types.lmp',forcefield=solidfood())
    
    # set gravity, timestep, adjusted kernel radius
    inte = integration()
    
    # modify which data is returned to the terminal
    thermo = thermo_print()
    
    # equilibration/relaxation protocol, iterations can be reduced or augmented
    equilsteps =   equilibration(it=15)
    
    # modify the dump settings, outstep, properties dumped etc.
    dmp = smddump(outstep=2000,outputfile=["dump.workshop1"],)
    
    # use equations to move specific objects or groups of atoms
    moves = translation(vx = ["0.1*exp(-step/100)"],vy = ["0"],vz = ["0"]) & \
            run() & \
            translation() & \
            force() & \
            run()

    #combine everything into a full script and write file
    
    collection = b1+b2+b3+b4

    fullscript = init + collection.script + inte + thermo + equilsteps + dmp + moves

    fullscript.write("./tmp/in.swimmingpool")
