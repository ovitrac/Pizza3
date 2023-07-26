WS4

# Workshop 4 <kbd>pizza.region</kbd>

>  INRAE\Han CHEN
>  `Creation date: 2023-07-15`
>  `Revision date:  2023-07-26`

[TOC]

## Overview

> <kbd>Pizza3</kbd> provide a variety of interfaces in Python to manipulate LAMMPS features (programming) before and after execution in LAMMPS. <kbd>pizza.region</kbd> is a feature adhering to the original concepts of <kbd>region</kbd> in LAMMPS.

### What does the command <kbd>region</kbd> do in LAMMPS?

In the computational software Large-scale Atomic/Molecular Massively Parallel Simulator (LAMMPS), the role of a "region" is critical for executing intricate molecular dynamics simulations. A region, in the context of LAMMPS, refers to a specified spatial volume within the broader simulation box. This volume can be tailored to represent various geometric forms such as boxes, spheres, cylinders, and more.

The principal functionality of these regions lies in their ability to define areas where specific operations or conditions are implemented. For example, regions can be employed to create or initialize a particular group of atoms or to regulate atom interactions within their defined spatial boundaries. These regions are also instrumental in applying diverse boundary conditions or constraints, such as setting distinct temperatures or pressures within specified areas of the simulation.

Beyond their role in boundary determination and localized control, regions are essential for performing spatially-resolved analyses, given their capability to compute properties solely within the defined volume. Moreover, the formation of complex regions through the use of boolean operations of simple regions enhances the flexibility of defining interaction spaces. 

In summary, regions in LAMMPS serve multiple purposes such as the specification of spatial boundaries, the regulation of local interactions, and providing a mechanism for localized measurement and manipulation in a simulation environment.



>NOTE: **In LAMMPS, the terms "region" and "group" serve different purposes and should not be conflated, even though both deal with subsets of atoms.**
>
>A **"region"** in LAMMPS refers to a spatial subset of the simulation domain. It is defined as a geometric shape within the simulation box, which can be any form like a sphere, box, cylinder, etc. Operations and conditions specified for a region apply to the space itself, irrespective of which atoms currently occupy that space. This spatial subset can change as the simulation evolves, with atoms entering and leaving the defined region based on their individual trajectories. 
>
>On the other hand, a **"group"** is a specified subset of atoms defined by their `ID`, `type`, or other properties at the time of group creation. Once a group is defined, it retains the same collection of atoms throughout the simulation, independent of their spatial positions. Operations applied to a group affect these specific atoms no matter where they are located in the simulation box. 
>
>> ==In essence, a region is a spatially defined subset, while a group is a set of specific atoms==. They operate independently, and one does not influence the other. An atom can be part of a group while also being inside a specific region, but these are two separate classifications. Understanding this distinction is crucial for accurately setting up and interpreting LAMMPS simulations.



### What does the class <kbd>pizza.region</kbd> do in <kbd>Pizza3</kbd>?

The `pizza.region` class from the `Pizza3` Python3 package provides an interface for users to define and manipulate native geometries for LAMMPS in Python. It allows for the creation and modification of regions and their corresponding objects within a simulation space.

Example usage:
```python
from pizza import region

R1 = region()   # creates a region object R1
R2 = region()   # creates a region object R2
R = R1 + R2     # concatenates two regions. Objects of R2 are inherited in R1, with higher precedence for R2
R.do()          # generates the objects within the region
script = R.script   # retrieves the script corresponding to the region
```

Regions also have various methods for modifying and evaluating objects within the region:
```python
o1 = R.o1   # retrieves an object within the region R
R.o1 = []   # deletes the object o1 from region R
R.union(o1, o2, name='union1')   # creates a union of objects o1 and o2 within the region R
R.intersect(o1, o2, name='intersect1')   # creates an intersection of objects o1 and o2 within the region R
R.eval('o1+o2', name='sum')   # evaluates an algebraic expression within the region R
```

The `pizza.region` class also supports operator overloading. For example, the '+' and '+=' operators can be used to merge regions, while the '|' operator is used to pipe them.

The `pizza.region` class operates on core geometry objects, which are organized into several sections: "variables", "region", "create", "group", "move". Each section corresponds to a script that defines operations on regions and their contained objects.

