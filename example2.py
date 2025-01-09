#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
### Comprehensive Documentation of Example 2

This example is a **showcase** of the powerful capabilities provided by the **Pizza3 toolkit** for creating, managing, and analyzing simulations in LAMMPS. It integrates multiple components of the Pizza3 framework, demonstrating their interplay and highlighting their advanced functionalities.

---

### **Objective**

This example demonstrates the programmatic creation of **3D geometries**, management of **atomic groups**, and generation of both **LAMMPS scripts** and **DSCRIPT files**. The goal is to illustrate the flexibility and modularity of the Pizza3 toolkit for handling simulation workflows efficiently and dynamically.

---

### **What You Will Learn**

1. **Initialization and Setup:**
   - Configure global settings for simulations.
   - Handle directory and file management for temporary data.

2. **Using the `region` Class:**
   - Define and initialize a 3D simulation box with SI units.
   - Create subdomains (regions) within the box using a lattice-based approach.
   - Add cylindrical regions with specific dimensions and bead types.

3. **Dynamic Group Management with `group` and `groupobject`:**
   - Create and manage groups of atoms based on bead types.
   - Perform arithmetic operations on groups (union, subtraction).
   - Dynamically assign masses and verify atom counts for each group.

4. **Combining Scripts:**
   - Use the `pipescript` class to combine multiple scripts into a cohesive workflow.
   - Modularly add initialization, lattice definitions, group assignments, and geometry preview scripts.

5. **Generating and Using DSCRIPT Files:**
   - Export LAMMPS scripts to DSCRIPT format for reusability.
   - Reconstruct and validate LAMMPS scripts from DSCRIPT files.

6. **Debugging and Visualization:**
   - Generate output files for debugging and visualizing the simulation geometry.
   - Use flexible templates and substitutions to manage dynamic variables.

---

### **Structure of the Script**

The script is divided into multiple logical sections, each demonstrating a specific feature of the Pizza3 toolkit:

#### **1. Setup and Directory Management**
- Initializes a temporary folder (`tmp/`) to store generated scripts and output files.
- Ensures the folder exists or creates it dynamically.

#### **2. Defining the Simulation Box**
- Creates a simulation box using the `region` class.
- Configures:
  - Dimensions (3D).
  - Boundary conditions (fixed).
  - Units (SI).
  - Lattice styles and spacing.

#### **3. Adding Subregions**
- Adds cylindrical subregions within the simulation box.
- Associates each cylinder with a specific bead type and dimensions.

#### **4. Managing Groups**
- Uses the `groupobject` class to define atom groups for each bead type.
- Combines groups dynamically using operations like union and subtraction.
- Assigns masses to groups and verifies atom counts.

#### **5. Generating Scripts**
- Creates modular LAMMPS scripts for initialization, group definitions, and geometry preview.
- Combines them into a single script using `pipescript`.

#### **6. Exporting and Validating DSCRIPT Files**
- Converts the LAMMPS script to a DSCRIPT format for future reuse.
- Loads the DSCRIPT file and regenerates the LAMMPS script to verify consistency.

---

### **Key Components and Tools**

#### **Pizza3 Classes and Methods**

| Class/Module   | Functionality                                                                 |
|----------------|-------------------------------------------------------------------------------|
| `region`       | Defines 3D simulation boxes and subregions.                                 |
| `groupobject`  | Manages groups of atoms or molecules.                                       |
| `group`        | Performs arithmetic operations on groups and evaluates atom counts.         |
| `pipescript`   | Combines multiple script components into a single executable pipeline.      |
| `dscript`      | Converts LAMMPS scripts into modular, reusable DSCRIPT files.              |

#### **LAMMPS Integration**
- The script generates valid LAMMPS input files with commands for defining regions, groups, and atoms.
- The generated scripts are compatible with LAMMPS' syntax and can be executed directly.

#### **DSCRIPT Features**
- Encodes LAMMPS workflows in a structured, modular format.
- Supports dynamic variable substitutions for maximum flexibility.

---

### **Execution Steps and Python Code**

#### **Step 1: Setup and Directory Management**

Before beginning, ensure that the required directory structure exists. This example uses a `tmp/` directory for storing temporary files.

```python
import os

# Path to the 'tmp' folder
tmp_folder = os.path.join(os.getcwd(), "tmp")
allow_create = True  # Set to False to prevent automatic creation

# Check and create the folder if necessary
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
```

---

#### **Step 2: Initialize the Simulation Box**

Use the `region` class to define the simulation box. Add global parameters such as dimensions, boundary conditions, and lattice details.

```python
from pizza.region import region

# Initialize the simulation box
R = region(
    name="SimulationBox",  # Name of the simulation box
    dimension=3,  # 3D simulation
    boundary=["f", "f", "f"],  # Fixed boundary conditions
    nbeads=3,  # Number of bead types
    width=0.08, height=0.08, depth=0.06,  # Dimensions in meters
    units="si",  # Use SI units
    regionunits="si",  # Define regions in SI units
    lattice_scale=0.001,  # Lattice scale in meters
    lattice_style="sc",  # Simple cubic lattice
    lattice_spacing=0.001,  # Spacing between lattice points
    separationdistance=0.001,  # Minimum separation between points
    mass=1.0  # Default mass
)
```

