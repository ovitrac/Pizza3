# Workshop on Post-treatment (Suspended Particle in a Fluid as an Example)

In an SPH simulation in LAMMPS, information related to the state of the system at various points in time is typically stored in dump files. These files can contain data such as particle positions, velocities, and other desired thermodynamic quantities. Here is how to proceed with the post-treatment of such a dump file:

1. **Format**: The dump files might be in custom LAMMPS formats or more general formats like XYZ. You'll need to identify the format and what information is contained within the file.
2. **Reading the File**: Depending on the needs and the size of the data, you can use different tools to read the dump files. Tools such as OVITO, VMD, or even Python or MATLAB can be used to read and manipulate these files. We also developed the function lamdumpread2() to preprocess and read dump files(more details in documentation lamdumpread2()).
3. **Visualization**: For an understanding of the dynamics and qualitative analysis, visualization tools like OVITO or VMD can provide graphical insight into the system's behavior. Plot tools in Matlab can also help visualization.
4. **Quantitative Analysis**: For more quantitative work, you might process the data using a custom script or other computational tools to calculate specific properties. This could include analyzing distribution functions, calculating transport properties, or performing Fourier analyses to determine spectral properties. In your specific domain, you may also look into the interaction of the fluid with different materials and the effect on the safety of those materials.
5. **Correlation with Experimental Data**: The simulated data can be compared to experimental results to validate the model or to understand discrepancies. 
6. **Special Considerations for SPH**: Since SPH is a mesh-free method for solving fluid dynamics problems, special care might be needed in the post-processing to analyze quantities that are represented in a Lagrangian frame. Analysis of pressure, viscosity, or other fluid-specific properties may require special considerations.
7. **Documenting the Results**: Using your daily tools like Markdown, you can document the analysis procedure, the results, and create a coherent report or paper.

This workshop provides tools and examples for handling suspended particles in a fluid, making use of the Lagrangian description.

[[_TOC_]]

## Workshop File Structure

The MATLAB files and dependencies are organized under various categories as follows:

### Main File
- `example1.m`

### Main Features Demonstrated
- `lamdumpread2.m`: Swiss knife for manipulating HUGE dump files (version 2 as it is the fork for Pizza3)
- `buildVerletList.m`: Basic tool for statistical physics, implements an efficient grid search method

### Other Dependencies and Future Workshop Extensions (from Pizza3)
- `checkfiles.m`
- `forceHertzAB.m`
- `forceHertz.m`
- `forceLandshoff.m`
- `interp2SPH.m`
- `interp3SPH.m`
- `interp3SPHVerlet.m`
- `kernelSPH.m`
- `KE_t.m`
- `packing.m`
- `packing_WJbranch.m`
- `packSPH.m`
- `particle_flux.m`
- `partitionVerletList.m`
- `selfVerletList.m`
- `updateVerletList.m`
- `wallstress.m`

### Dependencies from MS (INRAE/Molecular Studio)
- `color_line3.m`
- `dispb.m`
- `dispf.m`
- `explore.m`
- `fileinfo.m`
- `lastdir.m`
- `MDunidrnd.m`
- `plot3D.m`
- `rootdir.m`

### DUMP FILES Included in This Workshop
- `dumps`
  - `hertz`
    - `dump.ulsphBulk_hertzBoundary_referenceParameterExponent+1_with1SuspendedParticle`: Original dump file
    - `PREFETCH_dump.ulsphBulk_hertzBoundary_referenceParameterExponent+1_with1SuspendedParticle`: Split folder
      - `TIMESTEP_000000000.mat`        <-------- A split file
      - `TIMESTEP_000050000.mat`        <--------158 splits (frames)
      - `TIMESTEP_000100000.mat`        <--------The values represent time
      - ...



## Workshop Steps

### STEP 1 - PREPROCESSING
Preprocessing involves handling the dump files. It includes two preprocessors: `prefetch` and `split`. The choice between them depends on the file's dimensions:

- **`prefetch`**: Preferred for 2D files (relatively smaller number of particles and many time frames).
    - Usage: `lamdumpread2('dump.*','prefetch');`
- **`split`**: Preferred for large 3D files (large number of particles and a relatively smaller number of time frames).
    - Usage: `lamdumpread2('dump.*','split');`

**Note**: This step should only be used once, as applying it again will overwrite the previous splits (frames).

```matlab
PREPROCESS_FLAG = false; % set it to true to preprocess your data
if PREPROCESS_FLAG
    datafolder = './dumps/';
    lamdumpread2(fullfile(datafolder,'dump.*'),'split'); % for large 3D
end
```



### STEP 2 - PROCESS SPECIFICALLY ONE FILE

This step focuses on working with a specific dump file, identifying the data folder, and setting default parameters. 

```matlab
datafolder = './dumps/';
dumpfile = 'dump.ulsphBulk_hertzBoundary_referenceParameterExponent+1_with1SuspendedParticle';
datafolder = lamdumpread2(fullfile(datafolder,dumpfile),'search'); % fix datafolder based on initial guess
defaultfiles = lamdumpread2(fullfile(datafolder,dumpfile),'default'); % default folder (just for check)
```

Here, `datafolder` is set to the path containing the dump files, and `dumpfile` specifies the particular file to process. The functions `lamdumpread2` with 'search' and 'default' flags are used to fix the data folder based on an initial guess and set default parameters, respectively.



### STEP 3 - EXTRACT ATOM TYPES AND AVAILABLE FRAMES
This step extracts essential information from the dump file, such as the types of atoms and the list of available frames, utilizing the `lamdumpread2` function.

