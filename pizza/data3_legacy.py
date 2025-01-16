#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
# `data` Class (legacy code)

The `data` class provides tools to read, write, and manipulate LAMMPS data files, enabling seamless integration with the `dump` class for restart generation and simulation data management.

This is the legacy module, use pizza.data3 instead.

---

## Features

- **Input Handling**:
  - Supports single or multiple data files, including gzipped files.
  - Create empty data objects or initialize from an existing `dump` object.

- **Headers and Sections**:
  - Access and modify headers, including atom counts and box dimensions.
  - Define, reorder, append, and replace columns in data file sections.

- **Integration with `dump`**:
  - Generate restart files from `dump` snapshots.
  - Replace atomic positions and velocities in `Atoms` and `Velocities` sections.

- **Visualization**:
  - Extract atoms and bonds for visualization tools.
  - Iterate over single data file snapshots (compatible with `dump`).

---

## Usage

### Initialization
- **From a File**:
  ```python
  d = data("data.poly")          # Read a LAMMPS data file
  ```

- **Create an Empty Object**:
  ```python
  d = data()                     # Create an empty data object
  ```

- **From a `dump` Object**:
  ```python
  d = data(dump_obj, timestep)   # Generate data object from dump snapshot
  ```

### Accessing Data
- **Headers**:
  ```python
  d.headers["atoms"] = 1500       # Set atom count in header
  ```

- **Sections**:
  ```python
  d.sections["Atoms"] = lines     # Define the `Atoms` section
  ```

### Manipulation
- **Column Mapping**:
  ```python
  d.map(1, "id", 3, "x")          # Assign names to columns
  ```

- **Reorder Columns**:
  ```python
  d.reorder("Atoms", 1, 3, 2, 4)  # Reorder columns in a section
  ```

- **Replace or Append Data**:
  ```python
  d.replace("Atoms", 5, vec)      # Replace a column in `Atoms`
  d.append("Atoms", vec)          # Append a new column to `Atoms`
  ```

- **Delete Headers or Sections**:
  ```python
  d.delete("Bonds")               # Remove the `Bonds` section
  ```

### Output
- **Write to a File**:
  ```python
  d.write("data.new")             # Write the data object to a file
  ```

### Visualization
- **Extract Data for Visualization**:
  ```python
  time, box, atoms, bonds, tris, lines = d.viz(0)
  ```

### Integration with `dump`
- **Replace Atomic Positions**:
  ```python
  d.newxyz(dump_obj, timestep)    # Replace atomic positions with `dump` data
  ```

---

## Examples

### Basic Usage
```python
d = data("data.poly")             # Load a LAMMPS data file
d.headers["atoms"] = 2000         # Update atom count
d.reorder("Atoms", 1, 3, 2, 4)    # Reorder columns in `Atoms`
d.write("data.new")               # Save to a new file
```

### Restart Generation
```python
dump_obj = dump("dump.poly")
d = data(dump_obj, 1000)          # Create data object from dump
d.write("data.restart")           # Write restart file
```

### Visualization
```python
time, box, atoms, bonds, tris, lines = d.viz(0)
```

---

## Properties
- **Headers**:
  - `atoms`: Number of atoms in the data file.
  - `atom types`: Number of atom types.
  - `xlo xhi`, `ylo yhi`, `zlo zhi`: Box dimensions.

- **Sections**:
  - `Atoms`: Atomic data (e.g., ID, type, coordinates).
  - `Velocities`: Atomic velocities (optional).
  - Additional sections for bonds, angles, etc.

---

## Notes
- **Compatibility**: Fully compatible with `dump` for restart and visualization tasks.
- **Error Handling**: Automatically validates headers and sections for consistency.
- **Extensibility**: Easily add or modify headers, sections, and attributes.

