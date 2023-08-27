# forceLandshoff()

The `forceLandshoff` function calculates the Landshoff forces for a collection of atoms, considering their coordinates, velocities, and optional Verlet list. These forces are useful for fluid dynamic simulations, taking into account inter-particle interactions according to the defined configuration.

**Function Signature:**
```matlab
[F, n] = forceLandshoff(X, vX [,V, config, verbose])
```

**Inputs:**
- `X`: An `nX x 3` matrix representing the coordinates of atoms.
- `vX`: An `nX x 3` matrix representing the velocity components of atoms.
- `V` (Optional): An `nX x 1` cell array, output of `buildVerletList`, where `V{i}` includes the index of neighbors within the cutoff distance for atom `i`.
- `config` (Optional): A structure with fields:
  - `gradkernel`: Gradient kernel function (default value = `kernelSPH(h,'lucyder',3)`), depending on the radial distance `r`.
  - `h`: Smoothing length.
  - `c0`: Speed of sound.
  - `q1`: Coefficient `q1`.
  - `rho`: Density of the material.
- `verbose` (Optional): A flag for verbosity control (not explicitly defined in the provided description).

**Outputs:**
- `F`: If only one output is provided, `F` is an `nX x 3` matrix of Landshoff forces, where `F{i}` represents the `mi x 3` forces for atom `i`.
- `F` and `n`: If two outputs are provided, `F` is an `nX x 1` vector of Landshoff force magnitudes, and `n` is an `nX x 3` matrix of normal vectors.

**Remarks:**
- The function was revised on 2023-04-01 to sum forces instead of considering them individually, and a bug related to summation was fixed on 2023-04-02.
- There is also support to accept `X` as a table.
- Depending on how the function is used, the Landshoff forces can provide insights into the mechanical behavior and fluid dynamics of the system under consideration.

**Usage Example:**
```matlab
X = [1 2 3; 4 5 6]; % Example coordinates
vX = [0.1 0.2 0.3; 0.4 0.5 0.6]; % Example velocities
config = struct('h', 1, 'c0', 340, 'q1', 0.5, 'rho', 1e3); % Example config
[F, n] = forceLandshoff(X, vX, [], config);
```

The `forceLandshoff` function would be particularly useful for simulating the effects of force between particles in fluids, considering the velocity components and their spatial arrangement, and it can be a vital part of Smoothed Particle Hydrodynamics (SPH) or other computational fluid dynamics applications.



## THEORY

 

### 1. *Defining **viscosity** from collision theory*

In fact, kinetic viscosity, as self-diffusivity, is an emerging property associated with the diffusion of momentum between particles. Monaghan found the solution in earlier works of Von Neumann, suggesting that the trajectories of fluid particles were analogous to those of gas molecules in the kinetic theory of gases. Quoting Ref. [[BIR1961](#XXXXSPH04)] (page 8) "*Von Neumann himself decided to introduce "artificial viscosity" (dashpots) into the mass-spring system to simulate shocks, as being more efficient computationally than statistical averaging of the type used in the kinetic of gases. But no systematic exploration has been made of the analogy which seemed so interesting to von Neumann.*" The earliest statement of this daring but reasonable comparison for compressible fluids can be found in the paper of Von Neumann and Richtmyer published in 1950 on the numerical calculation of hydrodynamic shocks [[VON1950](#XXXXSPH06)]. The elements of rationale developed at Los Alamos during the Manhattan Project are justified hereafter.

The formalism combined with adequate solid particle definition may offer a potential strategy to control the propagation rate between particles. <kbd>Shock Waves</kbd> are associated with length scales comparable to a few molecular mean-free paths and, therefore, much smaller than SPH particles. They are usually simulated as <kbd>Rankine-Hugoniot conditions</kbd>, with discontinuous property jumps. By assuming a flow along $x$, The original approach adds a dissipative term $-q_2\rho h^2\frac{\partial v_x}{\partial y}\lvert\frac{\partial v_x}{\partial y}\rvert$, which is positive in compression and negative in tension, with $q_2$ a constant. This term controls the dilatational viscosity, also called bulk viscosity. Landshoff [[LAN1955](#XXXXSPH08)] added a term linear with the velocity gradient $\frac{\partial v_x}{\partial y}$, which scales as $q_1\rho h c_0\frac{\partial v_x}{\partial y}$, where $q_1$ is a constant and $c_0$ is the local speed of the sound. The characteristic length $h$ should be chosen commensurable to the particle size to dampen the shock rapidly and keep the jump inside the particle.



- [ ] ### 2. *The viscous pressure*

Monaghan and Gingold [[MON1983](#XXXXSPH07)] introduced the concept of viscous pressure, $\Pi_{ij}$, which is similar to Landshoff forces:
$$
\mathbf{F_i^D}=\sum_jm_j\nu_{ij}\frac{\mathbf{r_{ij}}\cdot\mathbf{v_{ij}}}{r_{ij}^2+0.01\overline{h_{ij}}^2}F_{ij}\mathbf{r_{ij}}
=-\sum_jm_j\Pi_{ij}F_{ij}\mathbf{r_{ij}}
\\
\mathrm{with}\; \nu_{ij}=\frac{q_1\overline{c_{ij}}\overline{h_{ij}}}{\overline{\rho_{ij}}}\;\mathrm{if}\;\mathbf{r_{ij}}\cdot\mathbf{v_{ij}}<0\;\mathrm{otherwise}\;0
$$
The force $\Pi_{ij}$ is <kbd>Galilean invariant</kbd> (*i.e.*, consistent across various inertial reference frames) and vanishes for rigid rotation (*i.e.*, it preserves angular momentum and remove spurious forces which could lead to artificial deformation or dissipation). The <kbd>pseudo-viscosity</kbd>, $\nu_{ij}$ produces a repulsive force when the particles $i$ and $j$ approach each other and vanishes when they recede from each other. In other words, the force is active in compression and not in rarefaction. It decreases non-physical results with nominally $C^0$ solutions (<kbd>Shock Waves</kbd>) by tunning $\nu_{ij}$. 

> In systems with homogeneous particles, the dynamic viscosity, $\eta$ is reads [[MON2005](#XXXXSPH03)]:
>
> $$
> \eta=q_1\frac{\rho h c_0}{\alpha_\eta}
> $$
>
> with $\alpha_\eta=8$ in 2D and $C^{te}=10$ in 3D.
>
> ****
>
> >  💡Alternative definitions of $\mathbf{F_i^D}$ have been proposed, possibly more accurate to reproduce simple shear flows, but none are more general than Landshoff and Richtmyer formulations in systems involving irregular packing. This condition arises in large inertial flows, wake flows, free surfaces, multiphasic flows or close to non-smooth walls due to the presence of particles representing walls. 
> >
> >  Very accurate shear stress descriptions have been proposed for almost incompressible flows. The model proposed by Morris *et al.* [[MOR1997](#XXXXSPH10)] gained popularity and is included in many packages. It has been designed for low Reynolds numbers but tolerates only one shear direction. In the same vein, the implementation of viscous boundary forces has been discussed and subjected to various implementations [[LI2022](#XXXXSPH11)].

