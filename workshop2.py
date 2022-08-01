#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Workshop 2 - main file
    
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
        from workshop2 import *
        
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
        
            translation()       ---> impose translation on object
            force()             ---> impose force on object
            


Created on Fri Feb 25 13:52:08 2022 - revised on 2022-07-

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
# 2022-04-20 [FORK] workshop2: (minor) integration modified, dtfix now acts on 
#            "ulsph", not "fluid", to make labelling consistent
#            (minor) feature added to equilibrate to make groups of atoms
#            static during equilibration process
#            (major) translation and force modified and improved, now possible
#            to chose equations for velocity and a NULL condition for objects
#            e.g. eq_vx="$ sin(temp)", v_fy="$ NULL"
# 2022-04-28 [FORK] viscosimeter, dedicated for numerical experiments in viscometry
# 2022-04-29 Viscous stress print to smddump: "c_P[1]","c_P[2]","c_P[3]" etc.
#            by diffult, adjust radius now does nothing
# 2022-7-26  [FORK] workshop2: ulsph stress tensor calculation was changed from
#            to virial stress tensor calculation due to the limits of SMD package
#            translation and force classes further improved so that variable 
#            names can be specified case-by-case
#            files section created, replacing filename arg in particle interaction section
# generic dependencies
import datetime, os, socket, getpass

# import script, forcefield and struct classes
from pizza.script import *
from pizza.forcefield import *
from pizza.private.struct import struct


# %% INITIALIZATION
class initialization(globalsection):
    """ 
    workshop2.initialization()
    workshop2.initialization(param1=value1,param2=value2)
    
        Initialize LAMMPS script of workshop2
        
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
dimension	${dimension}        # 2 or 3 dimensions
boundary    ${boundary}         # f = fixed, p = periodic
comm_modify ${comm_modify}      
comm_style  ${comm_style}       # brick or tiled (docs.lammps.org/comm_style.html)
atom_modify ${atom_modify}
newton      ${newton}
neighbor	${neighbor}         # search radius for neighbor list (=kernel radius)
neigh_modify    every ${neigh_modify_every} delay ${neigh_modify_delay} check ${neigh_modify_check}

atom_style	${atom_style}
 """


class file(globalsection):
    """ 
    workshop2.file(file_name = ["filelmp"],group_name = ["groupID"],group=False,append=False)
    
        Define how files are read. Use group=True to add the contents of the file to a custom group
        Use append=True for consecutive file loads (this is mandatory for every file except the first)
        
        Example
        -------
        file(file_name=["./data.file"],group=True,group_name=["data1"], append = False)   
        Previous step/class: initialization()
        Next step/class: group()        
        
    """
    description = 'file(param=value...)'
    userid = "file()"
    version = 1.0
    
    DEFINITIONS = scriptdata(
        file_name = ["filelmp"],
        group_name = ["groupID"],
        )
    def __init__(self,group=False,append=False,**args):
        READDATA = """
#   Load files
read_data ${file_name} """
        if append:
            READDATA = READDATA+"add append "
        if group:
            READDATA = READDATA+"group ${group_name}"
        self.TEMPLATE= READDATA
        self.USER = scriptdata(**args)


class group(globalsection):
    """ 
    workshop2.group()
    
        Define new groups by selection a region of atoms.
        By default, all spatial arguments are 'EDGE' which means the edge of the domain box.
        
        Example
        -------
        groups = group(groupID = ['fixed_bottom'], y=['EDGE',0.0002])
        Previous step/class: initialization()
        Next step/class: integration()        
        
    """
    description = 'group(param=value...)'
    userid = "group()"
    version = 1.0
    
    DEFINITIONS = scriptdata(
        groupID = ["regionID"],
              x = ['EDGE','EDGE'],
              y = ['EDGE','EDGE'],
              z = ['EDGE','EDGE']
        )
    TEMPLATE = """
region      ${groupID} block ${x} ${y} ${z} units box
group       ${groupID} region ${groupID}
    """