Additionally, users can extend the `pizza.region` class to add other geometrical shapes, such as blocks, spheres, cylinders, and more.

> A live visualization is offered:
>
> - either ATOMIFY (remove comments)
> - or its online variant (more developed): https://andeplane.github.io/atomify/

### Future evolution

<kbd>pizza.region</kbd> is fully operational for "static regions" with possibilities to translate|rotate them if needed. The regions can be converted into groups. A simplified mechanism will be devised to move **groups** based on **regions**, and to assign forcefields. They will use possibilities offered in <kbd>pizza.script.scriptobject</kbd> and  <kbd>pizza.script.scriptobjectgroup</kbd>.



## Geometry Constructors for <kbd>pizza.region</kbd>

> <kbd>pizza.region</kbd> follows a syntax similar to the one used in <kbd>pizza.raster</kbd>.

The `pizza.region.geometry` class in the `Pizza3` Python3 package provides constructors for creating 3D geometry objects for LAMMPS simulations.

This class defines a geometry object as a collection of `PIZZA.SCRIPT()` objects which contain the code for LAMMPS execution. However, the actual object creation is deferred to LAMMPS, allowing for variables from `PIZZA` to be mixed with LAMMPS variables in the same template.

The `region.geometry` class supports both static and dynamic variables. Static variables are known before LAMMPS execution and have a single, fixed value. Dynamic variables are defined within the generated LAMMPS script and created during LAMMPS execution.

### Example:

```python
R.ellipsoid(0,0,0,1,1,1,name="E2",side="out",
            move=["left","${up}*3",None],
            up=0.1)

R.E2.VARIABLES.left = '"swiggle(%s,%s,%s)"%(${a},${b},${c})'
R.E2.VARIABLES.a="${b}-5"
R.E2.VARIABLES.b=5
R.E2.VARIABLES.c=100
```

The `PIZZA.REGION.DO()` and `PIZZA.REGION.DOLIVE()` methods compile (statically) and generate the corresponding LAMMPS code.

The `region.geometry` class provides methods for the creation of various geometric shapes, including:

- `block(xlo, xhi, ylo, yhi, zlo, zhi)`: Creates a block region.
- `cone(dim, c1, c2, radlo, radhi, lo, hi)`: Creates a cone region.
- `cylinder(dim, c1, c2, radius, lo, hi)`: Creates a cylinder region.
- `ellipsoid(x, y, z, a, b, c)`: Creates an ellipsoid region.
- `plane(px, py, pz, nx, ny, n)`: Creates a plane region.
- `prism(xlo, xhi, ylo, yhi, zlo, zhi, xy, xz, yz)`: Creates a prism region.
- `sphere(x, y, z, radius)`: Creates a sphere region.
- `union(N, reg-ID1, reg-ID2, ...)`: Creates a union of multiple regions.
- `intersect(N, reg-ID1, reg-ID2, ...)`: Creates an intersection of multiple regions.

More information on these constructors can be found at:

