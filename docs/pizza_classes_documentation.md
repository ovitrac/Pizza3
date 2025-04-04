# Pizza Modules Documentation

Generated on: **2025-02-20 21:47:30**

<hr style="border: none; height: 1px; background-color: #e0e0e0;" />


## Configuration

To run Pizza3, ensure your Python environment is properly configured. This setup assumes that you are operating from the `Pizza3/` directory, which contains the `pizza/` and `docs/` folders. The main folder (`$mainfolder`) is set to the absolute path of the current directory.

### Setting Up PYTHONPATH

Add the following paths to your `PYTHONPATH` environment variable to allow Python to locate the Pizza3 library and its dependencies:

```bash
# Define mainfolder as the absolute path
mainfolder=$(realpath .)

# Dynamically retrieve Python paths
python_lib=$(python -c "import sysconfig; print(sysconfig.get_path('stdlib'))")
lib_dynload=$(python -c "import sysconfig; print(sysconfig.get_path('platlib'))")
site_packages=$(python -c "import site; print(site.getsitepackages()[0])")

# Paths to include in PYTHONPATH
additional_paths=(
    "$mainfolder"
    "$mainfolder/pizza"
    "$python_lib"
    "$lib_dynload"
    "$site_packages"
)

# Set PYTHONPATH dynamically
export PYTHONPATH=$(IFS=:; echo "${additional_paths[*]}")
echo "PYTHONPATH set to: $PYTHONPATH"

# Test Python Interpreter Configuration:
# You should read "Pizza library initialized successfully"
python -c "import pizza"
```

>**Note:**
>
>- The `.ipython/` directory has been excluded as it is not required for Pizza3.
>- If you're using a virtual environment, ensure it's activated before running the script to automatically include the virtual environment's `site-packages` in `PYTHONPATH`.
>- Replace `PYTHON_VERSION` with your actual Python version if different from `3.10`.
>- If you're not using `Conda`, adjust the environment creation and activation commands accordingly.

After setting up the `PYTHONPATH`, you can proceed to explore the Pizza3 modules below.

