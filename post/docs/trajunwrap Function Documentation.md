# `trajunwrap` Function Documentation

## Function Overview

The `trajunwrap` function unwraps the trajectory coordinates of atoms within a periodic simulation box after they have been wrapped due to periodic boundary conditions. It is specifically designed to efficiently handle large sets of atom coordinates and ensure that the continuous trajectories of atoms are accurately represented as they undergo displacements that might cause them to cross periodic boundaries.

## Usage

```matlab
trajunwrapped = trajunwrap(traj, box, PBC)
```

## Parameters

- **traj**: `nx2` or `nx3` array representing the trajectory coordinates of the `n` particles in 2D and 3D, respectively.
- **box**: `2x2` or `3x3` array specifying the dimensions of the periodic simulation box. The box spans along dimension `i` between `box(i,1)` and `box(i,2)`. It is assumed all trajectory values initially lie within these box limits.
- **PBC**: `1x2` or `1x3` flags (Boolean), where `PBC(j)` is `true` if the `j`-th dimension is periodic.

## Returns

- **trajunwrapped**: `nx2` or `nx3` array containing the unwrapped coordinates of the particles, reflecting their continuous trajectory across periodic boundaries.

## Description

This function calculates the differences between consecutive points in the trajectory to determine displacement. If a displacement in any dimension exceeds half the box length in that dimension (indicative of a wrap due to the periodic boundary), it is adjusted to reflect the true movement across the boundary. The function then cumulatively sums these adjusted displacements to compute the continuous, unwrapped trajectory.



## See Also

- `PBCimagesshift`
- `PBCgrid`
- `PBCgridshift`
- `PBCimages`
- `PBCincell`

## Examples

Here's a simple example of how to use `trajunwrap`:

```matlab
matlabCopy code% Define trajectory and box dimensions
traj = [1.0, 1.5; 9.5, 2.0; 0.1, 2.5];
box = [0, 10; 0, 3];  % Rectangular box with periodic boundaries
PBC = [true, false];  % Only the first dimension is periodic

% Unwrap the trajectory
trajunwrapped = trajunwrap(traj, box, PBC);
disp('Unwrapped Trajectory:');
disp(trajunwrapped);
```

