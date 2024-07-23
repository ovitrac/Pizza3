# Billy_results_template Documentation

## Overview

This document outlines the functionality and usage of a MATLAB script designed for analyzing fluid dynamics simulations. The script focuses on the distribution and movement of particles or beads in a fluid environment, leveraging data from Billy's paper 2 simulations.

## Revision History

- **2024/03/07**: Implementation of reverse streamlines, streamline binning from initial positions, and subsampling.
- **2024/03/12**: Implementation of bead distribution along streamlines.
- **2024/03/16**: Major update, forked from `Billy_results_template.m` with Periodic Boundary Conditions (PBC) adjustments.
- **2024/03/17 to 2024/03/27**: Continuous development including the implementation of density correction, force contours around objects, prefetch management, and sensitivity challenge tests.

## Features

1. **Environment Setup**: Initialization of the simulation environment, including output and prefetch folders.
2. **Data Retrieval**: Configuration for loading simulation data with support for selective copying if original data roots are available.
3. **Simulation Analysis**: Processing of simulation data to derive crucial parameters like bead sizes, timestep intervals, and spatial distributions.
4. **Frame Selection & Prefetch Management**: Support for selective analysis based on `tframe` intervals and efficient data handling through prefetching.
5. **Streamline and Bead Distribution Analysis**: Enhanced with sensitivity challenge tests and fixes for streamline processing under specific conditions.
6. **Visualization**: Extensive capabilities for generating visual representations of the simulation's dynamics.

## Usage

### Setting Up the Environment

```matlab
matlabCopy code% Clear workspace and initialize folders
close all;
clearvars -except tframe tframelist RESETPREFETCH;
outputfolder = fullfile(pwd, 'preproduction');
prefetchfolder = fullfile(pwd, 'prefetch');
if ~exist(outputfolder, 'dir'), mkdir(outputfolder); end
if ~exist(prefetchfolder, 'dir'), mkdir(prefetchfolder); end
```

### Configuring Data Paths

```matlab
matlabCopy code% Determine the root directory for simulation data
originalroot = '/media/olivi/T7 Shield/Thomazo_V2';
if exist(originalroot, 'dir')
    root = originalroot;
    copymode = true; % Enables selective copying of data
else
    root = fullfile(pwd, 'smalldumps');
    copymode = false;
end
```

### Processing Simulation Data

Ensure you have the necessary simulation data within the specified `root` directory. The script supports different configurations and viscosity models, allowing for a comprehensive analysis of the fluid dynamics simulation.

### Prefetch Management

```matlab
matlabCopy code% Check for existing prefetch files to avoid redundant processing
if ~exist('RESETPREFETCH', 'var'), RESETPREFETCH = false; end
prefetchvar = @(varargin) fullfile(prefetchfolder, sprintf('t%0.4f_%s.mat', tframe, varargin{1}));
isprefetch = @(varargin) exist(prefetchvar(varargin{1}), 'file') && ~RESETPREFETCH;
```

This mechanism enhances efficiency by skipping already processed frames if prefetch files exist, thereby saving computational resources and time.

### Copy Files (if possible)

This section is conditional on the `copymode` flag, indicating whether the script should attempt to copy prefetch files from a source to a local directory. This is particularly useful for reducing data retrieval times for simulations that have been pre-processed or are being analyzed across different machines.

```matlab
matlabCopy codeif copymode
    % Code to copy prefetch files from the source to the local directory
end
```

### Estimating Bead Size from the First Frame

Estimating the size of beads (or particles) is crucial for accurate density calculations and fluid dynamics analysis. The script makes an initial estimate assuming beads are uniformly distributed, then refines this estimate based on the minimum distance between particles, ensuring realistic physical representation.

```matlab
matlabCopy code% Initial estimate of bead volume and size
Vbead_guess = prod(boxdims) / natoms;
rbead_guess = (3 / (4 * pi) * Vbead_guess)^(1 / 3);
```

### Loading the Frame Closest to Specified Simulation Time

This step involves selecting the simulation frame that matches or is closest to the user-specified time (`tframe`). This selection is crucial for analyzing dynamic changes in the simulation at specific intervals.

```matlab
matlabCopy code% Load the simulation frame closest to the specified tframe
iframe = nearestpoint(tframe, times); % Find the closest index
Xframe = lamdumpread2(dumpfile, 'usesplit', [], timesteps(iframe)); % Load the data
```

### Interpolating the Velocity Field at `z = ztop`

This section calculates the velocity field at a specific height (`ztop`) within the simulation domain. It involves interpolating the velocities of fluid particles to a grid at this height, taking into account the periodic boundary conditions to simulate infinite domain behavior accurately.

(`Box` is the the full box of simulation. `viewbox` is the layer between ztop-2h and ztop+2h. `XYZ/vXYZ/XYZs/rhobeadXYZ` extract the information of atoms inside viewbox. Then force `PBCincell` for XYZ and XYZs and add `PBCimages`. Create interpolation grid, interpolate 3D velocity and density on the grid, add `PBCgrid`. )

