#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
example2ter.py: First version of part 3 of example2 setting displacements.

This script demonstrates the use of DSCRIPT templates for generating and managing
LAMMPS fix commands related to various types of displacements, including gravity,
oscillation, translation, and rotation. It showcases the following features:

1. **Template Definition**:
   - Templates are defined in DSCRIPT language within the `movetemplates` variable.
   - Each template specifies parameters and generates LAMMPS fix commands dynamically.

2. **Supported Displacement Types**:
   - **Gravity**:
     Adds gravitational acceleration to a specified group of atoms.
   - **Oscillation**:
     Defines sinusoidal velocity components to simulate periodic motion along specified axes.
   - **Translation**:
     Moves atoms at a constant velocity to achieve a specified displacement over a given time.
   - **Rotation**:
     Simulates rotational motion around a defined axis with a specified angular velocity.

3. **Template Syntax**:
   - Templates use DSCRIPT features such as the `!` flag for Pythonic evaluation of expressions
     and `${var[i]}` for indexed variable access.
   - Each displacement type is encapsulated in a named section, allowing modularity and reuse.

4. **Template Parsing and Execution**:
   - All templates are parsed into a single DSCRIPT instance (`M`) using `dscript.parsesyntax`.
   - Specific templates can be selected and executed, demonstrating flexible template management.

5. **Selection and Export**:
   - A subset of templates is selected for execution using `M("rotation", "translation")`.
   - The selected templates are saved to a DSCRIPT file (`tmp/example2ter_selection.d.txt`)
     for reuse or further modification.

6. **Re-Loading and Execution**:
   - The saved DSCRIPT file is reloaded into a new DSCRIPT instance (`Dter`), verifying
     the persistence and correctness of the saved templates.

### Script Workflow:
1. **Define Templates**:
   - Templates for gravity, oscillation, translation, and rotation are written in the DSCRIPT language.
2. **Parse and Select Templates**:
   - Parse all templates into a single instance (`M`) and select specific templates for execution (`Mselection`).
3. **Generate DSCRIPT File**:
   - Save the selected templates to a file for future use.
4. **Reload and Execute**:
   - Reload the DSCRIPT file into a new instance and execute the templates to ensure functionality.

### Example Output:
For the selected templates "rotation" and "translation", the generated DSCRIPT commands might look like:

```
fix rfix rotatableatoms smd/setvel v_r_vx v_r_vy v_r_vz
fix tfix translatableatoms smd/setvel ${t_vel1} ${t_vel2} ${t_vel3}
```

### Key Notes:
- The use of DSCRIPT enables dynamic and modular creation of LAMMPS commands, reducing the need
  for manual edits and repetitive definitions.
- The modularity allows users to manage, save, and reuse templates efficiently.
- The extended parsing and execution capabilities demonstrate the flexibility of DSCRIPT in managing
  complex simulation configurations.

### Dependencies:
- **pizza.dscript**: A Python library for managing DSCRIPT templates. Ensure it is installed and accessible.

### Output Files:
- `tmp/example2ter_selection.d.txt`: Contains the selected DSCRIPT templates, saved for further use or modifications.

### Usage:
Run this script as a standalone program or integrate it into a larger simulation workflow to dynamically manage LAMMPS displacements.



last revision: 2025-01-1
Author: INRAE\olivier.vitrac@agroparistech.fr

"""

# Imports
from pizza.dscript import dscript

# Templates written in DSCRIPT language
movetemplates = """

# MOVETEMPLATES

# Generic template structure:
#   fix_template: [!
#       # Description of the fix
#       ...
#       # Parameters
#       ...
#       # Resulting fix command
#       ...
# ]

# Error Handling:
# - If an expression fails to evaluate, return an error string indicating the failed variable and context.
# - Fallback mechanism for undefined .

# note1: The attributes are not explicitly defined for concision. The flag ! is used instead:
#        block:[! ... ] is equivalent to block: {...,eval=True,...}
# note2: ${var[i]} gives access to the ith component of the list ${var}


{
    section = None,
    position = None,
    role = "dscript instance",
    description = "Fix for gravity, move and translation",
    userid = "movefix",
    version = 1.0,
    verbose = False
}


# -----------------------------------------------
# GRAVITY TEMPLATE
# local variables start with the preffix "g_"
# -----------------------------------------------

# Gravity parameters
g_acceleration = 9.81       # acceleration (earth=9.81 m/s^2)
g_direction = [0,1,0]       # direction of gravity foeld
g_orientation = "$-"        # either "" or "$-"

# Fix parameters
g_targetGRP = "$heavyatoms" # group ID to be set by user
g_fixID = "$gfix"           # internal fix ID

# Gravity template (keep flag ! =evaluate)
gravity: [!
    # Add gravity
    fix ${g_fixID} ${g_targetGRP} gravity ${g_orientation}${g_acceleration} vector ${g_direction}
]