### Launch `example2.py`
You can now generate your first LAMMPS code from Python and run it with [LAMMPS-GUI](https://github.com/lammps/lammps/releases).
```bash
    mkdir -p ./tmp     # create the output folder tmp/ if it does not exist
    python example2.py # run example2
```


<hr style="border: none; height: 1px; background-color: #e0e0e0;" />

<a id="table_of_contents" name="table_of_contents"></a>
## Main Classes

<div id="table_of_contents" style="display: flex; flex-wrap: wrap; gap: 20px; justify-content: space-between; overflow-x: auto; padding: 10px;">
<div style="flex: 1 1 calc(33.33% - 20px); min-width: 200px;">
<a href="#pizza__ipynb_checkpoints_dscript-checkpoint" style="text-decoration: none; font-weight: bold;">
1. pizza..ipynb_checkpoints.dscript-checkpoint
</a>
</div>
<div style="flex: 1 1 calc(33.33% - 20px); min-width: 200px;">
<a href="#pizza__ipynb_checkpoints_dump3-checkpoint" style="text-decoration: none; font-weight: bold;">
2. pizza..ipynb_checkpoints.dump3-checkpoint
</a>
</div>
<div style="flex: 1 1 calc(33.33% - 20px); min-width: 200px;">
<a href="#pizza___init__" style="text-decoration: none; font-weight: bold;">
3. pizza.__init__
</a>
</div>
<div style="flex: 1 1 calc(33.33% - 20px); min-width: 200px;">
<a href="#pizza_converted_bdump3" style="text-decoration: none; font-weight: bold;">
4. pizza.converted.bdump3
</a>
</div>
<div style="flex: 1 1 calc(33.33% - 20px); min-width: 200px;">
<a href="#pizza_converted_cdata3" style="text-decoration: none; font-weight: bold;">
5. pizza.converted.cdata3
</a>
</div>
<div style="flex: 1 1 calc(33.33% - 20px); min-width: 200px;">
<a href="#pizza_converted_ldump3" style="text-decoration: none; font-weight: bold;">
6. pizza.converted.ldump3
</a>
</div>
<div style="flex: 1 1 calc(33.33% - 20px); min-width: 200px;">
<a href="#pizza_converted_mdump3" style="text-decoration: none; font-weight: bold;">
7. pizza.converted.mdump3
</a>
</div>
<div style="flex: 1 1 calc(33.33% - 20px); min-width: 200px;">
<a href="#pizza_converted_tdump3" style="text-decoration: none; font-weight: bold;">
8. pizza.converted.tdump3
</a>
</div>
<div style="flex: 1 1 calc(33.33% - 20px); min-width: 200px;">
<a href="#pizza_data3" style="text-decoration: none; font-weight: bold;">
9. pizza.data3
</a>
</div>
<div style="flex: 1 1 calc(33.33% - 20px); min-width: 200px;">
<a href="#pizza_data3_legacy" style="text-decoration: none; font-weight: bold;">
10. pizza.data3_legacy
</a>
</div>
<div style="flex: 1 1 calc(33.33% - 20px); min-width: 200px;">
<a href="#pizza_dforcefield" style="text-decoration: none; font-weight: bold;">
11. pizza.dforcefield
</a>
</div>
<div style="flex: 1 1 calc(33.33% - 20px); min-width: 200px;">
<a href="#pizza_dscript" style="text-decoration: none; font-weight: bold;">
12. pizza.dscript
</a>
</div>
<div style="flex: 1 1 calc(33.33% - 20px); min-width: 200px;">
<a href="#pizza_dump3" style="text-decoration: none; font-weight: bold;">
13. pizza.dump3
</a>
</div>
<div style="flex: 1 1 calc(33.33% - 20px); min-width: 200px;">
<a href="#pizza_dump3_legacy" style="text-decoration: none; font-weight: bold;">
14. pizza.dump3_legacy
</a>
</div>
<div style="flex: 1 1 calc(33.33% - 20px); min-width: 200px;">
<a href="#pizza_forcefield" style="text-decoration: none; font-weight: bold;">
15. pizza.forcefield
</a>
</div>
<div style="flex: 1 1 calc(33.33% - 20px); min-width: 200px;">
<a href="#pizza_generic" style="text-decoration: none; font-weight: bold;">
16. pizza.generic
</a>
</div>
<div style="flex: 1 1 calc(33.33% - 20px); min-width: 200px;">
<a href="#pizza_group" style="text-decoration: none; font-weight: bold;">
17. pizza.group
</a>
</div>
<div style="flex: 1 1 calc(33.33% - 20px); min-width: 200px;">
<a href="#pizza_private_mstruct" style="text-decoration: none; font-weight: bold;">
18. pizza.private.mstruct
</a>
</div>
<div style="flex: 1 1 calc(33.33% - 20px); min-width: 200px;">
<a href="#pizza_private_utils" style="text-decoration: none; font-weight: bold;">
19. pizza.private.utils
</a>
</div>
<div style="flex: 1 1 calc(33.33% - 20px); min-width: 200px;">
<a href="#pizza_raster" style="text-decoration: none; font-weight: bold;">
20. pizza.raster
</a>
</div>
<div style="flex: 1 1 calc(33.33% - 20px); min-width: 200px;">
<a href="#pizza_region" style="text-decoration: none; font-weight: bold;">
21. pizza.region
</a>
</div>
<div style="flex: 1 1 calc(33.33% - 20px); min-width: 200px;">
<a href="#pizza_script" style="text-decoration: none; font-weight: bold;">
22. pizza.script
</a>
</div>
</div>

## Module `pizza..ipynb_checkpoints.dscript-checkpoint`

**Error importing module**: No module named 'pizza.'

## Module `pizza..ipynb_checkpoints.dump3-checkpoint`

**Error importing module**: No module named 'pizza.'

<a id="pizza___init__" name="pizza___init__"></a>
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; font-size: 0.8em;"><a href="#pizza__ipynb_checkpoints_dump3-checkpoint" title="Go to Previous Module: pizza..ipynb_checkpoints.dump3-checkpoint" style="text-decoration: none;">⬅️ Previous</a>
<a href="#table_of_contents" title="Back to Table of Contents" style="text-decoration: none;">⬆️ TOC</a>
<a href="#pizza_converted_bdump3" title="Go to Next Module: pizza.converted.bdump3" style="text-decoration: none;">➡️ Next</a>
</div>

## Module `pizza.__init__`

### Class Inheritance Diagram
```mermaid
graph TD;
AttrErrorDict
Block
CallableScript
Collection
Cone
Cylinder
Ellipsoid
Evalgeometry
Intersect
LammpsCollectionGroup
LammpsCreate
LammpsFooter
LammpsFooterPreview
LammpsGeneric
LammpsGroup
LammpsHeader
LammpsHeaderBox
LammpsHeaderInit
LammpsHeaderLattice
LammpsHeaderMass
LammpsMove
LammpsRegion
LammpsSetGroup
LammpsSpacefilling
LammpsVariables
Operation
Plane
Prism
SafeEvaluator
ScriptTemplate
Sphere
USERSMD
Union
VariableOccurrences
boundarysection
coregeometry
coreshell
data
dforcefield
discretizationsection
dscript
dump
dumpsection
emulsion
forcefield
generic
genericdata
geometrysection
globalsection
groupcollection
groupobject
headersRegiondata
initializesection
integrationsection
interactionsection
lambdaScriptdata
lamdaScript
none
param
paramauto
parameterforcefield
pipescript
pstr
raster
region
regioncollection
regiondata
rigidwall
runsection
saltTLSPH
scatter
script
scriptdata
scriptobject
scriptobjectgroup
smd
solidfood
statussection
struct
tlsph
tlsphalone
ulsph
ulsphalone
water
LammpsGeneric --> LammpsCollectionGroup
LammpsGeneric --> LammpsCreate
LammpsGeneric --> LammpsFooter
LammpsGeneric --> LammpsFooterPreview
LammpsGeneric --> LammpsGroup
LammpsGeneric --> LammpsHeader
LammpsGeneric --> LammpsHeaderBox
LammpsGeneric --> LammpsHeaderInit
LammpsGeneric --> LammpsHeaderLattice
LammpsGeneric --> LammpsHeaderMass
LammpsGeneric --> LammpsMove
LammpsGeneric --> LammpsRegion
LammpsGeneric --> LammpsSetGroup
LammpsGeneric --> LammpsSpacefilling
LammpsGeneric --> LammpsVariables
NodeVisitor --> SafeEvaluator
coregeometry --> Block
coregeometry --> Cone
coregeometry --> Cylinder
coregeometry --> Ellipsoid
coregeometry --> Evalgeometry
coregeometry --> Intersect
coregeometry --> Plane
coregeometry --> Prism
coregeometry --> Sphere
coregeometry --> Union
dict --> AttrErrorDict
emulsion --> coreshell
forcefield --> smd
forcefield --> tlsphalone
generic --> USERSMD
none --> rigidwall
object --> CallableScript
object --> Collection
object --> Operation
object --> ScriptTemplate
object --> VariableOccurrences
object --> coregeometry
object --> data
object --> dforcefield
object --> dscript
object --> dump
object --> forcefield
object --> generic
object --> groupcollection
object --> groupobject
object --> pipescript
object --> raster
object --> region
object --> scatter
object --> script
object --> struct
param --> paramauto
param --> scriptdata
paramauto --> lambdaScriptdata
paramauto --> parameterforcefield
paramauto --> regiondata
parameterforcefield --> genericdata
regiondata --> headersRegiondata
scatter --> emulsion
script --> LammpsGeneric
script --> boundarysection
script --> discretizationsection
script --> dumpsection
script --> geometrysection
script --> globalsection
script --> initializesection
script --> integrationsection
script --> interactionsection
script --> lamdaScript
script --> runsection
script --> statussection
smd --> none
smd --> tlsph
smd --> ulsph
smd --> ulsphalone
str --> pstr
struct --> param
struct --> regioncollection
struct --> scriptobject
struct --> scriptobjectgroup
tlsph --> saltTLSPH
tlsph --> solidfood
ulsph --> water
```

**Class Examples:** Not available.

### Methods Table

| Class | Method | Docstring First Paragraph | # Lines | __version__ |
|-------|---------|---------------------------|---------|-------------|
| (module-level) | `check_PIL` |  | 14 |  |

<a id="pizza_converted_bdump3" name="pizza_converted_bdump3"></a>
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; font-size: 0.8em;"><a href="#pizza___init__" title="Go to Previous Module: pizza.__init__" style="text-decoration: none;">⬅️ Previous</a>
<a href="#table_of_contents" title="Back to Table of Contents" style="text-decoration: none;">⬆️ TOC</a>
<a href="#pizza_converted_cdata3" title="Go to Next Module: pizza.converted.cdata3" style="text-decoration: none;">➡️ Next</a>
</div>

## Module `pizza.converted.bdump3`

### Class Inheritance Diagram
```mermaid
graph TD;
Snap
bdump
object --> Snap
object --> bdump
```

**[Class Examples for `pizza/converted/bdump3.py` (1)](class_examples.html#pizza_converted_bdump3)**

### Methods Table

| Class | Method | Docstring First Paragraph | # Lines | __version__ |
|-------|---------|---------------------------|---------|-------------|
| `Snap` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 4 |  |
| `bdump` | `__init__` | Initialize the bdump object. | 32 |  |
| `bdump` | `cull` | Remove duplicate snapshots based on time stamps. | 11 |  |
| `bdump` | `map` | Assign names to atom columns. | 13 |  |
| `bdump` | `next` | Read the next snapshot in incremental mode. | 49 |  |
| `bdump` | `read_all` | Read all snapshots from the list of dump files. | 36 |  |
| `bdump` | `read_snapshot` | Read a single snapshot from the file. | 49 |  |
| `bdump` | `time` | Get a list of all snapshot time stamps. | 8 |  |
| `bdump` | `viz` | Return bond information for visualization. | 53 |  |

<a id="pizza_converted_cdata3" name="pizza_converted_cdata3"></a>
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; font-size: 0.8em;"><a href="#pizza_converted_bdump3" title="Go to Previous Module: pizza.converted.bdump3" style="text-decoration: none;">⬅️ Previous</a>
<a href="#table_of_contents" title="Back to Table of Contents" style="text-decoration: none;">⬆️ TOC</a>
<a href="#pizza_converted_ldump3" title="Go to Next Module: pizza.converted.ldump3" style="text-decoration: none;">➡️ Next</a>
</div>

## Module `pizza.converted.cdata3`

### Class Inheritance Diagram
```mermaid
graph TD;
Box
Capped
Cylinder
Group
Line
Random
Shell
Sphere
Surface
Union
cdata
Sphere --> Shell
object --> Box
object --> Capped
object --> Cylinder
object --> Group
object --> Line
object --> Random
object --> Sphere
object --> Surface
object --> Union
object --> cdata
```

**Class Examples:** Not available.

### Methods Table

| Class | Method | Docstring First Paragraph | # Lines | __version__ |
|-------|---------|---------------------------|---------|-------------|
| (module-level) | `box_triangulate` | Triangulate a unit box from (0,0,0) to (1,1,1) with spacings q1, q2, q3. Return a list of vertices and triangles. Triangles are oriented outward. | 39 |  |
| (module-level) | `connect` | Create connections between triangles in a triangulated surface. Each triangle has 3 vertices. Return a list of connections for each tri. | 42 |  |
| (module-level) | `cross` | Compute the cross product of vectors a and b (each 3D). | 9 |  |
| (module-level) | `normal` | Compute the normal vector for a triangle with vertices x, y, z. Each vertex is a 3D coordinate [x, y, z]. | 10 |  |
| (module-level) | `normalize` | Normalize vector a in-place to unit length. | 9 |  |
| (module-level) | `vertex` | Add a vertex to the vertices list if not already present. Return the index of the vertex in the vertices list. | 12 |  |
| `Box` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 13 |  |
| `Box` | `area` |  | 15 |  |
| `Box` | `bbox` |  | 2 |  |
| `Box` | `command` |  | 2 |  |
| `Box` | `inside` |  | 5 |  |
| `Box` | `loc2d` | Return a random point on the surface, ignoring partial sums for now. This is a simplified approach. Adjust to handle 'area' fraction properly. | 15 |  |
| `Box` | `triangulate` |  | 16 |  |
| `Capped` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 14 |  |
| `Capped` | `area` | Surface area of a capped cylinder = cylinder area + 2 * hemisphere discs. Approximate if needed. Or store partial sums if you want area-based loc2d. | 11 |  |
| `Capped` | `bbox` |  | 10 |  |
| `Capped` | `command` |  | 3 |  |
| `Capped` | `inside` |  | 24 |  |
| `Capped` | `loc2d` | Return a random location on the capped cylinder surface. | 6 |  |
| `Capped` | `triangulate` |  | 43 |  |
| `Cylinder` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 14 |  |
| `Cylinder` | `area` | Cylinder area = 2 * (circle area) + side area = 2 * (πr²) + (2πr * length) But we store partial sums if needed. | 11 |  |
| `Cylinder` | `bbox` |  | 11 |  |
| `Cylinder` | `command` |  | 3 |  |
| `Cylinder` | `inside` |  | 19 |  |
| `Cylinder` | `loc2d` |  | 3 |  |
| `Cylinder` | `triangulate` |  | 25 |  |
| `Group` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 11 |  |
| `Group` | `bbox` | Return bounding box of all particles in this group. | 10 |  |
| `Group` | `center` | Set center of the group explicitly or to the midpoint of bounding box. | 13 |  |
| `Line` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 6 |  |
| `Line` | `addline` | Add a single line segment (x1, y1, z1, x2, y2, z2). | 6 |  |
| `Line` | `bbox` | Return bounding box around all line segments. | 10 |  |
| `Random` | `__call__` | Call self as a function. | 6 |  |
| `Random` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 2 |  |
| `Shell` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 5 |  |
| `Shell` | `area` |  | 2 |  |
| `Shell` | `bbox` |  | 3 |  |
| `Shell` | `command` |  | 2 |  |
| `Shell` | `inside` |  | 8 |  |
| `Shell` | `loc2d` | Return a random location on the sphere surface. | 16 |  |
| `Shell` | `triangulate` |  | 21 |  |
| `Sphere` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 12 |  |
| `Sphere` | `area` |  | 2 |  |
| `Sphere` | `bbox` |  | 3 |  |
| `Sphere` | `command` |  | 2 |  |
| `Sphere` | `inside` |  | 7 |  |
| `Sphere` | `loc2d` | Return a random location on the sphere surface. | 16 |  |
| `Sphere` | `triangulate` |  | 21 |  |
| `Surface` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 15 |  |
| `Surface` | `area` | Return total surface area of this surface. By default, sum the area of each triangle. | 19 |  |
| `Surface` | `bbox` | Return bounding box of all vertices in this surface. | 10 |  |
| `Surface` | `center` | Set center of the surface explicitly or to the midpoint of bounding box. | 13 |  |
| `Surface` | `inside` | Check if point (x, y, z) is inside this closed surface. By default, return False (0). Implement if needed. | 7 |  |
| `Surface` | `inside_prep` | Prepare binning if you want to accelerate inside() checks. Depending on usage, implement as needed. | 6 |  |
| `Surface` | `loc2d` | Return a random point on the surface, given a pre-chosen 'area' fraction. By default, pick from triangles in ascending area order. Must implement your own partial sums if you want a strict area-based sampling. | 25 |  |
| `Union` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 11 |  |
| `Union` | `area` |  | 6 |  |
| `Union` | `bbox` |  | 13 |  |
| `Union` | `inside` |  | 6 |  |
| `Union` | `loc2d` | Return a random location on the union surface, if needed. This would require partial sums across each child's area. For brevity, pick first child. | 9 |  |
| `cdata` | `__init__` | Initialize the cdata object. | 14 |  |
| `cdata` | `append` | Append selected objects to an existing ChemCell data file. | 19 |  |
| `cdata` | `bbox` | Compute the bounding box that encloses all selected objects. | 21 |  |
| `cdata` | `bins` | Set binning parameters for a surface. | 14 |  |
| `cdata` | `box` | Create a box region. | 17 |  |
| `cdata` | `cap` | Create a capped-cylinder region. | 17 |  |
| `cdata` | `center` | Set the center point of an object. | 12 |  |
| `cdata` | `copy` | Create a deep copy of an object with a new identifier. | 17 |  |
| `cdata` | `cyl` | Create a cylinder region. | 17 |  |
| `cdata` | `delete` | Delete objects from the cdata. | 17 |  |
| `cdata` | `filewrite` | Write objects to an already opened data file. | 32 |  |
| `cdata` | `findtime` | Find the index of a given timestep. | 16 |  |
| `cdata` | `iterator` | Iterator method compatible with equivalent dump calls. | 13 |  |
| `cdata` | `join` | Join multiple objects of the same style into a new object. | 75 |  |
| `cdata` | `lbox` | Create a line object with 12 lines representing a box. | 32 |  |
| `cdata` | `line` | Create a line object with a single line. | 20 |  |
| `cdata` | `maxbox` | Return the bounding box that encloses all selected objects. | 8 |  |
| `cdata` | `part` | Create a group with N particles inside a specified object and optionally outside another. | 55 |  |
| `cdata` | `part2d` | Create a group with N 2D particles on a specified surface. | 34 |  |
| `cdata` | `partarray` | Create a 3D grid of particles. | 33 |  |
| `cdata` | `partring` | Create a ring of N particles. | 45 |  |
| `cdata` | `partsurf` | Change the surface assignment for a 2D group of particles. | 14 |  |
| `cdata` | `project` | Project particles in group ID to the surface of object ID2. | 94 |  |
| `cdata` | `q` | Set quality factors for a region's triangulation routine. | 13 |  |
| `cdata` | `random` | Pick a random point on the surface of the specified object. | 18 |  |
| `cdata` | `read` | Read ChemCell data files and populate objects. | 150 |  |
| `cdata` | `rename` | Rename an object. | 16 |  |
| `cdata` | `rotate` | Rotate an object so that its current axes align with new ones. | 64 |  |
| `cdata` | `scale` | Scale an object by specified factors along each axis. | 21 |  |
| `cdata` | `seed` | Set the random number generator seed. | 8 |  |
| `cdata` | `select` | Select one or more objects. | 14 |  |
| `cdata` | `shell` | Create a shell region. | 17 |  |
| `cdata` | `sphere` | Create a sphere region. | 17 |  |
| `cdata` | `surf` | Create a triangulated surface from a region object. | 26 |  |
| `cdata` | `surfselect` | Create a triangulated surface by selecting triangles based on a test string. | 60 |  |
| `cdata` | `surftri` | Create a triangulated surface from a list of triangle indices in another surface. | 41 |  |
| `cdata` | `trans` | Translate an object by a displacement. | 26 |  |
| `cdata` | `union` | Create a union object from a list of other objects. | 16 |  |
| `cdata` | `unselect` | Unselect one or more objects. | 14 |  |
| `cdata` | `viz` | Return list of atoms, bonds, tris, and lines for visualization. | 69 |  |
| `cdata` | `write` | Write selected objects to a ChemCell data file. | 19 |  |

<a id="pizza_converted_ldump3" name="pizza_converted_ldump3"></a>
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; font-size: 0.8em;"><a href="#pizza_converted_cdata3" title="Go to Previous Module: pizza.converted.cdata3" style="text-decoration: none;">⬅️ Previous</a>
<a href="#table_of_contents" title="Back to Table of Contents" style="text-decoration: none;">⬆️ TOC</a>
<a href="#pizza_converted_mdump3" title="Go to Next Module: pizza.converted.mdump3" style="text-decoration: none;">➡️ Next</a>
</div>

## Module `pizza.converted.ldump3`

### Class Inheritance Diagram
```mermaid
graph TD;
Snap
ldump
object --> Snap
object --> ldump
```

**[Class Examples for `pizza/converted/ldump3.py` (1)](class_examples.html#pizza_converted_ldump3)**

### Methods Table

| Class | Method | Docstring First Paragraph | # Lines | __version__ |
|-------|---------|---------------------------|---------|-------------|
| `Snap` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 5 |  |
| `ldump` | `__init__` | Initialize the ldump object. | 32 |  |
| `ldump` | `cull` | Remove duplicate snapshots based on time stamps. | 11 |  |
| `ldump` | `findtime` | Find the index of a given timestep. | 17 |  |
| `ldump` | `map` | Assign names to atom columns. | 13 |  |
| `ldump` | `next` | Read the next snapshot in incremental mode. | 49 |  |
| `ldump` | `owrap` | Wrap line end points associated with atoms through periodic boundaries. | 51 |  |
| `ldump` | `read_all` | Read all snapshots from the list of dump files. | 36 |  |
| `ldump` | `read_snapshot` | Read a single snapshot from the file. | 67 |  |
| `ldump` | `time` | Get a list of all snapshot time stamps. | 8 |  |
| `ldump` | `viz` | Return line segment information for visualization. | 63 |  |

<a id="pizza_converted_mdump3" name="pizza_converted_mdump3"></a>
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; font-size: 0.8em;"><a href="#pizza_converted_ldump3" title="Go to Previous Module: pizza.converted.ldump3" style="text-decoration: none;">⬅️ Previous</a>
<a href="#table_of_contents" title="Back to Table of Contents" style="text-decoration: none;">⬆️ TOC</a>
<a href="#pizza_converted_tdump3" title="Go to Next Module: pizza.converted.tdump3" style="text-decoration: none;">➡️ Next</a>
</div>

## Module `pizza.converted.mdump3`

### Class Inheritance Diagram
```mermaid
graph TD;
Snap
eselect
mdump
tselect
object --> Snap
object --> eselect
object --> mdump
object --> tselect
```

**[Class Examples for `pizza/converted/mdump3.py` (1)](class_examples.html#pizza_converted_mdump3)**

### Methods Table

| Class | Method | Docstring First Paragraph | # Lines | __version__ |
|-------|---------|---------------------------|---------|-------------|
| (module-level) | `normal` | Compute the normal vector for a triangle defined by vertices x, y, z. | 25 |  |
| `Snap` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 14 |  |
| `eselect` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 2 |  |
| `eselect` | `all` | Select all elements in all steps or in one specified step. | 29 |  |
| `eselect` | `test` | Select elements based on a Python Boolean expression. | 66 |  |
| `mdump` | `__init__` | Initialize the mdump object. | 36 |  |
| `mdump` | `compare_time` | Comparator for sorting snapshots by time. | 17 |  |
| `mdump` | `cull` | Remove duplicate snapshots based on time stamps and merge their data. | 33 |  |
| `mdump` | `delete` | Delete non-selected snapshots. | 16 |  |
| `mdump` | `iterator` | Iterator method compatible with equivalent dump calls. | 22 |  |
| `mdump` | `map` | Assign names to element value columns. | 14 |  |
| `mdump` | `mviz` | Return mesh visualization information for a snapshot, including nodes and elements. | 47 |  |
| `mdump` | `next` | Read the next snapshot in incremental mode. | 54 |  |
| `mdump` | `owrap` | Wrap line end points associated with atoms through periodic boundaries. | 52 |  |
| `mdump` | `read_all` | Read all snapshots from the list of dump files. | 70 |  |
| `mdump` | `read_snapshot` | Read a single snapshot from the file. | 94 |  |
| `mdump` | `reference` | Ensure every snapshot has node and element connectivity information by referencing previous snapshots. | 30 |  |
| `mdump` | `sort` | Sort snapshots by ID in all selected timesteps or one specified timestep. | 27 |  |
| `mdump` | `sort_one` | Sort elements in a single snapshot by ID column. | 14 |  |
| `mdump` | `time` | Get a list of all selected snapshot time stamps. | 8 |  |
| `mdump` | `vecs` | Extract vector(s) of values for selected elements at a specific timestep. | 41 |  |
| `mdump` | `viz` | Return mesh visualization information for a snapshot. | 159 |  |
| `tselect` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 2 |  |
| `tselect` | `all` | Select all timesteps. | 10 |  |
| `tselect` | `none` | Deselect all timesteps. | 9 |  |
| `tselect` | `one` | Select only timestep N. | 18 |  |
| `tselect` | `skip` | Select every Mth step. | 20 |  |
| `tselect` | `test` | Select timesteps based on a Python Boolean expression. | 30 |  |

<a id="pizza_converted_tdump3" name="pizza_converted_tdump3"></a>
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; font-size: 0.8em;"><a href="#pizza_converted_mdump3" title="Go to Previous Module: pizza.converted.mdump3" style="text-decoration: none;">⬅️ Previous</a>
<a href="#table_of_contents" title="Back to Table of Contents" style="text-decoration: none;">⬆️ TOC</a>
<a href="#pizza_data3" title="Go to Next Module: pizza.data3" style="text-decoration: none;">➡️ Next</a>
</div>

## Module `pizza.converted.tdump3`

### Class Inheritance Diagram
```mermaid
graph TD;
Snap
tdump
object --> Snap
object --> tdump
```

**[Class Examples for `pizza/converted/tdump3.py` (1)](class_examples.html#pizza_converted_tdump3)**

### Methods Table

| Class | Method | Docstring First Paragraph | # Lines | __version__ |
|-------|---------|---------------------------|---------|-------------|
| (module-level) | `normal` | Compute the normal vector for a triangle defined by vertices x, y, z. | 25 |  |
| `Snap` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 5 |  |
| `tdump` | `__init__` | Initialize the tdump object. | 32 |  |
| `tdump` | `compare_time` | Comparator for sorting snapshots by time. | 17 |  |
| `tdump` | `cull` | Remove duplicate snapshots based on time stamps. | 10 |  |
| `tdump` | `findtime` | Find the index of a given timestep. | 17 |  |
| `tdump` | `map` | Assign names to atom columns. | 14 |  |
| `tdump` | `next` | Read the next snapshot in incremental mode. | 49 |  |
| `tdump` | `owrap` | Wrap triangle corner points associated with atoms through periodic boundaries. | 60 |  |
| `tdump` | `read_all` | Read all snapshots from the list of dump files. | 36 |  |
| `tdump` | `read_snapshot` | Read a single snapshot from the file. | 67 |  |
| `tdump` | `time` | Get a list of all snapshot time stamps. | 8 |  |
| `tdump` | `viz` | Return triangle information for visualization. | 68 |  |

<a id="pizza_data3" name="pizza_data3"></a>
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; font-size: 0.8em;"><a href="#pizza_converted_tdump3" title="Go to Previous Module: pizza.converted.tdump3" style="text-decoration: none;">⬅️ Previous</a>
<a href="#table_of_contents" title="Back to Table of Contents" style="text-decoration: none;">⬆️ TOC</a>
<a href="#pizza_data3_legacy" title="Go to Next Module: pizza.data3_legacy" style="text-decoration: none;">➡️ Next</a>
</div>

## Module `pizza.data3`

### Class Inheritance Diagram
```mermaid
graph TD;
data
dump
object --> data
object --> dump
```

**[Class Examples for `pizza/data3.py` (2)](class_examples.html#pizza_data3)**

### Methods Table

| Class | Method | Docstring First Paragraph | # Lines | __version__ |
|-------|---------|---------------------------|---------|-------------|
| `data` | `__init__` | Initialize a data object. | 33 | 1.0 |
| `data` | `__repr__` | Return a string representation of the data object. | 32 | 1.0 |
| `data` | `_init_from_dump` | Initialize the data object from a dump object. | 68 | 1.0 |
| `data` | `_init_from_file` | Initialize the data object from a LAMMPS data file. | 84 | 1.0 |
| `data` | `append` | Append a new column to a named section. | 52 | 1.0 |
| `data` | `delete` | Delete a header value or section from the data object. | 18 | 1.0 |
| `data` | `dispsection` | Display information about a section. | 22 | 1.0 |
| `data` | `findtime` | Find the index of a given timestep. | 16 | 1.0 |
| `data` | `get` | Extract information from data file fields. | 38 | 1.0 |
| `data` | `iterator` | Iterator method compatible with other tools. | 13 | 1.0 |
| `data` | `map` | Assign names to atom columns. | 18 | 1.0 |
| `data` | `maxbox` | Return the box dimensions. | 13 | 1.0 |
| `data` | `maxtype` | Return the number of atom types. | 10 | 1.0 |
| `data` | `newxyz` | Replace x, y, z coordinates in the Atoms section with those from a dump object. | 28 | 1.0 |
| `data` | `reorder` | Reorder columns in a data file section. | 30 | 1.0 |
| `data` | `replace` | Replace a column in a named section with a vector of values. | 37 | 1.0 |
| `data` | `viz` | Return visualization data for a specified snapshot. | 75 | 1.0 |
| `data` | `write` | Write the data object to a LAMMPS data file. | 37 | 1.0 |

<a id="pizza_data3_legacy" name="pizza_data3_legacy"></a>
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; font-size: 0.8em;"><a href="#pizza_data3" title="Go to Previous Module: pizza.data3" style="text-decoration: none;">⬅️ Previous</a>
<a href="#table_of_contents" title="Back to Table of Contents" style="text-decoration: none;">⬆️ TOC</a>
<a href="#pizza_dforcefield" title="Go to Next Module: pizza.dforcefield" style="text-decoration: none;">➡️ Next</a>
</div>

## Module `pizza.data3_legacy`

### Class Inheritance Diagram
```mermaid
graph TD;
data
dump
object --> data
object --> dump
```

**[Class Examples for `pizza/data3_legacy.py` (1)](class_examples.html#pizza_data3_legacy)**

### Methods Table

| Class | Method | Docstring First Paragraph | # Lines | __version__ |
|-------|---------|---------------------------|---------|-------------|
| `data` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 138 | 1.0 |
| `data` | `__repr__` | Return repr(self). | 26 | 1.0 |
| `data` | `append` | append a new column: X.append("section",vectorofvalues,forceinteger=False,propertyname=None) | 37 | 1.0 |
| `data` | `delete` |  | 8 | 1.0 |
| `data` | `dispsection` | display section info: X.dispsection("sectionname") | 10 | 1.0 |
| `data` | `findtime` |  | 4 | 1.0 |
| `data` | `get` |  | 21 | 1.0 |
| `data` | `iterator` |  | 4 | 1.0 |
| `data` | `map` |  | 6 | 1.0 |
| `data` | `maxbox` |  | 5 | 1.0 |
| `data` | `maxtype` |  | 2 | 1.0 |
| `data` | `newxyz` |  | 16 | 1.0 |
| `data` | `reorder` | reorder columns: reorder("section",colidxfirst,colidxsecond,colidxthird,...) | 16 | 1.0 |
| `data` | `replace` | replace column values: replace("section",columnindex,vectorofvalues) with columnindex=1..ncolumns | 20 | 1.0 |
| `data` | `viz` |  | 61 | 1.0 |
| `data` | `write` |  | 20 | 1.0 |

<a id="pizza_dforcefield" name="pizza_dforcefield"></a>
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; font-size: 0.8em;"><a href="#pizza_data3_legacy" title="Go to Previous Module: pizza.data3_legacy" style="text-decoration: none;">⬅️ Previous</a>
<a href="#table_of_contents" title="Back to Table of Contents" style="text-decoration: none;">⬆️ TOC</a>
<a href="#pizza_dscript" title="Go to Next Module: pizza.dscript" style="text-decoration: none;">➡️ Next</a>
</div>

## Module `pizza.dforcefield`

### Class Inheritance Diagram
```mermaid
graph TD;
USERSMD
dforcefield
forcefield
generic
genericdata
param
paramauto
parameterforcefield
scriptdata
scriptobject
struct
generic --> USERSMD
object --> dforcefield
object --> forcefield
object --> generic
object --> struct
param --> paramauto
param --> scriptdata
paramauto --> parameterforcefield
parameterforcefield --> genericdata
struct --> param
struct --> scriptobject
```

**[Class Examples for `pizza/dforcefield.py` (15)](class_examples.html#pizza_dforcefield)**

### Methods Table

| Class | Method | Docstring First Paragraph | # Lines | __version__ |
|-------|---------|---------------------------|---------|-------------|
| (module-level) | `autoname` | generate automatically names | 3 | 0.99995 |
| (module-level) | `remove_comments` | Removes comments from a single or multi-line string. Handles quotes and escaped characters. | 68 | 0.99995 |
| `dforcefield` | `__add__` | Concatenate dforcefield attributes, i | 38 | 0.99995 |
| `dforcefield` | `__contains__` | Check if an attribute exists in the dforcefield instance or its parameters. | 3 | 0.99995 |
| `dforcefield` | `__copy__` | Shallow copy method for dforcefield. | 15 | 0.99995 |
| `dforcefield` | `__deepcopy__` | Deep copy method for dforcefield. | 21 | 0.99995 |
| `dforcefield` | `__getattr__` | Shorthand for accessing parameters, base class attributes, or attributes in 'name' and 'description'. If an attribute exists in both 'name' and 'description', their contents are combined with a newline. | 28 | 0.99995 |
| `dforcefield` | `__hasattr__` | Check if an attribute exists in the dforcefield instance, class, parameters, or the base class. | 15 | 0.99995 |
| `dforcefield` | `__init__` | Initialize a dynamic forcefield with default or custom values. | 169 | 0.99995 |
| `dforcefield` | `__iter__` | Iterate over all keys, including those in the merged struct, parameters, and scalar attributes. | 11 | 0.99995 |
| `dforcefield` | `__len__` | Return the number of parameters in the forcefield. This will use the len method of parameters. | 6 | 0.99995 |
| `dforcefield` | `__or__` | Overload | pipe operator in dscript | 6 | 0.99995 |
| `dforcefield` | `__repr__` | Custom __repr__ method that provides a detailed representation of the dforcefield instance, excluding attributes that start with an underscore (_). | 71 | 0.99995 |
| `dforcefield` | `__setattr__` | Shorthand for setting attributes. Attributes specific to dforcefield are handled separately. New attributes are added to parameters if they are not part of the dforcefield-specific attributes. | 27 | 0.99995 |
| `dforcefield` | `__str__` | Return str(self). | 3 | 0.99995 |
| `dforcefield` | `_inject_attributes` | Inject dforcefield attributes into the base class, bypassing __setattr__. | 22 | 0.99995 |
| `dforcefield` | `base_repr` | Returns the representation of the base_class. | 4 | 0.99995 |
| `dforcefield` | `combine_parameters` | Combine GLOBAL, LOCAL, and RULES to get the current parameter configuration. | 5 | 0.99995 |
| `dforcefield` | `compare` | Compare the current instance with another dforcefield instance, including RULES, GLOBAL, and LOCAL. | 142 | 0.99995 |
| `dforcefield` | `copy` | Create a new instance of dforcefield with the option to override key attributes including RULES, GLOBAL, and LOCAL. | 34 | 0.99995 |
| `dforcefield` | `detectVariables` | Detects variables in the form ${variable} from the outputs of pair_style, pair_diagcoeff, and pair_offdiagcoeff. | 30 | 0.99995 |
| `dforcefield` | `dispmax` | optimize display | 8 | 0.99995 |
| `dforcefield` | `generator` | Generate the forcefield definition as a formatted string without traceability features. | 55 | 0.99995 |
| `dforcefield` | `get_global` | Return the GLOBAL parameters for this dforcefield instance. | 3 | 0.99995 |
| `dforcefield` | `get_local` | Return the LOCAL parameters for this dforcefield instance. | 3 | 0.99995 |
| `dforcefield` | `get_rules` | Return the RULES parameters for this dforcefield instance. | 3 | 0.99995 |
| `dforcefield` | `items` | Return an iterator over (key, value) pairs from the merged struct, parameters, and scalar attributes. | 16 | 0.99995 |
| `dforcefield` | `keys` | Return the keys of the merged struct, parameters, and scalar attributes. | 8 | 0.99995 |
| `dforcefield` | `missingVariables` | List missing variables (undefined in parameters). | 46 | 0.99995 |
| `dforcefield` | `pair_diagcoeff` | Delegate pair_diagcoeff to the base class, ensuring it uses the correct attributes. | 6 | 0.99995 |
| `dforcefield` | `pair_offdiagcoeff` | Delegate pair_offdiagcoeff to the base class, ensuring it uses the correct attributes. | 6 | 0.99995 |
| `dforcefield` | `pair_style` | Delegate pair_style to the base class, ensuring it uses the correct attributes. | 6 | 0.99995 |
| `dforcefield` | `reset` | Reset the dforcefield instance to its initial state, reapplying the default values including RULES, GLOBAL, and LOCAL. | 22 | 0.99995 |
| `dforcefield` | `save` | Save the dforcefield instance to a file using the generated forcefield definition. | 116 | 0.99995 |
| `dforcefield` | `scriptobject` | Method to return a scriptobject based on the current dforcefield instance. | 77 | 0.99995 |
| `dforcefield` | `set_global` | Update the GLOBAL parameters and adjust the combined parameters accordingly. | 17 | 0.99995 |
| `dforcefield` | `set_local` | Update the LOCAL parameters and adjust the combined parameters accordingly. | 17 | 0.99995 |
| `dforcefield` | `set_rules` | Update the RULES parameters and adjust the combined parameters accordingly. | 17 | 0.99995 |
| `dforcefield` | `show` | Show the corresponding base_class forcefield definition | 4 | 0.99995 |
| `dforcefield` | `to_dict` | Serialize the dforcefield instance to a dictionary, including RULES, GLOBAL, and LOCAL. | 24 | 0.99995 |
| `dforcefield` | `update` | Update multiple attributes of the dforcefield instance at once, including RULES, GLOBAL, and LOCAL. | 16 | 0.99995 |
| `dforcefield` | `update_parameters` | Update self.parameters by combining GLOBAL, LOCAL, RULES, and USER parameters. | 6 | 0.99995 |
| `dforcefield` | `validate` | Validate the dforcefield instance to ensure all required attributes are set. | 14 | 0.99995 |
| `dforcefield` | `values` | Return the values of the merged struct, parameters, and scalar attributes. | 8 | 0.99995 |

<a id="pizza_dscript" name="pizza_dscript"></a>
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; font-size: 0.8em;"><a href="#pizza_dforcefield" title="Go to Previous Module: pizza.dforcefield" style="text-decoration: none;">⬅️ Previous</a>
<a href="#table_of_contents" title="Back to Table of Contents" style="text-decoration: none;">⬆️ TOC</a>
<a href="#pizza_dump3" title="Go to Next Module: pizza.dump3" style="text-decoration: none;">➡️ Next</a>
</div>

## Module `pizza.dscript`

### Class Inheritance Diagram
```mermaid
graph TD;
ScriptTemplate
VariableOccurrences
dscript
lambdaScriptdata
lamdaScript
param
paramauto
pipescript
script
scriptdata
scriptobjectgroup
struct
object --> ScriptTemplate
object --> VariableOccurrences
object --> dscript
object --> pipescript
object --> script
object --> struct
param --> paramauto
param --> scriptdata
paramauto --> lambdaScriptdata
script --> lamdaScript
struct --> param
struct --> scriptobjectgroup
```

**[Class Examples for `pizza/dscript.py` (46)](class_examples.html#pizza_dscript)**

### Methods Table

| Class | Method | Docstring First Paragraph | # Lines | __version__ |
|-------|---------|---------------------------|---------|-------------|
| (module-level) | `autoname` | generate automatically names | 3 | 1.006 |
| (module-level) | `get_metadata` | Return a dictionary of explicitly defined metadata. | 15 | 1.006 |
| `ScriptTemplate` | `__getattr__` | Handles attribute retrieval, checking the following in order: 1. If 'name' is in default_attributes, return the value from attributes if it exists, otherwise return the default value from default_attributes. 2. If 'name' is 'content', return the content (or an empty string if content is not set). 3. If 'name' exists in the attributes dictionary, return its value. 4. If attributes itself exists in __dict__, return the value from attributes if 'name' is found. 5. If all previous checks fail, raise an AttributeError indicating that 'name' is not found. | 39 | 1.006 |
| `ScriptTemplate` | `__init__` | Initializes a new `ScriptTemplate` object. | 96 | 1.006 |
| `ScriptTemplate` | `__repr__` | Return repr(self). | 87 | 1.006 |
| `ScriptTemplate` | `__setattr__` | Implement setattr(self, name, value). | 24 | 1.006 |
| `ScriptTemplate` | `__str__` | Return str(self). | 3 | 1.006 |
| `ScriptTemplate` | `_calculate_content_hash` | Generate hash for content. | 3 | 1.006 |
| `ScriptTemplate` | `_invalidate_cache` | Reset all cache entries. | 10 | 1.006 |
| `ScriptTemplate` | `_update_content` | Helper to set _content and _content_hash, refreshing cache as necessary. | 19 | 1.006 |
| `ScriptTemplate` | `check_variables` | Checks for undefined variables in the ScriptTemplate instance. | 56 | 1.006 |
| `ScriptTemplate` | `detect_variables` | Detects variables in the content of the template using an extended pattern to include indexed variables (e.g., ${var[i]}) if `with_index` is True. | 46 | 1.006 |
| `ScriptTemplate` | `do` | Executes or prepares the script template content based on its attributes and the `softrun` flag. | 105 | 1.006 |
| `ScriptTemplate` | `is_variable_defined` | Checks if a specified variable is defined (either as a default value or a set value). | 29 | 1.006 |
| `ScriptTemplate` | `is_variable_set_value_only` | Checks if a specified variable is defined and set to a specific (non-default) value. | 31 | 1.006 |
| `ScriptTemplate` | `refreshvar` | Detects variables in the content and adds them to definitions if needed. This method ensures that variables like ${varname} are correctly detected and added to the definitions if they are missing. | 14 | 1.006 |
| `dscript` | `__add__` | Concatenates two dscript objects, creating a new dscript object that combines the TEMPLATE and DEFINITIONS of both. This operation avoids deep copying of definitions by creating a new lambdaScriptdata instance from the definitions. | 55 | 1.006 |
| `dscript` | `__call__` | Extracts subobjects from the dscript based on the provided keys. | 37 | 1.006 |
| `dscript` | `__contains__` |  | 2 | 1.006 |
| `dscript` | `__copy__` | copy method | 6 | 1.006 |
| `dscript` | `__deepcopy__` | deep copy method | 8 | 1.006 |
| `dscript` | `__delitem__` |  | 2 | 1.006 |
| `dscript` | `__getattr__` |  | 16 | 1.006 |
| `dscript` | `__getitem__` | Implements index-based retrieval, slicing, or reordering for dscript objects. | 48 | 1.006 |
| `dscript` | `__init__` | Initializes a new `dscript` object. | 65 | 1.006 |
| `dscript` | `__iter__` |  | 2 | 1.006 |
| `dscript` | `__len__` |  | 2 | 1.006 |
| `dscript` | `__mul__` | Multiply the dscript instance to create multiple copies of its script. | 67 | 1.006 |
| `dscript` | `__or__` | Pipes a dscript object with other objects. When other is a dscript object, both objects are concatenated (+) before being converted into a pipescript object When other is a script, pipescript or scriptobjectgroup, self is converted into a pipescript | 29 | 1.006 |
| `dscript` | `__repr__` | Representation of dscript object with additional properties. | 48 | 1.006 |
| `dscript` | `__rmul__` |  | 2 | 1.006 |
| `dscript` | `__setattr__` | Implement setattr(self, name, value). | 24 | 1.006 |
| `dscript` | `__setitem__` |  | 7 | 1.006 |
| `dscript` | `__str__` | Return str(self). | 4 | 1.006 |
| `dscript` | `_build_html_table` | Helper method to build an HTML table with embedded CSS. | 98 | 1.006 |
| `dscript` | `_escape_html` | Helper method to escape HTML special characters in text. | 16 | 1.006 |
| `dscript` | `_format_field` | Helper method to format individual fields for the table. | 20 | 1.006 |
| `dscript` | `_format_list` | Helper method to format list-type fields for the table. | 17 | 1.006 |
| `dscript` | `_format_values` | Helper method to format the 'values' field, which is a list of tuples. | 17 | 1.006 |
| `dscript` | `add_dynamic_script` | Add a dynamic script step to the dscript object. | 33 | 1.006 |
| `dscript` | `check_all_variables` | Checks for undefined variables for each TEMPLATE key in the dscript object. | 38 | 1.006 |
| `dscript` | `clean` | Clean the TEMPLATE by removing or fixing empty steps. | 42 | 1.006 |
| `dscript` | `createEmptyVariables` | Creates empty variables in DEFINITIONS if they don't already exist. | 14 | 1.006 |
| `dscript` | `detect_all_variables` | Detects all variables across all templates in the dscript object. | 20 | 1.006 |
| `dscript` | `do` | Executes or previews all `ScriptTemplate` instances in `TEMPLATE`, concatenating their processed content. Allows for optional headers and footers based on verbosity settings, and offers a preliminary preview mode with `softrun`. Accumulates definitions across all templates if `return_definitions=True`. | 101 | 1.006 |
| `dscript` | `flattenvariables` | Flatten the variable definitions for each step based on usage and precedence. | 60 | 1.006 |
| `dscript` | `generator` | Returns ------- STR generated code corresponding to dscript (using dscript syntax/language). | 9 | 1.006 |
| `dscript` | `get_attributes_by_index` | Returns the attributes of the ScriptTemplate at the specified index. | 4 | 1.006 |
| `dscript` | `get_content_by_index` | Returns the content of the ScriptTemplate at the specified index. | 45 | 1.006 |
| `dscript` | `header` | Generate a formatted header for the DSCRIPT file. | 63 | 1.006 |
| `dscript` | `items` |  | 2 | 1.006 |
| `dscript` | `keys` | Return the keys of the TEMPLATE. | 3 | 1.006 |
| `dscript` | `list_values` | List all unique values taken by a specified key across global definitions and all steps in sequential order. | 179 | 1.006 |
| `dscript` | `pipescript` | Returns a pipescript object by combining script objects corresponding to the given keys. | 73 | 1.006 |
| `dscript` | `print_var_info` | Print or save a neatly formatted table of variable information based on the analysis from `var_info()`. | 205 | 1.006 |
| `dscript` | `reorder` | Reorder the TEMPLATE lines according to a list of indices. | 10 | 1.006 |
| `dscript` | `save` | Save the current script instance to a text file. | 222 | 1.006 |
| `dscript` | `script` | returns the corresponding script | 10 | 1.006 |
| `dscript` | `search` | Search for foreign/definition key values associated with given primary key/definition value(s). | 193 | 1.006 |
| `dscript` | `set_all_variables` | Ensures that all variables in the templates are added to the global definitions with default values if they are not already defined. | 11 | 1.006 |
| `dscript` | `values` | Return the ScriptTemplate objects in TEMPLATE. | 3 | 1.006 |
| `dscript` | `var_info` | Analyze and gather comprehensive information about variables used in the script. | 130 | 1.006 |
| `dscript` | `write` | Writes the provided script content to a specified file in a given folder, with a header if necessary. | 86 | 1.006 |
| `lambdaScriptdata` | `__init__` | Constructor for lambdaScriptdata. It forces the parent's _returnerror parameter to False. | 19 | 1.006 |
| `lamdaScript` | `__init__` | Initialize a new `lambdaScript` instance. | 66 | 1.006 |

<a id="pizza_dump3" name="pizza_dump3"></a>
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; font-size: 0.8em;"><a href="#pizza_dscript" title="Go to Previous Module: pizza.dscript" style="text-decoration: none;">⬅️ Previous</a>
<a href="#table_of_contents" title="Back to Table of Contents" style="text-decoration: none;">⬆️ TOC</a>
<a href="#pizza_dump3_legacy" title="Go to Next Module: pizza.dump3_legacy" style="text-decoration: none;">➡️ Next</a>
</div>

## Module `pizza.dump3`

### Class Inheritance Diagram
```mermaid
graph TD;
Frame
Snap
aselect
dump
tselect
object --> Frame
object --> Snap
object --> aselect
object --> dump
object --> tselect
```

**[Class Examples for `pizza/dump3.py` (2)](class_examples.html#pizza_dump3)**

### Methods Table

| Class | Method | Docstring First Paragraph | # Lines | __version__ |
|-------|---------|---------------------------|---------|-------------|
| `Frame` | `__eq__` | Return self==value. | 2 | 1.0 |
| `Frame` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 4 | 1.0 |
| `Frame` | `__lt__` | Return self<value. | 2 | 1.0 |
| `Frame` | `__repr__` | Return repr(self). | 3 | 1.0 |
| `Snap` | `__eq__` | Return self==value. | 2 | 1.0 |
| `Snap` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 9 | 1.0 |
| `Snap` | `__lt__` | Return self<value. | 2 | 1.0 |
| `Snap` | `__repr__` | Return repr(self). | 2 | 1.0 |
| `aselect` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 2 | 1.0 |
| `aselect` | `all` | Select all atoms in all timesteps or a specific timestep. | 24 | 1.0 |
| `aselect` | `test` | Select atoms based on a boolean expression. | 55 | 1.0 |
| `dump` | `__add__` | Merge two dump objects of the same type. | 14 | 1.0 |
| `dump` | `__init__` | Initialize a dump object. | 38 | 1.0 |
| `dump` | `__repr__` | Return a string representation of the dump object. | 18 | 1.0 |
| `dump` | `assign_column_names` | Assign column names based on the ATOMS section header. | 21 | 1.0 |
| `dump` | `atom` | Extract values for a specific atom ID across all selected snapshots. | 39 | 1.0 |
| `dump` | `clone` | Clone the value from a specific timestep's column to all selected snapshots for atoms with the same ID. | 31 | 1.0 |
| `dump` | `cull` | Remove duplicate snapshots based on timestep. | 14 | 1.0 |
| `dump` | `extra` | Extract bonds, tris, or lines from another object. | 52 | 1.0 |
| `dump` | `findtime` | Find the index of a given timestep. | 17 | 1.0 |
| `dump` | `iterator` | Iterator method to loop over selected snapshots. | 23 | 1.0 |
| `dump` | `kind` | Guess the kind of dump file based on column names. | 26 | 1.0 |
| `dump` | `maxbox` | Return the maximum box dimensions across all selected snapshots. | 21 | 1.0 |
| `dump` | `maxtype` | Return the maximum atom type across all selected snapshots and atoms. | 23 | 1.0 |
| `dump` | `minmax` | Find the minimum and maximum values for a specified column across all selected snapshots and atoms. | 32 | 1.0 |
| `dump` | `names2str` | Convert column names to a sorted string based on their indices. | 11 | 1.0 |
| `dump` | `newcolumn` | Add a new column to every snapshot and initialize it to zero. | 18 | 1.0 |
| `dump` | `read_all` | Read all snapshots from each file in the file list. | 55 | 1.0 |
| `dump` | `read_snapshot` | Read a single snapshot from a file. | 61 | 1.0 |
| `dump` | `realtime` | Return a list of selected snapshot real-time values. | 10 | 1.0 |
| `dump` | `scatter` | Write each selected snapshot to a separate dump file with timestep suffix. | 30 | 1.0 |
| `dump` | `set` | Set a column value using an equation for all selected snapshots and atoms. | 39 | 1.0 |
| `dump` | `setv` | Set a column value using a vector of values for all selected snapshots and atoms. | 24 | 1.0 |
| `dump` | `sort` | Sort atoms or snapshots. | 31 | 1.0 |
| `dump` | `spread` | Spread values from an old column into a new column as integers from 1 to n based on their relative positions. | 30 | 1.0 |
| `dump` | `time` | Return a list of selected snapshot timesteps. | 10 | 1.0 |
| `dump` | `vecs` | Extract values for selected atoms at a specific timestep. | 36 | 1.0 |
| `dump` | `viz` | Return visualization data for a specified snapshot. | 85 | 1.0 |
| `dump` | `write` | Write the dump object to a LAMMPS dump file. | 33 | 1.0 |
| `tselect` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 2 | 1.0 |
| `tselect` | `all` | Select all timesteps. | 9 | 1.0 |
| `tselect` | `none` | Deselect all timesteps. | 8 | 1.0 |
| `tselect` | `one` | Select only a specific timestep. | 18 | 1.0 |
| `tselect` | `skip` | Select every Mth timestep. | 20 | 1.0 |
| `tselect` | `test` | Select timesteps based on a boolean expression. | 23 | 1.0 |

<a id="pizza_dump3_legacy" name="pizza_dump3_legacy"></a>
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; font-size: 0.8em;"><a href="#pizza_dump3" title="Go to Previous Module: pizza.dump3" style="text-decoration: none;">⬅️ Previous</a>
<a href="#table_of_contents" title="Back to Table of Contents" style="text-decoration: none;">⬆️ TOC</a>
<a href="#pizza_forcefield" title="Go to Next Module: pizza.forcefield" style="text-decoration: none;">➡️ Next</a>
</div>

## Module `pizza.dump3_legacy`

### Class Inheritance Diagram
```mermaid
graph TD;
Frame
Snap
aselect
dump
tselect
object --> Frame
object --> Snap
object --> aselect
object --> dump
object --> tselect
```

**[Class Examples for `pizza/dump3_legacy.py` (1)](class_examples.html#pizza_dump3_legacy)**

### Methods Table

| Class | Method | Docstring First Paragraph | # Lines | __version__ |
|-------|---------|---------------------------|---------|-------------|
| `Frame` | `__eq__` | Return self==value. | 2 | 1.0 |
| `Frame` | `__ge__` | Return self>=value. | 2 | 1.0 |
| `Frame` | `__gt__` | Return self>value. | 2 | 1.0 |
| `Frame` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 2 | 1.0 |
| `Frame` | `__le__` | Return self<=value. | 2 | 1.0 |
| `Frame` | `__lt__` | Return self<value. | 2 | 1.0 |
| `Frame` | `__ne__` | Return self!=value. | 2 | 1.0 |
| `Frame` | `__repr__` | Return repr(self). | 6 | 1.0 |
| `Snap` | `__eq__` | Return self==value. | 2 | 1.0 |
| `Snap` | `__ge__` | Return self>=value. | 2 | 1.0 |
| `Snap` | `__gt__` | Return self>value. | 2 | 1.0 |
| `Snap` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 2 | 1.0 |
| `Snap` | `__le__` | Return self<=value. | 2 | 1.0 |
| `Snap` | `__lt__` | Return self<value. | 2 | 1.0 |
| `Snap` | `__ne__` | Return self!=value. | 2 | 1.0 |
| `Snap` | `__repr__` | Return repr(self). | 3 | 1.0 |
| `aselect` | `__init__` | private constructor (not to be used directly) | 3 | 1.0 |
| `aselect` | `all` | select all atoms: aselect.all() aselect.all(timestep) | 20 | 1.0 |
| `aselect` | `test` | " aselect.test(stringexpression [,timestep]) example: aselect.test("$y>0.4e-3 and $y<0.6e-3") | 71 | 1.0 |
| `dump` | `__add__` | merge dump objects of the same kind/type | 8 | 1.0 |
| `dump` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 31 | 1.0 |
| `dump` | `__repr__` | Return repr(self). | 12 | 1.0 |
| `dump` | `atom` |  | 29 | 1.0 |
| `dump` | `clone` |  | 16 | 1.0 |
| `dump` | `compare_atom` |  | 7 | 1.0 |
| `dump` | `compare_time` |  | 7 | 1.0 |
| `dump` | `cull` |  | 7 | 1.0 |
| `dump` | `delete` |  | 11 | 1.0 |
| `dump` | `extra` |  | 61 | 1.0 |
| `dump` | `findtime` |  | 5 | 1.0 |
| `dump` | `frame` | simplified class to access properties of a snapshot (INRAE\Olivier Vitrac) | 22 | 1.0 |
| `dump` | `iterator` |  | 9 | 1.0 |
| `dump` | `kind` | guessed kind of dump file based on column names (possibility to supply a personnalized list) (INRAE\Olivier Vitrac) | 31 | 1.0 |
| `dump` | `map` |  | 6 | 1.0 |
| `dump` | `maxbox` |  | 19 | 1.0 |
| `dump` | `maxtype` |  | 13 | 1.0 |
| `dump` | `minmax` |  | 16 | 1.0 |
| `dump` | `names2str` |  | 13 | 1.0 |
| `dump` | `newcolumn` |  | 12 | 1.0 |
| `dump` | `next` |  | 40 | 1.0 |
| `dump` | `owrap` |  | 30 | 1.0 |
| `dump` | `read_all` |  | 53 | 1.0 |
| `dump` | `read_snapshot` | low-level method to read a snapshot from a file identifier | 123 | 1.0 |
| `dump` | `realtime` | time as simulated: realtime() | 10 | 1.0 |
| `dump` | `scale` |  | 14 | 1.0 |
| `dump` | `scale_one` |  | 49 | 1.0 |
| `dump` | `scatter` |  | 42 | 1.0 |
| `dump` | `set` |  | 22 | 1.0 |
| `dump` | `setv` |  | 17 | 1.0 |
| `dump` | `sort` |  | 17 | 1.0 |
| `dump` | `sort_one` |  | 6 | 1.0 |
| `dump` | `spread` |  | 24 | 1.0 |
| `dump` | `time` | timestep as stored: time() | 10 | 1.0 |
| `dump` | `unscale` |  | 14 | 1.0 |
| `dump` | `unscale_one` |  | 39 | 1.0 |
| `dump` | `unwrap` |  | 18 | 1.0 |
| `dump` | `vecs` | vecs(timeste,columname1,columname2,...) Examples: tab = vecs(timestep,"id","x","y") tab = vecs(timestep,["id","x","y"],"z") X.vecs(X.time()[50],"vx","vy") | 35 | 1.0 |
| `dump` | `viz` |  | 94 | 1.0 |
| `dump` | `wrap` |  | 18 | 1.0 |
| `dump` | `write` |  | 55 | 1.0 |
| `tselect` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 2 | 1.0 |
| `tselect` | `all` |  | 7 | 1.0 |
| `tselect` | `none` |  | 6 | 1.0 |
| `tselect` | `one` |  | 9 | 1.0 |
| `tselect` | `skip` |  | 14 | 1.0 |
| `tselect` | `test` |  | 19 | 1.0 |

<a id="pizza_forcefield" name="pizza_forcefield"></a>
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; font-size: 0.8em;"><a href="#pizza_dump3_legacy" title="Go to Previous Module: pizza.dump3_legacy" style="text-decoration: none;">⬅️ Previous</a>
<a href="#table_of_contents" title="Back to Table of Contents" style="text-decoration: none;">⬆️ TOC</a>
<a href="#pizza_generic" title="Go to Next Module: pizza.generic" style="text-decoration: none;">➡️ Next</a>
</div>

## Module `pizza.forcefield`

### Class Inheritance Diagram
```mermaid
graph TD;
forcefield
none
param
paramauto
parameterforcefield
rigidwall
saltTLSPH
smd
solidfood
struct
tlsph
tlsphalone
ulsph
ulsphalone
water
forcefield --> smd
forcefield --> tlsphalone
none --> rigidwall
object --> forcefield
object --> struct
param --> paramauto
paramauto --> parameterforcefield
smd --> none
smd --> tlsph
smd --> ulsph
smd --> ulsphalone
struct --> param
tlsph --> saltTLSPH
tlsph --> solidfood
ulsph --> water
```

**[Class Examples for `pizza/forcefield.py` (1)](class_examples.html#pizza_forcefield)**

### Methods Table

| Class | Method | Docstring First Paragraph | # Lines | __version__ |
|-------|---------|---------------------------|---------|-------------|
| `forcefield` | `__repr__` | disp method | 21 | 1.006 |
| `forcefield` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 1.006 |
| `forcefield` | `pair_diagcoeff` | Generate and return the diagonal pair coefficients for the current forcefield instance. | 63 | 1.006 |
| `forcefield` | `pair_offdiagcoeff` | Generate and return the off-diagonal pair coefficients for the current forcefield instance. | 87 | 1.006 |
| `forcefield` | `pair_style` | Generate and return the pair style command for the current forcefield instance. | 58 | 1.006 |
| `forcefield` | `printheader` | print header | 7 | 1.006 |
| `none` | `__repr__` | disp method | 21 | 1.006 |
| `none` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 1.006 |
| `none` | `pair_diagcoeff` | Generate and return the diagonal pair coefficients for the current forcefield instance. | 63 | 1.006 |
| `none` | `pair_offdiagcoeff` | Generate and return the off-diagonal pair coefficients for the current forcefield instance. | 87 | 1.006 |
| `none` | `pair_style` | Generate and return the pair style command for the current forcefield instance. | 58 | 1.006 |
| `none` | `printheader` | print header | 7 | 1.006 |
| `parameterforcefield` | `__init__` | Constructor for parameterforcefield. It forces the parent's _returnerror parameter to False. | 19 | 1.006 |
| `rigidwall` | `__init__` | rigidwall forcefield: rigidwall(beadtype=index, userid="mywall") | 12 | 1.006 |
| `rigidwall` | `__repr__` | disp method | 21 | 1.006 |
| `rigidwall` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 1.006 |
| `rigidwall` | `pair_diagcoeff` | Generate and return the diagonal pair coefficients for the current forcefield instance. | 63 | 1.006 |
| `rigidwall` | `pair_offdiagcoeff` | Generate and return the off-diagonal pair coefficients for the current forcefield instance. | 87 | 1.006 |
| `rigidwall` | `pair_style` | Generate and return the pair style command for the current forcefield instance. | 58 | 1.006 |
| `rigidwall` | `printheader` | print header | 7 | 1.006 |
| `saltTLSPH` | `__init__` | saltTLSPH forcefield: saltTLSPH(beadtype=index, userid="salt") | 22 | 1.006 |
| `saltTLSPH` | `__repr__` | disp method | 21 | 1.006 |
| `saltTLSPH` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 1.006 |
| `saltTLSPH` | `pair_diagcoeff` | Generate and return the diagonal pair coefficients for the current forcefield instance. | 63 | 1.006 |
| `saltTLSPH` | `pair_offdiagcoeff` | Generate and return the off-diagonal pair coefficients for the current forcefield instance. | 87 | 1.006 |
| `saltTLSPH` | `pair_style` | Generate and return the pair style command for the current forcefield instance. | 58 | 1.006 |
| `saltTLSPH` | `printheader` | print header | 7 | 1.006 |
| `smd` | `__repr__` | disp method | 21 | 1.006 |
| `smd` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 1.006 |
| `smd` | `pair_diagcoeff` | Generate and return the diagonal pair coefficients for the current forcefield instance. | 63 | 1.006 |
| `smd` | `pair_offdiagcoeff` | Generate and return the off-diagonal pair coefficients for the current forcefield instance. | 87 | 1.006 |
| `smd` | `pair_style` | Generate and return the pair style command for the current forcefield instance. | 58 | 1.006 |
| `smd` | `printheader` | print header | 7 | 1.006 |
| `solidfood` | `__init__` | food forcefield: solidfood(beadtype=index, userid="myfood") | 22 | 1.006 |
| `solidfood` | `__repr__` | disp method | 21 | 1.006 |
| `solidfood` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 1.006 |
| `solidfood` | `pair_diagcoeff` | Generate and return the diagonal pair coefficients for the current forcefield instance. | 63 | 1.006 |
| `solidfood` | `pair_offdiagcoeff` | Generate and return the off-diagonal pair coefficients for the current forcefield instance. | 87 | 1.006 |
| `solidfood` | `pair_style` | Generate and return the pair style command for the current forcefield instance. | 58 | 1.006 |
| `solidfood` | `printheader` | print header | 7 | 1.006 |
| `tlsph` | `__repr__` | disp method | 21 | 1.006 |
| `tlsph` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 1.006 |
| `tlsph` | `pair_diagcoeff` | Generate and return the diagonal pair coefficients for the current forcefield instance. | 63 | 1.006 |
| `tlsph` | `pair_offdiagcoeff` | Generate and return the off-diagonal pair coefficients for the current forcefield instance. | 87 | 1.006 |
| `tlsph` | `pair_style` | Generate and return the pair style command for the current forcefield instance. | 58 | 1.006 |
| `tlsph` | `printheader` | print header | 7 | 1.006 |
| `tlsphalone` | `__repr__` | disp method | 21 | 1.006 |
| `tlsphalone` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 1.006 |
| `tlsphalone` | `pair_diagcoeff` | Generate and return the diagonal pair coefficients for the current forcefield instance. | 63 | 1.006 |
| `tlsphalone` | `pair_offdiagcoeff` | Generate and return the off-diagonal pair coefficients for the current forcefield instance. | 87 | 1.006 |
| `tlsphalone` | `pair_style` | Generate and return the pair style command for the current forcefield instance. | 58 | 1.006 |
| `tlsphalone` | `printheader` | print header | 7 | 1.006 |
| `ulsph` | `__repr__` | disp method | 21 | 1.006 |
| `ulsph` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 1.006 |
| `ulsph` | `pair_diagcoeff` | Generate and return the diagonal pair coefficients for the current forcefield instance. | 63 | 1.006 |
| `ulsph` | `pair_offdiagcoeff` | Generate and return the off-diagonal pair coefficients for the current forcefield instance. | 87 | 1.006 |
| `ulsph` | `pair_style` | Generate and return the pair style command for the current forcefield instance. | 58 | 1.006 |
| `ulsph` | `printheader` | print header | 7 | 1.006 |
| `ulsphalone` | `__repr__` | disp method | 21 | 1.006 |
| `ulsphalone` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 1.006 |
| `ulsphalone` | `pair_diagcoeff` | Generate and return the diagonal pair coefficients for the current forcefield instance. | 63 | 1.006 |
| `ulsphalone` | `pair_offdiagcoeff` | Generate and return the off-diagonal pair coefficients for the current forcefield instance. | 87 | 1.006 |
| `ulsphalone` | `pair_style` | Generate and return the pair style command for the current forcefield instance. | 58 | 1.006 |
| `ulsphalone` | `printheader` | print header | 7 | 1.006 |
| `water` | `__init__` | water forcefield: water(beadtype=index, userid="myfluid") | 16 | 1.006 |
| `water` | `__repr__` | disp method | 21 | 1.006 |
| `water` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 1.006 |
| `water` | `pair_diagcoeff` | Generate and return the diagonal pair coefficients for the current forcefield instance. | 63 | 1.006 |
| `water` | `pair_offdiagcoeff` | Generate and return the off-diagonal pair coefficients for the current forcefield instance. | 87 | 1.006 |
| `water` | `pair_style` | Generate and return the pair style command for the current forcefield instance. | 58 | 1.006 |
| `water` | `printheader` | print header | 7 | 1.006 |

<a id="pizza_generic" name="pizza_generic"></a>
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; font-size: 0.8em;"><a href="#pizza_forcefield" title="Go to Previous Module: pizza.forcefield" style="text-decoration: none;">⬅️ Previous</a>
<a href="#table_of_contents" title="Back to Table of Contents" style="text-decoration: none;">⬆️ TOC</a>
<a href="#pizza_group" title="Go to Next Module: pizza.group" style="text-decoration: none;">➡️ Next</a>
</div>

## Module `pizza.generic`

### Class Inheritance Diagram
```mermaid
graph TD;
USERSMD
forcefield
generic
genericdata
param
paramauto
parameterforcefield
smd
struct
ulsph
water
forcefield --> smd
generic --> USERSMD
object --> forcefield
object --> generic
object --> struct
param --> paramauto
paramauto --> parameterforcefield
parameterforcefield --> genericdata
smd --> ulsph
struct --> param
ulsph --> water
```

**[Class Examples for `pizza/generic.py` (1)](class_examples.html#pizza_generic)**

### Methods Table

| Class | Method | Docstring First Paragraph | # Lines | __version__ |
|-------|---------|---------------------------|---------|-------------|
| `USERSMD` | `__init__` | generic helper constructor | 11 | 0.9971 |
| `USERSMD` | `__repr__` | representation of generic() | 12 | 0.9971 |
| `USERSMD` | `newtonianfluid` | newtonianfluid() returns a parameterized ULSPH forcefield with prescribed viscosity (mu [Pa.s] or nu in [m2/s]) and density (rho). Based on recommendations of J. Comput. Phys 1997, 136, 214–226 | 24 | 0.9971 |
| `generic` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 3 | 0.9971 |
| `generic` | `__repr__` | representation of generic() | 12 | 0.9971 |

<a id="pizza_group" name="pizza_group"></a>
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; font-size: 0.8em;"><a href="#pizza_generic" title="Go to Previous Module: pizza.generic" style="text-decoration: none;">⬅️ Previous</a>
<a href="#table_of_contents" title="Back to Table of Contents" style="text-decoration: none;">⬆️ TOC</a>
<a href="#pizza_private_mstruct" title="Go to Next Module: pizza.private.mstruct" style="text-decoration: none;">➡️ Next</a>
</div>

## Module `pizza.group`

### Class Inheritance Diagram
```mermaid
graph TD;
Operation
dscript
group
groupcollection
groupobject
pipescript
object --> Operation
object --> dscript
object --> group
object --> groupcollection
object --> groupobject
object --> pipescript
```

**[Class Examples for `pizza/group.py` (6)](class_examples.html#pizza_group)**

### Methods Table

| Class | Method | Docstring First Paragraph | # Lines | __version__ |
|-------|---------|---------------------------|---------|-------------|
| (module-level) | `format_table` | Formats a table with given headers and rows, truncating text based on maximum column widths and aligning content based on the specified alignment. | 82 | 1.006 |
| (module-level) | `generate_random_name` |  | 3 | 1.006 |
| (module-level) | `truncate_text` | Truncates the input text to fit within the specified maximum width. If the text is longer than `maxwidth`, it is shortened by keeping the beginning and trailing parts, separated by " [...] ". | 26 | 1.006 |
| `Operation` | `__add__` | overload + as union | 3 | 1.006 |
| `Operation` | `__init__` | Initializes a new Operation instance with given parameters. | 10 | 1.006 |
| `Operation` | `__mul__` | overload * as intersect | 3 | 1.006 |
| `Operation` | `__repr__` | detailed representation | 10 | 1.006 |
| `Operation` | `__str__` | string representation | 18 | 1.006 |
| `Operation` | `__sub__` | overload - as subtract | 3 | 1.006 |
| `Operation` | `_operate` | Implements algebraic operations between self and other Operation instances. | 40 | 1.006 |
| `Operation` | `append` | Appends a single operand to the operands list of the Operation instance. | 3 | 1.006 |
| `Operation` | `extend` | Extends the operands list of the Operation instance with multiple operands. | 3 | 1.006 |
| `Operation` | `generateID` | Generates an ID for the Operation instance based on its operands or name. | 8 | 1.006 |
| `Operation` | `generate_hashname` | Generates an ID for the Operation instance based on its operands or name. | 9 | 1.006 |
| `Operation` | `get_proper_operand` | Returns the proper operand depending on whether the operation is finalized. | 17 | 1.006 |
| `Operation` | `is_empty` | Checks if the Operation instance has no operands. | 3 | 1.006 |
| `Operation` | `is_unary` | Checks if the Operation instance has exactly one operand. | 3 | 1.006 |
| `Operation` | `isfinalized` | Checks whether the Operation instance is finalized. Returns: - bool: True if the Operation is finalized, otherwise False. Functionality: - An Operation is considered finalized if its operator is not one of the algebraic operators '+', '-', '*'. | 10 | 1.006 |
| `Operation` | `script` | Generate the LAMMPS code using the dscript and script classes. | 14 | 1.006 |
| `group` | `__call__` | Allows subindexing of the group object using callable syntax with multiple keys. | 27 | 1.006 |
| `group` | `__copy__` | copy method | 6 | 1.006 |
| `group` | `__deepcopy__` | deep copy method | 8 | 1.006 |
| `group` | `__getattr__` | Allows accessing operations via attribute-style notation. If the attribute is one of the core attributes, returns it directly. For other attributes, searches for an operation with a matching name in the _operations list. | 33 | 1.006 |
| `group` | `__getitem__` | Enable shorthand for G.operations[G.find(operation_name)] using G[operation_name], or accessing operation by index using G[index]. | 18 | 1.006 |
| `group` | `__init__` | Initializes a new instance of the group class. | 57 | 1.006 |
| `group` | `__len__` | return the number of stored operations | 3 | 1.006 |
| `group` | `__repr__` | Returns a neatly formatted table representation of the group's operations. | 28 | 1.006 |
| `group` | `__setattr__` | Allows deletion of an operation via 'G.operation_name = []' after construction. During construction, attributes are set normally. | 20 | 1.006 |
| `group` | `__str__` | Return str(self). | 2 | 1.006 |
| `group` | `_get_subobject` | Retrieves a subobject based on the provided key. | 37 | 1.006 |
| `group` | `add_group_criteria` | Adds group(s) using existing methods based on key-value pairs. | 36 | 1.006 |
| `group` | `add_group_criteria_single` | Adds a single group based on criteria. | 99 | 1.006 |
| `group` | `add_operation` | add an operation | 6 | 1.006 |
| `group` | `byid` | select atoms by id and store them in group G.id(group_name,id_values) | 11 | 1.006 |
| `group` | `byregion` | set a group of atoms based on a regionID G.region(group_name,regionID) | 9 | 1.006 |
| `group` | `bytype` | select atoms by type and store them in group G.type(group_name,type_values) | 11 | 1.006 |
| `group` | `byvariable` | Sets a group of atoms based on a variable. | 16 | 1.006 |
| `group` | `clear` | clear group G.clear(group_name) | 9 | 1.006 |
| `group` | `clearall` | clear all operations | 3 | 1.006 |
| `group` | `code` | Joins the `code` attributes of all stored `operation` objects with ' '. | 5 | 1.006 |
| `group` | `copy` | Copies a stored operation to a new operation with a different name. | 20 | 1.006 |
| `group` | `count` | Generates DSCRIPT counters for specified groups with LAMMPS variable definitions and print commands. | 110 | 1.006 |
| `group` | `create` | create group G.create(group_name) | 9 | 1.006 |
| `group` | `create_groups` |  | 5 | 1.006 |
| `group` | `delete` | Deletes one or more stored operations based on their names. | 41 | 1.006 |
| `group` | `disp` | display the content of an operation | 7 | 1.006 |
| `group` | `dscript` | Generates a dscript object containing the group's LAMMPS commands. | 24 | 1.006 |
| `group` | `evaluate` | Evaluates the operation and stores the result in a new group. Expressions could combine +, - and * like o1+o2+o3-o4+o5+o6 | 65 | 1.006 |
| `group` | `find` | Returns the index of an operation based on its name. | 7 | 1.006 |
| `group` | `format_cell_content` |  | 7 | 1.006 |
| `group` | `generate_group_definitions_from_collection` | Generates group definitions based on the collection of groupobject instances. | 15 | 1.006 |
| `group` | `get_by_name` | Returns the operation matching "operation_name" Usage: group.get_by_name("operation_name") To be used by Operation, not by end-user, which should prefer getattr() | 10 | 1.006 |
| `group` | `get_group_criteria` | Retrieve the criteria that define a group. Handles group_name as a string or number. | 33 | 1.006 |
| `group` | `intersect` | Intersect group1, group2, group3 and store the result in group_name. Example usage: group.intersect(group_name, group1, group2, group3,...) | 10 | 1.006 |
| `group` | `list` | return the list of all operations | 3 | 1.006 |
| `group` | `operation_exists` | Returns true if "operation_name" exists To be used by Operation, not by end-user, which should prefer find() | 6 | 1.006 |
| `group` | `pipescript` | Generates a pipescript object containing the group's LAMMPS commands. | 36 | 1.006 |
| `group` | `reindex` | Change the index of a stored operation. | 19 | 1.006 |
| `group` | `rename` | Rename a stored operation. | 22 | 1.006 |
| `group` | `script` | Generates a script object containing the group's LAMMPS commands. | 19 | 1.006 |
| `group` | `subtract` | Subtract group2, group3 from group1 and store the result in group_name. Example usage: group.subtract(group_name, group1, group2, group3,...) | 10 | 1.006 |
| `group` | `union` | Union group1, group2, group3 and store the result in group_name. Example usage: group.union(group_name, group1, group2, group3,...) | 10 | 1.006 |
| `group` | `variable` | Assigns an expression to a LAMMPS variable. | 19 | 1.006 |
| `groupcollection` | `__add__` | Adds a `groupobject` or another `groupcollection` to this collection. | 19 | 1.006 |
| `groupcollection` | `__getitem__` | Retrieves a `groupobject` by its index. | 14 | 1.006 |
| `groupcollection` | `__iadd__` | In-place addition of a `groupobject` or a list/tuple of `groupobject` instances. | 23 | 1.006 |
| `groupcollection` | `__init__` | Initializes a new instance of the groupcollection class. | 34 | 1.006 |
| `groupcollection` | `__iter__` | Returns an iterator over the `groupobject` instances in the collection. | 8 | 1.006 |
| `groupcollection` | `__len__` | Returns the number of `groupobject` instances in the collection. | 8 | 1.006 |
| `groupcollection` | `__repr__` | Returns a neatly formatted string representation of the groupcollection. | 24 | 1.006 |
| `groupcollection` | `__str__` | Returns the same representation as `__repr__`. | 8 | 1.006 |
| `groupcollection` | `append` | Appends a `groupobject` to the collection. | 13 | 1.006 |
| `groupcollection` | `clear` | Clears all `groupobject` instances from the collection. | 5 | 1.006 |
| `groupcollection` | `extend` | Extends the collection with a list or tuple of `groupobject` instances. | 17 | 1.006 |
| `groupcollection` | `list` | Return a unique, stable list of groups in the original order | 3 | 1.006 |
| `groupcollection` | `mass` | Generates LAMMPS mass commands for each unique beadtype in the collection. | 71 | 1.006 |
| `groupcollection` | `remove` | Removes a `groupobject` from the collection. | 11 | 1.006 |
| `groupobject` | `__add__` | Adds this groupobject to another groupobject or a groupcollection. | 19 | 1.006 |
| `groupobject` | `__init__` | Initializes a new instance of the groupobject class. | 34 | 1.006 |
| `groupobject` | `__radd__` | Adds this groupobject to another groupobject or a groupcollection from the right. | 19 | 1.006 |
| `groupobject` | `__repr__` | Returns an unambiguous string representation of the groupobject. | 8 | 1.006 |
| `groupobject` | `__str__` | Returns a readable string representation of the groupobject. | 5 | 1.006 |

<a id="pizza_private_mstruct" name="pizza_private_mstruct"></a>
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; font-size: 0.8em;"><a href="#pizza_group" title="Go to Previous Module: pizza.group" style="text-decoration: none;">⬅️ Previous</a>
<a href="#table_of_contents" title="Back to Table of Contents" style="text-decoration: none;">⬆️ TOC</a>
<a href="#pizza_private_utils" title="Go to Next Module: pizza.private.utils" style="text-decoration: none;">➡️ Next</a>
</div>

## Module `pizza.private.mstruct`

### Class Inheritance Diagram
```mermaid
graph TD;
AttrErrorDict
SafeEvaluator
param
paramauto
pstr
struct
NodeVisitor --> SafeEvaluator
dict --> AttrErrorDict
object --> struct
param --> paramauto
str --> pstr
struct --> param
```

**[Class Examples for `pizza/private/mstruct.py` (20)](class_examples.html#pizza_private_mstruct)**

### Methods Table

| Class | Method | Docstring First Paragraph | # Lines | __version__ |
|-------|---------|---------------------------|---------|-------------|
| (module-level) | `evaluate_with_placeholders` | Evaluates only unescaped placeholders of the form ${...} in the input text. Escaped placeholders (\${...}) are left as literal text (after removing the escape). | 47 | 1.0062 |
| (module-level) | `is_empty` | Return True if value is considered empty (None, "", [] or ()). | 3 | 1.0062 |
| (module-level) | `is_literal_string` | Returns True if the first non-blank character in the string is '$' and it is not immediately followed by '{' or '['. | 20 | 1.0062 |
| `AttrErrorDict` | `__getitem__` | x.__getitem__(y) <==> x[y] | 11 | 1.0062 |
| `SafeEvaluator` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 30 | 1.0062 |
| `SafeEvaluator` | `evaluate` |  | 3 | 1.0062 |
| `SafeEvaluator` | `generic_visit` | Called if no explicit visitor function exists for a node. | 2 | 1.0062 |
| `SafeEvaluator` | `visit_Attribute` |  | 12 | 1.0062 |
| `SafeEvaluator` | `visit_BinOp` |  | 9 | 1.0062 |
| `SafeEvaluator` | `visit_Call` |  | 7 | 1.0062 |
| `SafeEvaluator` | `visit_Constant` |  | 2 | 1.0062 |
| `SafeEvaluator` | `visit_Dict` | Evaluate a dictionary expression by safely evaluating each key and value. This allows expressions like: {"a": ${v1}+${v2}, "b": ${var}}. | 6 | 1.0062 |
| `SafeEvaluator` | `visit_ExtSlice` |  | 3 | 1.0062 |
| `SafeEvaluator` | `visit_Index` |  | 2 | 1.0062 |
| `SafeEvaluator` | `visit_List` |  | 2 | 1.0062 |
| `SafeEvaluator` | `visit_Name` |  | 4 | 1.0062 |
| `SafeEvaluator` | `visit_Slice` |  | 5 | 1.0062 |
| `SafeEvaluator` | `visit_Subscript` |  | 7 | 1.0062 |
| `SafeEvaluator` | `visit_Tuple` |  | 2 | 1.0062 |
| `SafeEvaluator` | `visit_UnaryOp` |  | 6 | 1.0062 |
| `param` | `__add__` | Add two structure objects, with precedence as follows: | 49 | 1.0062 |
| `param` | `__call__` | Extract an evaluated sub-structure based on the specified keys, keeping the same class type. | 25 | 1.0062 |
| `param` | `__contains__` | in override | 3 | 1.0062 |
| `param` | `__copy__` | copy method | 6 | 1.0062 |
| `param` | `__deepcopy__` | deep copy method | 8 | 1.0062 |
| `param` | `__delattr__` | Delete an instance attribute if it exists and is not a class or excluded attribute. | 10 | 1.0062 |
| `param` | `__getattr__` | get attribute override | 3 | 1.0062 |
| `param` | `__getitem__` | s[i] returns the ith element of the structure s[:4] returns a structure with the four first fields s[[1,3]] returns the second and fourth elements | 41 | 1.0062 |
| `param` | `__getstate__` | getstate for cooperative inheritance / duplication | 3 | 1.0062 |
| `param` | `__iadd__` | iadd a structure set sortdefintions=True to sort definitions (to maintain executability) | 11 | 1.0062 |
| `param` | `__init__` | constructor | 8 | 1.0062 |
| `param` | `__isub__` | isub a structure | 9 | 1.0062 |
| `param` | `__iter__` | struct iterator | 6 | 1.0062 |
| `param` | `__len__` | return the number of fields | 4 | 1.0062 |
| `param` | `__lshift__` | Allows the syntax: | 15 | 1.0062 |
| `param` | `__next__` | increment iterator | 7 | 1.0062 |
| `param` | `__repr__` | display method | 68 | 1.0062 |
| `param` | `__setattr__` | set attribute override | 3 | 1.0062 |
| `param` | `__setitem__` | set the ith element of the structure | 24 | 1.0062 |
| `param` | `__setstate__` | setstate for cooperative inheritance / duplication | 3 | 1.0062 |
| `param` | `__str__` | Return str(self). | 2 | 1.0062 |
| `param` | `__sub__` | sub a structure | 10 | 1.0062 |
| `param` | `check` | populate fields from a default structure check(defaultstruct) missing field, None and [] values are replaced by default ones | 19 | 1.0062 |
| `param` | `clear` | clear() delete all fields while preserving the original class | 3 | 1.0062 |
| `param` | `convert_matlab_like_arrays` | Converts Matlab-like array syntax (including hybrid notations) into a NumPy-esque list syntax in multiple passes. | 166 | 1.0062 |
| `param` | `dict2struct` | create a structure from a dictionary | 8 | 1.0062 |
| `param` | `disp` | display method | 3 | 1.0062 |
| `param` | `dispmax` | optimize display | 8 | 1.0062 |
| `param` | `escape` | escape \${} as ${{}} --> keep variable names convert ${} as {} --> prepare Python replacement | 35 | 1.0062 |
| `param` | `eval` | Eval method for structure such as MS.alias | 210 | 1.0062 |
| `param` | `expand_ranges` | Expands MATLAB-style ranges in a string. | 44 | 1.0062 |
| `param` | `format` | Format a string with fields using {field} as placeholders. Handles expressions like ${variable1}. | 55 | 1.0062 |
| `param` | `format_array` | Format NumPy array for display with distinctions for scalars, row/column vectors, and ND arrays. Recursively formats multi-dimensional arrays without introducing unwanted commas. | 106 | 1.0062 |
| `param` | `format_legacy` | format a string with field (use {field} as placeholders) s.replace(string), s.replace(string,escape=True) where: s is a struct object string is a string with possibly ${variable1} escape is a flag to prevent ${} replaced by {} | 27 | 1.0062 |
| `param` | `formateval` | format method with evaluation feature | 59 | 1.0062 |
| `param` | `fromkeys` | returns a structure from keys | 3 | 1.0062 |
| `param` | `fromkeysvalues` | struct.keysvalues(keys,values) creates a structure from keys and values use makeparam = True to create a param instead of struct | 18 | 1.0062 |
| `param` | `generator` | Generate Python code of the equivalent structure. | 73 | 1.0062 |
| `param` | `getattr` | Get attribute override to access both instance attributes and properties if allowed. | 11 | 1.0062 |
| `param` | `getval` | returns the evaluated value | 4 | 1.0062 |
| `param` | `hasattr` | Return true if the field exists, considering properties as regular attributes if allowed. | 7 | 1.0062 |
| `param` | `importfrom` | Import values from 's' into self according to the following rules: | 30 | 1.0062 |
| `param` | `isdefined` | isdefined(ref) returns true if it is defined in ref | 19 | 1.0062 |
| `param` | `isstrdefined` | isstrdefined(string,ref) returns true if it is defined in ref | 14 | 1.0062 |
| `param` | `isstrexpression` | isstrexpression(string) returns true if s contains an expression | 5 | 1.0062 |
| `param` | `items` | return all elements as iterable key, value | 3 | 1.0062 |
| `param` | `keys` | return the fields | 4 | 1.0062 |
| `param` | `keyssorted` | sort keys by length() | 5 | 1.0062 |
| `param` | `np2str` | Convert all NumPy entries of s into their string representations, handling both lists and dictionaries. | 58 | 1.0062 |
| `param` | `numrepl` | Replace all placeholders of the form ${key} in the given text by the corresponding numeric value from the instance fields, under the following conditions: | 56 | 1.0062 |
| `param` | `protect` | protect $variable as ${variable} | 11 | 1.0062 |
| `param` | `read` | read the equivalent structure read(filename) | 35 | 1.0062 |
| `param` | `safe_fstring` | Safely evaluate expressions in ${} using SafeEvaluator. | 61 | 1.0062 |
| `param` | `scan` | scan(string) scan a string for variables | 11 | 1.0062 |
| `param` | `set` | initialization | 3 | 1.0062 |
| `param` | `setattr` | set field and value | 6 | 1.0062 |
| `param` | `sortdefinitions` | sortdefintions sorts all definitions so that they can be executed as param(). If any inconsistency is found, an error message is generated. | 53 | 1.0062 |
| `param` | `struct2dict` | create a dictionary from the current structure | 3 | 1.0062 |
| `param` | `struct2param` | convert an object struct() to param() | 8 | 1.0062 |
| `param` | `toparamauto` | convert a param instance into a paramauto instance toparamauto() | 6 | 1.0062 |
| `param` | `tostatic` | convert dynamic a param() object to a static struct() object. note: no interpretation note: use tostruct() to interpret them and convert it to struct note: tostatic().struct2param() makes it reversible | 7 | 1.0062 |
| `param` | `tostruct` | generate the evaluated structure tostruct(protection=False) | 6 | 1.0062 |
| `param` | `update` | Update multiple fields at once, while protecting certain attributes. | 21 | 1.0062 |
| `param` | `validkeys` | Validate and return the subset of keys from the provided list that are valid in the instance. | 38 | 1.0062 |
| `param` | `values` | return the values | 4 | 1.0062 |
| `param` | `write` | write the equivalent structure (not recursive for nested struct) write(filename, overwrite=True, mkdir=False) | 38 | 1.0062 |
| `param` | `zip` | zip keys and values | 3 | 1.0062 |
| `paramauto` | `__add__` | Add two structure objects, with precedence as follows: | 3 | 1.0062 |
| `paramauto` | `__call__` | Extract an evaluated sub-structure based on the specified keys, keeping the same class type. | 25 | 1.0062 |
| `paramauto` | `__contains__` | in override | 3 | 1.0062 |
| `paramauto` | `__copy__` | copy method | 6 | 1.0062 |
| `paramauto` | `__deepcopy__` | deep copy method | 8 | 1.0062 |
| `paramauto` | `__delattr__` | Delete an instance attribute if it exists and is not a class or excluded attribute. | 10 | 1.0062 |
| `paramauto` | `__getattr__` | get attribute override | 3 | 1.0062 |
| `paramauto` | `__getitem__` | s[i] returns the ith element of the structure s[:4] returns a structure with the four first fields s[[1,3]] returns the second and fourth elements | 41 | 1.0062 |
| `paramauto` | `__getstate__` | getstate for cooperative inheritance / duplication | 3 | 1.0062 |
| `paramauto` | `__iadd__` | iadd a structure set sortdefintions=True to sort definitions (to maintain executability) | 3 | 1.0062 |
| `paramauto` | `__init__` | constructor | 8 | 1.0062 |
| `paramauto` | `__isub__` | isub a structure | 9 | 1.0062 |
| `paramauto` | `__iter__` | struct iterator | 6 | 1.0062 |
| `paramauto` | `__len__` | return the number of fields | 4 | 1.0062 |
| `paramauto` | `__lshift__` | Allows the syntax: | 15 | 1.0062 |
| `paramauto` | `__next__` | increment iterator | 7 | 1.0062 |
| `paramauto` | `__repr__` | display method | 5 | 1.0062 |
| `paramauto` | `__setattr__` | set attribute override | 3 | 1.0062 |
| `paramauto` | `__setitem__` | set the ith element of the structure | 24 | 1.0062 |
| `paramauto` | `__setstate__` | setstate for cooperative inheritance / duplication | 3 | 1.0062 |
| `paramauto` | `__str__` | Return str(self). | 2 | 1.0062 |
| `paramauto` | `__sub__` | sub a structure | 10 | 1.0062 |
| `paramauto` | `check` | populate fields from a default structure check(defaultstruct) missing field, None and [] values are replaced by default ones | 19 | 1.0062 |
| `paramauto` | `clear` | clear() delete all fields while preserving the original class | 3 | 1.0062 |
| `paramauto` | `convert_matlab_like_arrays` | Converts Matlab-like array syntax (including hybrid notations) into a NumPy-esque list syntax in multiple passes. | 166 | 1.0062 |
| `paramauto` | `dict2struct` | create a structure from a dictionary | 8 | 1.0062 |
| `paramauto` | `disp` | display method | 3 | 1.0062 |
| `paramauto` | `dispmax` | optimize display | 8 | 1.0062 |
| `paramauto` | `escape` | escape \${} as ${{}} --> keep variable names convert ${} as {} --> prepare Python replacement | 35 | 1.0062 |
| `paramauto` | `eval` | Eval method for structure such as MS.alias | 210 | 1.0062 |
| `paramauto` | `expand_ranges` | Expands MATLAB-style ranges in a string. | 44 | 1.0062 |
| `paramauto` | `format` | Format a string with fields using {field} as placeholders. Handles expressions like ${variable1}. | 55 | 1.0062 |
| `paramauto` | `format_array` | Format NumPy array for display with distinctions for scalars, row/column vectors, and ND arrays. Recursively formats multi-dimensional arrays without introducing unwanted commas. | 106 | 1.0062 |
| `paramauto` | `format_legacy` | format a string with field (use {field} as placeholders) s.replace(string), s.replace(string,escape=True) where: s is a struct object string is a string with possibly ${variable1} escape is a flag to prevent ${} replaced by {} | 27 | 1.0062 |
| `paramauto` | `formateval` | format method with evaluation feature | 59 | 1.0062 |
| `paramauto` | `fromkeys` | returns a structure from keys | 3 | 1.0062 |
| `paramauto` | `fromkeysvalues` | struct.keysvalues(keys,values) creates a structure from keys and values use makeparam = True to create a param instead of struct | 18 | 1.0062 |
| `paramauto` | `generator` | Generate Python code of the equivalent structure. | 73 | 1.0062 |
| `paramauto` | `getattr` | Get attribute override to access both instance attributes and properties if allowed. | 11 | 1.0062 |
| `paramauto` | `getval` | returns the evaluated value | 4 | 1.0062 |
| `paramauto` | `hasattr` | Return true if the field exists, considering properties as regular attributes if allowed. | 7 | 1.0062 |
| `paramauto` | `importfrom` | Import values from 's' into self according to the following rules: | 30 | 1.0062 |
| `paramauto` | `isdefined` | isdefined(ref) returns true if it is defined in ref | 19 | 1.0062 |
| `paramauto` | `isstrdefined` | isstrdefined(string,ref) returns true if it is defined in ref | 14 | 1.0062 |
| `paramauto` | `isstrexpression` | isstrexpression(string) returns true if s contains an expression | 5 | 1.0062 |
| `paramauto` | `items` | return all elements as iterable key, value | 3 | 1.0062 |
| `paramauto` | `keys` | return the fields | 4 | 1.0062 |
| `paramauto` | `keyssorted` | sort keys by length() | 5 | 1.0062 |
| `paramauto` | `np2str` | Convert all NumPy entries of s into their string representations, handling both lists and dictionaries. | 58 | 1.0062 |
| `paramauto` | `numrepl` | Replace all placeholders of the form ${key} in the given text by the corresponding numeric value from the instance fields, under the following conditions: | 56 | 1.0062 |
| `paramauto` | `protect` | protect $variable as ${variable} | 11 | 1.0062 |
| `paramauto` | `read` | read the equivalent structure read(filename) | 35 | 1.0062 |
| `paramauto` | `safe_fstring` | Safely evaluate expressions in ${} using SafeEvaluator. | 61 | 1.0062 |
| `paramauto` | `scan` | scan(string) scan a string for variables | 11 | 1.0062 |
| `paramauto` | `set` | initialization | 3 | 1.0062 |
| `paramauto` | `setattr` | set field and value | 7 | 1.0062 |
| `paramauto` | `sortdefinitions` | sortdefintions sorts all definitions so that they can be executed as param(). If any inconsistency is found, an error message is generated. | 4 | 1.0062 |
| `paramauto` | `struct2dict` | create a dictionary from the current structure | 3 | 1.0062 |
| `paramauto` | `struct2param` | convert an object struct() to param() | 8 | 1.0062 |
| `paramauto` | `toparamauto` | convert a param instance into a paramauto instance toparamauto() | 6 | 1.0062 |
| `paramauto` | `tostatic` | convert dynamic a param() object to a static struct() object. note: no interpretation note: use tostruct() to interpret them and convert it to struct note: tostatic().struct2param() makes it reversible | 7 | 1.0062 |
| `paramauto` | `tostruct` | generate the evaluated structure tostruct(protection=False) | 6 | 1.0062 |
| `paramauto` | `update` | Update multiple fields at once, while protecting certain attributes. | 21 | 1.0062 |
| `paramauto` | `validkeys` | Validate and return the subset of keys from the provided list that are valid in the instance. | 38 | 1.0062 |
| `paramauto` | `values` | return the values | 4 | 1.0062 |
| `paramauto` | `write` | write the equivalent structure (not recursive for nested struct) write(filename, overwrite=True, mkdir=False) | 38 | 1.0062 |
| `paramauto` | `zip` | zip keys and values | 3 | 1.0062 |
| `pstr` | `__add__` | Return self+value. | 2 | 1.0062 |
| `pstr` | `__iadd__` |  | 2 | 1.0062 |
| `pstr` | `__repr__` | Return repr(self). | 5 | 1.0062 |
| `pstr` | `__truediv__` | overload / | 7 | 1.0062 |
| `pstr` | `eval` | evaluate the path of it os a path | 9 | 1.0062 |
| `pstr` | `topath` | return a validated path | 6 | 1.0062 |
| `struct` | `__add__` | Add two structure objects, with precedence as follows: | 49 | 1.0062 |
| `struct` | `__call__` | Extract a sub-structure based on the specified keys, keeping the same class type. | 35 | 1.0062 |
| `struct` | `__contains__` | in override | 3 | 1.0062 |
| `struct` | `__copy__` | copy method | 6 | 1.0062 |
| `struct` | `__deepcopy__` | deep copy method | 8 | 1.0062 |
| `struct` | `__delattr__` | Delete an instance attribute if it exists and is not a class or excluded attribute. | 10 | 1.0062 |
| `struct` | `__getattr__` | get attribute override | 3 | 1.0062 |
| `struct` | `__getitem__` | s[i] returns the ith element of the structure s[:4] returns a structure with the four first fields s[[1,3]] returns the second and fourth elements | 41 | 1.0062 |
| `struct` | `__getstate__` | getstate for cooperative inheritance / duplication | 3 | 1.0062 |
| `struct` | `__iadd__` | iadd a structure set sortdefintions=True to sort definitions (to maintain executability) | 11 | 1.0062 |
| `struct` | `__init__` | constructor, use debug=True to report eval errors | 6 | 1.0062 |
| `struct` | `__isub__` | isub a structure | 9 | 1.0062 |
| `struct` | `__iter__` | struct iterator | 6 | 1.0062 |
| `struct` | `__len__` | return the number of fields | 4 | 1.0062 |
| `struct` | `__lshift__` | Allows the syntax: | 15 | 1.0062 |
| `struct` | `__next__` | increment iterator | 7 | 1.0062 |
| `struct` | `__repr__` | display method | 68 | 1.0062 |
| `struct` | `__setattr__` | set attribute override | 3 | 1.0062 |
| `struct` | `__setitem__` | set the ith element of the structure | 24 | 1.0062 |
| `struct` | `__setstate__` | setstate for cooperative inheritance / duplication | 3 | 1.0062 |
| `struct` | `__str__` | Return str(self). | 2 | 1.0062 |
| `struct` | `__sub__` | sub a structure | 10 | 1.0062 |
| `struct` | `check` | populate fields from a default structure check(defaultstruct) missing field, None and [] values are replaced by default ones | 19 | 1.0062 |
| `struct` | `clear` | clear() delete all fields while preserving the original class | 3 | 1.0062 |
| `struct` | `dict2struct` | create a structure from a dictionary | 8 | 1.0062 |
| `struct` | `disp` | display method | 3 | 1.0062 |
| `struct` | `dispmax` | optimize display | 8 | 1.0062 |
| `struct` | `format` | Format a string with fields using {field} as placeholders. Handles expressions like ${variable1}. | 55 | 1.0062 |
| `struct` | `format_array` | Format NumPy array for display with distinctions for scalars, row/column vectors, and ND arrays. Recursively formats multi-dimensional arrays without introducing unwanted commas. | 106 | 1.0062 |
| `struct` | `format_legacy` | format a string with field (use {field} as placeholders) s.replace(string), s.replace(string,escape=True) where: s is a struct object string is a string with possibly ${variable1} escape is a flag to prevent ${} replaced by {} | 27 | 1.0062 |
| `struct` | `fromkeys` | returns a structure from keys | 3 | 1.0062 |
| `struct` | `fromkeysvalues` | struct.keysvalues(keys,values) creates a structure from keys and values use makeparam = True to create a param instead of struct | 18 | 1.0062 |
| `struct` | `generator` | Generate Python code of the equivalent structure. | 73 | 1.0062 |
| `struct` | `getattr` | Get attribute override to access both instance attributes and properties if allowed. | 11 | 1.0062 |
| `struct` | `hasattr` | Return true if the field exists, considering properties as regular attributes if allowed. | 7 | 1.0062 |
| `struct` | `importfrom` | Import values from 's' into self according to the following rules: | 30 | 1.0062 |
| `struct` | `isdefined` | isdefined(ref) returns true if it is defined in ref | 19 | 1.0062 |
| `struct` | `isstrdefined` | isstrdefined(string,ref) returns true if it is defined in ref | 14 | 1.0062 |
| `struct` | `isstrexpression` | isstrexpression(string) returns true if s contains an expression | 5 | 1.0062 |
| `struct` | `items` | return all elements as iterable key, value | 3 | 1.0062 |
| `struct` | `keys` | return the fields | 4 | 1.0062 |
| `struct` | `keyssorted` | sort keys by length() | 5 | 1.0062 |
| `struct` | `np2str` | Convert all NumPy entries of s into their string representations, handling both lists and dictionaries. | 58 | 1.0062 |
| `struct` | `numrepl` | Replace all placeholders of the form ${key} in the given text by the corresponding numeric value from the instance fields, under the following conditions: | 56 | 1.0062 |
| `struct` | `read` | read the equivalent structure read(filename) | 35 | 1.0062 |
| `struct` | `scan` | scan(string) scan a string for variables | 11 | 1.0062 |
| `struct` | `set` | initialization | 3 | 1.0062 |
| `struct` | `setattr` | set field and value | 6 | 1.0062 |
| `struct` | `sortdefinitions` | sortdefintions sorts all definitions so that they can be executed as param(). If any inconsistency is found, an error message is generated. | 53 | 1.0062 |
| `struct` | `struct2dict` | create a dictionary from the current structure | 3 | 1.0062 |
| `struct` | `struct2param` | convert an object struct() to param() | 8 | 1.0062 |
| `struct` | `update` | Update multiple fields at once, while protecting certain attributes. | 21 | 1.0062 |
| `struct` | `validkeys` | Validate and return the subset of keys from the provided list that are valid in the instance. | 38 | 1.0062 |
| `struct` | `values` | return the values | 4 | 1.0062 |
| `struct` | `write` | write the equivalent structure (not recursive for nested struct) write(filename, overwrite=True, mkdir=False) | 38 | 1.0062 |
| `struct` | `zip` | zip keys and values | 3 | 1.0062 |

<a id="pizza_private_utils" name="pizza_private_utils"></a>
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; font-size: 0.8em;"><a href="#pizza_private_mstruct" title="Go to Previous Module: pizza.private.mstruct" style="text-decoration: none;">⬅️ Previous</a>
<a href="#table_of_contents" title="Back to Table of Contents" style="text-decoration: none;">⬆️ TOC</a>
<a href="#pizza_raster" title="Go to Next Module: pizza.raster" style="text-decoration: none;">➡️ Next</a>
</div>

## Module `pizza.private.utils`

*No classes found in this module.*

**[Class Examples for `pizza/private/utils.py` (1)](class_examples.html#pizza_private_utils)**

### Methods Table

| Class | Method | Docstring First Paragraph | # Lines | __version__ |
|-------|---------|---------------------------|---------|-------------|
| (module-level) | `list` | list folders and files | 7 |  |
| (module-level) | `replaceall` | replaceall("some_dir", "find this", "replace with this", "*.txt") | 34 |  |
| (module-level) | `updatepptx` | update PPTX | 22 |  |

<a id="pizza_raster" name="pizza_raster"></a>
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; font-size: 0.8em;"><a href="#pizza_private_utils" title="Go to Previous Module: pizza.private.utils" style="text-decoration: none;">⬅️ Previous</a>
<a href="#table_of_contents" title="Back to Table of Contents" style="text-decoration: none;">⬆️ TOC</a>
<a href="#pizza_region" title="Go to Next Module: pizza.region" style="text-decoration: none;">➡️ Next</a>
</div>

## Module `pizza.raster`

### Class Inheritance Diagram
```mermaid
graph TD;
Circle
Collection
Diamond
Hexagon
Pentagon
Rectangle
Triangle
collection
coregeometry
coreshell
data
emulsion
genericpolygon
overlay
raster
scatter
struct
Circle --> Diamond
Circle --> Hexagon
Circle --> Pentagon
Circle --> Triangle
coregeometry --> genericpolygon
coregeometry --> overlay
emulsion --> coreshell
genericpolygon --> Circle
genericpolygon --> Rectangle
object --> Collection
object --> coregeometry
object --> data
object --> raster
object --> scatter
object --> struct
scatter --> emulsion
struct --> collection
```

**[Class Examples for `pizza/raster.py` (7)](class_examples.html#pizza_raster)**

### Methods Table

| Class | Method | Docstring First Paragraph | # Lines | __version__ |
|-------|---------|---------------------------|---------|-------------|
| (module-level) | `_extents` |  | 3 | 0.99991 |
| (module-level) | `_rotate` |  | 5 | 0.99991 |
| (module-level) | `arc` | Point distributed along an arc X,Y = arc(xmin=value,ymin=value,xmax=value,ymax=value,n=int, USER=struct(radius=value,direction=1)) Use direction to choose the upward +1 or downward -1 circle see: https://rosettacode.org/wiki/Circles_of_given_radius_through_two_points | 19 | 0.99991 |
| (module-level) | `imagesc` | imagesc à la Matlab imagesc(np2array) | 7 | 0.99991 |
| (module-level) | `ind2rgb` | Convert indexed image (NumPy array) to RGB rgb = ind2rgb(np2array,ncolors=nc) use rgb.save("/path/filename.png") for saving | 12 | 0.99991 |
| (module-level) | `linear` | Equispaced points along a trajectory X,Y = linear(xmin=value,ymin=value,xmax=value,ymax=value,n=int) | 5 | 0.99991 |
| `Circle` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 15 | 0.99991 |
| `Circle` | `__repr__` | display circle | 11 | 0.99991 |
| `Circle` | `copy` | returns a copy of the graphical object | 14 | 0.99991 |
| `Circle` | `corners` | returns xmin, ymin, xmax, ymax | 6 | 0.99991 |
| `Collection` | `__getattr__` | get attribute override | 3 | 0.99991 |
| `Collection` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 14 | 0.99991 |
| `Collection` | `__repr__` | Return repr(self). | 19 | 0.99991 |
| `Collection` | `get` | returns the object | 6 | 0.99991 |
| `Diamond` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 4 | 0.99991 |
| `Diamond` | `__repr__` | display circle | 11 | 0.99991 |
| `Diamond` | `copy` | returns a copy of the graphical object | 14 | 0.99991 |
| `Diamond` | `corners` | returns xmin, ymin, xmax, ymax | 6 | 0.99991 |
| `Hexagon` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 4 | 0.99991 |
| `Hexagon` | `__repr__` | display circle | 11 | 0.99991 |
| `Hexagon` | `copy` | returns a copy of the graphical object | 14 | 0.99991 |
| `Hexagon` | `corners` | returns xmin, ymin, xmax, ymax | 6 | 0.99991 |
| `Pentagon` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 4 | 0.99991 |
| `Pentagon` | `__repr__` | display circle | 11 | 0.99991 |
| `Pentagon` | `copy` | returns a copy of the graphical object | 14 | 0.99991 |
| `Pentagon` | `corners` | returns xmin, ymin, xmax, ymax | 6 | 0.99991 |
| `Rectangle` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 15 | 0.99991 |
| `Rectangle` | `__repr__` | display for rectangle class | 9 | 0.99991 |
| `Rectangle` | `copy` | returns a copy of the graphical object | 14 | 0.99991 |
| `Rectangle` | `corners` | returns xmin, ymin, xmax, ymax | 6 | 0.99991 |
| `Triangle` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 4 | 0.99991 |
| `Triangle` | `__repr__` | display circle | 11 | 0.99991 |
| `Triangle` | `copy` | returns a copy of the graphical object | 14 | 0.99991 |
| `Triangle` | `corners` | returns xmin, ymin, xmax, ymax | 6 | 0.99991 |
| `collection` | `__init__` | constructor, use debug=True to report eval errors | 11 | 0.99991 |
| `coregeometry` | `copy` | returns a copy of the graphical object | 14 | 0.99991 |
| `coreshell` | `__init__` | Parameters ---------- The insertions are performed between xmin,ymin and xmax,ymax xmin : int64 or real, optional x left corner. The default is 10. ymin : int64 or real, optional y bottom corner. The default is 10. xmax : int64 or real, optional x right corner. The default is 90. ymax : int64 or real, optional y top corner. The default is 90. beadtype : default beadtype to apply if not precised at insertion maxtrials : integer, optional Maximum of attempts for an object. The default is 1000. forcedinsertion : logical, optional Set it to true to force the next insertion. The default is True. | 35 | 0.99991 |
| `coreshell` | `__repr__` | Return repr(self). | 6 | 0.99991 |
| `coreshell` | `accepted` | acceptation criterion | 3 | 0.99991 |
| `coreshell` | `dist` | shortest distance of the center (x,y) to the wall or any object | 3 | 0.99991 |
| `coreshell` | `insertion` | insert a list of objects nsuccess=insertion(...) | 44 | 0.99991 |
| `coreshell` | `insertone` | insert one object of radius r properties: x,y coordinates (if missing, picked randomly from uniform distribution) r radius (default = 2% of diagonal) beadtype (default = defautbeadtype) overlap = False (accept only if no overlap) | 27 | 0.99991 |
| `coreshell` | `pairdist` | pair distance to the surface of all disks/spheres | 6 | 0.99991 |
| `coreshell` | `rand` | random position x,y | 4 | 0.99991 |
| `coreshell` | `setbeadtype` | set the default or the supplied beadtype | 8 | 0.99991 |
| `coreshell` | `walldist` | shortest distance to the wall | 3 | 0.99991 |
| `emulsion` | `__init__` | Parameters ---------- The insertions are performed between xmin,ymin and xmax,ymax xmin : int64 or real, optional x left corner. The default is 10. ymin : int64 or real, optional y bottom corner. The default is 10. xmax : int64 or real, optional x right corner. The default is 90. ymax : int64 or real, optional y top corner. The default is 90. beadtype : default beadtype to apply if not precised at insertion maxtrials : integer, optional Maximum of attempts for an object. The default is 1000. forcedinsertion : logical, optional Set it to true to force the next insertion. The default is True. | 35 | 0.99991 |
| `emulsion` | `__repr__` | Return repr(self). | 6 | 0.99991 |
| `emulsion` | `accepted` | acceptation criterion | 3 | 0.99991 |
| `emulsion` | `dist` | shortest distance of the center (x,y) to the wall or any object | 3 | 0.99991 |
| `emulsion` | `insertion` | insert a list of objects nsuccess=insertion(rlist,beadtype=None) beadtype=b forces the value b if None, defaultbeadtype is used instead | 21 | 0.99991 |
| `emulsion` | `insertone` | insert one object of radius r properties: x,y coordinates (if missing, picked randomly from uniform distribution) r radius (default = 2% of diagonal) beadtype (default = defautbeadtype) overlap = False (accept only if no overlap) | 27 | 0.99991 |
| `emulsion` | `pairdist` | pair distance to the surface of all disks/spheres | 6 | 0.99991 |
| `emulsion` | `rand` | random position x,y | 4 | 0.99991 |
| `emulsion` | `setbeadtype` | set the default or the supplied beadtype | 8 | 0.99991 |
| `emulsion` | `walldist` | shortest distance to the wall | 3 | 0.99991 |
| `genericpolygon` | `copy` | returns a copy of the graphical object | 14 | 0.99991 |
| `genericpolygon` | `corners` | returns xmin, ymin, xmax, ymax | 6 | 0.99991 |
| `overlay` | `__init__` | generate an overlay from file overlay(counter=(c1,c2),filename="this/is/myimage.jpg",xmin=x0,ymin=y0,colors=4) additional options overlay(...,flipud=True,angle=0,scale=(1,1)) | 48 | 0.99991 |
| `overlay` | `__repr__` | display for rectangle class | 13 | 0.99991 |
| `overlay` | `copy` | returns a copy of the graphical object | 14 | 0.99991 |
| `overlay` | `load` | load image and process it returns the image, the indexed image and its color map (à la Matlab, such as imread) | 23 | 0.99991 |
| `overlay` | `select` | select the color index: select(color = c) peeks pixels = c select(color = c, colormax = cmax) peeks pixels>=c and pixels<=cmax | 18 | 0.99991 |
| `raster` | `__getattr__` | get attribute override | 3 | 0.99991 |
| `raster` | `__init__` | initialize raster | 59 | 0.99991 |
| `raster` | `__len__` | len method | 3 | 0.99991 |
| `raster` | `__repr__` | display method | 27 | 0.99991 |
| `raster` | `circle` | circle object (or any regular polygon) circle(xcenter,ycenter,radius [, beadtype=1,shaperatio=1, angle=0, ismask=False], resolution=20, shiftangle=0) use circle(...,beadtype2=(type,ratio)) to salt an object with beads from another type and with a given ratio | 73 | 0.99991 |
| `raster` | `clear` | clear the plotting area, use clear("all")) to remove all objects | 16 | 0.99991 |
| `raster` | `collection` | collection of objects: collection(draftraster,name="mycollect" [,beadtype=1,ismask=True] collection(name="mycollect",newobjname1 = obj1, newobjname2 = obj2...) | 45 | 0.99991 |
| `raster` | `copyalongpath` | The method enable to copy an existing object (from the current raster, from another raster or a fake object) amp,g | 56 | 0.99991 |
| `raster` | `count` | count objects by type | 13 | 0.99991 |
| `raster` | `data` | return a pizza.data object data() data(scale=(scalex,scaley), center=(centerx,centery), maxtype=number, hexpacking=(0.5,0)) | 58 | 0.99991 |
| `raster` | `delete` | delete object | 12 | 0.99991 |
| `raster` | `diamond` | diamond object diamond(xcenter,ycenter,radius [, beadtype=1,shaperatio=1, angle=0, ismask=False] use diamond(...,beadtype2=(type,ratio)) to salt an object with beads from another type and with a given ratio | 9 | 0.99991 |
| `raster` | `exist` | exist object | 3 | 0.99991 |
| `raster` | `figure` | set the current figure | 5 | 0.99991 |
| `raster` | `frameobj` | frame coordinates by taking into account translation | 9 | 0.99991 |
| `raster` | `get` | returns the object | 6 | 0.99991 |
| `raster` | `hexagon` | hexagon object hexagon(xcenter,ycenter,radius [, beadtype=1,shaperatio=1, angle=0, ismask=False] use hexagon(...,beadtype2=(type,ratio)) to salt an object with beads from another type and with a given ratio | 9 | 0.99991 |
| `raster` | `label` | label: label(name [, contour=True,edgecolor="orange",facecolor="none",linewidth=2, ax=plt.gca()]) | 17 | 0.99991 |
| `raster` | `labelobj` | labelobj: labelobj(obj [, contour=True,edgecolor="orange",facecolor="none",linewidth=2, ax=plt.gca()]) | 23 | 0.99991 |
| `raster` | `length` | returns the total number of beads length(type,"beadtype") | 12 | 0.99991 |
| `raster` | `list` | list objects | 11 | 0.99991 |
| `raster` | `names` | return the names of objects sorted as index | 7 | 0.99991 |
| `raster` | `newfigure` | create a new figure (dpi=200) | 3 | 0.99991 |
| `raster` | `numeric` | retrieve the image as a numpy.array | 3 | 0.99991 |
| `raster` | `overlay` | overlay object: made from an image converted to nc colors the object is made from the level ranged between ic and jc (bounds included) note: if palette found, no conversion is applied | 66 | 0.99991 |
| `raster` | `pentagon` | pentagon object pentagon(xcenter,ycenter,radius [, beadtype=1,shaperatio=1, angle=0, ismask=False] use pentagon(...,beadtype2=(type,ratio)) to salt an object with beads from another type and with a given ratio | 9 | 0.99991 |
| `raster` | `plot` | plot | 13 | 0.99991 |
| `raster` | `plotobj` | plotobj(obj) | 64 | 0.99991 |
| `raster` | `print` | print method | 5 | 0.99991 |
| `raster` | `rectangle` | rectangle object rectangle(xleft,xright,ybottom,ytop [, beadtype=1,mode="lower", angle=0, ismask=False]) rectangle(xcenter,ycenter,width,height [, beadtype=1,mode="center", angle=0, ismask=False]) | 73 | 0.99991 |
| `raster` | `scatter` | Parameters ---------- E : scatter or emulsion object codes for x,y and r. name : string, optional name of the collection. The default is "emulsion". beadtype : integer, optional for all objects. The default is 1. ismask : logical, optional Set it to true to force a mask. The default is False. | 40 | 0.99991 |
| `raster` | `show` | show method: show(extra="label",contour=True,what="beadtype") | 17 | 0.99991 |
| `raster` | `string` | convert the image as ASCII strings | 12 | 0.99991 |
| `raster` | `torgb` | converts bead raster to image rgb = raster.torgb(what="beadtype") thumbnail = raster.torgb(what="beadtype",(128,128)) use: rgb.save("/path/filename.png") for saving | 16 | 0.99991 |
| `raster` | `triangle` | triangle object triangle(xcenter,ycenter,radius [, beadtype=1,shaperatio=1, angle=0, ismask=False] use triangle(...,beadtype2=(type,ratio)) to salt an object with beads from another type and with a given ratio | 9 | 0.99991 |
| `raster` | `unlabel` | unlabel | 10 | 0.99991 |
| `raster` | `valid` | validation of coordinates | 3 | 0.99991 |
| `scatter` | `__init__` | The scatter class provides an easy constructor to distribute in space objects according to their positions x,y, size r (radius) and beadtype. | 17 | 0.99991 |
| `scatter` | `pairdist` | pair distance to the surface of all disks/spheres | 6 | 0.99991 |

<a id="pizza_region" name="pizza_region"></a>
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; font-size: 0.8em;"><a href="#pizza_raster" title="Go to Previous Module: pizza.raster" style="text-decoration: none;">⬅️ Previous</a>
<a href="#table_of_contents" title="Back to Table of Contents" style="text-decoration: none;">⬆️ TOC</a>
<a href="#pizza_script" title="Go to Next Module: pizza.script" style="text-decoration: none;">➡️ Next</a>
</div>

## Module `pizza.region`

### Class Inheritance Diagram
```mermaid
graph TD;
AttrErrorDict
Block
Collection
Cone
Cylinder
Ellipsoid
Evalgeometry
Intersect
LammpsCollectionGroup
LammpsCreate
LammpsFooter
LammpsFooterPreview
LammpsGeneric
LammpsGroup
LammpsHeader
LammpsHeaderBox
LammpsHeaderInit
LammpsHeaderLattice
LammpsHeaderMass
LammpsMove
LammpsRegion
LammpsSetGroup
LammpsSpacefilling
LammpsVariables
Plane
Prism
SafeEvaluator
Sphere
Union
coregeometry
emulsion
forcefield
headersRegiondata
none
param
paramauto
parameterforcefield
pipescript
pstr
region
regioncollection
regiondata
rigidwall
saltTLSPH
scatter
script
scriptdata
scriptobject
smd
solidfood
struct
tlsph
tlsphalone
ulsph
ulsphalone
water
LammpsGeneric --> LammpsCollectionGroup
LammpsGeneric --> LammpsCreate
LammpsGeneric --> LammpsFooter
LammpsGeneric --> LammpsFooterPreview
LammpsGeneric --> LammpsGroup
LammpsGeneric --> LammpsHeader
LammpsGeneric --> LammpsHeaderBox
LammpsGeneric --> LammpsHeaderInit
LammpsGeneric --> LammpsHeaderLattice
LammpsGeneric --> LammpsHeaderMass
LammpsGeneric --> LammpsMove
LammpsGeneric --> LammpsRegion
LammpsGeneric --> LammpsSetGroup
LammpsGeneric --> LammpsSpacefilling
LammpsGeneric --> LammpsVariables
NodeVisitor --> SafeEvaluator
coregeometry --> Block
coregeometry --> Cone
coregeometry --> Cylinder
coregeometry --> Ellipsoid
coregeometry --> Evalgeometry
coregeometry --> Intersect
coregeometry --> Plane
coregeometry --> Prism
coregeometry --> Sphere
coregeometry --> Union
dict --> AttrErrorDict
forcefield --> smd
forcefield --> tlsphalone
none --> rigidwall
object --> Collection
object --> coregeometry
object --> forcefield
object --> pipescript
object --> region
object --> scatter
object --> script
object --> struct
param --> paramauto
param --> scriptdata
paramauto --> parameterforcefield
paramauto --> regiondata
regiondata --> headersRegiondata
scatter --> emulsion
script --> LammpsGeneric
smd --> none
smd --> tlsph
smd --> ulsph
smd --> ulsphalone
str --> pstr
struct --> param
struct --> regioncollection
struct --> scriptobject
tlsph --> saltTLSPH
tlsph --> solidfood
ulsph --> water
```

**[Class Examples for `pizza/region.py` (29)](class_examples.html#pizza_region)**

### Methods Table

| Class | Method | Docstring First Paragraph | # Lines | __version__ |
|-------|---------|---------------------------|---------|-------------|
| (module-level) | `<lambda>` |  | 1 | 1.0 |
| (module-level) | `<lambda>` |  | 7 | 1.0 |
| `Block` | `__add__` | overload addition ("+") operator | 19 | 1.0 |
| `Block` | `__copy__` | copy method | 6 | 1.0 |
| `Block` | `__deepcopy__` | deep copy method | 8 | 1.0 |
| `Block` | `__getstate__` | getstate for cooperative inheritance / duplication | 3 | 1.0 |
| `Block` | `__iadd__` | overload iaddition ("+=") operator | 16 | 1.0 |
| `Block` | `__init__` | constructor of the generic core geometry USER: any definitions requires by the geometry VARIABLES: variables used to define the geometry (to be used in LAMMPS) hasgroup, hasmove: flag to force the sections group and move SECTIONS: they must be PIZZA.script | 24 | 1.0 |
| `Block` | `__or__` | overload | pipe | 19 | 1.0 |
| `Block` | `__repr__` | display method | 24 | 1.0 |
| `Block` | `__setstate__` | setstate for cooperative inheritance / duplication | 3 | 1.0 |
| `Block` | `copy` | returns a copy of the graphical object | 11 | 1.0 |
| `Block` | `creategroup` | force the group creation in script | 3 | 1.0 |
| `Block` | `createmove` | force the fix move creation in script | 3 | 1.0 |
| `Block` | `do` | generates a script | 6 | 1.0 |
| `Block` | `fixmoveargs` | Validates all arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) the result is adictionary, all fixmove can be combined | 18 | 1.0 |
| `Block` | `fixmoveargvalidator` | Validation of arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) | 39 | 1.0 |
| `Block` | `get_fixmovesyntax` | Returns the syntax for LAMMPS command, or detailed explanation for a specific argument type | 39 | 1.0 |
| `Block` | `movearg` | Validation of move arguments for region command (https://docs.lammps.org/region.html) move args = v_x v_y v_z v_x,v_y,v_z = equal-style variables for x,y,z displacement of region over time (distance units) | 39 | 1.0 |
| `Block` | `openarg` | Validation of open arguments for region command (https://docs.lammps.org/region.html) open value = integer from 1-6 corresponding to face index (see below) The indices specified as part of the open keyword have the following meanings: | 32 | 1.0 |
| `Block` | `removegroup` | force the group creation in script | 3 | 1.0 |
| `Block` | `removemove` | force the fix move creation in script | 3 | 1.0 |
| `Block` | `rotatearg` | Validation of rotate arguments for region command (https://docs.lammps.org/region.html) rotate args = v_theta Px Py Pz Rx Ry Rz v_theta = equal-style variable for rotaton of region over time (in radians) Px,Py,Pz = origin for axis of rotation (distance units) Rx,Ry,Rz = axis of rotation vector | 36 | 1.0 |
| `Block` | `scriptobject` | Method to return a scriptobject based on region instead of an input file Syntax similar to script.scriptobject OBJ = scriptobject(...) Implemented properties: beadtype=1,2,... name="short name" fullname = "comprehensive name" style = "smd" forcefield = any valid forcefield instance (default = rigidwall()) | 34 | 1.0 |
| `Block` | `setgroup` | force the group creation in script | 3 | 1.0 |
| `Block` | `sidearg` | Validation of side arguments for region command (https://docs.lammps.org/region.html) side value = in or out in = the region is inside the specified geometry out = the region is outside the specified geometry | 20 | 1.0 |
| `Block` | `unitsarg` | Validation for units arguments for region command (https://docs.lammps.org/region.html) units value = lattice or box lattice = the geometry is defined in lattice units box = the geometry is defined in simulation box units | 20 | 1.0 |
| `Block` | `update` | update the USER content for all three scripts | 14 | 1.0 |
| `Block` | `volume` | Calculate the volume of the block based on USER.args | 24 | 1.0 |
| `Collection` | `__getattr__` | get attribute override | 3 | 1.0 |
| `Collection` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 26 | 1.0 |
| `Collection` | `__len__` | return length of collection | 3 | 1.0 |
| `Collection` | `__repr__` | Return repr(self). | 14 | 1.0 |
| `Collection` | `creategroup` | force the group creation in script | 5 | 1.0 |
| `Collection` | `get` | returns the object | 8 | 1.0 |
| `Collection` | `group` | return the grouped coregeometry object | 13 | 1.0 |
| `Collection` | `list` | return the list of objects | 3 | 1.0 |
| `Collection` | `removegroup` | force the group creation in script | 5 | 1.0 |
| `Collection` | `update` | update the USER content for the script | 6 | 1.0 |
| `Cone` | `__add__` | overload addition ("+") operator | 19 | 1.0 |
| `Cone` | `__copy__` | copy method | 6 | 1.0 |
| `Cone` | `__deepcopy__` | deep copy method | 8 | 1.0 |
| `Cone` | `__getstate__` | getstate for cooperative inheritance / duplication | 3 | 1.0 |
| `Cone` | `__iadd__` | overload iaddition ("+=") operator | 16 | 1.0 |
| `Cone` | `__init__` | constructor of the generic core geometry USER: any definitions requires by the geometry VARIABLES: variables used to define the geometry (to be used in LAMMPS) hasgroup, hasmove: flag to force the sections group and move SECTIONS: they must be PIZZA.script | 23 | 1.0 |
| `Cone` | `__or__` | overload | pipe | 19 | 1.0 |
| `Cone` | `__repr__` | display method | 24 | 1.0 |
| `Cone` | `__setstate__` | setstate for cooperative inheritance / duplication | 3 | 1.0 |
| `Cone` | `copy` | returns a copy of the graphical object | 11 | 1.0 |
| `Cone` | `creategroup` | force the group creation in script | 3 | 1.0 |
| `Cone` | `createmove` | force the fix move creation in script | 3 | 1.0 |
| `Cone` | `do` | generates a script | 6 | 1.0 |
| `Cone` | `fixmoveargs` | Validates all arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) the result is adictionary, all fixmove can be combined | 18 | 1.0 |
| `Cone` | `fixmoveargvalidator` | Validation of arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) | 39 | 1.0 |
| `Cone` | `get_fixmovesyntax` | Returns the syntax for LAMMPS command, or detailed explanation for a specific argument type | 39 | 1.0 |
| `Cone` | `movearg` | Validation of move arguments for region command (https://docs.lammps.org/region.html) move args = v_x v_y v_z v_x,v_y,v_z = equal-style variables for x,y,z displacement of region over time (distance units) | 39 | 1.0 |
| `Cone` | `openarg` | Validation of open arguments for region command (https://docs.lammps.org/region.html) open value = integer from 1-6 corresponding to face index (see below) The indices specified as part of the open keyword have the following meanings: | 32 | 1.0 |
| `Cone` | `removegroup` | force the group creation in script | 3 | 1.0 |
| `Cone` | `removemove` | force the fix move creation in script | 3 | 1.0 |
| `Cone` | `rotatearg` | Validation of rotate arguments for region command (https://docs.lammps.org/region.html) rotate args = v_theta Px Py Pz Rx Ry Rz v_theta = equal-style variable for rotaton of region over time (in radians) Px,Py,Pz = origin for axis of rotation (distance units) Rx,Ry,Rz = axis of rotation vector | 36 | 1.0 |
| `Cone` | `scriptobject` | Method to return a scriptobject based on region instead of an input file Syntax similar to script.scriptobject OBJ = scriptobject(...) Implemented properties: beadtype=1,2,... name="short name" fullname = "comprehensive name" style = "smd" forcefield = any valid forcefield instance (default = rigidwall()) | 34 | 1.0 |
| `Cone` | `setgroup` | force the group creation in script | 3 | 1.0 |
| `Cone` | `sidearg` | Validation of side arguments for region command (https://docs.lammps.org/region.html) side value = in or out in = the region is inside the specified geometry out = the region is outside the specified geometry | 20 | 1.0 |
| `Cone` | `unitsarg` | Validation for units arguments for region command (https://docs.lammps.org/region.html) units value = lattice or box lattice = the geometry is defined in lattice units box = the geometry is defined in simulation box units | 20 | 1.0 |
| `Cone` | `update` | update the USER content for all three scripts | 14 | 1.0 |
| `Cone` | `volume` | Calculate the volume of the cone based on USER.args | 21 | 1.0 |
| `Cylinder` | `__add__` | overload addition ("+") operator | 19 | 1.0 |
| `Cylinder` | `__copy__` | copy method | 6 | 1.0 |
| `Cylinder` | `__deepcopy__` | deep copy method | 8 | 1.0 |
| `Cylinder` | `__getstate__` | getstate for cooperative inheritance / duplication | 3 | 1.0 |
| `Cylinder` | `__iadd__` | overload iaddition ("+=") operator | 16 | 1.0 |
| `Cylinder` | `__init__` | constructor of the generic core geometry USER: any definitions requires by the geometry VARIABLES: variables used to define the geometry (to be used in LAMMPS) hasgroup, hasmove: flag to force the sections group and move SECTIONS: they must be PIZZA.script | 23 | 1.0 |
| `Cylinder` | `__or__` | overload | pipe | 19 | 1.0 |
| `Cylinder` | `__repr__` | display method | 24 | 1.0 |
| `Cylinder` | `__setstate__` | setstate for cooperative inheritance / duplication | 3 | 1.0 |
| `Cylinder` | `copy` | returns a copy of the graphical object | 11 | 1.0 |
| `Cylinder` | `creategroup` | force the group creation in script | 3 | 1.0 |
| `Cylinder` | `createmove` | force the fix move creation in script | 3 | 1.0 |
| `Cylinder` | `do` | generates a script | 6 | 1.0 |
| `Cylinder` | `fixmoveargs` | Validates all arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) the result is adictionary, all fixmove can be combined | 18 | 1.0 |
| `Cylinder` | `fixmoveargvalidator` | Validation of arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) | 39 | 1.0 |
| `Cylinder` | `get_fixmovesyntax` | Returns the syntax for LAMMPS command, or detailed explanation for a specific argument type | 39 | 1.0 |
| `Cylinder` | `movearg` | Validation of move arguments for region command (https://docs.lammps.org/region.html) move args = v_x v_y v_z v_x,v_y,v_z = equal-style variables for x,y,z displacement of region over time (distance units) | 39 | 1.0 |
| `Cylinder` | `openarg` | Validation of open arguments for region command (https://docs.lammps.org/region.html) open value = integer from 1-6 corresponding to face index (see below) The indices specified as part of the open keyword have the following meanings: | 32 | 1.0 |
| `Cylinder` | `removegroup` | force the group creation in script | 3 | 1.0 |
| `Cylinder` | `removemove` | force the fix move creation in script | 3 | 1.0 |
| `Cylinder` | `rotatearg` | Validation of rotate arguments for region command (https://docs.lammps.org/region.html) rotate args = v_theta Px Py Pz Rx Ry Rz v_theta = equal-style variable for rotaton of region over time (in radians) Px,Py,Pz = origin for axis of rotation (distance units) Rx,Ry,Rz = axis of rotation vector | 36 | 1.0 |
| `Cylinder` | `scriptobject` | Method to return a scriptobject based on region instead of an input file Syntax similar to script.scriptobject OBJ = scriptobject(...) Implemented properties: beadtype=1,2,... name="short name" fullname = "comprehensive name" style = "smd" forcefield = any valid forcefield instance (default = rigidwall()) | 34 | 1.0 |
| `Cylinder` | `setgroup` | force the group creation in script | 3 | 1.0 |
| `Cylinder` | `sidearg` | Validation of side arguments for region command (https://docs.lammps.org/region.html) side value = in or out in = the region is inside the specified geometry out = the region is outside the specified geometry | 20 | 1.0 |
| `Cylinder` | `unitsarg` | Validation for units arguments for region command (https://docs.lammps.org/region.html) units value = lattice or box lattice = the geometry is defined in lattice units box = the geometry is defined in simulation box units | 20 | 1.0 |
| `Cylinder` | `update` | update the USER content for all three scripts | 14 | 1.0 |
| `Cylinder` | `volume` | Calculate the volume of the cylinder based on USER.args | 17 | 1.0 |
| `Ellipsoid` | `__add__` | overload addition ("+") operator | 19 | 1.0 |
| `Ellipsoid` | `__copy__` | copy method | 6 | 1.0 |
| `Ellipsoid` | `__deepcopy__` | deep copy method | 8 | 1.0 |
| `Ellipsoid` | `__getstate__` | getstate for cooperative inheritance / duplication | 3 | 1.0 |
| `Ellipsoid` | `__iadd__` | overload iaddition ("+=") operator | 16 | 1.0 |
| `Ellipsoid` | `__init__` | constructor of the generic core geometry USER: any definitions requires by the geometry VARIABLES: variables used to define the geometry (to be used in LAMMPS) hasgroup, hasmove: flag to force the sections group and move SECTIONS: they must be PIZZA.script | 23 | 1.0 |
| `Ellipsoid` | `__or__` | overload | pipe | 19 | 1.0 |
| `Ellipsoid` | `__repr__` | display method | 24 | 1.0 |
| `Ellipsoid` | `__setstate__` | setstate for cooperative inheritance / duplication | 3 | 1.0 |
| `Ellipsoid` | `copy` | returns a copy of the graphical object | 11 | 1.0 |
| `Ellipsoid` | `creategroup` | force the group creation in script | 3 | 1.0 |
| `Ellipsoid` | `createmove` | force the fix move creation in script | 3 | 1.0 |
| `Ellipsoid` | `do` | generates a script | 6 | 1.0 |
| `Ellipsoid` | `fixmoveargs` | Validates all arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) the result is adictionary, all fixmove can be combined | 18 | 1.0 |
| `Ellipsoid` | `fixmoveargvalidator` | Validation of arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) | 39 | 1.0 |
| `Ellipsoid` | `get_fixmovesyntax` | Returns the syntax for LAMMPS command, or detailed explanation for a specific argument type | 39 | 1.0 |
| `Ellipsoid` | `movearg` | Validation of move arguments for region command (https://docs.lammps.org/region.html) move args = v_x v_y v_z v_x,v_y,v_z = equal-style variables for x,y,z displacement of region over time (distance units) | 39 | 1.0 |
| `Ellipsoid` | `openarg` | Validation of open arguments for region command (https://docs.lammps.org/region.html) open value = integer from 1-6 corresponding to face index (see below) The indices specified as part of the open keyword have the following meanings: | 32 | 1.0 |
| `Ellipsoid` | `removegroup` | force the group creation in script | 3 | 1.0 |
| `Ellipsoid` | `removemove` | force the fix move creation in script | 3 | 1.0 |
| `Ellipsoid` | `rotatearg` | Validation of rotate arguments for region command (https://docs.lammps.org/region.html) rotate args = v_theta Px Py Pz Rx Ry Rz v_theta = equal-style variable for rotaton of region over time (in radians) Px,Py,Pz = origin for axis of rotation (distance units) Rx,Ry,Rz = axis of rotation vector | 36 | 1.0 |
| `Ellipsoid` | `scriptobject` | Method to return a scriptobject based on region instead of an input file Syntax similar to script.scriptobject OBJ = scriptobject(...) Implemented properties: beadtype=1,2,... name="short name" fullname = "comprehensive name" style = "smd" forcefield = any valid forcefield instance (default = rigidwall()) | 34 | 1.0 |
| `Ellipsoid` | `setgroup` | force the group creation in script | 3 | 1.0 |
| `Ellipsoid` | `sidearg` | Validation of side arguments for region command (https://docs.lammps.org/region.html) side value = in or out in = the region is inside the specified geometry out = the region is outside the specified geometry | 20 | 1.0 |
| `Ellipsoid` | `unitsarg` | Validation for units arguments for region command (https://docs.lammps.org/region.html) units value = lattice or box lattice = the geometry is defined in lattice units box = the geometry is defined in simulation box units | 20 | 1.0 |
| `Ellipsoid` | `update` | update the USER content for all three scripts | 14 | 1.0 |
| `Ellipsoid` | `volume` | Calculate the volume of the ellipsoid based on USER.args | 15 | 1.0 |
| `Evalgeometry` | `__add__` | overload addition ("+") operator | 19 | 1.0 |
| `Evalgeometry` | `__copy__` | copy method | 6 | 1.0 |
| `Evalgeometry` | `__deepcopy__` | deep copy method | 8 | 1.0 |
| `Evalgeometry` | `__getstate__` | getstate for cooperative inheritance / duplication | 3 | 1.0 |
| `Evalgeometry` | `__iadd__` | overload iaddition ("+=") operator | 16 | 1.0 |
| `Evalgeometry` | `__init__` | constructor of the generic core geometry USER: any definitions requires by the geometry VARIABLES: variables used to define the geometry (to be used in LAMMPS) hasgroup, hasmove: flag to force the sections group and move SECTIONS: they must be PIZZA.script | 9 | 1.0 |
| `Evalgeometry` | `__or__` | overload | pipe | 19 | 1.0 |
| `Evalgeometry` | `__repr__` | display method | 24 | 1.0 |
| `Evalgeometry` | `__setstate__` | setstate for cooperative inheritance / duplication | 3 | 1.0 |
| `Evalgeometry` | `copy` | returns a copy of the graphical object | 11 | 1.0 |
| `Evalgeometry` | `creategroup` | force the group creation in script | 3 | 1.0 |
| `Evalgeometry` | `createmove` | force the fix move creation in script | 3 | 1.0 |
| `Evalgeometry` | `do` | generates a script | 6 | 1.0 |
| `Evalgeometry` | `fixmoveargs` | Validates all arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) the result is adictionary, all fixmove can be combined | 18 | 1.0 |
| `Evalgeometry` | `fixmoveargvalidator` | Validation of arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) | 39 | 1.0 |
| `Evalgeometry` | `get_fixmovesyntax` | Returns the syntax for LAMMPS command, or detailed explanation for a specific argument type | 39 | 1.0 |
| `Evalgeometry` | `movearg` | Validation of move arguments for region command (https://docs.lammps.org/region.html) move args = v_x v_y v_z v_x,v_y,v_z = equal-style variables for x,y,z displacement of region over time (distance units) | 39 | 1.0 |
| `Evalgeometry` | `openarg` | Validation of open arguments for region command (https://docs.lammps.org/region.html) open value = integer from 1-6 corresponding to face index (see below) The indices specified as part of the open keyword have the following meanings: | 32 | 1.0 |
| `Evalgeometry` | `removegroup` | force the group creation in script | 3 | 1.0 |
| `Evalgeometry` | `removemove` | force the fix move creation in script | 3 | 1.0 |
| `Evalgeometry` | `rotatearg` | Validation of rotate arguments for region command (https://docs.lammps.org/region.html) rotate args = v_theta Px Py Pz Rx Ry Rz v_theta = equal-style variable for rotaton of region over time (in radians) Px,Py,Pz = origin for axis of rotation (distance units) Rx,Ry,Rz = axis of rotation vector | 36 | 1.0 |
| `Evalgeometry` | `scriptobject` | Method to return a scriptobject based on region instead of an input file Syntax similar to script.scriptobject OBJ = scriptobject(...) Implemented properties: beadtype=1,2,... name="short name" fullname = "comprehensive name" style = "smd" forcefield = any valid forcefield instance (default = rigidwall()) | 34 | 1.0 |
| `Evalgeometry` | `setgroup` | force the group creation in script | 3 | 1.0 |
| `Evalgeometry` | `sidearg` | Validation of side arguments for region command (https://docs.lammps.org/region.html) side value = in or out in = the region is inside the specified geometry out = the region is outside the specified geometry | 20 | 1.0 |
| `Evalgeometry` | `unitsarg` | Validation for units arguments for region command (https://docs.lammps.org/region.html) units value = lattice or box lattice = the geometry is defined in lattice units box = the geometry is defined in simulation box units | 20 | 1.0 |
| `Evalgeometry` | `update` | update the USER content for all three scripts | 14 | 1.0 |
| `Intersect` | `__add__` | overload addition ("+") operator | 19 | 1.0 |
| `Intersect` | `__copy__` | copy method | 6 | 1.0 |
| `Intersect` | `__deepcopy__` | deep copy method | 8 | 1.0 |
| `Intersect` | `__getstate__` | getstate for cooperative inheritance / duplication | 3 | 1.0 |
| `Intersect` | `__iadd__` | overload iaddition ("+=") operator | 16 | 1.0 |
| `Intersect` | `__init__` | constructor of the generic core geometry USER: any definitions requires by the geometry VARIABLES: variables used to define the geometry (to be used in LAMMPS) hasgroup, hasmove: flag to force the sections group and move SECTIONS: they must be PIZZA.script | 14 | 1.0 |
| `Intersect` | `__or__` | overload | pipe | 19 | 1.0 |
| `Intersect` | `__repr__` | display method | 24 | 1.0 |
| `Intersect` | `__setstate__` | setstate for cooperative inheritance / duplication | 3 | 1.0 |
| `Intersect` | `copy` | returns a copy of the graphical object | 11 | 1.0 |
| `Intersect` | `creategroup` | force the group creation in script | 3 | 1.0 |
| `Intersect` | `createmove` | force the fix move creation in script | 3 | 1.0 |
| `Intersect` | `do` | generates a script | 6 | 1.0 |
| `Intersect` | `fixmoveargs` | Validates all arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) the result is adictionary, all fixmove can be combined | 18 | 1.0 |
| `Intersect` | `fixmoveargvalidator` | Validation of arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) | 39 | 1.0 |
| `Intersect` | `get_fixmovesyntax` | Returns the syntax for LAMMPS command, or detailed explanation for a specific argument type | 39 | 1.0 |
| `Intersect` | `movearg` | Validation of move arguments for region command (https://docs.lammps.org/region.html) move args = v_x v_y v_z v_x,v_y,v_z = equal-style variables for x,y,z displacement of region over time (distance units) | 39 | 1.0 |
| `Intersect` | `openarg` | Validation of open arguments for region command (https://docs.lammps.org/region.html) open value = integer from 1-6 corresponding to face index (see below) The indices specified as part of the open keyword have the following meanings: | 32 | 1.0 |
| `Intersect` | `removegroup` | force the group creation in script | 3 | 1.0 |
| `Intersect` | `removemove` | force the fix move creation in script | 3 | 1.0 |
| `Intersect` | `rotatearg` | Validation of rotate arguments for region command (https://docs.lammps.org/region.html) rotate args = v_theta Px Py Pz Rx Ry Rz v_theta = equal-style variable for rotaton of region over time (in radians) Px,Py,Pz = origin for axis of rotation (distance units) Rx,Ry,Rz = axis of rotation vector | 36 | 1.0 |
| `Intersect` | `scriptobject` | Method to return a scriptobject based on region instead of an input file Syntax similar to script.scriptobject OBJ = scriptobject(...) Implemented properties: beadtype=1,2,... name="short name" fullname = "comprehensive name" style = "smd" forcefield = any valid forcefield instance (default = rigidwall()) | 34 | 1.0 |
| `Intersect` | `setgroup` | force the group creation in script | 3 | 1.0 |
| `Intersect` | `sidearg` | Validation of side arguments for region command (https://docs.lammps.org/region.html) side value = in or out in = the region is inside the specified geometry out = the region is outside the specified geometry | 20 | 1.0 |
| `Intersect` | `unitsarg` | Validation for units arguments for region command (https://docs.lammps.org/region.html) units value = lattice or box lattice = the geometry is defined in lattice units box = the geometry is defined in simulation box units | 20 | 1.0 |
| `Intersect` | `update` | update the USER content for all three scripts | 14 | 1.0 |
| `LammpsCollectionGroup` | `do` | generate the LAMMPS code with VARIABLE definitions | 12 | 1.0 |
| `LammpsCreate` | `do` | generate the LAMMPS code with VARIABLE definitions | 12 | 1.0 |
| `LammpsFooter` | `do` | generate the LAMMPS code with VARIABLE definitions | 12 | 1.0 |
| `LammpsFooterPreview` | `do` | generate the LAMMPS code with VARIABLE definitions | 12 | 1.0 |
| `LammpsGeneric` | `do` | generate the LAMMPS code with VARIABLE definitions | 12 | 1.0 |
| `LammpsGroup` | `do` | generate the LAMMPS code with VARIABLE definitions | 12 | 1.0 |
| `LammpsHeader` | `do` | generate the LAMMPS code with VARIABLE definitions | 12 | 1.0 |
| `LammpsHeaderBox` | `do` | generate the LAMMPS code with VARIABLE definitions | 12 | 1.0 |
| `LammpsHeaderInit` | `__init__` | Constructor adding instance definitions stored in USER. | 4 | 1.0 |
| `LammpsHeaderInit` | `do` | generate the LAMMPS code with VARIABLE definitions | 12 | 1.0 |
| `LammpsHeaderInit` | `generate_template` | Generate the TEMPLATE based on USER definitions. | 15 | 1.0 |
| `LammpsHeaderLattice` | `__init__` | Constructor adding instance definitions stored in USER. | 4 | 1.0 |
| `LammpsHeaderLattice` | `do` | generate the LAMMPS code with VARIABLE definitions | 12 | 1.0 |
| `LammpsHeaderLattice` | `generate_template` | Generate the TEMPLATE based on USER definitions. | 8 | 1.0 |
| `LammpsHeaderMass` | `__init__` | Constructor adding instance definitions stored in USER. | 14 | 1.0 |
| `LammpsHeaderMass` | `do` | generate the LAMMPS code with VARIABLE definitions | 12 | 1.0 |
| `LammpsHeaderMass` | `generate_template` | Generate the TEMPLATE for mass assignments based on USER definitions. | 32 | 1.0 |
| `LammpsMove` | `do` | generate the LAMMPS code with VARIABLE definitions | 12 | 1.0 |
| `LammpsRegion` | `do` | generate the LAMMPS code with VARIABLE definitions | 12 | 1.0 |
| `LammpsSetGroup` | `do` | generate the LAMMPS code with VARIABLE definitions | 12 | 1.0 |
| `LammpsSpacefilling` | `do` | generate the LAMMPS code with VARIABLE definitions | 12 | 1.0 |
| `LammpsVariables` | `__init__` | constructor of LammpsVariables | 4 | 1.0 |
| `LammpsVariables` | `__rshift__` | overload right  shift operator (keep only the last template) | 12 | 1.0 |
| `LammpsVariables` | `do` | generate the LAMMPS code with VARIABLE definitions | 12 | 1.0 |
| `Plane` | `__add__` | overload addition ("+") operator | 19 | 1.0 |
| `Plane` | `__copy__` | copy method | 6 | 1.0 |
| `Plane` | `__deepcopy__` | deep copy method | 8 | 1.0 |
| `Plane` | `__getstate__` | getstate for cooperative inheritance / duplication | 3 | 1.0 |
| `Plane` | `__iadd__` | overload iaddition ("+=") operator | 16 | 1.0 |
| `Plane` | `__init__` | constructor of the generic core geometry USER: any definitions requires by the geometry VARIABLES: variables used to define the geometry (to be used in LAMMPS) hasgroup, hasmove: flag to force the sections group and move SECTIONS: they must be PIZZA.script | 19 | 1.0 |
| `Plane` | `__or__` | overload | pipe | 19 | 1.0 |
| `Plane` | `__repr__` | display method | 24 | 1.0 |
| `Plane` | `__setstate__` | setstate for cooperative inheritance / duplication | 3 | 1.0 |
| `Plane` | `copy` | returns a copy of the graphical object | 11 | 1.0 |
| `Plane` | `creategroup` | force the group creation in script | 3 | 1.0 |
| `Plane` | `createmove` | force the fix move creation in script | 3 | 1.0 |
| `Plane` | `do` | generates a script | 6 | 1.0 |
| `Plane` | `fixmoveargs` | Validates all arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) the result is adictionary, all fixmove can be combined | 18 | 1.0 |
| `Plane` | `fixmoveargvalidator` | Validation of arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) | 39 | 1.0 |
| `Plane` | `get_fixmovesyntax` | Returns the syntax for LAMMPS command, or detailed explanation for a specific argument type | 39 | 1.0 |
| `Plane` | `movearg` | Validation of move arguments for region command (https://docs.lammps.org/region.html) move args = v_x v_y v_z v_x,v_y,v_z = equal-style variables for x,y,z displacement of region over time (distance units) | 39 | 1.0 |
| `Plane` | `openarg` | Validation of open arguments for region command (https://docs.lammps.org/region.html) open value = integer from 1-6 corresponding to face index (see below) The indices specified as part of the open keyword have the following meanings: | 32 | 1.0 |
| `Plane` | `removegroup` | force the group creation in script | 3 | 1.0 |
| `Plane` | `removemove` | force the fix move creation in script | 3 | 1.0 |
| `Plane` | `rotatearg` | Validation of rotate arguments for region command (https://docs.lammps.org/region.html) rotate args = v_theta Px Py Pz Rx Ry Rz v_theta = equal-style variable for rotaton of region over time (in radians) Px,Py,Pz = origin for axis of rotation (distance units) Rx,Ry,Rz = axis of rotation vector | 36 | 1.0 |
| `Plane` | `scriptobject` | Method to return a scriptobject based on region instead of an input file Syntax similar to script.scriptobject OBJ = scriptobject(...) Implemented properties: beadtype=1,2,... name="short name" fullname = "comprehensive name" style = "smd" forcefield = any valid forcefield instance (default = rigidwall()) | 34 | 1.0 |
| `Plane` | `setgroup` | force the group creation in script | 3 | 1.0 |
| `Plane` | `sidearg` | Validation of side arguments for region command (https://docs.lammps.org/region.html) side value = in or out in = the region is inside the specified geometry out = the region is outside the specified geometry | 20 | 1.0 |
| `Plane` | `unitsarg` | Validation for units arguments for region command (https://docs.lammps.org/region.html) units value = lattice or box lattice = the geometry is defined in lattice units box = the geometry is defined in simulation box units | 20 | 1.0 |
| `Plane` | `update` | update the USER content for all three scripts | 14 | 1.0 |
| `Prism` | `__add__` | overload addition ("+") operator | 19 | 1.0 |
| `Prism` | `__copy__` | copy method | 6 | 1.0 |
| `Prism` | `__deepcopy__` | deep copy method | 8 | 1.0 |
| `Prism` | `__getstate__` | getstate for cooperative inheritance / duplication | 3 | 1.0 |
| `Prism` | `__iadd__` | overload iaddition ("+=") operator | 16 | 1.0 |
| `Prism` | `__init__` | constructor of the generic core geometry USER: any definitions requires by the geometry VARIABLES: variables used to define the geometry (to be used in LAMMPS) hasgroup, hasmove: flag to force the sections group and move SECTIONS: they must be PIZZA.script | 23 | 1.0 |
| `Prism` | `__or__` | overload | pipe | 19 | 1.0 |
| `Prism` | `__repr__` | display method | 24 | 1.0 |
| `Prism` | `__setstate__` | setstate for cooperative inheritance / duplication | 3 | 1.0 |
| `Prism` | `copy` | returns a copy of the graphical object | 11 | 1.0 |
| `Prism` | `creategroup` | force the group creation in script | 3 | 1.0 |
| `Prism` | `createmove` | force the fix move creation in script | 3 | 1.0 |
| `Prism` | `do` | generates a script | 6 | 1.0 |
| `Prism` | `fixmoveargs` | Validates all arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) the result is adictionary, all fixmove can be combined | 18 | 1.0 |
| `Prism` | `fixmoveargvalidator` | Validation of arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) | 39 | 1.0 |
| `Prism` | `get_fixmovesyntax` | Returns the syntax for LAMMPS command, or detailed explanation for a specific argument type | 39 | 1.0 |
| `Prism` | `movearg` | Validation of move arguments for region command (https://docs.lammps.org/region.html) move args = v_x v_y v_z v_x,v_y,v_z = equal-style variables for x,y,z displacement of region over time (distance units) | 39 | 1.0 |
| `Prism` | `openarg` | Validation of open arguments for region command (https://docs.lammps.org/region.html) open value = integer from 1-6 corresponding to face index (see below) The indices specified as part of the open keyword have the following meanings: | 32 | 1.0 |
| `Prism` | `removegroup` | force the group creation in script | 3 | 1.0 |
| `Prism` | `removemove` | force the fix move creation in script | 3 | 1.0 |
| `Prism` | `rotatearg` | Validation of rotate arguments for region command (https://docs.lammps.org/region.html) rotate args = v_theta Px Py Pz Rx Ry Rz v_theta = equal-style variable for rotaton of region over time (in radians) Px,Py,Pz = origin for axis of rotation (distance units) Rx,Ry,Rz = axis of rotation vector | 36 | 1.0 |
| `Prism` | `scriptobject` | Method to return a scriptobject based on region instead of an input file Syntax similar to script.scriptobject OBJ = scriptobject(...) Implemented properties: beadtype=1,2,... name="short name" fullname = "comprehensive name" style = "smd" forcefield = any valid forcefield instance (default = rigidwall()) | 34 | 1.0 |
| `Prism` | `setgroup` | force the group creation in script | 3 | 1.0 |
| `Prism` | `sidearg` | Validation of side arguments for region command (https://docs.lammps.org/region.html) side value = in or out in = the region is inside the specified geometry out = the region is outside the specified geometry | 20 | 1.0 |
| `Prism` | `unitsarg` | Validation for units arguments for region command (https://docs.lammps.org/region.html) units value = lattice or box lattice = the geometry is defined in lattice units box = the geometry is defined in simulation box units | 20 | 1.0 |
| `Prism` | `update` | update the USER content for all three scripts | 14 | 1.0 |
| `Prism` | `volume` | Calculate the volume of the prism based on USER.args | 22 | 1.0 |
| `Sphere` | `__add__` | overload addition ("+") operator | 19 | 1.0 |
| `Sphere` | `__copy__` | copy method | 6 | 1.0 |
| `Sphere` | `__deepcopy__` | deep copy method | 8 | 1.0 |
| `Sphere` | `__getstate__` | getstate for cooperative inheritance / duplication | 3 | 1.0 |
| `Sphere` | `__iadd__` | overload iaddition ("+=") operator | 16 | 1.0 |
| `Sphere` | `__init__` | constructor of the generic core geometry USER: any definitions requires by the geometry VARIABLES: variables used to define the geometry (to be used in LAMMPS) hasgroup, hasmove: flag to force the sections group and move SECTIONS: they must be PIZZA.script | 23 | 1.0 |
| `Sphere` | `__or__` | overload | pipe | 19 | 1.0 |
| `Sphere` | `__repr__` | display method | 24 | 1.0 |
| `Sphere` | `__setstate__` | setstate for cooperative inheritance / duplication | 3 | 1.0 |
| `Sphere` | `copy` | returns a copy of the graphical object | 11 | 1.0 |
| `Sphere` | `creategroup` | force the group creation in script | 3 | 1.0 |
| `Sphere` | `createmove` | force the fix move creation in script | 3 | 1.0 |
| `Sphere` | `do` | generates a script | 6 | 1.0 |
| `Sphere` | `fixmoveargs` | Validates all arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) the result is adictionary, all fixmove can be combined | 18 | 1.0 |
| `Sphere` | `fixmoveargvalidator` | Validation of arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) | 39 | 1.0 |
| `Sphere` | `get_fixmovesyntax` | Returns the syntax for LAMMPS command, or detailed explanation for a specific argument type | 39 | 1.0 |
| `Sphere` | `movearg` | Validation of move arguments for region command (https://docs.lammps.org/region.html) move args = v_x v_y v_z v_x,v_y,v_z = equal-style variables for x,y,z displacement of region over time (distance units) | 39 | 1.0 |
| `Sphere` | `openarg` | Validation of open arguments for region command (https://docs.lammps.org/region.html) open value = integer from 1-6 corresponding to face index (see below) The indices specified as part of the open keyword have the following meanings: | 32 | 1.0 |
| `Sphere` | `removegroup` | force the group creation in script | 3 | 1.0 |
| `Sphere` | `removemove` | force the fix move creation in script | 3 | 1.0 |
| `Sphere` | `rotatearg` | Validation of rotate arguments for region command (https://docs.lammps.org/region.html) rotate args = v_theta Px Py Pz Rx Ry Rz v_theta = equal-style variable for rotaton of region over time (in radians) Px,Py,Pz = origin for axis of rotation (distance units) Rx,Ry,Rz = axis of rotation vector | 36 | 1.0 |
| `Sphere` | `scriptobject` | Method to return a scriptobject based on region instead of an input file Syntax similar to script.scriptobject OBJ = scriptobject(...) Implemented properties: beadtype=1,2,... name="short name" fullname = "comprehensive name" style = "smd" forcefield = any valid forcefield instance (default = rigidwall()) | 34 | 1.0 |
| `Sphere` | `setgroup` | force the group creation in script | 3 | 1.0 |
| `Sphere` | `sidearg` | Validation of side arguments for region command (https://docs.lammps.org/region.html) side value = in or out in = the region is inside the specified geometry out = the region is outside the specified geometry | 20 | 1.0 |
| `Sphere` | `unitsarg` | Validation for units arguments for region command (https://docs.lammps.org/region.html) units value = lattice or box lattice = the geometry is defined in lattice units box = the geometry is defined in simulation box units | 20 | 1.0 |
| `Sphere` | `update` | update the USER content for all three scripts | 14 | 1.0 |
| `Sphere` | `volume` | Calculate the volume of the sphere based on USER.args | 13 | 1.0 |
| `Union` | `__add__` | overload addition ("+") operator | 19 | 1.0 |
| `Union` | `__copy__` | copy method | 6 | 1.0 |
| `Union` | `__deepcopy__` | deep copy method | 8 | 1.0 |
| `Union` | `__getstate__` | getstate for cooperative inheritance / duplication | 3 | 1.0 |
| `Union` | `__iadd__` | overload iaddition ("+=") operator | 16 | 1.0 |
| `Union` | `__init__` | constructor of the generic core geometry USER: any definitions requires by the geometry VARIABLES: variables used to define the geometry (to be used in LAMMPS) hasgroup, hasmove: flag to force the sections group and move SECTIONS: they must be PIZZA.script | 14 | 1.0 |
| `Union` | `__or__` | overload | pipe | 19 | 1.0 |
| `Union` | `__repr__` | display method | 24 | 1.0 |
| `Union` | `__setstate__` | setstate for cooperative inheritance / duplication | 3 | 1.0 |
| `Union` | `copy` | returns a copy of the graphical object | 11 | 1.0 |
| `Union` | `creategroup` | force the group creation in script | 3 | 1.0 |
| `Union` | `createmove` | force the fix move creation in script | 3 | 1.0 |
| `Union` | `do` | generates a script | 6 | 1.0 |
| `Union` | `fixmoveargs` | Validates all arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) the result is adictionary, all fixmove can be combined | 18 | 1.0 |
| `Union` | `fixmoveargvalidator` | Validation of arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) | 39 | 1.0 |
| `Union` | `get_fixmovesyntax` | Returns the syntax for LAMMPS command, or detailed explanation for a specific argument type | 39 | 1.0 |
| `Union` | `movearg` | Validation of move arguments for region command (https://docs.lammps.org/region.html) move args = v_x v_y v_z v_x,v_y,v_z = equal-style variables for x,y,z displacement of region over time (distance units) | 39 | 1.0 |
| `Union` | `openarg` | Validation of open arguments for region command (https://docs.lammps.org/region.html) open value = integer from 1-6 corresponding to face index (see below) The indices specified as part of the open keyword have the following meanings: | 32 | 1.0 |
| `Union` | `removegroup` | force the group creation in script | 3 | 1.0 |
| `Union` | `removemove` | force the fix move creation in script | 3 | 1.0 |
| `Union` | `rotatearg` | Validation of rotate arguments for region command (https://docs.lammps.org/region.html) rotate args = v_theta Px Py Pz Rx Ry Rz v_theta = equal-style variable for rotaton of region over time (in radians) Px,Py,Pz = origin for axis of rotation (distance units) Rx,Ry,Rz = axis of rotation vector | 36 | 1.0 |
| `Union` | `scriptobject` | Method to return a scriptobject based on region instead of an input file Syntax similar to script.scriptobject OBJ = scriptobject(...) Implemented properties: beadtype=1,2,... name="short name" fullname = "comprehensive name" style = "smd" forcefield = any valid forcefield instance (default = rigidwall()) | 34 | 1.0 |
| `Union` | `setgroup` | force the group creation in script | 3 | 1.0 |
| `Union` | `sidearg` | Validation of side arguments for region command (https://docs.lammps.org/region.html) side value = in or out in = the region is inside the specified geometry out = the region is outside the specified geometry | 20 | 1.0 |
| `Union` | `unitsarg` | Validation for units arguments for region command (https://docs.lammps.org/region.html) units value = lattice or box lattice = the geometry is defined in lattice units box = the geometry is defined in simulation box units | 20 | 1.0 |
| `Union` | `update` | update the USER content for all three scripts | 14 | 1.0 |
| `coregeometry` | `__add__` | overload addition ("+") operator | 19 | 1.0 |
| `coregeometry` | `__copy__` | copy method | 6 | 1.0 |
| `coregeometry` | `__deepcopy__` | deep copy method | 8 | 1.0 |
| `coregeometry` | `__getstate__` | getstate for cooperative inheritance / duplication | 3 | 1.0 |
| `coregeometry` | `__iadd__` | overload iaddition ("+=") operator | 16 | 1.0 |
| `coregeometry` | `__init__` | constructor of the generic core geometry USER: any definitions requires by the geometry VARIABLES: variables used to define the geometry (to be used in LAMMPS) hasgroup, hasmove: flag to force the sections group and move SECTIONS: they must be PIZZA.script | 48 | 1.0 |
| `coregeometry` | `__or__` | overload | pipe | 19 | 1.0 |
| `coregeometry` | `__repr__` | display method | 24 | 1.0 |
| `coregeometry` | `__setstate__` | setstate for cooperative inheritance / duplication | 3 | 1.0 |
| `coregeometry` | `copy` | returns a copy of the graphical object | 11 | 1.0 |
| `coregeometry` | `creategroup` | force the group creation in script | 3 | 1.0 |
| `coregeometry` | `createmove` | force the fix move creation in script | 3 | 1.0 |
| `coregeometry` | `do` | generates a script | 6 | 1.0 |
| `coregeometry` | `fixmoveargs` | Validates all arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) the result is adictionary, all fixmove can be combined | 18 | 1.0 |
| `coregeometry` | `fixmoveargvalidator` | Validation of arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) | 39 | 1.0 |
| `coregeometry` | `get_fixmovesyntax` | Returns the syntax for LAMMPS command, or detailed explanation for a specific argument type | 39 | 1.0 |
| `coregeometry` | `movearg` | Validation of move arguments for region command (https://docs.lammps.org/region.html) move args = v_x v_y v_z v_x,v_y,v_z = equal-style variables for x,y,z displacement of region over time (distance units) | 39 | 1.0 |
| `coregeometry` | `openarg` | Validation of open arguments for region command (https://docs.lammps.org/region.html) open value = integer from 1-6 corresponding to face index (see below) The indices specified as part of the open keyword have the following meanings: | 32 | 1.0 |
| `coregeometry` | `removegroup` | force the group creation in script | 3 | 1.0 |
| `coregeometry` | `removemove` | force the fix move creation in script | 3 | 1.0 |
| `coregeometry` | `rotatearg` | Validation of rotate arguments for region command (https://docs.lammps.org/region.html) rotate args = v_theta Px Py Pz Rx Ry Rz v_theta = equal-style variable for rotaton of region over time (in radians) Px,Py,Pz = origin for axis of rotation (distance units) Rx,Ry,Rz = axis of rotation vector | 36 | 1.0 |
| `coregeometry` | `scriptobject` | Method to return a scriptobject based on region instead of an input file Syntax similar to script.scriptobject OBJ = scriptobject(...) Implemented properties: beadtype=1,2,... name="short name" fullname = "comprehensive name" style = "smd" forcefield = any valid forcefield instance (default = rigidwall()) | 34 | 1.0 |
| `coregeometry` | `setgroup` | force the group creation in script | 3 | 1.0 |
| `coregeometry` | `sidearg` | Validation of side arguments for region command (https://docs.lammps.org/region.html) side value = in or out in = the region is inside the specified geometry out = the region is outside the specified geometry | 20 | 1.0 |
| `coregeometry` | `unitsarg` | Validation for units arguments for region command (https://docs.lammps.org/region.html) units value = lattice or box lattice = the geometry is defined in lattice units box = the geometry is defined in simulation box units | 20 | 1.0 |
| `coregeometry` | `update` | update the USER content for all three scripts | 14 | 1.0 |
| `emulsion` | `__init__` | Parameters ---------- The insertions are performed between xmin,ymin and xmax,ymax xmin : int64 or real, optional x left corner. The default is 10. ymin : int64 or real, optional y bottom corner. The default is 10. zmin : int64 or real, optional z bottom corner. The default is 10. xmax : int64 or real, optional x right corner. The default is 90. ymax : int64 or real, optional y top corner. The default is 90. zmax : int64 or real, optional z top corner. The default is 90. beadtype : default beadtype to apply if not precised at insertion maxtrials : integer, optional Maximum of attempts for an object. The default is 1000. forcedinsertion : logical, optional Set it to true to force the next insertion. The default is True. | 40 | 1.0 |
| `emulsion` | `__repr__` | Return repr(self). | 6 | 1.0 |
| `emulsion` | `accepted` | acceptation criterion | 3 | 1.0 |
| `emulsion` | `dist` | shortest distance of the center (x,y) to the wall or any object | 3 | 1.0 |
| `emulsion` | `insertion` | insert a list of objects nsuccess=insertion(rlist,beadtype=None) beadtype=b forces the value b if None, defaultbeadtype is used instead | 21 | 1.0 |
| `emulsion` | `insertone` | insert one object of radius r properties: x,y,z coordinates (if missing, picked randomly from uniform distribution) r radius (default = 2% of diagonal) beadtype (default = defautbeadtype) overlap = False (accept only if no overlap) | 28 | 1.0 |
| `emulsion` | `pairdist` | pair distance to the surface of all disks/spheres | 6 | 1.0 |
| `emulsion` | `rand` | random position x,y | 5 | 1.0 |
| `emulsion` | `setbeadtype` | set the default or the supplied beadtype | 8 | 1.0 |
| `emulsion` | `walldist` | shortest distance to the wall | 3 | 1.0 |
| `headersRegiondata` | `generatorforlammps` | generate LAMMPS code from regiondata (struct) generatorforlammps(verbose,hasvariables) hasvariables = False is used to prevent a call of generatorforLammps() for scripts others than LammpsGeneric ones | 31 | 1.0 |
| `region` | `__contains__` | in override | 3 | 1.0 |
| `region` | `__getattr__` | getattr attribute override | 14 | 1.0 |
| `region` | `__getitem__` | R[i] returns the ith element of the structure R[:4] returns a structure with the four first fields R[[1,3]] returns the second and fourth elements | 20 | 1.0 |
| `region` | `__getstate__` | getstate for cooperative inheritance / duplication | 3 | 1.0 |
| `region` | `__init__` | constructor | 202 | 1.0 |
| `region` | `__iter__` | region iterator | 6 | 1.0 |
| `region` | `__len__` | len method | 3 | 1.0 |
| `region` | `__next__` | region iterator | 7 | 1.0 |
| `region` | `__repr__` | display method | 24 | 1.0 |
| `region` | `__setattr__` | setattr override | 6 | 1.0 |
| `region` | `__setstate__` | setstate for cooperative inheritance / duplication | 3 | 1.0 |
| `region` | `__str__` | string representation of a region | 4 | 1.0 |
| `region` | `block` | creates a block region xlo,xhi,ylo,yhi,zlo,zhi = bounds of block in all dimensions (distance units) | 96 | 1.0 |
| `region` | `collection` |  | 27 | 1.0 |
| `region` | `cone` | creates a cone region dim = "x" or "y" or "z" = axis of the cone note: USER, LAMMPS variables are not authorized here c1,c2 = coords of cone axis in other 2 dimensions (distance units) radlo,radhi = cone radii at lo and hi end (distance units) lo,hi = bounds of cone in dim (distance units) | 127 | 1.0 |
| `region` | `count` | count objects by type | 13 | 1.0 |
| `region` | `cylinder` | creates a cylinder region dim = x or y or z = axis of cylinder c1,c2 = coords of cylinder axis in other 2 dimensions (distance units) radius = cylinder radius (distance units) c1,c2, and radius can be a LAMMPS variable lo,hi = bounds of cylinder in dim (distance units) | 122 | 1.0 |
| `region` | `delete` | delete object | 10 | 1.0 |
| `region` | `do` | execute the entire script | 3 | 1.0 |
| `region` | `dolive` | execute the entire script for online testing see: https://editor.lammps.org/ | 10 | 1.0 |
| `region` | `ellipsoid` | creates an ellipsoid region ellipsoid(x,y,z,a,b,c [,name=None,beadtype=None,property=value,...]) x,y,z = center of ellipsoid (distance units) a,b,c = half the length of the principal axes of the ellipsoid (distance units) | 114 | 1.0 |
| `region` | `eval` | evaluates (i.e, combine scripts) an expression combining objects R= region(name="my region") R.eval(o1+o2+...,name='obj') R.eval(o1|o2|...,name='obj') R.name will be the resulting object of class region.eval (region.coregeometry) | 41 | 1.0 |
| `region` | `get` | returns the object | 6 | 1.0 |
| `region` | `group` |  | 2 | 1.0 |
| `region` | `hasattr` | return true if the object exist | 4 | 1.0 |
| `region` | `intersect` | creates an intersection region intersect("reg-ID1","reg-ID2",name="myname",beadtype=1,...) reg-ID1,reg-ID2, ... = IDs of regions to join together | 60 | 1.0 |
| `region` | `list` | list objects | 10 | 1.0 |
| `region` | `pipescript` |  | 24 | 1.0 |
| `region` | `plane` | creates a plane region px,py,pz = point on the plane (distance units) nx,ny,nz = direction normal to plane (distance units) | 93 | 1.0 |
| `region` | `prism` | creates a prism region xlo,xhi,ylo,yhi,zlo,zhi = bounds of untilted prism (distance units) xy = distance to tilt y in x direction (distance units) xz = distance to tilt z in x direction (distance units) yz = distance to tilt z in y direction (distance units) | 101 | 1.0 |
| `region` | `pscriptHeaders` | Surrogate method for generating LAMMPS pipescript headers. Calls the `scriptHeaders` method with `pipescript=True`. | 19 | 1.0 |
| `region` | `scale_and_translate` | Scale and translate a value or encapsulate the formula within a string. | 47 | 1.0 |
| `region` | `scatter` | Parameters ---------- E : scatter or emulsion object codes for x,y,z and r. name : string, optional name of the collection. The default is "emulsion". beadtype : integer, optional for all objects. The default is 1. | 37 | 1.0 |
| `region` | `script` | script all objects in the region | 30 | 1.0 |
| `region` | `scriptHeaders` | Generate and return LAMMPS header scripts for initializing the simulation, defining the lattice, and specifying the simulation box for all region objects. | 71 | 1.0 |
| `region` | `set` | set field and value | 17 | 1.0 |
| `region` | `sphere` | creates a sphere region x,y,z = center of sphere (distance units) radius = radius of sphere (distance units) x,y,z, and radius can be a variable | 95 | 1.0 |
| `region` | `union` | creates a union region union("reg-ID1","reg-ID2",name="myname",beadtype=1,...) reg-ID1,reg-ID2, ... = IDs of regions to join together | 60 | 1.0 |
| `regioncollection` | `__init__` | constructor, use debug=True to report eval errors | 11 | 1.0 |
| `regiondata` | `generatorforlammps` | generate LAMMPS code from regiondata (struct) generatorforlammps(verbose,hasvariables) hasvariables = False is used to prevent a call of generatorforLammps() for scripts others than LammpsGeneric ones | 31 | 1.0 |
| `scatter` | `__init__` | The scatter class provides an easy constructor to distribute in space objects according to their positions x,y,z size r (radius) and beadtype. | 17 | 1.0 |
| `scatter` | `pairdist` | pair distance to the surface of all disks/spheres | 6 | 1.0 |

<a id="pizza_script" name="pizza_script"></a>
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; font-size: 0.8em;"><a href="#pizza_region" title="Go to Previous Module: pizza.region" style="text-decoration: none;">⬅️ Previous</a>
<a href="#table_of_contents" title="Back to Table of Contents" style="text-decoration: none;">⬆️ TOC</a>
<span></span>
</div>

## Module `pizza.script`

### Class Inheritance Diagram
```mermaid
graph TD;
CallableScript
VariableOccurrences
boundarysection
discretizationsection
dumpsection
forcefield
geometrysection
globalsection
initializesection
integrationsection
interactionsection
none
param
paramauto
parameterforcefield
pipescript
rigidwall
runsection
saltTLSPH
script
scriptdata
scriptobject
scriptobjectgroup
smd
solidfood
statussection
struct
tlsph
tlsphalone
ulsph
ulsphalone
water
forcefield --> smd
forcefield --> tlsphalone
none --> rigidwall
object --> CallableScript
object --> VariableOccurrences
object --> forcefield
object --> pipescript
object --> script
object --> struct
param --> paramauto
param --> scriptdata
paramauto --> parameterforcefield
script --> boundarysection
script --> discretizationsection
script --> dumpsection
script --> geometrysection
script --> globalsection
script --> initializesection
script --> integrationsection
script --> interactionsection
script --> runsection
script --> statussection
smd --> none
smd --> tlsph
smd --> ulsph
smd --> ulsphalone
struct --> param
struct --> scriptobject
struct --> scriptobjectgroup
tlsph --> saltTLSPH
tlsph --> solidfood
ulsph --> water
```

**[Class Examples for `pizza/script.py` (4)](class_examples.html#pizza_script)**

### Methods Table

| Class | Method | Docstring First Paragraph | # Lines | __version__ |
|-------|---------|---------------------------|---------|-------------|
| (module-level) | `frame_header` | Format the header content into an ASCII framed box with customizable properties. | 147 | 1.006 |
| (module-level) | `get_metadata` | Return a dictionary of explicitly defined metadata. | 15 | 1.006 |
| (module-level) | `<lambda>` |  | 1 | 1.006 |
| (module-level) | `is_scalar` | Determines if a value is scalar (not a list, dict, or tuple). | 5 | 1.006 |
| (module-level) | `make_hashable` | Recursively converts lists and dictionaries to tuples to make them hashable. | 9 | 1.006 |
| (module-level) | `picker` |  | 1 | 1.006 |
| (module-level) | `remove_comments` | Removes comments from a single or multi-line string, handling quotes, escaped characters, and line continuation. | 101 | 1.006 |
| (module-level) | `span` |  | 2 | 1.006 |
| `CallableScript` | `__call__` | Call self as a function. | 3 | 1.006 |
| `CallableScript` | `__get__` |  | 3 | 1.006 |
| `CallableScript` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 2 | 1.006 |
| `VariableOccurrences` | `__init__` | Initializes the VariableOccurrences object. | 38 | 1.006 |
| `VariableOccurrences` | `_determine_scopes` | Determines the unique scopes present across all variables. | 7 | 1.006 |
| `VariableOccurrences` | `export` | Exports the variable occurrences to a file or returns the content as a string. | 161 | 1.006 |
| `VariableOccurrences` | `get_all_elements_in_lists` | Retrieves all unique elements within list-type variable values. | 26 | 1.006 |
| `VariableOccurrences` | `get_all_values` | Retrieves all unique values of the variable(s). | 26 | 1.006 |
| `VariableOccurrences` | `get_raw_data` | Returns the raw data. | 8 | 1.006 |
| `VariableOccurrences` | `get_steps_with_value` | Retrieves the steps where the variable equals the specified value. | 52 | 1.006 |
| `VariableOccurrences` | `get_steps_with_value_in_scope` | Retrieves the steps within a specific scope where the variable equals the specified value. | 45 | 1.006 |
| `VariableOccurrences` | `get_usage_count` | Counts how many times a specific value is used. | 48 | 1.006 |
| `VariableOccurrences` | `summarize` | Provides a summary of the variable occurrences. | 72 | 1.006 |
| `boundarysection` | `__add__` | overload addition operator | 24 | 1.006 |
| `boundarysection` | `__and__` | overload and operator | 7 | 1.006 |
| `boundarysection` | `__copy__` | copy method | 6 | 1.006 |
| `boundarysection` | `__deepcopy__` | deep copy method | 8 | 1.006 |
| `boundarysection` | `__init__` | constructor adding instance definitions stored in USER | 14 | 1.006 |
| `boundarysection` | `__mul__` | overload * operator | 8 | 1.006 |
| `boundarysection` | `__or__` | overload | or for pipe | 19 | 1.006 |
| `boundarysection` | `__pow__` | overload ** operator | 8 | 1.006 |
| `boundarysection` | `__repr__` | disp method | 22 | 1.006 |
| `boundarysection` | `__rshift__` | overload right  shift operator (keep only the last template) | 10 | 1.006 |
| `boundarysection` | `__str__` | string representation | 3 | 1.006 |
| `boundarysection` | `_iadd__` | overload addition operator | 8 | 1.006 |
| `boundarysection` | `detect_variables` | Detects variables in the content of the template using an extended pattern to include indexed variables (e.g., ${var[i]}) if `with_index` is True. | 42 | 1.006 |
| `boundarysection` | `do` | Generate the LAMMPS script based on the current configuration. | 77 | 1.006 |
| `boundarysection` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 1.006 |
| `boundarysection` | `header` | Generate a formatted header for the script file. | 37 | 1.006 |
| `boundarysection` | `printheader` | print header | 7 | 1.006 |
| `boundarysection` | `tmpwrite` | Write the script to a temporary file and create optional persistent copies. | 92 | 1.006 |
| `boundarysection` | `write` | Write the script to a file. | 39 | 1.006 |
| `discretizationsection` | `__add__` | overload addition operator | 24 | 1.006 |
| `discretizationsection` | `__and__` | overload and operator | 7 | 1.006 |
| `discretizationsection` | `__copy__` | copy method | 6 | 1.006 |
| `discretizationsection` | `__deepcopy__` | deep copy method | 8 | 1.006 |
| `discretizationsection` | `__init__` | constructor adding instance definitions stored in USER | 14 | 1.006 |
| `discretizationsection` | `__mul__` | overload * operator | 8 | 1.006 |
| `discretizationsection` | `__or__` | overload | or for pipe | 19 | 1.006 |
| `discretizationsection` | `__pow__` | overload ** operator | 8 | 1.006 |
| `discretizationsection` | `__repr__` | disp method | 22 | 1.006 |
| `discretizationsection` | `__rshift__` | overload right  shift operator (keep only the last template) | 10 | 1.006 |
| `discretizationsection` | `__str__` | string representation | 3 | 1.006 |
| `discretizationsection` | `_iadd__` | overload addition operator | 8 | 1.006 |
| `discretizationsection` | `detect_variables` | Detects variables in the content of the template using an extended pattern to include indexed variables (e.g., ${var[i]}) if `with_index` is True. | 42 | 1.006 |
| `discretizationsection` | `do` | Generate the LAMMPS script based on the current configuration. | 77 | 1.006 |
| `discretizationsection` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 1.006 |
| `discretizationsection` | `header` | Generate a formatted header for the script file. | 37 | 1.006 |
| `discretizationsection` | `printheader` | print header | 7 | 1.006 |
| `discretizationsection` | `tmpwrite` | Write the script to a temporary file and create optional persistent copies. | 92 | 1.006 |
| `discretizationsection` | `write` | Write the script to a file. | 39 | 1.006 |
| `dumpsection` | `__add__` | overload addition operator | 24 | 1.006 |
| `dumpsection` | `__and__` | overload and operator | 7 | 1.006 |
| `dumpsection` | `__copy__` | copy method | 6 | 1.006 |
| `dumpsection` | `__deepcopy__` | deep copy method | 8 | 1.006 |
| `dumpsection` | `__init__` | constructor adding instance definitions stored in USER | 14 | 1.006 |
| `dumpsection` | `__mul__` | overload * operator | 8 | 1.006 |
| `dumpsection` | `__or__` | overload | or for pipe | 19 | 1.006 |
| `dumpsection` | `__pow__` | overload ** operator | 8 | 1.006 |
| `dumpsection` | `__repr__` | disp method | 22 | 1.006 |
| `dumpsection` | `__rshift__` | overload right  shift operator (keep only the last template) | 10 | 1.006 |
| `dumpsection` | `__str__` | string representation | 3 | 1.006 |
| `dumpsection` | `_iadd__` | overload addition operator | 8 | 1.006 |
| `dumpsection` | `detect_variables` | Detects variables in the content of the template using an extended pattern to include indexed variables (e.g., ${var[i]}) if `with_index` is True. | 42 | 1.006 |
| `dumpsection` | `do` | Generate the LAMMPS script based on the current configuration. | 77 | 1.006 |
| `dumpsection` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 1.006 |
| `dumpsection` | `header` | Generate a formatted header for the script file. | 37 | 1.006 |
| `dumpsection` | `printheader` | print header | 7 | 1.006 |
| `dumpsection` | `tmpwrite` | Write the script to a temporary file and create optional persistent copies. | 92 | 1.006 |
| `dumpsection` | `write` | Write the script to a file. | 39 | 1.006 |
| `geometrysection` | `__add__` | overload addition operator | 24 | 1.006 |
| `geometrysection` | `__and__` | overload and operator | 7 | 1.006 |
| `geometrysection` | `__copy__` | copy method | 6 | 1.006 |
| `geometrysection` | `__deepcopy__` | deep copy method | 8 | 1.006 |
| `geometrysection` | `__init__` | constructor adding instance definitions stored in USER | 14 | 1.006 |
| `geometrysection` | `__mul__` | overload * operator | 8 | 1.006 |
| `geometrysection` | `__or__` | overload | or for pipe | 19 | 1.006 |
| `geometrysection` | `__pow__` | overload ** operator | 8 | 1.006 |
| `geometrysection` | `__repr__` | disp method | 22 | 1.006 |
| `geometrysection` | `__rshift__` | overload right  shift operator (keep only the last template) | 10 | 1.006 |
| `geometrysection` | `__str__` | string representation | 3 | 1.006 |
| `geometrysection` | `_iadd__` | overload addition operator | 8 | 1.006 |
| `geometrysection` | `detect_variables` | Detects variables in the content of the template using an extended pattern to include indexed variables (e.g., ${var[i]}) if `with_index` is True. | 42 | 1.006 |
| `geometrysection` | `do` | Generate the LAMMPS script based on the current configuration. | 77 | 1.006 |
| `geometrysection` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 1.006 |
| `geometrysection` | `header` | Generate a formatted header for the script file. | 37 | 1.006 |
| `geometrysection` | `printheader` | print header | 7 | 1.006 |
| `geometrysection` | `tmpwrite` | Write the script to a temporary file and create optional persistent copies. | 92 | 1.006 |
| `geometrysection` | `write` | Write the script to a file. | 39 | 1.006 |
| `globalsection` | `__add__` | overload addition operator | 24 | 1.006 |
| `globalsection` | `__and__` | overload and operator | 7 | 1.006 |
| `globalsection` | `__copy__` | copy method | 6 | 1.006 |
| `globalsection` | `__deepcopy__` | deep copy method | 8 | 1.006 |
| `globalsection` | `__init__` | constructor adding instance definitions stored in USER | 14 | 1.006 |
| `globalsection` | `__mul__` | overload * operator | 8 | 1.006 |
| `globalsection` | `__or__` | overload | or for pipe | 19 | 1.006 |
| `globalsection` | `__pow__` | overload ** operator | 8 | 1.006 |
| `globalsection` | `__repr__` | disp method | 22 | 1.006 |
| `globalsection` | `__rshift__` | overload right  shift operator (keep only the last template) | 10 | 1.006 |
| `globalsection` | `__str__` | string representation | 3 | 1.006 |
| `globalsection` | `_iadd__` | overload addition operator | 8 | 1.006 |
| `globalsection` | `detect_variables` | Detects variables in the content of the template using an extended pattern to include indexed variables (e.g., ${var[i]}) if `with_index` is True. | 42 | 1.006 |
| `globalsection` | `do` | Generate the LAMMPS script based on the current configuration. | 77 | 1.006 |
| `globalsection` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 1.006 |
| `globalsection` | `header` | Generate a formatted header for the script file. | 37 | 1.006 |
| `globalsection` | `printheader` | print header | 7 | 1.006 |
| `globalsection` | `tmpwrite` | Write the script to a temporary file and create optional persistent copies. | 92 | 1.006 |
| `globalsection` | `write` | Write the script to a file. | 39 | 1.006 |
| `initializesection` | `__add__` | overload addition operator | 24 | 1.006 |
| `initializesection` | `__and__` | overload and operator | 7 | 1.006 |
| `initializesection` | `__copy__` | copy method | 6 | 1.006 |
| `initializesection` | `__deepcopy__` | deep copy method | 8 | 1.006 |
| `initializesection` | `__init__` | constructor adding instance definitions stored in USER | 14 | 1.006 |
| `initializesection` | `__mul__` | overload * operator | 8 | 1.006 |
| `initializesection` | `__or__` | overload | or for pipe | 19 | 1.006 |
| `initializesection` | `__pow__` | overload ** operator | 8 | 1.006 |
| `initializesection` | `__repr__` | disp method | 22 | 1.006 |
| `initializesection` | `__rshift__` | overload right  shift operator (keep only the last template) | 10 | 1.006 |
| `initializesection` | `__str__` | string representation | 3 | 1.006 |
| `initializesection` | `_iadd__` | overload addition operator | 8 | 1.006 |
| `initializesection` | `detect_variables` | Detects variables in the content of the template using an extended pattern to include indexed variables (e.g., ${var[i]}) if `with_index` is True. | 42 | 1.006 |
| `initializesection` | `do` | Generate the LAMMPS script based on the current configuration. | 77 | 1.006 |
| `initializesection` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 1.006 |
| `initializesection` | `header` | Generate a formatted header for the script file. | 37 | 1.006 |
| `initializesection` | `printheader` | print header | 7 | 1.006 |
| `initializesection` | `tmpwrite` | Write the script to a temporary file and create optional persistent copies. | 92 | 1.006 |
| `initializesection` | `write` | Write the script to a file. | 39 | 1.006 |
| `integrationsection` | `__add__` | overload addition operator | 24 | 1.006 |
| `integrationsection` | `__and__` | overload and operator | 7 | 1.006 |
| `integrationsection` | `__copy__` | copy method | 6 | 1.006 |
| `integrationsection` | `__deepcopy__` | deep copy method | 8 | 1.006 |
| `integrationsection` | `__init__` | constructor adding instance definitions stored in USER | 14 | 1.006 |
| `integrationsection` | `__mul__` | overload * operator | 8 | 1.006 |
| `integrationsection` | `__or__` | overload | or for pipe | 19 | 1.006 |
| `integrationsection` | `__pow__` | overload ** operator | 8 | 1.006 |
| `integrationsection` | `__repr__` | disp method | 22 | 1.006 |
| `integrationsection` | `__rshift__` | overload right  shift operator (keep only the last template) | 10 | 1.006 |
| `integrationsection` | `__str__` | string representation | 3 | 1.006 |
| `integrationsection` | `_iadd__` | overload addition operator | 8 | 1.006 |
| `integrationsection` | `detect_variables` | Detects variables in the content of the template using an extended pattern to include indexed variables (e.g., ${var[i]}) if `with_index` is True. | 42 | 1.006 |
| `integrationsection` | `do` | Generate the LAMMPS script based on the current configuration. | 77 | 1.006 |
| `integrationsection` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 1.006 |
| `integrationsection` | `header` | Generate a formatted header for the script file. | 37 | 1.006 |
| `integrationsection` | `printheader` | print header | 7 | 1.006 |
| `integrationsection` | `tmpwrite` | Write the script to a temporary file and create optional persistent copies. | 92 | 1.006 |
| `integrationsection` | `write` | Write the script to a file. | 39 | 1.006 |
| `interactionsection` | `__add__` | overload addition operator | 24 | 1.006 |
| `interactionsection` | `__and__` | overload and operator | 7 | 1.006 |
| `interactionsection` | `__copy__` | copy method | 6 | 1.006 |
| `interactionsection` | `__deepcopy__` | deep copy method | 8 | 1.006 |
| `interactionsection` | `__init__` | constructor adding instance definitions stored in USER | 14 | 1.006 |
| `interactionsection` | `__mul__` | overload * operator | 8 | 1.006 |
| `interactionsection` | `__or__` | overload | or for pipe | 19 | 1.006 |
| `interactionsection` | `__pow__` | overload ** operator | 8 | 1.006 |
| `interactionsection` | `__repr__` | disp method | 22 | 1.006 |
| `interactionsection` | `__rshift__` | overload right  shift operator (keep only the last template) | 10 | 1.006 |
| `interactionsection` | `__str__` | string representation | 3 | 1.006 |
| `interactionsection` | `_iadd__` | overload addition operator | 8 | 1.006 |
| `interactionsection` | `detect_variables` | Detects variables in the content of the template using an extended pattern to include indexed variables (e.g., ${var[i]}) if `with_index` is True. | 42 | 1.006 |
| `interactionsection` | `do` | Generate the LAMMPS script based on the current configuration. | 77 | 1.006 |
| `interactionsection` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 1.006 |
| `interactionsection` | `header` | Generate a formatted header for the script file. | 37 | 1.006 |
| `interactionsection` | `printheader` | print header | 7 | 1.006 |
| `interactionsection` | `tmpwrite` | Write the script to a temporary file and create optional persistent copies. | 92 | 1.006 |
| `interactionsection` | `write` | Write the script to a file. | 39 | 1.006 |
| `pipescript` | `__add__` | overload + as pipe with copy | 12 | 1.006 |
| `pipescript` | `__copy__` | copy method | 6 | 1.006 |
| `pipescript` | `__deepcopy__` | deep copy method | 8 | 1.006 |
| `pipescript` | `__getitem__` | return the ith or slice element(s) of the pipe | 24 | 1.006 |
| `pipescript` | `__iadd__` | overload += as pipe without copy | 6 | 1.006 |
| `pipescript` | `__init__` | constructor | 26 | 1.006 |
| `pipescript` | `__len__` | len() method | 3 | 1.006 |
| `pipescript` | `__mul__` | overload * as multiple pipes with copy | 9 | 1.006 |
| `pipescript` | `__or__` | Overload | pipe operator in pipescript | 52 | 1.006 |
| `pipescript` | `__repr__` | display method | 29 | 1.006 |
| `pipescript` | `__setitem__` | modify the ith element of the pipe p[4] = [] removes the 4th element p[4:7] = [] removes the elements from position 4 to 6 p[2:4] = p[0:2] copy the elements 0 and 1 in positions 2 and 3 p[[3,4]]=p[0] | 58 | 1.006 |
| `pipescript` | `__str__` | string representation | 3 | 1.006 |
| `pipescript` | `clear` |  | 16 | 1.006 |
| `pipescript` | `do` | Execute the pipeline or a part of the pipeline and generate the LAMMPS script. | 118 | 1.006 |
| `pipescript` | `do_legacy` | Execute the pipeline or a part of the pipeline and generate the LAMMPS script. | 99 | 1.006 |
| `pipescript` | `dscript` | Convert the current pipescript object to a dscript object. | 115 | 1.006 |
| `pipescript` | `generate_report` | Generates a comprehensive report for specified variables and writes it to a file. | 124 | 1.006 |
| `pipescript` | `getUSER` | getUSER get USER variable getUSER(idx,varname) | 9 | 1.006 |
| `pipescript` | `header` | Generate a formatted header for the pipescript file. | 33 | 1.006 |
| `pipescript` | `join` | join a combination scripts and pipescripts within a pipescript p = pipescript.join([s1,s2,p3,p4,p5...]) | 19 | 1.006 |
| `pipescript` | `list_multiple_values` | Lists all occurrences and values of multiple variables across the pipeline scripts. | 17 | 1.006 |
| `pipescript` | `list_values` | Lists all occurrences and values of a specified variable or all variables across the pipeline scripts. | 118 | 1.006 |
| `pipescript` | `plot_multiple_value_distributions` | Plots the distribution of elements for multiple variables across specified scopes. | 54 | 1.006 |
| `pipescript` | `rename` | rename scripts in the pipe p.rename(idx=[0,2,3],name=["A","B","C"]) | 17 | 1.006 |
| `pipescript` | `script` | script the pipeline or parts of the pipeline s = p.script() s = p.script([0,2]) | 50 | 1.006 |
| `pipescript` | `setUSER` | setUSER sets USER variables setUSER(idx,varname,varvalue) | 9 | 1.006 |
| `pipescript` | `write` | Write the combined script to a file. | 27 | 1.006 |
| `runsection` | `__add__` | overload addition operator | 24 | 1.006 |
| `runsection` | `__and__` | overload and operator | 7 | 1.006 |
| `runsection` | `__copy__` | copy method | 6 | 1.006 |
| `runsection` | `__deepcopy__` | deep copy method | 8 | 1.006 |
| `runsection` | `__init__` | constructor adding instance definitions stored in USER | 14 | 1.006 |
| `runsection` | `__mul__` | overload * operator | 8 | 1.006 |
| `runsection` | `__or__` | overload | or for pipe | 19 | 1.006 |
| `runsection` | `__pow__` | overload ** operator | 8 | 1.006 |
| `runsection` | `__repr__` | disp method | 22 | 1.006 |
| `runsection` | `__rshift__` | overload right  shift operator (keep only the last template) | 10 | 1.006 |
| `runsection` | `__str__` | string representation | 3 | 1.006 |
| `runsection` | `_iadd__` | overload addition operator | 8 | 1.006 |
| `runsection` | `detect_variables` | Detects variables in the content of the template using an extended pattern to include indexed variables (e.g., ${var[i]}) if `with_index` is True. | 42 | 1.006 |
| `runsection` | `do` | Generate the LAMMPS script based on the current configuration. | 77 | 1.006 |
| `runsection` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 1.006 |
| `runsection` | `header` | Generate a formatted header for the script file. | 37 | 1.006 |
| `runsection` | `printheader` | print header | 7 | 1.006 |
| `runsection` | `tmpwrite` | Write the script to a temporary file and create optional persistent copies. | 92 | 1.006 |
| `runsection` | `write` | Write the script to a file. | 39 | 1.006 |
| `script` | `__add__` | overload addition operator | 24 | 1.006 |
| `script` | `__and__` | overload and operator | 7 | 1.006 |
| `script` | `__copy__` | copy method | 6 | 1.006 |
| `script` | `__deepcopy__` | deep copy method | 8 | 1.006 |
| `script` | `__init__` | constructor adding instance definitions stored in USER | 14 | 1.006 |
| `script` | `__mul__` | overload * operator | 8 | 1.006 |
| `script` | `__or__` | overload | or for pipe | 19 | 1.006 |
| `script` | `__pow__` | overload ** operator | 8 | 1.006 |
| `script` | `__repr__` | disp method | 22 | 1.006 |
| `script` | `__rshift__` | overload right  shift operator (keep only the last template) | 10 | 1.006 |
| `script` | `__str__` | string representation | 3 | 1.006 |
| `script` | `_iadd__` | overload addition operator | 8 | 1.006 |
| `script` | `detect_variables` | Detects variables in the content of the template using an extended pattern to include indexed variables (e.g., ${var[i]}) if `with_index` is True. | 42 | 1.006 |
| `script` | `do` | Generate the LAMMPS script based on the current configuration. | 77 | 1.006 |
| `script` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 1.006 |
| `script` | `header` | Generate a formatted header for the script file. | 37 | 1.006 |
| `script` | `printheader` | print header | 7 | 1.006 |
| `script` | `tmpwrite` | Write the script to a temporary file and create optional persistent copies. | 92 | 1.006 |
| `script` | `write` | Write the script to a file. | 39 | 1.006 |
| `scriptobject` | `__add__` | Add two structure objects, with precedence as follows: | 12 | 1.006 |
| `scriptobject` | `__eq__` | Return self==value. | 3 | 1.006 |
| `scriptobject` | `__ge__` | Return self>=value. | 2 | 1.006 |
| `scriptobject` | `__gt__` | Return self>value. | 2 | 1.006 |
| `scriptobject` | `__init__` | constructor, use debug=True to report eval errors | 30 | 1.006 |
| `scriptobject` | `__le__` | Return self<=value. | 2 | 1.006 |
| `scriptobject` | `__lt__` | Return self<value. | 2 | 1.006 |
| `scriptobject` | `__ne__` | Return self!=value. | 2 | 1.006 |
| `scriptobject` | `__or__` | overload | or for pipe | 6 | 1.006 |
| `scriptobject` | `__str__` | string representation | 3 | 1.006 |
| `scriptobjectgroup` | `__add__` | overload + | 32 | 1.006 |
| `scriptobjectgroup` | `__init__` | SOG constructor | 18 | 1.006 |
| `scriptobjectgroup` | `__or__` | overload | or for pipe | 6 | 1.006 |
| `scriptobjectgroup` | `__str__` | string representation | 3 | 1.006 |
| `scriptobjectgroup` | `group_generator` | Generate and return a group object. | 28 | 1.006 |
| `scriptobjectgroup` | `<lambda>` |  | 1 | 1.006 |
| `scriptobjectgroup` | `mass` | Generates LAMMPS mass commands for each unique beadtype in the collection. | 89 | 1.006 |
| `scriptobjectgroup` | `<lambda>` |  | 1 | 1.006 |
| `scriptobjectgroup` | `select` | select bead from a keep beadlist | 11 | 1.006 |
| `scriptobjectgroup` | `struct` | create a group with name | 10 | 1.006 |
| `statussection` | `__add__` | overload addition operator | 24 | 1.006 |
| `statussection` | `__and__` | overload and operator | 7 | 1.006 |
| `statussection` | `__copy__` | copy method | 6 | 1.006 |
| `statussection` | `__deepcopy__` | deep copy method | 8 | 1.006 |
| `statussection` | `__init__` | constructor adding instance definitions stored in USER | 14 | 1.006 |
| `statussection` | `__mul__` | overload * operator | 8 | 1.006 |
| `statussection` | `__or__` | overload | or for pipe | 19 | 1.006 |
| `statussection` | `__pow__` | overload ** operator | 8 | 1.006 |
| `statussection` | `__repr__` | disp method | 22 | 1.006 |
| `statussection` | `__rshift__` | overload right  shift operator (keep only the last template) | 10 | 1.006 |
| `statussection` | `__str__` | string representation | 3 | 1.006 |
| `statussection` | `_iadd__` | overload addition operator | 8 | 1.006 |
| `statussection` | `detect_variables` | Detects variables in the content of the template using an extended pattern to include indexed variables (e.g., ${var[i]}) if `with_index` is True. | 42 | 1.006 |
| `statussection` | `do` | Generate the LAMMPS script based on the current configuration. | 77 | 1.006 |
| `statussection` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 1.006 |
| `statussection` | `header` | Generate a formatted header for the script file. | 37 | 1.006 |
| `statussection` | `printheader` | print header | 7 | 1.006 |
| `statussection` | `tmpwrite` | Write the script to a temporary file and create optional persistent copies. | 92 | 1.006 |
| `statussection` | `write` | Write the script to a file. | 39 | 1.006 |

