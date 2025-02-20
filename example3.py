#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Example 3: compression of central cylinder between two others

    High-level summary:
    -------------------
    - This script uses the Pizza3 package to set up a LAMMPS geometry and input file.
    - It creates a simulation region with cylindrical subregions, assigns group objects,
      and generates scripts for SPH discretization and dynamics.
    - Finally, it writes a LAMMPS input script (in.example3) that can be used to run
      a TLSPH (Total Lagrangian Smoothed Particle Hydrodynamics) simulation.

    Dependencies:
    -------------
    - Pizza3 (https://github.com/ovitrac/Pizza3) (version 1.006 or later)
    - LAMMPS (with MachDYN / USER-SMD)

    Note:
    -----
    This script demonstrates multiple ways to use Pizza3 scripting from scratch, without relying on user libraries.
    We encourage you to save relevant sections (which are written in DSCRIPT) for easy reuse or adaptation. Several
    parts of the script utilize docstrings to define templates and default variables; there's no need to modify the
    docstrings directly since they are automatically transformed into DSCRIPT instances, each with its own local or
    global variables. Moreover, these DSCRIPT instances can be seamlessly combined with scripts, pipescripts, and
    scriptobjects.

    Usage:
    ------
    Run in a folder containing a 'tmp/' directory, or with permission to create it.

    **Key Points in the Script**
    1. Region Definition
    2. Group Objects
    3. Discretization Script (DSCRIPT)
    4. Motion / Oscillation Template
    5. Forcefield Definitions
    6. Dynamics / Integration DSCRIPT
    7. Final LAMMPS Script Assembly


    The code uses:
    --------------------------------------------------
                  56 GLOBAL DEFINITIONS
    --------------------------------------------------
    [G] dimension    [G] units        [G] boundary
    [G] atom_style   [G] atom_modif   [G] comm_modif
    [G] neigh_modi   [G] newton       [G] lattice_st
    [G] lattice_sc   [G] name         [G] xmin
    [G] xmax         [G] ymin         [G] ymax
    [G] zmin         [G] zmax         [G] nbeads
    [G] boxid        [G] boxunits_a   [G] ID
    [G] style        [G] args         [G] side
    [G] move         [G] rotate       [G] open
    [G] mass         [G] n_external   [G] n_all
    [G] n_upper      [G] n_middle     [G] n_lower
    [G] vol_one      [G] l0           [G] skin
    [G] rho          [G] h            [G] densitygrp
    [G] mOvel20      [G] mO_T         [G] mOw2
    [G] mO_fixID     [G] mO_l         [G] mOw1
    [G] mO_targetG   [G] mOvel30      [G] mOvel10
    [G] mOw3         [G] tlsphgrp     [G] dt
    [G] intgrp       [G] outputfile   [G] outstep
    [G] thermo       [G] tsim


                  and 31 TEMPLATES
   """

# %% == Initialization ==
# Import necessary modules
from pizza.region import region
from pizza.group import group, groupobject
from pizza.dscript import dscript
from pizza.forcefield import parameterforcefield, tlsphalone
from pizza.dforcefield import dforcefield

# Ensure the script is run in a directory where 'tmp/' exists or can be created
import os
# Path to the 'tmp' folder
tmp_folder = os.path.join(os.getcwd(), "tmp")
# Allow the creation of the 'tmp' folder if it does not exist
allow_create = True  # Set to False to prevent automatic creation
if not os.path.exists(tmp_folder):
    if allow_create:
        os.makedirs(tmp_folder)
        print(f"Created temporary folder: {tmp_folder}")
    else:
        raise FileNotFoundError(
            f"\n\nThe 'tmp' folder does not exist in the current directory: {os.getcwd()}. "
            "Please create the 'tmp/' subfolder manually or set `allow_create = True`.\n"
        )
else:
    print(f"\n\nUsing existing temporary folder: {tmp_folder}\n")

# %% Define Region, Lattice, Group, Preview
"""
1. **Region Definition**
   - Uses `pizza.region.region` to create a 3D simulation box with specified dimensions and boundary conditions.
   - Defines three cylindrical subregions: lower, central, and upper cylinders.
   - The result is a pipescript instance: S

      ------------:----------------------------------------
      [*]  00: script:LammpsHeaderBox:headerinit with D(10:23: 0)
      [*]  01: script:LammpsHeaderLattice:headerlattice with D( 3:23: 0)
      [*]  02: script:LammpsHeaderBox:headerbox with D(11:23: 0)
      [*]  03: script:LammpsVariables:variable with D( 3:11: 0)
      [*]  04: script:LammpsVariables:variable with D( 3:11: 0)
      [*]  05: script:LammpsVariables:variable with D( 3:11: 0)
      [*]  06: script:LammpsRegion:region with D( 9:11: 0)
      [*]  07: script:LammpsRegion:region with D( 9:11: 0)
      [*]  08: script:LammpsRegion:region with D( 9:11: 0)
      [*]  09: script:LammpsCreate:create with D( 3:11: 0)
      [*]  10: script:LammpsCreate:create with D( 3:11: 0)
      [*]  11: script:LammpsCreate:create with D( 3:11: 0)
      [*]  12: script:1+2+3:dscript with D( 0: 0: 0)
      [*]  13: script:<dscript:group:beadtype=1,2,3:mass>:collection:dscript with D( 1: 1: 0)
      [*]  14: script:<dscript:group:1+2+3:count>:variables:dscript with D( 5: 5: 0)
      [*]  15: script:<dscript:group:1+2+3:count>:printvariables:dscript with D( 5: 5: 0)
      [*]  16: script:LammpsFooterPreview:footerpreview with D( 2:23: 0)
      ------------:----------------------------------------
      pipescript containing 17 scripts with 17 executed[*]

"""

# Initialize region with global parameters
l0 = 5e-5 # m
R = region(
    name="SimulationBox",  # Simulation box name
    dimension=3,  # 3D simulation
    boundary=["p", "p", "f"],  # Fixed boundary conditions in x, y; free in z
    nbeads=3,  # Number of bead types
    width=0.008, height=0.008, depth=0.006,  # Box dimensions (meters)
    units="si",  # SI units
    regionunits="si",  # Regions defined in SI units
    lattice_scale=l0,  # Lattice scale (meters)
    lattice_style="sc",  # Simple cubic lattice
    lattice_spacing=l0,  # Lattice point spacing (meters)
    separationdistance=l0,  # Minimum separation between points
    mass=1.0  # Default mass
)

# Add cylindrical subregions
radius = 0.003 # m
z0 = R.headersData.zmin          # floor position
thickness = [0.001,0.0015,0.001] # cylinder thicknesses
spacer = [0.0005,0,0.0005]       # spacer
# Calculate start/end z-coordinates for each cylinder
zlo = [z0 + sum(spacer[:i]) + sum(thickness[: max(i-1, 0)]) for i in range(1, 4)]
zhi = [z0 + sum(spacer[:i]) + sum(thickness[:i]) for i in range(1, 4)]
# Create three cylinders in the region, each assigned a different beadtype
R.cylinder(name="LowerCylinder", dim="z", c1=0, c2=0, radius=radius, lo=zlo[0], hi=zhi[0], beadtype=1)
R.cylinder(name="CentralCylinder", dim="z", c1=0, c2=0, radius=radius, lo=zlo[1], hi=zhi[1], beadtype=2)
R.cylinder(name="UpperCylinder", dim="z", c1=0, c2=0, radius=radius, lo=zlo[2], hi=zhi[2], beadtype=3)

# Generate initialization scripts (init, lattice, box)
Rheaders = R.pscriptHeaders(what=["init", "lattice", "box"])

"""
2. **Group Objects**
   - `groupobject` instances (`g1`, `g2`, `g3`) define bead types and associated mass adjustments.
   - The combined `gcollection` manages these group objects.
"""

# Create group objects for each bead type
g1 = groupobject(beadtype=1, group='lower', mass=2.0)
g2 = groupobject(beadtype=2, group='middle')
g3 = groupobject(beadtype=3, group='upper')

# Combine group objects into a collection
gcollection = g1 + g2 + g3

# Generate a script to assign masses to bead types
Mscript = gcollection.mass(default_mass=R.mass)

# Define and evaluate groups
G = group(name="1+2+3", collection=gcollection)
G.evaluate("all", G.lower + G.middle + G.upper)
G.evaluate("tlsph",G.lower + G.middle + G.upper) # mandatory group for TLSPH
G.evaluate("external", G.all - G.middle)

# Generate script for counting atoms in groups
Ncontrol = G.count(selection=["all", "lower", "middle", "upper","external"])

# Add Preview Scripts (for visualization, if used)
Rpreview = R.pscriptHeaders(what="preview")

# Combine all scripts into a single `pipescript`
S = Rheaders | R | G | Mscript | Ncontrol | Rpreview

# Write the full LAMMPS script to a file (no verbosity)
scriptfile = S.write("tmp/example3_geometry.txt", verbosity=0, overwrite=True)
print(f"The LAMMPS geometry script is available here:\n{scriptfile}")

# %% EXAMPLE3 LIBRARY
"""
    The dscript library summarizes steps specific to SPH and TLSPH simulation.
    The library could be moved to a separate file with `dlib.save("mylibrary.d.txt")`
    and loaded with `dlib = dscript.load("mylibrary.d.txt")`.

    * Variables are assigned as `var = value` and used as `${var}`.
    * A step code block starts with `stepname: LAMMPS code`.
    * Multi-line blocks are enclosed with `[]`.
    * '!' at the beginning of the code line indicates that the variables need to be interpolated.

    DSCRIPT usage examples:
    - `mydscript = dlib("step1") + dlib("step2")*ncopies + dlib("step3","step4")`
    - Update global definitions:
        `mydscript.DEFINITIONS.var = newvalue`
        `mydscript.DEFINITIONS.update(var1=value1update, var2=value2update, ...)`
    - Update local definitions:
        `mydscript.step.definitions.var = newvalue`
        `mydscript[idx].definitions.update(var=newvalue,...)`

    The result can be displayed with `print(mydscript.do(verbose=False))`.
    - DSCRIPT instances can combine seamlessly with `scripts`, `pipescripts`, `scriptobjects`.the pipe operator `|`
        `fullscript = previsousscripts | mydscript`
    - Save the result as LAMMPS input file with
        `fullscript.write("in.lammpsinputfile",verbosity=0)`
    """

mylibrary = """
# Global attributes
{
    description = "Library for example 3",
    userid = "example3",
    verbose = False
}

# -----------------[ SPH DISCRETIZATION ]-----------------
# SPH discretization variables
l0 = 1e-5
rho = 1000 # default density (to be changed)
# SPH discretization template with !
discretization: [! # note that ! ==> eval=True
variable        h equal 2.5*${l0} # SPH kernel diameter
variable        vol_one equal ${l0}^3 # initial particle volume (rough)
set             group all diameter ${h}
set             group all smd/contact/radius ${l0}
set             group all volume  ${vol_one}
set             group all smd/mass/density ${rho}
variable        contact_scale equal 1.5 # scale factor to increase contact gap between bodies
variable        skin equal ${h} # Verlet list range
neighbor        ${skin} bin
]
# SPH density variables
densitygrp = mygroup # to be set by the end-user
# SPH density template
density: !set             group ${densitygrp} smd/mass/density ${rho}

# -----------------[ MOVE TEMPLATE ]-----------------
# Oscillation parameters: mO_l, mO_T with i=1,2,3
mO_l = [0,1e-3,0]    # maximum displacement along dimension 1,2,3
mO_T = [0.5,0.5,0.5] # period for motion along dimension 1,2,3
# Fix parameters
mO_targetGRP = "$oscillableatoms" # group ID to be set by user
mO_fixID = "$mOfix"               # internal fix ID
# Oscillation template  (keep flag ! =evaluate)
oscillation: [!
    # Angular frequencies (pulsations) of oscillations (LAMMPS variables)
    variable mOw1 equal 2*PI/${mO_T[0]}  # Pulsation for motion along 1
    variable mOw2 equal 2*PI/${mO_T[1]}  # Pulsation for motion along 2
    variable mOw3 equal 2*PI/${mO_T[2]}  # Pulsation for motion along 3
    # Maximum velocities of oscillations (LAMMPS variables)
    variable mOvel10 equal ${mO_l[0]}*PI/${mO_T[0]}  # Max velocity along 1
    variable mOvel20 equal ${mO_l[1]}*PI/${mO_T[1]}  # Max velocity along 2
    variable mOvel30 equal ${mO_l[2]}*PI/${mO_T[2]}  # Max velocity along 3
    # Define sinusoidal velocity components as functions of time (oscillations)
    variable mOvel1 atom ${mOvel10}*sin(${mOw1}*time)
    variable mOvel2 atom ${mOvel20}*sin(${mOw2}*time)
    variable mOvel3 atom ${mOvel30}*sin(${mOw3}*time)
    # Add oscillations
    fix ${mO_fixID} ${mO_targetGRP} smd/setvel v_mOvel1 v_mOvel2 v_mOvel3
    ]

# -----------------[ DYNAMICS ]-----------------

# Integration parameters
dt = 0.1
tlsphgrp = tlsph # it is mandatory to have TLSPH particles part of a group TLSPH
intgrp = group
outstep = 1
outputfile = dump.mydump
thermo = 100
tsim = 1000
# Stepping Template
stepping: [!
fix             dtfix ${tlsphgrp} smd/adjust_dt ${dt} # dynamically adjust time increment every step
]
integration: !fix             intfix_${intgrp} ${intgrp} smd/integrate_tlsph
# Compute template
compute: [
compute         eint all smd/internal/energy
compute         contact_radius all smd/contact/radius
compute         S all smd/tlsph/stress
compute         epl all smd/plastic/strain
compute         vol all smd/vol
compute         rho all smd/rho
]
# Dump template
dump: [!
dump            dump_id all custom ${outstep} ${outputfile} id type x y &
                fx fy vx vy c_eint c_contact_radius mol &
                c_S[1] c_S[2] c_S[4] mass radius c_epl c_vol c_rho proc
dump_modify     dump_id first yes
]
status: [!
compute         alleint all reduce sum c_eint
variable        etot equal pe+ke+c_alleint # total energy of the system
thermo          ${thermo}
thermo_style    custom step ke pe v_etot c_alleint f_dtfix dt
thermo_modify   lost ignore
]
# balance template
balance: [!
#fix             balance_fix all balance 500 0.9 rcb # load balancing for MPI
fix              balance_fix all balance 500 0.9 shift
]
# run template
run: [!
run             ${tsim}
]
"""

# parse the library
dlib = dscript.parsesyntax(mylibrary,name="example3",authentification=False)

# %% SPH DISCRETIZATION
"""
3. **Discretization Script (DSCRIPT)**
   - `SPH_discretization_template` sets basic SPH parameters (kernel diameter, volume).
   - Dynamically adjusts densities for lower, middle, and upper cylinders via `D["densities"]`.
   - The result is a dscript instance: D

    --------------------------------------------------
               with 6 GLOBAL DEFINITIONS
    --------------------------------------------------
    [G] vol_one      [G] l0           [G] skin
    [G] rho          [G] h            [G] densitygrp

                  and with 4 TEMPLATES

    --------------------------------------------------
    <<<<<<<|  idx: 0 |  key: discretrization  |>>>>>>>
    --------------------------------------------------
    <<<<<<<<<<|  idx: 3 |  key: density1  |>>>>>>>>>>
    --------------------------------------------------
    <<<<<<<<<<|  idx: 3 |  key: density2  |>>>>>>>>>>
    --------------------------------------------------
    <<<<<<<<<<|  idx: 3 |  key: density3  |>>>>>>>>>>
    -------------------------------------------------

"""

# User defintions
rho = [1050, 1000, 1300]  # densities of each cylinder in kg/m3

# List the objects to be discretized
objects = gcollection.list()
nobjects =len(objects)

# call dlib with proper codelet names
# we need as many density codelets as the number of objects
D = dlib("discretization")+dlib("density")*nobjects

# we update the defintions
D.DEFINITIONS.l0 = l0 # update l0 globally
for iobj in range(nobjects): # update density locally
    D[iobj+1].definitions.update(rho=rho[iobj],densitygrp=objects[iobj])

# Control
print("\n== SPH Discretization ==\n",D.do(verbose=False))

# %% MOVE
"""
4. **Motion / Oscillation Template**
   - `MOVE_oscillation_template` defines parameters to create a sinusoidal motion or velocity boundary condition in one dimension.
   - The result is a dscript instance: T

    --------------------------------------------------
               with 10 GLOBAL DEFINITIONS
    --------------------------------------------------
    [G] mOvel20      [G] mO_T         [G] mOw2
    [G] mO_fixID     [G] mO_l         [G] mOw1
    [G] mO_targetG   [G] mOvel30      [G] mOvel10
    [G] mOw3

                   and with 1 TEMPLATE

"""

# User definitions
maxcompression = 0.1  # for central cylinder
maxstrainrate = 1     # in 1/s

# we retrieve the very generic oscillation template
T = dlib("oscillation")

# we update definitions
inf = 1e20 # large number to simulate 'infinity' for LAMMPS
lmax = spacer[2]+maxcompression*thickness[1]
tmax = 2 * lmax / (maxstrainrate * lmax)
T.DEFINITIONS.mO_l = [0,0,lmax] # maximum displacement
T.DEFINITIONS.mO_T = [inf,inf,tmax]
T.DEFINITIONS.mO_targetGRP = "upper"

print("\n== Move ==\n",T.do(verbose=False))

# %% FORCEFIELDS
"""
5. **Forcefield Definitions**
   - The `FFbase` is created using `parameterforcefield` for a TLSPH model, then copied with modifications for each cylinder’s different material properties.
   - The result is a scriptobject group: bcollection

          -------------:----------------------------------------
             lowerAtoms: script object | type=1 | name=lowerAtoms
           centralAtoms: script object | type [...]  | name=centralAtoms
             upperAtoms: script object | type=3 | name=upperAtoms
          -------------:----------------------------------------
             script object group (SOG object) with 3 objects

"""

# Create a default forcefield using `parameterforcefield` and `dforcefield`.
FFbase_parameters = parameterforcefield(
    base_class=tlsphalone,    # Forcefield class: Total Lagrangian Smoothed Particle Hydrodynamics
    rho=1050,                 # Density
    c0=10.0,                  # Speed of sound
    E="50*${c0}^2*${rho}",    # Elastic modulus
    nu=0.3,                   # Poisson's ratio
    q1=1.0, q2=0.0,           # Artificial viscosity parameters
    Hg=10.0, Cp=1.0,          # Heat capacity and specific energy
    sigma_yield="0.1*${E}",   # Yield stress
    hardening=0,              # Hardening coefficient
    contact_scale=1.5,        # Contact scale
    contact_stiffness="2.5*${c0}^2*${rho}"  # Contact stiffness
)
FFbase = dforcefield(userid="FFbase", **FFbase_parameters)

# DEFINE REGION-SPECIFIC FORCEFIELDS
FFlower = FFbase.copy(
    beadtype=R.LowerCylinder.beadtype,  # Assign bead type
    userid="LowerCylinder",             # Unique identifier
    E="2*"+FFbase.parameters.E,         # Increase elastic modulus
    rho=rho[0]                          # Same density as base
)

FFcentral = FFbase.copy(
    beadtype=R.CentralCylinder.beadtype,
    userid="CentralCylinder",
    E="0.5*"+FFbase.parameters.E,
    rho=rho[1]                          # Reduced density
)

FFupper = FFbase.copy(
    beadtype=R.UpperCylinder.beadtype,
    userid="UpperCylinder",
    E="10*"+FFbase.parameters.E,        # Much stiffer material
    rho=rho[2], nu=0.1                  # Higher density, lower Poisson's ratio
)

# ASSIGN FORCEFIELDS TO GROUPS
blower = FFlower.scriptobject(name="lowerAtoms", group="lowerAtoms")
bcentral = FFcentral.scriptobject(name="centralAtoms", group="centralAtoms")
bupper = FFupper.scriptobject(name="upperAtoms", group="upperAtoms")

# Combine all forcefield group scripts into a single collection
bcollection = blower + bcentral + bupper

# control
print("\n== FF ==\n",bcollection.script().do(verbose=False))

# %% Integration, compute, dump, status and run
"""
6. **Dynamics / Integration DSCRIPT**
   - Merges multiple DSCRIPT templates (integration, compute, dump, status, run) into one via string joining.
   - Uses `fix smd/adjust_dt` for dynamic time-step control.
   - Uses `fix smd/integrate_tlsph` for TLSPH integration in each group.
   - The result is a dscript instance: I

    --------------------------------------------------
               with 7 GLOBAL DEFINITIONS
    --------------------------------------------------
    [G] tlsphgrp     [G] dt           [G] intgrp
    [G] outputfile   [G] outstep      [G] thermo
    [G] tsim


                  and with 8 TEMPLATES

    --------------------------------------------------
    <<<<<<<<<<|  idx: 0 |  key: stepping  |>>>>>>>>>>
    --------------------------------------------------
    <<<<<<<<|  idx: 1 |  key: integration1  |>>>>>>>>
    --------------------------------------------------
    <<<<<<<<|  idx: 2 |  key: integration2  |>>>>>>>>
    --------------------------------------------------
    <<<<<<<<|  idx: 3 |  key: integration3  |>>>>>>>>
    --------------------------------------------------
    <<<<<<<<<<<|  idx: 4 |  key: compute  |>>>>>>>>>>>
    --------------------------------------------------
    <<<<<<<<<<<<|  idx: 5 |  key: dump  |>>>>>>>>>>>>
    --------------------------------------------------
    <<<<<<<<<<<|  idx: 6 |  key: status  |>>>>>>>>>>>
    --------------------------------------------------
    <<<<<<<<<<<<<|  idx: 7 |  key: run  |>>>>>>>>>>>>>

"""

# User definitions
dt = 0.1        # time step
outstep = 10    # output frequency
outputfile = "dump.example3"
thermo = 100    # thermodynamic output frequency
tsim = 10000    # total simulation steps

# We retrieve the codelets, integration (x3), compute, dump, status, run
I = dlib("stepping")+dlib("integration")*nobjects+dlib("compute","dump","status","run")

# We update locally the name of the group for integration step
for iobj in range(nobjects): # update density locally
    I[iobj+1].definitions.intgrp = objects[iobj]


# We update the other definitions as global variables
I.DEFINITIONS.update(dt=dt,
                     outstep=outstep,
                     outputfile=outputfile,
                     tlsphgrp = "tlsph",
                     thermo=thermo,
                     tsim=tsim)
print("\n== Dynamics ==\n",I.do(verbose=False))

# %% Full Assembly
"""
7. **Final LAMMPS Script Assembly**
   - Pipes together geometry, discretization, motion, forcefields, and dynamics scripts.
   - Writes final input to `"tmp/in.example3"` for direct use in LAMMPS.
   - The result is a pipescript instance: S1

  ------------:----------------------------------------
  [*]  00: script:LammpsHeaderBox:headerinit with D(10:23: 0)
  [*]  01: script:LammpsHeaderLattice:headerlattice with D( 3:23: 0)
  [*]  02: script:LammpsHeaderBox:headerbox with D(11:23: 0)
  [*]  03: script:LammpsVariables:variable with D( 3:11: 0)
  [*]  04: script:LammpsVariables:variable with D( 3:11: 0)
  [*]  05: script:LammpsVariables:variable with D( 3:11: 0)
  [*]  06: script:LammpsRegion:region with D( 9:11: 0)
  [*]  07: script:LammpsRegion:region with D( 9:11: 0)
  [*]  08: script:LammpsRegion:region with D( 9:11: 0)
  [*]  09: script:LammpsCreate:create with D( 3:11: 0)
  [*]  10: script:LammpsCreate:create with D( 3:11: 0)
  [*]  11: script:LammpsCreate:create with D( 3:11: 0)
  [*]  12: script:1+2+3:dscript with D( 0: 0: 0)
  [*]  13: script:<dscript:group:beadtype=1,2,3:mass>:collection:dscript with D( 1: 1: 0)
  [*]  14: script:<dscript:group:1+2+3:count>:variables:dscript with D( 5: 5: 0)
  [*]  15: script:<dscript:group:1+2+3:count>:printvariables:dscript with D( 5: 5: 0)
  [*]  16: script:LammpsFooterPreview:footerpreview with D( 2:23: 0)
  [*]  17: script:example3_subobject+example3_subobject*3:discretization:dscript with D( 6: 6: 0)
  [*]  18: script:example3_subobject+example3_subobject*3:density1:dscript with D( 6: 6: 0)
  [*]  19: script:example3_subobject+example3_subobject*3:density2:dscript with D( 6: 6: 0)
  [*]  20: script:example3_subobject+example3_subobject*3:density3:dscript with D( 6: 6: 0)
  [*]  21: script:example3_subobject:oscillation:example3 with D(10:10: 0)
  [*]  22: script:scriptobject script:scriptobject with D( 0: 0: 0)
  [*]  23: script:example3_subobject+example3_subobject*3+example3_subobject:stepping:dscript with D( 7: 7: 0)
  [*]  24: script:example3_subobject+example3_subobject*3+example3_subobject:integration1:dscript with D( 7: 7: 0)
  [*]  25: script:example3_subobject+example3_subobject*3+example3_subobject:integration2:dscript with D( 7: 7: 0)
  [*]  26: script:example3_subobject+example3_subobject*3+example3_subobject:integration3:dscript with D( 7: 7: 0)
  [*]  27: script:example3_subobject+example3_subobject*3+example3_subobject:compute:dscript with D( 7: 7: 0)
  [*]  28: script:example3_subobject+example3_subobject*3+example3_subobject:dump:dscript with D( 7: 7: 0)
  [*]  29: script:example3_subobject+example3_subobject*3+example3_subobject:status:dscript with D( 7: 7: 0)
  [*]  30: script:example3_subobject+example3_subobject*3+example3_subobject:run:dscript with D( 7: 7: 0)
  ------------:----------------------------------------
  pipescript containing 31 scripts with 31 executed[*]

"""

# Use S[:-1] to omit the last pipe from 'S' to chain without the geometry control
S1 = S | D | T | bcollection | I

# Write the updated LAMMPS script to a file (verbosity=0 remove comments)
updatedScriptfile = S1.write("tmp/in.example3", verbosity=0, overwrite=True)
print(f"The input LAMMPS file is available here:\n{updatedScriptfile}")