```matlab
matlabCopy code% Interpolate velocity field at the specified z = ztop
v3XYZgrid = interp3SPHVerlet(XYZwithImages, vXYZwithImages, XYZgrid, VXYZ, W, VbeadXYZwithImages); % 3D velocity interpolation
```

### Plotting the Velocity and Density Fields

After calculating the velocity and density fields, the script generates several plots to visualize these fields at the specified frame. This includes a mesh plot showing the velocity magnitude across the grid and a quiver plot overlaying velocity vectors on the field.

```matlab
matlabCopy code% Plotting velocity magnitude and direction
figure, mesh(XwPBC, YwPBC, vXYZPBC), axis equal, view(2), colorbar, title(sprintf('t=%0.3f s - velocity (m/s)', tframe));
figure, imagesc(xwPBC, ywPBC, vXYZPBC), axis tight, axis equal, colorbar, title(sprintf('t=%0.3f s - velocity magnitude (m/s)', tframe));
```

These visual representations are pivotal for understanding the fluid dynamics at play, offering insights into flow patterns, turbulence, and interactions between the fluid and embedded objects within the simulation domain.

## Streamline Analysis and Bead Distribution

### Generating Streamlines

The script computes streamlines in the fluid simulation from both bottom-to-top (UP) and top-to-bottom (DOWN) perspectives, effectively mapping fluid flow paths through the simulated domain. These streamlines are then used to distribute beads, representing fluid particles or tracer particles within the flow.

- **Streamline Configuration**: Determines the start points for streamline generation based on the grid boundaries and a specified step size. The streamlines are generated in multiple generations, with a horizontal shift applied every other generation to enhance coverage and reduce gaps in streamline distribution.

```matlab
matlabCopy code% Configure and generate streamlines
boundaries = [nearestpoint(double(xw([1,end])), double(xwPBC)),
              nearestpoint(double(yw([1,end])), double(ywPBC))];
step = 8;
```

- **Streamline Generation**: For each generation, streamlines are generated upwards (UP) and downwards (DOWN), with adjustments for horizontal shifts. These are then combined and filtered based on validity criteria to ensure meaningful analysis.

```matlab
matlabCopy code% Generative process for streamlines
for igen = 1:ngenerations
    % Adjustments for horizontal shift and streamline generation
    xshift = double(mod(igen-1,2)*(xwPBC(indxstreamline(2))-xwPBC(indxstreamline(1))));
end
```

### Distributing Beads Along Streamlines

After streamlines are established, beads are distributed along these paths to simulate the presence and movement of particles within the fluid flow. This distribution considers Periodic Boundary Conditions (PBC) and the separation distance between streamlines to ensure an even and realistic spread of particles.

- **Bead Distribution**: Beads are placed along the CELL-tagged streamlines, taking into account the streamline generation and horizontal shifts to fill the simulated space evenly.

```matlab
matlabCopy code% Distribute beads along CELL-tagged streamlines
traj = fillstreamline2(verticesCELL, XwPBC, YwPBC, vxXYZPBC, vyXYZPBC, rLagrangian, 0);
```

### Removing Duplicated Beads

To maintain physical accuracy in the simulation, beads that are too closely spaced (indicating overlap) are identified and removed. This process is particularly crucial for beads distributed along overlapping streamlines or within close proximity due to PBC effects.

- **Overlap Removal**: Identifies and removes beads that violate the minimum separation distance criterion, ensuring that the simulation remains realistic and avoids physically impossible overlaps.

```matlab
matlabCopy code% Remove duplicated beads to prevent overlap
for i = 1:ntraj
    for j = 1:ntraj
        if i ~= j
            dij = pdist2(XYZbeadsPBC{i}, XYZbeadsPBC{j}(indj,:));
            XYZbeadsPBC{j}(indj(any(dij < rLagrangian * sqrt(2), 1)), :) = NaN;
        end
    end
end
```

### Visualization and Analysis

The script provides extensive visualization features, plotting both the velocity and density fields along with the streamlines and the distributed beads. These visualizations serve to illustrate the flow dynamics within the simulation, highlighting areas of interest such as high-velocity regions, density variations, and the interaction between fluid and solid objects.

- **Control Plots**: Visualizes the computed streamlines and bead distributions, using color coding to differentiate between generations and streamline indices. This aids in visually assessing the simulation's accuracy and the effectiveness of the streamline generation and bead distribution algorithms.

```matlab
matlabCopy code% Visualization of streamlines and bead distributions
figure, hold on;
colors = tooclear(jet(ntraj));
for itraj = 1:ntraj
    plot(XYZbeadsPBC{itraj}(:,1), XYZbeadsPBC{itraj}(:,2), 'o', 'markerfacecolor', colors(itraj,:), 'markeredgecolor', colors(itraj,:));
end
```

# Density Calculation and Pressure Analysis

## Density Estimation

The script progresses to calculate the density at specific points in the simulation. This step is crucial for understanding the fluid's behavior and interaction with embedded objects. Here's how it's done:

### Preparing Data

