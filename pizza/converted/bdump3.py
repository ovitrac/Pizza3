#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__all__ = ['Snap', 'bdump']
# bdump3.py

"""
bdump3.py

Module converted from Python 2.x to Python 3.x.

bdump tool

Read and process dump files with bond information for visualization purposes.

## Usage

    b = bdump("dump.one")                 # Read one or more dump files
    b = bdump("dump.1 dump.2.gz")         # Can handle gzipped files
    b = bdump("dump.*")                    # Wildcard expands to multiple files
    b = bdump("dump.*", 0)                 # Two arguments: store filenames but don't read

    time = b.next()                        # Read next snapshot from dump files

    b.map(1, "id", 3, "x")                  # Assign names to atom columns

    time, box, atoms, bonds, tris, lines = b.viz(index)   # Return list of viz objects

      - `viz()` returns bond info for the specified timestep index
      - Can also call as `viz(time, 1)` to find index of preceding snapshot
      - `box`, `atoms`, `tris`, `lines` are `None` as bdump handles bonds only

## Notes

- Incomplete and duplicate snapshots are deleted.
- No column name assignment is performed unless explicitly mapped.
- `viz()` is tailored for visualization tools that require bond information.

## History

- 11/10, Steve Plimpton (SNL): original version
- 2025-01-17, INRAE\Olivier Vitrac conversion

## Dependencies

- Python 3.x
- `numpy` library (fallback to `Numeric` if `numpy` is not available)

"""

# History
#   11/10, Steve Plimpton (SNL): original version
# 2025-01-17, first conversion in connection with the update of pizza.dump3


# Imports and external programs

import sys
import glob
from os import popen
from math import sqrt
from copy import deepcopy
import numpy as np


# Define external dependency directly
PIZZA_GUNZIP = "gunzip"

# --------------------------------------------------------------------
# Helper Classes and Functions

class Snap:
    """
    Represents a single snapshot from a dump file.
    
    Attributes:
        time (int): Time stamp of the snapshot.
        natoms (int): Number of atoms in the snapshot.
        atoms (numpy.ndarray or list): Array of atom data.
    """
    def __init__(self):
        self.time = 0
        self.natoms = 0
        self.atoms = None

# --------------------------------------------------------------------
# bdump Class Definition

