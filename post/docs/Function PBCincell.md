# Function: PBCincell

## Purpose

`PBCincell` adjusts the coordinates of particles to ensure that they are within the specified dimensions of a simulation box, taking into account the periodicity of the box. This function is useful in molecular simulations, material science, and any domain where periodic boundary conditions (PBC) are applied to model infinite systems in a finite computational domain.

## Usage

```
matlabCopy code
Xincell = PBCincell(X, box, PBC)
```

## Input Arguments

- `X` (nx2 or nx3 matrix): Represents the coordinates of `n` particles in a 2D or 3D space, respectively. Each row corresponds to a particle, and each column corresponds to a coordinate dimension.
- `box` (2x2 or 3x2 matrix): Defines the dimensions of the simulation box. For each dimension `i`, the box spans from `box(i,1)` to `box(i,2)`.
- `PBC` (1x2 or 1x3 boolean array): Indicates the periodicity of the box dimensions. `PBC(i)` is `true` if the `i`th dimension is periodic, implying that the simulation box repeats along this dimension.

## Output Arguments

- `Xincell` (nx2 or nx3 matrix): Contains the adjusted coordinates of the `n` particles, ensuring all coordinates are within the box dimensions, considering the periodic boundary conditions.

## Description

The `PBCincell` function adjusts the coordinates of particles in a simulation, ensuring they remain within the specified bounds of a simulation box, considering the periodic nature of certain dimensions. This adjustment is crucial in simulations where particles may move across the boundaries of the simulation box and need to be repositioned within the box to maintain a continuous simulation space.

The function operates by looping through each dimension of the input coordinates. If a dimension is marked as periodic in the `PBC` array, the function calculates the size of the box in that dimension and uses the modulo operation to wrap the coordinates within the box dimensions. This approach ensures that all particle coordinates are "in cell," i.e., within the designated simulation space.

## Example

Consider a 2D simulation box with dimensions [0,10][0,10] in the �*x*-axis and [0,5][0,5] in the �*y*-axis, where both dimensions are periodic. For a set of particle coordinates:

```
matlabCopy codeX = [11.5, 2.5; -0.5, 4.5; 10.5, 6.5];
box = [0, 10; 0, 5];
PBC = [true, true];
```

Applying `PBCincell` yields the coordinates wrapped within the box dimensions:

```
matlabCopy code
Xincell = PBCincell(X, box, PBC);
```

`Xincell` will contain the adjusted coordinates, ensuring all particles are within the specified box dimensions, accounting for the periodic boundary conditions.

## References

- Understanding Molecular Simulation, Daan Frenkel and Berend Smit, Academic Press.
- Periodic Boundary Conditions in Molecular Simulations, M. Allen and D. Tildesley, Clarendon Press.

## Revision History

- MS 3.0 | 2024-03-16 | INRAE\han.chen@inrae.fr, INRAE\Olivier.vitrac@agroparistech.fr | Initial release.

## See Also

- `PBCgrid`
- `PBCgridshift`
- `PBCimages`
- `PBCimageshift`
- `PBCincell`