# `forceLandshoff` Function Documentation

## Function Overview

The `forceLandshoff` function calculates the Landshoff interaction forces between fluid particles based on their positions, velocities, and a provided neighborhood list. This function is particularly useful in fluid dynamics simulations where particle interactions determine the system's behavior.

## Usage

```matlab
F = forceLandshoff(X, vX [,V, config, verbose])
[F, W, n] = forceLandshoff()
```

## Parameters

- **X**: `nX x 3` array of coordinates of atoms.
- **vX**: `nX x 3` array of velocity components.
- **V**: Optional. `nX x 1` cell array containing indices of neighbors within a cutoff distance (output of `buildVerletList`).
- **config**: Optional. Structure containing simulation parameters such as gradient kernel, smoothing length, speed of sound, density, mass, and volume.
- **verbose**: Optional. Boolean flag to control verbosity of the output for debugging purposes.

## Outputs

- **F**: If a single output is provided, `nX x 3` vector of Landshoff forces.
- **W**: If two outputs are provided, `nX x 9` array representing virial stress tensor components (reshape `W(i)`, `3, 3` to recover the matrix).
- **n**: `nX x 3` array of normal vectors.

## Algorithm Details

### Initialization and Configuration

- Initializes default values for simulation parameters like smoothing length, density, mass, etc., and adjusts these based on input `config` if provided.
- Verifies input consistency and dimensions.
- Prepares for virial stress calculation if required by the number of function outputs.

### Force Calculation Loop

- Iterates over each particle, calculating forces based on the relative position and velocity vectors between the particle and its neighbors identified in the Verlet list.
- Employs a highly vectorized approach to minimize computational overhead and improve performance.
- Applies a conditional model where the interaction force is calculated only if the relative velocity is directed towards the particle, representing an approaching scenario commonly found in shock tube problems.
- Utilizes an analytical form of the kernel gradient function specified in `config` for force calculation.

### Post-Processing

- Calculates the norm of the force vector for each particle and normalizes it to derive the direction.
- If virial stress output is requested, computes the stress tensor based on the interaction forces and the geometric configuration of particle pairs.

## Example

```matlab
matlabCopy code% Define coordinates and velocities
X = [0,0,0; 1,0,0; 0,1,0];
vX = [0,0,0; 0,0,1; 0,1,0];

% Optional: Define neighbors manually or use buildVerletList function
V = {[2;3], [1;3], [1;2]};

% Configuration for interaction calculations
config = struct('h', 0.1, 'c0', 10, 'rho', 1000, 'mass', 1, 'vol', 1);

% Calculate forces
[F, W, n] = forceLandshoff(X, vX, V, config, true);
disp('Forces:');
disp(F);
disp('Virial Stress Tensor:');
disp(W);
disp('Normal Vectors:');
disp(n);
```