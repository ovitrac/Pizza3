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
Last revision: 2024-10-22

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
