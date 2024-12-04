# -*- coding: utf-8 -*-
"""
This example demonstrates how to programmatically generate 3D geometries and manage atoms in LAMMPS 
using the Pizza3 toolkit. It highlights the use of `pizza.region` and `pizza.group` classes for 
defining simulation regions and managing groups.

Specifically, this script:
1. Initializes a LAMMPS simulation with fixed boundaries and small spatial discretization.
2. Defines a simulation box in SI units with lattice-based discretization.
3. Creates cylindrical regions to represent subdomains within the simulation box.
4. Assigns atom types, groups, and masses, and verifies the number of atoms created.
5. Outputs the simulation geometry for visualization and debugging.
6. Generates equivalent DSCRIPT code for dynamic reusability and flexibility.

# Key Features of the Example:
- Demonstrates flexible region definitions using Pizza3's `region` class.
- Shows group arithmetic and dynamic group management with `group` and `groupobject`.
- Produces both LAMMPS scripts and DSCRIPT files for interoperability and modularity.

Created on Tue Nov 26, 2024
Author: olivi

last revision: 2024-12-04
"""

# Dependencies
from pizza.script import pipescript, script, scriptdata  # Base script and data structure classes
from pizza.dscript import dscript  # Dynamic script class for managing LAMMPS inputs
from pizza.group import group, groupobject  # Group management for atoms or molecules
from pizza.region import region  # Region class to define physical simulation regions
from pizza.dforcefield import dforcefield  # Dynamic forcefield for particles
from pizza.generic import generic  # Generic forcefield module

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



# %% Define Region and Lattice

# Initialize region with global parameters
R = region(
    name="SimulationBox",  # Simulation box name
    dimension=3,  # 3D simulation
    boundary=["f", "f", "f"],  # Fixed boundary conditions
    nbeads=3,  # Number of bead types
    width=0.08, height=0.08, depth=0.06,  # Box dimensions (meters)
    units="si",  # SI units
    regionunits="si",  # Regions defined in SI units
    lattice_scale=0.001,  # Lattice scale (meters)
    lattice_style="sc",  # Simple cubic lattice
    lattice_spacing=0.001,  # Lattice point spacing (meters)
    separationdistance=0.001,  # Minimum separation between points
    mass=1.0  # Default mass
)

# Add cylindrical subregions
R.cylinder(name="LowerCylinder", dim="z", c1=0, c2=0, radius=0.03, lo=-0.03, hi=-0.01, beadtype=1)
R.cylinder(name="CentralCylinder", dim="z", c1=0, c2=0, radius=0.03, lo=-0.01, hi=0.01, beadtype=2)
R.cylinder(name="UpperCylinder", dim="z", c1=0, c2=0, radius=0.03, lo=0.01, hi=0.03, beadtype=3)

# Generate initialization scripts
Rheaders = R.pscriptHeaders(what=["init", "lattice", "box"])

# %% Define Groups

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
G.evaluate("external", G.all - G.middle)

# Generate script for counting atoms in groups
Ncontrol = G.count(selection=["all", "lower", "middle", "upper"])

# %% Add Preview Scripts

Rpreview = R.pscriptHeaders(what="preview")

# %% Assemble the Full Script

# Combine all scripts into a single `pipescript`
S = Rheaders | R | G | Mscript | Ncontrol | Rpreview

# Write the full LAMMPS script to a file
scriptfile = S.write("tmp/example2.txt", verbosity=1, overwrite=True)
print(f"The LAMMPS script is available here:\n{scriptfile}")

# %% Generate DSCRIPT Code

# Convert the LAMMPS script to a DSCRIPT for dynamic reuse
D = S.dscript(verbose=True)
dscriptfile = D.save("tmp/example2.d.txt", overwrite=True)
print(f"The DSCRIPT is available here:\n{dscriptfile}")

# %% Verify Reversibility

# Load the DSCRIPT file and regenerate the LAMMPS script (without comments)
Dreverse = dscript.load(dscriptfile)
Sreverse = Dreverse.pipescript(verbose=False)
print("\n\n# Reverse LAMMPS code (from disk)", Sreverse.do(verbose=False), sep="\n")