- **Periodic Boundary Conditions (PBC)**: Ensures that beads considered in the density calculation respect the periodicity of the simulation domain.
- **Verlet List Creation**: Utilizes Verlet lists for efficient neighborhood search operations, enabling rapid density calculations.

### Density and Mass Calculations

- **Mass of Informed Beads**: Determines the mass of each bead based on the total volume of fluid represented in the simulation and the number of beads considered.
- **Kernel Density Estimation**: Employs a 2D SPH kernel to estimate the density at the center of informed beads. This step is critical for mapping density variations across the simulation domain.

```matlab
matlabCopy code% Calculate the volume and density of informed beads
Vbeadinformed = mbeadinformed ./ rhobeadinformed;
```

### Visualization

- **Control Figures**: Visualizes the density mapped to informed beads, comparing it against reference densities. This provides insights into the simulation's physical accuracy.

```matlab
matlabCopy code% Visual representation of bead densities
figure, viscircles(XYinformed, rLagrangian, 'color', 'g'), hold on;
viscircles(XYinformed, rbeadinformed, 'color', 'r');
```

## Pressure Analysis

Following density calculation, the script analyzes pressure around objects within the fluid. This involves identifying beads in contact with objects and calculating pressure based on their density.

### Object Contour Analysis

- **Contour Fitting**: Analyzes the contours of objects within the fluid by fitting circles and splines to identified contact points. This allows for an accurate representation of object boundaries.
- **Tangent and Normal Vectors**: Derives tangent and normal vectors along the object contours, essential for understanding the directionality of forces acting on the objects.

### Pressure Calculation

- **Pressure Estimation**: Utilizes the Tait equation to calculate pressure at the beads based on their density, facilitating the analysis of fluid pressure around embedded objects.

### Visualizing Pressure Distribution

- **Quiver Plots**: Depicts pressure vectors around objects, highlighting areas of high pressure and potential fluid-object interactions. This visualization is invaluable for analyzing the dynamic behavior of the fluid and its impact on embedded objects.

```matlab
matlabCopy code% Plot pressure vectors around objects
quiver(quiv.xy(:,1), quiv.xy(:,2), quiv.nxy(:,1), quiv.nxy(:,2), 3, 'color', 'k', 'LineWidth', 0.5);
```

## Production Figures

Finally, the script generates a series of figures for publication or further analysis:

- **Density Maps**: Shows the distribution of fluid density in the vicinity of objects.
- **Pressure Maps**: Highlights pressure variations around objects, providing insights into fluid-structure interactions.
- **Density Distribution**: Compares the distribution of calculated densities to reference values, offering a quantitative assessment of the simulation's physical fidelity.




The MATLAB script presented is an advanced tool designed for the detailed analysis and visualization of fluid dynamics simulations, particularly focusing on the interactions between fluid flows and embedded solid objects. This script not only processes simulation data to extract key fluid dynamics parameters but also applies sophisticated techniques to model and analyze the movement and distribution of particles within the fluid. Here's a summary and conclusion of the script's functionalities and its contributions to fluid dynamics research:

### Key Features and Functionalities

- **Data Extraction and Processing**: The script adeptly handles simulation data, extracting crucial information such as particle positions, velocities, and types, and sets the stage for in-depth analysis by preparing the simulation environment and managing data paths efficiently.
- **Velocity and Density Field Estimation**: By interpolating the velocity field at a specific plane and calculating the local density of particles, the script provides a detailed look into the flow characteristics and density variations within the fluid.
- **Streamline Generation and Bead Distribution**: It generates streamlines to map fluid flow paths and distributes beads along these lines, offering a particle-based view of fluid dynamics that accounts for periodic boundary conditions to simulate infinite domain behavior.
- **Density Calculation and Contact Analysis**: The script calculates densities at specific points and identifies beads in contact with solid objects, allowing for the exploration of fluid-structure interactions based on proximity and force estimations.
- **Pressure Analysis and Visualization**: Utilizing the calculated densities, the script proceeds to analyze pressure variations around solid objects, employing the Tait equation for relative pressure calculations. This analysis is crucial for understanding the forces at play and the potential impact on solid structures within the fluid.
- **Efficient Data Management**: Through the use of prefetching and selective processing, the script ensures efficient data handling, significantly reducing computational load and optimizing performance for large-scale simulations.
- **Advanced Visualization Capabilities**: The script excels in visualizing the complex dynamics of fluid simulations, from velocity fields and density distributions to pressure contours around embedded objects. These visualizations are not only essential for analysis but also for presenting findings in a comprehensible and impactful manner.

### Conclusion

This MATLAB script represents a significant contribution to the field of fluid dynamics research, offering a comprehensive toolkit for analyzing complex simulations with high precision and efficiency. By integrating advanced data processing techniques with sophisticated analysis and visualization methods, the script enables researchers to delve deeply into the mechanics of fluid flows and their interactions with solid objects. Such insights are invaluable for validating simulation models, exploring theoretical concepts in fluid dynamics, and guiding the design of experiments and engineering solutions in related fields.

