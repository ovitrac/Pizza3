# -*- coding: utf-8 -*-
"""
Principles of Coding with Pizza3 in Python for LAMMPS

This script demonstrates how to use Pizza3 version 0.9976+ to construct a complete LAMMPS input file 
for the simulation of three stacked cylinders (lower, central, upper) modeled as hyperelastic materials. 
Each cylinder is represented by a distinct bead type (1, 2, and 3), and the simulation is dynamically 
scripted to avoid external code snippets.

**Intent:**
The goal is to teach how to use Pizza3's `script`, `dscript`, `pipescript`, `scriptobject`, and `scriptobjectgroup` 
classes to generate flexible LAMMPS scripts with minimal manual intervention. Users will learn how to:
- Define simulation boxes, regions, and lattice configurations.
- Customize forcefields and apply them to specific materials.
- Create and manage groups of atoms or particles.
- Define and control movement for specific groups of particles.
- Set up time integration, trajectory output, and dump instructions.
- Pipe together multiple scripts into a final, executable LAMMPS input script.

**What to Learn:**
1. **Dynamic Scripting with Pizza3**: Learn how to dynamically generate LAMMPS input files without manually coding every section.
2. **Piping Scripts Together**: Explore the power of combining scripts using the pipe (`|`) operator, which allows for the inclusion of local variables and reordering of sections.
3. **LAMMPS-Specific Operations**: Understand how to define regions, set up forcefields, and manage object groups in the context of a LAMMPS simulation.
4. **Script Objects**: Learn how to use `scriptobject` and `scriptobjectgroup` to define and manage multiple physical entities with unique properties.

**Script Sections:**
1. **S1a, S1b: Simulation Box, Lattice, and Regions**  
   - Demonstrates the creation of the simulation box and cylindrical regions using the `region` class.
   - Involves the `pipescript` to handle initialization, lattice definition, and box setup.
   - **What You Learn**: How to create 3D simulation boxes and regions in LAMMPS, including the use of lattices and boundaries.
   - **Syntax Info**: You can access or modify sections either via `Sx.step = "..."` or `Sx["step"] = "..."`. Both are equivalent.
   
2. **S2: Customized Forcefields**  
   - Sets up a dynamic forcefield using the `dforcefield` class. 
   - Custom forcefield properties are applied to each of the three cylinders.
   - **What You Learn**: How to define and apply custom physical properties to different materials or objects in the simulation.
   - **Syntax Info**: Use forcefield templates with dynamic variable substitution by setting custom definitions using `USER` or the shorthand `USER.variable`.
   
3. **S3: Customized Groups**  
   - Demonstrates how to manage groups of particles and combine groups using operations like union (`+`) and subtraction (`-`).
   - **What You Learn**: How to create and manipulate groups of objects, which is critical for efficient simulation management.
   - **Syntax Info**: Groups can be manipulated with `G.evaluate("group_name", G.lower + G.upper)` or by subtracting groups like `G.all - G.middle`.

4. **S4a, S4b, S4c: Dynamics and Time Integration**  
   - Shows how to define movement for the upper cylinder and how to set up time integration using the `dscript` class.
   - **What You Learn**: How to control the movement of specific groups and integrate time dynamics into the simulation.
   - **Syntax Info**: The `dscript` class supports shorthands like `Sx["step"] = "..."` and `Sx.step = "..."` for adding steps.

5. **S5: Dump Instructions**  
   - Configures the trajectory dump, specifying which physical variables should be saved during the simulation.
   - **What You Learn**: How to set up trajectory dumps for capturing simulation data.
   - **Syntax Info**: You can directly modify dumping parameters using shorthand assignment (e.g., `Sx.dumpinit = "..."`).

6. **S6: Thermodynamic Output**  
   - Defines the thermodynamic output frequency and format using LAMMPS thermodynamic styles.
   - **What You Learn**: How to configure thermodynamic outputs for monitoring key simulation parameters.
   - **Syntax Info**: Use `Sx.thermo = "..."` to define thermodynamic steps easily.

7. **S7: Running the Simulation**  
   - Executes the LAMMPS simulation with the defined run time.
   - **What You Learn**: How to finalize and run a simulation with all defined steps.
   - **Syntax Info**: Use `Sx.run = "..."` to define the run command, and you can force evaluation with `Sx.run.eval = True`.

**Compatibility:**
This example requires Pizza3 version 0.9976 or above. All scripts (`script`, `pipescript`, `scriptobject`, and `scriptobjectgroup`) exhibit sufficient compatibility to be combined with operators. The pipe operator (`|`) is preferred as it facilitates reordering and the inclusion of local variables.

**Revision:**
Last revision: 2024-11-08

"""