---
"""


__project__ = "Pizza3"
__author__ = "Olivier Vitrac"
__copyright__ = "Copyright 2022"
__credits__ = ["Steve Plimpton", "Olivier Vitrac"]
__license__ = "GPLv3"
__maintainer__ = "Olivier Vitrac"
__email__ = "olivier.vitrac@agroparistech.fr"
__version__ = "1.0"


# Pizza.py toolkit, www.cs.sandia.gov/~sjplimp/pizza.html
# Steve Plimpton, sjplimp@sandia.gov, Sandia National Laboratories
#
# Copyright (2005) Sandia Corporation.  Under the terms of Contract
# DE-AC04-94AL85000 with Sandia Corporation, the U.S. Government retains
# certain rights in this software.  This software is distributed under
# the GNU General Public License.

# data tool

# Code converted to pyton 3.x
# INRAE\olivier.vitrac@agroparistech.fr
#
# last release
# 2022-02-03 - add flist, __repr__
# 2022-02-04 - add append and start to add comments
# 2022-02-10 - first implementation of a full restart object from a dump object
# 2022-02-12 - revised append method, more robust, more verbose
# 2024-12-08 - updated help
# 2025-01-15 - module renamed pizza.data3_legacy

oneline = "Read, write, manipulate LAMMPS data files"

docstr = """
d = data("data.poly")            read a LAMMPS data file, can be gzipped
d = data()			 create an empty data file

d.map(1,"id",3,"x")              assign names to atom columns (1-N)

coeffs = d.get("Pair Coeffs")    extract info from data file section
q = d.get("Atoms",4)

  1 arg = all columns returned as 2d array of floats
  2 args = Nth column returned as vector of floats

d.reorder("Atoms",1,3,2,4,5)     reorder columns (1-N) in a data file section

  1,3,2,4,5 = new order of previous columns, can delete columns this way

d.title = "My LAMMPS data file"	 set title of the data file
d.headers["atoms"] = 1500        set a header value
d.sections["Bonds"] = lines      set a section to list of lines (with newlines)
d.delete("bonds")		 delete a keyword or section of data file
d.delete("Bonds")
d.replace("Atoms",5,vec)      	 replace Nth column of section with vector
d.newxyz(dmp,1000)		 replace xyz in Atoms with xyz of snapshot N

  newxyz assumes id,x,y,z are defined in both data and dump files
    also replaces ix,iy,iz if they are defined

index,time,flag = d.iterator(0/1)          loop over single data file snapshot
time,box,atoms,bonds,tris,lines = d.viz(index)   return list of viz objects

  iterator() and viz() are compatible with equivalent dump calls
  iterator() called with arg = 0 first time, with arg = 1 on subsequent calls
    index = timestep index within dump object (only 0 for data file)
    time = timestep value (only 0 for data file)
    flag = -1 when iteration is done, 1 otherwise
  viz() returns info for specified timestep index (must be 0)
    time = 0
    box = [xlo,ylo,zlo,xhi,yhi,zhi]
    atoms = id,type,x,y,z for each atom as 2d array
    bonds = id,type,x1,y1,z1,x2,y2,z2,t1,t2 for each bond as 2d array
      NULL if bonds do not exist
    tris = NULL
    lines = NULL

