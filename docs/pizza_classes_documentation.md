# Pizza Modules Documentation

Generated on: **2024-12-26 12:43:19**

<hr style="border: none; height: 1px; background-color: #e0e0e0;" />


## Configuration

To run Pizza3, ensure your Python environment is properly configured. This setup assumes that you are operating from the `Pizza3/` directory, which contains the `pizza/` and `doc/` folders. The main folder (`$mainfolder`) is set to the absolute path of the current directory.

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

## Module `pizza.__init__`

### Class Inheritance Diagram
```mermaid
graph TD;
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
ScriptTemplate
Sphere
USERSMD
Union
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
ulsph
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
emulsion --> coreshell
forcefield --> smd
generic --> USERSMD
none --> rigidwall
object --> CallableScript
object --> Collection
object --> Operation
object --> ScriptTemplate
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

## Module `pizza.data3`

### Class Inheritance Diagram
```mermaid
graph TD;
data
dump
object --> data
object --> dump
```

**[Class Examples for `pizza/data3.py` (1)](class_examples.html#pizza_data3)**

### Methods Table

| Class | Method | Docstring First Paragraph | # Lines | __version__ |
|-------|---------|---------------------------|---------|-------------|
| `data` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 138 | 0.99991 |
| `data` | `__repr__` | Return repr(self). | 26 | 0.99991 |
| `data` | `append` | append a new column: X.append("section",vectorofvalues,forceinteger=False,propertyname=None) | 37 | 0.99991 |
| `data` | `delete` |  | 8 | 0.99991 |
| `data` | `dispsection` | display section info: X.dispsection("sectionname") | 10 | 0.99991 |
| `data` | `findtime` |  | 4 | 0.99991 |
| `data` | `get` |  | 21 | 0.99991 |
| `data` | `iterator` |  | 4 | 0.99991 |
| `data` | `map` |  | 6 | 0.99991 |
| `data` | `maxbox` |  | 5 | 0.99991 |
| `data` | `maxtype` |  | 2 | 0.99991 |
| `data` | `newxyz` |  | 16 | 0.99991 |
| `data` | `reorder` | reorder columns: reorder("section",colidxfirst,colidxsecond,colidxthird,...) | 16 | 0.99991 |
| `data` | `replace` | replace column values: replace("section",columnindex,vectorofvalues) with columnindex=1..ncolumns | 20 | 0.99991 |
| `data` | `viz` |  | 61 | 0.99991 |
| `data` | `write` |  | 20 | 0.99991 |

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
| (module-level) | `autoname` | generate automatically names | 3 | 0.9972 |
| (module-level) | `remove_comments` | Removes comments from a single or multi-line string. Handles quotes and escaped characters. | 68 | 0.9972 |
| `dforcefield` | `__add__` | Concatenate dforcefield attributes, i | 38 | 0.9972 |
| `dforcefield` | `__contains__` | Check if an attribute exists in the dforcefield instance or its parameters. | 3 | 0.9972 |
| `dforcefield` | `__copy__` | Shallow copy method for dforcefield. | 15 | 0.9972 |
| `dforcefield` | `__deepcopy__` | Deep copy method for dforcefield. | 21 | 0.9972 |
| `dforcefield` | `__getattr__` | Shorthand for accessing parameters, base class attributes, or attributes in 'name' and 'description'. If an attribute exists in both 'name' and 'description', their contents are combined with a newline. | 28 | 0.9972 |
| `dforcefield` | `__hasattr__` | Check if an attribute exists in the dforcefield instance, class, parameters, or the base class. | 15 | 0.9972 |
| `dforcefield` | `__init__` | Initialize a dynamic forcefield with default or custom values. | 166 | 0.9972 |
| `dforcefield` | `__iter__` | Iterate over all keys, including those in the merged struct, parameters, and scalar attributes. | 11 | 0.9972 |
| `dforcefield` | `__len__` | Return the number of parameters in the forcefield. This will use the len method of parameters. | 6 | 0.9972 |
| `dforcefield` | `__or__` | Overload | pipe operator in dscript | 6 | 0.9972 |
| `dforcefield` | `__repr__` | Custom __repr__ method that indicates it is a dforcefield instance and provides information about the base class, name, and parameters dynamically. | 55 | 0.9972 |
| `dforcefield` | `__setattr__` | Shorthand for setting attributes. Attributes specific to dforcefield are handled separately. New attributes are added to parameters if they are not part of the dforcefield-specific attributes. | 27 | 0.9972 |
| `dforcefield` | `__str__` | Return str(self). | 3 | 0.9972 |
| `dforcefield` | `_inject_attributes` | Inject dforcefield attributes into the base class, bypassing __setattr__. | 22 | 0.9972 |
| `dforcefield` | `base_repr` | Returns the representation of the base_class. | 4 | 0.9972 |
| `dforcefield` | `combine_parameters` | Combine GLOBAL, LOCAL, and RULES to get the current parameter configuration. | 5 | 0.9972 |
| `dforcefield` | `compare` | Compare the current instance with another dforcefield instance, including RULES, GLOBAL, and LOCAL. | 142 | 0.9972 |
| `dforcefield` | `copy` | Create a new instance of dforcefield with the option to override key attributes including RULES, GLOBAL, and LOCAL. | 34 | 0.9972 |
| `dforcefield` | `detectVariables` | Detects variables in the form ${variable} from the outputs of pair_style, pair_diagcoeff, and pair_offdiagcoeff. | 30 | 0.9972 |
| `dforcefield` | `dispmax` | optimize display | 8 | 0.9972 |
| `dforcefield` | `get_global` | Return the GLOBAL parameters for this dforcefield instance. | 3 | 0.9972 |
| `dforcefield` | `get_local` | Return the LOCAL parameters for this dforcefield instance. | 3 | 0.9972 |
| `dforcefield` | `get_rules` | Return the RULES parameters for this dforcefield instance. | 3 | 0.9972 |
| `dforcefield` | `items` | Return an iterator over (key, value) pairs from the merged struct, parameters, and scalar attributes. | 16 | 0.9972 |
| `dforcefield` | `keys` | Return the keys of the merged struct, parameters, and scalar attributes. | 8 | 0.9972 |
| `dforcefield` | `missingVariables` | List missing variables (undefined in parameters). | 46 | 0.9972 |
| `dforcefield` | `pair_diagcoeff` | Delegate pair_diagcoeff to the base class, ensuring it uses the correct attributes. | 6 | 0.9972 |
| `dforcefield` | `pair_offdiagcoeff` | Delegate pair_offdiagcoeff to the base class, ensuring it uses the correct attributes. | 6 | 0.9972 |
| `dforcefield` | `pair_style` | Delegate pair_style to the base class, ensuring it uses the correct attributes. | 6 | 0.9972 |
| `dforcefield` | `reset` | Reset the dforcefield instance to its initial state, reapplying the default values including RULES, GLOBAL, and LOCAL. | 22 | 0.9972 |
| `dforcefield` | `save` | Save the dforcefield instance to a file with a header, formatted content, and the base_class. | 99 | 0.9972 |
| `dforcefield` | `scriptobject` | Method to return a scriptobject based on the current dforcefield instance. | 77 | 0.9972 |
| `dforcefield` | `set_global` | Update the GLOBAL parameters and adjust the combined parameters accordingly. | 17 | 0.9972 |
| `dforcefield` | `set_local` | Update the LOCAL parameters and adjust the combined parameters accordingly. | 17 | 0.9972 |
| `dforcefield` | `set_rules` | Update the RULES parameters and adjust the combined parameters accordingly. | 17 | 0.9972 |
| `dforcefield` | `show` | Show the corresponding base_class forcefield definition | 4 | 0.9972 |
| `dforcefield` | `to_dict` | Serialize the dforcefield instance to a dictionary, including RULES, GLOBAL, and LOCAL. | 24 | 0.9972 |
| `dforcefield` | `update` | Update multiple attributes of the dforcefield instance at once, including RULES, GLOBAL, and LOCAL. | 16 | 0.9972 |
| `dforcefield` | `update_parameters` | Update self.parameters by combining GLOBAL, LOCAL, RULES, and USER parameters. | 6 | 0.9972 |
| `dforcefield` | `validate` | Validate the dforcefield instance to ensure all required attributes are set. | 14 | 0.9972 |
| `dforcefield` | `values` | Return the values of the merged struct, parameters, and scalar attributes. | 8 | 0.9972 |

## Module `pizza.dscript`

### Class Inheritance Diagram
```mermaid
graph TD;
ScriptTemplate
dscript
lambdaScriptdata
lamdaScript
param
paramauto
pipescript
script
scriptdata
struct
object --> ScriptTemplate
object --> dscript
object --> pipescript
object --> script
object --> struct
param --> paramauto
param --> scriptdata
paramauto --> lambdaScriptdata
script --> lamdaScript
struct --> param
```

**[Class Examples for `pizza/dscript.py` (46)](class_examples.html#pizza_dscript)**

### Methods Table

| Class | Method | Docstring First Paragraph | # Lines | __version__ |
|-------|---------|---------------------------|---------|-------------|
| (module-level) | `autoname` | generate automatically names | 3 | 0.99991 |
| (module-level) | `get_metadata` | Return a dictionary of explicitly defined metadata. | 15 | 0.99991 |
| `ScriptTemplate` | `__getattr__` | Handles attribute retrieval, checking the following in order: 1. If 'name' is in default_attributes, return the value from attributes if it exists, otherwise return the default value from default_attributes. 2. If 'name' is 'content', return the content (or an empty string if content is not set). 3. If 'name' exists in the attributes dictionary, return its value. 4. If attributes itself exists in __dict__, return the value from attributes if 'name' is found. 5. If all previous checks fail, raise an AttributeError indicating that 'name' is not found. | 39 | 0.99991 |
| `ScriptTemplate` | `__init__` | Initializes a new `ScriptTemplate` object. | 96 | 0.99991 |
| `ScriptTemplate` | `__repr__` | Return repr(self). | 87 | 0.99991 |
| `ScriptTemplate` | `__setattr__` | Implement setattr(self, name, value). | 24 | 0.99991 |
| `ScriptTemplate` | `__str__` | Return str(self). | 3 | 0.99991 |
| `ScriptTemplate` | `_calculate_content_hash` | Generate hash for content. | 3 | 0.99991 |
| `ScriptTemplate` | `_invalidate_cache` | Reset all cache entries. | 10 | 0.99991 |
| `ScriptTemplate` | `_update_content` | Helper to set _content and _content_hash, refreshing cache as necessary. | 19 | 0.99991 |
| `ScriptTemplate` | `check_variables` | Checks for undefined variables in the ScriptTemplate instance. | 56 | 0.99991 |
| `ScriptTemplate` | `detect_variables` | Detects variables in the content of the template using the pattern r'\$\{(\w+)\}'. | 19 | 0.99991 |
| `ScriptTemplate` | `do` | Executes or prepares the script template content based on its attributes and the `softrun` flag. | 89 | 0.99991 |
| `ScriptTemplate` | `is_variable_defined` | Checks if a specified variable is defined (either as a default value or a set value). | 29 | 0.99991 |
| `ScriptTemplate` | `is_variable_set_value_only` | Checks if a specified variable is defined and set to a specific (non-default) value. | 31 | 0.99991 |
| `ScriptTemplate` | `refreshvar` | Detects variables in the content and adds them to definitions if needed. This method ensures that variables like ${varname} are correctly detected and added to the definitions if they are missing. | 14 | 0.99991 |
| `dscript` | `__add__` | Concatenates two dscript objects, creating a new dscript object that combines the TEMPLATE and DEFINITIONS of both. This operation avoids deep copying of definitions by creating a new lambdaScriptdata instance from the definitions. | 52 | 0.99991 |
| `dscript` | `__call__` | Extracts subobjects from the dscript based on the provided keys. | 35 | 0.99991 |
| `dscript` | `__contains__` |  | 2 | 0.99991 |
| `dscript` | `__copy__` | copy method | 6 | 0.99991 |
| `dscript` | `__deepcopy__` | deep copy method | 8 | 0.99991 |
| `dscript` | `__delitem__` |  | 2 | 0.99991 |
| `dscript` | `__getattr__` |  | 16 | 0.99991 |
| `dscript` | `__getitem__` | Implements index-based retrieval, slicing, or reordering for dscript objects. | 47 | 0.99991 |
| `dscript` | `__init__` | Initializes a new `dscript` object. | 65 | 0.99991 |
| `dscript` | `__iter__` |  | 2 | 0.99991 |
| `dscript` | `__len__` |  | 2 | 0.99991 |
| `dscript` | `__repr__` | Representation of dscript object with additional properties. | 20 | 0.99991 |
| `dscript` | `__setattr__` | Implement setattr(self, name, value). | 24 | 0.99991 |
| `dscript` | `__setitem__` |  | 7 | 0.99991 |
| `dscript` | `__str__` | Return str(self). | 4 | 0.99991 |
| `dscript` | `add_dynamic_script` | Add a dynamic script step to the dscript object. | 29 | 0.99991 |
| `dscript` | `check_all_variables` | Checks for undefined variables for each TEMPLATE key in the dscript object. | 38 | 0.99991 |
| `dscript` | `createEmptyVariables` | Creates empty variables in DEFINITIONS if they don't already exist. | 14 | 0.99991 |
| `dscript` | `detect_all_variables` | Detects all variables across all templates in the dscript object. | 20 | 0.99991 |
| `dscript` | `do` | Executes or previews all `ScriptTemplate` instances in `TEMPLATE`, concatenating their processed content. Allows for optional headers and footers based on verbosity settings, and offers a preliminary preview mode with `softrun`. Accumulates definitions across all templates if `return_definitions=True`. | 101 | 0.99991 |
| `dscript` | `generator` | Returns ------- STR generated code corresponding to dscript (using dscript syntax/language). | 9 | 0.99991 |
| `dscript` | `get_attributes_by_index` | Returns the attributes of the ScriptTemplate at the specified index. | 4 | 0.99991 |
| `dscript` | `get_content_by_index` | Returns the content of the ScriptTemplate at the specified index. | 45 | 0.99991 |
| `dscript` | `header` | Generate a formatted header for the DSCRIPT file. | 63 | 0.99991 |
| `dscript` | `items` |  | 2 | 0.99991 |
| `dscript` | `keys` | Return the keys of the TEMPLATE. | 3 | 0.99991 |
| `dscript` | `pipescript` | Returns a pipescript object by combining script objects corresponding to the given keys. | 69 | 0.99991 |
| `dscript` | `reorder` | Reorder the TEMPLATE lines according to a list of indices. | 10 | 0.99991 |
| `dscript` | `save` | Save the current script instance to a text file. | 268 | 0.99991 |
| `dscript` | `script` | returns the corresponding script | 10 | 0.99991 |
| `dscript` | `set_all_variables` | Ensures that all variables in the templates are added to the global definitions with default values if they are not already defined. | 11 | 0.99991 |
| `dscript` | `values` | Return the ScriptTemplate objects in TEMPLATE. | 3 | 0.99991 |
| `lambdaScriptdata` | `__init__` | Constructor for lambdaScriptdata. It forces the parent's _returnerror parameter to False. | 19 | 0.99991 |
| `lamdaScript` | `__init__` | Initialize a new `lambdaScript` instance. | 66 | 0.99991 |

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

**[Class Examples for `pizza/dump3.py` (1)](class_examples.html#pizza_dump3)**

### Methods Table

| Class | Method | Docstring First Paragraph | # Lines | __version__ |
|-------|---------|---------------------------|---------|-------------|
| `Frame` | `__eq__` | Return self==value. | 2 | 0.99991 |
| `Frame` | `__ge__` | Return self>=value. | 2 | 0.99991 |
| `Frame` | `__gt__` | Return self>value. | 2 | 0.99991 |
| `Frame` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 2 | 0.99991 |
| `Frame` | `__le__` | Return self<=value. | 2 | 0.99991 |
| `Frame` | `__lt__` | Return self<value. | 2 | 0.99991 |
| `Frame` | `__ne__` | Return self!=value. | 2 | 0.99991 |
| `Frame` | `__repr__` | Return repr(self). | 6 | 0.99991 |
| `Snap` | `__eq__` | Return self==value. | 2 | 0.99991 |
| `Snap` | `__ge__` | Return self>=value. | 2 | 0.99991 |
| `Snap` | `__gt__` | Return self>value. | 2 | 0.99991 |
| `Snap` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 2 | 0.99991 |
| `Snap` | `__le__` | Return self<=value. | 2 | 0.99991 |
| `Snap` | `__lt__` | Return self<value. | 2 | 0.99991 |
| `Snap` | `__ne__` | Return self!=value. | 2 | 0.99991 |
| `Snap` | `__repr__` | Return repr(self). | 3 | 0.99991 |
| `aselect` | `__init__` | private constructor (not to be used directly) | 3 | 0.99991 |
| `aselect` | `all` | select all atoms: aselect.all() aselect.all(timestep) | 20 | 0.99991 |
| `aselect` | `test` | " aselect.test(stringexpression [,timestep]) example: aselect.test("$y>0.4e-3 and $y<0.6e-3") | 71 | 0.99991 |
| `dump` | `__add__` | merge dump objects of the same kind/type | 8 | 0.99991 |
| `dump` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 31 | 0.99991 |
| `dump` | `__repr__` | Return repr(self). | 12 | 0.99991 |
| `dump` | `atom` |  | 29 | 0.99991 |
| `dump` | `clone` |  | 16 | 0.99991 |
| `dump` | `compare_atom` |  | 7 | 0.99991 |
| `dump` | `compare_time` |  | 7 | 0.99991 |
| `dump` | `cull` |  | 7 | 0.99991 |
| `dump` | `delete` |  | 11 | 0.99991 |
| `dump` | `extra` |  | 61 | 0.99991 |
| `dump` | `findtime` |  | 5 | 0.99991 |
| `dump` | `frame` | simplified class to access properties of a snapshot (INRAE\Olivier Vitrac) | 22 | 0.99991 |
| `dump` | `iterator` |  | 9 | 0.99991 |
| `dump` | `kind` | guessed kind of dump file based on column names (possibility to supply a personnalized list) (INRAE\Olivier Vitrac) | 31 | 0.99991 |
| `dump` | `map` |  | 6 | 0.99991 |
| `dump` | `maxbox` |  | 19 | 0.99991 |
| `dump` | `maxtype` |  | 13 | 0.99991 |
| `dump` | `minmax` |  | 16 | 0.99991 |
| `dump` | `names2str` |  | 13 | 0.99991 |
| `dump` | `newcolumn` |  | 12 | 0.99991 |
| `dump` | `next` |  | 40 | 0.99991 |
| `dump` | `owrap` |  | 30 | 0.99991 |
| `dump` | `read_all` |  | 53 | 0.99991 |
| `dump` | `read_snapshot` | low-level method to read a snapshot from a file identifier | 123 | 0.99991 |
| `dump` | `realtime` | time as simulated: realtime() | 10 | 0.99991 |
| `dump` | `scale` |  | 14 | 0.99991 |
| `dump` | `scale_one` |  | 49 | 0.99991 |
| `dump` | `scatter` |  | 42 | 0.99991 |
| `dump` | `set` |  | 22 | 0.99991 |
| `dump` | `setv` |  | 17 | 0.99991 |
| `dump` | `sort` |  | 17 | 0.99991 |
| `dump` | `sort_one` |  | 6 | 0.99991 |
| `dump` | `spread` |  | 24 | 0.99991 |
| `dump` | `time` | timestep as stored: time() | 10 | 0.99991 |
| `dump` | `unscale` |  | 14 | 0.99991 |
| `dump` | `unscale_one` |  | 39 | 0.99991 |
| `dump` | `unwrap` |  | 18 | 0.99991 |
| `dump` | `vecs` | vecs(timeste,columname1,columname2,...) Examples: tab = vecs(timestep,"id","x","y") tab = vecs(timestep,["id","x","y"],"z") X.vecs(X.time()[50],"vx","vy") | 35 | 0.99991 |
| `dump` | `viz` |  | 94 | 0.99991 |
| `dump` | `wrap` |  | 18 | 0.99991 |
| `dump` | `write` |  | 55 | 0.99991 |
| `tselect` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 2 | 0.99991 |
| `tselect` | `all` |  | 7 | 0.99991 |
| `tselect` | `none` |  | 6 | 0.99991 |
| `tselect` | `one` |  | 9 | 0.99991 |
| `tselect` | `skip` |  | 14 | 0.99991 |
| `tselect` | `test` |  | 19 | 0.99991 |

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
ulsph
water
forcefield --> smd
none --> rigidwall
object --> forcefield
object --> struct
param --> paramauto
paramauto --> parameterforcefield
smd --> none
smd --> tlsph
smd --> ulsph
struct --> param
tlsph --> saltTLSPH
tlsph --> solidfood
ulsph --> water
```