class bdump:
    """
    bdump class for reading and processing ChemCell dump files with bond information.
    """
    
    # --------------------------------------------------------------------
    
    def __init__(self, *args):
        """
        Initialize the bdump object.
        
        Parameters:
            *args: Variable length argument list.
                   - If one argument, it's the list of files to read.
                   - If two arguments, the second argument indicates incremental reading.
        """
        self.snaps = []
        self.nsnaps = 0
        self.names = {}
        
        # flist = list of all dump file names
        if len(args) == 0:
            raise Exception("No dump files specified for bdump.")
        
        words = args[0].split()
        self.flist = []
        for word in words:
            self.flist += glob.glob(word)
        
        if len(self.flist) == 0 and len(args) == 1:
            raise Exception("No bdump file specified.")
        
        if len(args) == 1:
            self.increment = 0
            self.read_all()
        else:
            self.increment = 1
            self.nextfile = 0
            self.eof = 0
    
    # --------------------------------------------------------------------
    
    def read_all(self):
        """
        Read all snapshots from the list of dump files.
        """
        for file in self.flist:
            # Test for gzipped file
            if file.endswith(".gz"):
                try:
                    f = popen(f"{PIZZA_GUNZIP} -c {file}", 'r')
                except Exception as e:
                    print(f"Error opening gzipped file {file}: {e}")
                    continue
            else:
                try:
                    f = open(file, 'r')
                except Exception as e:
                    print(f"Error opening file {file}: {e}")
                    continue
    
            # Read all snapshots in the current file
            while True:
                snap = self.read_snapshot(f)
                if not snap:
                    break
                self.snaps.append(snap)
                print(snap.time, end=' ')
                sys.stdout.flush()
    
            f.close()
        print()
    
        # Sort entries by timestep and remove duplicates
        self.snaps.sort(key=lambda x: x.time)
        self.cull()
        self.nsnaps = len(self.snaps)
        print(f"read {self.nsnaps} snapshots")
    
    # --------------------------------------------------------------------
    # Read the next snapshot from the list of files (incremental reading)
    
    def next(self):
        """
        Read the next snapshot in incremental mode.
        
        Returns:
            int: Time stamp of the snapshot read, or -1 if no snapshots left.
        """
        if not self.increment:
            raise Exception("Cannot read incrementally with current bdump configuration.")
    
        # Read next snapshot in current file using eof as pointer
        while self.nextfile < len(self.flist):
            file = self.flist[self.nextfile]
            # Open the current file
            if file.endswith(".gz"):
                try:
                    f = popen(f"{PIZZA_GUNZIP} -c {file}", 'r')
                except Exception as e:
                    print(f"Error opening gzipped file {file}: {e}")
                    self.nextfile += 1
                    continue
            else:
                try:
                    f = open(file, 'r')
                except Exception as e:
                    print(f"Error opening file {file}: {e}")
                    self.nextfile += 1
                    continue
    
            # Seek to the last read position
            f.seek(self.eof)
            snap = self.read_snapshot(f)
            if not snap:
                # End of file reached
                f.close()
                self.nextfile += 1
                self.eof = 0
                continue
            self.eof = f.tell()
            f.close()
            
            # Check for duplicate time stamp
            if any(existing_snap.time == snap.time for existing_snap in self.snaps):
                continue  # Skip duplicate
            self.snaps.append(snap)
            self.nsnaps += 1
            return snap.time
    
        return -1  # No snapshots left
    
    # --------------------------------------------------------------------
    # Read a single snapshot from a file
    
    def read_snapshot(self, f):
        """
        Read a single snapshot from the file.
        
        Parameters:
            f (file object): Opened file object to read from.
        
        Returns:
            Snap: Snapshot object, or None if failed.
        """
        try:
            snap = Snap()
            # Read time stamp
            line = f.readline()
            if not line:
                return None
            snap.time = int(f.readline().strip().split()[0])  # Read first field as time
            # Read number of atoms
            f.readline()  # Read past header
            line = f.readline()
            if not line:
                return None
            snap.natoms = int(line.strip())
            f.readline()  # Read past another header
    
            # Read past BOX BOUNDS
            f.readline()
            f.readline()
            f.readline()
            f.readline()
    
            if snap.natoms:
                # Read atom data
                words = f.readline().split()
                ncol = len(words)
                atoms = []
                atoms.append([float(value) for value in words])
                for _ in range(1, snap.natoms):
                    words = f.readline().split()
                    if not words:
                        break
                    atoms.append([float(value) for value in words])
                snap.atoms = np.array(atoms, dtype=float)
            else:
                snap.atoms = None
            return snap
        except Exception as e:
            print(f"Error reading snapshot: {e}")
            return None
    
    # --------------------------------------------------------------------
    # Map atom column names
    
    def map(self, *pairs):
        """
        Assign names to atom columns.
        
        Parameters:
            *pairs: Pairs of (column_number, "column_name")
        """
        if len(pairs) % 2 != 0:
            raise Exception("bdump map() requires pairs of mappings.")
        for i in range(0, len(pairs), 2):
            col_num = pairs[i]
            col_name = pairs[i + 1]
            self.names[col_name] = col_num - 1  # Zero-based indexing
    
    # --------------------------------------------------------------------
    # Return vector of snapshot time stamps
    
    def time(self):
        """
        Get a list of all snapshot time stamps.
        
        Returns:
            list: List of time stamps.
        """
        return [snap.time for snap in self.snaps]
    
    # --------------------------------------------------------------------
    # Delete successive snapshots with duplicate time stamps
    
    def cull(self):
        """
        Remove duplicate snapshots based on time stamps.
        """
        unique_snaps = []
        seen_times = set()
        for snap in self.snaps:
            if snap.time not in seen_times:
                unique_snaps.append(snap)
                seen_times.add(snap.time)
        self.snaps = unique_snaps
    
    # --------------------------------------------------------------------
    # Return list of bonds to viz for snapshot isnap
    
    def viz(self, index, flag=0):
        """
        Return bond information for visualization.
        
        Parameters:
            index (int): Snapshot index or time stamp.
            flag (int): If 1, interpret index as time stamp.
        
        Returns:
            tuple: (time, box, atoms, bonds, tris, lines)
                   box, atoms, tris, lines are None.
                   bonds contain [id, type, atom1, atom2] for each bond.
        """
        if flag:
            # Find snapshot index based on time stamp
            times = self.time()
            isnap = -1
            for i, t in enumerate(times):
                if t > index:
                    break
                isnap = i
            if isnap == -1:
                return (-1, None, None, None, None, None)
        else:
            isnap = index
            if isnap < 0 or isnap >= self.nsnaps:
                return (-1, None, None, None, None, None)
        
        snap = self.snaps[isnap]
        time = snap.time
        
        # Retrieve column indices
        try:
            id_col = self.names["id"]
            type_col = self.names["type"]
            atom1_col = self.names["atom1"]
            atom2_col = self.names["atom2"]
        except KeyError as e:
            print(f"Column name {e} not mapped. Use b.map() to assign column names.")
            return (time, None, None, None, None, None)
        
        # Create bond list
        bonds = []
        for i in range(snap.natoms):
            atom = snap.atoms[i]
            bond_id = int(atom[id_col])
            bond_type = abs(int(atom[type_col]))
            atom1 = int(atom[atom1_col])
            atom2 = int(atom[atom2_col])
            bonds.append([bond_id, bond_type, atom1, atom2])
        
        # bonds only, others are None
        return (time, None, None, bonds, None, None)

# --------------------------------------------------------------------
# Example Usage (for testing purposes)
# Uncomment the following lines to test the bdump3.py module

if __name__ == "__main__":
    b = bdump("dump.one")
    b.map(1, "id", 3, "x", 4, "y", 5, "z")
    while True:
        time = b.next()
        if time == -1:
            break
        print(f"Snapshot Time: {time}")
        _, _, _, bonds, _, _ = b.viz(time, 1)
        print(f"Bonds: {bonds}")