# %% LAMMPS CODE
"""
# -------------------------------- [ LAMMPS CODE ] --------------------------------
# Initialize simulation
dimension    3
units        si
boundary     f f f
atom_style   smd
atom_modify  map array
comm_modify  vel yes
neigh_modify every 10 delay 0 check yes
newton       off

# Define finer lattice for better discretization
lattice sc 0.001

# Define simulation box in SI units
region box block -0.04 0.04 -0.04 0.04 -0.03 0.03 units box
create_box 3 box

# Define cylinder regions within the simulation box, using SI units
region LowerCylinder cylinder z 0.0 0.0 0.03 -0.03 -0.01 units box
region CentralCylinder cylinder z 0.0 0.0 0.03 -0.01 0.01 units box
region UpperCylinder cylinder z 0.0 0.0 0.03 0.01 0.03 units box

# Create atoms in each region
create_atoms 1 region LowerCylinder
create_atoms 2 region CentralCylinder
create_atoms 3 region UpperCylinder

# Group definitions
group lower type 1
group middle type 2
group upper type 3
group all union lower middle upper
group external subtract all middle

# Assign masses (required even if dynamics are not performed)
mass 1 2.0
mass 2 1.0
mass 3 1.0

# Verify the number of atoms created
variable n_all equal "count(all)"
variable n_lower equal "count(lower)"
variable n_middle equal "count(middle)"
variable n_upper equal "count(upper)"
print "Number of atoms in all: ${n_all}"
print "Number of atoms in lower: ${n_lower}"
print "Number of atoms in middle: ${n_middle}"
print "Number of atoms in upper: ${n_upper}"

# Output the initial geometry to a dump file for visualization
dump initial_dump all custom 1 dump.initial_geometry id type x y z
run 0
# -------------------------------- [ END ] --------------------------------
"""


# %% DSCRIPT FILE OUTPUT
"""
### DSCRIPT SAVE FILE Structure and Syntax

The **DSCRIPT SAVE FILE** is a modular and flexible representation of LAMMPS scripts, supporting reverse generation 
and easy integration into workflows. Below is a detailed explanation of its structure:

---

#### 0. Header
The header provides metadata about the DSCRIPT file:
- **Version**: DSCRIPT version used to generate the file.
- **License**: Licensing information for the script.
- **Email**: Contact email for the script author or maintainer.
- **Name**: The name of the DSCRIPT object.
- **Path**: Filepath where the DSCRIPT is saved (optional; excluded if `filepath=None`).
- **Generation Details**: Includes the user, hostname, current directory, and timestamp.


#### 1. Global Parameters
This section stores key-value pairs defining the DSCRIPT object's general settings. 
It is formatted in strict Python syntax, supporting lists, strings, numbers, and booleans.


#### 2. Global Definitions
This section defines variables that are globally available to all templates. It includes:
- **Defined Values**: Explicit variable definitions (e.g., `mass = 1.0`).
- **Referenced Variables**: Variables used but not explicitly defined (noted as "assumed to be defined outside this DSCRIPT file").


#### 3. Templates
Templates define reusable script content. Each template:
- Has a unique key (e.g., `0`, `1`, `2`) and optional local definitions.
- Supports variable substitution with `${variable_name}` syntax.
- Encodes complex structures like regions, groups, or simulation commands.


#### 4. Attributes
Attributes store metadata about each template, such as:
- **facultative**: Whether the template is optional.
- **eval**: Whether variables are evaluated.
- **readonly**: Whether the template is read-only.

"""

