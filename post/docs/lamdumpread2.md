# lamdumpread2()
#Synopsis

The command `dump` in LAMMPS is the basic tool to generate a snapshot of quantities of one or more files once every timesteps in one of several styles. Almost all the styles accept outputs per-atom data, i.e. one or more values per atom.  

```perl
dump ID group-ID style N file attribute1 attribute2 ...
```

`Lamdumpread2()` can load and manipulate most of the atom-style formats used by the command `dump`. Dump files contain specific information about the state of the simulated system at regular intervals during a simulation run including data such as atomic coordinates, velocities, forces, stress, or other computed quantities.

This Matlab function reads LAMMPS dump files on the fly with support for various formats including text, text gzipped, and binary and without the restriction of size. It's a work in progress to implement standards similar to those used in OVITO with more flexibility due to the Matlab environment.

To accommodate limited memory scenarios, large files may require pretreatment strategies. This function also offers various actions for controlling file reading and batching processes, such as `prefetch`, `split`,etc, which provides flexibility and control over the reading process.

> LAMDUMPRREAD2 is a fork of LAMDUMPREAD for <kbd>Pizza3</kbd>. LAMDUMPREAD was initially part of Molecular Studio 2.x developped by INRAE\Olivier Vitrac.
>
> > The current documentation is less detailed than the information available by typing `doc lamdumpread2`

Revision: $2023-08-23$



## Content

[TOC]



## LAMMPS Formats

| Format                                                       |   Loading Time   |  File Size  |
| ------------------------------------------------------------ | :--------------: | :---------: |
| **TEXT**:*Editable, readable format (default in LAMMPS)*     |      +++++       |   +++++++   |
| **TEXT GZIPPED**:*As TEXT but compressed (60% file size reduction; requires -DGZIP flag in LAMMPS)* | ++++++++++++++++ |    ++++     |
| **BINARY**: *Proprietary format (largest files but fastest to open)* |        ++        | +++++++++++ |

   

## Syntax and Outputs

### Basic Usage:
```matlab
X = lamdumpread2(dumpfilename)
```
- `X.KEYWORD{i} = RECORD`: by default
- `X.KEYWORD(:,:,i) = RECORD`: when collect is used
- KEYWORD refers to keywords like `TIMESTEP`, `NUMBEROFATOMS`, `BOXBOUNDS`, etc.
- RECORD is an array

### Extended Usage:
```matlab
X = lamdumpread2(dumpfilename, [action, molecules, itimes, iatoms])
```
- `action`: Keyword controlling file reading (e.g., `'collect'`, `'count'`, `'robot'`, `'split'`, `'default'`, `'search'`)

- `molecules`: Cell array to build molecules based on `X.ATOMS`

- `itimes`: Requested timestep index

- `iatoms`: Requested atom index; when `molecules` is used, index of molecules instead

  

### Options for All Formats

- Options like `'collect'`, `'count'`, `'robot'`, etc. control how the file is read, processed, or split
- Actions like `'default'` or `'search'` provide details on dump files and prefetches

| Actions               | Description                                                  |
| --------------------- | ------------------------------------------------------------ |
|                       | ==**Actions controlling the way the file filename is read**== |
| `collect`             | Array data are stored into a 3 dims-arrays instead of a cell array. |
| `count`               | The size of each dataset is determined and not loaded.       |
| *For binary files*    | 'collect' is always applied.                                 |
|                       | ==**Actions controlling batches**==                          |
| `robot` or `prefetch` | All files are read and a prefetch is created.                |
| `split`               | All files are split into small prefetch files.               |
| `usesplit`            | Split files have higher precedence than prefetch files.      |
| `forceprefetch`       | It forces the generation of prefetch files even if split files exist. |
| *notes*               | - `lampdumpread()` generate all prefetch files (high memory footprint).<br/>- `lamdumpread2('dump.*','split')` force split even if prefetch files have been generated.<br/>- `lamdumpread('mydump','usesplit',[],[0 500])` load specifically frames 0 and 500 from split files. |
|                       | ==**Actions giving details on dump files and their prefetches**== |
| `default`             | X is a structure with fields: `prefetch.file` giving the prefetch file or anonymous function doing so for any filename `fn`, `prefetch.folder` idem for the prefetch folder, `prefetch.frame` is an anonymous function giving the filename of each split frame. |
| `search`              | The dump file is looked for inside subfolders with the following precedence: splits, prefetch, and original files. |



### Options for Text and Gzipped Formats

These options mainly deal with reading specific time steps or atom indices.



### Output Example

The output `X` has the typical fields:

```perl
             TIME: 0
         TIMESTEP: 0
           NUMBER: 313344
              BOX: [3×2 single]
            ATOMS: [313344×38 table]
      description: [1×1 struct]
              nfo: [1×1 struct]
        TIMESTEPS: [0 50000 100000 150000 200000 250000 300000 350000 400000 450000 500000 550000 600000 650000 700000 750000 800000 850000 900000 … ]
    TIMESTEPfirst: 0
     TIMESTEPlast: 8500000
```