**[Class Examples for `pizza/forcefield.py` (1)](class_examples.html#pizza_forcefield)**

### Methods Table

| Class | Method | Docstring First Paragraph | # Lines | __version__ |
|-------|---------|---------------------------|---------|-------------|
| `forcefield` | `__repr__` | disp method | 21 | 0.9971 |
| `forcefield` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 0.9971 |
| `forcefield` | `pair_diagcoeff` | Generate and return the diagonal pair coefficients for the current forcefield instance. | 63 | 0.9971 |
| `forcefield` | `pair_offdiagcoeff` | Generate and return the off-diagonal pair coefficients for the current forcefield instance. | 87 | 0.9971 |
| `forcefield` | `pair_style` | Generate and return the pair style command for the current forcefield instance. | 58 | 0.9971 |
| `forcefield` | `printheader` | print header | 7 | 0.9971 |
| `none` | `__repr__` | disp method | 21 | 0.9971 |
| `none` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 0.9971 |
| `none` | `pair_diagcoeff` | Generate and return the diagonal pair coefficients for the current forcefield instance. | 63 | 0.9971 |
| `none` | `pair_offdiagcoeff` | Generate and return the off-diagonal pair coefficients for the current forcefield instance. | 87 | 0.9971 |
| `none` | `pair_style` | Generate and return the pair style command for the current forcefield instance. | 58 | 0.9971 |
| `none` | `printheader` | print header | 7 | 0.9971 |
| `parameterforcefield` | `__init__` | Constructor for parameterforcefield. It forces the parent's _returnerror parameter to False. | 19 | 0.9971 |
| `rigidwall` | `__init__` | rigidwall forcefield: rigidwall(beadtype=index, userid="mywall") | 12 | 0.9971 |
| `rigidwall` | `__repr__` | disp method | 21 | 0.9971 |
| `rigidwall` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 0.9971 |
| `rigidwall` | `pair_diagcoeff` | Generate and return the diagonal pair coefficients for the current forcefield instance. | 63 | 0.9971 |
| `rigidwall` | `pair_offdiagcoeff` | Generate and return the off-diagonal pair coefficients for the current forcefield instance. | 87 | 0.9971 |
| `rigidwall` | `pair_style` | Generate and return the pair style command for the current forcefield instance. | 58 | 0.9971 |
| `rigidwall` | `printheader` | print header | 7 | 0.9971 |
| `saltTLSPH` | `__init__` | saltTLSPH forcefield: saltTLSPH(beadtype=index, userid="salt") | 22 | 0.9971 |
| `saltTLSPH` | `__repr__` | disp method | 21 | 0.9971 |
| `saltTLSPH` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 0.9971 |
| `saltTLSPH` | `pair_diagcoeff` | Generate and return the diagonal pair coefficients for the current forcefield instance. | 63 | 0.9971 |
| `saltTLSPH` | `pair_offdiagcoeff` | Generate and return the off-diagonal pair coefficients for the current forcefield instance. | 87 | 0.9971 |
| `saltTLSPH` | `pair_style` | Generate and return the pair style command for the current forcefield instance. | 58 | 0.9971 |
| `saltTLSPH` | `printheader` | print header | 7 | 0.9971 |
| `smd` | `__repr__` | disp method | 21 | 0.9971 |
| `smd` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 0.9971 |
| `smd` | `pair_diagcoeff` | Generate and return the diagonal pair coefficients for the current forcefield instance. | 63 | 0.9971 |
| `smd` | `pair_offdiagcoeff` | Generate and return the off-diagonal pair coefficients for the current forcefield instance. | 87 | 0.9971 |
| `smd` | `pair_style` | Generate and return the pair style command for the current forcefield instance. | 58 | 0.9971 |
| `smd` | `printheader` | print header | 7 | 0.9971 |
| `solidfood` | `__init__` | food forcefield: solidfood(beadtype=index, userid="myfood") | 22 | 0.9971 |
| `solidfood` | `__repr__` | disp method | 21 | 0.9971 |
| `solidfood` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 0.9971 |
| `solidfood` | `pair_diagcoeff` | Generate and return the diagonal pair coefficients for the current forcefield instance. | 63 | 0.9971 |
| `solidfood` | `pair_offdiagcoeff` | Generate and return the off-diagonal pair coefficients for the current forcefield instance. | 87 | 0.9971 |
| `solidfood` | `pair_style` | Generate and return the pair style command for the current forcefield instance. | 58 | 0.9971 |
| `solidfood` | `printheader` | print header | 7 | 0.9971 |
| `tlsph` | `__repr__` | disp method | 21 | 0.9971 |
| `tlsph` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 0.9971 |
| `tlsph` | `pair_diagcoeff` | Generate and return the diagonal pair coefficients for the current forcefield instance. | 63 | 0.9971 |
| `tlsph` | `pair_offdiagcoeff` | Generate and return the off-diagonal pair coefficients for the current forcefield instance. | 87 | 0.9971 |
| `tlsph` | `pair_style` | Generate and return the pair style command for the current forcefield instance. | 58 | 0.9971 |
| `tlsph` | `printheader` | print header | 7 | 0.9971 |
| `ulsph` | `__repr__` | disp method | 21 | 0.9971 |
| `ulsph` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 0.9971 |
| `ulsph` | `pair_diagcoeff` | Generate and return the diagonal pair coefficients for the current forcefield instance. | 63 | 0.9971 |
| `ulsph` | `pair_offdiagcoeff` | Generate and return the off-diagonal pair coefficients for the current forcefield instance. | 87 | 0.9971 |
| `ulsph` | `pair_style` | Generate and return the pair style command for the current forcefield instance. | 58 | 0.9971 |
| `ulsph` | `printheader` | print header | 7 | 0.9971 |
| `water` | `__init__` | water forcefield: water(beadtype=index, userid="myfluid") | 16 | 0.9971 |
| `water` | `__repr__` | disp method | 21 | 0.9971 |
| `water` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 0.9971 |
| `water` | `pair_diagcoeff` | Generate and return the diagonal pair coefficients for the current forcefield instance. | 63 | 0.9971 |
| `water` | `pair_offdiagcoeff` | Generate and return the off-diagonal pair coefficients for the current forcefield instance. | 87 | 0.9971 |
| `water` | `pair_style` | Generate and return the pair style command for the current forcefield instance. | 58 | 0.9971 |
| `water` | `printheader` | print header | 7 | 0.9971 |

## Module `pizza.fork.region`

**Error importing module**: No module named 'pizza.private.struct'

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
| (module-level) | `format_table` | Formats a table with given headers and rows, truncating text based on maximum column widths and aligning content based on the specified alignment. | 82 | 0.9999 |
| (module-level) | `generate_random_name` |  | 3 | 0.9999 |
| (module-level) | `truncate_text` | Truncates the input text to fit within the specified maximum width. If the text is longer than `maxwidth`, it is shortened by keeping the beginning and trailing parts, separated by " [...] ". | 26 | 0.9999 |
| `Operation` | `__add__` | overload + as union | 3 | 0.9999 |
| `Operation` | `__init__` | Initializes a new Operation instance with given parameters. | 10 | 0.9999 |
| `Operation` | `__mul__` | overload * as intersect | 3 | 0.9999 |
| `Operation` | `__repr__` | detailed representation | 10 | 0.9999 |
| `Operation` | `__str__` | string representation | 18 | 0.9999 |
| `Operation` | `__sub__` | overload - as subtract | 3 | 0.9999 |
| `Operation` | `_operate` | Implements algebraic operations between self and other Operation instances. | 40 | 0.9999 |
| `Operation` | `append` | Appends a single operand to the operands list of the Operation instance. | 3 | 0.9999 |
| `Operation` | `extend` | Extends the operands list of the Operation instance with multiple operands. | 3 | 0.9999 |
| `Operation` | `generateID` | Generates an ID for the Operation instance based on its operands or name. | 8 | 0.9999 |
| `Operation` | `generate_hashname` | Generates an ID for the Operation instance based on its operands or name. | 9 | 0.9999 |
| `Operation` | `get_proper_operand` | Returns the proper operand depending on whether the operation is finalized. | 17 | 0.9999 |
| `Operation` | `is_empty` | Checks if the Operation instance has no operands. | 3 | 0.9999 |
| `Operation` | `is_unary` | Checks if the Operation instance has exactly one operand. | 3 | 0.9999 |
| `Operation` | `isfinalized` | Checks whether the Operation instance is finalized. Returns: - bool: True if the Operation is finalized, otherwise False. Functionality: - An Operation is considered finalized if its operator is not one of the algebraic operators '+', '-', '*'. | 10 | 0.9999 |
| `Operation` | `script` | Generate the LAMMPS code using the dscript and script classes. | 14 | 0.9999 |
| `group` | `__call__` | Allows subindexing of the group object using callable syntax with multiple keys. | 27 | 0.9999 |
| `group` | `__copy__` | copy method | 6 | 0.9999 |
| `group` | `__deepcopy__` | deep copy method | 8 | 0.9999 |
| `group` | `__getattr__` | Allows accessing operations via attribute-style notation. If the attribute is one of the core attributes, returns it directly. For other attributes, searches for an operation with a matching name in the _operations list. | 33 | 0.9999 |
| `group` | `__getitem__` | Enable shorthand for G.operations[G.find(operation_name)] using G[operation_name], or accessing operation by index using G[index]. | 18 | 0.9999 |
| `group` | `__init__` | Initializes a new instance of the group class. | 57 | 0.9999 |
| `group` | `__len__` | return the number of stored operations | 3 | 0.9999 |
| `group` | `__repr__` | Returns a neatly formatted table representation of the group's operations. | 28 | 0.9999 |
| `group` | `__setattr__` | Allows deletion of an operation via 'G.operation_name = []' after construction. During construction, attributes are set normally. | 20 | 0.9999 |
| `group` | `__str__` | Return str(self). | 2 | 0.9999 |
| `group` | `_get_subobject` | Retrieves a subobject based on the provided key. | 37 | 0.9999 |
| `group` | `add_group_criteria` | Adds group(s) using existing methods based on key-value pairs. | 36 | 0.9999 |
| `group` | `add_group_criteria_single` | Adds a single group based on criteria. | 99 | 0.9999 |
| `group` | `add_operation` | add an operation | 6 | 0.9999 |
| `group` | `byid` | select atoms by id and store them in group G.id(group_name,id_values) | 11 | 0.9999 |
| `group` | `byregion` | set a group of atoms based on a regionID G.region(group_name,regionID) | 9 | 0.9999 |
| `group` | `bytype` | select atoms by type and store them in group G.type(group_name,type_values) | 11 | 0.9999 |
| `group` | `byvariable` | Sets a group of atoms based on a variable. | 16 | 0.9999 |
| `group` | `clear` | clear group G.clear(group_name) | 9 | 0.9999 |
| `group` | `clearall` | clear all operations | 3 | 0.9999 |
| `group` | `code` | Joins the `code` attributes of all stored `operation` objects with ' '. | 5 | 0.9999 |
| `group` | `copy` | Copies a stored operation to a new operation with a different name. | 20 | 0.9999 |
| `group` | `count` | Generates DSCRIPT counters for specified groups with LAMMPS variable definitions and print commands. | 110 | 0.9999 |
| `group` | `create` | create group G.create(group_name) | 9 | 0.9999 |
| `group` | `create_groups` |  | 5 | 0.9999 |
| `group` | `delete` | Deletes one or more stored operations based on their names. | 41 | 0.9999 |
| `group` | `disp` | display the content of an operation | 7 | 0.9999 |
| `group` | `dscript` | Generates a dscript object containing the group's LAMMPS commands. | 24 | 0.9999 |
| `group` | `evaluate` | Evaluates the operation and stores the result in a new group. Expressions could combine +, - and * like o1+o2+o3-o4+o5+o6 | 65 | 0.9999 |
| `group` | `find` | Returns the index of an operation based on its name. | 7 | 0.9999 |
| `group` | `format_cell_content` |  | 7 | 0.9999 |
| `group` | `generate_group_definitions_from_collection` | Generates group definitions based on the collection of groupobject instances. | 15 | 0.9999 |
| `group` | `get_by_name` | Returns the operation matching "operation_name" Usage: group.get_by_name("operation_name") To be used by Operation, not by end-user, which should prefer getattr() | 10 | 0.9999 |
| `group` | `get_group_criteria` | Retrieve the criteria that define a group. Handles group_name as a string or number. | 33 | 0.9999 |
| `group` | `intersect` | Intersect group1, group2, group3 and store the result in group_name. Example usage: group.intersect(group_name, group1, group2, group3,...) | 10 | 0.9999 |
| `group` | `list` | return the list of all operations | 3 | 0.9999 |
| `group` | `operation_exists` | Returns true if "operation_name" exists To be used by Operation, not by end-user, which should prefer find() | 6 | 0.9999 |
| `group` | `pipescript` | Generates a pipescript object containing the group's LAMMPS commands. | 36 | 0.9999 |
| `group` | `reindex` | Change the index of a stored operation. | 19 | 0.9999 |
| `group` | `rename` | Rename a stored operation. | 22 | 0.9999 |
| `group` | `script` | Generates a script object containing the group's LAMMPS commands. | 19 | 0.9999 |
| `group` | `subtract` | Subtract group2, group3 from group1 and store the result in group_name. Example usage: group.subtract(group_name, group1, group2, group3,...) | 10 | 0.9999 |
| `group` | `union` | Union group1, group2, group3 and store the result in group_name. Example usage: group.union(group_name, group1, group2, group3,...) | 10 | 0.9999 |
| `group` | `variable` | Assigns an expression to a LAMMPS variable. | 19 | 0.9999 |
| `groupcollection` | `__add__` | Adds a `groupobject` or another `groupcollection` to this collection. | 19 | 0.9999 |
| `groupcollection` | `__getitem__` | Retrieves a `groupobject` by its index. | 14 | 0.9999 |
| `groupcollection` | `__iadd__` | In-place addition of a `groupobject` or a list/tuple of `groupobject` instances. | 23 | 0.9999 |
| `groupcollection` | `__init__` | Initializes a new instance of the groupcollection class. | 34 | 0.9999 |
| `groupcollection` | `__iter__` | Returns an iterator over the `groupobject` instances in the collection. | 8 | 0.9999 |
| `groupcollection` | `__len__` | Returns the number of `groupobject` instances in the collection. | 8 | 0.9999 |
| `groupcollection` | `__repr__` | Returns a neatly formatted string representation of the groupcollection. | 24 | 0.9999 |
| `groupcollection` | `__str__` | Returns the same representation as `__repr__`. | 8 | 0.9999 |
| `groupcollection` | `append` | Appends a `groupobject` to the collection. | 13 | 0.9999 |
| `groupcollection` | `clear` | Clears all `groupobject` instances from the collection. | 5 | 0.9999 |
| `groupcollection` | `extend` | Extends the collection with a list or tuple of `groupobject` instances. | 17 | 0.9999 |
| `groupcollection` | `mass` | Generates LAMMPS mass commands for each unique beadtype in the collection. | 71 | 0.9999 |
| `groupcollection` | `remove` | Removes a `groupobject` from the collection. | 11 | 0.9999 |
| `groupobject` | `__add__` | Adds this groupobject to another groupobject or a groupcollection. | 19 | 0.9999 |
| `groupobject` | `__init__` | Initializes a new instance of the groupobject class. | 34 | 0.9999 |
| `groupobject` | `__radd__` | Adds this groupobject to another groupobject or a groupcollection from the right. | 19 | 0.9999 |
| `groupobject` | `__repr__` | Returns an unambiguous string representation of the groupobject. | 8 | 0.9999 |
| `groupobject` | `__str__` | Returns a readable string representation of the groupobject. | 5 | 0.9999 |

## Module `pizza.private.mstruct`

### Class Inheritance Diagram
```mermaid
graph TD;
param
paramauto
pstr
struct
object --> struct
param --> paramauto
str --> pstr
struct --> param
```

**[Class Examples for `pizza/private/mstruct.py` (10)](class_examples.html#pizza_private_mstruct)**

### Methods Table

| Class | Method | Docstring First Paragraph | # Lines | __version__ |
|-------|---------|---------------------------|---------|-------------|
| `param` | `__add__` | add a structure set sortdefintions=True to sort definitions (to maintain executability) | 10 | 0.99991 |
| `param` | `__call__` | Extract a sub-structure based on the specified keys, keeping the same class type. | 35 | 0.99991 |
| `param` | `__contains__` | in override | 3 | 0.99991 |
| `param` | `__copy__` | copy method | 6 | 0.99991 |
| `param` | `__deepcopy__` | deep copy method | 8 | 0.99991 |
| `param` | `__delattr__` | Delete an instance attribute if it exists and is not a class or excluded attribute. | 10 | 0.99991 |
| `param` | `__getattr__` | get attribute override | 3 | 0.99991 |
| `param` | `__getitem__` | s[i] returns the ith element of the structure s[:4] returns a structure with the four first fields s[[1,3]] returns the second and fourth elements | 26 | 0.99991 |
| `param` | `__getstate__` | getstate for cooperative inheritance / duplication | 3 | 0.99991 |
| `param` | `__iadd__` | iadd a structure set sortdefintions=True to sort definitions (to maintain executability) | 9 | 0.99991 |
| `param` | `__init__` | constructor | 7 | 0.99991 |
| `param` | `__isub__` | isub a structure | 9 | 0.99991 |
| `param` | `__iter__` | struct iterator | 6 | 0.99991 |
| `param` | `__len__` | return the number of fields | 4 | 0.99991 |
| `param` | `__next__` | increment iterator | 7 | 0.99991 |
| `param` | `__repr__` | display method | 52 | 0.99991 |
| `param` | `__setattr__` | set attribute override | 3 | 0.99991 |
| `param` | `__setitem__` | set the ith element of the structure | 24 | 0.99991 |
| `param` | `__setstate__` | setstate for cooperative inheritance / duplication | 3 | 0.99991 |
| `param` | `__str__` | Return str(self). | 2 | 0.99991 |
| `param` | `__sub__` | sub a structure | 10 | 0.99991 |
| `param` | `check` | populate fields from a default structure check(defaultstruct) missing field, None and [] values are replaced by default ones | 19 | 0.99991 |
| `param` | `clear` | clear() delete all fields while preserving the original class | 3 | 0.99991 |
| `param` | `dict2struct` | create a structure from a dictionary | 8 | 0.99991 |
| `param` | `disp` | display method | 3 | 0.99991 |
| `param` | `dispmax` | optimize display | 8 | 0.99991 |
| `param` | `escape` | escape \${} as ${{}} --> keep variable names convert ${} as {} --> prepare Python replacement | 35 | 0.99991 |
| `param` | `eval` | Eval method for structure such as MS.alias | 79 | 0.99991 |
| `param` | `format` | format a string with field (use {field} as placeholders) s.replace(string), s.replace(string,escape=True) where: s is a struct object string is a string with possibly ${variable1} escape is a flag to prevent ${} replaced by {} | 27 | 0.99991 |
| `param` | `formateval` | format method with evaluation feature | 44 | 0.99991 |
| `param` | `fromkeys` | returns a structure from keys | 3 | 0.99991 |
| `param` | `fromkeysvalues` | struct.keysvalues(keys,values) creates a structure from keys and values use makeparam = True to create a param instead of struct | 18 | 0.99991 |
| `param` | `generator` | generate Python code of the equivalent structure | 21 | 0.99991 |
| `param` | `getattr` | Get attribute override to access both instance attributes and properties if allowed. | 11 | 0.99991 |
| `param` | `hasattr` | Return true if the field exists, considering properties as regular attributes if allowed. | 7 | 0.99991 |
| `param` | `isdefined` | isdefined(ref) returns true if it is defined in ref | 19 | 0.99991 |
| `param` | `isstrdefined` | isstrdefined(string,ref) returns true if it is defined in ref | 14 | 0.99991 |
| `param` | `isstrexpression` | isstrexpression(string) returns true if s contains an expression | 5 | 0.99991 |
| `param` | `items` | return all elements as iterable key, value | 3 | 0.99991 |
| `param` | `keys` | return the fields | 4 | 0.99991 |
| `param` | `keyssorted` | sort keys by length() | 5 | 0.99991 |
| `param` | `protect` | protect $variable as ${variable} | 11 | 0.99991 |
| `param` | `read` | read the equivalent structure read(filename) | 35 | 0.99991 |
| `param` | `scan` | scan(string) scan a string for variables | 11 | 0.99991 |
| `param` | `set` | initialization | 3 | 0.99991 |
| `param` | `setattr` | set field and value | 6 | 0.99991 |
| `param` | `sortdefinitions` | sortdefintions sorts all definitions so that they can be executed as param(). If any inconsistency is found, an error message is generated. | 53 | 0.99991 |
| `param` | `struct2dict` | create a dictionary from the current structure | 3 | 0.99991 |
| `param` | `struct2param` | convert an object struct() to param() | 8 | 0.99991 |
| `param` | `tostatic` | convert dynamic a param() object to a static struct() object. note: no interpretation note: use tostruct() to interpret them and convert it to struct note: tostatic().struct2param() makes it reversible | 7 | 0.99991 |
| `param` | `tostruct` | generate the evaluated structure tostruct(protection=False) | 6 | 0.99991 |
| `param` | `update` | Update multiple fields at once, while protecting certain attributes. | 22 | 0.99991 |
| `param` | `values` | return the values | 4 | 0.99991 |
| `param` | `write` | write the equivalent structure (not recursive for nested struct) write(filename, overwrite=True, mkdir=False) | 33 | 0.99991 |
| `param` | `zip` | zip keys and values | 3 | 0.99991 |
| `paramauto` | `__add__` | add a structure set sortdefintions=True to sort definitions (to maintain executability) | 2 | 0.99991 |
| `paramauto` | `__call__` | Extract a sub-structure based on the specified keys, keeping the same class type. | 35 | 0.99991 |
| `paramauto` | `__contains__` | in override | 3 | 0.99991 |
| `paramauto` | `__copy__` | copy method | 6 | 0.99991 |
| `paramauto` | `__deepcopy__` | deep copy method | 8 | 0.99991 |
| `paramauto` | `__delattr__` | Delete an instance attribute if it exists and is not a class or excluded attribute. | 10 | 0.99991 |
| `paramauto` | `__getattr__` | get attribute override | 3 | 0.99991 |
| `paramauto` | `__getitem__` | s[i] returns the ith element of the structure s[:4] returns a structure with the four first fields s[[1,3]] returns the second and fourth elements | 26 | 0.99991 |
| `paramauto` | `__getstate__` | getstate for cooperative inheritance / duplication | 3 | 0.99991 |
| `paramauto` | `__iadd__` | iadd a structure set sortdefintions=True to sort definitions (to maintain executability) | 2 | 0.99991 |
| `paramauto` | `__init__` | constructor | 7 | 0.99991 |
| `paramauto` | `__isub__` | isub a structure | 9 | 0.99991 |
| `paramauto` | `__iter__` | struct iterator | 6 | 0.99991 |
| `paramauto` | `__len__` | return the number of fields | 4 | 0.99991 |
| `paramauto` | `__next__` | increment iterator | 7 | 0.99991 |
| `paramauto` | `__repr__` | display method | 5 | 0.99991 |
| `paramauto` | `__setattr__` | set attribute override | 3 | 0.99991 |
| `paramauto` | `__setitem__` | set the ith element of the structure | 24 | 0.99991 |
| `paramauto` | `__setstate__` | setstate for cooperative inheritance / duplication | 3 | 0.99991 |
| `paramauto` | `__str__` | Return str(self). | 2 | 0.99991 |
| `paramauto` | `__sub__` | sub a structure | 10 | 0.99991 |
| `paramauto` | `check` | populate fields from a default structure check(defaultstruct) missing field, None and [] values are replaced by default ones | 19 | 0.99991 |
| `paramauto` | `clear` | clear() delete all fields while preserving the original class | 3 | 0.99991 |
| `paramauto` | `dict2struct` | create a structure from a dictionary | 8 | 0.99991 |
| `paramauto` | `disp` | display method | 3 | 0.99991 |
| `paramauto` | `dispmax` | optimize display | 8 | 0.99991 |
| `paramauto` | `escape` | escape \${} as ${{}} --> keep variable names convert ${} as {} --> prepare Python replacement | 35 | 0.99991 |
| `paramauto` | `eval` | Eval method for structure such as MS.alias | 79 | 0.99991 |
| `paramauto` | `format` | format a string with field (use {field} as placeholders) s.replace(string), s.replace(string,escape=True) where: s is a struct object string is a string with possibly ${variable1} escape is a flag to prevent ${} replaced by {} | 27 | 0.99991 |
| `paramauto` | `formateval` | format method with evaluation feature | 44 | 0.99991 |
| `paramauto` | `fromkeys` | returns a structure from keys | 3 | 0.99991 |
| `paramauto` | `fromkeysvalues` | struct.keysvalues(keys,values) creates a structure from keys and values use makeparam = True to create a param instead of struct | 18 | 0.99991 |
| `paramauto` | `generator` | generate Python code of the equivalent structure | 21 | 0.99991 |
| `paramauto` | `getattr` | Get attribute override to access both instance attributes and properties if allowed. | 11 | 0.99991 |
| `paramauto` | `hasattr` | Return true if the field exists, considering properties as regular attributes if allowed. | 7 | 0.99991 |
| `paramauto` | `isdefined` | isdefined(ref) returns true if it is defined in ref | 19 | 0.99991 |
| `paramauto` | `isstrdefined` | isstrdefined(string,ref) returns true if it is defined in ref | 14 | 0.99991 |
| `paramauto` | `isstrexpression` | isstrexpression(string) returns true if s contains an expression | 5 | 0.99991 |
| `paramauto` | `items` | return all elements as iterable key, value | 3 | 0.99991 |
| `paramauto` | `keys` | return the fields | 4 | 0.99991 |
| `paramauto` | `keyssorted` | sort keys by length() | 5 | 0.99991 |
| `paramauto` | `protect` | protect $variable as ${variable} | 11 | 0.99991 |
| `paramauto` | `read` | read the equivalent structure read(filename) | 35 | 0.99991 |
| `paramauto` | `scan` | scan(string) scan a string for variables | 11 | 0.99991 |
| `paramauto` | `set` | initialization | 3 | 0.99991 |
| `paramauto` | `setattr` | set field and value | 6 | 0.99991 |
| `paramauto` | `sortdefinitions` | sortdefintions sorts all definitions so that they can be executed as param(). If any inconsistency is found, an error message is generated. | 53 | 0.99991 |
| `paramauto` | `struct2dict` | create a dictionary from the current structure | 3 | 0.99991 |
| `paramauto` | `struct2param` | convert an object struct() to param() | 8 | 0.99991 |
| `paramauto` | `tostatic` | convert dynamic a param() object to a static struct() object. note: no interpretation note: use tostruct() to interpret them and convert it to struct note: tostatic().struct2param() makes it reversible | 7 | 0.99991 |
| `paramauto` | `tostruct` | generate the evaluated structure tostruct(protection=False) | 6 | 0.99991 |
| `paramauto` | `update` | Update multiple fields at once, while protecting certain attributes. | 22 | 0.99991 |
| `paramauto` | `values` | return the values | 4 | 0.99991 |
| `paramauto` | `write` | write the equivalent structure (not recursive for nested struct) write(filename, overwrite=True, mkdir=False) | 33 | 0.99991 |
| `paramauto` | `zip` | zip keys and values | 3 | 0.99991 |
| `pstr` | `__add__` | Return self+value. | 2 | 0.99991 |
| `pstr` | `__iadd__` |  | 2 | 0.99991 |
| `pstr` | `__repr__` | Return repr(self). | 5 | 0.99991 |
| `pstr` | `__truediv__` | overload / | 7 | 0.99991 |
| `pstr` | `eval` | evaluate the path of it os a path | 9 | 0.99991 |
| `pstr` | `topath` | return a validated path | 6 | 0.99991 |
| `struct` | `__add__` | add a structure set sortdefintions=True to sort definitions (to maintain executability) | 10 | 0.99991 |
| `struct` | `__call__` | Extract a sub-structure based on the specified keys, keeping the same class type. | 35 | 0.99991 |
| `struct` | `__contains__` | in override | 3 | 0.99991 |
| `struct` | `__copy__` | copy method | 6 | 0.99991 |
| `struct` | `__deepcopy__` | deep copy method | 8 | 0.99991 |
| `struct` | `__delattr__` | Delete an instance attribute if it exists and is not a class or excluded attribute. | 10 | 0.99991 |
| `struct` | `__getattr__` | get attribute override | 3 | 0.99991 |
| `struct` | `__getitem__` | s[i] returns the ith element of the structure s[:4] returns a structure with the four first fields s[[1,3]] returns the second and fourth elements | 26 | 0.99991 |
| `struct` | `__getstate__` | getstate for cooperative inheritance / duplication | 3 | 0.99991 |
| `struct` | `__iadd__` | iadd a structure set sortdefintions=True to sort definitions (to maintain executability) | 9 | 0.99991 |
| `struct` | `__init__` | constructor | 5 | 0.99991 |
| `struct` | `__isub__` | isub a structure | 9 | 0.99991 |
| `struct` | `__iter__` | struct iterator | 6 | 0.99991 |
| `struct` | `__len__` | return the number of fields | 4 | 0.99991 |
| `struct` | `__next__` | increment iterator | 7 | 0.99991 |
| `struct` | `__repr__` | display method | 52 | 0.99991 |
| `struct` | `__setattr__` | set attribute override | 3 | 0.99991 |
| `struct` | `__setitem__` | set the ith element of the structure | 24 | 0.99991 |
| `struct` | `__setstate__` | setstate for cooperative inheritance / duplication | 3 | 0.99991 |
| `struct` | `__str__` | Return str(self). | 2 | 0.99991 |
| `struct` | `__sub__` | sub a structure | 10 | 0.99991 |
| `struct` | `check` | populate fields from a default structure check(defaultstruct) missing field, None and [] values are replaced by default ones | 19 | 0.99991 |
| `struct` | `clear` | clear() delete all fields while preserving the original class | 3 | 0.99991 |
| `struct` | `dict2struct` | create a structure from a dictionary | 8 | 0.99991 |
| `struct` | `disp` | display method | 3 | 0.99991 |
| `struct` | `dispmax` | optimize display | 8 | 0.99991 |
| `struct` | `format` | format a string with field (use {field} as placeholders) s.replace(string), s.replace(string,escape=True) where: s is a struct object string is a string with possibly ${variable1} escape is a flag to prevent ${} replaced by {} | 27 | 0.99991 |
| `struct` | `fromkeys` | returns a structure from keys | 3 | 0.99991 |
| `struct` | `fromkeysvalues` | struct.keysvalues(keys,values) creates a structure from keys and values use makeparam = True to create a param instead of struct | 18 | 0.99991 |
| `struct` | `generator` | generate Python code of the equivalent structure | 21 | 0.99991 |
| `struct` | `getattr` | Get attribute override to access both instance attributes and properties if allowed. | 11 | 0.99991 |
| `struct` | `hasattr` | Return true if the field exists, considering properties as regular attributes if allowed. | 7 | 0.99991 |
| `struct` | `isdefined` | isdefined(ref) returns true if it is defined in ref | 19 | 0.99991 |
| `struct` | `isstrdefined` | isstrdefined(string,ref) returns true if it is defined in ref | 14 | 0.99991 |
| `struct` | `isstrexpression` | isstrexpression(string) returns true if s contains an expression | 5 | 0.99991 |
| `struct` | `items` | return all elements as iterable key, value | 3 | 0.99991 |
| `struct` | `keys` | return the fields | 4 | 0.99991 |
| `struct` | `keyssorted` | sort keys by length() | 5 | 0.99991 |
| `struct` | `read` | read the equivalent structure read(filename) | 35 | 0.99991 |
| `struct` | `scan` | scan(string) scan a string for variables | 11 | 0.99991 |
| `struct` | `set` | initialization | 3 | 0.99991 |
| `struct` | `setattr` | set field and value | 6 | 0.99991 |
| `struct` | `sortdefinitions` | sortdefintions sorts all definitions so that they can be executed as param(). If any inconsistency is found, an error message is generated. | 53 | 0.99991 |
| `struct` | `struct2dict` | create a dictionary from the current structure | 3 | 0.99991 |
| `struct` | `struct2param` | convert an object struct() to param() | 8 | 0.99991 |
| `struct` | `update` | Update multiple fields at once, while protecting certain attributes. | 22 | 0.99991 |
| `struct` | `values` | return the values | 4 | 0.99991 |
| `struct` | `write` | write the equivalent structure (not recursive for nested struct) write(filename, overwrite=True, mkdir=False) | 33 | 0.99991 |
| `struct` | `zip` | zip keys and values | 3 | 0.99991 |

## Module `pizza.private.utils`

*No classes found in this module.*

**[Class Examples for `pizza/private/utils.py` (1)](class_examples.html#pizza_private_utils)**

### Methods Table

| Class | Method | Docstring First Paragraph | # Lines | __version__ |
|-------|---------|---------------------------|---------|-------------|
| (module-level) | `list` | list folders and files | 7 |  |
| (module-level) | `replaceall` | replaceall("some_dir", "find this", "replace with this", "*.txt") | 34 |  |
| (module-level) | `updatepptx` | update PPTX | 22 |  |

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
| `collection` | `__init__` | constructor | 11 | 0.99991 |
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

## Module `pizza.region`

### Class Inheritance Diagram
```mermaid
graph TD;
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
ulsph
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
forcefield --> smd
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
| (module-level) | `<lambda>` |  | 1 | 0.99991 |
| (module-level) | `<lambda>` |  | 7 | 0.99991 |
| `Block` | `__add__` | overload addition ("+") operator | 19 | 0.99991 |
| `Block` | `__copy__` | copy method | 6 | 0.99991 |
| `Block` | `__deepcopy__` | deep copy method | 8 | 0.99991 |
| `Block` | `__getstate__` | getstate for cooperative inheritance / duplication | 3 | 0.99991 |
| `Block` | `__iadd__` | overload iaddition ("+=") operator | 16 | 0.99991 |
| `Block` | `__init__` | constructor of the generic core geometry USER: any definitions requires by the geometry VARIABLES: variables used to define the geometry (to be used in LAMMPS) hasgroup, hasmove: flag to force the sections group and move SECTIONS: they must be PIZZA.script | 24 | 0.99991 |
| `Block` | `__or__` | overload | pipe | 19 | 0.99991 |
| `Block` | `__repr__` | display method | 24 | 0.99991 |
| `Block` | `__setstate__` | setstate for cooperative inheritance / duplication | 3 | 0.99991 |
| `Block` | `copy` | returns a copy of the graphical object | 11 | 0.99991 |
| `Block` | `creategroup` | force the group creation in script | 3 | 0.99991 |
| `Block` | `createmove` | force the fix move creation in script | 3 | 0.99991 |
| `Block` | `do` | generates a script | 6 | 0.99991 |
| `Block` | `fixmoveargs` | Validates all arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) the result is adictionary, all fixmove can be combined | 18 | 0.99991 |
| `Block` | `fixmoveargvalidator` | Validation of arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) | 39 | 0.99991 |
| `Block` | `get_fixmovesyntax` | Returns the syntax for LAMMPS command, or detailed explanation for a specific argument type | 39 | 0.99991 |
| `Block` | `movearg` | Validation of move arguments for region command (https://docs.lammps.org/region.html) move args = v_x v_y v_z v_x,v_y,v_z = equal-style variables for x,y,z displacement of region over time (distance units) | 39 | 0.99991 |
| `Block` | `openarg` | Validation of open arguments for region command (https://docs.lammps.org/region.html) open value = integer from 1-6 corresponding to face index (see below) The indices specified as part of the open keyword have the following meanings: | 32 | 0.99991 |
| `Block` | `removegroup` | force the group creation in script | 3 | 0.99991 |
| `Block` | `removemove` | force the fix move creation in script | 3 | 0.99991 |
| `Block` | `rotatearg` | Validation of rotate arguments for region command (https://docs.lammps.org/region.html) rotate args = v_theta Px Py Pz Rx Ry Rz v_theta = equal-style variable for rotaton of region over time (in radians) Px,Py,Pz = origin for axis of rotation (distance units) Rx,Ry,Rz = axis of rotation vector | 36 | 0.99991 |
| `Block` | `scriptobject` | Method to return a scriptobject based on region instead of an input file Syntax similar to script.scriptobject OBJ = scriptobject(...) Implemented properties: beadtype=1,2,... name="short name" fullname = "comprehensive name" style = "smd" forcefield = any valid forcefield instance (default = rigidwall()) | 34 | 0.99991 |
| `Block` | `setgroup` | force the group creation in script | 3 | 0.99991 |
| `Block` | `sidearg` | Validation of side arguments for region command (https://docs.lammps.org/region.html) side value = in or out in = the region is inside the specified geometry out = the region is outside the specified geometry | 20 | 0.99991 |
| `Block` | `unitsarg` | Validation for units arguments for region command (https://docs.lammps.org/region.html) units value = lattice or box lattice = the geometry is defined in lattice units box = the geometry is defined in simulation box units | 20 | 0.99991 |
| `Block` | `update` | update the USER content for all three scripts | 14 | 0.99991 |
| `Block` | `volume` | Calculate the volume of the block based on USER.args | 24 | 0.99991 |
| `Collection` | `__getattr__` | get attribute override | 3 | 0.99991 |
| `Collection` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 26 | 0.99991 |
| `Collection` | `__len__` | return length of collection | 3 | 0.99991 |
| `Collection` | `__repr__` | Return repr(self). | 14 | 0.99991 |
| `Collection` | `creategroup` | force the group creation in script | 5 | 0.99991 |
| `Collection` | `get` | returns the object | 8 | 0.99991 |
| `Collection` | `group` | return the grouped coregeometry object | 13 | 0.99991 |
| `Collection` | `list` | return the list of objects | 3 | 0.99991 |
| `Collection` | `removegroup` | force the group creation in script | 5 | 0.99991 |
| `Collection` | `update` | update the USER content for the script | 6 | 0.99991 |
| `Cone` | `__add__` | overload addition ("+") operator | 19 | 0.99991 |
| `Cone` | `__copy__` | copy method | 6 | 0.99991 |
| `Cone` | `__deepcopy__` | deep copy method | 8 | 0.99991 |
| `Cone` | `__getstate__` | getstate for cooperative inheritance / duplication | 3 | 0.99991 |
| `Cone` | `__iadd__` | overload iaddition ("+=") operator | 16 | 0.99991 |
| `Cone` | `__init__` | constructor of the generic core geometry USER: any definitions requires by the geometry VARIABLES: variables used to define the geometry (to be used in LAMMPS) hasgroup, hasmove: flag to force the sections group and move SECTIONS: they must be PIZZA.script | 23 | 0.99991 |
| `Cone` | `__or__` | overload | pipe | 19 | 0.99991 |
| `Cone` | `__repr__` | display method | 24 | 0.99991 |
| `Cone` | `__setstate__` | setstate for cooperative inheritance / duplication | 3 | 0.99991 |
| `Cone` | `copy` | returns a copy of the graphical object | 11 | 0.99991 |
| `Cone` | `creategroup` | force the group creation in script | 3 | 0.99991 |
| `Cone` | `createmove` | force the fix move creation in script | 3 | 0.99991 |
| `Cone` | `do` | generates a script | 6 | 0.99991 |
| `Cone` | `fixmoveargs` | Validates all arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) the result is adictionary, all fixmove can be combined | 18 | 0.99991 |
| `Cone` | `fixmoveargvalidator` | Validation of arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) | 39 | 0.99991 |
| `Cone` | `get_fixmovesyntax` | Returns the syntax for LAMMPS command, or detailed explanation for a specific argument type | 39 | 0.99991 |
| `Cone` | `movearg` | Validation of move arguments for region command (https://docs.lammps.org/region.html) move args = v_x v_y v_z v_x,v_y,v_z = equal-style variables for x,y,z displacement of region over time (distance units) | 39 | 0.99991 |
| `Cone` | `openarg` | Validation of open arguments for region command (https://docs.lammps.org/region.html) open value = integer from 1-6 corresponding to face index (see below) The indices specified as part of the open keyword have the following meanings: | 32 | 0.99991 |
| `Cone` | `removegroup` | force the group creation in script | 3 | 0.99991 |
| `Cone` | `removemove` | force the fix move creation in script | 3 | 0.99991 |
| `Cone` | `rotatearg` | Validation of rotate arguments for region command (https://docs.lammps.org/region.html) rotate args = v_theta Px Py Pz Rx Ry Rz v_theta = equal-style variable for rotaton of region over time (in radians) Px,Py,Pz = origin for axis of rotation (distance units) Rx,Ry,Rz = axis of rotation vector | 36 | 0.99991 |
| `Cone` | `scriptobject` | Method to return a scriptobject based on region instead of an input file Syntax similar to script.scriptobject OBJ = scriptobject(...) Implemented properties: beadtype=1,2,... name="short name" fullname = "comprehensive name" style = "smd" forcefield = any valid forcefield instance (default = rigidwall()) | 34 | 0.99991 |
| `Cone` | `setgroup` | force the group creation in script | 3 | 0.99991 |
| `Cone` | `sidearg` | Validation of side arguments for region command (https://docs.lammps.org/region.html) side value = in or out in = the region is inside the specified geometry out = the region is outside the specified geometry | 20 | 0.99991 |
| `Cone` | `unitsarg` | Validation for units arguments for region command (https://docs.lammps.org/region.html) units value = lattice or box lattice = the geometry is defined in lattice units box = the geometry is defined in simulation box units | 20 | 0.99991 |
| `Cone` | `update` | update the USER content for all three scripts | 14 | 0.99991 |
| `Cone` | `volume` | Calculate the volume of the cone based on USER.args | 21 | 0.99991 |
| `Cylinder` | `__add__` | overload addition ("+") operator | 19 | 0.99991 |
| `Cylinder` | `__copy__` | copy method | 6 | 0.99991 |
| `Cylinder` | `__deepcopy__` | deep copy method | 8 | 0.99991 |
| `Cylinder` | `__getstate__` | getstate for cooperative inheritance / duplication | 3 | 0.99991 |
| `Cylinder` | `__iadd__` | overload iaddition ("+=") operator | 16 | 0.99991 |
| `Cylinder` | `__init__` | constructor of the generic core geometry USER: any definitions requires by the geometry VARIABLES: variables used to define the geometry (to be used in LAMMPS) hasgroup, hasmove: flag to force the sections group and move SECTIONS: they must be PIZZA.script | 23 | 0.99991 |
| `Cylinder` | `__or__` | overload | pipe | 19 | 0.99991 |
| `Cylinder` | `__repr__` | display method | 24 | 0.99991 |
| `Cylinder` | `__setstate__` | setstate for cooperative inheritance / duplication | 3 | 0.99991 |
| `Cylinder` | `copy` | returns a copy of the graphical object | 11 | 0.99991 |
| `Cylinder` | `creategroup` | force the group creation in script | 3 | 0.99991 |
| `Cylinder` | `createmove` | force the fix move creation in script | 3 | 0.99991 |
| `Cylinder` | `do` | generates a script | 6 | 0.99991 |
| `Cylinder` | `fixmoveargs` | Validates all arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) the result is adictionary, all fixmove can be combined | 18 | 0.99991 |
| `Cylinder` | `fixmoveargvalidator` | Validation of arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) | 39 | 0.99991 |
| `Cylinder` | `get_fixmovesyntax` | Returns the syntax for LAMMPS command, or detailed explanation for a specific argument type | 39 | 0.99991 |
| `Cylinder` | `movearg` | Validation of move arguments for region command (https://docs.lammps.org/region.html) move args = v_x v_y v_z v_x,v_y,v_z = equal-style variables for x,y,z displacement of region over time (distance units) | 39 | 0.99991 |
| `Cylinder` | `openarg` | Validation of open arguments for region command (https://docs.lammps.org/region.html) open value = integer from 1-6 corresponding to face index (see below) The indices specified as part of the open keyword have the following meanings: | 32 | 0.99991 |
| `Cylinder` | `removegroup` | force the group creation in script | 3 | 0.99991 |
| `Cylinder` | `removemove` | force the fix move creation in script | 3 | 0.99991 |
| `Cylinder` | `rotatearg` | Validation of rotate arguments for region command (https://docs.lammps.org/region.html) rotate args = v_theta Px Py Pz Rx Ry Rz v_theta = equal-style variable for rotaton of region over time (in radians) Px,Py,Pz = origin for axis of rotation (distance units) Rx,Ry,Rz = axis of rotation vector | 36 | 0.99991 |
| `Cylinder` | `scriptobject` | Method to return a scriptobject based on region instead of an input file Syntax similar to script.scriptobject OBJ = scriptobject(...) Implemented properties: beadtype=1,2,... name="short name" fullname = "comprehensive name" style = "smd" forcefield = any valid forcefield instance (default = rigidwall()) | 34 | 0.99991 |
| `Cylinder` | `setgroup` | force the group creation in script | 3 | 0.99991 |
| `Cylinder` | `sidearg` | Validation of side arguments for region command (https://docs.lammps.org/region.html) side value = in or out in = the region is inside the specified geometry out = the region is outside the specified geometry | 20 | 0.99991 |
| `Cylinder` | `unitsarg` | Validation for units arguments for region command (https://docs.lammps.org/region.html) units value = lattice or box lattice = the geometry is defined in lattice units box = the geometry is defined in simulation box units | 20 | 0.99991 |
| `Cylinder` | `update` | update the USER content for all three scripts | 14 | 0.99991 |
| `Cylinder` | `volume` | Calculate the volume of the cylinder based on USER.args | 17 | 0.99991 |
| `Ellipsoid` | `__add__` | overload addition ("+") operator | 19 | 0.99991 |
| `Ellipsoid` | `__copy__` | copy method | 6 | 0.99991 |
| `Ellipsoid` | `__deepcopy__` | deep copy method | 8 | 0.99991 |
| `Ellipsoid` | `__getstate__` | getstate for cooperative inheritance / duplication | 3 | 0.99991 |
| `Ellipsoid` | `__iadd__` | overload iaddition ("+=") operator | 16 | 0.99991 |
| `Ellipsoid` | `__init__` | constructor of the generic core geometry USER: any definitions requires by the geometry VARIABLES: variables used to define the geometry (to be used in LAMMPS) hasgroup, hasmove: flag to force the sections group and move SECTIONS: they must be PIZZA.script | 23 | 0.99991 |
| `Ellipsoid` | `__or__` | overload | pipe | 19 | 0.99991 |
| `Ellipsoid` | `__repr__` | display method | 24 | 0.99991 |
| `Ellipsoid` | `__setstate__` | setstate for cooperative inheritance / duplication | 3 | 0.99991 |
| `Ellipsoid` | `copy` | returns a copy of the graphical object | 11 | 0.99991 |
| `Ellipsoid` | `creategroup` | force the group creation in script | 3 | 0.99991 |
| `Ellipsoid` | `createmove` | force the fix move creation in script | 3 | 0.99991 |
| `Ellipsoid` | `do` | generates a script | 6 | 0.99991 |
| `Ellipsoid` | `fixmoveargs` | Validates all arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) the result is adictionary, all fixmove can be combined | 18 | 0.99991 |
| `Ellipsoid` | `fixmoveargvalidator` | Validation of arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) | 39 | 0.99991 |
| `Ellipsoid` | `get_fixmovesyntax` | Returns the syntax for LAMMPS command, or detailed explanation for a specific argument type | 39 | 0.99991 |
| `Ellipsoid` | `movearg` | Validation of move arguments for region command (https://docs.lammps.org/region.html) move args = v_x v_y v_z v_x,v_y,v_z = equal-style variables for x,y,z displacement of region over time (distance units) | 39 | 0.99991 |
| `Ellipsoid` | `openarg` | Validation of open arguments for region command (https://docs.lammps.org/region.html) open value = integer from 1-6 corresponding to face index (see below) The indices specified as part of the open keyword have the following meanings: | 32 | 0.99991 |
| `Ellipsoid` | `removegroup` | force the group creation in script | 3 | 0.99991 |
| `Ellipsoid` | `removemove` | force the fix move creation in script | 3 | 0.99991 |
| `Ellipsoid` | `rotatearg` | Validation of rotate arguments for region command (https://docs.lammps.org/region.html) rotate args = v_theta Px Py Pz Rx Ry Rz v_theta = equal-style variable for rotaton of region over time (in radians) Px,Py,Pz = origin for axis of rotation (distance units) Rx,Ry,Rz = axis of rotation vector | 36 | 0.99991 |
| `Ellipsoid` | `scriptobject` | Method to return a scriptobject based on region instead of an input file Syntax similar to script.scriptobject OBJ = scriptobject(...) Implemented properties: beadtype=1,2,... name="short name" fullname = "comprehensive name" style = "smd" forcefield = any valid forcefield instance (default = rigidwall()) | 34 | 0.99991 |
| `Ellipsoid` | `setgroup` | force the group creation in script | 3 | 0.99991 |
| `Ellipsoid` | `sidearg` | Validation of side arguments for region command (https://docs.lammps.org/region.html) side value = in or out in = the region is inside the specified geometry out = the region is outside the specified geometry | 20 | 0.99991 |
| `Ellipsoid` | `unitsarg` | Validation for units arguments for region command (https://docs.lammps.org/region.html) units value = lattice or box lattice = the geometry is defined in lattice units box = the geometry is defined in simulation box units | 20 | 0.99991 |
| `Ellipsoid` | `update` | update the USER content for all three scripts | 14 | 0.99991 |
| `Ellipsoid` | `volume` | Calculate the volume of the ellipsoid based on USER.args | 15 | 0.99991 |
| `Evalgeometry` | `__add__` | overload addition ("+") operator | 19 | 0.99991 |
| `Evalgeometry` | `__copy__` | copy method | 6 | 0.99991 |
| `Evalgeometry` | `__deepcopy__` | deep copy method | 8 | 0.99991 |
| `Evalgeometry` | `__getstate__` | getstate for cooperative inheritance / duplication | 3 | 0.99991 |
| `Evalgeometry` | `__iadd__` | overload iaddition ("+=") operator | 16 | 0.99991 |
| `Evalgeometry` | `__init__` | constructor of the generic core geometry USER: any definitions requires by the geometry VARIABLES: variables used to define the geometry (to be used in LAMMPS) hasgroup, hasmove: flag to force the sections group and move SECTIONS: they must be PIZZA.script | 9 | 0.99991 |
| `Evalgeometry` | `__or__` | overload | pipe | 19 | 0.99991 |
| `Evalgeometry` | `__repr__` | display method | 24 | 0.99991 |
| `Evalgeometry` | `__setstate__` | setstate for cooperative inheritance / duplication | 3 | 0.99991 |
| `Evalgeometry` | `copy` | returns a copy of the graphical object | 11 | 0.99991 |
| `Evalgeometry` | `creategroup` | force the group creation in script | 3 | 0.99991 |
| `Evalgeometry` | `createmove` | force the fix move creation in script | 3 | 0.99991 |
| `Evalgeometry` | `do` | generates a script | 6 | 0.99991 |
| `Evalgeometry` | `fixmoveargs` | Validates all arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) the result is adictionary, all fixmove can be combined | 18 | 0.99991 |
| `Evalgeometry` | `fixmoveargvalidator` | Validation of arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) | 39 | 0.99991 |
| `Evalgeometry` | `get_fixmovesyntax` | Returns the syntax for LAMMPS command, or detailed explanation for a specific argument type | 39 | 0.99991 |
| `Evalgeometry` | `movearg` | Validation of move arguments for region command (https://docs.lammps.org/region.html) move args = v_x v_y v_z v_x,v_y,v_z = equal-style variables for x,y,z displacement of region over time (distance units) | 39 | 0.99991 |
| `Evalgeometry` | `openarg` | Validation of open arguments for region command (https://docs.lammps.org/region.html) open value = integer from 1-6 corresponding to face index (see below) The indices specified as part of the open keyword have the following meanings: | 32 | 0.99991 |
| `Evalgeometry` | `removegroup` | force the group creation in script | 3 | 0.99991 |
| `Evalgeometry` | `removemove` | force the fix move creation in script | 3 | 0.99991 |
| `Evalgeometry` | `rotatearg` | Validation of rotate arguments for region command (https://docs.lammps.org/region.html) rotate args = v_theta Px Py Pz Rx Ry Rz v_theta = equal-style variable for rotaton of region over time (in radians) Px,Py,Pz = origin for axis of rotation (distance units) Rx,Ry,Rz = axis of rotation vector | 36 | 0.99991 |
| `Evalgeometry` | `scriptobject` | Method to return a scriptobject based on region instead of an input file Syntax similar to script.scriptobject OBJ = scriptobject(...) Implemented properties: beadtype=1,2,... name="short name" fullname = "comprehensive name" style = "smd" forcefield = any valid forcefield instance (default = rigidwall()) | 34 | 0.99991 |
| `Evalgeometry` | `setgroup` | force the group creation in script | 3 | 0.99991 |
| `Evalgeometry` | `sidearg` | Validation of side arguments for region command (https://docs.lammps.org/region.html) side value = in or out in = the region is inside the specified geometry out = the region is outside the specified geometry | 20 | 0.99991 |
| `Evalgeometry` | `unitsarg` | Validation for units arguments for region command (https://docs.lammps.org/region.html) units value = lattice or box lattice = the geometry is defined in lattice units box = the geometry is defined in simulation box units | 20 | 0.99991 |
| `Evalgeometry` | `update` | update the USER content for all three scripts | 14 | 0.99991 |
| `Intersect` | `__add__` | overload addition ("+") operator | 19 | 0.99991 |
| `Intersect` | `__copy__` | copy method | 6 | 0.99991 |
| `Intersect` | `__deepcopy__` | deep copy method | 8 | 0.99991 |
| `Intersect` | `__getstate__` | getstate for cooperative inheritance / duplication | 3 | 0.99991 |
| `Intersect` | `__iadd__` | overload iaddition ("+=") operator | 16 | 0.99991 |
| `Intersect` | `__init__` | constructor of the generic core geometry USER: any definitions requires by the geometry VARIABLES: variables used to define the geometry (to be used in LAMMPS) hasgroup, hasmove: flag to force the sections group and move SECTIONS: they must be PIZZA.script | 14 | 0.99991 |
| `Intersect` | `__or__` | overload | pipe | 19 | 0.99991 |
| `Intersect` | `__repr__` | display method | 24 | 0.99991 |
| `Intersect` | `__setstate__` | setstate for cooperative inheritance / duplication | 3 | 0.99991 |
| `Intersect` | `copy` | returns a copy of the graphical object | 11 | 0.99991 |
| `Intersect` | `creategroup` | force the group creation in script | 3 | 0.99991 |
| `Intersect` | `createmove` | force the fix move creation in script | 3 | 0.99991 |
| `Intersect` | `do` | generates a script | 6 | 0.99991 |
| `Intersect` | `fixmoveargs` | Validates all arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) the result is adictionary, all fixmove can be combined | 18 | 0.99991 |
| `Intersect` | `fixmoveargvalidator` | Validation of arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) | 39 | 0.99991 |
| `Intersect` | `get_fixmovesyntax` | Returns the syntax for LAMMPS command, or detailed explanation for a specific argument type | 39 | 0.99991 |
| `Intersect` | `movearg` | Validation of move arguments for region command (https://docs.lammps.org/region.html) move args = v_x v_y v_z v_x,v_y,v_z = equal-style variables for x,y,z displacement of region over time (distance units) | 39 | 0.99991 |
| `Intersect` | `openarg` | Validation of open arguments for region command (https://docs.lammps.org/region.html) open value = integer from 1-6 corresponding to face index (see below) The indices specified as part of the open keyword have the following meanings: | 32 | 0.99991 |
| `Intersect` | `removegroup` | force the group creation in script | 3 | 0.99991 |
| `Intersect` | `removemove` | force the fix move creation in script | 3 | 0.99991 |
| `Intersect` | `rotatearg` | Validation of rotate arguments for region command (https://docs.lammps.org/region.html) rotate args = v_theta Px Py Pz Rx Ry Rz v_theta = equal-style variable for rotaton of region over time (in radians) Px,Py,Pz = origin for axis of rotation (distance units) Rx,Ry,Rz = axis of rotation vector | 36 | 0.99991 |
| `Intersect` | `scriptobject` | Method to return a scriptobject based on region instead of an input file Syntax similar to script.scriptobject OBJ = scriptobject(...) Implemented properties: beadtype=1,2,... name="short name" fullname = "comprehensive name" style = "smd" forcefield = any valid forcefield instance (default = rigidwall()) | 34 | 0.99991 |
| `Intersect` | `setgroup` | force the group creation in script | 3 | 0.99991 |
| `Intersect` | `sidearg` | Validation of side arguments for region command (https://docs.lammps.org/region.html) side value = in or out in = the region is inside the specified geometry out = the region is outside the specified geometry | 20 | 0.99991 |
| `Intersect` | `unitsarg` | Validation for units arguments for region command (https://docs.lammps.org/region.html) units value = lattice or box lattice = the geometry is defined in lattice units box = the geometry is defined in simulation box units | 20 | 0.99991 |
| `Intersect` | `update` | update the USER content for all three scripts | 14 | 0.99991 |
| `LammpsCollectionGroup` | `do` | generate the LAMMPS code with VARIABLE definitions | 12 | 0.99991 |
| `LammpsCreate` | `do` | generate the LAMMPS code with VARIABLE definitions | 12 | 0.99991 |
| `LammpsFooter` | `do` | generate the LAMMPS code with VARIABLE definitions | 12 | 0.99991 |
| `LammpsFooterPreview` | `do` | generate the LAMMPS code with VARIABLE definitions | 12 | 0.99991 |
| `LammpsGeneric` | `do` | generate the LAMMPS code with VARIABLE definitions | 12 | 0.99991 |
| `LammpsGroup` | `do` | generate the LAMMPS code with VARIABLE definitions | 12 | 0.99991 |
| `LammpsHeader` | `do` | generate the LAMMPS code with VARIABLE definitions | 12 | 0.99991 |
| `LammpsHeaderBox` | `do` | generate the LAMMPS code with VARIABLE definitions | 12 | 0.99991 |
| `LammpsHeaderInit` | `__init__` | Constructor adding instance definitions stored in USER. | 4 | 0.99991 |
| `LammpsHeaderInit` | `do` | generate the LAMMPS code with VARIABLE definitions | 12 | 0.99991 |
| `LammpsHeaderInit` | `generate_template` | Generate the TEMPLATE based on USER definitions. | 15 | 0.99991 |
| `LammpsHeaderLattice` | `__init__` | Constructor adding instance definitions stored in USER. | 4 | 0.99991 |
| `LammpsHeaderLattice` | `do` | generate the LAMMPS code with VARIABLE definitions | 12 | 0.99991 |
| `LammpsHeaderLattice` | `generate_template` | Generate the TEMPLATE based on USER definitions. | 8 | 0.99991 |
| `LammpsHeaderMass` | `__init__` | Constructor adding instance definitions stored in USER. | 14 | 0.99991 |
| `LammpsHeaderMass` | `do` | generate the LAMMPS code with VARIABLE definitions | 12 | 0.99991 |
| `LammpsHeaderMass` | `generate_template` | Generate the TEMPLATE for mass assignments based on USER definitions. | 32 | 0.99991 |
| `LammpsMove` | `do` | generate the LAMMPS code with VARIABLE definitions | 12 | 0.99991 |
| `LammpsRegion` | `do` | generate the LAMMPS code with VARIABLE definitions | 12 | 0.99991 |
| `LammpsSetGroup` | `do` | generate the LAMMPS code with VARIABLE definitions | 12 | 0.99991 |
| `LammpsSpacefilling` | `do` | generate the LAMMPS code with VARIABLE definitions | 12 | 0.99991 |
| `LammpsVariables` | `__init__` | constructor of LammpsVariables | 4 | 0.99991 |
| `LammpsVariables` | `__rshift__` | overload right  shift operator (keep only the last template) | 12 | 0.99991 |
| `LammpsVariables` | `do` | generate the LAMMPS code with VARIABLE definitions | 12 | 0.99991 |
| `Plane` | `__add__` | overload addition ("+") operator | 19 | 0.99991 |
| `Plane` | `__copy__` | copy method | 6 | 0.99991 |
| `Plane` | `__deepcopy__` | deep copy method | 8 | 0.99991 |
| `Plane` | `__getstate__` | getstate for cooperative inheritance / duplication | 3 | 0.99991 |
| `Plane` | `__iadd__` | overload iaddition ("+=") operator | 16 | 0.99991 |
| `Plane` | `__init__` | constructor of the generic core geometry USER: any definitions requires by the geometry VARIABLES: variables used to define the geometry (to be used in LAMMPS) hasgroup, hasmove: flag to force the sections group and move SECTIONS: they must be PIZZA.script | 19 | 0.99991 |
| `Plane` | `__or__` | overload | pipe | 19 | 0.99991 |
| `Plane` | `__repr__` | display method | 24 | 0.99991 |
| `Plane` | `__setstate__` | setstate for cooperative inheritance / duplication | 3 | 0.99991 |
| `Plane` | `copy` | returns a copy of the graphical object | 11 | 0.99991 |
| `Plane` | `creategroup` | force the group creation in script | 3 | 0.99991 |
| `Plane` | `createmove` | force the fix move creation in script | 3 | 0.99991 |
| `Plane` | `do` | generates a script | 6 | 0.99991 |
| `Plane` | `fixmoveargs` | Validates all arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) the result is adictionary, all fixmove can be combined | 18 | 0.99991 |
| `Plane` | `fixmoveargvalidator` | Validation of arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) | 39 | 0.99991 |
| `Plane` | `get_fixmovesyntax` | Returns the syntax for LAMMPS command, or detailed explanation for a specific argument type | 39 | 0.99991 |
| `Plane` | `movearg` | Validation of move arguments for region command (https://docs.lammps.org/region.html) move args = v_x v_y v_z v_x,v_y,v_z = equal-style variables for x,y,z displacement of region over time (distance units) | 39 | 0.99991 |
| `Plane` | `openarg` | Validation of open arguments for region command (https://docs.lammps.org/region.html) open value = integer from 1-6 corresponding to face index (see below) The indices specified as part of the open keyword have the following meanings: | 32 | 0.99991 |
| `Plane` | `removegroup` | force the group creation in script | 3 | 0.99991 |
| `Plane` | `removemove` | force the fix move creation in script | 3 | 0.99991 |
| `Plane` | `rotatearg` | Validation of rotate arguments for region command (https://docs.lammps.org/region.html) rotate args = v_theta Px Py Pz Rx Ry Rz v_theta = equal-style variable for rotaton of region over time (in radians) Px,Py,Pz = origin for axis of rotation (distance units) Rx,Ry,Rz = axis of rotation vector | 36 | 0.99991 |
| `Plane` | `scriptobject` | Method to return a scriptobject based on region instead of an input file Syntax similar to script.scriptobject OBJ = scriptobject(...) Implemented properties: beadtype=1,2,... name="short name" fullname = "comprehensive name" style = "smd" forcefield = any valid forcefield instance (default = rigidwall()) | 34 | 0.99991 |
| `Plane` | `setgroup` | force the group creation in script | 3 | 0.99991 |
| `Plane` | `sidearg` | Validation of side arguments for region command (https://docs.lammps.org/region.html) side value = in or out in = the region is inside the specified geometry out = the region is outside the specified geometry | 20 | 0.99991 |
| `Plane` | `unitsarg` | Validation for units arguments for region command (https://docs.lammps.org/region.html) units value = lattice or box lattice = the geometry is defined in lattice units box = the geometry is defined in simulation box units | 20 | 0.99991 |
| `Plane` | `update` | update the USER content for all three scripts | 14 | 0.99991 |
| `Prism` | `__add__` | overload addition ("+") operator | 19 | 0.99991 |
| `Prism` | `__copy__` | copy method | 6 | 0.99991 |
| `Prism` | `__deepcopy__` | deep copy method | 8 | 0.99991 |
| `Prism` | `__getstate__` | getstate for cooperative inheritance / duplication | 3 | 0.99991 |
| `Prism` | `__iadd__` | overload iaddition ("+=") operator | 16 | 0.99991 |
| `Prism` | `__init__` | constructor of the generic core geometry USER: any definitions requires by the geometry VARIABLES: variables used to define the geometry (to be used in LAMMPS) hasgroup, hasmove: flag to force the sections group and move SECTIONS: they must be PIZZA.script | 23 | 0.99991 |
| `Prism` | `__or__` | overload | pipe | 19 | 0.99991 |
| `Prism` | `__repr__` | display method | 24 | 0.99991 |
| `Prism` | `__setstate__` | setstate for cooperative inheritance / duplication | 3 | 0.99991 |
| `Prism` | `copy` | returns a copy of the graphical object | 11 | 0.99991 |
| `Prism` | `creategroup` | force the group creation in script | 3 | 0.99991 |
| `Prism` | `createmove` | force the fix move creation in script | 3 | 0.99991 |
| `Prism` | `do` | generates a script | 6 | 0.99991 |
| `Prism` | `fixmoveargs` | Validates all arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) the result is adictionary, all fixmove can be combined | 18 | 0.99991 |
| `Prism` | `fixmoveargvalidator` | Validation of arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) | 39 | 0.99991 |
| `Prism` | `get_fixmovesyntax` | Returns the syntax for LAMMPS command, or detailed explanation for a specific argument type | 39 | 0.99991 |
| `Prism` | `movearg` | Validation of move arguments for region command (https://docs.lammps.org/region.html) move args = v_x v_y v_z v_x,v_y,v_z = equal-style variables for x,y,z displacement of region over time (distance units) | 39 | 0.99991 |
| `Prism` | `openarg` | Validation of open arguments for region command (https://docs.lammps.org/region.html) open value = integer from 1-6 corresponding to face index (see below) The indices specified as part of the open keyword have the following meanings: | 32 | 0.99991 |
| `Prism` | `removegroup` | force the group creation in script | 3 | 0.99991 |
| `Prism` | `removemove` | force the fix move creation in script | 3 | 0.99991 |
| `Prism` | `rotatearg` | Validation of rotate arguments for region command (https://docs.lammps.org/region.html) rotate args = v_theta Px Py Pz Rx Ry Rz v_theta = equal-style variable for rotaton of region over time (in radians) Px,Py,Pz = origin for axis of rotation (distance units) Rx,Ry,Rz = axis of rotation vector | 36 | 0.99991 |
| `Prism` | `scriptobject` | Method to return a scriptobject based on region instead of an input file Syntax similar to script.scriptobject OBJ = scriptobject(...) Implemented properties: beadtype=1,2,... name="short name" fullname = "comprehensive name" style = "smd" forcefield = any valid forcefield instance (default = rigidwall()) | 34 | 0.99991 |
| `Prism` | `setgroup` | force the group creation in script | 3 | 0.99991 |
| `Prism` | `sidearg` | Validation of side arguments for region command (https://docs.lammps.org/region.html) side value = in or out in = the region is inside the specified geometry out = the region is outside the specified geometry | 20 | 0.99991 |
| `Prism` | `unitsarg` | Validation for units arguments for region command (https://docs.lammps.org/region.html) units value = lattice or box lattice = the geometry is defined in lattice units box = the geometry is defined in simulation box units | 20 | 0.99991 |
| `Prism` | `update` | update the USER content for all three scripts | 14 | 0.99991 |
| `Prism` | `volume` | Calculate the volume of the prism based on USER.args | 22 | 0.99991 |
| `Sphere` | `__add__` | overload addition ("+") operator | 19 | 0.99991 |
| `Sphere` | `__copy__` | copy method | 6 | 0.99991 |
| `Sphere` | `__deepcopy__` | deep copy method | 8 | 0.99991 |
| `Sphere` | `__getstate__` | getstate for cooperative inheritance / duplication | 3 | 0.99991 |
| `Sphere` | `__iadd__` | overload iaddition ("+=") operator | 16 | 0.99991 |
| `Sphere` | `__init__` | constructor of the generic core geometry USER: any definitions requires by the geometry VARIABLES: variables used to define the geometry (to be used in LAMMPS) hasgroup, hasmove: flag to force the sections group and move SECTIONS: they must be PIZZA.script | 23 | 0.99991 |
| `Sphere` | `__or__` | overload | pipe | 19 | 0.99991 |
| `Sphere` | `__repr__` | display method | 24 | 0.99991 |
| `Sphere` | `__setstate__` | setstate for cooperative inheritance / duplication | 3 | 0.99991 |
| `Sphere` | `copy` | returns a copy of the graphical object | 11 | 0.99991 |
| `Sphere` | `creategroup` | force the group creation in script | 3 | 0.99991 |
| `Sphere` | `createmove` | force the fix move creation in script | 3 | 0.99991 |
| `Sphere` | `do` | generates a script | 6 | 0.99991 |
| `Sphere` | `fixmoveargs` | Validates all arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) the result is adictionary, all fixmove can be combined | 18 | 0.99991 |
| `Sphere` | `fixmoveargvalidator` | Validation of arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) | 39 | 0.99991 |
| `Sphere` | `get_fixmovesyntax` | Returns the syntax for LAMMPS command, or detailed explanation for a specific argument type | 39 | 0.99991 |
| `Sphere` | `movearg` | Validation of move arguments for region command (https://docs.lammps.org/region.html) move args = v_x v_y v_z v_x,v_y,v_z = equal-style variables for x,y,z displacement of region over time (distance units) | 39 | 0.99991 |
| `Sphere` | `openarg` | Validation of open arguments for region command (https://docs.lammps.org/region.html) open value = integer from 1-6 corresponding to face index (see below) The indices specified as part of the open keyword have the following meanings: | 32 | 0.99991 |
| `Sphere` | `removegroup` | force the group creation in script | 3 | 0.99991 |
| `Sphere` | `removemove` | force the fix move creation in script | 3 | 0.99991 |
| `Sphere` | `rotatearg` | Validation of rotate arguments for region command (https://docs.lammps.org/region.html) rotate args = v_theta Px Py Pz Rx Ry Rz v_theta = equal-style variable for rotaton of region over time (in radians) Px,Py,Pz = origin for axis of rotation (distance units) Rx,Ry,Rz = axis of rotation vector | 36 | 0.99991 |
| `Sphere` | `scriptobject` | Method to return a scriptobject based on region instead of an input file Syntax similar to script.scriptobject OBJ = scriptobject(...) Implemented properties: beadtype=1,2,... name="short name" fullname = "comprehensive name" style = "smd" forcefield = any valid forcefield instance (default = rigidwall()) | 34 | 0.99991 |
| `Sphere` | `setgroup` | force the group creation in script | 3 | 0.99991 |
| `Sphere` | `sidearg` | Validation of side arguments for region command (https://docs.lammps.org/region.html) side value = in or out in = the region is inside the specified geometry out = the region is outside the specified geometry | 20 | 0.99991 |
| `Sphere` | `unitsarg` | Validation for units arguments for region command (https://docs.lammps.org/region.html) units value = lattice or box lattice = the geometry is defined in lattice units box = the geometry is defined in simulation box units | 20 | 0.99991 |
| `Sphere` | `update` | update the USER content for all three scripts | 14 | 0.99991 |
| `Sphere` | `volume` | Calculate the volume of the sphere based on USER.args | 13 | 0.99991 |
| `Union` | `__add__` | overload addition ("+") operator | 19 | 0.99991 |
| `Union` | `__copy__` | copy method | 6 | 0.99991 |
| `Union` | `__deepcopy__` | deep copy method | 8 | 0.99991 |
| `Union` | `__getstate__` | getstate for cooperative inheritance / duplication | 3 | 0.99991 |
| `Union` | `__iadd__` | overload iaddition ("+=") operator | 16 | 0.99991 |
| `Union` | `__init__` | constructor of the generic core geometry USER: any definitions requires by the geometry VARIABLES: variables used to define the geometry (to be used in LAMMPS) hasgroup, hasmove: flag to force the sections group and move SECTIONS: they must be PIZZA.script | 14 | 0.99991 |
| `Union` | `__or__` | overload | pipe | 19 | 0.99991 |
| `Union` | `__repr__` | display method | 24 | 0.99991 |
| `Union` | `__setstate__` | setstate for cooperative inheritance / duplication | 3 | 0.99991 |
| `Union` | `copy` | returns a copy of the graphical object | 11 | 0.99991 |
| `Union` | `creategroup` | force the group creation in script | 3 | 0.99991 |
| `Union` | `createmove` | force the fix move creation in script | 3 | 0.99991 |
| `Union` | `do` | generates a script | 6 | 0.99991 |
| `Union` | `fixmoveargs` | Validates all arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) the result is adictionary, all fixmove can be combined | 18 | 0.99991 |
| `Union` | `fixmoveargvalidator` | Validation of arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) | 39 | 0.99991 |
| `Union` | `get_fixmovesyntax` | Returns the syntax for LAMMPS command, or detailed explanation for a specific argument type | 39 | 0.99991 |
| `Union` | `movearg` | Validation of move arguments for region command (https://docs.lammps.org/region.html) move args = v_x v_y v_z v_x,v_y,v_z = equal-style variables for x,y,z displacement of region over time (distance units) | 39 | 0.99991 |
| `Union` | `openarg` | Validation of open arguments for region command (https://docs.lammps.org/region.html) open value = integer from 1-6 corresponding to face index (see below) The indices specified as part of the open keyword have the following meanings: | 32 | 0.99991 |
| `Union` | `removegroup` | force the group creation in script | 3 | 0.99991 |
| `Union` | `removemove` | force the fix move creation in script | 3 | 0.99991 |
| `Union` | `rotatearg` | Validation of rotate arguments for region command (https://docs.lammps.org/region.html) rotate args = v_theta Px Py Pz Rx Ry Rz v_theta = equal-style variable for rotaton of region over time (in radians) Px,Py,Pz = origin for axis of rotation (distance units) Rx,Ry,Rz = axis of rotation vector | 36 | 0.99991 |
| `Union` | `scriptobject` | Method to return a scriptobject based on region instead of an input file Syntax similar to script.scriptobject OBJ = scriptobject(...) Implemented properties: beadtype=1,2,... name="short name" fullname = "comprehensive name" style = "smd" forcefield = any valid forcefield instance (default = rigidwall()) | 34 | 0.99991 |
| `Union` | `setgroup` | force the group creation in script | 3 | 0.99991 |
| `Union` | `sidearg` | Validation of side arguments for region command (https://docs.lammps.org/region.html) side value = in or out in = the region is inside the specified geometry out = the region is outside the specified geometry | 20 | 0.99991 |
| `Union` | `unitsarg` | Validation for units arguments for region command (https://docs.lammps.org/region.html) units value = lattice or box lattice = the geometry is defined in lattice units box = the geometry is defined in simulation box units | 20 | 0.99991 |
| `Union` | `update` | update the USER content for all three scripts | 14 | 0.99991 |
| `coregeometry` | `__add__` | overload addition ("+") operator | 19 | 0.99991 |
| `coregeometry` | `__copy__` | copy method | 6 | 0.99991 |
| `coregeometry` | `__deepcopy__` | deep copy method | 8 | 0.99991 |
| `coregeometry` | `__getstate__` | getstate for cooperative inheritance / duplication | 3 | 0.99991 |
| `coregeometry` | `__iadd__` | overload iaddition ("+=") operator | 16 | 0.99991 |
| `coregeometry` | `__init__` | constructor of the generic core geometry USER: any definitions requires by the geometry VARIABLES: variables used to define the geometry (to be used in LAMMPS) hasgroup, hasmove: flag to force the sections group and move SECTIONS: they must be PIZZA.script | 48 | 0.99991 |
| `coregeometry` | `__or__` | overload | pipe | 19 | 0.99991 |
| `coregeometry` | `__repr__` | display method | 24 | 0.99991 |
| `coregeometry` | `__setstate__` | setstate for cooperative inheritance / duplication | 3 | 0.99991 |
| `coregeometry` | `copy` | returns a copy of the graphical object | 11 | 0.99991 |
| `coregeometry` | `creategroup` | force the group creation in script | 3 | 0.99991 |
| `coregeometry` | `createmove` | force the fix move creation in script | 3 | 0.99991 |
| `coregeometry` | `do` | generates a script | 6 | 0.99991 |
| `coregeometry` | `fixmoveargs` | Validates all arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) the result is adictionary, all fixmove can be combined | 18 | 0.99991 |
| `coregeometry` | `fixmoveargvalidator` | Validation of arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html) | 39 | 0.99991 |
| `coregeometry` | `get_fixmovesyntax` | Returns the syntax for LAMMPS command, or detailed explanation for a specific argument type | 39 | 0.99991 |
| `coregeometry` | `movearg` | Validation of move arguments for region command (https://docs.lammps.org/region.html) move args = v_x v_y v_z v_x,v_y,v_z = equal-style variables for x,y,z displacement of region over time (distance units) | 39 | 0.99991 |
| `coregeometry` | `openarg` | Validation of open arguments for region command (https://docs.lammps.org/region.html) open value = integer from 1-6 corresponding to face index (see below) The indices specified as part of the open keyword have the following meanings: | 32 | 0.99991 |
| `coregeometry` | `removegroup` | force the group creation in script | 3 | 0.99991 |
| `coregeometry` | `removemove` | force the fix move creation in script | 3 | 0.99991 |
| `coregeometry` | `rotatearg` | Validation of rotate arguments for region command (https://docs.lammps.org/region.html) rotate args = v_theta Px Py Pz Rx Ry Rz v_theta = equal-style variable for rotaton of region over time (in radians) Px,Py,Pz = origin for axis of rotation (distance units) Rx,Ry,Rz = axis of rotation vector | 36 | 0.99991 |
| `coregeometry` | `scriptobject` | Method to return a scriptobject based on region instead of an input file Syntax similar to script.scriptobject OBJ = scriptobject(...) Implemented properties: beadtype=1,2,... name="short name" fullname = "comprehensive name" style = "smd" forcefield = any valid forcefield instance (default = rigidwall()) | 34 | 0.99991 |
| `coregeometry` | `setgroup` | force the group creation in script | 3 | 0.99991 |
| `coregeometry` | `sidearg` | Validation of side arguments for region command (https://docs.lammps.org/region.html) side value = in or out in = the region is inside the specified geometry out = the region is outside the specified geometry | 20 | 0.99991 |
| `coregeometry` | `unitsarg` | Validation for units arguments for region command (https://docs.lammps.org/region.html) units value = lattice or box lattice = the geometry is defined in lattice units box = the geometry is defined in simulation box units | 20 | 0.99991 |
| `coregeometry` | `update` | update the USER content for all three scripts | 14 | 0.99991 |
| `emulsion` | `__init__` | Parameters ---------- The insertions are performed between xmin,ymin and xmax,ymax xmin : int64 or real, optional x left corner. The default is 10. ymin : int64 or real, optional y bottom corner. The default is 10. zmin : int64 or real, optional z bottom corner. The default is 10. xmax : int64 or real, optional x right corner. The default is 90. ymax : int64 or real, optional y top corner. The default is 90. zmax : int64 or real, optional z top corner. The default is 90. beadtype : default beadtype to apply if not precised at insertion maxtrials : integer, optional Maximum of attempts for an object. The default is 1000. forcedinsertion : logical, optional Set it to true to force the next insertion. The default is True. | 40 | 0.99991 |
| `emulsion` | `__repr__` | Return repr(self). | 6 | 0.99991 |
| `emulsion` | `accepted` | acceptation criterion | 3 | 0.99991 |
| `emulsion` | `dist` | shortest distance of the center (x,y) to the wall or any object | 3 | 0.99991 |
| `emulsion` | `insertion` | insert a list of objects nsuccess=insertion(rlist,beadtype=None) beadtype=b forces the value b if None, defaultbeadtype is used instead | 21 | 0.99991 |
| `emulsion` | `insertone` | insert one object of radius r properties: x,y,z coordinates (if missing, picked randomly from uniform distribution) r radius (default = 2% of diagonal) beadtype (default = defautbeadtype) overlap = False (accept only if no overlap) | 28 | 0.99991 |
| `emulsion` | `pairdist` | pair distance to the surface of all disks/spheres | 6 | 0.99991 |
| `emulsion` | `rand` | random position x,y | 5 | 0.99991 |
| `emulsion` | `setbeadtype` | set the default or the supplied beadtype | 8 | 0.99991 |
| `emulsion` | `walldist` | shortest distance to the wall | 3 | 0.99991 |
| `headersRegiondata` | `generatorforlammps` | generate LAMMPS code from regiondata (struct) generatorforlammps(verbose,hasvariables) hasvariables = False is used to prevent a call of generatorforLammps() for scripts others than LammpsGeneric ones | 31 | 0.99991 |
| `region` | `__contains__` | in override | 3 | 0.99991 |
| `region` | `__getattr__` | getattr attribute override | 14 | 0.99991 |
| `region` | `__getitem__` | R[i] returns the ith element of the structure R[:4] returns a structure with the four first fields R[[1,3]] returns the second and fourth elements | 20 | 0.99991 |
| `region` | `__getstate__` | getstate for cooperative inheritance / duplication | 3 | 0.99991 |
| `region` | `__init__` | constructor | 202 | 0.99991 |
| `region` | `__iter__` | region iterator | 6 | 0.99991 |
| `region` | `__len__` | len method | 3 | 0.99991 |
| `region` | `__next__` | region iterator | 7 | 0.99991 |
| `region` | `__repr__` | display method | 24 | 0.99991 |
| `region` | `__setattr__` | setattr override | 6 | 0.99991 |
| `region` | `__setstate__` | setstate for cooperative inheritance / duplication | 3 | 0.99991 |
| `region` | `__str__` | string representation of a region | 4 | 0.99991 |
| `region` | `block` | creates a block region xlo,xhi,ylo,yhi,zlo,zhi = bounds of block in all dimensions (distance units) | 96 | 0.99991 |
| `region` | `collection` |  | 27 | 0.99991 |
| `region` | `cone` | creates a cone region dim = "x" or "y" or "z" = axis of the cone note: USER, LAMMPS variables are not authorized here c1,c2 = coords of cone axis in other 2 dimensions (distance units) radlo,radhi = cone radii at lo and hi end (distance units) lo,hi = bounds of cone in dim (distance units) | 127 | 0.99991 |
| `region` | `count` | count objects by type | 13 | 0.99991 |
| `region` | `cylinder` | creates a cylinder region dim = x or y or z = axis of cylinder c1,c2 = coords of cylinder axis in other 2 dimensions (distance units) radius = cylinder radius (distance units) c1,c2, and radius can be a LAMMPS variable lo,hi = bounds of cylinder in dim (distance units) | 122 | 0.99991 |
| `region` | `delete` | delete object | 10 | 0.99991 |
| `region` | `do` | execute the entire script | 3 | 0.99991 |
| `region` | `dolive` | execute the entire script for online testing see: https://editor.lammps.org/ | 10 | 0.99991 |
| `region` | `ellipsoid` | creates an ellipsoid region ellipsoid(x,y,z,a,b,c [,name=None,beadtype=None,property=value,...]) x,y,z = center of ellipsoid (distance units) a,b,c = half the length of the principal axes of the ellipsoid (distance units) | 114 | 0.99991 |
| `region` | `eval` | evaluates (i.e, combine scripts) an expression combining objects R= region(name="my region") R.eval(o1+o2+...,name='obj') R.eval(o1|o2|...,name='obj') R.name will be the resulting object of class region.eval (region.coregeometry) | 41 | 0.99991 |
| `region` | `get` | returns the object | 6 | 0.99991 |
| `region` | `group` |  | 2 | 0.99991 |
| `region` | `hasattr` | return true if the object exist | 4 | 0.99991 |
| `region` | `intersect` | creates an intersection region intersect("reg-ID1","reg-ID2",name="myname",beadtype=1,...) reg-ID1,reg-ID2, ... = IDs of regions to join together | 60 | 0.99991 |
| `region` | `list` | list objects | 10 | 0.99991 |
| `region` | `pipescript` |  | 24 | 0.99991 |
| `region` | `plane` | creates a plane region px,py,pz = point on the plane (distance units) nx,ny,nz = direction normal to plane (distance units) | 93 | 0.99991 |
| `region` | `prism` | creates a prism region xlo,xhi,ylo,yhi,zlo,zhi = bounds of untilted prism (distance units) xy = distance to tilt y in x direction (distance units) xz = distance to tilt z in x direction (distance units) yz = distance to tilt z in y direction (distance units) | 101 | 0.99991 |
| `region` | `pscriptHeaders` | Surrogate method for generating LAMMPS pipescript headers. Calls the `scriptHeaders` method with `pipescript=True`. | 19 | 0.99991 |
| `region` | `scale_and_translate` | Scale and translate a value or encapsulate the formula within a string. | 47 | 0.99991 |
| `region` | `scatter` | Parameters ---------- E : scatter or emulsion object codes for x,y,z and r. name : string, optional name of the collection. The default is "emulsion". beadtype : integer, optional for all objects. The default is 1. | 37 | 0.99991 |
| `region` | `script` | script all objects in the region | 30 | 0.99991 |
| `region` | `scriptHeaders` | Generate and return LAMMPS header scripts for initializing the simulation, defining the lattice, and specifying the simulation box for all region objects. | 71 | 0.99991 |
| `region` | `set` | set field and value | 17 | 0.99991 |
| `region` | `sphere` | creates a sphere region x,y,z = center of sphere (distance units) radius = radius of sphere (distance units) x,y,z, and radius can be a variable | 95 | 0.99991 |
| `region` | `union` | creates a union region union("reg-ID1","reg-ID2",name="myname",beadtype=1,...) reg-ID1,reg-ID2, ... = IDs of regions to join together | 60 | 0.99991 |
| `regioncollection` | `__init__` | constructor | 11 | 0.99991 |
| `regiondata` | `generatorforlammps` | generate LAMMPS code from regiondata (struct) generatorforlammps(verbose,hasvariables) hasvariables = False is used to prevent a call of generatorforLammps() for scripts others than LammpsGeneric ones | 31 | 0.99991 |
| `scatter` | `__init__` | The scatter class provides an easy constructor to distribute in space objects according to their positions x,y,z size r (radius) and beadtype. | 17 | 0.99991 |
| `scatter` | `pairdist` | pair distance to the surface of all disks/spheres | 6 | 0.99991 |

## Module `pizza.script`

### Class Inheritance Diagram
```mermaid
graph TD;
CallableScript
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
ulsph
water
forcefield --> smd
none --> rigidwall
object --> CallableScript
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
| (module-level) | `frame_header` | Format the header content into an ASCII framed box with customizable properties. | 147 | 0.99991 |
| (module-level) | `get_metadata` | Return a dictionary of explicitly defined metadata. | 15 | 0.99991 |
| (module-level) | `<lambda>` |  | 1 | 0.99991 |
| (module-level) | `picker` |  | 1 | 0.99991 |
| (module-level) | `remove_comments` | Removes comments from a single or multi-line string, handling quotes, escaped characters, and line continuation. | 101 | 0.99991 |
| (module-level) | `span` |  | 2 | 0.99991 |
| `CallableScript` | `__call__` | Call self as a function. | 3 | 0.99991 |
| `CallableScript` | `__get__` |  | 3 | 0.99991 |
| `CallableScript` | `__init__` | Initialize self.  See help(type(self)) for accurate signature. | 2 | 0.99991 |
| `boundarysection` | `__add__` | overload addition operator | 24 | 0.99991 |
| `boundarysection` | `__and__` | overload and operator | 7 | 0.99991 |
| `boundarysection` | `__copy__` | copy method | 6 | 0.99991 |
| `boundarysection` | `__deepcopy__` | deep copy method | 8 | 0.99991 |
| `boundarysection` | `__init__` | constructor adding instance definitions stored in USER | 14 | 0.99991 |
| `boundarysection` | `__mul__` | overload * operator | 8 | 0.99991 |
| `boundarysection` | `__or__` | overload | or for pipe | 19 | 0.99991 |
| `boundarysection` | `__pow__` | overload ** operator | 8 | 0.99991 |
| `boundarysection` | `__repr__` | disp method | 22 | 0.99991 |
| `boundarysection` | `__rshift__` | overload right  shift operator (keep only the last template) | 10 | 0.99991 |
| `boundarysection` | `__str__` | string representation | 3 | 0.99991 |
| `boundarysection` | `_iadd__` | overload addition operator | 8 | 0.99991 |
| `boundarysection` | `detect_variables` | Detects variables in the content of the template using the pattern r'\$\{(\w+)\}'. | 22 | 0.99991 |
| `boundarysection` | `do` | Generate the LAMMPS script based on the current configuration. | 58 | 0.99991 |
| `boundarysection` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 0.99991 |
| `boundarysection` | `header` | Generate a formatted header for the script file. | 37 | 0.99991 |
| `boundarysection` | `printheader` | print header | 7 | 0.99991 |
| `boundarysection` | `tmpwrite` | Write the script to a temporary file and create optional persistent copies. | 92 | 0.99991 |
| `boundarysection` | `write` | Write the script to a file. | 39 | 0.99991 |
| `discretizationsection` | `__add__` | overload addition operator | 24 | 0.99991 |
| `discretizationsection` | `__and__` | overload and operator | 7 | 0.99991 |
| `discretizationsection` | `__copy__` | copy method | 6 | 0.99991 |
| `discretizationsection` | `__deepcopy__` | deep copy method | 8 | 0.99991 |
| `discretizationsection` | `__init__` | constructor adding instance definitions stored in USER | 14 | 0.99991 |
| `discretizationsection` | `__mul__` | overload * operator | 8 | 0.99991 |
| `discretizationsection` | `__or__` | overload | or for pipe | 19 | 0.99991 |
| `discretizationsection` | `__pow__` | overload ** operator | 8 | 0.99991 |
| `discretizationsection` | `__repr__` | disp method | 22 | 0.99991 |
| `discretizationsection` | `__rshift__` | overload right  shift operator (keep only the last template) | 10 | 0.99991 |
| `discretizationsection` | `__str__` | string representation | 3 | 0.99991 |
| `discretizationsection` | `_iadd__` | overload addition operator | 8 | 0.99991 |
| `discretizationsection` | `detect_variables` | Detects variables in the content of the template using the pattern r'\$\{(\w+)\}'. | 22 | 0.99991 |
| `discretizationsection` | `do` | Generate the LAMMPS script based on the current configuration. | 58 | 0.99991 |
| `discretizationsection` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 0.99991 |
| `discretizationsection` | `header` | Generate a formatted header for the script file. | 37 | 0.99991 |
| `discretizationsection` | `printheader` | print header | 7 | 0.99991 |
| `discretizationsection` | `tmpwrite` | Write the script to a temporary file and create optional persistent copies. | 92 | 0.99991 |
| `discretizationsection` | `write` | Write the script to a file. | 39 | 0.99991 |
| `dumpsection` | `__add__` | overload addition operator | 24 | 0.99991 |
| `dumpsection` | `__and__` | overload and operator | 7 | 0.99991 |
| `dumpsection` | `__copy__` | copy method | 6 | 0.99991 |
| `dumpsection` | `__deepcopy__` | deep copy method | 8 | 0.99991 |
| `dumpsection` | `__init__` | constructor adding instance definitions stored in USER | 14 | 0.99991 |
| `dumpsection` | `__mul__` | overload * operator | 8 | 0.99991 |
| `dumpsection` | `__or__` | overload | or for pipe | 19 | 0.99991 |
| `dumpsection` | `__pow__` | overload ** operator | 8 | 0.99991 |
| `dumpsection` | `__repr__` | disp method | 22 | 0.99991 |
| `dumpsection` | `__rshift__` | overload right  shift operator (keep only the last template) | 10 | 0.99991 |
| `dumpsection` | `__str__` | string representation | 3 | 0.99991 |
| `dumpsection` | `_iadd__` | overload addition operator | 8 | 0.99991 |
| `dumpsection` | `detect_variables` | Detects variables in the content of the template using the pattern r'\$\{(\w+)\}'. | 22 | 0.99991 |
| `dumpsection` | `do` | Generate the LAMMPS script based on the current configuration. | 58 | 0.99991 |
| `dumpsection` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 0.99991 |
| `dumpsection` | `header` | Generate a formatted header for the script file. | 37 | 0.99991 |
| `dumpsection` | `printheader` | print header | 7 | 0.99991 |
| `dumpsection` | `tmpwrite` | Write the script to a temporary file and create optional persistent copies. | 92 | 0.99991 |
| `dumpsection` | `write` | Write the script to a file. | 39 | 0.99991 |
| `geometrysection` | `__add__` | overload addition operator | 24 | 0.99991 |
| `geometrysection` | `__and__` | overload and operator | 7 | 0.99991 |
| `geometrysection` | `__copy__` | copy method | 6 | 0.99991 |
| `geometrysection` | `__deepcopy__` | deep copy method | 8 | 0.99991 |
| `geometrysection` | `__init__` | constructor adding instance definitions stored in USER | 14 | 0.99991 |
| `geometrysection` | `__mul__` | overload * operator | 8 | 0.99991 |
| `geometrysection` | `__or__` | overload | or for pipe | 19 | 0.99991 |
| `geometrysection` | `__pow__` | overload ** operator | 8 | 0.99991 |
| `geometrysection` | `__repr__` | disp method | 22 | 0.99991 |
| `geometrysection` | `__rshift__` | overload right  shift operator (keep only the last template) | 10 | 0.99991 |
| `geometrysection` | `__str__` | string representation | 3 | 0.99991 |
| `geometrysection` | `_iadd__` | overload addition operator | 8 | 0.99991 |
| `geometrysection` | `detect_variables` | Detects variables in the content of the template using the pattern r'\$\{(\w+)\}'. | 22 | 0.99991 |
| `geometrysection` | `do` | Generate the LAMMPS script based on the current configuration. | 58 | 0.99991 |
| `geometrysection` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 0.99991 |
| `geometrysection` | `header` | Generate a formatted header for the script file. | 37 | 0.99991 |
| `geometrysection` | `printheader` | print header | 7 | 0.99991 |
| `geometrysection` | `tmpwrite` | Write the script to a temporary file and create optional persistent copies. | 92 | 0.99991 |
| `geometrysection` | `write` | Write the script to a file. | 39 | 0.99991 |
| `globalsection` | `__add__` | overload addition operator | 24 | 0.99991 |
| `globalsection` | `__and__` | overload and operator | 7 | 0.99991 |
| `globalsection` | `__copy__` | copy method | 6 | 0.99991 |
| `globalsection` | `__deepcopy__` | deep copy method | 8 | 0.99991 |
| `globalsection` | `__init__` | constructor adding instance definitions stored in USER | 14 | 0.99991 |
| `globalsection` | `__mul__` | overload * operator | 8 | 0.99991 |
| `globalsection` | `__or__` | overload | or for pipe | 19 | 0.99991 |
| `globalsection` | `__pow__` | overload ** operator | 8 | 0.99991 |
| `globalsection` | `__repr__` | disp method | 22 | 0.99991 |
| `globalsection` | `__rshift__` | overload right  shift operator (keep only the last template) | 10 | 0.99991 |
| `globalsection` | `__str__` | string representation | 3 | 0.99991 |
| `globalsection` | `_iadd__` | overload addition operator | 8 | 0.99991 |
| `globalsection` | `detect_variables` | Detects variables in the content of the template using the pattern r'\$\{(\w+)\}'. | 22 | 0.99991 |
| `globalsection` | `do` | Generate the LAMMPS script based on the current configuration. | 58 | 0.99991 |
| `globalsection` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 0.99991 |
| `globalsection` | `header` | Generate a formatted header for the script file. | 37 | 0.99991 |
| `globalsection` | `printheader` | print header | 7 | 0.99991 |
| `globalsection` | `tmpwrite` | Write the script to a temporary file and create optional persistent copies. | 92 | 0.99991 |
| `globalsection` | `write` | Write the script to a file. | 39 | 0.99991 |
| `initializesection` | `__add__` | overload addition operator | 24 | 0.99991 |
| `initializesection` | `__and__` | overload and operator | 7 | 0.99991 |
| `initializesection` | `__copy__` | copy method | 6 | 0.99991 |
| `initializesection` | `__deepcopy__` | deep copy method | 8 | 0.99991 |
| `initializesection` | `__init__` | constructor adding instance definitions stored in USER | 14 | 0.99991 |
| `initializesection` | `__mul__` | overload * operator | 8 | 0.99991 |
| `initializesection` | `__or__` | overload | or for pipe | 19 | 0.99991 |
| `initializesection` | `__pow__` | overload ** operator | 8 | 0.99991 |
| `initializesection` | `__repr__` | disp method | 22 | 0.99991 |
| `initializesection` | `__rshift__` | overload right  shift operator (keep only the last template) | 10 | 0.99991 |
| `initializesection` | `__str__` | string representation | 3 | 0.99991 |
| `initializesection` | `_iadd__` | overload addition operator | 8 | 0.99991 |
| `initializesection` | `detect_variables` | Detects variables in the content of the template using the pattern r'\$\{(\w+)\}'. | 22 | 0.99991 |
| `initializesection` | `do` | Generate the LAMMPS script based on the current configuration. | 58 | 0.99991 |
| `initializesection` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 0.99991 |
| `initializesection` | `header` | Generate a formatted header for the script file. | 37 | 0.99991 |
| `initializesection` | `printheader` | print header | 7 | 0.99991 |
| `initializesection` | `tmpwrite` | Write the script to a temporary file and create optional persistent copies. | 92 | 0.99991 |
| `initializesection` | `write` | Write the script to a file. | 39 | 0.99991 |
| `integrationsection` | `__add__` | overload addition operator | 24 | 0.99991 |
| `integrationsection` | `__and__` | overload and operator | 7 | 0.99991 |
| `integrationsection` | `__copy__` | copy method | 6 | 0.99991 |
| `integrationsection` | `__deepcopy__` | deep copy method | 8 | 0.99991 |
| `integrationsection` | `__init__` | constructor adding instance definitions stored in USER | 14 | 0.99991 |
| `integrationsection` | `__mul__` | overload * operator | 8 | 0.99991 |
| `integrationsection` | `__or__` | overload | or for pipe | 19 | 0.99991 |
| `integrationsection` | `__pow__` | overload ** operator | 8 | 0.99991 |
| `integrationsection` | `__repr__` | disp method | 22 | 0.99991 |
| `integrationsection` | `__rshift__` | overload right  shift operator (keep only the last template) | 10 | 0.99991 |
| `integrationsection` | `__str__` | string representation | 3 | 0.99991 |
| `integrationsection` | `_iadd__` | overload addition operator | 8 | 0.99991 |
| `integrationsection` | `detect_variables` | Detects variables in the content of the template using the pattern r'\$\{(\w+)\}'. | 22 | 0.99991 |
| `integrationsection` | `do` | Generate the LAMMPS script based on the current configuration. | 58 | 0.99991 |
| `integrationsection` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 0.99991 |
| `integrationsection` | `header` | Generate a formatted header for the script file. | 37 | 0.99991 |
| `integrationsection` | `printheader` | print header | 7 | 0.99991 |
| `integrationsection` | `tmpwrite` | Write the script to a temporary file and create optional persistent copies. | 92 | 0.99991 |
| `integrationsection` | `write` | Write the script to a file. | 39 | 0.99991 |
| `interactionsection` | `__add__` | overload addition operator | 24 | 0.99991 |
| `interactionsection` | `__and__` | overload and operator | 7 | 0.99991 |
| `interactionsection` | `__copy__` | copy method | 6 | 0.99991 |
| `interactionsection` | `__deepcopy__` | deep copy method | 8 | 0.99991 |
| `interactionsection` | `__init__` | constructor adding instance definitions stored in USER | 14 | 0.99991 |
| `interactionsection` | `__mul__` | overload * operator | 8 | 0.99991 |
| `interactionsection` | `__or__` | overload | or for pipe | 19 | 0.99991 |
| `interactionsection` | `__pow__` | overload ** operator | 8 | 0.99991 |
| `interactionsection` | `__repr__` | disp method | 22 | 0.99991 |
| `interactionsection` | `__rshift__` | overload right  shift operator (keep only the last template) | 10 | 0.99991 |
| `interactionsection` | `__str__` | string representation | 3 | 0.99991 |
| `interactionsection` | `_iadd__` | overload addition operator | 8 | 0.99991 |
| `interactionsection` | `detect_variables` | Detects variables in the content of the template using the pattern r'\$\{(\w+)\}'. | 22 | 0.99991 |
| `interactionsection` | `do` | Generate the LAMMPS script based on the current configuration. | 58 | 0.99991 |
| `interactionsection` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 0.99991 |
| `interactionsection` | `header` | Generate a formatted header for the script file. | 37 | 0.99991 |
| `interactionsection` | `printheader` | print header | 7 | 0.99991 |
| `interactionsection` | `tmpwrite` | Write the script to a temporary file and create optional persistent copies. | 92 | 0.99991 |
| `interactionsection` | `write` | Write the script to a file. | 39 | 0.99991 |
| `pipescript` | `__add__` | overload + as pipe with copy | 7 | 0.99991 |
| `pipescript` | `__copy__` | copy method | 6 | 0.99991 |
| `pipescript` | `__deepcopy__` | deep copy method | 8 | 0.99991 |
| `pipescript` | `__getitem__` | return the ith or slice element(s) of the pipe | 24 | 0.99991 |
| `pipescript` | `__iadd__` | overload += as pipe without copy | 6 | 0.99991 |
| `pipescript` | `__init__` | constructor | 26 | 0.99991 |
| `pipescript` | `__len__` | len() method | 3 | 0.99991 |
| `pipescript` | `__mul__` | overload * as multiple pipes with copy | 9 | 0.99991 |
| `pipescript` | `__or__` | Overload | pipe operator in pipescript | 51 | 0.99991 |
| `pipescript` | `__repr__` | display method | 29 | 0.99991 |
| `pipescript` | `__setitem__` | modify the ith element of the pipe p[4] = [] removes the 4th element p[4:7] = [] removes the elements from position 4 to 6 p[2:4] = p[0:2] copy the elements 0 and 1 in positions 2 and 3 p[[3,4]]=p[0] | 58 | 0.99991 |
| `pipescript` | `__str__` | string representation | 3 | 0.99991 |
| `pipescript` | `clear` |  | 16 | 0.99991 |
| `pipescript` | `do` | Execute the pipeline or a part of the pipeline and generate the LAMMPS script. | 118 | 0.99991 |
| `pipescript` | `do_legacy` | Execute the pipeline or a part of the pipeline and generate the LAMMPS script. | 99 | 0.99991 |
| `pipescript` | `dscript` | Convert the current pipescript object to a dscript object. | 107 | 0.99991 |
| `pipescript` | `getUSER` | getUSER get USER variable getUSER(idx,varname) | 9 | 0.99991 |
| `pipescript` | `header` | Generate a formatted header for the pipescript file. | 33 | 0.99991 |
| `pipescript` | `join` | join a combination scripts and pipescripts within a pipescript p = pipescript.join([s1,s2,p3,p4,p5...]) | 19 | 0.99991 |
| `pipescript` | `rename` | rename scripts in the pipe p.rename(idx=[0,2,3],name=["A","B","C"]) | 17 | 0.99991 |
| `pipescript` | `script` | script the pipeline or parts of the pipeline s = p.script() s = p.script([0,2]) | 50 | 0.99991 |
| `pipescript` | `setUSER` | setUSER sets USER variables setUSER(idx,varname,varvalue) | 9 | 0.99991 |
| `pipescript` | `write` | Write the combined script to a file. | 27 | 0.99991 |
| `runsection` | `__add__` | overload addition operator | 24 | 0.99991 |
| `runsection` | `__and__` | overload and operator | 7 | 0.99991 |
| `runsection` | `__copy__` | copy method | 6 | 0.99991 |
| `runsection` | `__deepcopy__` | deep copy method | 8 | 0.99991 |
| `runsection` | `__init__` | constructor adding instance definitions stored in USER | 14 | 0.99991 |
| `runsection` | `__mul__` | overload * operator | 8 | 0.99991 |
| `runsection` | `__or__` | overload | or for pipe | 19 | 0.99991 |
| `runsection` | `__pow__` | overload ** operator | 8 | 0.99991 |
| `runsection` | `__repr__` | disp method | 22 | 0.99991 |
| `runsection` | `__rshift__` | overload right  shift operator (keep only the last template) | 10 | 0.99991 |
| `runsection` | `__str__` | string representation | 3 | 0.99991 |
| `runsection` | `_iadd__` | overload addition operator | 8 | 0.99991 |
| `runsection` | `detect_variables` | Detects variables in the content of the template using the pattern r'\$\{(\w+)\}'. | 22 | 0.99991 |
| `runsection` | `do` | Generate the LAMMPS script based on the current configuration. | 58 | 0.99991 |
| `runsection` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 0.99991 |
| `runsection` | `header` | Generate a formatted header for the script file. | 37 | 0.99991 |
| `runsection` | `printheader` | print header | 7 | 0.99991 |
| `runsection` | `tmpwrite` | Write the script to a temporary file and create optional persistent copies. | 92 | 0.99991 |
| `runsection` | `write` | Write the script to a file. | 39 | 0.99991 |
| `script` | `__add__` | overload addition operator | 24 | 0.99991 |
| `script` | `__and__` | overload and operator | 7 | 0.99991 |
| `script` | `__copy__` | copy method | 6 | 0.99991 |
| `script` | `__deepcopy__` | deep copy method | 8 | 0.99991 |
| `script` | `__init__` | constructor adding instance definitions stored in USER | 14 | 0.99991 |
| `script` | `__mul__` | overload * operator | 8 | 0.99991 |
| `script` | `__or__` | overload | or for pipe | 19 | 0.99991 |
| `script` | `__pow__` | overload ** operator | 8 | 0.99991 |
| `script` | `__repr__` | disp method | 22 | 0.99991 |
| `script` | `__rshift__` | overload right  shift operator (keep only the last template) | 10 | 0.99991 |
| `script` | `__str__` | string representation | 3 | 0.99991 |
| `script` | `_iadd__` | overload addition operator | 8 | 0.99991 |
| `script` | `detect_variables` | Detects variables in the content of the template using the pattern r'\$\{(\w+)\}'. | 22 | 0.99991 |
| `script` | `do` | Generate the LAMMPS script based on the current configuration. | 58 | 0.99991 |
| `script` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 0.99991 |
| `script` | `header` | Generate a formatted header for the script file. | 37 | 0.99991 |
| `script` | `printheader` | print header | 7 | 0.99991 |
| `script` | `tmpwrite` | Write the script to a temporary file and create optional persistent copies. | 92 | 0.99991 |
| `script` | `write` | Write the script to a file. | 39 | 0.99991 |
| `scriptobject` | `__add__` | add a structure set sortdefintions=True to sort definitions (to maintain executability) | 12 | 0.99991 |
| `scriptobject` | `__eq__` | Return self==value. | 3 | 0.99991 |
| `scriptobject` | `__ge__` | Return self>=value. | 2 | 0.99991 |
| `scriptobject` | `__gt__` | Return self>value. | 2 | 0.99991 |
| `scriptobject` | `__init__` | constructor | 30 | 0.99991 |
| `scriptobject` | `__le__` | Return self<=value. | 2 | 0.99991 |
| `scriptobject` | `__lt__` | Return self<value. | 2 | 0.99991 |
| `scriptobject` | `__ne__` | Return self!=value. | 2 | 0.99991 |
| `scriptobject` | `__or__` | overload | or for pipe | 6 | 0.99991 |
| `scriptobject` | `__str__` | string representation | 3 | 0.99991 |
| `scriptobjectgroup` | `__add__` | overload + | 32 | 0.99991 |
| `scriptobjectgroup` | `__init__` | SOG constructor | 18 | 0.99991 |
| `scriptobjectgroup` | `__or__` | overload | or for pipe | 6 | 0.99991 |
| `scriptobjectgroup` | `__str__` | string representation | 3 | 0.99991 |
| `scriptobjectgroup` | `group_generator` | Generate and return a group object. | 28 | 0.99991 |
| `scriptobjectgroup` | `<lambda>` |  | 1 | 0.99991 |
| `scriptobjectgroup` | `mass` | Generates LAMMPS mass commands for each unique beadtype in the collection. | 89 | 0.99991 |
| `scriptobjectgroup` | `<lambda>` |  | 1 | 0.99991 |
| `scriptobjectgroup` | `select` | select bead from a keep beadlist | 11 | 0.99991 |
| `scriptobjectgroup` | `struct` | create a group with name | 10 | 0.99991 |
| `statussection` | `__add__` | overload addition operator | 24 | 0.99991 |
| `statussection` | `__and__` | overload and operator | 7 | 0.99991 |
| `statussection` | `__copy__` | copy method | 6 | 0.99991 |
| `statussection` | `__deepcopy__` | deep copy method | 8 | 0.99991 |
| `statussection` | `__init__` | constructor adding instance definitions stored in USER | 14 | 0.99991 |
| `statussection` | `__mul__` | overload * operator | 8 | 0.99991 |
| `statussection` | `__or__` | overload | or for pipe | 19 | 0.99991 |
| `statussection` | `__pow__` | overload ** operator | 8 | 0.99991 |
| `statussection` | `__repr__` | disp method | 22 | 0.99991 |
| `statussection` | `__rshift__` | overload right  shift operator (keep only the last template) | 10 | 0.99991 |
| `statussection` | `__str__` | string representation | 3 | 0.99991 |
| `statussection` | `_iadd__` | overload addition operator | 8 | 0.99991 |
| `statussection` | `detect_variables` | Detects variables in the content of the template using the pattern r'\$\{(\w+)\}'. | 22 | 0.99991 |
| `statussection` | `do` | Generate the LAMMPS script based on the current configuration. | 58 | 0.99991 |
| `statussection` | `getallattributes` | advanced method to get all attributes including class ones | 4 | 0.99991 |
| `statussection` | `header` | Generate a formatted header for the script file. | 37 | 0.99991 |
| `statussection` | `printheader` | print header | 7 | 0.99991 |
| `statussection` | `tmpwrite` | Write the script to a temporary file and create optional persistent copies. | 92 | 0.99991 |
| `statussection` | `write` | Write the script to a file. | 39 | 0.99991 |

