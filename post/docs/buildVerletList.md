#buildVerletList()

[[_TOC_]]

## Overview

The `buildVerletList` function constructs a Verlet list, a data structure commonly used in molecular dynamics simulations to store neighbor information. It can be employed to identify particles within a given cutoff distance, enabling efficient force calculations. The function is equipped to work with 3D grid systems, providing functionality for exclusion checks, grid management, and flexible options through configuration.

#### Background

In molecular dynamics simulations, one of the most computationally demanding tasks is the calculation of forces between pairs of particles. The force is typically calculated using a potential function that depends on the distance between particles. However, in systems with a large number of particles, calculating the distances between all pairs can be expensive.

The Verlet list approach addresses this problem by creating a list of "neighbors" for each particle. The neighbors are those particles within a specified cutoff distance, and they are the ones that contribute significantly to the force on a given particle.

#### Key Concepts

- **Cutoff Radius**: A critical parameter that determines which particles are considered neighbors. Particles beyond this distance do not contribute significantly to the forces and are ignored.
- **Grid Management**: The function can optionally manage data on a 3D grid, dividing the space into cells. By searching only nearby cells, the number of distance calculations can be further reduced.
- **Exclusion Checks**: The ability to exclude certain particles from search or being considered as neighbors adds flexibility for specific use cases like atomistic simulations.



> Further reading:
>
>  https://en.wikipedia.org/wiki/Verlet_list
>
> https://www.sciencedirect.com/science/article/pii/001046559090007N

## Syntax

```matlab
[verletList, cutoffout, dminout, config, distout] = buildVerletList(X, cutoff, sorton, nblocks, verbose, excludedfromsearch, excludedneighbors)
```

## Inputs

- `X`: (n x 3 matrix) Contains the coordinates of particles. It can be one of the following:
  - A table with columns 'x', 'y', 'z'.
  - A cell `{Xgrid, X}` to search the neighbors `X` around `Xgrid`.
- `cutoff`: The cutoff distance for building the Verlet list.
  - Default: distribution mode (1000 classes).
- `sorton`: Flag to force the Verlet list to be sorted in increasing order.
  - Default: true.
- `nblocks`: Number of blocks to reduce the amount of memory required (typically max 8 GB).
- `verbose`: Set it to false to remove messages.
- `excludedfromsearch`: (nx1 logical array) True if the coordinate does not need to be included in the search.
- `excludedneighbors`: (nx1 logical array) True if the coordinate is not a possible neighbor.

## Outputs

- `verletList`: (n x 1 cell) Coding for the Verlet list. `verletList{i}` lists all indices `j` within the cutoff distance. If `sorton` is used, `verletList{i}(1)` is the closest neighbor.
- `cutoff`: Cutoff distance as provided or estimated.
- `dmin`: Minimum distance (off-diagonal term).
- `config`: Configuration structure to be used with `updateVerletList()`.
- `distances`: Pair distance matrix (equals NaN if `nblocks > 1`).

## Remarks

- The function is capable of working with grid points and can efficiently handle large-scale data using blocks.
- In DEBUG mode, the function compares results with and without blocks for internal validation.
- Extensive error handling and default assignment are implemented to ensure robustness.

## Example

```matlab
matlabCopy codeX = rand(1000, 3); % Generate random 3D coordinates for 1000 particles
cutoff = 0.1; % Define a cutoff distance
[verletList, ~, ~, ~, ~] = buildVerletList(X, cutoff); % Build the Verlet list
```

This will return the Verlet list for the given coordinates and cutoff distance.