d.write("data.new")             write a LAMMPS data file
"""

# History
#   8/05, Steve Plimpton (SNL): original version
#   11/07, added triclinic box support

# ToDo list

# Variables
#   title = 1st line of data file
#   names = dictionary with atom attributes as keys, col #s as values
#   headers = dictionary with header name as key, value or tuple as values
#   sections = dictionary with section name as key, array of lines as values
#   nselect = 1 = # of snapshots

# Imports and external programs

# External dependency
from os import popen
import numpy as np

# Dependecy for the creation of DATA restart object from a DUMP object
from pizza.dump3 import dump

__all__ = ['data', 'dump']

#try:
#    tmp = PIZZA_GUNZIP
#except:
PIZZA_GUNZIP = "gunzip"

# Class definition


class data:

    # --------------------------------------------------------------------

    def __init__(self, *list):
        self.nselect = 1

        if len(list) == 0:

        # ========================================
        # Default Constructor (empty object)
        # ========================================

            self.title = "LAMMPS data file"
            self.names = {}
            self.headers = {}
            self.sections = {}
            self.flist = []
            self.restart = False
            return

        elif isinstance(list[0],dump):

        # ========================================
        # Constructor from an existing DUMP object
        # ========================================

            X = list[0]     # supplied dump object
            t = X.time()
            nt = len(t)
            if len(list)>1:
                tselect = list[1]
                if tselect not in t:
                    raise ValueError("the input time is not available in the dump object")
            else:
                tselect = t[-1]
            itselect = next(i for i in range(nt) if t[i]==tselect)
            # set object title
            self.title = 'LAMMPS data file (restart from "%s" t = %0.5g (frame %d of %d))' %  \
                (X.flist[0],tselect,itselect,nt)
            # set default names                       ------------- HEADERS SECTION -------------
            self.names = {}
            X.tselect.one(tselect)
            snap = X.snaps[itselect]
            # set headers
            self.headers = {    'atoms': snap.natoms,
                                'atom types': X.minmax("type")[1],
                                'xlo xhi': (snap.xlo, snap.xhi),
                                'ylo yhi': (snap.ylo, snap.yhi),
                                'zlo zhi': (snap.zlo, snap.zhi)}
            # Default sections
            self.sections = {}
            # set atoms (specific to your style/kind) ------------- ATOMS SUBSECTION -------------
            template_atoms = {"smd": ["id","type","mol","c_vol", "mass", "radius",
                                      "c_contact_radius", "x", "y", "z", "f_1[1]", "f_1[2]", "f_1[3]"] }
            if X.kind(template_atoms["smd"]):
                for col in template_atoms["smd"]:
                    self.append("Atoms", X.vecs(tselect, col), col in ["id","type","mol"],col)
            else:
                raise ValueError("Please add your ATOMS section in the constructor")
            # set velocities (if required)           ------------- VELOCITIES SUBSECTION -------------
            template_velocities = {"smd": ["id","vx","vy","vz"]}
            if X.kind(template_atoms["smd"]):
                if X.kind(template_velocities["smd"]):
                    for col in template_velocities["smd"]:
                        self.append("Velocities", X.vecs(tselect, col), col == "id",col)
                else:
                    raise ValueError("the velocities are missing for the style SMD")
            # store filename
            self.flist = list[0].flist
            self.restart = True
            return

        # ===========================================================
        # Regular constructor from DATA file (supplied as filename)
        # ===========================================================

        flist = list
        file = list[0]
        if file[-3:] == ".gz":
            f = popen("%s -c %s" % (PIZZA_GUNZIP, file), "r")
        else:
            f = open(file)

        self.title = f.readline()
        self.names = {}

        headers = {}
        while 1:
            line = f.readline()
            line = line.strip()
            if len(line) == 0:
                continue
            found = 0
            for keyword in hkeywords:
                if line.find(keyword) >= 0:
                    found = 1
                    words = line.split()
                    if (
                        keyword == "xlo xhi"
                        or keyword == "ylo yhi"
                        or keyword == "zlo zhi"
                    ):
                        headers[keyword] = (float(words[0]), float(words[1]))
                    elif keyword == "xy xz yz":
                        headers[keyword] = (
                            float(words[0]),
                            float(words[1]),
                            float(words[2]),
                        )
                    else:
                        headers[keyword] = int(words[0])
            if not found:
                break

        sections = {}
        while 1:
            found = 0
            for pair in skeywords:
                keyword, length = pair[0], pair[1]
                if keyword == line:
                    found = 1
                    if length not in headers: #if not headers.has_key(length):
                        raise ValueError("data section %s has no matching header value" % line)
                    f.readline()
                    list = []
                    for i in range(headers[length]):
                        list.append(f.readline())
                    sections[keyword] = list
            if not found:
                raise ValueError("invalid section %s in data file" % line)
            f.readline()
            line = f.readline()
            if not line:
                break
            line = line.strip()

        f.close()
        self.headers = headers
        self.sections = sections
        self.flist = flist
        self.restart = False

    # --------------------------------------------------------------------
    # Display method (added OV - 2022-02-03)
    def __repr__(self):
        if self.sections == {} or self.headers == {}:
            ret = "empty %s" % self.title
            print(ret)
            return ret
        if self.restart:
            kind = "restart"
        else:
            kind = "source"
        print("Data file: %s\n\tcontains %d atoms from %d atom types\n\twith box = [%0.4g %0.4g %0.4g %0.4g %0.4g %0.4g]"
              % (self.flist[0],
                 self.headers['atoms'],
                 self.headers['atom types'],
                 self.headers['xlo xhi'][0],
                 self.headers['xlo xhi'][1],
                 self.headers['ylo yhi'][0],
                 self.headers['ylo yhi'][1],
                 self.headers['zlo zhi'][0],
                 self.headers['zlo zhi'][1],
                 ) )
        print("\twith the following sections:")
        for sectionname in self.sections.keys():
            print("\t\t" +self.dispsection(sectionname,False))
        ret = 'LAMMPS data object including %d atoms (%d types, %s="%s")' \
            % (self.headers['atoms'],self.maxtype(),kind,self.flist[0])
        return ret


    # --------------------------------------------------------------------
    # assign names to atom columns

    def map(self, *pairs):
        if len(pairs) % 2 != 0:
            raise ValueError ("data map() requires pairs of mappings")
        for i in range(0, len(pairs), 2):
            j = i + 1
            self.names[pairs[j]] = pairs[i] - 1

    # --------------------------------------------------------------------
    # extract info from data file fields

    def get(self, *list):
        if len(list) == 1:
            field = list[0]
            array = []
            lines = self.sections[field]
            for line in lines:
                words = line.split()
                values = map(float, words)
                array.append(values)
            return array
        elif len(list) == 2:
            field = list[0]
            n = list[1] - 1
            vec = []
            lines = self.sections[field]
            for line in lines:
                words = line.split()
                vec.append(float(words[n]))
            return vec
        else:
            raise ValueError("invalid arguments for data.get()")

    # --------------------------------------------------------------------
    # reorder columns in a data file field

    def reorder(self, name, *order):
        """ reorder columns: reorder("section",colidxfirst,colidxsecond,colidxthird,...)  """
        if name not in self.sections:
            raise ValueError('"%s" is not a valid section name' % name)
        n = len(order)
        print(">> reorder for %d columns" % n)
        natoms = len(self.sections[name])
        oldlines = self.sections[name]
        newlines = natoms * [""]
        for index in order:
            for i in range(len(newlines)):
                words = oldlines[i].split()
                newlines[i] += words[index - 1] + " "
        for i in range(len(newlines)):
            newlines[i] += "\n"
        self.sections[name] = newlines

    # --------------------------------------------------------------------
    # replace a column of named section with vector of values
    # the number of data is checked and repeated for scalars (added 2022-02-04)

    def replace(self, name, icol, vector):
        """ replace column values: replace("section",columnindex,vectorofvalues) with columnindex=1..ncolumns """
        lines = self.sections[name]
        nlines = len(lines)
        if name not in self.sections:
            raise ValueError('"%s" is not a valid section name' % name)
        if not isinstance(vector,list): vector = [vector]
        if len(vector)==1: vector = vector * nlines
        if len(vector) != nlines:
            raise ValueError('the length of new data (%d) in section "%s" does not match the number of rows %d' % \
                             (len(vector),name,nlines))
        newlines = []
        j = icol - 1
        for i in range(nlines):
            line = lines[i]
            words = line.split()
            words[j] = str(vector[i])
            newline = " ".join(words) + "\n"
            newlines.append(newline)
        self.sections[name] = newlines

    # --------------------------------------------------------------------
    # append a column of named section with vector of values (added 2022-02-04)

    def append(self, name, vector, forceinteger = False, propertyname=None):
        """ append a new column: X.append("section",vectorofvalues,forceinteger=False,propertyname=None) """
        if name not in self.sections:
            self.sections[name] = []
            print('Add section [%s] - file="%s"' % (name,self.title) )
        lines = self.sections[name]
        nlines = len(lines)
        if not isinstance(vector,list) and not isinstance(vector,np.ndarray):
            vector = [vector]
        if propertyname != None:
            print('\t> Add "%s" (%d values) to [%s]' % (propertyname,len(vector),name))
        else:
            print('\t> Add %d values (no name) to [%s]' % (len(vector),name))
        newlines = []
        if nlines == 0:           # empty atoms section, create first column
            nlines = len(vector)  # new column length = input column length
            for i in range(nlines):
                if forceinteger:
                    line = str(int(vector[i]))
                else:
                    line = str(vector[i])
                newlines.append(line)
        else:
            if len(vector)==1: vector = vector * nlines
            if len(vector) != nlines:
                raise ValueError('the length of new data (%d) in section "%s" does not match the number of rows %d' % \
                                 (len(vector),name,nlines))
            for i in range(nlines):
                line = lines[i]
                words = line.split()
                if forceinteger:
                    words.append(str(int(vector[i])))
                else:
                    words.append(str(vector[i]))
                newline = " ".join(words) + "\n"
                newlines.append(newline)
        self.sections[name] = newlines


    # --------------------------------------------------------------------
    # disp section info (added 2022-02-04)

    def dispsection(self, name,flaghead=True):
        """ display section info: X.dispsection("sectionname") """
        lines = self.sections[name]
        nlines = len(lines)
        line = lines[0]
        words = line.split()
        ret = '"%s": %d x %d values' % (name,nlines,len(words))

        if flaghead: ret = "LAMMPS data section "+ret
        return ret

    # --------------------------------------------------------------------
    # replace x,y,z in Atoms with x,y,z values from snapshot ntime of dump object
    # assumes id,x,y,z are defined in both data and dump files
    # also replaces ix,iy,iz if they are defined

    def newxyz(self, dm, ntime):
        nsnap = dm.findtime(ntime)
        print(">> newxyz for %d snaps" % nsnap)

        dm.sort(ntime)
        x, y, z = dm.vecs(ntime, "x", "y", "z")

        self.replace("Atoms", self.names["x"] + 1, x)
        self.replace("Atoms", self.names["y"] + 1, y)
        self.replace("Atoms", self.names["z"] + 1, z)

        if "ix" in dm.names and "ix" in self.names: #if dm.names.has_key("ix") and self.names.has_key("ix"):
            ix, iy, iz = dm.vecs(ntime, "ix", "iy", "iz")
            self.replace("Atoms", self.names["ix"] + 1, ix)
            self.replace("Atoms", self.names["iy"] + 1, iy)
            self.replace("Atoms", self.names["iz"] + 1, iz)

    # --------------------------------------------------------------------
    # delete header value or section from data file

    def delete(self, keyword):

        if keyword in self.headers: # if self.headers.has_key(keyword):
            del self.headers[keyword]
        elif keyword in self.sections: # elif self.sections.has_key(keyword):
            del self.sections[keyword]
        else:
            raise ValueError("keyword not found in data object")

    # --------------------------------------------------------------------
    # write out a LAMMPS data file

    def write(self, file):
        f = open(file, "w")
        print(self.title,file=f)
        for keyword in hkeywords:
            if keyword in self.headers: # self.headers.has_key(keyword):
                if keyword == "xlo xhi" or keyword == "ylo yhi" or keyword == "zlo zhi":
                    pair = self.headers[keyword]
                    print(pair[0], pair[1], keyword,file=f)
                elif keyword == "xy xz yz":
                    triple = self.headers[keyword]
                    print(triple[0], triple[1], triple[2], keyword,file=f)
                else:
                    print(self.headers[keyword], keyword,file=f)
        for pair in skeywords:
            keyword = pair[0]
            if keyword in self.sections: #self.sections.has_key(keyword):
                print("\n%s\n" % keyword,file=f)
                for line in self.sections[keyword]:
                    print(line,file=f,end="")
        f.close()

    # --------------------------------------------------------------------
    # iterator called from other tools

    def iterator(self, flag):
        if flag == 0:
            return 0, 0, 1
        return 0, 0, -1

    # --------------------------------------------------------------------
    # time query from other tools

    def findtime(self, n):
        if n == 0:
            return 0
        raise ValueError("no step %d exists" % n)

    # --------------------------------------------------------------------
    # return list of atoms and bonds to viz for data object

    def viz(self, isnap):
        if isnap:
            raise ValueError("cannot call data.viz() with isnap != 0")

        id = self.names["id"]
        type = self.names["type"]
        x = self.names["x"]
        y = self.names["y"]
        z = self.names["z"]

        xlohi = self.headers["xlo xhi"]
        ylohi = self.headers["ylo yhi"]
        zlohi = self.headers["zlo zhi"]
        box = [xlohi[0], ylohi[0], zlohi[0], xlohi[1], ylohi[1], zlohi[1]]

        # create atom list needed by viz from id,type,x,y,z

        atoms = []
        atomlines = self.sections["Atoms"]
        for line in atomlines:
            words = line.split()
            atoms.append(
                [
                    int(words[id]),
                    int(words[type]),
                    float(words[x]),
                    float(words[y]),
                    float(words[z]),
                ]
            )

        # create list of current bond coords from list of bonds
        # assumes atoms are sorted so can lookup up the 2 atoms in each bond

        bonds = []
        if self.sections.has_key("Bonds"):
            bondlines = self.sections["Bonds"]
            for line in bondlines:
                words = line.split()
                bid, btype = int(words[0]), int(words[1])
                atom1, atom2 = int(words[2]), int(words[3])
                atom1words = atomlines[atom1 - 1].split()
                atom2words = atomlines[atom2 - 1].split()
                bonds.append(
                    [
                        bid,
                        btype,
                        float(atom1words[x]),
                        float(atom1words[y]),
                        float(atom1words[z]),
                        float(atom2words[x]),
                        float(atom2words[y]),
                        float(atom2words[z]),
                        float(atom1words[type]),
                        float(atom2words[type]),
                    ]
                )

        tris = []
        lines = []
        return 0, box, atoms, bonds, tris, lines

    # --------------------------------------------------------------------
    # return box size

    def maxbox(self):
        xlohi = self.headers["xlo xhi"]
        ylohi = self.headers["ylo yhi"]
        zlohi = self.headers["zlo zhi"]
        return [xlohi[0], ylohi[0], zlohi[0], xlohi[1], ylohi[1], zlohi[1]]

    # --------------------------------------------------------------------
    # return number of atom types

    def maxtype(self):
        return self.headers["atom types"]


# --------------------------------------------------------------------
# data file keywords, both header and main sections

hkeywords = [
    "atoms",
    "ellipsoids",
    "lines",
    "triangles",
    "bodies",
    "bonds",
    "angles",
    "dihedrals",
    "impropers",
    "atom types",
    "bond types",
    "angle types",
    "dihedral types",
    "improper types",
    "xlo xhi",
    "ylo yhi",
    "zlo zhi",
    "xy xz yz",
]

skeywords = [
    ["Masses", "atom types"],
    ["Atoms", "atoms"],
    ["Ellipsoids", "ellipsoids"],
    ["Lines", "lines"],
    ["Triangles", "triangles"],
    ["Bodies", "bodies"],
    ["Bonds", "bonds"],
    ["Angles", "angles"],
    ["Dihedrals", "dihedrals"],
    ["Impropers", "impropers"],
    ["Velocities", "atoms"],
    ["Pair Coeffs", "atom types"],
    ["Bond Coeffs", "bond types"],
    ["Angle Coeffs", "angle types"],
    ["Dihedral Coeffs", "dihedral types"],
    ["Improper Coeffs", "improper types"],
    ["BondBond Coeffs", "angle types"],
    ["BondAngle Coeffs", "angle types"],
    ["MiddleBondTorsion Coeffs", "dihedral types"],
    ["EndBondTorsion Coeffs", "dihedral types"],
    ["AngleTorsion Coeffs", "dihedral types"],
    ["AngleAngleTorsion Coeffs", "dihedral types"],
    ["BondBond13 Coeffs", "dihedral types"],
    ["AngleAngle Coeffs", "improper types"],
    ["Molecules", "atoms"],
    ["Tinker Types", "atoms"],
]

# %%
# ===================================================
# main()
# ===================================================
# for debugging purposes (code called as a script)
# the code is called from here
# ===================================================
if __name__ == '__main__':
    datafile = "../data/play_data/data.play.lmp"
    X = data(datafile)
    Y = dump("../data/play_data/dump.play.restartme")
    t = Y.time()
    step = 2000
    R = data(Y,step)
    R.write("../tmp/data.myfirstrestart.lmp")
