# `unwrapPBC` Function Documentation

## Function Overview

The `unwrapPBC` function is designed to unwrap the coordinates of atoms within a periodic simulation box that have been wrapped due to periodic boundary conditions (PBC). The function leverages efficient, vectorized operations to handle large datasets and ensures that the continuous trajectories of atoms are accurately represented, especially when they undergo displacements that may cause them to cross periodic boundaries.

## Usage

```matlab
Xunwrapped = unwrapPBC(X, Pshift, box, PBC)
```

## Parameters

- **X**: `nx2` or `nx3` array containing the initial coordinates of the `n` particles in 2D or 3D, respectively.
- **Pshift**: `1x2` or `1x3` array specifying the translation applied to the coordinates, which will be subject to periodic wrapping.
- **box**: `2x2` or `3x3` array detailing the dimensions of the periodic simulation box. The box spans from `box(i,1)` to `box(i,2)` in each dimension `i`.
- **PBC**: `1x2` or `1x3` Boolean array (flags) indicating whether the j-th dimension is periodic (`true`) or not.

## Returns

- **Xunwrapped**: `nx2` or `nx3` array of unwrapped coordinates, reflecting the continuous trajectory of the particles across periodic boundaries.

## Description

This function unwraps the coordinates of atoms by first applying a translation and periodic wrapping through the `PBCincell` function. It then calculates the displacement caused by this translation and adjusts any displacements that exceed half the length of the box in any dimension (indicative of a wrap). These adjustments ensure that the unwrapped coordinates represent a true, continuous trajectory, even when atoms cross periodic boundaries.

## See Also

- `PBCimagesshift`
- `PBCgrid`
- `PBCgridshift`
- `PBCimages`
- `PBCincell`

## Example

Here is an example demonstrating how to use the `unwrapPBC` function:

```matlab
matlabCopy code% Define initial positions, a periodic shift, and box dimensions
X = [1.0, 1.5; 0.5, 2.0]; % Example in 2D
Pshift = [0.5, 0.0]; % Shift right by 0.5 units
box = [0, 3; 0, 3]; % Square box with sides of length 3
PBC = [true, false];  % Periodicity in first dimension only

% Unwrap the coordinates
Xunwrapped = unwrapPBC(X, Pshift, box, PBC);
disp('Unwrapped Coordinates:');
disp(Xunwrapped);
```