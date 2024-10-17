# -*- coding: utf-8 -*-
"""
Principles of Coding with Pizza3 in Python for LAMMPS

This script demonstrates how to use Pizza3 to construct a complete LAMMPS input file for the simulation
of three stacked cylinders (lower, central, upper) modeled as hyperelastic materials. Each cylinder is
represented by a distinct bead type (1, 2, and 3), and the simulation is dynamically scripted to avoid 
external code snippets.

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
   
2. **S2: Customized Forcefields**  
   - Sets up a dynamic forcefield using the `dforcefield` class. 
   - Custom forcefield properties are applied to each of the three cylinders.
   
3. **S3: Customized Groups**  
   - Demonstrates how to manage groups of particles and combine groups using operations like union (`+`) and subtraction (`-`).

4. **S4a, S4b, S4c: Dynamics and Time Integration**  
   - Shows how to define movement for the upper cylinder and how to set up time integration using the `dscript` class.
   
5. **S5: Dump Instructions**  
   - Configures the trajectory dump, specifying which physical variables should be saved during the simulation.
   
6. **S6: Thermodynamic Output**  
   - Defines the thermodynamic output frequency and format using LAMMPS thermodynamic styles.
   
7. **S7: Running the Simulation**  
   - Executes the LAMMPS simulation with the defined run time.

**Compatibility:**
All scripts (including `script`, `pipescript`, `scriptobject`, and `scriptobjectgroup`) exhibit sufficient compatibility to be combined with operators. The pipe operator (`|`) is preferred as it facilitates reordering and the inclusion of local variables.

**Revision:**
Last revision: 2024-10-14

"""

# Dependencies
from pizza.script import script, scriptdata  # Import the base script and data structure classes
from pizza.dscript import dscript  # Dynamic script class to manage LAMMPS inputs dynamically
from pizza.group import group  # Group management for LAMMPS atoms or molecules
from pizza.region import region  # Region class to define physical simulation regions
from pizza.dforcefield import dforcefield  # Dynamic forcefield definitions for particles
from pizza.generic import generic  # Generic modules that can be used for custom properties


# %% Workshop Initialization
# Initialize the dscript object for managing the LAMMPS script.
# This acts as a container for the whole workshop.
R = dscript(name="LammpsWorkshop")


# %% S1a, S1b: Defining Simulation Box, Lattice, and Regions
# Goal:
#   Demonstrate the creation of the simulation box, lattice, and cylindrical regions using the `region` class.

# Define the simulation container (box), with boundaries and lattice settings.
R_container = region(
    name="SimulationBox",  # Name of the simulation box
    dimension=3,  # 3D simulation
    boundary=["f", "f", "f"],  # 'f' = fixed boundary conditions in all directions
    nbeads=3,  # Number of bead types in the simulation
    width=0.06, height=0.02, depth=0.06,  # Box dimensions in meters
    units="si",  # Using SI units for LAMMPS
    lattice_scale=0.0008271, lattice_style="sc",  # Define a simple cubic lattice
    lattice_spacing=0.0008271,  # Spacing of the lattice points
    separationdistance=0.0001  # Minimum separation distance between lattice points
)

# Define cylindrical regions for each of the three cylinders (lower, central, upper)
R_container.cylinder(name="LowerCylinder", dim="z", c1=0, c2=0, radius=0.03, lo=0.0, hi=0.005, beadtype=1)
R_container.cylinder(name="CentralCylinder", dim="z", c1=0, c2=0, radius=0.03, lo=0.005, hi=0.015, beadtype=2)
R_container.cylinder(name="UpperCylinder", dim="z", c1=0, c2=0, radius=0.03, lo=0.015, hi=0.02, beadtype=3)

# Generate LAMMPS script headers for initialization, lattice setup, and box setup
S1_headers = R_container.pscriptHeaders(what=["init", "lattice", "box"])  # Create initialization script
S1_core = R_container.pipescript()  # Core script for defining regions

