#!/bin/bash
. /apps/spack-gcc/0.19.0/share/spack/setup-env.sh

spack load lammps

mpirun -np 24 lmp -in in.ulsphBulk_hertzBoundary_referenceParameterExponent+1_with1SuspendedParticle_with4ParticleTypes
