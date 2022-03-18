# Pizza3 #

> Contributors:
>
> ​	INRAE\Olivier Vitrac, E-mail: [olivier.vitrac@agroparistech.fr](olivier.vitrac@agroparistech.fr) (main contact)
>
> ​	INRAE\William Jenkinson, E-mail: [william.jenkinson@agroparistech.fr](olivier.vitrac@agroparistech.fr)
>
> $ 2020-04-18 $

*Click [here](https://htmlpreview.github.io/?https://raw.githubusercontent.com/ovitrac/Pizza3/main/README.html) to read this file in HTML (including with videos)*

[TOC]

##  Scope

Pizza3 is a fork and an extension of Pizza.py toolkit for LAMMPS witten in Python 3.x (the original one is in Python 2.x). It should be seen as loosely integrated collection of tools for LAMMPS.



 The most important achievements are discussed hereafter. Work in progress, come back regularly.



## Overview

Main scripts and classes are shown here.

| Workshops<br> (workable demonstrations) |             **Main classes<br/>and subclasses**              |                    Low-level<br/> classes                    |
| :-------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
|            class: workshop1             |                2D drawing class: pizza.raster                |    generic struct class à la Matlab: pizza.private.struct    |
|            script: geometry             |      class to read/write input files: pizza.data3.data       | self-evaluable struct with scripting/alias features: pizza.private.param |
|            script: assembly             |         class to manage dump files: pizza.dump3.dump         |                                                              |
|                                         | advanced scripting classes: pizza.script.script, pizza.script.datascript, pizza.script.scriptobject, pizza.script.scriptobjectgroup, pizza.script.pipescript |                                                              |
|                                         | forcefield classes: pizza.forcefield.forcefield, pizza.forcefield.smd, pizza.forcefield.tlsph, pizza.forcefield.ulsph, pizza.forcefield.none, pizza.forcefield.water, pizza.forcefield.solidfood, pizza.forcefield.rigidwall |                                                              |

## Key steps

The main steps to use  workshop1 are shown here:

```mermaid
graph TD;
    G[geometry] --> R
    R[raster] --> F[data.write]
    W[workshop1] --> A
    F --> A
    A[assembly] --> D[dump]
```

## Overview of workshop1 classes

Workshop1 contains 7 main steps and codes as:


```python
# initizalization of the scheme 
bead_kernel_radius = 0.0015
init = initialization(neighbor =[bead_kernel_radius,"bin"])
    
# scriptobject handles bead interactions
FLUID = scriptdata(
        rho = 1000,
        c0 = 100.0,
        q1 = 1.0,
        contact_stiffness = 10000000
    )    
SOLID = scriptdata(
        rho = 2000,
        c0 = 200.0,
        sigma_yield = '0.1*${E}',
        contact_stiffness = 10000000
    )
WALL = scriptdata(
        rho = 3000,
        c0 = 200.0,
        contact_stiffness = 10000000,
        contact_scale = 1.5
    )
b1 = scriptobject(name="bead 1",
                  group = ["rigid", "solid"],
                  filename='./raster_2_types.lmp',
                  forcefield=rigidwall(USER=WALL))
b2 = scriptobject(name="bead 2",
                  group = ["fluid", "ulsph"],
                  filename = './raster_2_types.lmp',
                  forcefield=water(USER=FLUID))
b3 = scriptobject(name="bead 3",
                  group = ["oscillating", "solid","tlsph"],
                  filename = './raster_4_types.lmp',
                  forcefield=solidfood(USER=SOLID))
b4 = scriptobject(name="bead 4",
                  group = ["solid", "tlsph"],
                  filename = './raster_4_types.lmp',
                  forcefield=solidfood(USER=SOLID))

# set gravity, timestep, adjusted kernel radius
inte = integration()
    
# modify which data is returned to the terminal
thermo = thermo_print()
    
# equilibration/relaxation protocol, iterations can be reduced or augmented
equilsteps =   equilibration(it=15)
    
# modify the dump settings, outstep, properties dumped etc.
dmp = smddump(outstep=2000,outputfile=["dump.workshop1"],)
    
# use equations to move specific objects or groups of atoms
moves = translation(vx = ["0.1*exp(-step/100)"],
                        vy = ["0"],vz = ["0"]) & \
		run() & \
        translation() & \
        force() & \
        run()

# combine everything into a full script and write file  
collection = b1+b2+b3+b4
fullscript = init + collection.script + inte \
     			 + thermo + equilsteps + dmp + moves
fullscript.write("./tmp/in.swimmingpool")
```

The equivalent flowchart reads:

```mermaid
classDiagram
class initialization{
	<<globalsection>>
	                units= "$ si"
            dimension= 2
             boundary= ["p","f","p"]
          comm_modify= ["vel","yes"]
           comm_style= "$ tiled"
          atom_modify= ["map","array"]
               newton= "$ off"
              neighbor= [1,"bin"]
    neigh_modify_every= 5 
    neigh_modify_delay= 0
    neigh_modify_check= "$ yes"
            atom_style= "$ smd"
}

class integration{
	 <<integrationsection>>
            g = 9.81
            g_vector = [0,1,0]
              dt = 0.1
   adjust_radius = [1.01,10,15]
        balance = [500, 0.9, "rcb"] # load balancing for MPI
}

class thermo_print{
	<<integrationsection>>
	            g = 9.81
            g_vector = [0,1,0]
              dt = 0.1
   adjust_radius = [1.01,10,15]
        balance = [500, 0.9, "rcb"] # load balancing for MPI
}

class equilibration{
	<<integrationsection>>
	    it = 50,
        re = 0.9
}

class smddump{
	<<dumpsection>>
	            outstep = 1000,
         outputfile = "$ dump.file",
      particle_data = ["id","type","x","y","z","mol"...]
              v_xyz = ["vx","vy","vz"]
              f_xyz = ["fx","fy","fz"]
      stress_tensor = ["c_S[1]","c_S[2]"]
      strain_tensor = ["c_E[1]","c_E[2]"]
 strain_rate_tensor = ["c_L[1]","c_L[2]"]
  thermo_properties = ["c_epl"]
          calc_data = ["c_nn","proc","c_HGe"]
}

class translation{
	<<runsection>>
	    eqvx = 0
        eqvy = 0
        eqvz = 0
        fixIDv = ["setvelocities"]
        group = ["all"]
}

class force{
	<<runsection>>
        eqfx = 0
        eqfy = 0
        eqfz = 0
        fixIDf = ["setforces"]
        group = ["all"]
}

class run{
	<<runsection>>
		runs = 50000
		}
		

initialization --o collection
collection --o integration
integration --o thermo_print
thermo_print --o equilibration
equilibration --o smddump
translation --o moves
run --o moves
translation --o moves
force --o moves
smddump --o moves

```




## Overview of top classes

The figure highlights the  dependencies between all classes. Note that several operators have been overloaded to facilitate scripting and indexing.

```mermaid
classDiagram
class raster{
	<<core>>
	width=200
	height=200
	dpi=300
	rectangle()
	circle()
	triangle()
	diamond()
	pentagon()
	hexagon()
	list()
	get()
	plot()
	show()
	label()
	unlabel()
	numeric()
	string()
	print()
	data()
	write()
}

class data{
	<<pizza>>
	title
	names
	headers
	sections
	flist
	restart
	append()
	findtime()
	map()
	reorder()
	replace()
	write()
}

class dump{
	<<pizza>>
	flist
	names
	snaps
	kind()
	type()
	maxbox()
	maxtype()
	tselect()
	aselect()
	frame()
	findtime()
	time()
	read_all()
	write()
}
	
class struct{
	<<private>>
	var=value
	generator()
	scan()
}
class param{
	<<private>>
	var=value
	eval()
	formateval()
}
class scriptdata{
	<<core>>
	var1=value1
	var2=value2
	var3=value3
}
class forcefield{
	<<core>>
	name=forcefield:style:material
	description
	beadtype
	parameters
	userid
	version
	USER
}
class script{
		<<core>>
    	DEFINITIONS
    	TEMPLATE
        USER
        +, &, *, **, |, +=
        do()
        write()
}
class scriptobject{
		<<core>>
    	beadtype
    	name
        fullname
        filename
        style
        forcefield
        group
        USER
}
class scriptobjectgroup{
		<<core>>
    	groupid
    	groupidname
        groupname
        beadtype
        name
        str
        forcefield
        script
        interactions
        select()     
}
class pipescript{
	<<core>>
	[]
	|, +, +=, *
	scripts
	script
	clear()
	rename()
	do()
	
}
data --* raster
struct --|>  param : extended
struct --* dump
param --* paramforcefield
param --|> scriptdata
param --* scriptobject
paramforcefield --* forcefield
forcefield --* scriptobject
scriptobject --|> scriptobjectgroup
scriptdata --* script
script --o pipescript
scriptobject --o pipescript
scriptobjectgroup --o pipescript
data --o dump


```

##  Output of workshop1

### LAMMPS script

```perl
# Automatic LAMMPS script (version 0.4)
# olivi@LX-Olivier2021:/home/olivi/billy/python
# ven. 18 mars 2022 19:33:50 

 

# INRAE\SAYFOOD\olivier.vitrac@agroparistech.fr
# INRAE\SAYFOOD\william.jenkinson@agroparistech.fr



#   Scheme initialization
units       si
dimension	2 
boundary    p f p         # f = fixed, p = periodic
comm_modify vel yes
comm_style  tiled
atom_modify map array
newton off
neighbor	0.0015 bin            # search radius for neighbor list (=kernel radius)
neigh_modify    every 5 delay 0 check yes

atom_style	smd
 

# ===== [ BEGIN INPUT FILES SECTION ] ===============================================================================

# load files for objects: bead 1, bead 2
	read_data ./raster_2_types.lmp

# load files for objects: bead 3, bead 4
	read_data ./raster_4_types.lmp add append

# ===== [ END INPUT FILES SECTION ] =================================================================================


# ===== [ BEGIN GROUP SECTION ] =====================================================================================

	#	Definition of group 1:rigid
	#	=bead 1
	#	Similar groups: rigid, solid
	group 	 rigid 	type 	 1

	#	Definition of group 2:solid
	#	=bead 1, bead 3, bead 4
	#	Similar groups: rigid, solid, oscillating, tlsph
	group 	 solid 	type 	 1 3 4

	#	Definition of group 3:fluid
	#	=bead 2
	#	Similar groups: fluid, ulsph
	group 	 fluid 	type 	 2

	#	Definition of group 4:ulsph
	#	=bead 2
	#	Similar groups: fluid, ulsph
	group 	 ulsph 	type 	 2

	#	Definition of group 5:oscillating
	#	=bead 3
	#	Similar groups: oscillating, solid, tlsph
	group 	 oscillating 	type 	 3

	#	Definition of group 6:tlsph
	#	=bead 3, bead 4
	#	Similar groups: oscillating, solid, tlsph
	group 	 tlsph 	type 	 3 4

# ===== [ END GROUP SECTION ] =======================================================================================


# ===== [ BEGIN FORCEFIELD SECTION ] ================================================================================
    # [1:bead 1] PAIR STYLE SMD
    pair_style      hybrid/overlay smd/ulsph *DENSITY_CONTINUITY *VELOCITY_GRADIENT *NO_GRADIENT_CORRECTION &
                                   smd/tlsph smd/hertz 1.5
    
    # [1:bead 1 x 1:bead 1] Diagonal pair coefficient tlsph
    pair_coeff      1 1 none
    
    # [2:bead 2 x 2:bead 2] Pair diagonal coefficient ulsph
    pair_coeff      2 2 smd/ulsph *COMMON 1000 100.0 1.0 1.0 0 &
                    *EOS_TAIT 7 &
                    *END
    
    # [3:bead 3 x 3:bead 3] Diagonal pair coefficient tlsph
    pair_coeff      3 3 smd/tlsph *COMMON 2000 400000000.0 0.3 1.0 0.0 10 1.0 &
                    *STRENGTH_LINEAR_PLASTIC 40000000.0 0 &
                    *EOS_LINEAR &
                    *END
    
    # [4:bead 4 x 4:bead 4] Diagonal pair coefficient tlsph
    pair_coeff      4 4 smd/tlsph *COMMON 2000 400000000.0 0.3 1.0 0.0 10 1.0 &
                    *STRENGTH_LINEAR_PLASTIC 40000000.0 0 &
                    *EOS_LINEAR &
                    *END
    
    # [1:bead 1 x 2:bead 2] Off-diagonal pair coefficient (generic)
    pair_coeff      1 2 smd/hertz 10000000
    
    # [1:bead 1 x 3:bead 3] Off-diagonal pair coefficient (generic)
    pair_coeff      1 3 smd/hertz 10000000
    
    # [2:bead 2 x 3:bead 3] Off-diagonal pair coefficient (generic)
    pair_coeff      2 3 smd/hertz 10000000
    
    # [1:bead 1 x 4:bead 4] Off-diagonal pair coefficient (generic)
    pair_coeff      1 4 smd/hertz 10000000
    
    # [2:bead 2 x 4:bead 4] Off-diagonal pair coefficient (generic)
    pair_coeff      2 4 smd/hertz 10000000
    
    # [3:bead 3 x 4:bead 4] Off-diagonal pair coefficient (generic)
    pair_coeff      3 4 smd/hertz 10000000
    
# ===== [ END FORCEFIELD SECTION ] ==================================================================================


#   Gravity
fix             gfix all gravity 9.81 vector 0 1 0
#   Time integration conditions
fix             dtfix fluid smd/adjust_dt 0.1 # dynamically adjust time increment every step
fix             integration_fix_ulsph ulsph smd/integrate_ulsph adjust_radius 1.01 10 15
fix             integration_fix_tlsph tlsph smd/integrate_tlsph
#   balancing
fix             balance_fix all balance 500 0.9 rcb


#   thermodynamic information
thermo		   100
thermo_modify  lost ignore
thermo_style   custom step dt


#   Equilibration
dump            dump_equilibrate all custom 100 dump.equilibrate id type x y z &
                fx fy fz vx vy vz radius
dump_modify     dump_equilibrate first yes

variable vmag atom sqrt(vx^2+vy^2+vz^2)
compute         maxvel all reduce max v_vmag
variable        maxvelre equal 0.6*c_maxvel
run     10000 every 1000 &
    "print ${maxvelre}" &
    "fix             ulsph_equilibration ulsph smd/integrate_ulsph limit_velocity ${maxvelre}" &
    "fix             tlsph_equilibration tlsph smd/integrate_tlsph limit_velocity ${maxvelre}"

dump_modify     dump_equilibrate every 1000000

fix             ulsph_equilibration ulsph smd/integrate_ulsph
fix             tlsph_equilibration tlsph smd/integrate_tlsph



#   Additional computed values
        
#   Compute supp particle data
compute         contact_radius all smd/contact/radius
compute         vol all smd/vol
compute         rho all smd/rho


#   dump command
dump            dump_id all custom 100 dump.workshop1 &
id type x y z mol mass c_rho c_vol radius c_contact_radius &
vx vy vz fx fy fz 
dump_modify     dump_id first yes #every/time 0.001


#   Translation
variable        vx equal 0
variable        vy equal 1
variable        vz equal 0
fix             setvelocities oscillating smd/setvel v_vx v_vy v_vz


#   run section
run 50000


#   Force
variable        fx equal 0/count(all)
variable        fy equal 0/count(all)
variable        fz equal 0/count(all)
fix             setforces all smd/setvel v_fx v_fy v_fz


#   run section
run 50000


```



###  Videos of workshop1

The videos are generated with Ovito directly from dump files.



#### Equilibration step

<video width="50%" controls="controls" preload="auto">
    <source type="video/mp4" src="https://github.com/ovitrac/Pizza3/raw/main/examples/workshop1_equilibration.mp4">
</video>


#### Run step

<video width="50%" controls="controls" preload="auto">
    <source type="video/mp4" src="https://github.com/ovitrac/Pizza3/raw/main/examples/workshop1_run.mp4">
</video>