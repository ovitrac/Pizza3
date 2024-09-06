from pizza.dscript import dscript

# %% SYNOPSIS
# Example: Fluid-Structure Interaction
# This simulation demonstrates the coupling between fluid flow and deformable solids.
# Original source: in.fluid_structure_interaction

fluid_structure_interaction_template = """# DSCRIPT SAVE FILE
####################################################################################################
# TLSPH example: Fluid-Structure Interaction
####################################################################################################
{
    SECTIONS = ['INITIALIZE', 'CREATE_GEOMETRY', 'DISCRETIZATION', 'BOUNDARY_CONDITIONS', 'PHYSICS', 'OUTPUT', 'RUN'],
    section = 0,
    position = 0,
    role = "dscript instance",
    description = "Fluid-Structure Interaction",
    userid = "ChatGPT",
    version = 2.0,
    verbose = False
}

# GLOBAL PARAMETERS
E=1.0              # Young's modulus for solid
nu=0.3             # Poisson ratio
rho=1.0            # Initial mass density for fluid
q1=0.06            # Artificial viscosity linear coefficient
q2=0.0             # Artificial viscosity quadratic coefficient
hg=10.0            # Hourglass control coefficient
cp=1.0             # Heat capacity
l0=1.0             # Lattice spacing
h=2.01 * ${l0}     # SPH smoothing kernel radius
vel0=0.005         # Pull velocity
runtime=2000       # Simulation runtimes
skin=${h}          # Verlet list range
boxlength=10
boxdepth=0.1

initialize: [
    dimension 2
    units si
    boundary sm sm p
    atom_style smd
    atom_modify map array
    comm_modify vel yes
    neigh_modify every 10 delay 0 check yes
    newton off
]

create: [
    lattice sq ${l0}
    region box block -${boxlength} ${boxlength} -${boxlength} ${boxlength} -${boxdepth} ${boxdepth} units box
    create_box 1 box
    create_atoms 1 box
    group tlsph type 1
]

physics: [
    pair_style smd/ulsph
    pair_coeff 1 1 *COMMON ${rho} ${E} ${q1} ${cp} ${hg} &
    *EOS_LINEAR &
    *END
]

output: [
    compute S all smd/tlsph_stress
    compute nn all smd/tlsph_num_neighs
    dump dump_id all custom 10 dump.LAMMPS id type x y z vx vy vz &
    c_S[1] c_S[2] c_S[4] c_nn &
    vx vy vz
    dump_modify dump_id first yes
]

run_simulation: run ${runtime}
"""

# Generate the dscript object
fluid_structure_interaction = dscript.parsesyntax(fluid_structure_interaction_template)
# Generate LAMMPS code
print(fluid_structure_interaction.script().do())