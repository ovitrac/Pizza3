# updateVerletList()

**Function**: `[verletList, configout] = updateVerletList(X, previousVerletList, config)`

**Purpose**: This function updates the Verlet list when the number of modified neighbors exceeds a predefined threshold. In molecular dynamics and particle simulations, a Verlet list is used to efficiently track particle interactions within a specific range. This function allows for the timely update of this list, considering changes in neighboring particles.

### Inputs:
1. `X`: `n x 3` updated positions of the particles.
2. `previousVerletList`: `n x 1` cell array representing the previous Verlet list, containing information about the neighboring particles for each particle.
3. `config`: Configuration structure output from the `buildVerletList` function. It includes:
   - `config.tolerance`: Tolerance level that determines the threshold for updating the list.
   - `config.nsamples`: Sets the number of samples considered when updating.

### Outputs:
- `verletList`: `n x 1` cell array representing the updated Verlet list.
- `configout`: Updated configuration structure to be used with future calls to `updateVerletList()`.

### Example Use:
The update of the Verlet list can be performed within a simulation loop, allowing the system to respond dynamically to changes in the particle positions. This continuous updating can enhance the efficiency and accuracy of force calculations in the simulation.

### Related Functions:
- `buildVerletList`: Constructs the initial Verlet list.
- `partitionVerletList`: Partitions the Verlet list based on type or other criteria.
- `selfVerletList`: Potentially related to handling specific self-interactions within the Verlet list.
- `interp3SPHVerlet`: Possibly an interpolation function utilizing the Verlet list in the context of SPH (Smoothed Particle Hydrodynamics) simulations.

This function integrates into a broader ecosystem of functions to manage and utilize Verlet lists in particle-based simulations. By dynamically updating the Verlet list, it enables more accurate and efficient computation of inter-particle interactions, which is essential for the simulation of complex systems such as fluids or granular materials.