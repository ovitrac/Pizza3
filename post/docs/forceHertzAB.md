# forceHertzAB()

The `forceHertzAB` function calculates the Hertz contact forces between two sets of atoms, namely atoms A and B. It models the physical interaction between these particles according to Hertz contact theory.

**Function Signature:**
```matlab
[FAB, nAB] = forceHertzAB(XA, XB, config, verbose)
```

**Inputs:**
- `XA`: An `nA x 3` matrix representing the coordinates of atoms A.
- `XB`: An `nB x 3` matrix representing the coordinates of atoms B.
- `config`: A 2x1 structure array with fields:
  - `R`: The radius of particles.
  - `E`: The elasticity modulus.
  Example: `config = struct('R',{1 1},'E',{1e6 1e6})`
- `verbose` (Optional): A flag for verbosity control (not explicitly defined in the provided description).

**Outputs:**
- `FAB`: If only one output is provided, `FAB` is an `(nA*nB) x 3` matrix of Hertz forces.
- `FAB` and `nAB`: If two outputs are provided, `FAB` is an `(nA*nB) x 1` vector of force magnitudes, and `nAB` is an `(nA*nB) x 3` matrix of coordinates of unitary direction vectors AB.

**Remarks:**
- The function is vectorized, and this may generate Overflow/OutOfMemory errors, as mentioned in the TODO list within the code comments. An iterative version with automatic switching must be implemented to overcome this potential issue.
- A revision history is included in the comments, detailing the renaming of the function, updating the force Hertz equation, an additional delta calculation step, and wrapping particles along the x direction.

**Usage Example:**
```matlab
config = struct('R',{1 1},'E',{1e6 1e6});
XA = [1 2 3; 4 5 6]; % Example coordinates for atoms A
XB = [7 8 9; 10 11 12]; % Example coordinates for atoms B
[FAB, nAB] = forceHertzAB(XA, XB, config);
```

**See Also:**
- Other related functions are `forceHertz` and `forceLandshoff`.

The `forceHertzAB` function is particularly relevant for simulating pairwise interactions between two different groups of particles, offering precise control over the mechanical properties of these particles. It can be a useful component in multi-body simulations, granular materials modeling, or molecular dynamics studies.



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