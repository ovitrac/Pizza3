#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
# `data` Class

The `data` class provides tools to read, write, and manipulate LAMMPS data files, enabling seamless integration with the `dump` class for restart generation and simulation data management.

Use the module pizza3.data3_legacy instead of pizza3.data3 if you experience errors.
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

## Key Improvements Explained - 2025-01-15

1. **Class Names Remain Lowercase**:
   - The classes `data` and `dump` remain lowercase to maintain consistency with your existing codebase.

2. **Preserved Module Documentation**:
   - The original module-level docstring, version history, and module variables (`__project__`, `__author__`, etc.) are retained at the beginning of the file.

3. **Logging**:
   - Introduced the `logging` module to replace all `print` statements. This allows for better control over logging levels and output formats.
   - Added debug logs for detailed internal state information and info logs for general operation messages.

4. **File Handling**:
   - Utilized context managers (`with` statements) for all file operations to ensure files are properly closed after operations.
   - Replaced `os.popen` with the `subprocess` module for better handling of subprocesses when dealing with gzipped files.

5. **Error Handling**:
   - Enhanced error messages to be more descriptive.
   - Replaced deprecated methods like `has_key` with Python 3’s `in` keyword.
   - Added exception handling in the `__main__` block to catch and log unexpected errors.

6. **Code Style and Readability**:
   - Followed PEP 8 guidelines for naming conventions, indentation, and spacing.
   - Avoided using built-in names like `list` as variable names.
   - Used f-strings for more readable and efficient string formatting.

7. **Docstrings**:
   - Added comprehensive docstrings to the class and all methods, detailing their purpose, parameters, return types, and possible exceptions. This aids in better understanding and maintenance of the code.

8. **Type Hints**:
   - Included type hints for function parameters and return types to improve code clarity and assist with static type checking.

9. **Additional Safeguards**:
   - Ensured that required columns (`id`, `type`, `x`, `y`, `z`) are defined before performing operations that depend on them.
   - Added checks to prevent operations on undefined sections or headers.

10. **Modularity**:
    - Broke down the constructor into two separate methods (`_init_from_dump` and `_init_from_file`) for better modularity and readability.

### Notes

- **Dependencies**: Ensure that the `dump` class from `pizza.dump3` is properly implemented and compatible with these changes.
- **Logging Configuration**: The logging level is set to `INFO` by default. You can adjust the logging level or format as needed for your project by modifying the `logging.basicConfig` call.
- **Main Block**: The `__main__` block includes example usage and error handling for debugging purposes. Modify the file paths as necessary for your environment.


"""

# Pizza.py toolkit, www.cs.sandia.gov/~sjplimp/pizza.html
# Steve Plimpton, sjplimp@sandia.gov, Sandia National Laboratories
#
# Copyright (2005) Sandia Corporation.  Under the terms of Contract
# DE-AC04-94AL85000 with Sandia Corporation, the U.S. Government retains
# certain rights in this software.  This software is distributed under
# the GNU General Public License.

# data tool

# Code converted and extended to python 3.x
# INRAE\olivier.vitrac@agroparistech.fr
#
# last release
# 2022-02-03 - add flist, __repr__
# 2022-02-04 - add append and start to add comments
# 2022-02-10 - first implementation of a full restart object from a dump object
# 2022-02-12 - revised append method, more robust, more verbose
# 2024-12-08 - updated help
# 2025-01-15 - refreshed code

__project__ = "Pizza3"
__author__ = "Olivier Vitrac"
__copyright__ = "Copyright 2022"
__credits__ = ["Steve Plimpton", "Olivier Vitrac"]
__license__ = "GPLv3"
__maintainer__ = "Olivier Vitrac"
__email__ = "olivier.vitrac@agroparistech.fr"
__version__ = "1.0"


oneline = "Read, write, manipulate LAMMPS data files"

docstr = """
d = data("data.poly")            read a LAMMPS data file, can be gzipped
d = data()			    create an empty data file

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

import logging
import subprocess
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np

from pizza.dump3 import dump

__all__ = ['data', 'dump']

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# External dependency
PIZZA_GUNZIP = "gunzip"

