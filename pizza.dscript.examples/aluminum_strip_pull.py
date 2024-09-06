from pizza.dscript import dscript

# %% SYNOPSIS
# Example: Aluminum Strip Pull
# This example simulates the tensile loading of an aluminum strip.
# Original source: in.aluminum_strip_pull

aluminum_strip_pull_template = """# DSCRIPT SAVE FILE
####################################################################################################
# TLSPH example: Aluminum Strip Pull
####################################################################################################
{
    SECTIONS = ['INITIALIZE', 'CREATE_GEOMETRY', 'DISCRETIZATION', 'BOUNDARY_CONDITIONS', 'PHYSICS', 'OUTPUT', 'RUN'],
    section = 0,
    position = 0,
    role = "dscript instance",
    description = "Aluminum Strip Pull",
    userid = "ChatGPT",
    version = 2.0,
    verbose = False
}

# GLOBAL PARAMETERS
E=69.0             # Young's modulus for aluminum (GPa)
nu=0.33            # Poisson ratio
rho=2.7            # Initial mass density (g/cm^3)
q1=0.06            # Artificial viscosity linear coefficient
q2=0.0             # Artificial viscosity quadratic coefficient
hg=10.0            # Hourglass control coefficient
cp=0.9             # Heat capacity
l0=1.0             # Lattice spacing
h=2.01 * ${l0}     # SPH smoothing kernel radius
vel0=0.005         # Pull velocity
runtime=3000       # Simulation runtime
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

boundary_conditions: [
    region top block EDGE EDGE 9.0 EDGE EDGE EDGE units box
    region bot block EDGE EDGE EDGE -9.1 EDGE EDGE units box
    group top region top
    group bot region bot
    variable vel_up equal ${vel0} * (1.0 - exp(-0.01 * time))
    variable vel_down equal -v_vel_up
    fix veltop_fix top smd/setvelocity 0 v_vel_up 0
    fix velbot_fix bot smd/setvelocity 0 v_vel_down 0
]

physics: [
    pair_style smd/tlsph
    pair_coeff 1 1 *COMMON ${rho} ${E} ${nu} ${q1} ${q2} ${hg} ${cp} &
    *STRENGTH_LINEAR_PLASTIC 0.2 0.05 &
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
aluminum_strip_pull = dscript.parsesyntax(aluminum_strip_pull_template)
# Generate LAMMPS code
print(aluminum_strip_pull.script().do())