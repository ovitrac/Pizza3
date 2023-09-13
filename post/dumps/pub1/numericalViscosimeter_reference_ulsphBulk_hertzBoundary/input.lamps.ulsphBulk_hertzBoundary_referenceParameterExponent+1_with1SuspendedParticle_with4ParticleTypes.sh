#!/bin/bash

#PBS -l myhpc_cunit=Profile=c5.24xlarge:Topology=hton:KeepForever=false:MaxIdleHourPercent=22
#PBS -N in.ulsphBulk_hertzBoundary_referenceParameterExponent+1_with1SuspendedParticle_with4ParticleTypes
#PBS -q parallel
#PBS -l select=48
#PBS -o localhost:/fsx/data/MaterialScience/Midas/inrae/Viscosimeter_SMJ_V6/Production/numericalViscosimeter_reference_ulsphBulk_hertzBoundary
#PBS -e localhost:/fsx/data/MaterialScience/Midas/inrae/Viscosimeter_SMJ_V6/Production/numericalViscosimeter_reference_ulsphBulk_hertzBoundary

echo "START..."
/bin/date
mkdir DUMPDESTINATION
. /apps/spack-gcc/0.19.0/share/spack/setup-env.sh
spack load lammps 2> >(grep -v 'Missing dependency not in database')

cd /fsx/data/MaterialScience/Midas/inrae/Viscosimeter_SMJ_V6/Production/numericalViscosimeter_reference_ulsphBulk_hertzBoundary
mpirun -np 48 lmp -in in.ulsphBulk_hertzBoundary_referenceParameterExponent+1_with1SuspendedParticle_with4ParticleTypes

/bin/date
echo "END..."