```matlab
X0 = lamdumpread2(fullfile(datafolder,dumpfile)); % default frame
natoms = X0.NUMBER; % total number of atoms
timesteps = X0.TIMESTEPS; % list of available time steps
atomtypes = unique(X0.ATOMS.type); % unique atom types
ntimesteps = length(timesteps); % total number of time steps
```

- `X0`: Represents the default frame.

- `natoms`: Contains the total number of atoms.

- `timesteps`: Provides the list of available time steps.

- `atomtypes`: Holds the unique types of atoms.

- `ntimesteps`: Contains the total number of time steps.

  This step is crucial for understanding the data's structure and providing insights into the atom types and available frames.

### STEP 4 - EXTRACT MIDDLE FRAME
This step concentrates on extracting the middle frame of the simulation duration. The default frame `X0` might be too far from the steady state for advanced analysis, so the middle frame is specifically targeted.

```matlab
Xmiddle = lamdumpread2(fullfile(datafolder,dumpfile),'usesplit',[],timesteps(ceil(ntimesteps/2))); % middle frame
```

- `Xmiddle`: Represents the middle frame of the simulation, which is extracted using the `lamdumpread2` function with the `usesplit` flag.



### STEP 5 - EXTRACT NUMBER OF BEADS FOR EACH TYPE
In this step, the number of beads for each atom type is extracted. The most populated type is assumed to be the fluid, while the least populated type is assumed to be the particle.

```matlab
T = X0.ATOMS.type;
natomspertype = arrayfun(@(t) length(find(T==t)),atomtypes);
[~,fluidtype] = max(natomspertype);
[~,solidtype] = min(natomspertype);
walltypes = setdiff(atomtypes,[fluidtype,solidtype]);
```

- `T`: Represents the types of atoms from the default frame.
- `natomspertype`: An array that contains the number of atoms for each type.
- `fluidtype`: Identifies the type corresponding to the fluid (the most populated).
- `solidtype`: Identifies the type corresponding to the particle (the least populated).
- `walltypes`: Contains the types other than fluid and solid.

This step assists in classifying the types of beads in the system and understanding their distribution, crucial for further analyses and simulations.

### STEP 6 - ESTIMATE FLUID BEAD SIZE
This step aims to estimate the size of the fluid bead. The calculation starts with an initial guess based on the assumption that the bead is cubic to estimate the cutoff, followed by a more refined estimation using the `buildVerletList()` function.

```matlab
fluidxyz = X0.ATOMS{T==fluidtype,{'x','y','z'}};
fluidid = X0.ATOMS{T==fluidtype,'id'};
nfluidatoms = length(fluidid);
nsolidatoms = natomspertype(solidtype);
boxdims = X0.BOX(:,2) - X0.BOX(:,1);
Vbead_guess = prod(boxdims)/natoms;
rbead_guess = (3/(4*pi)*Vbead_guess)^(1/3);
cutoff = 3*rbead_guess;
[verletList,cutoff,dmin,config,dist] = buildVerletList(fluidxyz,cutoff);
rbead = dmin/2;
```

- `fluidxyz`: Coordinates of the fluid atoms.
- `fluidid`: IDs of the fluid atoms.
- `nfluidatoms`: Number of fluid atoms.
- `nsolidatoms`: Number of solid atoms (calculated based on the previously identified solid type).
- `rbead_guess`: Initial guess of bead radius.
- `cutoff`: Cutoff distance for the Verlet list.
- `rbead`: Final estimated bead radius.

The process estimates bead size using a specific tool (`buildVerletList`) designed to work with the physical arrangement of the beads. The accurate bead size is essential for subsequent calculations involving fluid dynamics and interactions.



### STEP 7 - FINDING THE FLOW DIRECTION
This step is crucial for identifying the primary flow direction within the system. The main idea is to determine the largest dimension of the bounding box and assume that the fluid flows along this axis. 

```matlab
[~,iflow] = max(boxdims);
iothers = setdiff(1:size(X0.BOX,1),iflow);
```

- `iflow`: Index corresponding to the largest dimension of the bounding box, considered as the main direction of fluid flow.
- `iothers`: Indices of the other dimensions, orthogonal to the main flow direction.

This simple analysis provides essential information about the orientation of the system, helping to define a reference direction for fluid movement. It serves as a basis for many downstream analyses, such as calculating velocity profiles.



### STEP 8 - SEPARATING TOP AND BOTTOM WALLS

In this simulation, two walls are present, and they move in opposite directions. This step serves to identify and separate the top and bottom walls based on their directional movement. 

```matlab
vel = {'vx','vy','vz'};
wall1vel = Xmiddle.ATOMS{Xmiddle.ATOMS.type==walltypes(1),vel{iflow}}; wall1vel = wall1vel(1);
wall2vel = Xmiddle.ATOMS{Xmiddle.ATOMS.type==walltypes(2),vel{iflow}}; wall2vel = wall2vel(1);
[wallvel,iwall] = sort([wall1vel,wall2vel],'descend'); % 1 is top (>0), 2 is bottom;
walltypes = walltypes(iwall);
```

- `wall1vel` and `wall2vel`: Velocities of the first and second walls along the main flow direction (identified in STEP 7).
- The top wall's velocity is expected to be positive, and the bottom wall's velocity is expected to be negative.



### STEP 9 - LOCATING THE PARTICLE (OBSTACLE) POSITION WITHIN THE FLOW

In this step, the position of a particle (referred to as an "obstacle") within the flow is determined. 

```matlab
solidxyz = Xmiddle.ATOMS{T==solidtype,{'x','y','z'}};
solidid = Xmiddle.ATOMS{T==solidtype,'id'};
solidbox = [min(solidxyz);max(solidxyz)]';
```