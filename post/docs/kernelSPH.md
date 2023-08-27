# kernelSPH()

**Function**: `W = kernelSPH(h, type, d)`

**Purpose**: This function returns a smoothed particle hydrodynamics (SPH) kernel, utilized in various computational mechanics simulations within the LAMMPS software.

### Inputs:
1. `h`: The cutoff value.
2. `type`: The kernel name. Default is 'Lucy'.
3. `d`: The dimension.

### Output:
- `W`: A kernel function with respect to `r`.

### Specific Kernels:
- `lucy` and `lucydir`: Used for Morris calculation in the SPH source code of LAMMPS.
- `poly6kernel`: Used for ULSPH density calculation in SMD source code of LAMMPS.
- `cubicspline`: Used for ULSPH artificial pressure calculation in SMD source code of LAMMPS.
- `spikykernel`: Used for ULSPH and TLSPH force calculation in SMD source code of LAMMPS.

### TODO:
- There is a note to double-check the cubic spline kernel, as symengine is unable to generate code.

### Example Usage:
- `W = kernelSPH(1, 'lucy', 3)`

### Revision History:
- The function has been actively revised, with the latest addition being the `poly6kernel`, `cubicsplinekernel`, and `spikykernel` on 2023-04-03, as set in the SMD source code of LAMMPS.

### Related Functions:
- `interp3SPH`, `interp2SPH`, `packSPH`

### Context:
The function is part of a broader effort in computational fluid dynamics and can be leveraged in multiscale modeling, which might align with your interests in fluid dynamics applied to food transformation.

Feel free to ask if you need more specific details or explanations.