# Dependencies
from pizza.script import script, scriptdata  # Base script and data structure classes
from pizza.dscript import dscript  # Dynamic script class for managing LAMMPS inputs
from pizza.group import group  # Group management for atoms or molecules
from pizza.region import region  # Region class to define physical simulation regions
from pizza.dforcefield import dforcefield  # Dynamic forcefield for particles
from pizza.generic import generic  # Generic forcefield module


# %% S1a, S1b: Defining Simulation Box, Lattice, and Regions
# Goal: Demonstrate how to define the simulation box and cylindrical regions.
# Syntax: Both `Sx.step = "..."` and `Sx["step"] = "..."` are supported shorthands.
# Learn how to initialize the simulation setup, including dimensions and lattice.

R_container = region(
    name="SimulationBox",  # Name of the box
    dimension=3,  # 3D simulation
    boundary=["f", "f", "f"],  # Fixed boundary conditions
    nbeads=3,  # Number of bead types
    width=0.06, height=0.02, depth=0.06,  # Box dimensions in meters
    units="si",  # Using SI units for LAMMPS
    lattice_scale=0.0008271, lattice_style="sc",  # Lattice type and scaling
    lattice_spacing=0.0008271,  # Lattice point spacing
    separationdistance=0.0001  # Minimum separation between points
)

# Define cylindrical regions for the three cylinders
R_container.cylinder(name="LowerCylinder", dim="z", c1=0, c2=0, radius=0.03, lo=0.0, hi=0.005, beadtype=1)
R_container.cylinder(name="CentralCylinder", dim="z", c1=0, c2=0, radius=0.03, lo=0.005, hi=0.015, beadtype=2)
R_container.cylinder(name="UpperCylinder", dim="z", c1=0, c2=0, radius=0.03, lo=0.015, hi=0.02, beadtype=3)

# Generate scripts for initialization, lattice setup, and region definition
S1_headers = R_container.pscriptHeaders(what=["init", "lattice", "box"])
S1_core = R_container.pipescript()

# Combine header and region definitions into one script
S1 = S1_headers | S1_core
print(' \n# S1: HEADERS & REGIONS\n', S1.do(printflag=False, verbose=False), sep="\n")


# %% S2: Customized Forcefields
# Goal: Define and apply dynamic forcefields to the cylinders.
# Syntax: Use `USER` to pass custom properties to the forcefield.
# Learn how to customize material properties like elasticity, density, and viscosity.

# Additional modules can be added to forcefields
additional_modules = [generic]

# Define the dynamic forcefield with custom properties
dynamic_ff = dforcefield(
    base_class="solidfood",
    beadtype=None,  # Set dynamically
    userid="solid",
    additional_modules=additional_modules,
    rho=1.0e3, E=1e4, nu=0.3, c0="0.1*sqrt(${E}/${rho})", sigma_yield="0.1*${E}", 
    hardening=0, q1=1.0, q2=2.0, Hg=10.0, Cp=1000.0,
    contact_scale=1.5, contact_stiffness="2.5*${c0}^2*${rho}"
)

# Forcefield properties for each cylinder
customff1 = scriptdata(E=1e4, rho=1000)
customff2 = scriptdata(E=5e3, rho=1000)
customff3 = scriptdata(E=4e4, rho=1000)

# Assign forcefield to each cylinder (b1, b2, b3)
b1 = dynamic_ff.scriptobject(beadtype=1, USER=customff1, name="b1", group=["lower", "solid", "fixed"])
b2 = dynamic_ff.scriptobject(beadtype=2, USER=customff2, name="b2", group=["middle", "solid", "movable"])
b3 = dynamic_ff.scriptobject(beadtype=3, USER=customff3, name="b3", group=["upper", "solid", "movable"])