# The generated output is reproduced here
output = """
# DSCRIPT SAVE FILE

# ╔════════════════════════════════════════════════════════════════════════════════════════╗
# ║  PIZZA.DSCRIPT FILE v0.9999 | License: GPLv3 | Email: olivier.vitrac@agroparistech.fr  ║
# ║════════════════════════════════════════════════════════════════════════════════════════║
# ║                                     Name: akuWzPlc                                     ║
# ╚════════════════════════════════════════════════════════════════════════════════════════╝


# GLOBAL PARAMETERS (8 parameters)
{
    SECTIONS = ['DYNAMIC'],
    section = 0,
    position = 0,
    role = 'dscript instance',
    description = 'dynamic script',
    userid = 'script:LammpsHeaderBox:headerinit...script:LammpsFooterPreview:footerpreview',
    version = 0.9999,
    verbose = False
}


# GLOBAL DEFINITIONS (number of definitions=5)
mass = 1.0
n_middle = ${n_middle}  # value assumed to be defined outside this DSCRIPT file
n_upper = ${n_upper}  # value assumed to be defined outside this DSCRIPT file
n_all = ${n_all}  # value assumed to be defined outside this DSCRIPT file
n_lower = ${n_lower}  # value assumed to be defined outside this DSCRIPT file


# TEMPLATES (number of items=17)

# LOCAL DEFINITIONS for key '0'
name = $SimulationBox
dimension = 3
units = $si
boundary = ['f', 'f', 'f']
atom_style = $smd
atom_modify = ['map', 'array']
comm_modify = ['vel', 'yes']
neigh_modify = ['every', 10, 'delay', 0, 'check', 'yes']
newton = $off
boxid = $box

0: [
    % --------------[ Initialization for <${name}:${boxid}>   ]--------------
    # set a parameter to None or "" to remove the definition
    dimension    ${dimension}
    units        ${units}
    boundary     ${boundary}
    atom_style   ${atom_style}
    atom_modify  ${atom_modify}
    comm_modify  ${comm_modify}
    neigh_modify ${neigh_modify}
    newton       ${newton}
    # ------------------------------------------
 ]

# LOCAL DEFINITIONS for key '1'
lattice_style = $sc
lattice_scale = 0.001
lattice_spacing = [0.001, 0.001, 0.001]

1: [
    % --------------[ Lattice for <${name}:${boxid}>, style=${lattice_style}, scale=${lattice_scale} ]--------------
    lattice ${lattice_style} ${lattice_scale} spacing ${lattice_spacing}
    # ------------------------------------------
 ]

# LOCAL DEFINITIONS for key '2'
boxunits_arg = $units box
xmin = -0.04
xmax = 0.04
ymin = -0.04
ymax = 0.04
zmin = -0.03
zmax = 0.03
nbeads = 3

2: [
    % --------------[ Box for <${name}:${boxid}> incl. ${nbeads} bead types ]--------------
    region ${boxid} block ${xmin} ${xmax} ${ymin} ${ymax} ${zmin} ${zmax} ${boxunits_arg}
    create_box	${nbeads} ${boxid}
    # ------------------------------------------
 ]

# LOCAL DEFINITIONS for key '3'
style = $cylinder
ID = $LowerCylinder

3: % variables to be used for ${ID} ${style}

# LOCAL DEFINITIONS for key '4'
ID = $CentralCylinder
4: % variables to be used for ${ID} ${style}

# LOCAL DEFINITIONS for key '5'
ID = $UpperCylinder
5: % variables to be used for ${ID} ${style}

# LOCAL DEFINITIONS for key '6'
ID = $LowerCylinder
args = ['z', 0, 0, 0.03, 0.0, 0.005]
side = ""
move = ""
units = $ units box
rotate = ""
open = ""

6: [
    % Create region ${ID} ${style} args ...  (URL: https://docs.lammps.org/region.html)
    # keywords: side, units, move, rotate, open
    # values: in|out, lattice|box, v_x v_y v_z, v_theta Px Py Pz Rx Ry Rz, integer
    region ${ID} ${style} ${args} ${side}${units}${move}${rotate}${open}
 ]

# LOCAL DEFINITIONS for key '7'
ID = $CentralCylinder
args = ['z', 0, 0, 0.03, 0.005, 0.015]

7: [
    % Create region ${ID} ${style} args ...  (URL: https://docs.lammps.org/region.html)
    # keywords: side, units, move, rotate, open
    # values: in|out, lattice|box, v_x v_y v_z, v_theta Px Py Pz Rx Ry Rz, integer
    region ${ID} ${style} ${args} ${side}${units}${move}${rotate}${open}
 ]

# LOCAL DEFINITIONS for key '8'
ID = $UpperCylinder
args = ['z', 0, 0, 0.03, 0.015, 0.02]

8: [
    % Create region ${ID} ${style} args ...  (URL: https://docs.lammps.org/region.html)
    # keywords: side, units, move, rotate, open
    # values: in|out, lattice|box, v_x v_y v_z, v_theta Px Py Pz Rx Ry Rz, integer
    region ${ID} ${style} ${args} ${side}${units}${move}${rotate}${open}
 ]

# LOCAL DEFINITIONS for key '9'
ID = $LowerCylinder
beadtype = 1

9: [
    % Create atoms of type ${beadtype} for ${ID} ${style} (https://docs.lammps.org/create_atoms.html)
    create_atoms ${beadtype} region ${ID}
 ]

# LOCAL DEFINITIONS for key '10'
ID = $CentralCylinder
beadtype = 2

10: [
    % Create atoms of type ${beadtype} for ${ID} ${style} (https://docs.lammps.org/create_atoms.html)
    create_atoms ${beadtype} region ${ID}
 ]

# LOCAL DEFINITIONS for key '11'
ID = $UpperCylinder
beadtype = 3

11: [
    % Create atoms of type ${beadtype} for ${ID} ${style} (https://docs.lammps.org/create_atoms.html)
    create_atoms ${beadtype} region ${ID}
 ]

12: [
    # --------------[ TEMPLATE "1+2+3" ]--------------
    group lower type 1
    group middle type 2
    group upper type 3
    group all union lower middle upper
    group external subtract all middle
    # --------------------------------------------
    # ---> Total items: 5 - Ignored item: 0
 ]

13: [
    mass 1 2.0
    mass 2 ${mass}
    mass 3 ${mass}
 ]

14: [
    variable n_all equal "count(all)"
    variable n_lower equal "count(lower)"
    variable n_middle equal "count(middle)"
    variable n_upper equal "count(upper)"
 ]

15: [
    print "Number of atoms in all: ${n_all}"
    print "Number of atoms in lower: ${n_lower}"
    print "Number of atoms in middle: ${n_middle}"
    print "Number of atoms in upper: ${n_upper}"
 ]

# LOCAL DEFINITIONS for key '16'
previewfilename = $dump.initial.region_SimulationBox

16: [
    % --------------[ Preview for <${name}:${boxid}> incl. ${nbeads} bead types ]--------------
    % Output the initial geometry to a dump file "${previewfilename}" for visualization
    dump initial_dump all custom 1 ${previewfilename} id type x y z
    run 0
    # ------------------------------------------
 ]

# ATTRIBUTES (number of items with explicit attributes=17)
0:{facultative=False, eval=True, readonly=False, condition=None, condeval=False, detectvar=True}
1:{facultative=False, eval=True, readonly=False, condition=None, condeval=False, detectvar=True}
2:{facultative=False, eval=True, readonly=False, condition=None, condeval=False, detectvar=True}
3:{facultative=False, eval=True, readonly=False, condition=None, condeval=False, detectvar=True}
4:{facultative=False, eval=True, readonly=False, condition=None, condeval=False, detectvar=True}
5:{facultative=False, eval=True, readonly=False, condition=None, condeval=False, detectvar=True}
6:{facultative=False, eval=True, readonly=False, condition=None, condeval=False, detectvar=True}
7:{facultative=False, eval=True, readonly=False, condition=None, condeval=False, detectvar=True}
8:{facultative=False, eval=True, readonly=False, condition=None, condeval=False, detectvar=True}
9:{facultative=False, eval=True, readonly=False, condition=None, condeval=False, detectvar=True}
10:{facultative=False, eval=True, readonly=False, condition=None, condeval=False, detectvar=True}
11:{facultative=False, eval=True, readonly=False, condition=None, condeval=False, detectvar=True}
12:{facultative=False, eval=False, readonly=False, condition=None, condeval=False, detectvar=True}
13:{facultative=False, eval=True, readonly=False, condition=None, condeval=False, detectvar=True}
14:{facultative=False, eval=False, readonly=False, condition=None, condeval=False, detectvar=True}
15:{facultative=False, eval=True, readonly=False, condition=None, condeval=False, detectvar=True}
16:{facultative=False, eval=True, readonly=False, condition=None, condeval=False, detectvar=True}

"""
Doutput = dscript.parsesyntax(output)  # it is parsed here