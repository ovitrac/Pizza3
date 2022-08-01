# Pizza3 #

> Contributors:
>
> ​	INRAE\Olivier Vitrac, E-mail: [olivier.vitrac@agroparistech.fr](olivier.vitrac@agroparistech.fr) (main contact)
>
> ​	INRAE\William Jenkinson, E-mail: [william.jenkinson@agroparistech.fr](olivier.vitrac@agroparistech.fr)
>
> ​	INRAE\Pei Sun, E-mail: [pei.sun@agroparistech.fr](olivier.vitrac@agroparistech.fr)
>
> $ 2022-08-01 $

*Click [here](https://htmlpreview.github.io/?https://raw.githubusercontent.com/ovitrac/Pizza3/main/README.html) to read this file in HTML (including with videos)*

[TOC]

##  Scope

<kbd>Pizza3</kbd> is a fork and an extension of Pizza.py toolkit for [LAMMPS](https://www.lammps.org/) witten in Python 3.x, whereas the original `Pizza.py` has been written in Python 2.x. <kbd>Pizza3</kbd> should be seen as loosely integrated collection of tools for  [LAMMPS](https://www.lammps.org/)  regardless the considered style. Our main goal is to achieve a set of tools facilitating multiscale modeling in LAMMPS: the connection of results obtained at different scales with different levels of coarse graining or details.

>  The most important achievements are discussed hereafter. *The work is in progress, come back regularly.*



## Overview

Main scripts and classes are shown here. The demonstrations of implemented features are available as "==workshops==" (currently 0 = draft, 1=first workable, 2=first production). <kbd>Pizza3</kbd> is fully object-oriented and use a universal container a structure à la Matlab with self-evaluating capabilities (`param()`) or not (`pizza.private.struct()`). The design capabilities will remain limited in <kbd>Pizza3</kbd> but a set of methods are proposed in `pizza.raster()` to allow the testing of 2D algorithms with a much lower computational cost than in 3D without a loss of generality. 



>The class `pizza.script()` is the main class to code in [LAMMPS](https://www.lammps.org/) from *codelets* written in Python.  *Codelets* are essential for our purpose of multiscale modeling. They parse and interpret [LAMMPS](https://www.lammps.org/) codes, so-called `TEMPLATES`, without importing them in LAMMPS either in real or deferred time. *Codelet* instances offer static, global and local variables, so-called `DEFINITIONS`, which facilitate the chaining of instructions (*e.g.*, programmed displacements, forcefield definitions) and the conversion from one style to the other. The static interpreter reorders mathematical expressions and definitions to make them executable.

Input and output [LAMMPS](https://www.lammps.org/) data are managed as `pizza.data()` and `pizza.dump()` original objects. New methods extend original capabilities to facilitate the manipulation of frames, the conversion of outputs to inputs (equivalent restart files).

> Forcefields are specific to each style and are manipulated through the concept of inheritance. A user library of forcefields can be set by overriding existing definitions. It is recommended to implement user rules with the class `pizza.generic()` (follows ) . 



**Table 1**. Overview of classes

| Workshops<br> (workable demonstrations) |             **Main classes<br/>and subclasses**              |                    Low-level<br/> classes                    |
| :-------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
|          class: ==workshop1==           |                2D drawing class: pizza.raster                |    generic struct class à la Matlab: pizza.private.struct    |
|          class: ==workshop2==           | as above (with exemplification of advanced features, incl. time-steps, region of interest and salting selection |                           as above                           |
|            script: geometry             |      class to read/write input files: pizza.data3.data       | self-evaluable struct with scripting/alias features: pizza.private.param |
|            script: assembly             |         class to manage dump files: pizza.dump3.dump         |                                                              |
|                                         | advanced scripting classes: pizza.script.script, pizza.script.datascript, pizza.script.scriptobject, pizza.script.scriptobjectgroup, pizza.script.pipescript |                                                              |
|                                         | forcefield classes: pizza.forcefield.forcefield, pizza.forcefield.smd, pizza.forcefield.tlsph, pizza.forcefield.ulsph, pizza.forcefield.none, pizza.forcefield.water, pizza.forcefield.solidfood, pizza.forcefield.rigidwall |                                                              |

## Key steps

Workshop1 illustrates the main steps to design, run and analyze a LAMMPS project from Python 3.x.

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



###  Videos from workshop1

The videos are generated with Ovito directly from dump files.



#### Equilibration step

<video width="50%" controls="controls" preload="auto">
    <source type="video/mp4" src="https://github.com/ovitrac/Pizza3/raw/main/examples/workshop1_equilibration.mp4">
</video>


#### Run step

<video width="50%" controls="controls" preload="auto">
    <source type="video/mp4" src="https://github.com/ovitrac/Pizza3/raw/main/examples/workshop1_run.mp4">
</video>


## Extensions offered by workshop2

### Scope

Workshop 2 addresses several issues and improve the user experience (better commenting, documentation, certain improvements to the intuition) and elaborates specific aspects of the pipeline. New features include

1. Inputs set from microscopic images
2. Setting time-step,  salting
3.  two examples (squeeze case and shearing case)

> With workshop 2, more complex systems should be achievable to the user including the use of "*sensing*" surfaces and better control of system parameters such as viscosity.



### New classes and updates

A few classes have been updated/improved to be more usable and funcitonal, and two new classes have been created; file and group. Both these classes give additional methods of creating groups in lammps to suppliment the use of the intereactions class.

#### workshop2.file

The *file* class can be used to read the files, and it is a new method of creating a group. If you want all the atoms in your file to be part of a group, use the arguments group=True and specify an ID for them with group_name = "your_group_name"

Example:

```PYTHON
files = file(file_name=["./file1"],group=True,group_name=["sensor"]) & \
        file(file_name=["./file2"],group=True,group_name=["substance"], append = True)
```

N.B. for subsequent files, if you want to preserve the files already uploaded use append=True

#### workshop2.group

The group class can create new groups from an input of arguments to specify a sub-domain of the simulation. You have four arguments; x = [x1 x2], x = [x1 x2], x = [x1 x2] and groupID="sensor".

Example:

```PYTHON
groups = group(groupID = ['bottom'], y=['EDGE',0.2])
```

By default, all spatial arguments are 'EDGE' which means the edge of the domain box.

### Improvements and updates

#### workshop2.equilibrate

- by default, tlsph object are frozen but using static='yourgroup', an group of atoms can be frozen
- equilibrate is simplified, periodically all velocities in the simulation are set to 0 in order to remove the kinetic energy from the system, it= can be used to specify the number of such cycles

#### workshop2.translation/force

- bugs in the translation and force classes resolved
- names can be specified case-by-case and multiple actions can be performed

### Examples

#### squeeze_flow

A block of fluid is squeezed between two surfaces, the lower surface is "sensory" and detects stresses



<img src="tmp/workshop2/images/squeezing.png" style="zoom:33%;" /><img src="https://github.com/ovitrac/Pizza3/raw/main/examples/squeezing_salted.png" style="zoom:33%;" />





#### shear_flow

<img src="https://github.com/ovitrac/Pizza3/raw/main/examples/shearing.png" style="zoom:33%;" />



## pizza.raster()

Raster is a 2D space-filling model for very coarse-grained systems. The code has been written in such a way as to allow an easy generalization in 3D: only the concept of convex hull must be added.

```python
from pizza.raster import raster, emulsion, coreshell
```



### Principle to generate input data

The example creates simple objects with different shapes and bead types.

<img src="https://github.com/ovitrac/Pizza3/raw/main/examples/raster01.png" style="zoom:33%;" />

```python
# drawing area
R = raster()
# rectangle shapes
R.rectangle(1,24,2,20,name='rect1')
R.rectangle(60,80,50,81,
            name='rect2',beadtype=2,angle=40)
R.rectangle(50,50,10,10,
                mode="center",angle=45,beadtype=1)
# circules and ellipses
R.circle(45,20,5,name='C1',beadtype=3)
R.circle(35,10,5,name='C2',beadtype=3) R.circle(15,30,10,
 name='p1',beadtype=4,shaperatio=0.2,angle=-30)
R.circle(12,40,8,
 name='p2',beadtype=4,shaperatio=0.2,angle=20)   R.circle(12,80,22,name='p3',beadtype=4,shaperatio=1.3,angle=20)
# other polygons
R.triangle(85,20,10,name='T1',beadtype=5,angle=20)
R.diamond(85,35,5,name='D1',beadtype=5,angle=20)
R.pentagon(50,35,5,name='P1',beadtype=5,angle=90)
R.hexagon(47,85,12,name='H1',beadtype=5,angle=90)
# labels and first plot
R.label("rect003")
R.plot()
R.list()
R.show()
# refresh with all labels except one
R.clear()
R.plot()
R.show(extra="label")
R.label("rect003")
R.unlabel('rect1')
# generate and write the corresponding pizza.data() object
X=R.data()
X.write("tmp/example.lmp") # scaling is available
```



### Duplicate and replicate objects along a path

Geometry objects can be copied between `pizza.raster()` objects and copied along arbitrary paths or coordinates.

<img src="https://github.com/ovitrac/Pizza3/raw/main/examples/raster02.png" style="zoom:33%;" />

```python
# source
draft = raster()
draft.rectangle(1,24,2,20,name='rect1'),
draft.circle(10,10,2,name="X",beadtype=4)
# copy an entire raster to the collection "C1"
A = raster()
A.collection(draft,name="C1",beadtype=1,translate=[10,30])
# copy along a path "PX"
B = raster()
B.copyalongpath(draft.X,name="PX",beadtype=2,
                    path=arc,
                     xmin=10,
                     ymin=10,
                     xmax=90,
                     ymax=50,
                        n=12)
B.plot()
B.show(extra="label")
```



### Customized classes

Customized classes facilitate the construction of the collection of objects and can be inserted in `pizza.raster() ` instances.



#### Create a suspension/emulsion with different species

<img src="https://github.com/ovitrac/Pizza3/raw/main/examples/raster03.png" style="zoom:33%;" />

```python
# generate the suspension/emulsion object with multiple random insertions by indicating the radius of the object
e = emulsion(xmin=10, ymin=10, xmax=390, ymax=390)
e.insertion([60,50,40,30,20,15,15,10,8,20,12,8,6,4,11,13],beadtype=1)
e.insertion([30,10,20,2,4,5,5,10,12,20,25,12,14,16,17],beadtype=2)
e.insertion([40,2,8,6,6,5,5,2,3,4,4,4,4,4,10,16,12,14,13],beadtype=3)
# generate the corresponing raster
C = raster(width=400,height=400)
C.scatter(e,name="emulsion")
C.plot()
C.show()
```



#### Create a suspension of core-shell particles

<img src="https://github.com/ovitrac/Pizza3/raw/main/examples/raster04.png" style="zoom:33%;" />

```python
# generate the core-shell model
cs = coreshell(xmin=10, ymin=10, xmax=390, ymax=390)
cs.insertion([60,50,40,30,20,15,15,10,8,20,12,8,11,13],beadtype=(1,2),thickness = 4)
# generate the corresponding raster
D = raster(width=400,height=400)
D.scatter(cs,name="core-shell")
D.plot()
D.show()
```



## pizza.forcefield()

Forcefields are essential, but complex to setup. The class `pizza.forcefield()` facilitate their design and use via libraries.

```python
from pizza.forcefield import *
```



```python
# basic examples from user library
w = water(beadtype=1, userid="fluid")
w.parameters.Cp = 20
print("\n"*2,w)
f = solidfood(beadtype=2, userid="elastic")
print("\n"*2,f)
r = rigidwall(beadtype=3, userid="wall")
print("\n"*2,r)
```



`Example of output for r`



```perl
============================ [ wall | version=0.1 ] ============================

  Bead of type 3 = [LAMMPS:SMD:none:walls]
forcefield (FF object) with 4 parameters

............................... [ description ] ................................

	# 	LAMMPS:SMD - solid, liquid, rigid forcefields (continuum mechanics)
	# 	no interactions
	# 	rigid walls

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ [ methods ] ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

replace FFi,FFj by your variable names <<<
	To assign a type, use: FFi.beadtype = integer value
	Use the methods FFi.pair_style() and FFi.pair_coeff(FFj)
	Note for pairs: the caller object is i (FFi), the argument is j (FFj or j)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ [ template ] ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    # [3:wall] PAIR STYLE SMD
    pair_style      hybrid/overlay smd/ulsph *DENSITY_CONTINUITY *VELOCITY_GRADIENT *NO_GRADIENT_CORRECTION &
                                   smd/tlsph smd/hertz 1.5
    

    # [3:wall x 3:wall] Diagonal pair coefficient tlsph
    pair_coeff      3 3 none
    

    # [3:wall x 2:none] Off-diagonal pair coefficient (generic)
    pair_coeff      2 3 smd/hertz 750000.0
    

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
```



## pizza.script.script(), pizza.script.pipescript()

`pizza.script()` is the Swiss knife of <kbd>Pizza3</kbd>.

```python
from pizza.script import *
```



| classes               | description                     | overloaded operators and attributes                          |
| --------------------- | ------------------------------- | ------------------------------------------------------------ |
| `scriptdata()`        | variable space: $s.variable$    | $s_{12}=s_1+s_2$<br />$s_1+=s_2$<br />$s_1=s_{12}-s_2$<br />$s.variable=value$<br />$s.variable=[]$<br />$s[0]$<br />$s[-1]$ |
| `scriptobject()`      | "bead" object: $b_i$            | `name="bead name", group=["group1","group2"], filename="input_filename.lmp", forcefield=forcefield_class` <br />$C=b_1+b_2+...$<br />$b_2>b_1$ |
| `scriptobjectgroup()` | collection of beads: $C_k$      | `select(),group(), interactions(), forcefield(), script`<br />$C=C_1+C_2$<br />$P=C_1|C_2$ |
| `script()`            | script object: $S_k$            | $S(...,USER=s)$<br />`do(),write()`<br />Immediate execution: $S_{12}=S(context1)\& S(context2)$<br />Differed execution: $S_{12}=S_1+ S_2$<br />$S_{123}=S_1+ S_2*2+S_3*3$ /> |
| `pipescript()`        | pipescript object: $P_k$, $Q_k$ | `do(),script,clear,rename()`<br />$P=P_0|C_0|S_1|S_2|S_3$<br />$P_{12}=P_1+P_2*2$<br />$P[0:1]=Q[0:1]$<br />$Q = p[[2,0,1,1,2]]$<br />$Q.do([0,1,4,3])$<br />$P.USER[0].a=1$<br />$P.scripts[0].USER.a=10$ |



## pizza.data3.data(), pizza.dump3.dump()

The objects `data()` and `dump()` are partly compatible and can be used alone or together.



```python
# input data objects and methods
from pizza.data3 import data
# dump objects and methods
from pizza.dump3 import dump
```



```python
# basic example, see documentation for details
datafile = "../data/play_data/data.play.lmp"
X = data(datafile)
Y = dump("../data/play_data/dump.play.restartme")
t = Y.time()
step = 2000
R = data(Y,step)
R.write("../tmp/data.myfirstrestart.lmp")
```