---

#### **Step 3: Add Cylindrical Subregions**

Define subregions (cylinders) within the simulation box using the `cylinder` method of the `region` class.

```python
# Add cylindrical subregions with different bead types
R.cylinder(name="LowerCylinder", dim="z", c1=0, c2=0, radius=0.03, lo=-0.03, hi=-0.01, beadtype=1)
R.cylinder(name="CentralCylinder", dim="z", c1=0, c2=0, radius=0.03, lo=-0.01, hi=0.01, beadtype=2)
R.cylinder(name="UpperCylinder", dim="z", c1=0, c2=0, radius=0.03, lo=0.01, hi=0.03, beadtype=3)
```

Generate initialization scripts for the region.

```python
# Generate initialization headers for the region
Rheaders = R.pscriptHeaders(what=["init", "lattice", "box"])
```

---

#### **Step 4: Manage Groups**

Use `groupobject` to define groups of atoms for each bead type and combine them into a collection.

```python
from pizza.group import group, groupobject

# Create group objects for each bead type
g1 = groupobject(beadtype=1, group='lower', mass=2.0)
g2 = groupobject(beadtype=2, group='middle')
g3 = groupobject(beadtype=3, group='upper')

# Combine group objects into a collection
gcollection = g1 + g2 + g3

# Generate a script to assign masses
Mscript = gcollection.mass(default_mass=R.mass)
```

Evaluate and define relationships between groups.

```python
# Define and evaluate groups
G = group(name="1+2+3", collection=gcollection)
G.evaluate("all", G.lower + G.middle + G.upper)
G.evaluate("external", G.all - G.middle)

# Generate a script to count atoms in each group
Ncontrol = G.count(selection=["all", "lower", "middle", "upper"])
```

---

#### **Step 5: Preview and Combine Scripts**

Preview the region geometry and combine all scripts using `pipescript`.

```python
# Preview the region geometry
Rpreview = R.pscriptHeaders(what="preview")

# Combine all scripts into a single pipeline
from pizza.script import pipescript

S = Rheaders | R | G | Mscript | Ncontrol | Rpreview
```

Write the full script to a file.

```python
# Write the combined LAMMPS script to a file
scriptfile = S.write("tmp/example2.txt", verbosity=1, overwrite=True)
print(f"The LAMMPS script is available here:\n{scriptfile}")
```

---

#### **Step 6: Generate DSCRIPT**

Export the combined LAMMPS script to a DSCRIPT format for future reuse.

```python
from pizza.dscript import dscript

# Convert to DSCRIPT
D = S.dscript(verbose=True)
dscriptfile = D.save("tmp/example2.d.txt", overwrite=True)
print(f"The DSCRIPT is available here:\n{dscriptfile}")
```

---

#### **Step 7: Validate Reversibility**

Reload the DSCRIPT file and regenerate the LAMMPS script to ensure consistency.

```python
# Load DSCRIPT and regenerate the LAMMPS script
Dreverse = dscript.load(dscriptfile)
Sreverse = Dreverse.pipescript(verbose=False)

# Output the regenerated script
print("\n\n# Reverse LAMMPS code (from disk)", Sreverse.do(verbose=False), sep="\n")
```

---

### **Key Outputs**

1. **Generated Files**:
   - LAMMPS script (`tmp/example2.txt`).
   - DSCRIPT file (`tmp/example2.d.txt`).

2. **Debug Information**:
   - Atom counts for each group.
   - Validation of script reversibility.

3. **Visualization**:
   - Geometry dump file for previewing the simulation setup.

---

### **Next Steps**

- Modify dimensions, bead types, and subregions to explore flexibility.
- Add dynamic forcefield definitions using `dforcefield`.
- Incorporate additional physical parameters and dynamics into the simulation.

This tutorial equips you to efficiently design, manage, and analyze LAMMPS simulations with the Pizza3 toolkit. Explore its modular and reusable approach to streamline your workflow!

---

### **Conclusion**

This example is a **comprehensive guide** to using Pizza3 for managing LAMMPS simulations programmatically. By integrating flexible region definitions, dynamic group management, and reusable script generation, this workflow demonstrates how to simplify and enhance the process of creating and managing complex simulations.

### **Next Steps**
- Explore the generated files (`example2.txt` and `example2.d.txt`) to understand the structure of LAMMPS and DSCRIPT outputs.
- Modify parameters (e.g., dimensions, bead types) to test the adaptability of the script.
- Use the Pizza3 toolkit to integrate additional features like forcefields and dynamics.



Created on Tue Nov 26, 2024
Author: olivi

last revision: 2024-01-07
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

# %% Generate DSCRIPT Code and Variable Report

# Convert the LAMMPS script to a DSCRIPT for dynamic reuse
D = S.dscript(verbose=True)
# check variable definitions in an HTML report
D.print_var_info(output_file="tmp/example2.d.var.html",overwrite=True)
# save this Python code in DSCRIPT format
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