# Combine forcefields into one collection
collection = b1 + b2 + b3
S2 = collection.script(printflag=False, verbosity=1)
S2.name = "S2:forcefield"

# Output forcefield definitions
print("\n# FORCEFIELDS\n", S2.do(printflag=False, verbose=False), sep="\n")


# %% S3: Customized Groups
# Goal: Define and manage groups of objects.
# Syntax: Use `+` for group union and `-` for group subtraction.
# Learn how to manage groups for controlling particle behavior.

# Create a group container for managing groups
G = collection.group_generator()

# Define groups: "all" and "external"
G.evaluate("all", G.lower + G.middle + G.upper)
G.evaluate("external", G.all - G.middle)

# Generate group script
Gall = G("all", "external")
S3 = Gall.script(verbose=False)
S3.name = "S3:customgroup"

# Output group definitions
print("\n# CUSTOMIZED GROUPS\n", S3.do(printflag=False, verbose=False), sep="\n")


# %% S4a: Movable Objects (Upper Cylinder Movement)
# Goal: Define movement and dynamic behavior of particles.
# Learn how to initialize movement and apply periodic forces.

move = dscript(name="S4a:move",
               amplitude=1.0e-3,  # Movement amplitude
               period=1.0)  # Period in seconds

# If needed, movement variables can be modified later
move.DEFINITIONS.update(
    amplitude=1.0e-3,  # Amplitude of movement (1 mm)
    period=1.0  # Period of movement (1 second)
)

# CODELET "moveinit" initializes velocity for all beads
# It can be defined via several shorthands
#   move["moveinit"] = "..." is a shorthand of move.TEMPLATE["moveinit"]="..."
#   move.moveinit =  "..." is a shorthand of move.TEMPLATE["moveinit"]="..."
# Note: it is imperative to use move["move:init"] if you use special characters in name
move.moveinit = """
# Set initial velocities to zero
velocity all set 0.0 0.0 0.0 units box # note box units
"""

# CODELET "movelower" fixes the position of the lower cylinder
move.movelower = """
# Fix the lower cylinder to prevent movement
fix fix_lower lower setforce 0.0 0.0 0.0
"""

# CODELET "moveupper" applies periodic movement to the upper cylinder
move.moveupper = """
# Apply periodic movement to the upper cylinder
fix move_upper upper move wiggle 0.0 0.0 ${amplitude} ${period} units box
"""
#move.moveupper.eval = True  # Force evaluation of movement # not needed anymore, see note 1

# for a rapid control
move.moveupper

# full control
print("\n# MOVABLE OBJECTS", move.do(printflag=False, verbose=True), sep="\n")


# %% S4b: Time Integration Setup
# Goal: Define time integration methods for the simulation.
# Learn how to set and dynamically adjust the timestep.

# Note 1: Defined variables are recognized on the fly.
#         There is no need to force: integration.intinit.eval = True

integration = dscript(name="S4b:timeintegration", dt=0.1)
integration.intinit = "fix dtfix tlsph smd/adjust_dt ${dt}"
integration.intset = "fix integration_fix tlsph smd/integrate_tlsph"
print("\n# TIME INTEGRATION", integration.do(printflag=False, verbose=False), sep="\n")


# %% S4c: Trajectory Output
# Goal: Define trajectory output for post-processing and visualization.
# Learn how to capture stress, strain, and neighbor information for each particle.

trajectory = dscript(name="S4c:trajectoryoutput")
trajectory.compute = """
compute S all smd/tlsph_stress
compute E all smd/tlsph_strain
compute nn all smd/tlsph_num_neighs
"""
print("\n# TRAJECTORY OUTPUT", trajectory.do(printflag=False, verbose=False), sep="\n")


# %% S4: Combine S4a, S4b, S4c
S4 = move + integration + trajectory
S4.name = "S4:dynamics"
print("\n# DYNAMICS", S4.do(printflag=False, verbose=False), sep="\n")