# %% THERMO
class integration(integrationsection):
    """ 
    workshop2.integration( g = 9.81,g_vector = [0,1,0],dt = 0.1,adjust_radius = [1.01,10,15],
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
            
        Previous step/class: file()
        Next step/class: thermo_print()        
        
    """
    description = 'thermo(param=value...)'
    userid = "thermo()"
    version = 1.0
    
    DEFINITIONS = scriptdata(
            g = 9.81,
            g_vector = [0,1,0],
              sf = 0.1,
              dt = 1E-7,
   adjust_radius = [1.00,10,15],
        balance = [500, 0.9, "rcb"] # load balancing for MPI
        )

    def __init__(self,timestep=False,**args):
        READDATA = """
#   Gravity
fix             gfix all gravity ${g} vector ${g_vector} # apply gravitational force
#   Time integration conditions
fix             integration_fix_ulsph ulsph smd/integrate_ulsph adjust_radius ${adjust_radius}
fix             integration_fix_tlsph tlsph smd/integrate_tlsph
#   balancing
fix             balance_fix all balance ${balance}
    """
        if timestep:
            READDATA = READDATA+"""#   A user-speficied timestep is applied
timestep        ${dt} """
        else:
            READDATA = READDATA+"""#   timestep calculated using CFL criteria
            fix             dtfix ulsph smd/adjust_dt ${sf} # dynamic timestep (CFL criteria)"""
        self.TEMPLATE= READDATA
        self.USER = scriptdata(**args)

class thermo_print(integrationsection):
    """ 
    workshop2.thermo_print()
    
        Set frequency and parameters of terminal output
        
        Example
        -------
        thermo = thermo_print()
        thermo = thermo_print(print_freq = 1000) # less terminal output
        
        Comments:
            refer to TEMPLATE for details
            default thermo_style prints number of steps and timestep (which is dynamic)
            
            
            
        Previous step/class: group()
        Next step/class: equilibration()        
        
    """
    description = 'thermo(param=value...)'
    userid = "thermo_print()"
    version = 1.0
    
    DEFINITIONS = scriptdata(
            print_freq = 100,
         thermo_modify = ["lost","ignore"],
          thermo_style = ["custom","step","dt"]
        )
    
    TEMPLATE = """
#   thermodynamic information
thermo		   ${print_freq}       # print TD information every N steps    
thermo_modify  ${thermo_modify} # set options for how TD info is computed and printed
thermo_style   ${thermo_style}  # specify what TD info is printed (default [N dt])
"""
# %% EQUILIBRATION

class equilibration(integrationsection):
    """ 
    workshop2.equilibration()
    
        Relax and equilibrate the simulation 
        It performs 50 iterations of setting all velocities in the system to 0
        I.E. the simulation relaxes for 1000 steps to turn PE -> KE, then after
        all KE is set to 0
        
        Example
        -------
        equilsteps = equilibration(iterations=10, static="walls")       
        
        Comments:
            Heuristic, based on destroying kinetic energy in the system
            iterations can be modified
            static = "$ group" fixes atoms in a group during equilibration
            example use being to maintain an enclosure around a fluid
            
        Previous step/class: thermo_print()
        Next step/class: smddump()        
        
    """
    description = 'equilibration()'
    userid = "equilibration()"
    version = 1.0
    
    DEFINITIONS = scriptdata(
        it = 50,
        re = 0.9,
        static = "$ tlsph"
        )
    
    TEMPLATE = """
#   Equilibration
fix             static_objects ${static} smd/setvel 0 0 0 # ${static} have 0 velocity during equilibration

dump            dump_equilibrate all custom 100 dump.equilibrate id type x y z &
                fx fy fz vx vy vz radius
dump_modify     dump_equilibrate first yes time yes # a light equilibration dump file is made for forensics

variable vmag atom sqrt(vx^2+vy^2+vz^2)         # velocity magnitude is computed
compute         maxvel all reduce max v_vmag    # maximum velocity among all atoms
variable        maxvelre equal ${re}*c_maxvel   # reduced maximum velocity is computed
run     ${it}000 every 1000 &
    "fix             ulsph_equilibration ulsph smd/integrate_ulsph limit_velocity 0" &
    "fix             tlsph_equilibration tlsph smd/integrate_tlsph limit_velocity 0" &
    "run             0"                                                              &
    "fix             ulsph_equilibration ulsph smd/integrate_ulsph" &
    "fix             tlsph_equilibration tlsph smd/integrate_tlsph" # Every 1000 steps set destroy all KE

dump_modify     dump_equilibrate every 1000000 # frequency of dumps into the equilibrate file is replaced by a very large number

fix             ulsph_equilibration ulsph smd/integrate_ulsph # velocity limits are removed ahead of the product run
fix             tlsph_equilibration tlsph smd/integrate_tlsph # velocity limits are removed ahead of the product run
fix             static_objects ${static} smd/setvel NULL NULL NULL  # ${static} have 0 velocity during equilibration

"""   