1. **`TIME`**:
   A scalar representing the current time value in the simulation. It may be related to the current `TIMESTEP`.

2. **`TIMESTEP`**:
   A scalar representing the current timestep in the simulation. It shows the current iteration or computational cycle within the simulation.

3. **`NUMBER`**:
   A scalar value representing the total number of atoms or particles within the system. This number remains constant throughout the simulation.

4. **`BOX`**:
   A 3×2 matrix defining the boundaries of the simulated domain. It represents the spatial extents of the simulation box, likely providing the minimum and maximum values for each spatial dimension.

5. **`ATOMS`**:
   A table containing detailed information about 313344 individual atoms or particles. It likely includes properties such as position, velocity, type, force, etc., for each atom.

6. **`description`**:
   A structure containing descriptive metadata about the simulation. This could include details about the simulation setup, model used, parameters, etc.

7. **`nfo`**:
   A structure containing additional information or parameters related to the simulation. The specific contents would depend on the context of the simulation.

8. **`TIMESTEPS`**:
   An array of numerical values representing the progression of simulation steps throughout the entire simulation. It includes the timestep values for the entire simulation run.

9. **`TIMESTEPfirst`**:
   A scalar value representing the first timestep of the simulation. In this example, it is 0, indicating the start of the simulation.

10. **`TIMESTEPlast`**:
    A scalar value representing the last timestep of the simulation, which is 8500000 in this example.



The `ATOMS` field  represent a set of atoms in a simulation or analysis context. It includes detailed information about each atom, such as its position, mass, volume, and other properties. Below is an overview of the table columns available with <kbd>Pizza3</kbd>.

| Column Name          | Description                                   |
| -------------------- | --------------------------------------------- |
| TIMESTEP             | Simulation timestep                           |
| id                   | Atom identifier                               |
| type                 | Atom type                                     |
| x, y, z              | Position coordinates                          |
| mol                  | Molecule identifier                           |
| mass                 | Atom mass                                     |
| c_rho_smd, c_rho_sph | Density parameters                            |
| c_vol                | Volume parameter                              |
| radius               | Atom radius                                   |
| c_contact_radius     | Contact radius parameter                      |
| vx, vy, vz           | Velocity components                           |
| fx, fy, fz           | Force components                              |
| c_S[1] to c_S[7]     | S-type parameters (specific meaning may vary) |
| c_E[1] to c_E[6]     | E-type parameters (specific meaning may vary) |
| c_L[1] to c_L[6]     | L-type parameters (specific meaning may vary) |

This table is a snapshot of the state of a collection of atoms at a given moment or over a range of timesteps. The exact meanings of some columns might be domain-specific, requiring knowledge of the specific simulation or analysis being conducted.



## EXAMPLES

### Simple Example

Based on in.LJ, the following example demonstrates how to use the function:

```matlab
X = lamdumpread2('dump.atom')
% Outputs include TIMESTEP, NUMBEROFATOMS, BOXBOUNDS, ATOMS, etc.
plot3(X.ATOMS{2}(:,3),X.ATOMS{2}(:,4),X.ATOMS{2}(:,5),'ro') % 3D plot
```

#### Notes

- `lamdumpread2` is a fork of `lamdumpread` and is a part of an ongoing work
- Compatibility with different file types might require specific LAMMPS compilation flags
- Proper usage of the action keywords can allow for optimized file reading and manipulation

This documentation provides a comprehensive overview of the function and can be used as a reference for those working with LAMMPS dump files.



Certainly! Below are explanations for the examples you have shared, organized into three major sections: advanced examples, simple 2D simulation, and complex 3D simulations.



### More Advanced examples

1. **Extracting Specific Molecular Coordinates for Specific Time Steps**:
   This code extracts the coordinates of two specific molecules. The molecules consist of atoms with indices 1 to 1000 and 3001 to 4000. The coordinates are extracted for the time step indices 1 and 11.

   ```matlab
   X=lamdumpread('dump.atom.gz','collect',{1:1000 3001:4000},[1 11])
   ```

   The result is stored in `X`, and the molecular data is stored in a 2x1 cell with information related to these two molecules for the specified time steps.

2. **Extracting Coordinates for Specific Atom Groups Across All Time Steps**:
   This code extracts the coordinates of a group of atoms (1:1000 and 3001:4000) across all time steps.

   ```matlab
   X=lamdumpread('dump.atom.gz','collect',{},[],[1:1000 3001:4000])
   ```

   This will give you detailed data for the chosen atoms at every time step, storing the information in `X`.



### Examples from <kbd>Pizza3</kbd>



#### Simple 2D Simulation:

- **Reading 2D Data**: Reads the 2D simulation data from the file `'dump.wall.2d'` using the function `lamdumpread2`.

   ```matlab
   X = lamdumpread2(fullfile('misc_dumpfiles','dump.wall.2d'))
   ```



#### Complex 3D Simulations:

- **3D Simulation with Static and Moving Cylinders**:
   This segment of the code deals with a complex 3D simulation where it differentiates between liquid atoms and wall atoms. It also categorizes the wall atoms into static and moving cylinders.

   - The liquid atoms are identified by `type==1`, and the wall atoms are identified by `type==2`.
   
   - The `arrayfun` line calculates the mean displacement for identifying moving cylinders.

   - The plot function `plotback` plots the liquid atoms in blue, static cylinders in red, and moving cylinders in green for each time step, with a 3D view.
   
     
   
   1. **Reading 3D Back Extrusion Data (v3b version)**:
   
      ```matlab
      X = lamdumpread2(fullfile('misc_dumpfiles','dump.backextrusion_v3b'));
      ```
   
   2. **Extracting Liquid and Walls from the Simulation**:
   
      ```matlab
      A = X.ATOMS(X.ATOMS.type==1,:); % liquid
      B = X.ATOMS(X.ATOMS.type==2,:); % walls
      ```
   
   3. **Mean Displacement Calculation for Walls and Separation into Static and Moving Cylinders**:
   
      ```matlab
      zB = B.z; idB = B.id;
      dzB = arrayfun(@(id) sqrt(mean(diff(zB(idB==id)).^2)),listidB);
      B0 = B(ismember(B.id,listidB(dzB==0)),:); % static cylinder
      B1 = B(ismember(B.id,listidB(dzB>0)),:);  % moving cylinder
      ```
   
   4. **Plotting the Simulation**:
      This code block plots the liquid, static cylinders, and moving cylinders at each time step:
   
      ```matlab
      figure, view(3), for it=1:length(TIMESTEP), cla, hold on, plotback(it); title(sprintf('t= %4g',TIMESTEP(it))), drawnow, end
      ```
   
      
   
- **Complex 3D Simulation with Profile Extraction**:
   Another complex 3D simulation that involves extracting various profiles.

   - **Bottom Position of B0**: This extracts the z-position of the bottom of B1 and plots it against time.
   - **Center and Radius of B0**: This part calculates the mean x and y coordinates and the radius of B0.
   - **Sample Positions and Velocity Profile**: Here, the radial velocity profile is calculated at different radii, and the mean radial velocity is plotted against the radius. The color varies according to the time step.



1. **Complex 3D Simulation (v3a version)**:
   Similar to the v3b version, but reads data from a different file:

   ```matlab
   X = lamdumpread2('/home/olivi/billy/lammps/sandbox/dump.backextrusion_v3a');
   ```

2. **Profile Extraction**:

   - **Bottom Position of B0**: 

   ```matlab
   [~,ibottom] = min(B1.z(B1.TIMESTEP==TIMESTEP(1)));
   zbottom = B1.z(B1.id==B1.id(ibottom));
   figure, plot(TIMESTEP,zbottom), ylabel('z'), xlabel('t')
   ```

   - **Center and Radius of B0**:

   ```matlab
   xmean = mean(B0.x(B0.TIMESTEP==TIMESTEP(1)));
   ymean = mean(B0.y(B0.TIMESTEP==TIMESTEP(1)));
   rB0 = max( sqrt( (B0.x(B0.TIMESTEP==TIMESTEP(1)) - xmean).^2 + (B0.y(B0.TIMESTEP==TIMESTEP(1)) - ymean).^2 ) );
   ```

   - **Velocity Profile Extraction**:

   ```matlab
      % bottom position of B0
       [~,ibottom] = min(B1.z(B1.TIMESTEP==TIMESTEP(1)));
       zbottom = B1.z(B1.id==B1.id(ibottom));
       figure, plot(TIMESTEP,zbottom), ylabel('z'), xlabel('t')
       % center and radius of B0
       xmean = mean(B0.x(B0.TIMESTEP==TIMESTEP(1)));
       ymean = mean(B0.y(B0.TIMESTEP==TIMESTEP(1)));
       rB0 = max( sqrt( (B0.x(B0.TIMESTEP==TIMESTEP(1)) - xmean).^2 + (B0.y(B0.TIMESTEP==TIMESTEP(1)) - ymean).^2 ) );
       % sample positions
       nr = 200; r = linspace(0,rB0,nr+1);
       rA = sqrt( (A.x - xmean).^2 + (A.y - ymean).^2 );
   	nt = length(TIMESTEP);
       vz = zeros(nt,nr);
       for it=1:nt
           okt  = (A.TIMESTEP==TIMESTEP(it)) & (A.z>zbottom(it));
           if any(okt)
               vzt  = A.vz(okt);
               rAt = rA(okt); 
               for ir = 1:nr
                   ind = (rAt>=r(ir)) & (rAt<r(ir+1));
                   vz(it,ir) = max(0,mean(vzt(ind)));
               end
           end
       end
       itplot = find(any(abs(vz)>0,1),1,'first'):nt; nitplot = length(itplot);
       figure, colororder(jet(nitplot)); plot(r(1:end-1),vz(itplot,:),'-','linewidth',2), xlabel('r'), ylabel('vz')
   ```



> Overall, these examples reflect advanced applications involving the reading, extraction, and plotting of specific molecular or atomic information from complex simulation data. They include functionalities like identifying specific molecule/atom groups, managing time steps, handling 2D/3D data, and complex visualization.