- [LAMMPS Region Documentation](https://docs.lammps.org/region.html)
- [LAMMPS Variable Documentation](https://docs.lammps.org/variable.html)
- [LAMMPS Create Atoms Documentation](https://docs.lammps.org/create_atoms.html)
- [LAMMPS Create Box Documentation](https://docs.lammps.org/create_box.html)



## Example 0: Toy Examples

In this section, we demonstrate how to generate LAMMPS code for specified geometries while defining dynamic variables within the Python environment using the `Pizza.region` package.

### Example 0.1: Define and Manipulate Ellipsoid Region

```Python
from pizza import region

R = region(name="my region")
R.ellipsoid(0, 0, 0, 1, 1, 1, name="E1", toto=3)

# Define dynamic variables
R.E1.VARIABLES.a=1
R.E1.VARIABLES.b=2
R.E1.VARIABLES.c="(${a},${b},100)"
R.E1.VARIABLES.d = '"%s%s" %("test",${c})' # "test" can be replaced by any function

# Generate LAMMPS code for this region
code1 = R.E1.do()
print(code1)
```

### Example 0.2: Evaluate the Combination of Objects

```Python
R.ellipsoid(0,0,0,1,1,1, name="E2", side="out", move=["left","${up}*3", None], up=0.1)

# Define dynamic variables
R.E2.VARIABLES.left = '"swiggle(%s,%s,%s)"%(${a},${b},${c})'
R.E2.VARIABLES.a="${b}-5"
R.E2.VARIABLES.b=5
R.E2.VARIABLES.c=100

# Generate LAMMPS code for this region
code2 = R.E2.do()
print(code2)

# Evaluate objects
R.set('E3', R.E2)
R.E3.beadtype = 2
R.set('add', R.E1 + R.E2)  # Add regions E1 and E2
R.addd2 = R.E1 + R.E2
R.eval(R.E1 | R.E2, 'E12')  # Evaluate the union of regions E1 and E2
```

### Example 0.3: Check the Object in Atomify

```Python
P = region(name="live test", width=20)
P.ellipsoid(0, 0, 0, "${Ra}", "${Rb}", "${Rc}", name="E1", Ra=5, Rb=2, Rc=3)
P.sphere(7, 0, 0, radius="${R}", name = "S1", R=2)

# Generate LAMMPS code for this region
cmd = P.do()
print(cmd)

# Generate output file for atomify
outputfile = P.dolive()
```

These examples show the process of creating regions, defining dynamic variables, and generating corresponding LAMMPS codes. The generated codes can then be used in LAMMPS simulations. Note that only LAMMPS can generate the actual geometry based on the generated codes.



## Example 1: Gel Compression

In this example, we set up a 3D geometry for a gel compression test. We use the `pizza.region` package to define regions of interest, taking advantage of the `region` class's ability to create complex geometric objects.

```Python
from pizza.region import region

# Create a test region
P = region(name="live test", width=20)
P.ellipsoid(0, 0, 0, "${Ra}", "${Rb}", "${Rc}", name="E1", Ra=5, Rb=2, Rc=3)
P.sphere(7, 0, 0, radius="${R}", name="S1", R=2)
cmd = P.do()
print(cmd)

# Define regions for gel compression
name = ['top', 'food', 'tongue', 'bottom']
scale = 1 
radius = [r * scale for r in [10, 5, 8, 10]]
height = [h * scale for h in [1, 4, 3, 1]]
spacer = 2 * scale
position_original = [spacer + height[1] + height[2] + height[3],
                     height[2] + height[3],
                     height[3],
                     0]
beadtype = [1, 2, 3, 1]
total_height = sum(height) + spacer
position = [x - total_height/2 for x in position_original]

B = region(name='region container', width=2*max(radius), height=total_height, depth=2*max(radius))

for i in range(len(name)):
    B.cylinder(name=name[i], c1=0, c2=0, radius=radius[i], lo=position[i], hi=position[i] + height[i], beadtype=beadtype[i])

B.dolive()
```

## Example 2: Emulsion

In this example, we simulate an emulsion, using the `emulsion` and `region` classes from the `pizza.region` package. The emulsion is created by inserting globules made of three different bead types into a region.

```Python
from pizza.region import region, emulsion

# Create an emulsion
e = emulsion(xmin=-5, ymin=-5, zmin=-5, xmax=5, ymax=5, zmax=5)
e.insertion([2, 2, 2, 1, 1.6, 1.2, 1.4, 1.3], beadtype=3)
e.insertion([0.6, 0.3, 2, 1.5, 1.5, 1, 2, 1.2, 1.1, 1.3], beadtype=1)
e.insertion([3, 1, 2, 2, 4, 1, 1.2, 2, 2.5, 1.2, 1.4, 1.6, 1.7], beadtype=2)

C = region(name='cregion')
C.scatter(e)  # Insert the emulsion into the region
C.dolive()

```

We can make the emulsion bigger and a fourth type.

```python
# Expand the previous example with more globules and a fourth type
mag = 3
e.insertion([3, 1, 2, 2, 4, 1, 5.2, 2, 4.5, 1.2, 1.4, 1.6, 1.7], beadtype=4)

C = region(name='cregion', width=11*mag, height=11*mag, depth=11*mag)
C.scatter(e)  # Insert the emulsion into the region
C.dolive()
```

These examples demonstrate the flexibility of the `pizza.region` package for creating and manipulating complex 3D geometries for LAMMPS simulations.