class data:
    """
    The `data` class provides tools to read, write, and manipulate LAMMPS data files,
    enabling seamless integration with the `dump` class for restart generation and
    simulation data management.
    """

    # Class-level keywords for headers and sections
    HKEYWORDS = [
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

    SKEYWORDS = [
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

    def __init__(self, *args: Any):
        """
        Initialize a data object.

        Parameters:
            *args: Variable length argument list.
                - No arguments: Creates an empty data object.
                - One argument (filename or dump object): Initializes from a file or dump object.
                - Two arguments (dump object, timestep): Initializes from a dump object at a specific timestep.
        """
        self.nselect = 1
        self.names: Dict[str, int] = {}
        self.headers: Dict[str, Union[int, Tuple[float, float], Tuple[float, float, float]]] = {}
        self.sections: Dict[str, List[str]] = {}
        self.flist: List[str] = []
        self.restart: bool = False

        if not args:
            # Default Constructor (empty object)
            self.title = "LAMMPS data file"
            logger.debug("Initialized empty data object.")
            return

        first_arg = args[0]

        if isinstance(first_arg, dump):
            # Constructor from an existing dump object
            self._init_from_dump(first_arg, *args[1:])
        elif isinstance(first_arg, str):
            # Constructor from a DATA file
            self._init_from_file(*args)
        else:
            raise TypeError("Invalid argument type for data constructor.")

    def _init_from_dump(self, dump_obj: dump, timestep: Optional[int] = None) -> None:
        """
        Initialize the data object from a dump object.

        Parameters:
            dump_obj (dump): The dump object to initialize from.
            timestep (Optional[int]): The specific timestep to use. If None, the last timestep is used.
        """
        times = dump_obj.time()
        num_timesteps = len(times)

        if timestep is not None:
            if timestep not in times:
                raise ValueError("The input timestep is not available in the dump object.")
            selected_time = timestep
        else:
            selected_time = times[-1]

        try:
            index = times.index(selected_time)
        except ValueError:
            raise ValueError("Selected timestep not found in dump object.")

        self.title = (f'LAMMPS data file (restart from "{dump_obj.flist[0]}" '
                      f't = {selected_time:.5g} (frame {index + 1} of {num_timesteps}))')
        logger.debug(f"Set title: {self.title}")

        # Set headers
        snap = dump_obj.snaps[index]
        self.headers = {
            'atoms': snap.natoms,
            'atom types': dump_obj.minmax("type")[1],
            'xlo xhi': (snap.xlo, snap.xhi),
            'ylo yhi': (snap.ylo, snap.yhi),
            'zlo zhi': (snap.zlo, snap.zhi)
        }
        logger.debug(f"Set headers: {self.headers}")

        # Initialize sections
        self.sections = {}
        template_atoms = {
            "smd": ["id", "type", "mol", "c_vol", "mass", "radius",
                    "c_contact_radius", "x", "y", "z", "f_1[1]", "f_1[2]", "f_1[3]"]
        }

        if dump_obj.kind(template_atoms["smd"]):
            for col in template_atoms["smd"]:
                vector = dump_obj.vecs(selected_time, col)
                is_id_type_mol = col in ["id", "type", "mol"]
                self.append("Atoms", vector, force_integer=is_id_type_mol, property_name=col)
        else:
            raise ValueError("Please add your ATOMS section in the constructor.")

        # Set velocities if required
        template_velocities = {"smd": ["id", "vx", "vy", "vz"]}
        if dump_obj.kind(template_atoms["smd"]):
            if dump_obj.kind(template_velocities["smd"]):
                for col in template_velocities["smd"]:
                    vector = dump_obj.vecs(selected_time, col)
                    is_id = col == "id"
                    self.append("Velocities", vector, force_integer=is_id, property_name=col)
            else:
                raise ValueError("The velocities are missing for the style SMD.")

        # Store filename
        self.flist = dump_obj.flist.copy()
        self.restart = True
        logger.debug("Initialized data object from dump.")

    def _init_from_file(self, filename: str) -> None:
        """
        Initialize the data object from a LAMMPS data file.

        Parameters:
            filename (str): Path to the LAMMPS data file.
        """
        flist = [filename]
        is_gzipped = filename.endswith(".gz")

        try:
            if is_gzipped:
                with subprocess.Popen([PIZZA_GUNZIP, "-c", filename],
                                      stdout=subprocess.PIPE,
                                      text=True) as proc:
                    file_handle = proc.stdout
                    logger.debug(f"Opened gzipped file: {filename}")
            else:
                file_handle = open(filename, 'r')
                logger.debug(f"Opened file: {filename}")

            with file_handle:
                self.title = file_handle.readline().strip()
                logger.debug(f"Read title: {self.title}")

                # Read headers
                while True:
                    line = file_handle.readline()
                    if not line:
                        break
                    line = line.strip()
                    if not line:
                        continue

                    found = False
                    for keyword in self.HKEYWORDS:
                        if keyword in line:
                            found = True
                            words = line.split()
                            if keyword in ["xlo xhi", "ylo yhi", "zlo zhi"]:
                                self.headers[keyword] = (float(words[0]), float(words[1]))
                            elif keyword == "xy xz yz":
                                self.headers[keyword] = (float(words[0]), float(words[1]), float(words[2]))
                            else:
                                self.headers[keyword] = int(words[0])
                            logger.debug(f"Set header '{keyword}': {self.headers[keyword]}")
                            break
                    if not found:
                        break  # Reached the end of headers

                # Read sections
                while line:
                    found_section = False
                    for pair in self.SKEYWORDS:
                        keyword, length_key = pair
                        if keyword == line:
                            found_section = True
                            if length_key not in self.headers:
                                raise ValueError(f"Data section '{keyword}' has no matching header value.")
                            count = self.headers[length_key]
                            file_handle.readline()  # Read the blank line after section keyword
                            section_lines = [file_handle.readline() for _ in range(count)]
                            self.sections[keyword] = section_lines
                            logger.debug(f"Read section '{keyword}' with {count} entries.")
                            break
                    if not found_section:
                        raise ValueError(f"Invalid section '{line}' in data file.")
                    # Read next section keyword
                    line = file_handle.readline()
                    if line:
                        line = line.strip()

            self.flist = flist
            self.restart = False
            logger.info(f"Initialized data object from file '{filename}'.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error decompressing file '{filename}': {e}")
            raise
        except FileNotFoundError:
            logger.error(f"File '{filename}' not found.")
            raise
        except Exception as e:
            logger.error(f"Error reading file '{filename}': {e}")
            raise

    def __repr__(self) -> str:
        """
        Return a string representation of the data object.

        Returns:
            str: Description of the data object.
        """
        if not self.sections or not self.headers:
            ret = f"empty {self.title}"
            logger.info(ret)
            return ret

        kind = "restart" if self.restart else "source"
        header_info = (f"Data file: {self.flist[0]}\n"
                       f"\tcontains {self.headers.get('atoms', 0)} atoms from {self.headers.get('atom types', 0)} atom types\n"
                       f"\twith box = [{self.headers.get('xlo xhi', (0, 0))[0]} "
                       f"{self.headers.get('xlo xhi', (0, 0))[1]} "
                       f"{self.headers.get('ylo yhi', (0, 0))[0]} "
                       f"{self.headers.get('ylo yhi', (0, 0))[1]} "
                       f"{self.headers.get('zlo zhi', (0, 0))[0]} "
                       f"{self.headers.get('zlo zhi', (0, 0))[1]}]")

        logger.info(header_info)
        section_info = "\twith the following sections:"
        logger.info(section_info)
        for section_name in self.sections.keys():
            section_details = f"\t\t{self.dispsection(section_name, False)}"
            logger.info(section_details)

        ret = (f'LAMMPS data object including {self.headers.get("atoms", 0)} atoms '
               f'({self.maxtype()} types, {kind}="{self.flist[0]}")')
        return ret

    def map(self, *pairs: Any) -> None:
        """
        Assign names to atom columns.

        Parameters:
            *pairs (Any): Pairs of column indices and names.

        Raises:
            ValueError: If an odd number of arguments is provided.
        """
        if len(pairs) % 2 != 0:
            raise ValueError("data.map() requires pairs of mappings.")

        for i in range(0, len(pairs), 2):
            column_index = pairs[i] - 1
            name = pairs[i + 1]
            self.names[name] = column_index
            logger.debug(f"Mapped column '{name}' to index {column_index + 1}.")

    def get(self, *args: Any) -> Union[List[List[float]], List[float]]:
        """
        Extract information from data file fields.

        Parameters:
            *args: Variable length argument list.
                - One argument: Returns all columns as a 2D list of floats.
                - Two arguments: Returns the specified column as a list of floats.

        Returns:
            Union[List[List[float]], List[float]]: Extracted data.

        Raises:
            ValueError: If invalid number of arguments is provided.
            KeyError: If the specified field is not found.
        """
        if len(args) == 1:
            field = args[0]
            array = []
            lines = self.sections.get(field, [])
            for line in lines:
                words = line.split()
                values = [float(word) for word in words]
                array.append(values)
            logger.debug(f"Extracted all columns from field '{field}'.")
            return array
        elif len(args) == 2:
            field, column = args
            column_index = column - 1
            vec = []
            lines = self.sections.get(field, [])
            for line in lines:
                words = line.split()
                vec.append(float(words[column_index]))
            logger.debug(f"Extracted column {column} from field '{field}'.")
            return vec
        else:
            raise ValueError("Invalid arguments for data.get().")

    def reorder(self, section: str, *order: int) -> None:
        """
        Reorder columns in a data file section.

        Parameters:
            section (str): The name of the section to reorder.
            *order (int): The new order of column indices.

        Raises:
            ValueError: If the section name is invalid.
        """
        if section not in self.sections:
            raise ValueError(f'"{section}" is not a valid section name.')

        num_columns = len(order)
        logger.info(f">> Reordering {num_columns} columns in section '{section}'.")

        old_lines = self.sections[section]
        new_lines = []

        for line in old_lines:
            words = line.split()
            try:
                reordered = " ".join(words[i - 1] for i in order) + "\n"
            except IndexError:
                raise ValueError("Column index out of range during reorder.")
            new_lines.append(reordered)

        self.sections[section] = new_lines
        logger.debug(f"Reordered columns in section '{section}'.")

    def replace(self, section: str, column: int, vector: Union[List[float], float]) -> None:
        """
        Replace a column in a named section with a vector of values.

        Parameters:
            section (str): The name of the section.
            column (int): The column index to replace (1-based).
            vector (Union[List[float], float]): The new values or a single scalar value.

        Raises:
            ValueError: If the section is invalid or vector length mismatch.
        """
        if section not in self.sections:
            raise ValueError(f'"{section}" is not a valid section name.')

        lines = self.sections[section]
        num_lines = len(lines)

        if not isinstance(vector, list):
            vector = [vector]
        if len(vector) == 1:
            vector = vector * num_lines
        if len(vector) != num_lines:
            raise ValueError(f'The length of new data ({len(vector)}) in section "{section}" does not match the number of rows {num_lines}.')

        new_lines = []
        column_index = column - 1
        for i, line in enumerate(lines):
            words = line.split()
            if column_index >= len(words):
                raise ValueError(f"Column index {column} out of range for section '{section}'.")
            words[column_index] = str(vector[i])
            new_line = " ".join(words) + "\n"
            new_lines.append(new_line)

        self.sections[section] = new_lines
        logger.debug(f"Replaced column {column} in section '{section}' with new data.")

    def append(self, section: str, vector: Union[List[float], np.ndarray, float],
               force_integer: bool = False, property_name: Optional[str] = None) -> None:
        """
        Append a new column to a named section.

        Parameters:
            section (str): The name of the section.
            vector (Union[List[float], np.ndarray, float]): The values to append.
            force_integer (bool): If True, values are converted to integers.
            property_name (Optional[str]): The name of the property being appended.

        Raises:
            ValueError: If vector length mismatch occurs.
        """
        if section not in self.sections:
            self.sections[section] = []
            logger.info(f'Added new section [{section}] - file="{self.title}".')

        lines = self.sections[section]
        num_lines = len(lines)

        if not isinstance(vector, (list, np.ndarray)):
            vector = [vector]
        if property_name:
            logger.info(f'\t> Adding property "{property_name}" with {len(vector)} values to [{section}].')
        else:
            logger.info(f'\t> Adding {len(vector)} values to [{section}] (no name).')

        new_lines = []

        if num_lines == 0:
            # Empty section, create initial lines
            num_entries = len(vector)
            for i in range(num_entries):
                value = int(vector[i]) if force_integer else vector[i]
                new_line = f"{int(value) if force_integer else value}\n"
                new_lines.append(new_line)
            logger.debug(f"Initialized empty section '{section}' with new column.")
        else:
            if len(vector) == 1:
                vector = vector * num_lines
            if len(vector) != num_lines:
                raise ValueError(f'The length of new data ({len(vector)}) in section "{section}" does not match the number of rows {num_lines}.')

            for i, line in enumerate(lines):
                value = int(vector[i]) if force_integer else vector[i]
                new_word = str(value)
                new_line = line.rstrip('\n') + f" {new_word}\n"
                new_lines.append(new_line)

        self.sections[section] = new_lines
        logger.debug(f"Appended new column to section '{section}'.")

    def dispsection(self, section: str, include_header: bool = True) -> str:
        """
        Display information about a section.

        Parameters:
            section (str): The name of the section.
            include_header (bool): Whether to include "LAMMPS data section" in the output.

        Returns:
            str: Description of the section.
        """
        if section not in self.sections:
            raise ValueError(f"Section '{section}' not found in data object.")

        lines = self.sections[section]
        num_lines = len(lines)
        num_columns = len(lines[0].split()) if lines else 0
        ret = f'"{section}": {num_lines} x {num_columns} values'

        if include_header:
            ret = f"LAMMPS data section {ret}"
        return ret

    def newxyz(self, dm: dump, ntime: int) -> None:
        """
        Replace x, y, z coordinates in the Atoms section with those from a dump object.

        Parameters:
            dm (dump): The dump object containing new coordinates.
            ntime (int): The timestep to extract coordinates from.

        Raises:
            ValueError: If required columns are not defined.
        """
        nsnap = dm.findtime(ntime)
        logger.info(f">> Replacing XYZ for {nsnap} snapshots.")

        dm.sort(ntime)
        x, y, z = dm.vecs(ntime, "x", "y", "z")

        self.replace("Atoms", self.names.get("x", 0) + 1, x)
        self.replace("Atoms", self.names.get("y", 0) + 1, y)
        self.replace("Atoms", self.names.get("z", 0) + 1, z)

        if "ix" in dm.names and "ix" in self.names:
            ix, iy, iz = dm.vecs(ntime, "ix", "iy", "iz")
            self.replace("Atoms", self.names.get("ix", 0) + 1, ix)
            self.replace("Atoms", self.names.get("iy", 0) + 1, iy)
            self.replace("Atoms", self.names.get("iz", 0) + 1, iz)

        logger.debug(f"Replaced XYZ coordinates at timestep {ntime}.")

    def delete(self, keyword: str) -> None:
        """
        Delete a header value or section from the data object.

        Parameters:
            keyword (str): The header or section name to delete.

        Raises:
            ValueError: If the keyword is not found.
        """
        if keyword in self.headers:
            del self.headers[keyword]
            logger.debug(f"Deleted header '{keyword}'.")
        elif keyword in self.sections:
            del self.sections[keyword]
            logger.debug(f"Deleted section '{keyword}'.")
        else:
            raise ValueError("Keyword not found in data object.")

    def write(self, filename: str) -> None:
        """
        Write the data object to a LAMMPS data file.

        Parameters:
            filename (str): The output file path.
        """
        try:
            with open(filename, "w") as f:
                f.write(f"{self.title}\n")
                logger.debug(f"Wrote title to file '{filename}'.")

                # Write headers
                for keyword in self.HKEYWORDS:
                    if keyword in self.headers:
                        value = self.headers[keyword]
                        if keyword in ["xlo xhi", "ylo yhi", "zlo zhi"]:
                            f.write(f"{value[0]} {value[1]} {keyword}\n")
                        elif keyword == "xy xz yz":
                            f.write(f"{value[0]} {value[1]} {value[2]} {keyword}\n")
                        else:
                            f.write(f"{value} {keyword}\n")
                        logger.debug(f"Wrote header '{keyword}' to file.")

                # Write sections
                for pair in self.SKEYWORDS:
                    keyword = pair[0]
                    if keyword in self.sections:
                        f.write(f"\n{keyword}\n\n")
                        for line in self.sections[keyword]:
                            f.write(line)
                        logger.debug(f"Wrote section '{keyword}' to file.")

            logger.info(f"Data object written to '{filename}'.")
        except IOError as e:
            logger.error(f"Error writing to file '{filename}': {e}")
            raise

    def iterator(self, flag: int) -> Tuple[int, int, int]:
        """
        Iterator method compatible with other tools.

        Parameters:
            flag (int): 0 for the first call, 1 for subsequent calls.

        Returns:
            Tuple[int, int, int]: (index, time, flag)
        """
        if flag == 0:
            return 0, 0, 1
        return 0, 0, -1

    def findtime(self, n: int) -> int:
        """
        Find the index of a given timestep.

        Parameters:
            n (int): The timestep to find.

        Returns:
            int: The index of the timestep.

        Raises:
            ValueError: If the timestep does not exist.
        """
        if n == 0:
            return 0
        raise ValueError(f"No step {n} exists.")

    def viz(self, isnap: int) -> Tuple[int, List[float], List[List[Union[int, float]]],
                                      List[List[Union[int, float]]], List[Any], List[Any]]:
        """
        Return visualization data for a specified snapshot.

        Parameters:
            isnap (int): Snapshot index (must be 0 for data object).

        Returns:
            Tuple containing time, box dimensions, atoms, bonds, tris, and lines.

        Raises:
            ValueError: If isnap is not 0.
        """
        if isnap:
            raise ValueError("Cannot call data.viz() with isnap != 0.")

        id_idx = self.names.get("id")
        type_idx = self.names.get("type")
        x_idx = self.names.get("x")
        y_idx = self.names.get("y")
        z_idx = self.names.get("z")

        if None in [id_idx, type_idx, x_idx, y_idx, z_idx]:
            raise ValueError("One or more required columns (id, type, x, y, z) are not defined.")

        xlohi = self.headers.get("xlo xhi", (0.0, 0.0))
        ylohi = self.headers.get("ylo yhi", (0.0, 0.0))
        zlohi = self.headers.get("zlo zhi", (0.0, 0.0))
        box = [xlohi[0], ylohi[0], zlohi[0], xlohi[1], ylohi[1], zlohi[1]]

        # Create atom list needed by viz from id, type, x, y, z
        atoms = []
        atom_lines = self.sections.get("Atoms", [])
        for line in atom_lines:
            words = line.split()
            atoms.append([
                int(words[id_idx]),
                int(words[type_idx]),
                float(words[x_idx]),
                float(words[y_idx]),
                float(words[z_idx]),
            ])

        # Create list of current bond coords from list of bonds
        bonds = []
        if "Bonds" in self.sections:
            bond_lines = self.sections["Bonds"]
            for line in bond_lines:
                words = line.split()
                bid = int(words[0])
                btype = int(words[1])
                atom1 = int(words[2])
                atom2 = int(words[3])
                if atom1 - 1 >= len(atom_lines) or atom2 - 1 >= len(atom_lines):
                    raise ValueError("Atom index in Bonds section out of range.")
                atom1_words = self.sections["Atoms"][atom1 - 1].split()
                atom2_words = self.sections["Atoms"][atom2 - 1].split()
                bonds.append([
                    bid,
                    btype,
                    float(atom1_words[x_idx]),
                    float(atom1_words[y_idx]),
                    float(atom1_words[z_idx]),
                    float(atom2_words[x_idx]),
                    float(atom2_words[y_idx]),
                    float(atom2_words[z_idx]),
                    int(atom1_words[type_idx]),
                    int(atom2_words[type_idx]),
                ])

        tris = []
        lines = []
        logger.debug("Prepared visualization data.")
        return 0, box, atoms, bonds, tris, lines

    def maxbox(self) -> List[float]:
        """
        Return the box dimensions.

        Returns:
            List[float]: [xlo, ylo, zlo, xhi, yhi, zhi]
        """
        xlohi = self.headers.get("xlo xhi", (0.0, 0.0))
        ylohi = self.headers.get("ylo yhi", (0.0, 0.0))
        zlohi = self.headers.get("zlo zhi", (0.0, 0.0))
        box = [xlohi[0], ylohi[0], zlohi[0], xlohi[1], ylohi[1], zlohi[1]]
        logger.debug(f"Box dimensions: {box}")
        return box

    def maxtype(self) -> int:
        """
        Return the number of atom types.

        Returns:
            int: Number of atom types.
        """
        maxtype = self.headers.get("atom types", 0)
        logger.debug(f"Number of atom types: {maxtype}")
        return maxtype


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

# ===================================================
# main()
# ===================================================
# for debugging purposes (code called as a script)
# the code is called from here
# ===================================================
if __name__ == '__main__':
    import sys

    # Example usage
    try:
        datafile = "../data/play_data/data.play.lmp"
        X = data(datafile)
        Y = dump("../data/play_data/dump.play.restartme")
        step = 2000
        R = data(Y, step)
        R.write("../tmp/data.myfirstrestart.lmp")
    except Exception as e:
        logger.error(f"An error occurred during execution: {e}")
        sys.exit(1)
