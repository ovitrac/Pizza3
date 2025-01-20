#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

================================================================================
REGION Module Documentation
================================================================================

Project: Pizza3
Authors: Olivier Vitrac, Han Chen
Copyright: 2024
Credits: Olivier Vitrac, Han Chen
License: GPLv3
Maintainer: Olivier Vitrac
Email: olivier.vitrac@agroparistech.fr
Version: 1.0

Overview
--------
The REGION module provides a suite of tools to define and manipulate native geometries in Python
 for LAMMPS (Large-scale Atomic/Molecular Massively Parallel Simulator). It is designed to facilitate
 the creation, concatenation, and manipulation of geometric regions used in molecular dynamics simulations.

Public Features
---------------
- Concatenation of Regions:
  - `R1 + R2` concatenates two regions (objects of R2 are inherited in R1, higher precedence for R2).
- Generation of Objects:
  - `R.do()` generates the objects (similar functionality to `do()` in pizza.script).
- Script Generation:
  - `R.script` returns the script (similar functionality to `script()` in pizza.script).
- Object Deletion:
  - `R.o1 = []` deletes object `o1`.
- Union of Objects:
  - `R.union(o1, o2, name=...)` creates a union of `o1` and `o2` (in the LAMMPS sense, see region manual).

Classes and Methods
-------------------
### Class: `region`
#### Description:
The `region` class is used to define and manipulate geometries for LAMMPS simulations. It includes
 methods for creating different geometric shapes, combining regions, and generating corresponding LAMMPS scripts.

#### Methods:
- **`__init__(self, name='', width=0, height=0, depth=0, regionunits='lattice', separationdistance=0.0, lattice_scale=1.0)`**
  - **Description**: Initializes a new region with specified dimensions and parameters.
  - **Parameters**:
    - `name` (str): The name of the region.
    - `width` (float): Width of the region.
    - `height` (float): Height of the region.
    - `depth` (float): Depth of the region.
    - `regionunits` (str): Units of the region dimensions ('lattice' or 'si').
    - `separationdistance` (float): Separation distance between regions.
    - `lattice_scale` (float): Scale of the lattice.

- **`do(self)`**
  - **Description**: Generates the objects within the region.
  - **Returns**: None

- **`script(self)`**
  - **Description**: Returns the LAMMPS script for the region.
  - **Returns**: str

- **`union(self, o1, o2, name='')`**
  - **Description**: Creates a union of two objects within the region.
  - **Parameters**:
    - `o1` (object): The first object.
    - `o2` (object): The second object.
    - `name` (str): The name of the union.
  - **Returns**: None

- **`cylinder(self, name, dim, c1, c2, radius, lo, hi, beadtype)`**
  - **Description**: Adds a cylinder to the region.
  - **Parameters**:
    - `name` (str): The name of the cylinder.
    - `dim` (str): Dimension along which the cylinder is oriented ('x', 'y', or 'z').
    - `c1` (float): First coordinate of the center of the cylinder's base.
    - `c2` (float): Second coordinate of the center of the cylinder's base.
    - `radius` (float): Radius of the cylinder.
    - `lo` (float): Lower bound of the cylinder along the specified dimension.
    - `hi` (float): Upper bound of the cylinder along the specified dimension.
    - `beadtype` (int): Type of beads to use for the cylinder.
  - **Returns**: None

- **`delete(self, name)`**
  - **Description**: Deletes an object from the region.
  - **Parameters**:
    - `name` (str): The name of the object to delete.
  - **Returns**: None

Examples
--------
Below are some examples demonstrating how to use the REGION module:

1. **Concatenating Two Regions**:
    ```python
    R1 = pizza.regions()
    R2 = pizza.regions()
    R = R1 + R2
    ```

2. **Generating Objects**:
    ```python
    R.do()
    ```

3. **Retrieving the Script**:
    ```python
    script_content = R.script()
    ```

4. **Deleting an Object**:
    ```python
    R.o1 = []
    ```

5. **Creating a Union of Objects**:
    ```python
    R.union(o1, o2, name='union_name')
    ```

6. **Adding a Cylinder**:
    ```python
    R.cylinder(name='cyl1', dim='z', c1=0, c2=0, radius=1.0, lo=0.0, hi=5.0, beadtype=1)


Advanced features
-----------------
Public features (i.e. to be used by the end-user)
    	Let R1, R2 being pizza.regions()
    	R = R1 + R2 concatenates two regions (objects of R2 are inherited in R1, higher precedence for R2)
    	R.do()   generate the objects (do() should work as in pizza.script)
    	R.script returns the script (script() should work as in pizza.script)

    	Let o1, o2 are objects of R
    	R.o1 = [] delete o1
    	R.union(o1,o2,name=...) creates an union of o1 and o2 (in the LAMMPS sense, see region manual)
    	R.intersect(o1,o2,name=...) creates an intersection of o1 and o2 (in the LAMMPS sense, see region manual)
    	R.eval(expr,name=)
    		expr any algebraic expression including +
    		o1+o2+...

Private features (i.e. to be used inside the code)
    	Overloading operators +, +=, | for any coregeometry object
   	Note that coregeometry have four main SECTIONS (scripts)
       SECTIONS["variables"]
       SECTIONS["region"]
       SECTIONS["create"]
       SECTIONS["group"]
       SECTIONS["move"]
   		USER, VARIABLES are overdefined as attributes

	+, += merge regions (no piping)
	| pipe them

   Add other geometries: block, sphere, cylinder....

    ```

Dependencies
------------
- Python 3.x
- LAMMPS
- pizza3.pizza

Installation
------------
To use the REGION module, ensure that you have Python 3.x and LAMMPS installed. You can integrate the module into your project by placing the `region.py` file in your working directory or your Python path.

License
-------
This project is licensed under the terms of the GPLv3 license.

Contact
-------
For any queries or contributions, please contact the maintainer:
- Olivier Vitrac, Han Chen
- Email: olivier.vitrac@agroparistech.fr
"""

__project__ = "Pizza3"
__author__ = "Olivier Vitrac, Han Chen"
__copyright__ = "Copyright 2024"
__credits__ = ["Olivier Vitrac", "Han Chen"]
__license__ = "GPLv3"
__maintainer__ = "Olivier Vitrac"
__email__ = "olivier.vitrac@agroparistech.fr"
__version__ = "1.0"




# INRAE\Olivier Vitrac - rev. 2025-01-17 (community)
# contact: olivier.vitrac@agroparistech.fr, han.chen@inrae.fr

# Revision history
# 2023-01-04 code initialization
# 2023-01-10 early alpha version
# 2023-01-11 alpha version (many fixes), wrap and align all displays with textwrap.fill, textwrap.shorten
# 2023-01-12 implement methods of keyword(units/rotate/open)
# 2023-01-18 split a script into subscripts to be executed in pipescripts
# 2023-01-19 use of LammpsGeneric.do() and hasvariables flag to manage VARIABLES
# 2023-01-20 app PythonPath management for VScode, add comments region.ellipsoid()
# 2023-01-22 todo list added
# 2023-01-24 implementation (o1 = R.E1, o2 = R.E2): o1+o2+... and o1 | o2 | ...
# 2023-01-25 full implementation of eval(), set(), get(), __setattr__(), __getattr__(), iterators
# 2023-01-26 add an example with for and join
# 2023-01-27 add coregometry.__iadd__, region.pipescript, region.script, region.do()
# 2023-01-27 true alpha version, workable with https://andeplane.github.io/atomify/
# 2023-01-31 fix browser and temporary files on Linux
# 2023-02-06 major update, internal documentation for all objects, livelammps attribute
# 2023-02-16 fix object counters, add width, height, depth to region(), data are stored in live
# 2023-02-16 add a specific >> (__rshift__) method for LammpsVariables, to be used by pipescript.do()
# 2023-02-21 add gel compression exemple, modification of the footer section to account for several beadtypes
# 2023-03-16 add emulsion, collection
# 2023-07-07 fix region.union()
# 2023-07-15 add the preffix "$" to units, fix prism and other minor issues
# 2023-07-15 (code works with the current state of Workshop4)
# 2023-07-17 avoid duplicates if union or intersect is used, early implemeantion of "move"
# 2023-07-19 add region.hasfixmove, region.livelammps.options["static" | "dynamic"]
# 2023-07-19 early design for LammpsGroup class, Group class, region.group()
# 2023-07-20 reimplement, validate and extend the original emulsion example
# 2023-07-25 add group section (not active by default)
# 2023-07-29 symmetric design for coregeometry and collection objects with flag control, implementation in pipescript
# 2023-07-29 fix for the class LammpsCollectionGroup() - previous bug resolved
# 2023-08-11 full implementation of the space-filled model such as in pizza.raster
# 2024-04-18 workshop compatible (i.e., implementation of region.scriptobject(), to be used along with region.do())
# 2024-06-14 add mass, density attributes to all region objects and region (overdefinitions are possible), natoms return the number of atoms
# 2024-06-20 debug the calculation of volume of cylinder
# 2024-07-03 full implementation of scaling in pizza.region()
# 2024-07-04 implementation of scaling with formula (when variables are used), add live attributes to region along with an updated LammpsHeader
# 2024-07-05 full implementation of natoms, geometry
# 2024-07-29 consolidation of the method scriptobject (note that a do() is required before calling scriptobject)
# 2024-08-02 community implementation
# 2024-08-31 add method R.beadtypes(), class headerbox(), method R.headerbox()
# 2024-08-01 more robust implementation via method: scriptHeaders() and headersData object
# 2024-10-08 add lattice_scale
# 2024-12-01 standarize scripting features, automatically call script/pscript methods
# 2024-12-09 fix getattr for region objects to be compatible with inspect, pdoc
# 2025-01-17 fix numpy import (it was removed)


# %% Imports and private library
import os, sys, math
import numpy as np
from datetime import datetime
from copy import copy as duplicate
from copy import deepcopy as deepduplicate
from textwrap import fill, shorten
from webbrowser import open as livelammps

# update python path if needed (for development only)
# try: pwd = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
# except NameError: pwd = os.getcwd()
# try: sys.path.index(pwd) # sys.path.insert(0, os.getcwd())
# except ValueError: sys.path.append(pwd)
# print('\n>>>',pwd,'\n')
# os.chdir(pwd)

# import struct, param, paramauto, span
from pizza.private.mstruct import *
from pizza.script import pipescript, script, scriptdata, scriptobject, span
from pizza.forcefield import *


__all__ = ['AttrErrorDict', 'Block', 'Collection', 'Cone', 'Cylinder', 'Ellipsoid', 'Evalgeometry', 'Intersect', 'LammpsCollectionGroup', 'LammpsCreate', 'LammpsFooter', 'LammpsFooterPreview', 'LammpsGeneric', 'LammpsGroup', 'LammpsHeader', 'LammpsHeaderBox', 'LammpsHeaderInit', 'LammpsHeaderLattice', 'LammpsHeaderMass', 'LammpsMove', 'LammpsRegion', 'LammpsSetGroup', 'LammpsSpacefilling', 'LammpsVariables', 'Plane', 'Prism', 'SafeEvaluator', 'Sphere', 'Union', 'cleanname', 'coregeometry', 'emulsion', 'forcefield', 'headersRegiondata', 'none', 'param', 'paramauto', 'parameterforcefield', 'pipescript', 'pstr', 'region', 'regioncollection', 'regiondata', 'rigidwall', 'saltTLSPH', 'scatter', 'script', 'scriptdata', 'scriptobject', 'smd', 'solidfood', 'span', 'struct', 'tlsph', 'ulsph', 'water', 'wrap']


# protected properties in region
protectedregionkeys = ('name', 'live', 'nbeads' 'volume', 'mass', 'radius', 'contactradius', 'velocities',
                        'forces', 'filename', 'index', 'objects', 'nobjects', 'counter','_iter_',
                        'livelammps','copy', 'hasfixmove', 'spacefilling', 'isspacefilled', 'spacefillingbeadtype','mass','density',
                        'units','center','separationdistance','regionunits',
                        'lattice_scale','lattice_style','lattice_scale_siunits', 'lattice_spacing',
                        'geometry', 'natoms', 'headersData'
                            )

# livelammps
#livelammpsURL = 'https://editor.lammps.org/'
livelammpsURL = "https://andeplane.github.io/atomify/"
livetemplate = {
    'mass':'mass		    %d 1.0',
    'pair_coeff':'pair_coeff	    %d %d 1.0 1.0 2.5',
    }
groupprefix = "GRP"  # prefix for all group IDs created from a named region
fixmoveprefix = "FM" # prefix for all fix move IDs created from a named region
# %% Low level functions
# wrap and indent text for variables
wrap = lambda k,op,v,indent,width,maxwidth: fill(
        shorten(v,width=maxwidth+indent,
        fix_sentence_endings=True),
        width=width+indent,
        initial_indent=" "*(indent-len(k)-len(op)-2)+f'{k} {op} ',
        subsequent_indent=' '*(indent+(1 if v[0]=='"' else 0) )
        )

# remove $ from variable names
cleanname = lambda name: "".join([x for x in name if x!="$"])

# %% Top generic classes for storing region data and objects
# they are not intended to be used outside script data and objects

class regiondata(paramauto):
    """
        class of script parameters
            Typical constructor:
                DEFINITIONS = regiondata(
                    var1 = value1,
                    var2 = value2
                    )
        See script, struct, param to get review all methods attached to it
    """
    _type = "RD"
    _fulltype = "region data"
    _ftype = "definition"

    def generatorforlammps(self,verbose=False,hasvariables=False):
        """
            generate LAMMPS code from regiondata (struct)
            generatorforlammps(verbose,hasvariables)
            hasvariables = False is used to prevent a call of generatorforLammps()
            for scripts others than LammpsGeneric ones
        """
        nk = len(self)
        if nk>0:
            self.sortdefinitions(raiseerror=False)
            s = self.tostruct()
            ik = 0
            fmt = "variable %s equal %s"
            cmd = "\n#"+"_"*40+"\n"+f"#[{str(datetime.now())}]\n" if verbose else ""
            cmd += f"\n# Definition of {nk} variables (URL: https://docs.lammps.org/variable.html)\n"
            if hasvariables:
                for k in s.keys():
                    ik += 1
                    end = "\n" if ik<nk else "\n"*2
                    v = getattr(s,k)
                    if v is None: v = "NULL"
                    if isinstance(v,(int,float)) or v == None:
                        cmd += fmt % (k,v)+end
                    elif isinstance(v,str):
                        cmd += fmt % (k,f'{v}')+end
                    elif isinstance(v,(list,tuple)):
                        cmd += fmt % (k,span(v))+end
                    else:
                        raise TypeError(f"unsupported type for the variable {k} set to {v}")
                if verbose: cmd += "#"+"_"*40+"\n"
        return cmd

class regioncollection(struct):
    """ regioncollection class container (not to be called directly) """
    _type = "collect"               # object type
    _fulltype = "Collections"    # full name
    _ftype = "collection"        # field name
    def __init__(self,*obj,**kwobj):
        # store the objects with their alias
        super().__init__(**kwobj)
        # store objects with their real names
        for o in obj:
            if isinstance(o,region):
                s = struct.dict2struct(o.objects)
                list_s = s.keys()
                for i in range(len(list_s)): self.setattr(list_s[i], s[i].copy())
            elif o!=None:
                self.setattr(o.name, o.copy())

# Class for headersData (added on 2024-09-01)
class headersRegiondata(regiondata):
    """
        class of script parameters
            Typical constructor:
                DEFINITIONS = headersRegiondata(
                    var1 = value1,
                    var2 = value2
                    )
        See script, struct, param to get review all methods attached to it
    """
    _type = "HRD"
    _fulltype = "Header parameters - helper for scripts"
    _ftype = "header definition"


# %% PRIVATE SUB-CLASSES
# Use the equivalent methods of raster() to call these constructors

class LammpsGeneric(script):
    """
        common class to override standard do() method from script
        LammpsVariables, LammpsRegion, LammpsCreate are LammpsGeneric
        note:: the only difference with the common script class is that
        LammpsGeneric accepts VARIABLES AND To SHOW THEM
    """
    def do(self,printflag=True,verbose=False):
        """ generate the LAMMPS code with VARIABLE definitions """
        if self.DEFINITIONS.hasvariables and hasattr(self,'VARIABLES'): # attribute VARIABLES checked 2023-08-11
            cmd = f"#[{str(datetime.now())}] {self.name} > {self.SECTIONS[0]}" \
                if verbose else ""
            if len(self.VARIABLES)>0: cmd += \
            self.VARIABLES.generatorforlammps(verbose=verbose,hasvariables=True)
        else:
            cmd = ""
        cmd += super().do(printflag=False,verbose=verbose)
        if printflag: print(cmd)
        return cmd

class LammpsVariables(LammpsGeneric):
    """
        script for LAMMPS variables section
        myvars = LammpsVariables(regiondata(var1=...),ID='....',style='....')
    """
    name = "LammpsVariables"
    SECTIONS = ["VARIABLES"]
    position = 2
    role = "variable command definition"
    description = "variable name style args"
    userid = "variable"
    version = 0.1
    verbose = True

    # Definitions used in TEMPLATE
    DEFINITIONS = scriptdata(
                    ID = "${ID}",
                 style = "${style}",
          hasvariables = True
                    )

    # Template  (using % instead of # enables replacements)
    TEMPLATE = "% variables to be used for ${ID} ${style}"

    def __init__(self,VARIABLES=regiondata(),**userdefinitions):
        """ constructor of LammpsVariables """
        super().__init__(**userdefinitions)
        self.VARIABLES = VARIABLES

    # override >>
    def __rshift__(self,s):
        """ overload right  shift operator (keep only the last template) """
        if isinstance(s,script):
            dup = deepduplicate(self) # instead of duplicate (added 2023-08-11)
            dup.DEFINITIONS = dup.DEFINITIONS + s.DEFINITIONS
            dup.USER = dup.USER + s.USER
            if self.DEFINITIONS.hasvariables and s.DEFINITIONS.hasvariables:
                dup.VARIABLES = s.VARIABLES
            dup.TEMPLATE = s.TEMPLATE
            return dup
        else:
            raise TypeError("the second operand must a script object")


class LammpsCreate(LammpsGeneric):
    """ script for LAMMPS variables section """
    name = "LammpsCreate"
    SECTIONS = ["create_atoms"]
    position = 4
    role = "create_atoms command"
    description = "create_atoms type style args keyword values ..."
    userid = "create"
    version = 0.1
    verbose = True

    # Definitions used in TEMPLATE
    DEFINITIONS = scriptdata(
                    ID = "${ID}",
                 style = "${style}",
                 hasvariables = False
                    )

    # Template (using % instead of # enables replacements)
    TEMPLATE = """
