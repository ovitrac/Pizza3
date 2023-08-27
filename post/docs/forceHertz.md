# forceHertz()

The `forceHertz` function calculates the Hertz contact forces for a collection of atoms. The Verlet list, partitioned coordinates, and configuration parameters are used to compute these forces, simulating interactions between particles in a physical system.

**Function Signature:**
```matlab
[F,nout] = forceHertz(X,V,config,verbose)
```

**Inputs:**
- `X`: An `nX x 3` matrix representing the coordinates of atoms.
- `V`: An `nX x 1` cell array (output of `partitionVerletList`). Each `V{i}` includes all atoms that are not of the same type as `i`.
- `config`: A 2x1 structure array with fields:
  - `R`: The radius of particles.
  - `E`: The elasticity modulus.
  Example: `config = struct('R',{1 1},'E',{1e6 1e6})`
- `verbose` (Optional): A flag for verbosity control (not explicitly defined in the provided description).

**Outputs:**
- `F`: If only one output is provided, `F` is an `nX x 3` vector of Hertz forces, with `F{i} = mi x 3` forces.
- `F` and `nout`: If two outputs are provided, `F` is an `nX x 1` vector of Hertz force magnitudes, and `nout` is an `nX x 3` matrix of normal vectors.

**Remarks:**

- The function assumes that the Verlet list `V` has been partitioned.
- The description of the function includes a revision history, detailing changes to the implementation, including a rename and an update to the force Hertz equation as set in the SMD source code of LAMMPS.
- The `verbose` input, mentioned in the function signature, is not detailed in the comments, so the behavior related to this input remains unclear.

**Usage Example:**
```matlab
config = struct('R',{1 1},'E',{1e6 1e6});
V = partitionVerletList(...); % Example Verlet list partitioning
X = [1 2 3; 4 5 6]; % Example coordinates
[F, nout] = forceHertz(X, V, config);
```

The function provides a mathematical model to calculate forces between particles based on the Hertz contact theory, which is useful in simulations involving granular and particle-based systems.



## THEORY

##### Interaction between fluids and solids (rigid or deformable)

Due to the lack of resolution below particle size, the no-slip condition cannot be enforced on curved and movable solid-fluid interfaces with sufficient accuracy. A weakest but more general condition is enforced by setting a <kbd>Hertzian contact</kbd> model between particles of different kinds and obeying different physics. The  Hertz contact model the repulsive normal force between two particles when they come into contact by assuming they deform as elastic spheres. The resulting force is based on the deformation (overlap) of the two particles, denoted $i$ and $j$, with radii $R_i$ and $R_j$, respectively:
$$
\mathbf{f_{ij}^{Hertz}}\left(r\right)=\sqrt{E_iE_j}\sqrt{\left(r_{cut}-r\right)\frac{R_iR_j}{r_{cut}}}\;\mathrm{when}\;r<r_{cut}\;\mathrm{otherwise}\;0 \\
\mathrm{with}\;r_{cut}=R_i+R_j
$$
 The contact stiffness of each particle, $E_i$ and $E_j$ determine the intensity of the repulsion. This force is added to the balance of forces of each particle. It controls the non-penetration of objects and enforces a somewhat no-slip condition for sufficiently well packaged particles as shown in **Figure 9a**.

| (a) Domain boundary                                          | (b) Hertz contacts                                           |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| <img src="assets/image-20230408133226524.png" alt="image-20230408133226524" style="zoom:25%;" /> | <img src="assets/image-20230408133311860.png" alt="image-20230408133311860" style="zoom:25%;" /> |

**Figure 1.** Example of Implementation of pair interactions between a fluid (blue) and a rigid wall (gray).