# %% S5: Dump Settings
# Define how the output data will be dumped.
S5 = dscript(name="S5:dump", dumpdt=50, dumpfile="$dump.LAMMPS")
S5.dumpinit = """
dump dump_id all custom ${dumpdt} ${dumpfile} id type x y z vx vy vz &
c_S[1] c_S[2] c_S[4] c_nn &
c_E[1] c_E[2] c_E[4] &
vx vy vz
"""
# S5.dumpinit.eval = True  # not needed anymore, see note 1
S5.dumpset = """
dump_modify dump_id first yes
"""


# %% S6: Thermodynamic Output
# Define thermodynamic output frequency and format.
S6 = dscript(name="S6:thermo", thermodt=100)
S6.thermo = """
thermo ${thermodt}
thermo_style custom step dt f_dtfix v_strain
"""
# S6.thermo.eval = True  # not needed anymore, see note 1


# %% S7: Run the Simulation
# Define the final run command for the simulation.
S7 = dscript(name="S7:run", runtime=5000)
S7.run = "run ${runtime}"
# S7.run.eval = True # not needed anymore, see note 1


# %% Combine All Sections (S1, S2, S3, S4, S5, S6, S7)
Sall = S1 | S2 | S3 | S4 | S5 | S6 | S7  # Pipe all sections together
print("\n\n# ALL SCRIPTS", Sall.do(printflag=False, verbose=False), sep="\n")


# %% Write the final LAMMPS script to file
Sall.write("tmp/example.txt", verbosity=1)


# %% Convert the full script back to a dynamic dscript
Dall = Sall.dscript(verbose=True)


# %% Write Dall as dynamic script for reuse
Dall.save("tmp/example.d.txt", overwrite=True)


# %% Retrieve the Dscript file and convert it back to a pipescript
Dall2 = dscript.load("tmp/example.d.txt")
Sall2 = Dall2.pipescript(verbose=False)
print("\n\n# ALL SCRIPTS (from disk)", Sall2.do(printflag=False, verbose=False), sep="\n")


# %% Repeat the whole code in DSCRIPT language
"""
**DSCRIPT File Example and Dynamic Re-conversion with Dall3**

This example demonstrates how to leverage the DSCRIPT syntax in Pizza3 for defining complex simulation parameters dynamically. The `Dcode` variable contains the entire simulation configuration in the DSCRIPT syntax, enabling both persistent storage and later re-conversion into dynamic objects.

**Key Concepts Illustrated in Dcode:**
1. **Global and Local Definitions**:
   - **Global Definitions**: Variables set globally at the beginning, such as `dumpfile`, `dumpdt`, `thermodt`, and `runtime`, are applied across multiple templates if not overridden locally. When saved, global values can be annotated, indicating if they're set externally.
   - **Local Definitions**: Variables are defined with a specified "scope" per template section. This allows values to be overridden or dynamically updated only for certain steps in the simulation without affecting other sections.

2. **Templates and Steps**:
   - **Step-based Scripting**: Each section in the simulation corresponds to a numbered "step" that represents a unique template in the script. Local definitions for each step can be configured independently.
   - **Special Syntax**: Local definitions leverage Pizza3's dynamic substitution, allowing variables such as `${ID}`, `${style}`, and `${args}` to be dynamically evaluated within each template.

3. **Simulation Structure**:
   - **Pipeline of Steps**: Dcode’s steps flow in sequence to establish each simulation stage: initialization, lattice setup, region definitions, group definitions, forcefield configurations, and more. This structure aligns with LAMMPS, ensuring reproducibility and compatibility with specific physical behaviors.
   - **Comments and Header Sections**: Each step includes comments or headers for easy reading and reuse. Headers describe the purpose of each template, with inline comments highlighting variable options and expected parameter values.

4. **Overrides in `Dall3`**:
   - **Dynamic Updates and Local Precedence**: The `Dall3` instance, derived from Dcode, retains the entire sequence as a `dscript` object. The `dscript` format allows flexible adjustments, with both global and local values manageable at runtime.
   - **Local Precedence**: When values are overridden locally, they take precedence in the final generated script, illustrating the control and precision available in the Pizza3 DSCRIPT system.

**Usage**:
- `Dall3.DEFINITIONS.runtime = 1e4`: Sets the global definition of `runtime` to `1e4`.
- `Dall3[-1].definitions.runtime = 2e5`: Sets a local definition of `runtime` specifically for the final step in `Dall3`, giving it precedence over the global value.

**Example Output**:
- The last command, `print(Dall3[-1].do())`, demonstrates that `Dall3` reflects the local override by outputting `run 200000.0`, verifying the variable hierarchy and precedence.
"""