# %% DUMP SECTION
class smddump(dumpsection):
    """ 
    workshop2.smddump(outstep=1000,outputfile="$myfile")
    
        Dump file format for SMD
        
        Example
        -------
        dump = smddump(dump_freq=5000,outputfile="$ dump.workshop0")
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
          dump_freq = 1000,
         outputfile = "$ dump.file",
      particle_data = ["id","type","x","y","z","mol","mass","c_rho","c_vol","radius","c_contact_radius"],
              v_xyz = ["vx","vy","vz"],
              f_xyz = ["fx","fy","fz"],
   stress_tensor_tl = ["c_S[1]","c_S[2]","c_S[3]","c_S[4]","c_S[5]","c_S[6]","c_S[7]"],
   strain_tensor_tl = ["c_E[1]","c_E[2]","c_E[3]","c_E[4]","c_E[5]","c_E[6]"],
strain_rate_tensor_tl = ["c_L[1]","c_L[2]","c_L[3]","c_L[4]","c_L[5]","c_L[6]"],
   stress_tensor_ul = ["c_P[1]","c_P[2]"],
  thermo_properties = ["c_epl"],
          calc_data = ["c_nn","proc","c_HGe"]
  
            )
    def __init__(self,particle_data=True,velocity_force=True,mechanical=False,thermo=False,calc_data=False,**args):
        COMPUTE = """
#   Additional computed values
        """
        DUMP = """

#   dump command
dump            dump_id all custom ${dump_freq} ${outputfile} """
        if particle_data:
            COMPUTE += """
#   Compute supp particle data
compute         contact_radius all smd/contact/radius # compute contact radius
compute         vol all smd/vol # compute local volume
compute         rho all smd/rho # compute local density
"""
            DUMP += """&
${particle_data} """
        if velocity_force:
            DUMP += """&
${v_xyz} ${f_xyz} """
        if mechanical:
            COMPUTE += """
#   Compute mechanical data
compute         S tlsph smd/tlsph/stress # computed Cauchy stress tensor terms and Von Mises eqv; xx yy zz xy xz yz vm
compute         E tlsph smd/tlsph/strain # computed strain tensor terms; xx yy zz xy xz yz
compute         L tlsph smd/tlsph/strain/rate # computed strain rate tensor terms; xx yy zz xy xz yz
#compute         P ulsph smd/ulsph/stress # computed Cauchy stress tensor (currently a non-feature in SMD package)
compute         P ulsph stress/atom NULL  #Virial stress tensor to approximate stress in units pressure*volume (https://docs.lammps.org/compute_stress_atom.html)
"""
            DUMP += """&
${stress_tensor_tl} ${strain_tensor_tl} ${strain_rate_tensor_tl} &
${stress_tensor_ul} """
        if thermo:
            COMPUTE +=  """
#   Compute thermo data
compute         e_int all smd/internal_energy # compute internal energy"""
            DUMP += """&
${thermo_properties} """
        if calc_data:
            COMPUTE += """
#   Compute calculation data
compute         nn ulsph smd/ulsph/num/neighs # compute number of neighbors
computer        HGE all smd/hourglass_error # compute hourglass error"""
            DUMP += """&
${calc_data}"""
        self.TEMPLATE = COMPUTE + DUMP + """
dump_modify     dump_id first yes time yes
"""
        self.USER = scriptdata(**args)
        