# Output the headers and core for debugging and control
print('# HEADERS\n', S1_headers.do(printflag=False, verbose=False), sep="\n")
print(' \n# REGIONS\n', S1_core.do(printflag=False, verbose=False), sep="\n")

# Combine the header and core into one section S1
S1 = S1_headers | S1_core  # Use the pipe operator to combine the scripts
print(' \n# S1: HEADERS & REGIONS\n', S1.do(printflag=False, verbose=False), sep="\n")


# %% S2: Customized Forcefields
# This section defines and applies dynamic forcefields to each of the three cylinders using `dforcefield`.

# Specify additional modules if needed for the forcefield (in this case, generic)
additional_modules = [generic]

# Define a dynamic forcefield with basic properties (elastic, density, etc.)
dynamic_ff = dforcefield(
    base_class="solidfood",  # Base forcefield type (solid food, for example)
    beadtype=None,  # Beadtype will be assigned later
    userid="solid",  # Unique identifier for the forcefield instance
    additional_modules=additional_modules,  # Import additional forcefield behaviors from modules

    # Define physical properties of the forcefield
    rho=1.0e3,  # Density (kg/m^3)
    E=1e4,  # Young's modulus (Pa)
    nu=0.3,  # Poisson's ratio
    c0="0.1*sqrt(${E}/${rho})",  # Speed of sound
    sigma_yield="0.1*${E}",  # Yield stress
    hardening=0,  # No hardening
    q1=1.0,  # Artificial viscosity parameters
    q2=2.0,
    Hg=10.0,  # Hourglass control parameter
    Cp=1000.0,  # Specific heat capacity (J/kg·K)
    contact_scale=1.5,  # Contact stiffness scaling factor
    contact_stiffness="2.5*${c0}^2*${rho}"  # Hertzian contact stiffness
)

# Define forcefield properties for each cylinder using `scriptdata`
customff1 = scriptdata(E=1e4, rho=1000)  # Cylinder 1 (lower)
customff2 = scriptdata(E=5e3, rho=1000)  # Cylinder 2 (central)
customff3 = scriptdata(E=4e4, rho=1000)  # Cylinder 3 (upper)

# Apply the forcefield to each bead type and create script objects
b1 = dynamic_ff.scriptobject(beadtype=1, USER=customff1, name="b1", group=["lower", "solid", "fixed"])
b2 = dynamic_ff.scriptobject(beadtype=2, USER=customff2, name="b2", group=["middle", "solid", "movable"])
b3 = dynamic_ff.scriptobject(beadtype=3, USER=customff3, name="b3", group=["upper", "solid", "movable"])

# Combine the three script objects into one collection
collection = b1 + b2 + b3
S2 = collection.script(printflag=False, verbosity=1)
S2.name = "S2:forcefield"

# Output the forcefield definitions
print("\n# FORCEFIELDS\n", S2.do(printflag=False, verbose=False), sep="\n")


# %% S3: Customized Groups
# The group definitions are already handled within the `collection.script()` method.
# This section demonstrates additional group operations such as union and subtraction.

# Create a group container for additional group operations
G = collection.group_generator()

# Define a custom group "all" which includes all three cylinders (lower, middle, upper)
G.evaluate("all", G.lower + G.middle + G.upper)

# Create another group "external" which excludes the central (middle) cylinder
G.evaluate("external", G.all - G.middle)

# Generate the script for the "all" and "external" groups
Gall = G("all", "external")
S3 = Gall.script(verbose=False)
S3.name = "S3:customgroup"

# Output the custom group definitions
print("\n# CUSTOMIZED GROUPS\n", S3.do(printflag=False, verbose=False), sep="\n")


# %% S4a: Movable Objects (Upper Cylinder Movement)
# Define movement for lower (fixed) and upper (wingle) cylinders using dynamic scripting `dscript`.
# Three codelets are defined:  "moveinit", "movelower" and "moveupper"
# They can be set and checked via several shorthands