% Create atoms of type ${beadtype} for ${ID} ${style} (https://docs.lammps.org/create_atoms.html)
create_atoms ${beadtype} region ${ID}
"""

class LammpsSetGroup(LammpsGeneric):
    """ script for LAMMPS set group section """
    name = "LammpsSetGroup"
    SECTIONS = ["set group"]
    position = 4
    role = "create_atoms command"
    description = "set group groupID type beadtype"
    userid = "setgroup"
    version = 0.1
    verbose = True

    # Definitions used in TEMPLATE
    DEFINITIONS = scriptdata(
                    ID = "${ID}",
               groupID = "$"+groupprefix+"${ID}", # freeze the interpretation,
          hasvariables = False
                    )

    # Template (using % instead of # enables replacements)
    TEMPLATE = """
% Reassign atom type to ${beadtype} for the group ${groupID} associated with region ${ID} (https://docs.lammps.org/set.html)
set group ${groupID} type ${beadtype}
"""

class LammpsMove(LammpsGeneric):
    """ script for LAMMPS variables section """
    name = "LammpsMove"
    SECTIONS = ["move_fix"]
    position = 6
    role = "move along a trajectory"
    description = "fix ID group-ID move style args keyword values ..."
    userid = "move"
    version = 0.2
    verbose = True

    # Definitions used in TEMPLATE
    DEFINITIONS = scriptdata(
                    ID = "${ID}",
                moveID = "$"+fixmoveprefix+"${ID}", # freeze the interpretation
               groupID = "$"+groupprefix+"${ID}", # freeze the interpretation
                 style = "${style}",
                  args = "${args}",
          hasvariables = False
                    )

    # Template (using % instead of # enables replacements)
    TEMPLATE = """
# Move atoms fix ID group-ID move style args keyword values (https://docs.lammps.org/fix_move.html)
% move_fix for group ${groupID} using ${style}
% prefix "g" added to ${ID} to indicate a group of atoms
% prefix "fm" added to ${ID} to indicate the ID of the fix move
fix ${moveID} ${groupID} move ${style} ${args}
"""


class LammpsRegion(LammpsGeneric):
    """ generic region based on script """
    name = "LammpsRegion"
    SECTIONS = ["REGION"]
    position = 3
    role = "region command definition"
    description = "region ID style args keyword arg"
    userid = "region"              # user name
    version = 0.1                  # version
    verbose = True

    # DEFINITIONS USED IN TEMPLATE
    DEFINITIONS = scriptdata(
                    ID = "${ID}",
                 style = "${style}",
                  args = "${args}",
                  side = "${side}",
                 units = "${units}",
                  move = "${move}",
                rotate = "${rotate}",
                  open = "${open}",
          hasvariables = False
                    )

    # Template  (using % instead of # enables replacements)
    TEMPLATE = """
% Create region ${ID} ${style} args ...  (URL: https://docs.lammps.org/region.html)
# keywords: side, units, move, rotate, open
# values: in|out, lattice|box, v_x v_y v_z, v_theta Px Py Pz Rx Ry Rz, integer
region ${ID} ${style} ${args} ${side}${units}${move}${rotate}${open}
"""


class LammpsGroup(LammpsGeneric):
    """ generic group class based on script """
    name = "LammpsGroup"
    SECTIONS = ["GROUP"]
    position = 5
    role = "group command definition"
    description = "group ID region regionID"
    userid = "region"              # user name
    version = 0.2                  # version
    verbose = True

    # DEFINITIONS USED IN TEMPLATE
    DEFINITIONS = scriptdata(
                    ID = "${ID}",
               groupID = "$"+groupprefix+"${ID}", # freeze the interpretation
          countgroupID = "$count"+"${groupID}", # either using $
           grouptoshow = ["${groupID}"], # or []
                 hasvariables = False
                    )

    # Template  (using % instead of # enables replacements)
    TEMPLATE = """
% Create group ${groupID} region ${ID} (URL: https://docs.lammps.org/group.html)
group ${groupID} region ${ID}
variable ${countgroupID} equal count(${grouptoshow})
print "Number of atoms in ${groupID}: \${{countgroupID}}"
"""


class LammpsCollectionGroup(LammpsGeneric):
    """ Collection group class based on script """
    name = "LammpsCollection Group"
    SECTIONS = ["COLLECTIONGROUP"]
    position = 6
    role = "group command definition for a collection"
    description = "group ID union regionID1 regionID2..."
    userid = "collectionregion"              # user name
    version = 0.3                            # version
    verbose = True

    # DEFINITIONS USED IN TEMPLATE
    DEFINITIONS = scriptdata(
                    ID = "${ID}",
               groupID = "$"+groupprefix+"${ID}", # freeze the interpretation
          hasvariables = False
                    )

    # Template  (ID is spanned over all regionIDs)
    TEMPLATE = """
% Create group ${groupID} region ${ID} (URL: https://docs.lammps.org/group.html)
group ${groupID} union ${ID}
"""

class LammpsHeader(LammpsGeneric):
    """ generic header for pizza.region """
    name = "LammpsHeader"
    SECTIONS = ["HEADER"]
    position = 0
    role = "header for live view"
    description = "To be used with https://editor.lammps.org/"
    userid = "header"              # user name
    version = 0.1                  # version
    verbose = False

    # DEFINITIONS USED IN TEMPLATE
    DEFINITIONS = scriptdata(
                    width = 10,
                   height = 10,
                    depth = 10,
                    nbeads = 1,
            hasvariables = False
                    )

    # Template
    TEMPLATE = """
# --------------[    INIT   ]--------------
# assuming generic LJ units and style
units           ${live_units}
atom_style	    ${live_atom_style}
lattice		    ${live_lattice_style} ${live_lattice_scale}
# ------------------------------------------

# --------------[    B O X   ]--------------
variable        halfwidth equal ${width}/2
variable        halfheight equal ${height}/2
variable        halfdepth equal ${depth}/2
region box block -${halfwidth} ${halfwidth} -${halfheight} ${halfheight} -${halfdepth} ${halfdepth}
create_box	${nbeads} box
# ------------------------------------------
"""

class LammpsHeaderInit(LammpsGeneric): # --- helper script ---
    """
    Generates an initialization header script for a pizza.region object in LAMMPS.

    This class constructs a LAMMPS header based on user-defined properties stored
    in `R.headersData` of the pizza.region object. Properties set to `None` or an
    empty string will be omitted from the script.

    Attributes:
        DEFINITIONS: Defines the parameters like dimension, units, boundary, etc.,
        that can be set in `R.headersData`.

    Methods:
        __init__(persistentfile=True, persistentfolder=None, **userdefinitions):
            Initializes the header script and sets up the `USER` attribute.

        generate_template():
            Creates the header template based on the provided `USER` definitions.

    Note: This class is primarily intended for internal use within the simulation setup.
    """
    name = "LammpsHeaderBox"
    SECTIONS = ["HEADER"]
    position = -2
    role = "initialization header for pizza.region"
    description = "helper method"
    userid = "headerinit"          # user name
    version = 0.1                  # version
    verbose = False

    # DEFINITIONS USED IN TEMPLATE
    # circular references (the variable is defined by its field in USER of class regiondata)
    # are not needed but this explicits the requirements.
    # All fields are stored in R.headersData with R a region object.
    # Use R.headersData.property = value to assign a value
    # Use R.headersData.property = None or "" to prevent the initialization of property
    DEFINITIONS = scriptdata(
                regionname = "${name}",
                 dimension = "${dimension}",
                     units = "${units}",
                  boundary = "${boundary}",
                atom_style = "${atom_style}",
               atom_modify = "${atom_modify}",
               comm_modify = "${comm_modify}",
              neigh_modify = "${neigh_modify}",
                    newton = "${newton}",
            hasvariables = False
                    )

    def __init__(self, persistentfile=True, persistentfolder=None, **userdefinitions):
        """Constructor adding instance definitions stored in USER."""
        super().__init__(persistentfile, persistentfolder, **userdefinitions)
        self.generate_template()

    def generate_template(self):
        """Generate the TEMPLATE based on USER definitions."""
        self.TEMPLATE = """
% --------------[ Initialization for <${name}:${boxid}>   ]--------------
    """
        self.TEMPLATE += '# set a parameter to None or "" to remove the definition\n'
        if self.USER.dimension:   self.TEMPLATE += "dimension    ${dimension}\n"
        if self.USER.units:       self.TEMPLATE += "units        ${units}\n"
        if self.USER.boundary:    self.TEMPLATE += "boundary     ${boundary}\n"
        if self.USER.atom_style:  self.TEMPLATE += "atom_style   ${atom_style}\n"
        if self.USER.atom_modify: self.TEMPLATE += "atom_modify  ${atom_modify}\n"
        if self.USER.comm_modify: self.TEMPLATE += "comm_modify  ${comm_modify}\n"
        if self.USER.neigh_modify:self.TEMPLATE += "neigh_modify ${neigh_modify}\n"
        if self.USER.newton:      self.TEMPLATE += "newton       ${newton}\n"
        self.TEMPLATE += "# ------------------------------------------\n"


class LammpsHeaderLattice(LammpsGeneric): # --- helper script ---
    """
        Lattice header for pizza.region

        Use R.headersData.property = value to assign a value
        with R a pizza.region object
    """
    name = "LammpsHeaderLattice"
    SECTIONS = ["HEADER"]
    position = 0
    role = "lattice header for pizza.region"
    description = "helper method"
    userid = "headerlattice"       # user name
    version = 0.1                  # version
    verbose = False

    # DEFINITIONS USED IN TEMPLATE
    # circular references (the variable is defined by its field in USER of class regiondata)
    # are not needed but this explicits the requirements.
    # All fields are stored in R.headersData with R a region object.
    # Use R.headersData.property = value to assign a value
    DEFINITIONS = scriptdata(
             lattice_style = "${lattice_style}",
             lattice_scale = "${lattice_scale}",
            hasvariables = False
                    )
    def __init__(self, persistentfile=True, persistentfolder=None, **userdefinitions):
        """Constructor adding instance definitions stored in USER."""
        super().__init__(persistentfile, persistentfolder, **userdefinitions)
        self.generate_template()

    def generate_template(self):
        """Generate the TEMPLATE based on USER definitions."""
        self.TEMPLATE = "\n% --------------[ Lattice for <${name}:${boxid}>, style=${lattice_style}, scale=${lattice_scale} ]--------------\n"
        if self.USER.lattice_spacing is None:
            self.TEMPLATE += "lattice ${lattice_style} ${lattice_scale}\n"
        else:
            self.TEMPLATE += "lattice ${lattice_style} ${lattice_scale} spacing ${lattice_spacing}\n"
        self.TEMPLATE += "# ------------------------------------------\n"


class LammpsHeaderBox(LammpsGeneric): # --- helper script ---
    """
        Box header for pizza.region

        Use R.headersData.property = value to assign a value
        with R a pizza.region object
    """
    name = "LammpsHeaderBox"
    SECTIONS = ["HEADER"]
    position = 0
    role = "box header for pizza.region"
    description = "helper method"
    userid = "headerbox"           # user name
    version = 0.1                  # version
    verbose = False

    # DEFINITIONS USED IN TEMPLATE
    # circular references (the variable is defined by its field in USER of class regiondata)
    # are not needed but this explicits the requirements.
    # All fields are stored in R.headersData with R a region object.
    # Use R.headersData.property = value to assign a value
    # Extra arguments
    #   ${boxid_arg} is by default "box"
    #   ${boxunits_arg} can be "", "units lattice", "units box"
    DEFINITIONS = scriptdata(
                      name = "${name}",
                      xmin = "${xmin}",
                      xmax = "${xmax}",
                      ymin = "${ymin}",
                      ymax = "${ymax}",
                      zmin = "${zmin}",
                      zmax = "${zmax}",
                    nbeads = "${nbeads}",
                     boxid = "${boxid}",
              boxunits_arg = "",     # default units
            hasvariables = False
                    )

    # Template
    TEMPLATE = """
% --------------[ Box for <${name}:${boxid}> incl. ${nbeads} bead types ]--------------
region ${boxid} block ${xmin} ${xmax} ${ymin} ${ymax} ${zmin} ${zmax} ${boxunits_arg}
create_box	${nbeads} ${boxid}
# ------------------------------------------
"""

class LammpsHeaderMass(LammpsGeneric):
    """
    Mass assignment header for pizza.region.

    Use R.headersData.property = value to assign a value
    with R a pizza.region object.
    """
    name = "LammpsHeaderMass"
    SECTIONS = ["HEADER"]
    position = 2  # Positioned after other headers like Box and Lattice
    role = "mass assignment header for pizza.region"
    description = "Assigns masses to bead types based on nbeads and default mass."
    userid = "headermass"  # User identifier
    version = 0.1
    verbose = False

    # DEFINITIONS USED IN TEMPLATE
    # All fields are stored in R.headersData with R a region object.
    # Use R.headersData.property = value to assign a value.
    # Mass overrides are provided via the 'mass' keyword argument as a list or tuple.
    DEFINITIONS = scriptdata(
        nbeads="${nbeads}",  # these default values are not used
        mass="${mass}",      # but reported for records
        hasvariables=False
    )

    def __init__(self, persistentfile=True, persistentfolder=None, **userdefinitions):
        """
            Constructor adding instance definitions stored in USER.

            Parameters:
                persistentfile (bool, optional): Whether to use a persistent file. Defaults to True.
                persistentfolder (str, optional): Folder path for persistent files. Defaults to None.
                **userdefinitions: Arbitrary keyword arguments for user definitions.
                    - mass (list or tuple, optional): List or tuple to override masses for specific bead types.
                      Example: mass=[1.2, 1.0, 0.8] assigns mass 1.2 to bead type 1, 1.0 to bead type 2,
                      and 0.8 to bead type 3.
        """
        super().__init__(persistentfile, persistentfolder, **userdefinitions)
        self.generate_template()

    def generate_template(self):
        """
            Generate the TEMPLATE for mass assignments based on USER definitions.

            The method constructs mass assignments for each bead type. If `mass` overrides
            are provided as a list or tuple, it assigns the specified mass to the corresponding
            bead types. Otherwise, it uses the default `mass` value from `USER.headersData.mass`.
        """
        # Retrieve user-defined parameters
        nbeads = self.USER.nbeads
        mass = self.USER.mass
        # Validate mass
        if not isinstance(mass, (list, tuple)): mass = [mass]  # Convert single value to a list
        if len(mass) > nbeads:
            mass = mass[:nbeads]  # Truncate excess entries
        elif len(mass) < nbeads:
            last_mass = mass[-1]  # Repeat the last value for missing entries
            mass += [last_mass] * (nbeads - len(mass))
        # Initialize TEMPLATE with header comment
        self.TEMPLATE = "\n% --------------[ Mass Assignments for <${name}:${boxid}>" + f" (nbeads={nbeads}) " +" ]--------------\n"
        # Iterate over bead types and assign masses
        for bead_type in range(1, nbeads + 1):
            bead_mass = mass[bead_type - 1]
            if isinstance(bead_mass, str):
                # If mass is a string (e.g., formula), ensure proper formatting
                mass_str = f"({bead_mass})"
            else:
                # If mass is a numeric value, convert to string
                mass_str = f"{bead_mass}"
            self.TEMPLATE += f"mass {bead_type} {mass_str}\n"
        # Close the TEMPLATE with a comment
        self.TEMPLATE += "# ------------------------------------------\n"


class LammpsFooterPreview(LammpsGeneric): # --- helper script ---
    """
        Box header for pizza.region

        Use R.headersData.property = value to assign a value
        with R a pizza.region object
    """
    name = "LammpsFooterPreview"
    SECTIONS = ["Footer"]
    position = 0
    role = "box footer for pizza.region"
    description = "helper method"
    userid = "footerpreview"       # user name
    version = 0.1                  # version
    verbose = False

    # DEFINITIONS USED IN TEMPLATE
    # circular references (the variable is defined by its field in USER of class regiondata)
    # are not needed but this explicits the requirements.
    # All fields are stored in R.headersData with R a region object.
    # Use R.headersData.property = value to assign a value
    # Extra arguments
    #   ${boxid_arg} is by default "box"
    #   ${boxunits_arg} can be "", "units lattice", "units box"
    DEFINITIONS = scriptdata(
                filename = "${previewfilename}",
            hasvariables = False
                    )

    # Template
    TEMPLATE = """
% --------------[ Preview for <${name}:${boxid}> incl. ${nbeads} bead types ]--------------
% Output the initial geometry to a dump file "${previewfilename}" for visualization
dump initial_dump all custom 1 ${previewfilename} id type x y z
run 0
# ------------------------------------------
"""

class LammpsSpacefilling(LammpsGeneric):
    """ Spacefilling script: fill space with a block """
    name = "LammpsSpacefilling"
    SECTIONS = ["SPACEFILLING"]
    position = 1
    role = "fill space with fillingbeadtype atoms"
    description = 'fill the whole space (region "filledspace") with default atoms (beadtype)'
    userid = "spacefilling"              # user name
    version = 0.1                        # version
    verbose = False

    # DEFINITIONS USED IN TEMPLATE
    DEFINITIONS = scriptdata(
             fillingunits = "${fillingunits}",
             fillingwidth = "${fillingwidth}",
            fillingheight = "${fillingheight}",
             fillingdepth = "${fillingdepth}",
               fillingxlo = "-${fillingwidth}/2",
               fillingxhi = "${fillingwidth}/2",
               fillingylo = "-${fillingheight}/2",
               fillingyhi = "${fillingheight}/2",
               fillingzlo = "-${fillingdepth}/2",
               fillingzhi = "${fillingdepth}/2",
          fillingbeadtype = "${fillingbeadtype}",
             fillingstyle = "${block}",
             hasvariables = False
                    )

    # Template
    TEMPLATE = """
region filledspace ${fillingstyle} ${fillingxlo} ${fillingxhi} ${fillingylo} ${fillingyhi} ${fillingzlo} ${fillingzhi}
create_atoms ${fillingbeadtype} region filledspace
# ------------------------------------------
"""

class LammpsFooter(LammpsGeneric):
    """ generic header for pizza.region """
    name = "LammpsFooter"
    SECTIONS = ["FOOTER"]
    position = 1000
    role = "footer for live view"
    description = "To be used with https://editor.lammps.org/"
    userid = "footer"              # user name
    version = 0.1                  # version
    verbose = False

    # DEFINITIONS USED IN TEMPLATE
    DEFINITIONS = scriptdata(
                      run = 1,
             hasvariables = False
                    )

    # Template
    TEMPLATE = """
# --------------[  DYNAMICS  ]--------------
${mass}
velocity	    all create 1.44 87287 loop geom
pair_style	    lj/cut 2.5
${pair_coeff}
neighbor	    0.3 bin
neigh_modify	delay 0 every 20 check no
fix		        1 all nve
run		        ${run}
# ------------------------------------------
"""

class coregeometry:
    """
        core geometry object
        (helper class for attributes, side,units, move, rotate, open)

        SECTIONS store scripts (variables, region and create for the geometry)
        USER = common USER definitions for the three scripts
        VARIABLES = variables definitions (used by variables only)
        update() propagate USER to the three scripts
        script returns SECTIONS as a pipescript
        do() generate the script

        Parameters to be used along scriptobject()
                 style
            forcefield
                 group
        They are stored SCRIPTOBJECT_USER

    """

    _version = "0.35"
    __custom_documentations__ = "pizza.region.coregeometry class"


    def __init__(self,USER=regiondata(),VARIABLES=regiondata(),
                 hasgroup=False, hasmove=False, spacefilling=False,
                 style="smd",
                 forcefield=rigidwall(),
                 group=[],
                 mass=1, density=1,
                 lattice_style="sc", lattice_scale=1, lattice_scale_siunits=1 # added on 2024-07-05
                 ):
        """
            constructor of the generic core geometry
                USER: any definitions requires by the geometry
           VARIABLES: variables used to define the geometry (to be used in LAMMPS)
           hasgroup, hasmove: flag to force the sections group and move
           SECTIONS: they must be PIZZA.script

           The flag spacefilling is true of the container of objects (class region) is filled with beads
        """
        self.USER = USER
        self.SECTIONS = {
            'variables': LammpsVariables(VARIABLES,**USER),
               'region': LammpsRegion(**USER),
               'create': LammpsCreate(**USER),
                'group': LammpsGroup(**USER),
             'setgroup': LammpsSetGroup(**USER),
                 'move': LammpsMove(**USER)
            }
        self.FLAGSECTIONS = {
            'variables': True,
               'region': True,
               'create': not spacefilling,
                'group': hasgroup,
             'setgroup': spacefilling,
                 'move': hasmove
            }
        self.spacefilling = spacefilling

        # add comptaibility with scriptobjects
        self.SCRIPTOBJECT_USER = {
                 'style': style,
            'forcefield': forcefield,
                 'group': group
            }
        # collect information from parent region
        self.mass = mass
        self.density = density
        self.lattice_style = lattice_style
        self.lattice_scale = lattice_scale
        self.lattice_scale_siunits = lattice_scale_siunits

    def update(self):
        """ update the USER content for all three scripts """
        if isinstance(self.SECTIONS["variables"],script):
            self.SECTIONS["variables"].USER += self.USER
        if isinstance(self.SECTIONS["region"],script):
            self.SECTIONS["region"].USER += self.USER
        if isinstance(self.SECTIONS["create"],script):
            self.SECTIONS["create"].USER += self.USER
        if isinstance(self.SECTIONS["group"],script):
            self.SECTIONS["group"].USER += self.USER
        if isinstance(self.SECTIONS["setgroup"],script):
            self.SECTIONS["setgroup"].USER += self.USER
        if isinstance(self.SECTIONS["move"],script):
            self.SECTIONS["move"].USER += self.USER


    def copy(self,beadtype=None,name=""):
        """ returns a copy of the graphical object """
        if self.alike != "mixed":
            dup = deepduplicate(self)
            if beadtype != None: # update beadtype
                dup.beadtype = beadtype
            if name != "": # update name
                dup.name = name
            return dup
        else:
            raise ValueError("collections cannot be copied, regenerate the collection instead")


    def creategroup(self):
        """  force the group creation in script """
        self.FLAGSECTIONS["group"] = True

    def setgroup(self):
        """  force the group creation in script """
        self.FLAGSECTIONS["setgroup"] = True

    def createmove(self):
        """  force the fix move creation in script """
        self.FLAGSECTIONS["move"] = True

    def removegroup(self):
        """  force the group creation in script """
        self.FLAGSECTIONS["group"] = False

    def removemove(self):
        """  force the fix move creation in script """
        self.FLAGSECTIONS["move"] = False

    def scriptobject(self, beadtype=None, name=None, fullname=None, group=None, style=None, forcefield=None, USER = scriptdata()):
        """
        Method to return a scriptobject based on region instead of an input file
        Syntax similar to script.scriptobject
        OBJ = scriptobject(...)
        Implemented properties:
            beadtype=1,2,...
            name="short name"
            fullname = "comprehensive name"
            style = "smd"
            forcefield = any valid forcefield instance (default = rigidwall())
        """
        # Set defaults using instance attributes if parameters are None
        if beadtype is None:
            beadtype = self.beadtype
        if name is None:
            name = f"{self.name} bead"
        if fullname is None:
            fullname = f"beads of type {self.beadtype} | object {self.name} of kind region.{self.kind}"
        if group is None:
            group = self.SCRIPTOBJECT_USER["group"]
        if style is None:
            style = self.SCRIPTOBJECT_USER["style"]
        if forcefield is None:
            style = self.SCRIPTOBJECT_USER["forcefield"]
        return scriptobject(
            beadtype=beadtype,
            name=name,
            fullname=fullname,
            style=style,
            group=group,
            filename=None,  # No need for a file
            USER = USER
        )

    @property
    def hasvariables(self):
        """ return the flag VARIABLES """
        return isinstance(self.SECTIONS["variables"],script) \
               and self.FLAGSECTIONS["variables"]

    @property
    def hasregion(self):
        """ return the flag REGION """
        return isinstance(self.SECTIONS["region"],script) \
               and self.FLAGSECTIONS["region"]

    @property
    def hascreate(self):
        """ return the flag CREATE """
        return isinstance(self.SECTIONS["create"],script) \
               and self.FLAGSECTIONS["create"] \
               and (not self.spacefilling)

    @property
    def hasgroup(self):
        """ return the flag GROUP """
        return isinstance(self.SECTIONS["group"],script) \
               and self.FLAGSECTIONS["group"]

    @property
    def hassetgroup(self):
        """ return the flag GROUP """
        return isinstance(self.SECTIONS["setgroup"],script) \
               and self.FLAGSECTIONS["setgroup"] \
               and self.hasgroup \
               and (not self.hascreate)

    @property
    def hasmove(self):
        """ return the flag MOVE """
        return isinstance(self.SECTIONS["move"],script) \
               and self.FLAGSECTIONS["move"]

    @property
    def isspacefilled(self):
        """ return the flag spacefilling """
        return isinstance(self.SECTIONS["spacefilling"],script) \
               and self.FLAGSECTIONS["spacefilling"]

    @property
    def flags(self):
        """ return a list of all flags that are currently set """
        flag_names = list(self.SECTIONS.keys())
        return [flag for flag in flag_names if getattr(self, f"has{flag}")]

    @property
    def shortflags(self):
        """ return a string made from the first letter of each set flag """
        return "".join([flag[0] for flag in self.flags])


    @property
    def VARIABLES(self):
        """ return variables """
        if isinstance(self.SECTIONS["variables"],script):
            return self.SECTIONS["variables"].VARIABLES
        else:
            v = regiondata()
            for i in range(len(self.SECTIONS["variables"].scripts)):
                v = v + self.SECTIONS["variables"].scripts[i].VARIABLES
            return v

    @property
    def script(self):
        """ generates a pipe script from sections """
        self.update()
        ptmp = self.SECTIONS["variables"] if self.hasvariables else None
        if self.hasregion:
            ptmp = self.SECTIONS["region"] if ptmp is None else ptmp | self.SECTIONS["region"]
        if self.hascreate:
            ptmp = self.SECTIONS["create"] if ptmp is None else ptmp | self.SECTIONS["create"]
        if self.hasgroup:
            ptmp = self.SECTIONS["group"] if ptmp is None else ptmp | self.SECTIONS["group"]
        if self.hassetgroup:
            ptmp = self.SECTIONS["setgroup"] if ptmp is None else ptmp | self.SECTIONS["setgroup"]
        if self.hasmove:
            ptmp = self.SECTIONS["move"] if ptmp is None else ptmp | self.SECTIONS["move"]
        return ptmp
        # before 2023-07-17
        #return self.SECTIONS["variables"] | self.SECTIONS["region"] | self.SECTIONS["create"]

    def do(self,printflag=False,verbosity=1):
        """ generates a script """
        p = self.script # intentional, force script before do(), comment added on 2023-07-17
        cmd = p.do(printflag=printflag,verbosity=verbosity)
        # if printflag: print(cmd)
        return cmd

    def __repr__(self):
        """ display method"""
        nVAR = len(self.VARIABLES)
        print("%s - %s object - beadtype=%d " % (self.name, self.kind,self.beadtype))
        if hasattr(self,"filename"): print(f'\tfilename: "{self.filename}"')
        if nVAR>0:
            print(f"\t<-- {nVAR} variables are defined -->")
            print(f"\tUse {self.name}.VARIABLES to see details and their evaluation")
            for k,v in self.VARIABLES.items():
                v0 = '"'+v+'"' if isinstance(v,str) else repr(v)
                print(wrap(k,"=",v0,20,40,80))
        print("\t<-- keyword arg -->")
        haskeys = False
        for k in ("side","move","units","rotate","open"):
            if k in self.USER:
                v = self.USER.getattr(k)
                if v != "":
                    print(wrap(k,":",v[1:],20,60,80))
                    haskeys = True
        if not haskeys: print(wrap("no keywords","<","from side|move|units|rotate|open",20,60,80))
        flags = self.flags
        if flags: print(f'defined scripts: {span(flags,sep=",")}',"\n")
        print("\n"+self.geometry) # added 2024-07-05
        return "%s object: %s (beadtype=%d)" % (self.kind,self.name,self.beadtype)


    # ~~~~ validator for region arguments (the implementation is specific and not generic as fix move ones)
    def sidearg(self,side):
        """
            Validation of side arguments for region command (https://docs.lammps.org/region.html)
            side value = in or out
              in = the region is inside the specified geometry
              out = the region is outside the specified geometry
        """
        prefix = "$"
        if side is None:
            return ""
        elif isinstance(side, str):
            side = side.lower()
            if side in ("in","out"):
                return f"{prefix} side {side}"
            elif side in ("","none"):
                return ""
            else:
                raise ValueError(f'the value of side: "{side}" is not recognized')
        else:
            raise ValueError('the parameter side can be "in|out|None"')

    def movearg(self,move):
        """
            Validation of move arguments for region command (https://docs.lammps.org/region.html)
            move args = v_x v_y v_z
              v_x,v_y,v_z = equal-style variables for x,y,z displacement of region over time (distance units)
        """
        prefix = "$"
        if move is None:
            return ""
        elif isinstance(move, str):
            move = move.lower()
            if move in("","none"):
                return ""
            else:
                return f"{prefix} move {move}"
        elif isinstance(move,(list,tuple)):
            if len(move)<3:
                print("NULL will be added to move")
            elif len(move)>3:
                print("move will be truncated to 3 elements")
            movevalid = ["NULL","NULL","NULL"]
            for i in range(min(3,len(move))):
                if isinstance(move[i],str):
                    if move[i].upper()!="NULL":
                        if prefix in move[i]:
                            # we assume a numeric result after evaluation
                            # Pizza variables will be evaluated
                            # formateval for the evaluation of ${}
                            # eval for residual expressions
                            movevalid[i] = round(eval(self.VARIABLES.formateval(move[i])),6)
                        else:
                            # we assume a variable (LAMMPS variable, not Pizza ones)
                            movevalid[i] = "v_" + move[i]
                elif not isinstance(move[i],(int,float)):
                    if (move[i] is not None):
                        raise TypeError("move values should be str, int or float")
            return f"{prefix} move {span(movevalid)}"
        else:
            raise TypeError("the parameter move should be a list or tuple")

    def unitsarg(self,units):
        """
            Validation for units arguments for region command (https://docs.lammps.org/region.html)
            units value = lattice or box
              lattice = the geometry is defined in lattice units
              box = the geometry is defined in simulation box units
        """
        prefix = "$"
        if units is None:
            return ""
        elif isinstance(units,str):
            units = units.lower()
            if units in ("lattice","box"):
                return f"{prefix} units {units}"
            elif (units=="") or (units=="none"):
                return ""
            else:
                raise ValueError(f'the value of side: "{units}" is not recognized')
        else:
            raise TypeError('the parameter units can be "lattice|box|None"')

    def rotatearg(self,rotate):
        """
            Validation of rotate arguments for region command (https://docs.lammps.org/region.html)
            rotate args = v_theta Px Py Pz Rx Ry Rz
              v_theta = equal-style variable for rotaton of region over time (in radians)
              Px,Py,Pz = origin for axis of rotation (distance units)
              Rx,Ry,Rz = axis of rotation vector
        """
        prefix = "$"
        if rotate is None:
            return ""
        elif isinstance(rotate, str):
            rotate = rotate.lower()
            if rotate in ("","none",None):
                return ""
            else:
                return f"{prefix} rotate {rotate}"
        elif isinstance(rotate,(list,tuple)):
            if len(rotate)<7:
                print("NULL will be added to rotate")
            elif len(rotate)>7:
                print("rotate will be truncated to 7 elements")
            rotatevalid = ["NULL"]*7
            for i in range(min(7,len(rotate))):
                if isinstance(rotate[i],str):
                    if rotate[i].upper()!="NULL":
                        if prefix in rotate[i]:
                            rotatevalid[i] = round(eval(self.VARIABLES.formateval(rotate[i])),6)
                        else:
                            rotatevalid[i] = rotate[i]
                elif not isinstance(rotate[i],(int,float)):
                    if (rotate[i] is not None):
                        raise TypeError("rotate values should be str, int or float")
            return f"{prefix} move {span(rotatevalid)}"
        else:
            raise TypeError("the parameter rotate should be a list or tuple")

    def openarg(self,open):
        """
            Validation of open arguments for region command (https://docs.lammps.org/region.html)
            open value = integer from 1-6 corresponding to face index (see below)
            The indices specified as part of the open keyword have the following meanings:

            For style block, indices 1-6 correspond to the xlo, xhi, ylo, yhi, zlo, zhi surfaces of the block.
            I.e. 1 is the yz plane at x = xlo, 2 is the yz-plane at x = xhi, 3 is the xz plane at y = ylo,
            4 is the xz plane at y = yhi, 5 is the xy plane at z = zlo, 6 is the xy plane at z = zhi).
            In the second-to-last example above, the region is a box open at both xy planes.

            For style prism, values 1-6 have the same mapping as for style block.
            I.e. in an untilted prism, open indices correspond to the xlo, xhi, ylo, yhi, zlo, zhi surfaces.

            For style cylinder, index 1 corresponds to the flat end cap at the low coordinate along the cylinder axis,
            index 2 corresponds to the high-coordinate flat end cap along the cylinder axis, and index 3 is the curved
            cylinder surface. For example, a cylinder region with open 1 open 2 keywords will be open at both ends
            (e.g. a section of pipe), regardless of the cylinder orientation.
        """
        prefix = "$"
        if open in ("","none",None):
            return ""
        elif isinstance(open, str):
            raise TypeError(" the parameter open should be an integer or a list/tuple of integers from 1-6")
        elif isinstance(open, int):
            if open in range(1,7):
                return f"{prefix} open {open}"
            else:
                raise TypeError(" open value should be integer from 1-6")
        elif isinstance(open, (list,tuple)):
            openvalid = [f"{prefix} open {i}" for i in range(1,7) if i in open]
            return f"$ {span(openvalid)}"
    # ~~~~ end validator for region arguments

    # ~~~~ validator for fix move arguments (implemented generically on 2023-07-17)
    def fixmoveargvalidator(self, argtype, arg, arglen):
        """
            Validation of arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html)

            LAMMPS syntax:
                fix ID group-ID move style args
                - linear args = Vx Vy Vz
                - wiggle args = Ax Ay Az period
                - rotate args = Px Py Pz Rx Ry Rz period
                - transrot args = Vx Vy Vz Px Py Pz Rx Ry Rz period
                - variable args = v_dx v_dy v_dz v_vx v_vy v_vz

            Args:
                argtype: Type of the argument (linear, wiggle, rotate, transrot, variable)
                arg: The argument to validate
                arglen: Expected length of the argument
        """
        prefix = "$"
        if arg in ("","none",None):
            return ""
        elif isinstance(arg,(list,tuple)):
            if len(arg) < arglen:
                print(f"NULL will be added to {argtype}")
            elif len(arg) > arglen:
                print(f"{argtype} will be truncated to {arglen} elements")
            argvalid = ["NULL"]*arglen
            for i in range(min(arglen,len(arg))):
                if isinstance(arg[i],str):
                    if arg[i].upper()!="NULL":
                        if prefix in arg[i]:
                            argvalid[i] = round(eval(self.VARIABLES.formateval(arg[i])),6)
                        else:
                            argvalid[i] = arg[i]
                elif not isinstance(arg[i],(int,float)):
                    if (arg[i] is not None):
                        raise TypeError(f"{argtype} values should be str, int or float")
            return f"{prefix} move {span(argvalid)}"
        else:
            raise TypeError(f"the parameter {argtype} should be a list or tuple")


    def fixmoveargs(self, linear=None, wiggle=None, rotate=None, transrot=None, variable=None):
        """
            Validates all arguments for fix move command in LAMMPS (https://docs.lammps.org/fix_move.html)
            the result is adictionary, all fixmove can be combined
        """
        argsdict = {
            "linear": [linear, 3],
            "wiggle": [wiggle, 4],
            "rotate": [rotate, 7],
            "transrot": [transrot, 10],
            "variable": [variable, 6]
        }

        for argtype, arginfo in argsdict.items():
            arg, arglen = arginfo
            if arg is not None:
                argsdict[argtype] = self.fixmoveargvalidator(argtype, arg, arglen)
        return argsdict


    def get_fixmovesyntax(self, argtype=None):
        """
        Returns the syntax for LAMMPS command, or detailed explanation for a specific argument type

        Args:
        argtype: Optional; Type of the argument (linear, wiggle, rotate, transrot, variable)
        """
        syntax = {
            "linear": "linear args = Vx Vy Vz\n"
                      "Vx,Vy,Vz = components of velocity vector (velocity units), any component can be specified as NULL",
            "wiggle": "wiggle args = Ax Ay Az period\n"
                       "Ax,Ay,Az = components of amplitude vector (distance units), any component can be specified as NULL\n"
                       "period = period of oscillation (time units)",
            "rotate": "rotate args = Px Py Pz Rx Ry Rz period\n"
                       "Px,Py,Pz = origin point of axis of rotation (distance units)\n"
                       "Rx,Ry,Rz = axis of rotation vector\n"
                       "period = period of rotation (time units)",
            "transrot": "transrot args = Vx Vy Vz Px Py Pz Rx Ry Rz period\n"
                        "Vx,Vy,Vz = components of velocity vector (velocity units)\n"
                        "Px,Py,Pz = origin point of axis of rotation (distance units)\n"
                        "Rx,Ry,Rz = axis of rotation vector\n"
                        "period = period of rotation (time units)",
            "variable": "variable args = v_dx v_dy v_dz v_vx v_vy v_vz\n"
                        "v_dx,v_dy,v_dz = 3 variable names that calculate x,y,z displacement as function of time, any component can be specified as NULL\n"
                        "v_vx,v_vy,v_vz = 3 variable names that calculate x,y,z velocity as function of time, any component can be specified as NULL",
        }

        base_syntax = (
            "fix ID group-ID move style args\n"
            " - linear args = Vx Vy Vz\n"
            " - wiggle args = Ax Ay Az period\n"
            " - rotate args = Px Py Pz Rx Ry Rz period\n"
            " - transrot args = Vx Vy Vz Px Py Pz Rx Ry Rz period\n"
            " - variable args = v_dx v_dy v_dz v_vx v_vy v_vz\n\n"
            'use get_movesyntax("movemethod") for details'
            "manual: https://docs.lammps.org/fix_move.html"
        )

        return syntax.get(argtype, base_syntax)

    # ~~~~ end validator for fix move arguments

    def __add__(self,C):
        """ overload addition ("+") operator """
        if isinstance(C,coregeometry):
            dup = deepduplicate(self)
            dup.name = cleanname(self.name) +"+"+ cleanname(C.name)
            dup.USER = dup.USER + C.USER
            dup.USER.ID = "$" + cleanname(self.USER.ID) +"+"+ cleanname(C.USER.ID)
            dup.SECTIONS["variables"] = dup.SECTIONS["variables"] + C.SECTIONS["variables"]
            dup.SECTIONS["region"] = dup.SECTIONS["region"] + C.SECTIONS["region"]
            dup.SECTIONS["create"] = dup.SECTIONS["create"] + C.SECTIONS["create"]
            dup.SECTIONS["group"] = dup.SECTIONS["group"] + C.SECTIONS["group"]
            dup.SECTIONS["move"] = dup.SECTIONS["move"] + C.SECTIONS["move"]
            dup.FLAGSECTIONS["variables"] = dup.FLAGSECTIONS["variables"] or C.FLAGSECTIONS["variables"]
            dup.FLAGSECTIONS["region"] = dup.FLAGSECTIONS["region"] or C.FLAGSECTIONS["region"]
            dup.FLAGSECTIONS["create"] = dup.FLAGSECTIONS["create"] or C.FLAGSECTIONS["create"]
            dup.FLAGSECTIONS["group"] = dup.FLAGSECTIONS["group"] or C.FLAGSECTIONS["group"]
            dup.FLAGSECTIONS["move"] = dup.FLAGSECTIONS["move"] or C.FLAGSECTIONS["move"]
            return dup
        raise TypeError("the second operand must a region.coregeometry object")

    def __iadd__(self,C):
        """ overload iaddition ("+=") operator """
        if isinstance(C,coregeometry):
            self.USER += C.USER
            self.SECTIONS["variables"] += C.SECTIONS["variables"]
            self.SECTIONS["region"] += C.SECTIONS["region"]
            self.SECTIONS["create"] += C.SECTIONS["create"]
            self.SECTIONS["group"] += C.SECTIONS["group"]
            self.SECTIONS["move"] += C.SECTIONS["move"]
            self.FLAGSECTIONS["variables"] = self.FLAGSECTIONS["variables"] or C.FLAGSECTIONS["variables"]
            self.FLAGSECTIONS["region"] = self.FLAGSECTIONS["region"] or C.FLAGSECTIONS["region"]
            self.FLAGSECTIONS["create"] = self.FLAGSECTIONS["create"] or C.FLAGSECTIONS["create"]
            self.FLAGSECTIONS["group"] = self.FLAGSECTIONS["group"] or C.FLAGSECTIONS["group"]
            self.FLAGSECTIONS["move"] = self.FLAGSECTIONS["move"] or C.FLAGSECTIONS["move"]
            return self
        raise TypeError("the operand must a region.coregeometry object")

    def __or__(self,C):
        """ overload | pipe """
        if isinstance(C,coregeometry):
            dup = deepduplicate(self)
            dup.name = cleanname(self.name) +"|"+ cleanname(C.name)
            dup.USER = dup.USER + C.USER
            dup.USER.ID = "$" + cleanname(self.USER.ID) +"|"+ cleanname(C.USER.ID)
            dup.SECTIONS["variables"] = dup.SECTIONS["variables"] | C.SECTIONS["variables"]
            dup.SECTIONS["region"] = dup.SECTIONS["region"] | C.SECTIONS["region"]
            dup.SECTIONS["create"] = dup.SECTIONS["create"] | C.SECTIONS["create"]
            dup.SECTIONS["group"] = dup.SECTIONS["group"] | C.SECTIONS["group"]
            dup.SECTIONS["move"] = dup.SECTIONS["move"] | C.SECTIONS["move"]
            self.FLAGSECTIONS["variables"] = self.FLAGSECTIONS["variables"] or C.FLAGSECTIONS["variables"]
            self.FLAGSECTIONS["region"] = self.FLAGSECTIONS["region"] or C.FLAGSECTIONS["region"]
            self.FLAGSECTIONS["create"] = self.FLAGSECTIONS["create"] or C.FLAGSECTIONS["create"]
            self.FLAGSECTIONS["group"] = self.FLAGSECTIONS["group"] or C.FLAGSECTIONS["group"]
            self.FLAGSECTIONS["move"] = self.FLAGSECTIONS["move"] or C.FLAGSECTIONS["move"]
            return dup
        raise TypeError("the second operand must a region.coregeometry object")

    # copy and deep copy methods for the class (required)
    def __getstate__(self):
        """ getstate for cooperative inheritance / duplication """
        return self.__dict__.copy()

    def __setstate__(self,state):
        """ setstate for cooperative inheritance / duplication """
        self.__dict__.update(state)

    def __copy__(self):
        """ copy method """
        cls = self.__class__
        copie = cls.__new__(cls)
        copie.__dict__.update(self.__dict__)
        return copie

    def __deepcopy__(self, memo):
        """ deep copy method """
        cls = self.__class__
        copie = cls.__new__(cls)
        memo[id(self)] = copie
        for k, v in self.__dict__.items():
            setattr(copie, k, deepduplicate(v, memo)) # replace duplicatedeep by deepduplicate (OV: 2023-07-28)
        return copie

    # Return the number of atoms
    @property
    def natoms(self):
        """Calculate the number of beads based on density, mass, and volume"""
        if hasattr(self, 'volume'):
            try:
                volume_siunits = self.volume("si")
                voxel_volume_siunits = self.lattice_scale**3
                number_of_beads = volume_siunits / voxel_volume_siunits
                packing_factors = {
                    'sc': 1.0,
                    'fcc': 4.0,
                    'bcc': 2.0,
                    'hcp': 6.0,  # Approximate value, requires specific volume calculation for accuracy
                    'dia': 8.0,
                    'bco': 2.0,  # Assuming orthorhombic lattice similar to bcc
                    'fco': 4.0,  # Assuming orthorhombic lattice similar to fcc
                }
                packing_factor = packing_factors.get(self.lattice_style, 1.0)  # Default to simple cubic if unknown
                number_of_beads *= packing_factor
                return round(number_of_beads)
            except Exception as e:
                print(f"Error calculating number of beads: {e}")
                return None
        else:
            print("Volume attribute is missing.")
            return None

    # return parent region details
    @property
    def regiondetails(self):
        return "\n".join((
        f"\n--- | Region Details | ---",
        f"Name: {self.name}",
        f"Lattice Style: {self.lattice_style}",
        f"Lattice Scale: {self.lattice_scale}",
        f"Lattice Scale (SI units): {self.lattice_scale_siunits}",
        f"Volume: {self.volume()}",
        f"Volume (SI units): {self.volume('si')}",
        f"Number of Atoms: {self.natoms}","\n"
        ))


    # return geometry details (2024-07-04)
    @property
    def geometry(self):
        """Return the geometry details of the object."""
        details = self.regiondetails
        details += "\n--- | Geometry Details | ---\n"
        if hasattr(self.USER, 'geometry'):
            details += self.USER.geometry
        else:
            details = "No geometry available.\n"
        return details


class Block(coregeometry):
    """ Block class """

    def __init__(self,counter,index=None,subindex=None, mass=1, density=1,
                 lattice_style="sc",lattice_scale=1,lattice_scale_siunits=1,
                 hasgroup=False,hasmove=False,spacefilling=False,
                 style=None, group=None, forcefield=None, **variables):
        self.name = "block%03d" % counter[1]
        self.kind = "block"     # kind of object
        self.alike = "block"    # similar object for plotting
        self.beadtype = 1       # bead type
        self.index = counter[0] if index is None else index
        self.subindex = subindex
        self.mass = mass
        self.density = density

        # call the generic constructor
        super().__init__(
                USER = regiondata(style="$block"),
                VARIABLES = regiondata(**variables),
                hasgroup=hasgroup,hasmove=hasmove,spacefilling=spacefilling,
                mass=mass, density=density,
                lattice_style=lattice_style,
                lattice_scale=lattice_scale,
                lattice_scale_siunits=lattice_scale_siunits,
                style=style, group=group, forcefield=forcefield # script object properties
                )

    def volume(self,units=None):
        """Calculate the volume of the block based on USER.args"""
        #args = [xlo, xhi, ylo, yhi, zlo, zhi]
        try:
            # Extract the arguments from USER.args
            args = self.USER.args_siunits if units=="si" else self.USER.args
            xlo = float(args[0])
            xhi = float(args[1])
            ylo = float(args[2])
            yhi = float(args[3])
            zlo = float(args[4])
            zhi = float(args[5])

            # Calculate the dimensions of the block
            length = xhi - xlo
            width = yhi - ylo
            height = zhi - zlo

            # Calculate the volume of the block
            volume = length * width * height
            return volume
        except Exception as e:
            print(f"Error calculating volume: {e}")
            return None


class Cone(coregeometry):
    """ Cone class """

    def __init__(self,counter,index=None,subindex=None, mass=1, density=1,
                 lattice_style="sc",lattice_scale=1,lattice_scale_siunits=1,
                 hasgroup=False,hasmove=False,spacefilling=False,
                 style=None, group=None, forcefield=None, **variables):
        self.name = "cone%03d" % counter[1]
        self.kind = "cone"     # kind of object
        self.alike = "cone"    # similar object for plotting
        self.beadtype = 1      # bead type
        self.index = counter[0] if index is None else index
        self.subindex = subindex
        self.mass = mass
        self.density = density
        # call the generic constructor
        super().__init__(
                USER = regiondata(style="$cone"),
                VARIABLES = regiondata(**variables),
                hasgroup=hasgroup,hasmove=hasmove,spacefilling=spacefilling,
                mass=mass, density=density,
                lattice_style=lattice_style,
                lattice_scale=lattice_scale,
                lattice_scale_siunits=lattice_scale_siunits,
                style=style, group=group, forcefield=forcefield # script object properties
                )

    def volume(self,units=None):
        """Calculate the volume of the cone based on USER.args"""
        #args = [dim, c1, c2, radlo, radhi, lo, hi]
        try:
            # Extract the arguments from USER.args
            args = self.USER.args_siunits if units=="si" else self.USER.args
            radius_low = float(args[3])
            radius_high = float(args[4])
            lo = float(args[5])
            hi = float(args[6])
            # Calculate the height of the cone
            height = hi - lo
            # Calculate the volume of the cone (assuming a conical frustum if radii are different)
            if radius_low == radius_high:
                volume = (1/3) * 3.141592653589793 * (radius_low ** 2) * height
            else:
                volume = (1/3) * 3.141592653589793 * height * (radius_low ** 2 + radius_low * radius_high + radius_high ** 2)
            return volume
        except Exception as e:
            print(f"Error calculating volume: {e}")
            return None


class Cylinder(coregeometry):
    """ Cylinder class """
    def __init__(self,counter,index=None,subindex=None, mass=1, density=1,
                 lattice_style="sc",lattice_scale=1,lattice_scale_siunits=1,
                 hasgroup=False,hasmove=False,spacefilling=False,
                 style=None, group=None, forcefield=None, **variables):
        self.name = "cylinder%03d" % counter[1]
        self.kind = "cylinder"     # kind of object
        self.alike = "cylinder"    # similar object for plotting
        self.beadtype = 1          # bead type
        self.index = counter[0] if index is None else index
        self.subindex = subindex
        self.mass = mass
        self.density = density
        # call the generic constructor
        super().__init__(
                USER = regiondata(style="$cylinder"),
                VARIABLES = regiondata(**variables),
                hasgroup=hasgroup,hasmove=hasmove,spacefilling=spacefilling,
                mass=mass, density=density,
                lattice_style=lattice_style,
                lattice_scale=lattice_scale,
                lattice_scale_siunits=lattice_scale_siunits,
                style=style, group=group, forcefield=forcefield # script object properties
                )

    def volume(self,units=None):
        """Calculate the volume of the cylinder based on USER.args"""
        # args = [dim,c1,c2,radius,lo,hi]
        try:
            # Extract the arguments from USER.args
            args = self.USER.args_siunits if units=="si" else self.USER.args
            radius = float(args[3])
            lo = float(args[4])
            hi = float(args[5])
            # Calculate the height of the cylinder
            height = hi - lo
            # Calculate the volume of the cylinder
            volume = 3.141592653589793 * (radius ** 2) * height
            return volume
        except Exception as e:
            print(f"Error calculating volume: {e}")
            return None

class Ellipsoid(coregeometry):
    """ Ellipsoid class """

    def __init__(self,counter,index=None,subindex=None, mass=1, density=1,
                 lattice_style="sc",lattice_scale=1,lattice_scale_siunits=1,
                 hasgroup=False,hasmove=False,spacefilling=False,
                 style=None, group=None, forcefield=None, **variables):
        self.name = "ellipsoid%03d" % counter[1]
        self.kind = "ellipsoid"     # kind of object
        self.alike = "ellipsoid"    # similar object for plotting
        self.beadtype = 1           # bead type
        self.index = counter[0] if index is None else index
        self.subindex = subindex
        self.mass = mass
        self.density = density
        # call the generic constructor
        super().__init__(
                USER = regiondata(style="$ellipsoid"),
                VARIABLES = regiondata(**variables),
                hasgroup=hasgroup,hasmove=hasmove,spacefilling=spacefilling,
                mass=mass, density=density,
                lattice_style=lattice_style,
                lattice_scale=lattice_scale,
                lattice_scale_siunits=lattice_scale_siunits,
                style=style, group=group, forcefield=forcefield # script object properties
                )

    def volume(self,units=None):
        #args = [x, y, z, a, b, c]
        """Calculate the volume of the ellipsoid based on USER.args"""
        try:
            # Extract the arguments from USER.args
            args = self.USER.args_siunits if units=="si" else self.USER.args
            a = float(args[3])
            b = float(args[4])
            c = float(args[5])
            # Calculate the volume of the ellipsoid
            volume = (4/3) * 3.141592653589793 * a * b * c
            return volume
        except Exception as e:
            print(f"Error calculating volume: {e}")
            return None

class Plane(coregeometry):
    """ Plane class """

    def __init__(self,counter,index=None,subindex=None, mass=1, density=1,
                 lattice_style="sc",lattice_scale=1,lattice_scale_siunits=1,
                 hasgroup=False,hasmove=False,spacefilling=False,
                 style=None, group=None, forcefield=None, **variables):
        self.name = "plane%03d" % counter[1]
        self.kind = "plane"      # kind of object
        self.alike = "plane"     # similar object for plotting
        self.beadtype = 1       # bead type
        self.index = counter[0] if index is None else index
        self.subindex = subindex
        self.mass = mass
        self.density = density
        # call the generic constructor
        super().__init__(
                USER = regiondata(style="$plane"),
                VARIABLES = regiondata(**variables),
                hasgroup=hasgroup,hasmove=hasmove,spacefilling=spacefilling,
                style=style, group=group, forcefield=forcefield # script object properties
                )

    @property
    def volume(self,units=None):
        """Dummy method returning None for volume"""
        #args = [px, py, pz, nx, ny, nz]
        return None

class Prism(coregeometry):
    """ Prism class """

    def __init__(self,counter,index=None,subindex=None, mass=1, density=1,
                 lattice_style="sc",lattice_scale=1,lattice_scale_siunits=1,
                 hasgroup=False,hasmove=False,spacefilling=False,
                 style=None, group=None, forcefield=None, **variables):
        self.name = "prism%03d" % counter[1]
        self.kind = "prism"      # kind of object
        self.alike = "prism"     # similar object for plotting
        self.beadtype = 1       # bead type
        self.index = counter[0] if index is None else index
        self.subindex = subindex
        self.mass = mass
        self.density = density
        # call the generic constructor
        super().__init__(
                USER = regiondata(style="$prism"),
                VARIABLES = regiondata(**variables),
                hasgroup=hasgroup,hasmove=hasmove,spacefilling=spacefilling,
                mass=mass, density=density,
                lattice_style=lattice_style,
                lattice_scale=lattice_scale,
                lattice_scale_siunits=lattice_scale_siunits,
                style=style, group=group, forcefield=forcefield # script object properties
                )

    def volume(self,units=None):
        """Calculate the volume of the prism based on USER.args"""
        #args = [xlo, xhi, ylo, yhi, zlo, zhi, xy, xz, yz]
        try:
            # Extract the arguments from USER.args
            args = self.USER.args_siunits if units=="si" else self.USER.args
            xlo = float(args[0])
            xhi = float(args[1])
            ylo = float(args[2])
            yhi = float(args[3])
            zlo = float(args[4])
            zhi = float(args[5])
            # Calculate the dimensions of the prism
            length = xhi - xlo
            width = yhi - ylo
            height = zhi - zlo
            # Calculate the volume of the prism
            volume = length * width * height
            return volume
        except Exception as e:
            print(f"Error calculating volume: {e}")
            return None

class Sphere(coregeometry):
    """ Sphere class """

    def __init__(self,counter,index=None,subindex=None, mass=1, density=1,
                 lattice_style="sc",lattice_scale=1,lattice_scale_siunits=1,
                 hasgroup=False,hasmove=False,spacefilling=False,
                 style=None, group=None, forcefield=None, **variables):
        self.name = "sphere%03d" % counter[1]
        self.kind = "sphere"      # kind of object
        self.alike = "ellipsoid"     # similar object for plotting
        self.beadtype = 1       # bead type
        self.index = counter[0] if index is None else index
        self.subindex = subindex
        self.mass = mass
        self.density = density
        # call the generic constructor
        super().__init__(
                USER = regiondata(style="$sphere"),
                VARIABLES = regiondata(**variables),
                hasgroup=hasgroup,hasmove=hasmove,spacefilling=spacefilling,
                mass=mass, density=density,
                lattice_style=lattice_style,
                lattice_scale=lattice_scale,
                lattice_scale_siunits=lattice_scale_siunits,
                style=style, group=group, forcefield=forcefield # script object properties
                )

    def volume(self,units=None):
        """Calculate the volume of the sphere based on USER.args"""
        #args = [x, y, z, radius]
        try:
            # Extract the arguments from USER.args
            args = self.USER.args_siunits if units=="si" else self.USER.args
            radius = float(args[3])
            # Calculate the volume of the sphere
            volume = (4/3) * 3.141592653589793 * (radius ** 3)
            return volume
        except Exception as e:
            print(f"Error calculating volume: {e}")
            return None

class Union(coregeometry):
    """ Union class """

    def __init__(self,counter,index=None,subindex=None,
                 hasgroup=False,hasmove=False,spacefilling=False,**variables):
        self.name = "union%03d" % counter[1]
        self.kind = "union"      # kind of object
        self.alike = "operator"     # similar object for plotting
        self.beadtype = 1       # bead type
        self.index = counter[0] if index is None else index
        self.subindex = subindex
        # call the generic constructor
        super().__init__(
                USER = regiondata(style="$union"),
                VARIABLES = regiondata(**variables),
                hasgroup=hasgroup,hasmove=hasmove,spacefilling=spacefilling
                )

class Intersect(coregeometry):
    """ Intersect class """

    def __init__(self,counter,index=None,subindex=None,
                 hasgroup=False,hasmove=False,spacefilling=False,**variables):
        self.name = "intersect%03d" % counter[1]
        self.kind = "intersect"      # kind of object
        self.alike = "operator"     # similar object for plotting
        self.beadtype = 1       # bead type
        self.index = counter[0] if index is None else index
        self.subindex = subindex
        # call the generic constructor
        super().__init__(
                USER = regiondata(style="$intersect"),
                VARIABLES = regiondata(**variables),
                hasgroup=hasgroup,hasmove=hasmove,spacefilling=spacefilling
                )

class Evalgeometry(coregeometry):
    """ generic class to store evaluated objects with region.eval() """

    def __init__(self,counter,index=None,subindex=None,
                 hasgroup=False,hasmove=False,spacefilling=False):
        self.name = "eval%03d" % counter[1]
        self.kind = "eval"      # kind of object
        self.alike = "eval"     # similar object for plotting
        self.beadtype = 1       # bead type
        self.index = counter[0] if index is None else index
        self.subindex = subindex
        super().__init__(hasgroup=hasgroup,hasmove=hasmove,spacefilling=spacefilling)


class Collection:
    """
        Collection class (including many objects)
    """
    _version = "0.31"
    __custom_documentations__ = "pizza.region.Collection class"

    # CONSTRUCTOR
    def __init__(self,counter,
                 name=None,
                 index = None,
                 subindex = None,
                 hasgroup = False,
                 USER = regiondata()):
        if (name is None) or (name==""):
            self.name = "collect%03d" % counter[1]
        elif name in self:
            raise KeyError(f'the name "{name}" already exist')
        else:
            self.name = name
        if not isinstance(USER,regiondata):
            raise TypeError("USER should be a regiondata object")
        USER.groupID = "$"+self.name # the content is frozen
        USER.ID = ""
        self.USER = USER
        self.kind = "collection"    # kind of object
        self.alike = "mixed"        # similar object for plotting
        self.index = counter[0] if index is None else index
        self.subindex = counter[1]
        self.collection = regioncollection()
        self.SECTIONS = {
        	'group': LammpsCollectionGroup(**USER)
        }
        self.FLAGSECTIONS = {"group": hasgroup}

    def update(self):
        """ update the USER content for the script """
        if isinstance(self.SECTIONS["group"],script):
            self.USER.ID = "$"\
                +span([groupprefix+x for x in self.list()]) # the content is frozen
            self.SECTIONS["group"].USER += self.USER

    def creategroup(self):
        """  force the group creation in script """
        for o in self.collection: o.creategroup()
        self.update()
        self.FLAGSECTIONS["group"] = True

    def removegroup(self,recursive=True):
        """  force the group creation in script """
        if recursive:
            for o in self.collection: o.removegroup()
        self.FLAGSECTIONS["group"] = False

    @property
    def hasgroup(self):
        """ return the flag hasgroup """
        return self.FLAGSECTIONS["group"]

    @property
    def flags(self):
        """ return a list of all flags that are currently set """
        flag_names = list(self.SECTIONS.keys())
        return [flag for flag in flag_names if getattr(self, f"has{flag}")]

    @property
    def shortflags(self):
        """ return a string made from the first letter of each set flag """
        return "".join([flag[0] for flag in self.flags])

    @property
    def script(self):
        """ generates a pipe script from SECTIONS """
        self.update()
        return self.SECTIONS["group"]

    def __repr__(self):
        keylengths = [len(key) for key in self.collection.keys()]
        width = max(10,max(keylengths)+2)
        fmt = "%%%ss:" % width
        line = ( fmt % ('-'*(width-2)) ) + ( '-'*(min(40,width*5)) )
        print(line,"  %s - %s object" % (self.name, self.kind), line,sep="\n")
        for key,value in self.collection.items():
            flags = "("+self.collection[key].shortflags+")" if self.collection[key].flags else "(no script)"
            print(fmt % key,value.kind,
                  '"%s"' % value.name," > ",flags)
        flags = self.flags
        if flags: print(line,f'defined scripts: {span(flags,sep=",")}',sep="\n")
        print(line)
        return "%s object: %s (beadtype=[%s])" % (self.kind,self.name,", ".join(map(str,self.beadtype)))

    # GET -----------------------------
    def get(self,name):
        """ returns the object """
        if name in self.collection:
            return self.collection.getattr(name)
        elif name in ["collection","hasgroup","flags","shortflags","script"]:
            return getattr(self,name)
        else:
            raise ValueError('the object "%s" does not exist, use list()' % name)

    # GETATTR --------------------------
    def __getattr__(self,key):
        """ get attribute override """
        return self.get(key)

    @property
    def beadtype(self):
        """ returns the beadtypes used in the collection """
        b = []
        for o in self.collection:
            if o.beadtype not in b:
                b.append(o.beadtype)
        if len(b)==0:
            return 1
        else:
            return b

    # GROUP -------------------------------
    def group(self):
        """ return the grouped coregeometry object """
        if len(self) == 0:return pipescript()
        # execute all objects
        for i in range(len(self)): self.collection[i].do()
        # concatenate all objects into a pipe script
        liste = [x.SECTIONS["variables"] for x in self.collection if x.hasvariables] + \
                [x.SECTIONS["region"]    for x in self.collection if x.hasregion] + \
                [x.SECTIONS["create"]    for x in self.collection if x.hascreate] + \
                [x.SECTIONS["group"]     for x in self.collection if x.hasgroup] + \
                [x.SECTIONS["setgroup"]  for x in self.collection if x.hassetgroup] + \
                [x.SECTIONS["move"]      for x in self.collection if x.hasmove]
        return pipescript.join(liste)

    # LEN ---------------------------------
    def __len__(self):
        """ return length of collection """
        return len(self.collection)

    # LIST ---------------------------------
    def list(self):
        """ return the list of objects """
        return self.collection.keys()



# %% region class (main class)
class region:
    """
    The `region` class represents a simulation region, centered at the origin (0, 0, 0) by default,
    and is characterized by its physical dimensions, properties, and boundary conditions. It supports
    setting up lattice structures, particle properties, and options for live previews.

    Attributes:
    ----------
    name : str, optional
        Name of the region (default is 'region container').

    dimension : int, optional
        Number of spatial dimensions for the simulation (either 2 or 3, default is 3).

    boundary : list of str or None, optional
        Boundary conditions for each dimension. If None, defaults to ["sm"] * dimension.
        Must be a list of length `dimension`, where "s" indicates shrink-wrapped, and "m" indicates a non-periodic boundary.

    nbeads : int, optional
        Number of beads in the region (default is 1).

    units : str, optional
        Units for the simulation box (default is "").

    Particle Properties:
    -------------------
    mass : float, optional
        Mass of particles in the region (default is 1).

    volume : float, optional
        Volume of the region (default is 1).

    density : float, optional
        Density of the region (default is 1).

    radius : float, optional
        Radius of the particles (default is 1.5).

    contactradius : float, optional
        Contact radius of the particles (default is 0.5).

    velocities : list of floats, optional
        Initial velocities of particles (default is [0, 0, 0]).

    forces : list of floats, optional
        External forces acting on the particles (default is [0, 0, 0]).

    Other Properties:
    ----------------
    filename : str, optional
        Name of the output file (default is an empty string, which will auto-generate a name based on the region name).

    index : int, optional
        Index or identifier for the region.

    run : int, optional
        Run configuration parameter (default is 1).

    Box Properties:
    ---------------
    center : list of floats, optional
        Center of the simulation box for coordinate scaling (default is [0, 0, 0]).

    width : float, optional
        Width of the region (default is 10).

    height : float, optional
        Height of the region (default is 10).

    depth : float, optional
        Depth of the region (default is 10).

    hasfixmove : bool, optional
        Indicates whether the region has a fixed movement (default is False).

    Spacefilling Design:
    -------------------
    spacefilling : bool, optional
        Indicates whether the design is space-filling (default is False).

    fillingbeadtype : int, optional
        Type of bead used for space filling (default is 1).

    Lattice Properties:
    ------------------
    regionunits : str, optional
        Defines the units of the region. Can be either "lattice" (default) or "si".

    separationdistance : float, optional
        Separation distance between atoms in SI units (default is 5e-6).

    lattice_scale : float, optional
        Scaling factor for the lattice, used mainly in visualization (default is 0.8442).

    lattice_spacing : list or None, optional
        Specifies the spacing between lattice points. If None, the default spacing is used. Can be a list of [dx, dy, dz].

    lattice_style : str, optional
        Specifies the lattice structure style (default is "fcc"). Accepts any LAMMPS valid style, e.g., "sc" for simple cubic.

    Atom Properties:
    ----------------
    atom_style : str, optional
        Defines the atom style for the region (default is "smd").

    atom_modify : list of str, optional
        LAMMPS command for atom modification (default is ["map", "array"]).

    comm_modify : list of str, optional
        LAMMPS command for communication modification (default is ["vel", "yes"]).

    neigh_modify : list, optional
        LAMMPS command for neighbor list modification (default is ["every", 10, "delay", 0, "check", "yes"]).

    newton : str, optional
        Specifies the Newton flag (default is "off").

    Live Preview:
    ------------
    live_units : str, optional
        Units for live preview (default is "lj", for Lennard-Jones units).

    live_atom_style : str, optional
        Atom style used specifically for live LAMMPS sessions (default is "atomic").

    livepreview_options : dict, optional
        Contains options for live preview. The dictionary includes 'static' (default: run = 1) and 'dynamic' (default: run = 100) options.

    Methods:
    -------
    __init__ :
        Constructor method to initialize all the attributes of the `region` class.
    """

    _version = "0.9997"
    __custom_documentations__ = "pizza.region.region class"

    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
    #
    # CONSTRUCTOR METHOD
    #
    #
    # The constructor include
    #   the main container: objects (a dictionnary)
    #   several attributes covering current and future use of PIZZA.REGION()
    #
    # The original constructor is derived from PIZZA.RASTER() with
    # an intent to allow at some point some forward and backward port between
    # objects of the class PIZZA.RASTER() and PIZZA.REGION().
    #
    # The code will evolve according to the needs, please come back regularly.
    #
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-

    # CONSTRUCTOR ----------------------------
    def __init__(self,
                 # container properties
                 name="region container",
                 dimension = 3,
                 boundary = None,
                 nbeads=1,
                 units = "",

                 # particle properties
                 mass=1.0,
                 volume=1.0,
                 density=1.0,
                 radius=1.5,
                 contactradius=0.5,
                 velocities=[0.0,0.0,0.0],
                 forces=[0.0,0.0,0.0],

                 # other properties
                 filename="",
                 previewfilename="",
                 index = None,
                 run=1,

                 # Box lengths
                 center = [0.0,0.0,0.0],    # center of the box for coordinates scaling
                 width = 10.0,  # along x
                 height = 10.0, # along y
                 depth = 10.0,  # along z
                 hasfixmove = False, # by default no fix move

                 # Spacefilling design (added on 2023-08-10)
                 spacefilling = False,
                 fillingbeadtype = 1,

                 # Lattice properties
                 boxid = "box",             # default value for ${boxid_arg}
                 regionunits = "lattice",   # units ("lattice" or "si")
                 separationdistance = 5e-6, # SI units
                 lattice_scale = 0.8442,    # LJ units (for visualization)
                 lattice_spacing = None,    # lattice spacing is not used by default (set [dx dy dz] if needed)
                 lattice_style = "fcc" ,    # any valid lattice style accepted by LAMMPS (sc=simple cubic)

                 # Atom properties
                 atom_style = "smd",
                 atom_modify = ["map","array"],
                 comm_modify = ["vel","yes"],
                 neigh_modify = ["every",10,"delay",0,"check","yes"],
                 newton ="off",

                 # Live preview
                 live_units = "lj",         # units to be used ONLY with livelammps (https://andeplane.github.io/atomify/)
                 live_atom_style = "atomic",# atom style to be used ONLY with livelammps (https://andeplane.github.io/atomify/)

                 # livepreview options
                 livepreview_options = {
                     'static':{'run':1},
                     'dynamic':{'run':100}
                     },

                 # common flags (for scripting)
                 printflag = False,
                 verbose = True,
                 verbosity = None

                 ):
        """ constructor """
        self.name = name

        # Ensure dimension is an integer (must be 2 or 3 for LAMMPS)
        if not isinstance(dimension, int) or dimension not in (2, 3):
            raise ValueError("dimension must be either 2 or 3.")

        # Handle boundary input
        if boundary is None:
            boundary = ["sm"] * dimension
        elif isinstance(boundary, list):
            if len(boundary) != dimension:
                raise ValueError(f"The length of boundary ({len(boundary)}) must match the dimension ({dimension}).")
        else:
            raise ValueError("boundary must be a list of strings or None.")

        # Validate regionunits
        if regionunits not in ("lattice", "si"):
            raise ValueError("regionunits can only be 'lattice' or 'si'.")

        # Lattice scaling logic
        lattice_scale_siunits = lattice_scale if regionunits == "si" else separationdistance
        if lattice_scale_siunits is None or lattice_scale_siunits=="":
            lattice_scale_siunits = separationdistance
        if lattice_spacing == "":
            lattice_spacing = None
        elif isinstance(lattice_spacing, (int, float)):
            lattice_spacing = [lattice_spacing] * dimension
        elif isinstance(lattice_spacing, list):
            lattice_spacing = lattice_spacing + [lattice_spacing[-1]] * (dimension - len(lattice_spacing)) if len(lattice_spacing) < dimension else lattice_spacing[:dimension]

        # live data (updated 2024-07-04)
        live_lattice_scale = lattice_scale/separationdistance if regionunits == "si" else lattice_scale
        live_box_scale = 1/lattice_scale_siunits if regionunits == "si" else 1
        self.live = regiondata(nbeads=nbeads,
                               run=run,
                               width=math.ceil(width*live_box_scale),    # live_box_scale force lattice units for live visualization
                               height=math.ceil(height*live_box_scale),  # live_box_scale force lattice units for live visualization
                               depth=math.ceil(depth*live_box_scale),    # live_box_scale force lattice units for live visualization
                               live_units = "$"+live_units,
                               live_atom_style = "$"+live_atom_style,
                               live_lattice_style="$"+lattice_style,
                               live_lattice_scale=live_lattice_scale)
        # generic SMD properties (to be rescaled)
        self.volume = volume
        self.mass = mass
        self.density = density
        self.radius = radius
        self.contactradius = contactradius
        self.velocities = velocities
        self.forces = forces
        if filename == "":
            self.filename = f"region_{self.name}"
        else:
            self.filename = filename
        self.index = index
        self.objects = {}    # object container
        self.nobjects = 0    # total number of objects (alive)
        # count objects per type
        self.counter = {
                  "ellipsoid":0,
                  "block":0,
                  "sphere":0,
                  "cone":0,
                  "cylinder":0,
                  "prism":0,
                  "plane":0,
                  "union":0,
                  "intersect":0,
                  "eval":0,
                  "collection":0,
                  "all":0
            }
        # fix move flag
        self.hasfixmove = hasfixmove
        # livelammps (for live sessions) - added 2023-02-06
        self.livelammps = {
            "URL": livelammpsURL,
         "active": False,
           "file": None,
        "options": livepreview_options
            }
        # space filling  (added 2023-08-10)
        self.spacefilling = {
                   "flag": spacefilling,
           "fillingstyle": "$block",
        "fillingbeadtype": fillingbeadtype,
           "fillingwidth": width,
          "fillingheight": height,
           "fillingdepth": depth,
           "fillingunits": units
               }
        # region object units
        self.regionunits = regionunits
        # lattice
        self.units = units
        self.center = center
        self.separationdistance = separationdistance
        self.lattice_scale = lattice_scale
        self.lattice_spacing = lattice_spacing
        self.lattice_scale_siunits = lattice_scale_siunits
        self.lattice_style = lattice_style
        # headers for header scripts (added 2024-09-01)
        # geometry is assumed to be units set by ${boxunits_arg} (new standard 2024-11-26)
        self.headersData = headersRegiondata(
            # use $ and [] to prevent execution
            name = "$"+name,
            previewfilename = "$dump.initial."+self.filename if previewfilename=="" else "$"+previewfilename,
            # Initialize Lammps
            dimension = dimension,
            units = "$"+units,
            boundary = boundary,
            atom_style = "$" + atom_style,
            atom_modify = atom_modify,
            comm_modify = comm_modify,
            neigh_modify = neigh_modify,
            newton ="$" + newton,
            # Box (added 2024-11-26)
            boxid = "$"+boxid,
            boxunits_arg = "$units box" if regionunits=="si" else "", # standard on 2025-11-26
            # Lattice
            lattice_style = "$"+lattice_style,
            lattice_scale = lattice_scale,
            lattice_spacing = lattice_spacing,
            # Box
            xmin = -(width/2)  +center[0],
            xmax = +(width/2)   +center[0],
            ymin = -(height/2) +center[1],
            ymax = +(height/2) +center[1],
            zmin = -(depth/2)  +center[2],
            zmax = +(depth/2)  +center[2],
            nbeads = nbeads,
            mass = mass
            )
        self.printflag = printflag
        self.verbose = verbose if verbosity is None else verbosity>0
        self.verbosity = 0 if not verbose else verbosity

    # Method for coordinate/length scaling and translation including with formula embedded strings (updated 2024-07-03, fixed 2024-07-04)
    # Note that the translation is not fully required since the scaling applies also to full coordinates.
    # However, an implementation is provided for arbitrary offset.
    def scale_and_translate(self, value, offset=0):
        """
        Scale and translate a value or encapsulate the formula within a string.

        If self.regionunits is "si", only the offset is applied without scaling.
        Otherwise, scaling and translation are performed based on self.units ("si" or "lattice").

        Parameters:
            value (str or float): The value or formula to be scaled and translated.
            offset (float, optional): The offset to apply. Defaults to 0.

        Returns:
            str or float: The scaled and translated value or formula.
        """
        if self.regionunits == "si":
            # Only apply offset without scaling
            if isinstance(value, str):
                if offset:
                    translated = f"({value}) - {offset}"
                else:
                    translated = f"{value}"
                return translated
            else:
                if offset:
                    return value - offset
                else:
                    return value
        else:
            # Existing behavior based on self.units
            if isinstance(value, str):
                if offset:
                    translated = f"({value}) - {offset}"
                else:
                    translated = f"{value}"
                if self.units == "si":
                    return f"({translated}) / {self.lattice_scale} + {offset / self.lattice_scale}"
                else:  # "lattice"
                    return f"({translated}) * {self.lattice_scale} + {offset * self.lattice_scale}"
            else:
                if offset:
                    translated = value - offset
                else:
                    translated = value
                if self.units == "si":
                    return translated / self.lattice_scale + (offset / self.lattice_scale)
                else:  # "lattice"
                    return translated * self.lattice_scale + (offset * self.lattice_scale)



    # space filling attributes (cannot be changed)
    @property
    def isspacefilled(self):
        return self.spacefilling["flag"]

    @property
    def spacefillingbeadtype(self):
        return self.spacefilling["fillingbeadtype"]

    # total number of atoms in the region
    @property
    def natoms(self):
        """Count the total number of atoms in all objects within the region."""
        total_atoms = 0
        for eachobj in self:
            total_atoms += eachobj.natoms
        return total_atoms

    # details if the geometry of the region
    @property
    def geometry(self):
        """Display the dimensions and characteristics of the region and its objects."""
        details = f"Region: {self.name}\n"
        details += f"Total atoms: {self.natoms}\n"
        details += f"Span: width={self.spacefilling['fillingwidth']}, height={self.spacefilling['fillingheight']}, depth={self.spacefilling['fillingdepth']}\n"
        details += f"Box center: {self.center}\n"
        details += "Objects in the region:\n\n"
        for obj in self:
            details += "\n\n"+"-"*32+"\n"
            details += f"\nObject: {obj.name}\n"
            details += f"Type: {type(obj).__name__}\n"
            if hasattr(obj, 'geometry'):
                details += "\n"+"-"*32+"\n"
                details += obj.geometry
            else:
                details += "No geometry information available.\n"
        print(details)

    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
    #
    # REGION.GEOMETRY constructors
    #
    #
    #   These methods create the 3D geometry objects (at least their code)
    #   A geometry is a collection of PIZZA.SCRIPT() objects (LAMMPS codelet)
    #   not a real geometry. The distinction between the creation (definition)
    #   and the execution (generation) of the gometry object existed already
    #   in PIZZA.RASTER(), but here they remain codelets as ONLY LAMMPS can
    #   generate the real object.
    #
    #   This level of abstraction makes it possible to mix PIZZA variables
    #   (USER, PIZZA.SCRIPT.USER, PIZZA.PIPESCRIPT.USER) with LAMMPS variables.
    #   The same object template can be used in different LAMMPS scripts with
    #   different values and without writting additional Python code.
    #   In shorts: USER fields store PIZZA.SCRIPT() like variables
    #              (they are compiled [statically] before LAMMPS execution)
    #              VARIABLES are defined in the generated LAMMPS script but
    #              created [dynamically] in LAMMPS. Note that these variables
    #              are defined explicitly with the LAMMPS variable command:
    #                   variable name style args ...
    #   Note: static variables can have only one single value for LAMMPS, which
    #         is known before LAMMPS is launched. The others can be assigned
    #         at runtime when LAMMPS is running.
    #   Example with complex definitions
    #       R.ellipsoid(0,0,0,1,1,1,name="E2",side="out",
    #                   move=["left","${up}*3",None],
    #                   up=0.1)
    #       R.E2.VARIABLES.left = '"swiggle(%s,%s,%s)"%(${a},${b},${c})'
    #       R.E2.VARIABLES.a="${b}-5"
    #       R.E2.VARIABLES.b=5
    #       R.E2.VARIABLES.c=100
    #
    #   The methods PIZZA.REGION.DO(), PIZZA.REGION.DOLIVE() compiles
    #   (statically) and generate the corresponding LAMMPS code. The static
    #   compiler accepts hybrid constructions where USER and VARIABLES are
    #   mixed. Any undefined variables will be assumed to be defined elsewhere
    #   in the LAMMPS code.
    #
    #  Current attributes of PIZZA.REGION.OBJECT cover current and future use
    #  of these objects and will allow some point some forward and backward
    #  compatibility with the same PIZZA.RASTER.OBJECT.
    #
    #
    #   References:
    #       https://docs.lammps.org/region.html
    #       https://docs.lammps.org/variable.html
    #       https://docs.lammps.org/create_atoms.html
    #       https://docs.lammps.org/create_box.html
    #
    #
    #   List of implemented geometries (shown here with the LAMMPS syntax)
    #       block args = xlo xhi ylo yhi zlo zhi
    #       cone args = dim c1 c2 radlo radhi lo hi
    #       cylinder args = dim c1 c2 radius lo hi
    #       ellipsoid args = x y z a b c <-- first method to be implemented
    #       plane args = px py pz nx ny n
    #       prism args = xlo xhi ylo yhi zlo zhi xy xz yz
    #       sphere args = x y z radius
    #       union args = N reg-ID1 reg-ID2 ..
    #       intersect args = N reg-ID1 reg-ID2 ...
    #
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-

    # BLOCK method ---------------------------
    # block args = xlo xhi ylo yhi zlo zhi
    # xlo,xhi,ylo,yhi,zlo,zhi = bounds of block in all dimensions (distance units)
    def block(self,xlo=-5,xhi=5,ylo=-5,yhi=5,zlo=-5,zhi=5,
                  name=None,beadtype=None,fake=False,
                  mass=None, density=None,
                  side=None,units=None,move=None,rotate=None,open=None,
                  index = None,subindex = None,
                  **variables
                  ):
        """
        creates a block region
            xlo,xhi,ylo,yhi,zlo,zhi = bounds of block in all dimensions (distance units)

            URL: https://docs.lammps.org/region.html

            Main properties = default value
                name = "block001"
            beadtype = 1
                fake = False (use True to test the execution)
     index, subindex = object index and subindex

            Extra properties
                side = "in|out"
               units = "lattice|box" ("box" is forced if regionunits=="si")
                move = "[${v1} ${v2} ${v3}]" or [v1,v2,v3] as a list
                       with v1,v2,v3 equal-style variables for x,y,z displacement
                       of region over time (distance units)
              rotate = string or 1x7 list (see move) coding for vtheta Px Py Pz Rx Ry Rz
                       vtheta = equal-style variable for rotation of region over time (in radians)
                       Px,Py,Pz = origin for axis of rotation (distance units)
                       Rx,Ry,Rz = axis of rotation vector
                open = integer from 1-6 corresponding to face index

            See examples for elliposid()
        """
        # prepare object creation
        kind = "block"
        if index is None: index = self.counter["all"]+1
        if subindex is None: subindex = self.counter[kind]+1
        units = "box" if self.regionunits=="si" and units is None else units  # force box units of regionunits=="si"
        # create the object B with B for block
        obj_mass = mass if mass is not None else self.mass
        obj_density = density if density is not None else self.density
        B = Block((self.counter["all"]+1,self.counter[kind]+1),
                      spacefilling=self.isspacefilled, # added on 2023-08-11
                      mass=obj_mass, density=obj_density, # added on 2024-06-14
                      index=index,subindex=subindex,
                      lattice_style=self.lattice_style,
                      lattice_scale=self.lattice_scale,
                      lattice_scale_siunits=self.lattice_scale_siunits,
                      **variables)
        # feed USER fields
        if name not in (None,""): B.name = name # object name (if not defined, default name will be used)
        if name in self.name: raise NameError('the name "%s" is already used' % name)
        if beadtype is not None: B.beadtype = beadtype # bead type (if not defined, default index will apply)
        B.USER.ID = "$"+B.name        # add $ to prevent its execution
        # geometry args (2024-07-04)  -------------------------------------
        args = [xlo, xhi, ylo, yhi, zlo, zhi]  # args = [....] as defined in the class Block
        args_scaled = [
            self.scale_and_translate(xlo, self.center[0]),
            self.scale_and_translate(xhi, self.center[0]),
            self.scale_and_translate(ylo, self.center[1]),
            self.scale_and_translate(yhi, self.center[1]),
            self.scale_and_translate(zlo, self.center[2]),
            self.scale_and_translate(zhi, self.center[2])
        ]
        if self.units == "si":
            B.USER.args = args_scaled
            B.USER.args_siunits = args
        else:  # "lattice"
            B.USER.args = args
            B.USER.args_siunits = args_scaled
        # geometry
        B.USER.geometry = (
            f"Block Region: {B.name}\n"
            "Coordinates: [xlo,xhi,ylo,yhi,zlo,zhi] = bounds of block in all dimensions"
            f"Coordinates (scaled): {B.USER.args}\n"
            f"Coordinates (SI units): {B.USER.args_siunits}\n"
            f"\talong x: [{B.USER.args[0]}, {B.USER.args[1]}]\n"
            f"\talong y: [{B.USER.args[2]}, {B.USER.args[3]}]\n"
            f"\talong z: [{B.USER.args[4]}, {B.USER.args[5]}]"
        )
        # other attributes  -------------------------------------
        B.USER.beadtype = B.beadtype  # beadtype to be used for create_atoms
        B.USER.side = B.sidearg(side) # extra parameter side
        B.USER.move = B.movearg(move) # move arg
        B.USER.units = B.unitsarg(units) # units
        B.USER.rotate = B.rotatearg(rotate) # rotate
        B.USER.open = B.openarg(open) # open
        # Create the object if not fake
        if fake:
            return B
        else:
            self.counter["all"] += 1
            self.counter[kind] +=1
            self.objects[name] = B
            self.nobjects += 1
            return None

    # CONE method ---------------------------
    # cone args = dim c1 c2 radlo radhi lo hi
    # dim = x or y or z = axis of cone
    # c1,c2 = coords of cone axis in other 2 dimensions (distance units)
    # radlo,radhi = cone radii at lo and hi end (distance units)
    # lo,hi = bounds of cone in dim (distance units)
    def cone(self,dim="z",c1=0,c2=0,radlo=2,radhi=5,lo=-10,hi=10,
                  name=None,beadtype=None,fake=False,
                  mass=None, density=None,
                  side=None,units=None,move=None,rotate=None,open=None,
                  index = None,subindex = None,
                  **variables
                  ):
        """
        creates a cone region
            dim = "x" or "y" or "z" = axis of the cone
                 note: USER, LAMMPS variables are not authorized here
            c1,c2 = coords of cone axis in other 2 dimensions (distance units)
            radlo,radhi = cone radii at lo and hi end (distance units)
            lo,hi = bounds of cone in dim (distance units)

            URL: https://docs.lammps.org/region.html

            Main properties = default value
                name = "cone001"
            beadtype = 1
                fake = False (use True to test the execution)
     index, subindex = object index and subindex

            Extra properties
                side = "in|out"
               units = "lattice|box" ("box" is forced if regionunits=="si")
                move = "[${v1} ${v2} ${v3}]" or [v1,v2,v3] as a list
                       with v1,v2,v3 equal-style variables for x,y,z displacement
                       of region over time (distance units)
              rotate = string or 1x7 list (see move) coding for vtheta Px Py Pz Rx Ry Rz
                       vtheta = equal-style variable for rotation of region over time (in radians)
                       Px,Py,Pz = origin for axis of rotation (distance units)
                       Rx,Ry,Rz = axis of rotation vector
                open = integer from 1-6 corresponding to face index

            See examples for elliposid()
        """
        # prepare object creation
        kind = "cone"
        if index is None: index = self.counter["all"]+1
        if subindex is None: subindex = self.counter[kind]+1
        units = "box" if self.regionunits=="si" and units is None else units  # force box units of regionunits=="si"
        # create the object C with C for cone
        obj_mass = mass if mass is not None else self.mass
        obj_density = density if density is not None else self.density
        C = Cone((self.counter["all"]+1,self.counter[kind]+1),
                      spacefilling=self.isspacefilled, # added on 2023-08-11
                      mass=obj_mass, density=obj_density, # added on 2024-06-14
                      index=index,subindex=subindex,
                      lattice_style=self.lattice_style,
                      lattice_scale=self.lattice_scale,
                      lattice_scale_siunits=self.lattice_scale_siunits,
                      **variables)
        # feed USER fields
        if name not in (None,""): C.name = name # object name (if not defined, default name will be used)
        if name in self.name: raise NameError('the name "%s" is already used' % name)
        if beadtype is not None: C.beadtype = beadtype # bead type (if not defined, default index will apply)
        C.USER.ID = "$"+C.name        # add $ to prevent its execution
        # geometry args (2024-07-04)  -------------------------------------
        args = [dim, c1, c2, radlo, radhi, lo, hi]  # args = [....] as defined in the class Cone
        if dim == "x":  # x-axis
            args_scaled = [
                dim,
                self.scale_and_translate(c1, self.center[1]),
                self.scale_and_translate(c2, self.center[2]),
                self.scale_and_translate(radlo, 0),
                self.scale_and_translate(radhi, 0),
                self.scale_and_translate(lo, self.center[0]),
                self.scale_and_translate(hi, self.center[0])
            ]
        elif dim == "y":  # y-axis
            args_scaled = [
                dim,
                self.scale_and_translate(c1, self.center[0]),
                self.scale_and_translate(c2, self.center[2]),
                self.scale_and_translate(radlo, 0),
                self.scale_and_translate(radhi, 0),
                self.scale_and_translate(lo, self.center[1]),
                self.scale_and_translate(hi, self.center[1])
            ]
        else:  # z-axis
            args_scaled = [
                dim,
                self.scale_and_translate(c1, self.center[0]),
                self.scale_and_translate(c2, self.center[1]),
                self.scale_and_translate(radlo, 0),
                self.scale_and_translate(radhi, 0),
                self.scale_and_translate(lo, self.center[2]),
                self.scale_and_translate(hi, self.center[2])
            ]

        if self.units == "si":
            C.USER.args = args_scaled
            C.USER.args_siunits = args
        else:  # "lattice"
            C.USER.args = args
            C.USER.args_siunits = args_scaled
        # geometry
        C.USER.geometry = (
            f"Cone Region: {C.name}\n"
            "Coordinates: [dim,c1,c2,radlo,radhi,lo,hi] = dimensions of cone\n"
            f"Coordinates (scaled): {C.USER.args}\n"
            f"Coordinates (SI units): {C.USER.args_siunits}\n"
            f"\tdim: {C.USER.args[0]}\n"
            f"\tc1: {C.USER.args[1]}\n"
            f"\tc2: {C.USER.args[2]}\n"
            f"\tradlo: {C.USER.args[3]}\n"
            f"\tradhi: {C.USER.args[4]}\n"
            f"\tlo: {C.USER.args[5]}\n"
            f"\thi: {C.USER.args[6]}"
        )
        # other attributes  -------------------------------------
        C.USER.beadtype = C.beadtype  # beadtype to be used for create_atoms
        C.USER.side = C.sidearg(side) # extra parameter side
        C.USER.move = C.movearg(move) # move arg
        C.USER.units = C.unitsarg(units) # units
        C.USER.rotate = C.rotatearg(rotate) # rotate
        C.USER.open = C.openarg(open) # open
        # Create the object if not fake
        if fake:
            return C
        else:
            self.counter["all"] += 1
            self.counter[kind] +=1
            self.objects[name] = C
            self.nobjects += 1
            return None

    # CYLINDER method ---------------------------
    # cylinder args = dim c1 c2 radius lo hi
    # dim = x or y or z = axis of cylinder
    # c1,c2 = coords of cylinder axis in other 2 dimensions (distance units)
    # radius = cylinder radius (distance units)
    # c1,c2, and radius can be a variable (see below)
    # lo,hi = bounds of cylinder in dim (distance units)
    def cylinder(self,dim="z",c1=0,c2=0,radius=4,lo=-10,hi=10,
                  name=None,beadtype=None,fake=False,
                  mass=None, density=None,
                  side=None,units=None,move=None,rotate=None,open=None,
                  index = None,subindex = None,
                  **variables
                  ):
        """
        creates a cylinder region
              dim = x or y or z = axis of cylinder
              c1,c2 = coords of cylinder axis in other 2 dimensions (distance units)
              radius = cylinder radius (distance units)
              c1,c2, and radius can be a LAMMPS variable
              lo,hi = bounds of cylinder in dim (distance units)

            URL: https://docs.lammps.org/region.html

            Main properties = default value
                name = "cylinder001"
            beadtype = 1
                fake = False (use True to test the execution)
     index, subindex = object index and subindex

            Extra properties
                side = "in|out"
               units = "lattice|box" ("box" is forced if regionunits=="si")
                move = "[${v1} ${v2} ${v3}]" or [v1,v2,v3] as a list
                       with v1,v2,v3 equal-style variables for x,y,z displacement
                       of region over time (distance units)
              rotate = string or 1x7 list (see move) coding for vtheta Px Py Pz Rx Ry Rz
                       vtheta = equal-style variable for rotation of region over time (in radians)
                       Px,Py,Pz = origin for axis of rotation (distance units)
                       Rx,Ry,Rz = axis of rotation vector
                open = integer from 1-6 corresponding to face index

            See examples for elliposid()
        """
        # prepare object creation
        kind = "cylinder"
        if index is None: index = self.counter["all"]+1
        if subindex is None: subindex = self.counter[kind]+1
        units = "box" if self.regionunits=="si" and units is None else units  # force box units of regionunits=="si"
        # create the object C with C for cylinder
        obj_mass = mass if mass is not None else self.mass
        obj_density = density if density is not None else self.density
        C = Cylinder((self.counter["all"]+1,self.counter[kind]+1),
                      spacefilling=self.isspacefilled, # added on 2023-08-11
                      mass=obj_mass, density=obj_density,
                      index=index,subindex=subindex,
                      lattice_style=self.lattice_style,
                      lattice_scale=self.lattice_scale,
                      lattice_scale_siunits=self.lattice_scale_siunits,
                      **variables)
        # feed USER fields
        if name not in (None,""): C.name = name # object name (if not defined, default name will be used)
        if name in self.name: raise NameError('the name "%s" is already used' % name)
        if beadtype is not None: C.beadtype = beadtype # bead type (if not defined, default index will apply)
        C.USER.ID = "$"+C.name        # add $ to prevent its execution
        # geometry args (2024-07-04)  -------------------------------------
        args = [dim, c1, c2, radius, lo, hi]  # args = [....] as defined in the class Cylinder
        if dim == "x":  # x-axis
            args_scaled = [
                dim,
                self.scale_and_translate(c1, self.center[1]),
                self.scale_and_translate(c2, self.center[2]),
                self.scale_and_translate(radius, 0),
                self.scale_and_translate(lo, self.center[0]),
                self.scale_and_translate(hi, self.center[0])
            ]
        elif dim == "y":  # y-axis
            args_scaled = [
                dim,
                self.scale_and_translate(c1, self.center[0]),
                self.scale_and_translate(c2, self.center[2]),
                self.scale_and_translate(radius, 0),
                self.scale_and_translate(lo, self.center[1]),
                self.scale_and_translate(hi, self.center[1])
            ]
        else:  # z-axis
            args_scaled = [
                dim,
                self.scale_and_translate(c1, self.center[0]),
                self.scale_and_translate(c2, self.center[1]),
                self.scale_and_translate(radius, 0),
                self.scale_and_translate(lo, self.center[2]),
                self.scale_and_translate(hi, self.center[2])
            ]
        if self.units == "si":
            C.USER.args = args_scaled
            C.USER.args_siunits = args
        else:  # "lattice"
            C.USER.args = args
            C.USER.args_siunits = args_scaled
        # geometry
        C.USER.geometry = (
            f"Cylinder Region: {C.name}\n"
            "Coordinates: [dim,c1,c2,radius,lo,hi] = dimensions of cylinder\n"
            f"Coordinates (scaled): {C.USER.args}\n"
            f"Coordinates (SI units): {C.USER.args_siunits}\n"
            f"\tdim: {C.USER.args[0]}\n"
            f"\tc1: {C.USER.args[1]}\n"
            f"\tc2: {C.USER.args[2]}\n"
            f"\tradius: {C.USER.args[3]}\n"
            f"\tlo: {C.USER.args[4]}\n"
            f"\thi: {C.USER.args[5]}"
        )
        # other attributes  -------------------------------------
        C.USER.beadtype = C.beadtype  # beadtype to be used for create_atoms
        C.USER.side = C.sidearg(side) # extra parameter side
        C.USER.move = C.movearg(move) # move arg
        C.USER.units = C.unitsarg(units) # units
        C.USER.rotate = C.rotatearg(rotate) # rotate
        C.USER.open = C.openarg(open) # open
        # Create the object if not fake
        if fake:
            return C
        else:
            self.counter["all"] += 1
            self.counter[kind] +=1
            self.objects[name] = C
            self.nobjects += 1
            return None

    # ELLIPSOID method ---------------------------
    # ellipsoid args = x y z a b c
    # x,y,z = center of ellipsoid (distance units)
    # a,b,c = half the length of the principal axes of the ellipsoid (distance units)
    # x,y,z,a,b,c can be variables
    def ellipsoid(self,x=0,y=0,z=0,a=5,b=3,c=2,
                  name=None,beadtype=None,fake=False,
                  mass=None, density=None,
                  side=None,units=None,move=None,rotate=None,open=None,
                  index = None,subindex = None,
                  **variables
                  ):
        """
        creates an ellipsoid region
            ellipsoid(x,y,z,a,b,c [,name=None,beadtype=None,property=value,...])
            x,y,z = center of ellipsoid (distance units)
            a,b,c = half the length of the principal axes of the ellipsoid (distance units)

            URL: https://docs.lammps.org/region.html

            Main properties = default value
                name = "ellipsoid001"
            beadtype = 1
                fake = False (use True to test the execution)
                index, subindex = object index and subindex

            Extra properties
                side = "in|out"
               units = "lattice|box" ("box" is forced if regionunits=="si")
                move = "[${v1} ${v2} ${v3}]" or [v1,v2,v3] as a list
                       with v1,v2,v3 equal-style variables for x,y,z displacement
                       of region over time (distance units)
              rotate = string or 1x7 list (see move) coding for vtheta Px Py Pz Rx Ry Rz
                       vtheta = equal-style variable for rotation of region over time (in radians)
                       Px,Py,Pz = origin for axis of rotation (distance units)
                       Rx,Ry,Rz = axis of rotation vector
                open = integer from 1-6 corresponding to face index


            Examples:
                # example with variables created either at creation or later
                    R = region(name="my region")
                    R.ellipsoid(0, 0, 0, 1, 1, 1,name="E1",toto=3)
                    repr(R.E1)
                    R.E1.VARIABLES.a=1
                    R.E1.VARIABLES.b=2
                    R.E1.VARIABLES.c="(${a},${b},100)"
                    R.E1.VARIABLES.d = '"%s%s" %("test",${c}) # note that test could be replaced by any function'
                # example with extra parameters
                    R.ellipsoid(0,0,0,1,1,1,name="E2",side="out",move=["left","${up}*3",None],up=0.1)
                    R.E2.VARIABLES.left = '"swiggle(%s,%s,%s)"%(${a},${b},${c})'
                    R.E2.VARIABLES.a="${b}-5"
                    R.E2.VARIABLES.b=5
                    R.E2.VARIABLES.c=100
        """
        # prepare object creation
        kind = "ellipsoid"
        if index is None: index = self.counter["all"]+1
        if subindex is None: subindex = self.counter[kind]+1
        units = "box" if self.regionunits=="si" and units is None else units  # force box units of regionunits=="si"
        # create the object E with E for Ellipsoid
        obj_mass = mass if mass is not None else self.mass
        obj_density = density if density is not None else self.density
        E = Ellipsoid((self.counter["all"]+1,self.counter[kind]+1),
                      spacefilling=self.isspacefilled, # added on 2023-08-11
                      mass=obj_mass, density=obj_density,
                      index=index,subindex=subindex,
                      lattice_style=self.lattice_style,
                      lattice_scale=self.lattice_scale,
                      lattice_scale_siunits=self.lattice_scale_siunits,
                      **variables)
        # feed USER fields
        if name not in (None,""): E.name = name # object name (if not defined, default name will be used)
        if name in self.name: raise NameError('the name "%s" is already used' % name)
        if beadtype is not None: E.beadtype = beadtype # bead type (if not defined, default index will apply)
        E.USER.ID = "$"+E.name        # add $ to prevent its execution
        # geometry args (2024-07-04)  -------------------------------------
        args = [x, y, z, a, b, c]  # args = [....] as defined in the class Ellipsoid
        args_scaled = [
            self.scale_and_translate(x, self.center[0]),
            self.scale_and_translate(y, self.center[1]),
            self.scale_and_translate(z, self.center[2]),
            self.scale_and_translate(a, 0),
            self.scale_and_translate(b, 0),
            self.scale_and_translate(c, 0)
        ]
        if self.units == "si":
            E.USER.args = args_scaled
            E.USER.args_siunits = args
        else:  # "lattice"
            E.USER.args = args
            E.USER.args_siunits = args_scaled
        # geometry
        E.USER.geometry = (
            f"Ellipsoid Region: {E.name}\n"
            "Coordinates: [x,y,z,a,b,c] = center and radii of ellipsoid\n"
            f"Coordinates (scaled): {E.USER.args}\n"
            f"Coordinates (SI units): {E.USER.args_siunits}\n"
            f"\tcenter: [{E.USER.args[0]}, {E.USER.args[1]}, {E.USER.args[2]}]\n"
            f"\ta: {E.USER.args[3]}\n"
            f"\tb: {E.USER.args[4]}\n"
            f"\tc: {E.USER.args[5]}"
        )
        # other attributes  -------------------------------------
        E.USER.beadtype = E.beadtype  # beadtype to be used for create_atoms
        E.USER.side = E.sidearg(side) # extra parameter side
        E.USER.move = E.movearg(move) # move arg
        E.USER.units = E.unitsarg(units) # units
        E.USER.rotate = E.rotatearg(rotate) # rotate
        E.USER.open = E.openarg(open) # open
        # Create the object if not fake
        if fake:
            return E
        else:
            self.counter["all"] += 1
            self.counter[kind] +=1
            self.objects[name] = E
            self.nobjects += 1
            return None

    # PLANE method ---------------------------
    # plane args = px py pz nx ny nz
    # px,py,pz = point on the plane (distance units)
    # nx,ny,nz = direction normal to plane (distance units)
    def plane(self,px=0,py=0,pz=0,nx=0,ny=0,nz=1,
                  name=None,beadtype=None,fake=False,
                  side=None,units=None,move=None,rotate=None,open=None,
                  index = None,subindex = None,
                  **variables
                  ):
        """
        creates a plane region
              px,py,pz = point on the plane (distance units)
              nx,ny,nz = direction normal to plane (distance units)

            URL: https://docs.lammps.org/region.html

            Main properties = default value
                name = "plane001"
            beadtype = 1
                fake = False (use True to test the execution)
     index, subindex = object index and subindex

            Extra properties
                side = "in|out"
               units = "lattice|box" ("box" is forced if regionunits=="si")
                move = "[${v1} ${v2} ${v3}]" or [v1,v2,v3] as a list
                       with v1,v2,v3 equal-style variables for x,y,z displacement
                       of region over time (distance units)
              rotate = string or 1x7 list (see move) coding for vtheta Px Py Pz Rx Ry Rz
                       vtheta = equal-style variable for rotation of region over time (in radians)
                       Px,Py,Pz = origin for axis of rotation (distance units)
                       Rx,Ry,Rz = axis of rotation vector
                open = integer from 1-6 corresponding to face index

            See examples for elliposid()
        """
        # prepare object creation
        kind = "plane"
        if index is None: index = self.counter["all"]+1
        if subindex is None: subindex = self.counter[kind]+1
        units = "box" if self.regionunits=="si" and units is None else units  # force box units of regionunits=="si"
        # create the object P with P for plane
        P = Plane((self.counter["all"]+1,self.counter[kind]+1),
                      spacefilling=self.isspacefilled, # added on 2023-08-11
                      mass=self.mass, density=self.density, # added on 2024-06-14
                      index=index,subindex=subindex,
                      lattice_style=self.lattice_style,
                      lattice_scale=self.lattice_scale,
                      lattice_scale_siunits=self.lattice_scale_siunits,
                      **variables)
        # feed USER fields
        if name not in (None,""): P.name = name # object name (if not defined, default name will be used)
        if name in self.name: raise NameError('the name "%s" is already used' % name)
        if beadtype is not None: P.beadtype = beadtype # bead type (if not defined, default index will apply)
        P.USER.ID = "$"+P.name        # add $ to prevent its execution
        # geometry args (2024-07-04) ---------------------------
        args = [px, py, pz, nx, ny, nz]  # args = [....] as defined in the class Plane
        args_scaled = [
            self.scale_and_translate(px, self.center[0]),
            self.scale_and_translate(py, self.center[1]),
            self.scale_and_translate(pz, self.center[2]),
            self.scale_and_translate(nx, 0),
            self.scale_and_translate(ny, 0),
            self.scale_and_translate(nz, 0)
        ]
        if self.units == "si":
            P.USER.args = args_scaled
            P.USER.args_siunits = args
        else:  # "lattice"
            P.USER.args = args
            P.USER.args_siunits = args_scaled
        # geometry
        P.USER.geometry = (
            f"Plane Region: {P.name}\n"
            "Coordinates: [px,py,pz,nx,ny,nz] = point and normal vector of plane\n"
            f"Coordinates (scaled): {P.USER.args}\n"
            f"Coordinates (SI units): {P.USER.args_siunits}\n"
            f"\tpoint: [{P.USER.args[0]}, {P.USER.args[1]}, {P.USER.args[2]}]\n"
            f"\tnormal: [{P.USER.args[3]}, {P.USER.args[4]}, {P.USER.args[5]}]"
            )
        # other attributes ---------------------------
        P.USER.beadtype = P.beadtype  # beadtype to be used for create_atoms
        P.USER.side = P.sidearg(side) # extra parameter side
        P.USER.move = P.movearg(move) # move arg
        P.USER.units = P.unitsarg(units) # units
        P.USER.rotate = P.rotatearg(rotate) # rotate
        P.USER.open = P.openarg(open) # open
        # Create the object if not fake
        if fake:
            return P
        else:
            self.counter["all"] += 1
            self.counter[kind] +=1
            self.objects[name] = P
            self.nobjects += 1
            return None

    # PRISM method ---------------------------
    # prism args = xlo xhi ylo yhi zlo zhi xy xz yz
    # xlo,xhi,ylo,yhi,zlo,zhi = bounds of untilted prism (distance units)
    # xy = distance to tilt y in x direction (distance units)
    # xz = distance to tilt z in x direction (distance units)
    # yz = distance to tilt z in y direction (distance units)
    def prism(self,xlo=-5,xhi=5,ylo=-5,yhi=5,zlo=-5,zhi=5,xy=1,xz=1,yz=1,
                  name=None,beadtype=None,fake=False,
                  mass=None, density=None,
                  side=None,units=None,move=None,rotate=None,open=None,
                  index = None,subindex = None,
                  **variables
                  ):
        """
        creates a prism region
            xlo,xhi,ylo,yhi,zlo,zhi = bounds of untilted prism (distance units)
            xy = distance to tilt y in x direction (distance units)
            xz = distance to tilt z in x direction (distance units)
            yz = distance to tilt z in y direction (distance units)

            URL: https://docs.lammps.org/region.html

            Main properties = default value
                name = "prism001"
            beadtype = 1
                fake = False (use True to test the execution)
     index, subindex = object index and subindex

            Extra properties
                side = "in|out"
               units = "lattice|box" ("box" is forced if regionunits=="si")
                move = "[${v1} ${v2} ${v3}]" or [v1,v2,v3] as a list
                       with v1,v2,v3 equal-style variables for x,y,z displacement
                       of region over time (distance units)
              rotate = string or 1x7 list (see move) coding for vtheta Px Py Pz Rx Ry Rz
                       vtheta = equal-style variable for rotation of region over time (in radians)
                       Px,Py,Pz = origin for axis of rotation (distance units)
                       Rx,Ry,Rz = axis of rotation vector
                open = integer from 1-6 corresponding to face index

            See examples for elliposid()
        """
        # prepare object creation
        kind = "prism"
        if index is None: index = self.counter["all"]+1
        if subindex is None: subindex = self.counter[kind]+1
        units = "box" if self.regionunits=="si" and units is None else units  # force box units of regionunits=="si"
        # create the object P with P for prism
        obj_mass = mass if mass is not None else self.mass
        obj_density = density if density is not None else self.density
        P = Prism((self.counter["all"]+1,self.counter[kind]+1),
                      spacefilling=self.isspacefilled, # added on 2023-08-11
                      mass=obj_mass, density=obj_density, # added on 2024-06-14
                      index=index,subindex=subindex,
                      lattice_style=self.lattice_style,
                      lattice_scale=self.lattice_scale,
                      lattice_scale_siunits=self.lattice_scale_siunits,
                      **variables)
        # feed USER fields
        if name not in (None,""): P.name = name # object name (if not defined, default name will be used)
        if name in self.name: raise NameError('the name "%s" is already used' % name)
        if beadtype is not None: P.beadtype = beadtype # bead type (if not defined, default index will apply)
        P.USER.ID = "$"+P.name        # add $ to prevent its execution
        # geometry args (2024-07-04) ---------------------------
        args = [xlo, xhi, ylo, yhi, zlo, zhi, xy, xz, yz]  # args = [....] as defined in the class Prism
        args_scaled = [
            self.scale_and_translate(xlo, self.center[0]),
            self.scale_and_translate(xhi, self.center[0]),
            self.scale_and_translate(ylo, self.center[1]),
            self.scale_and_translate(yhi, self.center[1]),
            self.scale_and_translate(zlo, self.center[2]),
            self.scale_and_translate(zhi, self.center[2]),
            self.scale_and_translate(xy, 0),
            self.scale_and_translate(xz, 0),
            self.scale_and_translate(yz, 0)
        ]
        if self.units == "si":
            P.USER.args = args_scaled
            P.USER.args_siunits = args
        else:  # "lattice"
            P.USER.args = args
            P.USER.args_siunits = args_scaled
        # geometry
        P.USER.geometry = (
            f"Prism Region: {P.name}\n"
            "Coordinates: [xlo,xhi,ylo,yhi,zlo,zhi,xy,xz,yz] = bounds and tilts of prism\n"
            f"Coordinates (scaled): {P.USER.args}\n"
            f"Coordinates (SI units): {P.USER.args_siunits}\n"
            f"\tbounds: [{P.USER.args[0]}, {P.USER.args[1]}, {P.USER.args[2]}, {P.USER.args[3]}, {P.USER.args[4]}, {P.USER.args[5]}]\n"
            f"\ttilts: [{P.USER.args[6]}, {P.USER.args[7]}, {P.USER.args[8]}]"
        )
        # other attributes ---------------------------
        P.USER.beadtype = P.beadtype  # beadtype to be used for create_atoms
        P.USER.side = P.sidearg(side) # extra parameter side
        P.USER.move = P.movearg(move) # move arg
        P.USER.units = P.unitsarg(units) # units
        P.USER.rotate = P.rotatearg(rotate) # rotate
        P.USER.open = P.openarg(open) # open
        # Create the object if not fake
        if fake:
            return P
        else:
            self.counter["all"] += 1
            self.counter[kind] +=1
            self.objects[name] = P
            self.nobjects += 1
            return None

    # SPHERE method ---------------------------
    # sphere args = x y z radius
    # x,y,z = center of sphere (distance units)
    # radius = radius of sphere (distance units)
    # x,y,z, and radius can be a variable (see below)
    def sphere(self,x=0,y=0,z=0,radius=3,
                  name=None,beadtype=None,fake=False,
                  mass=None, density=None,
                  side=None,units=None,move=None,rotate=None,open=None,
                  index = None,subindex = None,
                  **variables
                  ):
        """
        creates a sphere region
              x,y,z = center of sphere (distance units)
              radius = radius of sphere (distance units)
              x,y,z, and radius can be a variable

            URL: https://docs.lammps.org/region.html

            Main properties = default value
                name = "sphere001"
            beadtype = 1
                fake = False (use True to test the execution)
     index, subindex = object index and subindex

            Extra properties
                side = "in|out"
               units = "lattice|box" ("box" is forced if regionunits=="si")
                move = "[${v1} ${v2} ${v3}]" or [v1,v2,v3] as a list
                       with v1,v2,v3 equal-style variables for x,y,z displacement
                       of region over time (distance units)
              rotate = string or 1x7 list (see move) coding for vtheta Px Py Pz Rx Ry Rz
                       vtheta = equal-style variable for rotation of region over time (in radians)
                       Px,Py,Pz = origin for axis of rotation (distance units)
                       Rx,Ry,Rz = axis of rotation vector
                open = integer from 1-6 corresponding to face index

            See examples for elliposid()
        """
        # prepare object creation
        kind = "sphere"
        if index is None: index = self.counter["all"]+1
        if subindex is None: subindex = self.counter[kind]+1
        units = "box" if self.regionunits=="si" and units is None else units  # force box units of regionunits=="si"
        # create the object S with S for sphere
        obj_mass = mass if mass is not None else self.mass
        obj_density = density if density is not None else self.density
        S = Sphere((self.counter["all"]+1,self.counter[kind]+1),
                      spacefilling=self.isspacefilled, # added on 2023-08-11
                      mass=obj_mass, density=obj_density, # added on 2024-06-14
                      index=index,subindex=subindex,
                      lattice_style=self.lattice_style,
                      lattice_scale=self.lattice_scale,
                      lattice_scale_siunits=self.lattice_scale_siunits,
                      **variables)
        # feed USER fields
        if name not in (None,""): S.name = name # object name (if not defined, default name will be used)
        if name in self.name: raise NameError('the name "%s" is already used' % name)
        if beadtype is not None: S.beadtype = beadtype # bead type (if not defined, default index will apply)
        S.USER.ID = "$"+S.name        # add $ to prevent its execution
        # geometry args (2024-07-04) ---------------------------
        args = [x, y, z, radius]  # args = [....] as defined in the class Sphere
        args_scaled = [
            self.scale_and_translate(x, self.center[0]),
            self.scale_and_translate(y, self.center[1]),
            self.scale_and_translate(z, self.center[2]),
            self.scale_and_translate(radius, 0)
        ]
        if self.units == "si":
            S.USER.args = args_scaled
            S.USER.args_siunits = args
        else:  # "lattice"
            S.USER.args = args
            S.USER.args_siunits = args_scaled
        # geometry
        S.USER.geometry = (
            f"Sphere Region: {S.name}\n"
            "Coordinates: [x,y,z,radius] = center and radius of sphere\n"
            f"Coordinates (scaled): {S.USER.args}\n"
            f"Coordinates (SI units): {S.USER.args_siunits}\n"
            f"\tcenter: [{S.USER.args[0]}, {S.USER.args[1]}, {S.USER.args[2]}]\n"
            f"\tradius: {S.USER.args[3]}"
        )
        # other attributes ---------------------------
        S.USER.beadtype = S.beadtype  # beadtype to be used for create_atoms
        S.USER.side = S.sidearg(side) # extra parameter side
        S.USER.move = S.movearg(move) # move arg
        S.USER.units = S.unitsarg(units) # units
        S.USER.rotate = S.rotatearg(rotate) # rotate
        S.USER.open = S.openarg(open) # open
        # Create the object if not fake
        if fake:
            return S
        else:
            self.counter["all"] += 1
            self.counter[kind] +=1
            self.objects[name] = S
            self.nobjects += 1
            return None

    # UNION method ---------------------------
    # union args = N reg-ID1 reg-ID2
    def union(self,*regID,
              name=None,beadtype=1,fake=False,
              index = None,subindex = None,
              **variables):
        """
        creates a union region
              union("reg-ID1","reg-ID2",name="myname",beadtype=1,...)
              reg-ID1,reg-ID2, ... = IDs of regions to join together

            URL: https://docs.lammps.org/region.html

            Main properties = default value
                name = "union001"
            beadtype = 1
                fake = False (use True to test the execution)
     index, subindex = object index and subindex
        """
        kind = "union"
        if index is None: index = self.counter["all"]+1
        if subindex is None: subindex = self.counter[kind]+1
        # create the object U with U for union
        U = Union((self.counter["all"]+1,self.counter[kind]+1),
                      index=index,subindex=subindex,**variables)
        # feed USER fields
        if name not in (None,""): U.name = name # object name (if not defined, default name will be used)
        if name in self.name: raise NameError('the name "%s" is already used' % name)
        if beadtype is not None: U.beadtype = beadtype # bead type (if not defined, default index will apply)
        U.USER.ID = "$"+U.name        # add $ to prevent its execution
        U.USER.side, U.USER.move, U.USER.units, U.USER.rotate, U.USER.open = "","","","",""
        # build arguments based on regID
        nregID = len(regID)
        if nregID<2: raise ValueError('two objects must be given at least for an union')
        args = [None] # the number of arguments is not known yet
        validID = range(nregID)
        for ireg in validID:
            if isinstance(regID[ireg],int):
                if regID[ireg] in validID:
                    args.append(self.names[regID[ireg]])
                else:
                    raise IndexError(f"the index {regID[ireg]} exceeds the number of objects {len(self)}")
            elif isinstance(regID[ireg],str):
                if regID[ireg] in self:
                    args.append(regID[ireg])
                else:
                    raise KeyError(f'the object "{regID[ireg]}" does not exist')
            else:
                raise KeyError(f"the {ireg+1}th object should be given as a string or an index")
            # prevent the creation of atoms merged (avoid duplicates)
            self.objects[regID[ireg]].FLAGSECTIONS["create"] = False
        args[0] = len(regID)
        U.USER.args = args   # args = [....] as defined in the class Union
        # Create the object if not fake
        if fake:
            return U
        else:
            self.counter["all"] += 1
            self.counter[kind] +=1
            self.objects[name] = U
            self.nobjects += 1
            return None

    # UNION method ---------------------------
    # union args = N reg-ID1 reg-ID2
    def intersect(self,*regID,
              name=None,beadtype=1,fake=False,
              index = None,subindex = None,
              **variables):
        """
        creates an intersection region
              intersect("reg-ID1","reg-ID2",name="myname",beadtype=1,...)
              reg-ID1,reg-ID2, ... = IDs of regions to join together

            URL: https://docs.lammps.org/region.html

            Main properties = default value
                name = "intersect001"
            beadtype = 1
                fake = False (use True to test the execution)
     index, subindex = object index and subindex
        """
        kind = "intersect"
        if index is None: index = self.counter["all"]+1
        if subindex is None: subindex = self.counter[kind]+1
        # create the object I with I for intersect
        I = Intersect((self.counter["all"]+1,self.counter[kind]+1),
                      index=index,subindex=subindex,**variables)
        # feed USER fields
        if name not in (None,""): I.name = name # object name (if not defined, default name will be used)
        if name in self.name: raise NameError('the name "%s" is already used' % name)
        if beadtype is not None: I.beadtype = beadtype # bead type (if not defined, default index will apply)
        I.USER.ID = "$"+I.name        # add $ to prevent its execution
        I.USER.side, I.USER.move, I.USER.units, I.USER.rotate, I.USER.open = "","","","",""
        # build arguments based on regID
        nregID = len(regID)
        if nregID<2: raise ValueError('two objects must be given at least for an intersection')
        args = [None] # the number of arguments is not known yet
        validID = range(nregID)
        for ireg in validID:
            if isinstance(regID[ireg],int):
                if regID[ireg] in validID:
                    args.append(self.names[regID[ireg]])
                else:
                    raise IndexError(f"the index {regID[ireg]} exceeds the number of objects {len(self)}")
            elif isinstance(regID[ireg],str):
                if regID[ireg] in self:
                    args.append(regID[ireg])
                else:
                    raise KeyError(f'the object "{regID[ireg]}" does not exist')
            else:
                raise KeyError(f"the {ireg+1}th object should be given as a string or an index")
            # prevent the creation of atoms (avoid duplicates)
            self.objects[regID[ireg]].FLAGSECTIONS["create"] = False
        args[0] = len(regID)
        I.USER.args = args   # args = [....] as defined in the class Union
        # Create the object if not fake
        if fake:
            return I
        else:
            self.counter["all"] += 1
            self.counter[kind] +=1
            self.objects[name] = I
            self.nobjects += 1
            return None


    # Group method ---------------------------
    def group(self,obj,name=None,fake=False):
        pass


    # COLLECTION method ---------------------------
    def collection(self,*obj,name=None,beadtype=None,fake=False,
              index = None,subindex = None,
              **kwobj):
        kind = "collection"
        if index is None: index = self.counter["all"]+1
        if subindex is None: subindex = self.counter[kind]+1
        # create the object C with C for collection
        C = Collection((index,subindex))
        if name not in (None,""): C.name = name # object name (if not defined, default name will be used)
        if name in self.name: raise NameError('the name "%s" is already used' % name)
        if beadtype is not None: C.beadtype = beadtype # bead type (if not defined, default index will apply)
        # add objects
        C.collection = regioncollection(*obj,**kwobj)
        # apply modifications (beadtype, ismask)
        for o in C.collection.keys():
            tmp = C.collection.getattr(o)
            if beadtype != None: tmp.beadtype = beadtype
            C.collection.setattr(o,tmp)
        # Create the object if not fake
        if fake:
            return C
        else:
            self.counter["all"] += 1
            self.counter[kind] +=1
            self.objects[name] = C
            self.nobjects += 1
            return None

    def scatter(self,
                 E,
                 name="emulsion",
                 beadtype=None,
                 ):
        """


        Parameters
        ----------
        E : scatter or emulsion object
            codes for x,y,z and r.
        name : string, optional
            name of the collection. The default is "emulsion".
        beadtype : integer, optional
            for all objects. The default is 1.

        Raises
        ------
        TypeError
            Return an error of the object is not a scatter type.

        Returns
        -------
        None.

        """
        if isinstance(E,scatter):
            collect = {}
            for i in range(E.n):
                b = E.beadtype[i] if beadtype==None else beadtype
                nameobj = "glob%02d" % i
                collect[nameobj] = self.sphere(E.x[i],E.y[i],E.z[i],E.r[i],
                            name=nameobj,beadtype=b,fake=True)
            self.collection(**collect,name=name)
        else:
            raise TypeError("the first argument must be an emulsion object")



    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
    #
    # LOW-LEVEL METHODS
    #
    #
    # Low-level methods to manipulate and operate region objects (e.g., R).
    # They implement essentially some Python standards with the following
    # shortcut: R[i] or R[objecti] and R.objecti and R.objects[objecti] are
    # the same ith object where R.objects is the original container
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-

    # repr() method ----------------------------
    def __repr__(self):
        """ display method """
        spacefillingstr = f"\n(space filled with beads of type {self.spacefillingbeadtype})" \
            if self.isspacefilled else ""
        print("-"*40)
        print('REGION container "%s" with %d objects %s\n(units="%s", lattice="%s", scale=%0.4g [m])' \
              % (self.name,self.nobjects,spacefillingstr,self.units,self.lattice_style,self.lattice_scale_siunits))
        if self.nobjects>0:
            names = self.names
            l = [len(n) for n in names]
            width = max(10,max(l)+2)
            fmt = "%%%ss:" % width
            for i in range(self.nobjects):
                flags = "("+self.objects[names[i]].shortflags+")" if self.objects[names[i]].flags else "(no script)"
                if isinstance(self.objects[names[i]],Collection):
                        print(fmt % names[i]," %s region (%d beadtypes)" % \
                              (self.objects[names[i]].kind,len(self.objects[names[i]].beadtype))," > ",flags)
                else:
                    print(fmt % names[i]," %s region (beadtype=%d)" % \
                          (self.objects[names[i]].kind,self.objects[names[i]].beadtype)," > ",flags)
            print(wrap("they are",":",", ".join(self.names),10,60,80))
        print("-"*40)
        return "REGION container %s with %d objects (%s)" % \
            (self.name,self.nobjects,",".join(self.names))

    # str() method ----------------------------
    def __str__(self):
        """ string representation of a region """
        return "REGION container %s with %d objects (%s)" % \
            (self.name,self.nobjects,",".join(self.names))

    # generic GET method ----------------------------
    def get(self,name):
        """ returns the object """
        if name in self.objects:
            return self.objects[name]
        else:
            raise NameError('the object "%s" does not exist, use list()' % name)

    # getattr() method ----------------------------
    def __getattr__(self,name):
        """ getattr attribute override """
        if (name in self.__dict__) or (name in protectedregionkeys):
            return self.__dict__[name] # higher precedence for root attributes
        if name in protectedregionkeys:
            return getattr(type(self), name).__get__(self) # for methods decorated as properties (@property)
        # Handle special cases like __wrapped__ explicitly
        if name == "__wrapped__":
            return None  # Default value or appropriate behavior
        # Leave legitimate __dunder__ attributes to the default mechanism
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(f"{type(self).__name__!r} object has no attribute {name!r}")
        # Default
        return self.get(name)

    # generic SET method ----------------------------
    def set(self,name,value):
        """ set field and value """
        if isinstance(value,list) and len(value)==0:
            if name not in self.objects:
                raise NameError('the object "%s" does not exist, use list()' % name)
            self.delete(name)
        elif isinstance(value,coregeometry):
            if name in self.objects: self.delete(name)
            if isinstance(value.SECTIONS,pipescript) or isinstance(value,Evalgeometry):
                self.eval(deepduplicate(value),name) # not a scalar
            else: # scalar
                self.objects[name] = deepduplicate(value)
                self.objects[name].name = name
                self.nobjects += 1
                self.counter["all"] += 1
                self.objects[name].index = self.counter["all"]
                self.counter[value.kind] += 1

    # setattr() method ----------------------------
    def __setattr__(self,name,value):
        """ setattr override """
        if name in protectedregionkeys: # do not forget to increment protectedregionkeys
            self.__dict__[name] = value # if not, you may enter in infinite loops
        else:
            self.set(name,value)

    # generic HASATTR method ----------------------------
    def hasattr(self,name):
        """ return true if the object exist """
        if not isinstance(name,str): raise TypeError("please provide a string")
        return name in self.objects

    # IN operator ----------------------------
    def __contains__(self,obj):
        """ in override """
        return self.hasattr(obj)

    # len() method ----------------------------
    def __len__(self):
        """ len method """
        return len(self.objects)

    # indexing [int] and ["str"] method ----------------------------
    def __getitem__(self,idx):
        """
            R[i] returns the ith element of the structure
            R[:4] returns a structure with the four first fields
            R[[1,3]] returns the second and fourth elements
        """
        if isinstance(idx,int):
            if idx<len(self):
                return self.get(self.names[idx])
            raise IndexError(f"the index should be comprised between 0 and {len(self)-1}")
        elif isinstance(idx,str):
            if idx in self:
                return self.get(idx)
            raise NameError(f'{idx} does not exist, use list() to list objects')
        elif isinstance(idx,list):
            pass
        elif isinstance(idx,slice):
            return self.__getitem__(self,list(range(*idx.indices(len(self)))))
        else:
            raise IndexError("not implemented yet")

    # duplication GET method based on DICT ----------------------------
    def __getstate__(self):
        """ getstate for cooperative inheritance / duplication """
        return self.__dict__.copy()

    # duplication SET method based on DICT ----------------------------
    def __setstate__(self,state):
        """ setstate for cooperative inheritance / duplication """
        self.__dict__.update(state)

    # iterator method ----------------------------
    def __iter__(self):
        """ region iterator """
        # note that in the original object _iter_ is a static property not in dup
        dup = duplicate(self)
        dup._iter_ = 0
        return dup

    # next iterator method ----------------------------
    def __next__(self):
        """ region iterator """
        self._iter_ += 1
        if self._iter_<=len(self):
            return self[self._iter_-1]
        self._iter_ = 0
        raise StopIteration(f"Maximum region.objects iteration reached {len(self)}")


    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
    #
    # MIDDLE-LEVEL METHODS
    #
    #
    # These methods are specific to PIZZA.REGION() objects.
    # They bring useful methods for the user and developer.
    # Similar methods exist in PIZZA.RASTER()
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-

    # LIST method ----------------------------
    def list(self):
        """ list objects """
        fmt = "%%%ss:" % max(10,max([len(n) for n in self.names])+2)
        print('REGION container "%s" with %d objects' % (self.name,self.nobjects))
        for o in self.objects.keys():
            print(fmt % self.objects[o].name,"%-10s" % self.objects[o].kind,
                  "(beadtype=%d,object index=[%d,%d])" % \
                      (self.objects[o].beadtype,
                       self.objects[o].index,
                       self.objects[o].subindex))

    # NAMES method set as an attribute ----------------------------
    @property
    def names(self):
        """ return the names of objects sorted as index """
        namesunsorted=namessorted=list(self.objects.keys())
        nobj = len(namesunsorted)
        if nobj<1:
            return []
        elif nobj<2:
            return namessorted
        else:
            for iobj in range(nobj):
                namessorted[self.objects[namesunsorted[iobj]].index-1] = namesunsorted[iobj]
            return namessorted

    # NBEADS method set as an attribute
    @property
    def nbeads(self):
        "return the number of beadtypes used"
        if len(self)>0:
            guess = max(len(self.count()),self.live.nbeads)
            return guess+1 if self.isspacefilled else guess
        else:
            return self.live.nbeads

    # COUNT method
    def count(self):
        """ count objects by type """
        typlist = []
        for  o in self.names:
            if isinstance(self.objects[o].beadtype,list):
                typlist += self.objects[o].beadtype
            else:
                typlist.append(self.objects[o].beadtype)
        utypes = list(set(typlist))
        c = []
        for t in utypes:
            c.append((t,typlist.count(t)))
        return c

    # BEADTYPES property
    @property
    def beadtypes(self):
        """ list the beadtypes """
        return [ x[0] for x in self.count() ]

    # DELETE method
    def delete(self,name):
        """ delete object """
        if name in self.objects:
            kind = self.objects[name].kind
            del self.objects[name]
            self.nobjects -= 1
            self.counter[kind] -= 1
            self.counter["all"] -= 1
        else:
            raise NameError("%s does not exist (use list()) to list valid objects" % name)

    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
    #
    # HIGH-LEVEL METHODS
    #
    #
    # These methods are connect PIZZA.REGION() objects with their equivalent
    # as PIZZA.SCRIPT() and PIZZA.PIPESCRIPT() objects and methods.
    #
    # They are essential to PIZZA.REGION(). They do not have equivalent in
    # PIZZA.RASTER(). They use extensively the methods attached to :
    #        PIZZA.REGION.LAMMPSGENERIC()
    #        PIZZA.REGION.COREGEOMETRY()
    #
    # Current real-time rendering relies on
    #   https://andeplane.github.io/atomify/
    # which gives better results than
    #   https://editor.lammps.org/
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-

    # EVALUATE algebraic operation on PIZZA.REGION() objects (operation on codes)
    def eval(self,expression,name=None,beadtype = None,
             fake=False,index = None,subindex = None):
        """
            evaluates (i.e, combine scripts) an expression combining objects
                R= region(name="my region")
                R.eval(o1+o2+...,name='obj')
                R.eval(o1|o2|...,name='obj')
            R.name will be the resulting object of class region.eval (region.coregeometry)
        """
        if not isinstance(expression, coregeometry): raise TypeError("the argument should be a region.coregeometry")
        # prepare object creation
        kind = "eval"
        self.counter["all"] += 1
        self.counter[kind] +=1
        if index is None: index = self.counter["all"]
        if subindex is None: subindex = self.counter[kind]
        # create the object E with E for Ellipsoid
        E = Evalgeometry((self.counter["all"],self.counter[kind]),
                      index=index,subindex=subindex)
        # link expression to E
        if beadtype is not None: E.beadtype = beadtype # bead type (if not defined, default index will apply)
        if name is None: name = expression.name
        if name in self.name: raise NameError('the name "%s" is already used' % name)
        E.name = name
        E.SECTIONS = expression.SECTIONS
        E.USER = expression.USER
        if isinstance(E.SECTIONS,pipescript):
            # set beadtypes for all sections and scripts in the pipeline
            for i in E.SECTIONS.keys():
                for j in range(len(E.SECTIONS[i])):
                    E.SECTIONS[i].USER[j].beadtype = E.beadtype
        E.USER.beadtype = beadtype
        # Create the object if not fake
        if fake:
            self.counter["all"] -= 1
            self.counter[kind] -= 1
            return E
        else:
            self.objects[name] = E
            self.nobjects += 1
            return None

    # PIPESCRIPT method generates a pipe for all objects and sections
    def pipescript(self,printflag=False,verbose=False,verbosity=0):
        printflag = self.printflag if printflag is None else printflag
        verbose = verbosity > 0 if verbosity is not None else (self.verbose if verbose is None else verbose)
        verbosity = 0 if not verbose else verbosity
        """ pipescript all objects in the region """
        if len(self)<1: return pipescript()
        # execute all objects
        for myobj in self:
            if not isinstance(myobj,Collection): myobj.do(printflag=printflag,verbosity=verbosity)
        # concatenate all objects into a pipe script
        # for collections, only group is accepted
        liste = [x.SECTIONS["variables"] for x in self if not isinstance(x,Collection) and x.hasvariables] + \
                [x.SECTIONS["region"]    for x in self if not isinstance(x,Collection) and x.hasregion] + \
                [x.SECTIONS["create"]    for x in self if not isinstance(x,Collection) and x.hascreate] + \
                [x.SECTIONS["group"]     for x in self if not isinstance(x,Collection) and x.hasgroup] + \
                [x.SECTIONS["setgroup"]  for x in self if not isinstance(x,Collection) and x.hassetgroup] + \
                [x.SECTIONS["move"]      for x in self if not isinstance(x,Collection) and x.hasmove]
        # add the objects within the collection
        for x in self:
            if isinstance(x,Collection): liste += x.group()
        # add the eventual group for the collection
        liste += [x.SECTIONS["group"] for x in self if isinstance(x,Collection) and x.hasgroup]
        # chain all scripts
        return pipescript.join(liste)

    # SCRIPT add header and footer to PIPECRIPT
    def script(self,live=False, printflag=None, verbose=None, verbosity=None):
        """ script all objects in the region """
        printflag = self.printflag if printflag is None else printflag
        verbose = verbosity > 0 if verbosity is not None else (self.verbose if verbose is None else verbose)
        verbosity = 0 if not verbose else verbosity
        s = self.pipescript(printflag=printflag,verbose=verbose,verbosity=verbosity).script(printflag=printflag,verbose=verbose,verbosity=verbosity)
        if self.isspacefilled:
            USERspacefilling =regiondata(**self.spacefilling)
            s = LammpsSpacefilling(**USERspacefilling)+s
        if live:
            beadtypes = self.beadtypes
            USER = regiondata(**self.live)
            USER.nbeads = self.nbeads
            USER.mass = "$"
            USER.pair_coeff = "$"
            # list beadtype and prepare  mass, pair_coeff
            beadtypes = [ x[0] for x in self.count() ]
            if self.isspacefilled and self.spacefillingbeadtype not in beadtypes:
                beadtypes = [self.spacefillingbeadtype]+beadtypes
            for b in beadtypes:
                USER.mass += livetemplate["mass"] % b +"\n"
                USER.pair_coeff += livetemplate["pair_coeff"] %(b,b) +"\n"
            for b1 in beadtypes:
                for b2 in beadtypes:
                    if b2>b1:
                        USER.pair_coeff += livetemplate["pair_coeff"] %(b1,b2) +"\n"
            livemode = "dynamic" if self.hasfixmove else "static"
            USER.run =self.livelammps["options"][livemode]["run"]
            s = LammpsHeader(**USER)+s+LammpsFooter(**USER)
        return s

    # SCRIPTHEADERS add header scripts for initializing script, lattice, box for region
    def scriptHeaders(self, what=["init", "lattice", "box"], pipescript=False, **userdefinitions):
        """
            Generate and return LAMMPS header scripts for initializing the simulation, defining the lattice,
            and specifying the simulation box for all region objects.

            Parameters:
            - what (list of str): Specifies which scripts to generate. Options are "init", "lattice", "box", "mass" and "preview".
                                  Multiple scripts can be generated by passing a list of these options.
                                  Default is ["init", "lattice", "box"].
            - pipescript (bool): If True, the generated scripts are combined with `|` instead of `+`. Default is False.

            Property/pair value
            - nbeads (int): Specifies the number of beads, overriding the default if larger than `self.nbeads`.
                            Default is 1.
            - mass (real value or list): Sets the mass for each bead, overrriding `self.mass`
                            Default is 1.0.


            Returns:
            - object: The combined header scripts as a single object.
                      Header values can be overridden by updating `self.headersData`.

            Raises:
            - Exception: If no valid script options are provided in `what`.

            Example usage:
                sRheader = R.scriptHeaders("box").do()  # Generate the box header script.
                sRallheaders = R.scriptHeaders(["init", "lattice", "box"])  # Generate all headers.

                Example usage without naming parameters:
                sRheader = R.scriptHeaders("box")  # "what" specified as "box", nbeads defaults to 1.

                Example of overriding values
                sRheader = R.scriptHeaders("lattice",lattice_style = "$sq")  # Generate the lattice header script with the overridden value.
        """
        # handle overrides
        USERregion = self.headersData + regiondata(**userdefinitions)
        # Fix singletons
        if not isinstance(what, list):
            what = [what]
        # Generate the initialization script
        scripts = []  # Store all generated script objects here
        if "init" in what:
            scripts.append(LammpsHeaderInit(**USERregion))
        # Generate the lattice script
        if "lattice" in what:
            scripts.append(LammpsHeaderLattice(**USERregion))
        # Generate the box script
        if "box" in what:
            scripts.append(LammpsHeaderBox(**USERregion))
            if self.isspacefilled:
                scripts.append(LammpsSpacefilling(**self.spacefilling))
        # Generate the mass script
        if "mass" in what:
            scripts.append(LammpsHeaderMass(**USERregion))
        # Generate the preview script
        if "preview" in what:
            scripts.append(LammpsFooterPreview(**USERregion))
        if not scripts:
            raise Exception('nothing to do (use: "init", "lattice", "box", "mass" or "preview" within [ ])')

        # Combine the scripts based on the pipescript flag
        combined_script = scripts[0]  # Initialize the combined script with the first element
        for script in scripts[1:]:
            if pipescript:
                # Combine scripts using the | operator, maintaining pipescript format
                combined_script = combined_script | script  # p_ab = s_a | s_b or p_ab = s_a | p_b
            else:
                # Combine scripts using the + operator, maintaining regular script format
                combined_script = combined_script + script  # s_ab = s_a + s_b
        return combined_script


    def pscriptHeaders(self, what=["init", "lattice", "box"], **userdefinitions):
        """
        Surrogate method for generating LAMMPS pipescript headers.
        Calls the `scriptHeaders` method with `pipescript=True`.

        Parameters:
        - what (list of str): Specifies which scripts to generate. Options are "init", "lattice", and "box".
                              Multiple scripts can be generated by passing a list of these options.
                              Default is ["init", "lattice", "box"].
        Property/pair value
        - nbeads (int): Specifies the number of beads, overriding the default if larger than `self.nbeads`.
                        Default is 1.
        - mass (real value or list): Sets the mass for each bead, overrriding `self.mass`
                        Default is 1.0.
        Returns:
        - object: The combined pipescript header scripts as a single object.
        """
        # Call scriptHeaders with pipescript=True
        return self.scriptHeaders(what=what, pipescript=True, **userdefinitions)


    # DO METHOD = main static compiler
    def do(self, printflag=False, verbosity=1):
        """ execute the entire script """
        return self.pipescript().do(printflag=printflag, verbosity=verbosity)

    # DOLIVE = fast code generation for online rendering
    def dolive(self):
        """
            execute the entire script for online testing
            see: https://editor.lammps.org/
        """
        self.livelammps["file"] = self.script(live=True).tmpwrite()
        if not self.livelammps["active"]:
            livelammps(self.livelammps["URL"],new=0)
            self.livelammps["active"] = True
        return self.livelammps["file"]

# %% scatter class and emulsion class
#    Simplified scatter and emulsion generator
#    generalized from its 2D version in raster.scatter and raster.emulsion
#    added on 2023-03-10

class scatter():
    """ generic top scatter class """
    def __init__(self):
        """
        The scatter class provides an easy constructor
        to distribute in space objects according to their
        positions x,y,z size r (radius) and beadtype.

        The class is used to derive emulsions.

        Returns
        -------
        None.
        """
        self.x = np.array([],dtype=int)
        self.y = np.array([],dtype=int)
        self.z = np.array([],dtype=int)
        self.r = np.array([],dtype=int)
        self.beadtype = []

    @property
    def n(self):
        return len(self.x)

    def pairdist(self,x,y,z):
        """ pair distance to the surface of all disks/spheres """
        if self.n==0:
            return np.Inf
        else:
            return np.sqrt((x-self.x)**2+(y-self.y)**2+(z-self.z)**2)-self.r


class emulsion(scatter):
    """ emulsion generator """

    def __init__(self, xmin=10, ymin=10, zmin=10, xmax=90, ymax=90, zmax=90,
                 maxtrials=1000, beadtype=1, forcedinsertion=True):
        """


        Parameters
        ----------
        The insertions are performed between xmin,ymin and xmax,ymax
        xmin : int64 or real, optional
            x left corner. The default is 10.
        ymin : int64 or real, optional
            y bottom corner. The default is 10.
        zmin : int64 or real, optional
            z bottom corner. The default is 10.
        xmax : int64 or real, optional
            x right corner. The default is 90.
        ymax : int64 or real, optional
            y top corner. The default is 90.
        zmax : int64 or real, optional
            z top corner. The default is 90.
        beadtype : default beadtype to apply if not precised at insertion
        maxtrials : integer, optional
            Maximum of attempts for an object. The default is 1000.
        forcedinsertion : logical, optional
            Set it to true to force the next insertion. The default is True.

        Returns
        -------
        None.

        """
        super().__init__()
        self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax = xmin, xmax, ymin, ymax, zmin, zmax
        self.lastinsertion = (None,None,None,None,None) # x,y,z,r, beadtype
        self.length = xmax-xmin
        self.width = ymax-ymin
        self.height = zmax-zmin
        self.defautbeadtype = beadtype
        self.maxtrials = maxtrials
        self.forcedinsertion = forcedinsertion

    def __repr__(self):
        print(f" Emulsion object\n\t{self.length}x{self.width}x{self.height} starting at x={self.xmin}, y={self.ymin}, z={self.zmin}")
        print(f"\tcontains {self.n} insertions")
        print("\tmaximum insertion trials:", self.maxtrials)
        print("\tforce next insertion if previous fails:", self.forcedinsertion)
        return f"emulsion with {self.n} insertions"


    def walldist(self,x,y,z):
        """ shortest distance to the wall """
        return min(abs(x-self.xmin),abs(y-self.ymin),abs(z-self.zmin),abs(x-self.xmax),abs(y-self.ymax),abs(z-self.zmax))

    def dist(self,x,y,z):
        """ shortest distance of the center (x,y) to the wall or any object"""
        return np.minimum(np.min(self.pairdist(x,y,z)),self.walldist(x,y,z))

    def accepted(self,x,y,z,r):
        """ acceptation criterion """
        return self.dist(x,y,z)>r

    def rand(self):
        """ random position x,y  """
        return  np.random.uniform(low=self.xmin,high=self.xmax), \
                np.random.uniform(low=self.ymin,high=self.ymax),\
                np.random.uniform(low=self.zmin,high=self.zmax)

    def setbeadtype(self,beadtype):
        """ set the default or the supplied beadtype  """
        if beadtype == None:
            self.beadtype.append(self.defautbeadtype)
            return self.defautbeadtype
        else:
            self.beadtype.append(beadtype)
            return beadtype

    def insertone(self,x=None,y=None,z=None,r=None,beadtype=None,overlap=False):
        """
            insert one object of radius r
            properties:
                x,y,z coordinates (if missing, picked randomly from uniform distribution)
                r radius (default = 2% of diagonal)
                beadtype (default = defautbeadtype)
                overlap = False (accept only if no overlap)
        """
        attempt, success = 0, False
        random = (x==None) or (y==None) or (z==None)
        if r==None:
            r = 0.02*np.sqrt(self.length**2+self.width**2+self.height**2)
        while not success and attempt<self.maxtrials:
            attempt += 1
            if random: x,y,z = self.rand()
            if overlap:
                success = True
            else:
                success = self.accepted(x,y,z,r)
        if success:
            self.x = np.append(self.x,x)
            self.y = np.append(self.y,y)
            self.z = np.append(self.z,z)
            self.r = np.append(self.r,r)
            b=self.setbeadtype(beadtype)
            self.lastinsertion = (x,y,z,r,b)
        return success

    def insertion(self,rlist,beadtype=None):
        """
            insert a list of objects
                nsuccess=insertion(rlist,beadtype=None)
                beadtype=b forces the value b
                if None, defaultbeadtype is used instead
        """
        rlist.sort(reverse=True)
        ntodo = len(rlist)
        n = nsuccess = 0
        stop = False
        while not stop:
            n += 1
            success = self.insertone(r=rlist[n-1],beadtype=beadtype)
            if success: nsuccess += 1
            stop = (n==ntodo) or (not success and not self.forcedinsertion)
        if nsuccess==ntodo:
            print(f"{nsuccess} objects inserted successfully")
        else:
            print(f"partial success: {nsuccess} of {ntodo} objects inserted")
        return nsuccess



# %% debug section - generic code to test methods (press F5)
# ===================================================
# main()
# ===================================================
# for debugging purposes (code called as a script)
# the code is called from here
# ===================================================
if __name__ == '__main__':

    R = region(name="my region", mass=2, density=5)
    # Create a Block object using the block method of the region container with specific dimensions
    R.block(xlo=0, xhi=10, ylo=0, yhi=10, zlo=0, zhi=10, name="B1",mass=3)
    # Access the natoms property of the Block object
    print("Number of atoms in the block:", R.B1.natoms)

    # early example
    a=region(name="region A")
    b=region(name="region B")
    c = [a,b]
    # step 1
    R = region(name="my region")
    R.ellipsoid(0, 0, 0, 1, 1, 1,name="E1",toto=3)
    R
    repr(R.E1)
    R.E1.VARIABLES.a=1
    R.E1.VARIABLES.b=2
    R.E1.VARIABLES.c="(${a},${b},100)"
    R.E1.VARIABLES.d = '"%s%s" %("test",${c}) # note that test could be replaced by any function'
    R.E1
    code1 = R.E1.do()
    print(code1)
    # step 2
    R.ellipsoid(0,0,0,1,1,1,name="E2",side="out",move=["left","${up}*3",None],up=0.1)
    R.E2.VARIABLES.left = '"swiggle(%s,%s,%s)"%(${a},${b},${c})'
    R.E2.VARIABLES.a="${b}-5"
    R.E2.VARIABLES.b=5
    R.E2.VARIABLES.c=100
    code2 = R.E2.do()
    print(R)
    repr(R.E2)
    print(code2)
    print(R.names)
    R.list()

    # eval objects
    R.set('E3',R.E2)
    R.E3.beadtype = 2
    R.set('add',R.E1 + R.E2)
    R.addd2 = R.E1 + R.E2
    R.eval(R.E1 | R.E2,'E12')


    # How to manage pipelines
    print("\n","-"*20,"pipeline","-"*20)
    p = R.E2.script
    s = p.script() # first execution
    s = p.script() # do nothing
    s # check

    # reorganize scripts
    print("\n","-"*20,"change order","-"*20)
    p.clear() # undo executions first
    q = p[[0,2,1]]
    sq = q.script()
    print(q.do())

    # join sections
    liste = [x.SECTIONS["variables"] for x in R]
    pliste = pipescript.join(liste)


    # Example closer to production
    P = region(name="live test",width = 20)
    P.ellipsoid(0, 0, 0, "${Ra}", "${Rb}", "${Rc}",
              name="E1", Ra=5,Rb=2,Rc=3)
    P.sphere(7,0,0,radius="${R}",name = "S1", R=2)
    cmd = P.do()
    print(cmd)
    #outputfile = P.dolive()

    # EXAMPLE: gel compression
    scale = 1
    name = ['top','food','tongue','bottom']
    radius = [10,5,8,10]
    height = [1,4,3,1]
    spacer = 2 * scale
    radius = [r*scale for r in radius]
    height = [h*scale for h in height]
    position_original = [spacer+height[1]+height[2]+height[3],
                          height[2]+height[3],
                          height[3],
                          0]
    beadtype = [1,2,3,1]
    total_height = sum(height) +spacer
    position = [x-total_height/2 for x in position_original]
    B = region(name = 'region container',
                width=2*max(radius),
                height=total_height,
                depth=2*max(radius))
    for i in range(len(name)):
        B.cylinder(name = name[i],
                    c1=0,
                    c2=0,
                    radius=radius[i],
                    lo=position[i],
                    hi=position[i]+height[i],
                    beadtype=beadtype[i])
    B.dolive()

    # Draft for workshop
    sB = B.do()
    b1 = B[0].scriptobject()
    b2 = B[1].scriptobject()
    b3 = B[2].scriptobject()
    b4 = B[3].scriptobject()
    collection = b1 + b2 + b3 + b4;

    # # emulsion example
    scale = 1 # tested up to scale = 10 to reach million of beads
    mag = 3
    e = emulsion(xmin=-5*mag, ymin=-5*mag, zmin=-5*mag,xmax=5*mag, ymax=5*mag, zmax=5*mag)
    e.insertion([2,2,2,1,1.6,1.2,1.4,1.3],beadtype=3)
    e.insertion([0.6,0.3,2,1.5,1.5,1,2,1.2,1.1,1.3],beadtype=1)
    e.insertion([3,1,2,2,4,1,1.2,2,2.5,1.2,1.4,1.6,1.7],beadtype=2)
    e.insertion([3,1,2,2,4,1,5.2,2,4.5,1.2,1.4,1.6,1.7],beadtype=4)

    # b = region()
    # a = region()
    # a.sphere(1,1,1,1,name='sphere1')
    # a.sphere(1,2,2,1,name='sphere2')
    # b.collection(a, name='acollection')

    C = region(name='cregion',width=11*mag,height=11*mag,depth=11*mag)
    C.scatter(e)
    C.script()
    g = C.emulsion.group()
    C.dolive()


    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    #             F O R   P R O D U C T I O N
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    # History: 2024-07-04 (first version), 2024-07-29 (update), 2024-09-01 (community, per request)

    """
=== [  S Y N O P S I S  ] ===
This script provides a detailed example of simulating gel compression using cylindrical objects
within a defined region, employing SI units. The example is designed for production and includes
steps to create, script, and visualize the simulation setup using LAMMPS-compatible scripts.

Key Features:
1. **Geometry Setup**:
    - Four cylindrical objects ('top', 'food', 'tongue', 'bottom') are defined with specific radii
      and heights.
    - The cylinders are positioned within a central container, with spacing determined by a spacer
      element.
    - The total height of the system is calculated, and the objects are centered within the region.

2. **Forcefield Assignment**:
    - Each object is assigned a bead type and grouped with attributes such as rigidity or softness.
    - Custom forcefields are applied to each object, simulating different physical properties like
      rigid walls or soft materials.

3. **Region Definition**:
    - A simulation region is created with specific dimensions, accounting for the maximum radius of
      the cylinders and the total height of the system.
    - The region is defined in SI units, with additional parameters like separation distance and
      lattice scale.

4. **Script Generation**:
    - The script converts the defined region and objects into LAMMPS-compatible code.
    - Header scripts for initialization, lattice, and the bounding box are generated.
    - The example emphasizes the flexibility in scripting, allowing dynamic reordering and
      combination of scripts.

5. **Execution and Visualization**:
    - The region setup is executed for visualization purposes, enabling control and inspection of
      the geometry.
    - The geometry details, including an estimation of the number of atoms, are provided for
      further analysis.

This example showcases how to effectively set up a gel compression simulation, highlighting key
aspects of geometry definition, forcefield application, and scripting for simulation execution.
"""

    # EXAMPLE: gel compression with SI units
    name = ['top', 'food', 'tongue', 'bottom']
    radius = [10e-3, 5e-3, 8e-3, 10e-3]  # in m
    height = [1e-3, 4e-3, 3e-3, 1e-3]  # in m
    spacer = 2e-3  # in m

    # Calculate positions in SI units (meters)
    position_original = [
        spacer + height[1] + height[2] + height[3],
        height[2] + height[3],
        height[3],
        0
    ]
    total_height = sum(height) + spacer * 1e-3  # converting spacer to meters

    # Center positions around the middle of the container
    position = [x - total_height / 2 for x in position_original]

    # information for beads
    # add attributes to forcefields to match your needs or derive new forcefields
    beadtypes = [1, 2, 3, 1]
    groups = [["rigid","wall1"],["food1","soft"],["food2","soft"],["rigid","wall2"]]
    forcefields = [rigidwall(),solidfood(),solidfood(),rigidwall()]

    # Create the region container with SI units
    R = region(
        name='region container',
        width=2 * max(radius),
        height=total_height,
        depth=2 * max(radius),
        regionunits="si",
        separationdistance=100e-6,  # 50 µm
        lattice_scale=100e-6  # 50 µm
    )

    # Add cylinders to the region R
    # the objects are added "statically"
    # since they contain variables a do() is required to make them a script
    nobjects = len(name)
    for i in range(nobjects):
        R.cylinder(
            name=name[i],
            dim="z",  # Assuming z-axis as the dimension
            c1=0,
            c2=0,
            radius=radius[i],
            lo=position[i],
            hi=position[i] + height[i],
            beadtype=beadtypes[i],
            style="smd",      # the script oject properties
            group=groups[i],  # can be defined in the geometry or
            forcefield=forcefields[i] # when scriptoject() is called
        )

    # Compile statically all objects
    # sR contains the LAMMPS code to generate all region objects and their atoms
    # sR is a string, all variables have been executed
    sR = R.do() # this line force the execution of R

    # Header Scripts facilitate the deployment and initialization of region objects.
    # ------------- Summary ---------------
    # Available scripts include "init", "lattice", and "box".
    # Multiple scripts can be generated simultaneously by specifying them in a list.
    #   For example: ["init", "lattice", "box"] will generate all three scripts.
    # Script parameters and variables can be customized via R.headersData.
    #   For instance: R.headersData.lattice_style = "$sq"
    #   This overrides the lattice style, which was originally set in the region object.
    #   The "$" prefix indicates that lattice_style is a static value.
    #   Alternatively, R.headersData.lattice_style = ["sq"] can also be used.
    # --------------------------------------
    # use help(R.scriptHeaders) to get a full help
    # Note: sRheader is a string since a do()
    sRheader = R.scriptHeaders("box").do() # generate the box that contains R
    print(sRheader)
    # To generate all header scripts in the specified order, use R.scriptHeaders.
    # Note: sRallheaders is a script object. Use sRallheaders.do() to convert it into a string.
    # Scripts can be dynamically combined using the + operator or statically with the & operator.
    # Scripts can also be combined with pipescripts using the + or | (piped) operator.
    # Region and collection objects are considered pipescripts.
    #
    # Comment on the differences between scripts and pipescripts:
    #   - Scripts operate within a single variable space and cannot be reordered once combined.
    #   - Pipescripts, however, include both global and local variable spaces and can be reordered,
    #     and indexed, offering greater flexibility in complex simulations.
    #
    # A property can be removed from the initialization process by setting it to None or ""
    # In this example, atom_style is removed as it also set with forcefields
    R.headersData.atom_style = None
    sRallheaders = R.scriptHeaders(["init", "lattice", "box"] )

    # Generate information on beads from the scripted objects
    # note that scriptobject is a method of script extended to region
    # the region must have been preallably scripted, which has been done with "sR = R.do()"
    # Note that the current implementation include also style definitions in init
    b = []
    for i in range(nobjects):
        # style, group and forcefield can be overdefined if needed
        b.append(R[i].scriptobject(style="smd"))
    collection = b[0] + b[1] + b[2] + b[3]

    # The script corresponding to the collection is given by:
    # scollection is an object of the class script
    # its final execution can be still affected by variables
    scollection = collection.script.do()

    # Execute the region setup only for visualization (control only)
    R.dolive()

    # The detail of the geometry with an estimation of the number of atoms (control only)
    R.geometry

    # to be continued as in the previous workshops
    # sRheader, sR and scollection can be concatenated (they are strings)
    # Note that scripts can be concatenated before do()