# -----------------------------------------------
# OSCILLATION MOVE TEMPLATE
# local variables start with the preffix "mo_"
# -----------------------------------------------

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
    variable mOvel10 equal ${mO_l[0]}*PI/${mO_T[0]}  # Maximum velocity along 1
    variable mOvel20 equal ${mO_l[1]}*PI/${mO_T[1]}  # Maximum velocity along 2
    variable mOvel30 equal ${mO_l[2]}*PI/${mO_T[2]}  # Maximum velocity along 3
    # Define sinusoidal velocity components as functions of time (oscillations)
    variable mOvel1 atom ${mOvel10}*sin(${mOw1}*time)
    variable mOvel2 atom ${mOvel20}*sin(${mOw2}*time)
    variable mOvel3 atom ${mOvel30}*sin(${mOw3}*time)
    # Add oscillations
    fix ${mO_fixID} ${mO_targetGRP} smd/setvel v_mOvel1 v_mOvel2 v_mOvel3
    ]

# -----------------------------------------------
# TRANSLATION MOVE TEMPLATE
# local variables start with the prefix "t_"
# -----------------------------------------------

# Translation parameters: t_distance (displacement) and t_time (duration)
t_distance = [1.0, 0.0, 0.0]  # translation distance along dimension 1,2,3
t_time = 10.0                  # total translation time (LAMMPS time units)

# Fix parameters
t_targetGRP = "$translatableatoms" # group ID to be set by user
t_fixID = "$tfix"                  # internal fix ID

# Translation template (keep flag ! =evaluate)
translation: [!
    # Calculate translation velocity components
    variable t_vel1 equal ${t_distance[0]}/${t_time}  # Velocity along dimension 1
    variable t_vel2 equal ${t_distance[1]}/${t_time}  # Velocity along dimension 2
    variable t_vel3 equal ${t_distance[2]}/${t_time}  # Velocity along dimension 3
    # Add constant translation
    fix ${t_fixID} ${t_targetGRP} smd/setvel ${t_vel1} ${t_vel2} ${t_vel3}
]

# -----------------------------------------------
# ROTATIONAL DISPLACEMENT TEMPLATE (smd/setvel)
# local variables start with the prefix "r_"
# -----------------------------------------------

# Rotation parameters (keep ![...] to defne numeric vectors)
r_center = [0, 0, 0]      # Center of rotation along dimension 1,2,3
r_axis = [0, 0, 1]        # Axis of rotation (normalized vector)
r_angular_velocity = 1.0   # Angular velocity in radians per time unit

# Fix parameters
r_targetGRP = "$rotatableatoms"   # group ID to be set by user
r_fixID = "$rfix"                # internal fix ID

# Rotational template (keep flag ! =evaluate)
rotation: [!
    # Ensure the rotation axis is normalized (magnitude = 1)
    variable r_axis_norm equal sqrt(${r_axis[0]}^2 + ${r_axis[1]}^2 + ${r_axis[2]}^2)
    variable r_axis1 equal ${r_axis[0]}/${r_axis_norm}
    variable r_axis2 equal ${r_axis[1]}/${r_axis_norm}
    variable r_axis3 equal ${r_axis[2]}/${r_axis_norm}
    # Define angular velocity
    variable r_omega equal ${r_angular_velocity}
    # Compute relative positions of atoms to the rotation center
    variable dx atom x - ${r_center[0]}
    variable dy atom y - ${r_center[1]}
    variable dz atom z - ${r_center[2]}
    # Compute velocity components for rotation
    variable r_vx atom ${r_omega} * (${r_axis2} * dz - ${r_axis3} * dy)
    variable r_vy atom ${r_omega} * (${r_axis3} * dx - ${r_axis1} * dz)
    variable r_vz atom ${r_omega} * (${r_axis1} * dy - ${r_axis2} * dx)
    # Apply the rotational velocity using smd/setvel
    fix ${r_fixID} ${r_targetGRP} smd/setvel v_r_vx v_r_vy v_r_vz
]

"""

# Parse all templates at once
M = dscript.parsesyntax(movetemplates,name="move template database",authentification=False)

# check one template with M[index] or M["name"]
M["gravity"]

# Selection of displacements, note that () are used instead of []
Mselection = M("rotation","translation")
print(Mselection.do(verbose=True))

# Generate the Dscript file for the selection
MselectionScriptFile = Mselection.save("tmp/example2ter_selection.d.txt", overwrite=True)

# Load again the Dscript file, and compare the outputs (control)
Dter = dscript.load(MselectionScriptFile)
print(Dter.do(verbose=True))

# Change the distance of translation
Dter.DEFINITIONS.t_distance = [1e-3,0,0]
print(Dter.do(verbose=True))