Dcode = """
# DSCRIPT SAVE FILE

# GLOBAL DEFINITIONS
dumpfile = $dump.LAMMPS
dumpdt = 50
thermodt = 100
runtime = 5000

# LOCAL DEFINITIONS for step '0'
dimension = 3
units = $si
boundary = ['f', 'f', 'f']
atom_style = $smd
atom_modify = ['map', 'array']
comm_modify = ['vel', 'yes']
neigh_modify = ['every', 10, 'delay', 0, 'check', 'yes']
newton = $off
name = $SimulationBox

0: [    % --------------[ Initialization Header (helper) for "${name}"   ]--------------
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

# LOCAL DEFINITIONS for step '1'
lattice_style = $sc
lattice_scale = 0.0008271
lattice_spacing = [0.0008271, 0.0008271, 0.0008271]

1: [
    % --------------[ LatticeHeader 'helper' for "${name}"   ]--------------
    lattice ${lattice_style} ${lattice_scale} spacing ${lattice_spacing}
    # ------------------------------------------
 ]

# LOCAL DEFINITIONS for step '2'
xmin = -0.03
xmax = 0.03
ymin = -0.01
ymax = 0.01
zmin = -0.03
zmax = 0.03
nbeads = 3

2: [
    % --------------[ Box Header 'helper' for "${name}"   ]--------------
    region box block ${xmin} ${xmax} ${ymin} ${ymax} ${zmin} ${zmax}
    create_box	${nbeads} box
    # ------------------------------------------
 ]

# LOCAL DEFINITIONS for step '3'
ID = $LowerCylinder
style = $cylinder

3: % variables to be used for ${ID} ${style}

# LOCAL DEFINITIONS for step '4'
ID = $CentralCylinder

4: % variables to be used for ${ID} ${style}

# LOCAL DEFINITIONS for step '5'
ID = $UpperCylinder

5: % variables to be used for ${ID} ${style}

# LOCAL DEFINITIONS for step '6'
args = ['z', 0.0, 0.0, 36.27130939426913, 0.0, 6.045218232378189]
side = ""
move = ""
rotate = ""
open = ""
ID = $LowerCylinder
units = ""

6: [
    % Create region ${ID} ${style} args ...  (URL: https://docs.lammps.org/region.html)
    # keywords: side, units, move, rotate, open
    # values: in|out, lattice|box, v_x v_y v_z, v_theta Px Py Pz Rx Ry Rz, integer
    region ${ID} ${style} ${args} ${side}${units}${move}${rotate}${open}
 ]

# LOCAL DEFINITIONS for step '7'
ID = $CentralCylinder
args = ['z', 0.0, 0.0, 36.27130939426913, 6.045218232378189, 18.135654697134566]

7: [
    % Create region ${ID} ${style} args ...  (URL: https://docs.lammps.org/region.html)
    # keywords: side, units, move, rotate, open
    # values: in|out, lattice|box, v_x v_y v_z, v_theta Px Py Pz Rx Ry Rz, integer
    region ${ID} ${style} ${args} ${side}${units}${move}${rotate}${open}
 ]

# LOCAL DEFINITIONS for step '8'
ID = $UpperCylinder
args = ['z', 0.0, 0.0, 36.27130939426913, 18.135654697134566, 24.180872929512756]

8: [
    % Create region ${ID} ${style} args ...  (URL: https://docs.lammps.org/region.html)
    # keywords: side, units, move, rotate, open
    # values: in|out, lattice|box, v_x v_y v_z, v_theta Px Py Pz Rx Ry Rz, integer
    region ${ID} ${style} ${args} ${side}${units}${move}${rotate}${open}
 ]

# LOCAL DEFINITIONS for step '9'
ID = $LowerCylinder
beadtype = 1

9: [
    % Create atoms of type ${beadtype} for ${ID} ${style} (https://docs.lammps.org/create_atoms.html)
    create_atoms ${beadtype} region ${ID}
 ]

# LOCAL DEFINITIONS for step '10'
ID = $CentralCylinder
beadtype = 2

10: [
    % Create atoms of type ${beadtype} for ${ID} ${style} (https://docs.lammps.org/create_atoms.html)
    create_atoms ${beadtype} region ${ID}
 ]

# LOCAL DEFINITIONS for step '11'
ID = $UpperCylinder
beadtype = 3

11: [
    % Create atoms of type ${beadtype} for ${ID} ${style} (https://docs.lammps.org/create_atoms.html)
    create_atoms ${beadtype} region ${ID}
 ]

12: [
    # ===== [ BEGIN GROUP SECTION ] =====================================================================================
    group 	 lower 	type 	 1
    group 	 solid 	type 	 1 2 3
    group 	 fixed 	type 	 1
    group 	 middle 	type 	 2
    group 	 movable 	type 	 2 3
    group 	 upper 	type 	 3
    
    # ===== [ END GROUP SECTION ] =======================================================================================
    
    
    # [1:b1] PAIR STYLE SMD
    pair_style      hybrid/overlay smd/ulsph *DENSITY_CONTINUITY *VELOCITY_GRADIENT *NO_GRADIENT_CORRECTION &
    smd/tlsph smd/hertz 1.5
    
    # [1:b1 x 1:b1] Diagonal pair coefficient tlsph
    pair_coeff      1 1 smd/tlsph *COMMON 1000 10000.0 0.3 1.0 2.0 10.0 1000.0 &
    *STRENGTH_LINEAR_PLASTIC 1000.0 0 &
    *EOS_LINEAR &
    *END
    
    # [2:b2 x 2:b2] Diagonal pair coefficient tlsph
    pair_coeff      2 2 smd/tlsph *COMMON 1000 5000.0 0.3 1.0 2.0 10.0 1000.0 &
    *STRENGTH_LINEAR_PLASTIC 500.0 0 &
    *EOS_LINEAR &
    *END
    
    # [3:b3 x 3:b3] Diagonal pair coefficient tlsph
    pair_coeff      3 3 smd/tlsph *COMMON 1000 40000.0 0.3 1.0 2.0 10.0 1000.0 &
    *STRENGTH_LINEAR_PLASTIC 4000.0 0 &
    *EOS_LINEAR &
    *END
    
    # [1:b1 x 2:b2] Off-diagonal pair coefficient (generic)
    pair_coeff      1 2 smd/hertz 250.0000000000001
    
    # [1:b1 x 3:b3] Off-diagonal pair coefficient (generic)
    pair_coeff      1 3 smd/hertz 250.0000000000001
    
    # [2:b2 x 3:b3] Off-diagonal pair coefficient (generic)
    pair_coeff      2 3 smd/hertz 125.00000000000003
    
    # ===== [ END FORCEFIELD SECTION ] ==================================================================================
 ]

13: [
    group all union lower middle upper
    group external subtract all middle
 ]

14: velocity all set 0.0 0.0 0.0 units box
15: fix fix_lower lower setforce 0.0 0.0 0.0
16: fix move_upper upper move wiggle 0.0 0.0 ${amplitude} ${period} units box
17: fix dtfix tlsph smd/adjust_dt ${dt}
18: fix integration_fix tlsph smd/integrate_tlsph

19: [
    compute S all smd/tlsph_stress
    compute E all smd/tlsph_strain
    compute nn all smd/tlsph_num_neighs
 ]

20: [
    dump dump_id all custom ${dumpdt} ${dumpfile} id type x y z vx vy vz &
    c_S[1] c_S[2] c_S[4] c_nn &
    c_E[1] c_E[2] c_E[4] &
    vx vy vz
 ]

21: dump_modify dump_id first yes

22: [ 
    thermo ${thermodt}
    thermo_style custom step dt f_dtfix v_strain
 ]

23: run ${runtime}
"""
Dall3 = dscript.parsesyntax(Dcode)
print(Dall3.do(verbose=False))


# %% Illustration of overrides
Dall3.DEFINITIONS.runtime = 1e4  # global definitions (note the uppercase)
Dall3[-1].definitions.runtime = 2e5 # local definitions (higher precedence)
print(Dall3[-1].do()) # the result is run 200000.0