# Create the container of for the  dynamic script 
# All codelets share the same global variables (DEFINITIONS).
# Codelets are independent and their behavior are specifically managed via attributes.
# Only variables can be set at construction time.
move = dscript(name="S4a:move",  # Create a new dynamic script
               SECTIONS = ["DYNAMICS","move"], section = 4, position = None,
               description = "Movements of lower and upper cylinders ",
               verbose = True, # we keep comments
               amplitude=1.0e-3,  # Amplitude of movement (1 mm)
               period=1.0 # Period of movement (1 second)
             )

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
move.moveinit= """
# Set initial velocities to zero
velocity all set 0.0 0.0 0.0 units box # note box units
"""
# rapid control showing template and default attributes
move.moveinit


# CODELET "movelower" fixes the position of the lower cylinder
move.movelower = """
# Fix the lower cylinder to prevent movement
fix fix_lower lower setforce 0.0 0.0 0.0
"""

# CODELET "movelower" fixes the position of the lower cylinder
move.moveupper = """
# Apply periodic movement to the upper cylinder
fix move_upper upper move wiggle 0.0 0.0 ${amplitude} ${period} units box
"""
move.moveupper.eval = True  # Force evaluation of movement

print("\n# MOVABLE OBJECTS", move.do(printflag=False, verbose=True), sep="\n")


# %% S4b: Time Integration Setup
# we use a compact syntax, verbosity is removed
integration = dscript(name="S4b:timeintegration",
                      dt=0.1)  # Create the time integration script
integration.intinit = "fix dtfix tlsph smd/adjust_dt ${dt} # Adjust time increment dynamically"
integration.intinit.eval = True
integration.intset = "fix integration_fix tlsph smd/integrate_tlsph"  # Set up integration
print("\n# TIME INTEGRATION", integration.do(printflag=False, verbose=False), sep="\n")


# %% S4c: Trajectory Output Setup
trajectory = dscript(name="S4c:trajectoryoutput")  # Create trajectory output script
trajectory.compute = """
compute S all smd/tlsph_stress # Cauchy stress tensor
compute E all smd/tlsph_strain # Green-Lagrange strain tensor
compute nn all smd/tlsph_num_neighs # Number of neighbors for each particle
"""
print("\n# TRAJECTORY OUTPUT", trajectory.do(printflag=False, verbose=False), sep="\n")


# %% S4: Combine S4a + S4b + S4c
S4 = move + integration + trajectory  # Combine movement, integration, and output into one script
S4.name = "S4:dynamics"
print ("\n","-"*70,"S4 code which be saved with S4.save():","-"*70,S4.generator(),"-"*70,sep="\n")
print("\n# DYNAMICS", S4.do(printflag=False, verbose=False), sep="\n")


# %% S5: Dump Settings
S5 = dscript(name="S5:dump",
             dumpdt=50,
             dumpfile="$dump.LAMMPS")  # Set dump interval and file name
S5.dumpinit = """
dump dump_id all custom ${dumpdt} ${dumpfile} id type x y z vx vy vz & 
c_S[1] c_S[2] c_S[4] c_nn & 
c_E[1] c_E[2] c_E[4] & 
vx vy vz
"""
S5.dumpset = """
dump_modify dump_id first yes
"""


# %% S6: Thermodynamic Output
S6 = dscript(name="S6:thermo",
             thermodt = 100)  # Set thermodynamic output interval
S6.thermo = """
thermo ${thermodt}
thermo_style custom step dt f_dtfix v_strain
"""
S6.thermo.eval = True


# %% S7: Run the Simulation
S7 = dscript(name="S7:run",
             runtime = 5000)  # Set the simulation runtime (5000 steps)
S7.run = "run ${runtime}"
S7.run.eval = True


# %% Combine All Sections (S1, S2, S3, S4, S5, S6, S7)
Sall = S1 | S2 | S3 | S4 | S5 | S6 | S7  # Use pipe operator to combine all scripts
print("\n\n# ALL SCRIPTS", Sall.do(printflag=False, verbose=False), sep="\n")


# %% Write the final LAMMPS script to file
# The final LAMMPS script is written to a text file for execution.
Sall.write("tmp/example.txt", verbosity=1)