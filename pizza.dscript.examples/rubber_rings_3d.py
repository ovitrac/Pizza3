from pizza.dscript import dscript

# %% SYNOPSIS
# Example: Rubber Rings 3D
# This simulation demonstrates the deformation and interaction of rubber rings in 3D.
# Original source: in.rubber_rings_3d

rubber_rings_3d_template = """# DSCRIPT SAVE FILE
####################################################################################################
# TLSPH example: Rubber Rings 3D
####################################################################################################
{
    SECTIONS = ['INITIALIZE', 'CREATE_GEOMETRY', 'DISCRETIZATION', 'BOUNDARY_CONDITIONS', 'PHYSICS', 'OUTPUT', 'RUN'],
    section = 0,
    position = 0,
    role = "dscript instance",
    description = "Rubber Rings 3D",
    userid = "ChatGPT",
    version = 2.0,
    verbose = False
}

# GLOBAL PARAMETERS
E=1.0              # Young's modulus
nu=0.3             # Poisson ratio
rho=1.0            # Initial mass density
q1=0.06            # Artificial viscosity linear coefficient
q2=0.0             # Artificial viscosity quadratic coefficient
hg=10.0            # Hourglass control coefficient
cp=1.0             # Heat capacity
l0=1.0             # Lattice spacing
h=2.01 * ${l0}     # SPH smoothing kernel radius
vel0=0.005         # Pull velocity
runtime=2000       # Simulation runtime
skin=${h}          # Verlet list range
boxlength=10
boxdepth=0.1

initialize: [
    dimension 3
    units si
    boundary sm sm sm
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
    pair_style smd/tlsph
    pair_coeff 1 1 *COMMON ${rho} ${E} ${nu} ${q1} ${q2} ${hg} ${cp} &
    *STRENGTH_LINEAR &
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
rubber_rings_3d = dscript.parsesyntax(rubber_rings_3d_template)
# Generate LAMMPS code
print(rubber_rings_3d.script().do())