# %% DISPLACEMENTS AND FORCES
class translation(runsection):
    """ 
    workshop2.translation(vx_name = "vel_x", vy_name = "vel_y", vz_name = "vel_z",
                          vx_eq = 0, vy_eq = 0, vz_eq = 0, vx = "$ v_vel_x",
                          vy = "$ v_vel_y", vz = "$ v_vel_z", 
                          fix_ID = ["setvelocities"], group = "all")
    
        Translates objects according to imposed velocities (units m/s)
        By default, everything is set to 0 velocity (i.e. object is frozen)
                
        Example
        -------
        moves = translation(vy_eq = 0,vz_eq ="$ sin(time)", vx="NULL", group=["object1"])
        
        Comments:
       
            Refer to TEMPLATE for details

            vx_name, vy_name, vz_name, sets the name of the velocity variable,
            if consecutive movements are being performed in one script, they each 
            need their own name
        
            vx_eq, vy_eq, vz_eq, specifies an equation to perform an action (see 
            https://docs.lammps.org/variable.html for the syntax for maths)

            N.B. vx_eq=0 sets velocity to 0 (i.e. frozen) whereas vx=NULL means do not alter (i.e. free movement)
            To set a NULL condition, vx="NULL", vy="NULL", vz="NULL"
            You also have the right to set vx, vy, vz directly to constants,
            annulling any previous set values e.g. vx=1, vy=0 
        Previous step/class: smddump()
        Next step/class: force()
    """
    
    description = 'translation(vx_eq=[],vy_eq=[],group="object1")'
    userid = "translate()"
    version = 1.0
    

    DEFINITIONS = scriptdata(
    vx_name = "$ vel_x",
    vy_name = "$ vel_y",
    vz_name = "$ vel_z",
      vx_eq = 0,
      vy_eq = 0,
      vz_eq = 0,
     fixIDv = "$ setvelocities",
      group = "$ all",
      vx = "$ v_${vx_name}",
      vy = "$ v_${vy_name}",
      vz = "$ v_${vz_name}"
        )

    
    TEMPLATE = """
#   Translation
variable        ${vx_name} equal ${vx_eq} # variable defined in x-direction
variable        ${vy_name} equal ${vy_eq} # variable defined in y-direction
variable        ${vz_name} equal ${vz_eq} # variable defined in z-direction
fix             ${fixIDv} ${group} smd/setvel ${vx} ${vy} ${vz}  # set velocities to ${group}
"""

class force(runsection):
    """ 
    workshop2.force(fx_name = "force_x", fy_name = "force_y", fz_name = "force_z",
                          fx_eq = 0, fy_eq = 0, fz_eq = 0, fx = "$ v_force_x",
                          fy = "$ v_force_y", fz = "$ v_force_z", 
                          fix_ID = ["setforces"], group = "all")
    
        Imposes forces on an object (units N (Newtons))
        By default, everything is set to 0 force (i.e. object is frozen)
                
        Example
        -------
        moves = force(fy_eq = 0,fz_eq ="$ sin(time)", fx="NULL", group=["object1"])
        
        Comments:
       
            Refer to TEMPLATE for details

            fx_name, fy_name, fz_name, sets the name of the force variable, if 
            consecutive movements are being performed in one script, they each 
            need their own name
        
            fx_eq, fy_eq, fz_eq, specifies an equation to perform an action (see 
            https://docs.lammps.org/variable.html for the syntax for maths)

            N.B. fx_eq=0 sets force to 0 (acceleration=0 i.e. frozen) whereas 
            fx=NULL means do not alter (i.e. free movement)
            To set a NULL condition, fx="NULL", fy="NULL", fz="NULL"
            You also have the right to set fx, fy, fz directly to constants,
            annulling any previous set values e.g. fx=1, fy=0 
        Previous step/class: translation()
        Next step/class: run()
    """
    
    description = 'force(fx_eq=[],fy_eq=[],group="object1")'
    userid = "force()"
    version = 1.0
    
    
    DEFINITIONS = scriptdata(
    fx_name = "$ force_x",
    fy_name = "$ force_y",
    fz_name = "$ force_z",
      fx_eq = 0,
      fy_eq = 0,
      fz_eq = 0,
     fixIDv = "$ setforces",
      group = "$ all",
       fx = "$ v_${fx_name}",
       fy = "$ v_${fy_name}",
       fz = "$ v_${fz_name}"
        ) 
    
    TEMPLATE = """
#   Translation
variable        ${fx_name} equal ${fx_eq} # variable defined in x-direction
variable        ${fy_name} equal ${fy_eq} # variable defined in y-direction
variable        ${fz_name} equal ${fz_eq} # variable defined in z-direction
fix             ${fixIDv} ${group} smd/setvel ${fx} ${fy} ${fz}  # set forces to ${group}
"""

# %% RUN

class run(runsection):
    """ 
    workshop2.run(runs=50000)
    
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
    dmp = smddump(outstep=2000,outputfile=["dump.workshop2"],)
    
    # use equations to move specific objects or groups of atoms
    moves = translation(vx = "$ 0.1*exp(-step/100)",v_vy = "$ NULL",vz = 0) & \
            run() & \
            translation() & \
            force() & \
            run()

    #combine everything into a full script and write file
    
    collection = b1+b2+b3+b4

    fullscript = init + collection.script + inte + thermo + equilsteps + dmp + moves

    fullscript.write("./tmp/in.swimmingpool")
