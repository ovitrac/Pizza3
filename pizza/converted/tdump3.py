#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__all__ = ['Snap', 'normal', 'tdump']
# tdump3.py

"""
tdump3.py

Module converted from Python 2.x to Python 3.x.

tdump tool

Read dump files with triangle information for visualization purposes.

## Usage

    t = tdump("dump.one")                             # Read one or more dump files
    t = tdump("dump.1 dump.2.gz")                     # Can handle gzipped files
    t = tdump("dump.*")                                # Wildcard expands to multiple files
    t = tdump("dump.*", 0)                             # Two arguments: store filenames but don't read

    time = t.next()                                    # Read next snapshot from dump files

    t.map(1, "id", 3, "x")                             # Assign names to atom columns

      - Must assign id, type, corner1x, corner1y, corner1z,
        corner2x, corner2y, corner2z, corner3x, corner3y, corner3z

    time, box, atoms, bonds, tris, lines = t.viz(index)  # Return list of viz objects

      - `viz()` returns triangle info for the specified timestep index
      - Can also call as `viz(time, 1)` to find index of preceding snapshot
      - `atoms`, `bonds`, `lines` are NULL
      - `tris` contain [id, type, x1, y1, z1, x2, y2, z2, x3, y3, z3, nx, ny, nz] for each triangle

    t.owrap(...)                                       # Wrap triangles to the same image as their atoms

      - `owrap()` is called by dump tool's `owrap()`
      - Useful for wrapping all molecule's atoms/triangles the same so they are contiguous

## Notes

- Incomplete and duplicate snapshots are deleted.
- No column name assignment is performed unless explicitly mapped.
- `viz()` is tailored for visualization tools that require triangle information.
- `owrap()` ensures periodic boundary conditions are maintained for triangles.

## History

- 4/11, Steve Plimpton (SNL): original version
- 2025-01-17, INRAE\Olivier Vitrac conversion

## Dependencies

- Python 3.x
- `numpy` library (fallback to `Numeric` if `numpy` is not available)
"""

# History
#   4/11, Steve Plimpton (SNL): original version
# 2025-01-17, first conversion in connection with the update of pizza.dump3

# Imports and external programs

import sys
import glob
import re
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
        natoms (int): Number of atoms (triangles) in the snapshot.
        xlo, xhi, ylo, yhi, zlo, zhi (float): Box bounds.
        atoms (numpy.ndarray or list): Array of atom (triangle) data.
    """
    def __init__(self):
        self.time = 0
        self.natoms = 0
        self.xlo = self.xhi = self.ylo = self.yhi = self.zlo = self.zhi = 0.0
        self.atoms = None

# --------------------------------------------------------------------
# Function to compute the normal vector for a triangle with 3 vertices

def normal(x, y, z):
    """
    Compute the normal vector for a triangle defined by vertices x, y, z.
    
    Parameters:
        x, y, z (list or tuple): Coordinates of the three vertices.
    
    Returns:
        list: Normal vector [nx, ny, nz].
    """
    v1 = [y[0] - x[0], y[1] - x[1], y[2] - x[2]]
    v2 = [z[0] - y[0], z[1] - y[1], z[2] - y[2]]
    
    n = [
        v1[1]*v2[2] - v1[2]*v2[1],
        v1[2]*v2[0] - v1[0]*v2[2],
        v1[0]*v2[1] - v1[1]*v2[0]
    ]
    
    length = sqrt(n[0]**2 + n[1]**2 + n[2]**2)
    if length == 0:
        return [0.0, 0.0, 0.0]
    n = [component / length for component in n]
    
    return n

# --------------------------------------------------------------------
# tdump Class Definition

class tdump:
    """
    tdump class for reading and processing dump files with triangle information.
    """
    
    # --------------------------------------------------------------------
    
    def __init__(self, *args):
        """
        Initialize the tdump object.
        
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
            raise Exception("No dump files specified for tdump.")
        
        words = args[0].split()
        self.flist = []
        for word in words:
            self.flist += glob.glob(word)
        
        if len(self.flist) == 0 and len(args) == 1:
            raise Exception("No tdump file specified.")
        
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
            raise Exception("Cannot read incrementally with current tdump configuration.")
    
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
            # Read and discard the first line (usually a comment or header)
            item = f.readline()
            if not item:
                return None
            # Read time stamp
            line = f.readline()
            if not line:
                return None
            snap.time = int(line.strip().split()[0])  # Read first field as time
            # Read number of atoms (triangles)
            line = f.readline()
            if not line:
                return None
            snap.natoms = int(line.strip())
    
            # Read box bounds
            line = f.readline()
            if not line:
                return None
            words = f.readline().split()
            if len(words) < 2:
                raise Exception("Incomplete box bounds data.")
            snap.xlo, snap.xhi = float(words[0]), float(words[1])
            words = f.readline().split()
            if len(words) < 2:
                raise Exception("Incomplete box bounds data.")
            snap.ylo, snap.yhi = float(words[0]), float(words[1])
            words = f.readline().split()
            if len(words) < 2:
                raise Exception("Incomplete box bounds data.")
            snap.zlo, snap.zhi = float(words[0]), float(words[1])
    
            # Read past another line (possibly a header)
            item = f.readline()
            if not item:
                return None
    
            if snap.natoms:
                # Read atom (triangle) data
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
                   Example: map(1, "id", 3, "x")
        """
        if len(pairs) % 2 != 0:
            raise Exception("tdump map() requires pairs of mappings.")
        for i in range(0, len(pairs), 2):
            col_num = pairs[i]
            col_name = pairs[i + 1]
            self.names[col_name] = col_num - 1  # Zero-based indexing
    
    # --------------------------------------------------------------------
    # Return list of snapshot time stamps
    
    def time(self):
        """
        Get a list of all snapshot time stamps.
        
        Returns:
            list: List of time stamps.
        """
        return [snap.time for snap in self.snaps]
    
    # --------------------------------------------------------------------
    # Sort snapshots on time stamp
    
    def compare_time(self, a, b):
        """
        Comparator for sorting snapshots by time.
        
        Parameters:
            a (Snap): First snapshot.
            b (Snap): Second snapshot.
        
        Returns:
            int: -1 if a < b, 1 if a > b, 0 if equal.
        """
        if a.time < b.time:
            return -1
        elif a.time > b.time:
            return 1
        else:
            return 0
    
    # --------------------------------------------------------------------
    # Find the index of a given timestep
    
    def findtime(self, n):
        """
        Find the index of a given timestep.
        
        Parameters:
            n (int): The timestep to find.
        
        Returns:
            int: The index of the timestep.
        
        Raises:
            Exception: If the timestep does not exist.
        """
        for i in range(self.nsnaps):
            if self.snaps[i].time == n:
                return i
        raise Exception(f"No step {n} exists.")
    
    # --------------------------------------------------------------------
    # Delete successive snapshots with duplicate time stamp
    
    def cull(self):
        """
        Remove duplicate snapshots based on time stamps.
        """
        i = 1
        while i < len(self.snaps):
            if self.snaps[i].time == self.snaps[i - 1].time:
                del self.snaps[i]
            else:
                i += 1
    
    # --------------------------------------------------------------------
    # Return list of triangles to viz for snapshot isnap
    # If called with flag, then index is timestep, so convert to snapshot index
    
    def viz(self, index, flag=0):
        """
        Return triangle information for visualization.
        
        Parameters:
            index (int): Snapshot index or time stamp.
            flag (int): If 1, interpret index as time stamp.
        
        Returns:
            tuple: (time, box, atoms, bonds, tris, lines)
                   atoms, bonds, lines are None.
                   tris contain [id, type, x1, y1, z1, x2, y2, z2, x3, y3, z3, nx, ny, nz] for each triangle.
        """
        if not flag:
            isnap = index
        else:
            times = self.time()
            n = len(times)
            i = 0
            while i < n:
                if times[i] > index:
                    break
                i += 1
            isnap = i - 1
        if isnap < 0 or isnap >= self.nsnaps:
            return (-1, None, None, None, None, None)
        snap = self.snaps[isnap]
    
        time = snap.time
        box = [snap.xlo, snap.ylo, snap.zlo, snap.xhi, snap.yhi, snap.zhi]
        try:
            id_col = self.names["id"]
            type_col = self.names["type"]
            corner1x_col = self.names["corner1x"]
            corner1y_col = self.names["corner1y"]
            corner1z_col = self.names["corner1z"]
            corner2x_col = self.names["corner2x"]
            corner2y_col = self.names["corner2y"]
            corner2z_col = self.names["corner2z"]
            corner3x_col = self.names["corner3x"]
            corner3y_col = self.names["corner3y"]
            corner3z_col = self.names["corner3z"]
        except KeyError as e:
            print(f"Column name {e} not mapped. Use t.map() to assign column names.")
            return (time, box, None, None, None, None)
    
        tris = []
        for i in range(snap.natoms):
            atom = snap.atoms[i]
            try:
                c1 = [atom[corner1x_col], atom[corner1y_col], atom[corner1z_col]]
                c2 = [atom[corner2x_col], atom[corner2y_col], atom[corner2z_col]]
                c3 = [atom[corner3x_col], atom[corner3y_col], atom[corner3z_col]]
            except IndexError:
                print(f"Error accessing corners for triangle {i} in timestep {time}.")
                continue
            n = normal(c1, c2, c3)
            # Skip triangle if all corners are zero
            if (c1[0] == 0.0 and c1[1] == 0.0 and c1[2] == 0.0 and
                c2[0] == 0.0 and c2[1] == 0.0 and c2[2] == 0.0):
                continue
            tris.append([int(atom[id_col]), int(atom[type_col])] + c1 + c2 + c3 + n)
    
        atoms = None
        bonds = None
        lines = None
    
        return (time, box, atoms, bonds, tris, lines)
    
    # --------------------------------------------------------------------
    # Wrap triangle corner points associated with atoms through periodic boundaries
    # Invoked by dump() when it does an owrap() on its atoms
    
    def owrap(self, time, xprd, yprd, zprd, idsdump, atomsdump, iother, ix, iy, iz):
        """
        Wrap triangle corner points associated with atoms through periodic boundaries.
        
        Parameters:
            time (int): Time stamp of the snapshot.
            xprd, yprd, zprd (float): Periodicity in x, y, z directions.
            idsdump (dict): Dictionary mapping atom IDs to dump indices.
            atomsdump (list): List of atoms from the dump.
            iother (int): Other index for wrapping.
            ix, iy, iz (int): Column indices for x, y, z coordinates.
        """
        try:
            id_col = self.names["id"]
            corner1x_col = self.names["corner1x"]
            corner1y_col = self.names["corner1y"]
            corner1z_col = self.names["corner1z"]
            corner2x_col = self.names["corner2x"]
            corner2y_col = self.names["corner2y"]
            corner2z_col = self.names["corner2z"]
            corner3x_col = self.names["corner3x"]
            corner3y_col = self.names["corner3y"]
            corner3z_col = self.names["corner3z"]
        except KeyError as e:
            print(f"Column name {e} not mapped. Use t.map() to assign column names.")
            return
    
        try:
            isnap = self.findtime(time)
        except Exception as e:
            print(e)
            return
        snap = self.snaps[isnap]
        atoms = snap.atoms
    
        # idump = index of my triangle I in dump's atoms
        # jdump = atom J in dump's atoms that triangle I was owrapped on
        # delx, dely, delz = offset applied to triangle I
        
        for i in range(snap.natoms):
            try:
                tag = int(atoms[i][id_col])
                idump = idsdump[tag]
                jdump = idsdump[int(atomsdump[idump][iother])]
                delx = (atomsdump[idump][ix] - atomsdump[jdump][ix]) * xprd
                dely = (atomsdump[idump][iy] - atomsdump[jdump][iy]) * yprd
                delz = (atomsdump[idump][iz] - atomsdump[jdump][iz]) * zprd
                # Apply offsets to all corners
                atoms[i][corner1x_col] += delx
                atoms[i][corner1y_col] += dely
                atoms[i][corner1z_col] += delz
                atoms[i][corner2x_col] += delx
                atoms[i][corner2y_col] += dely
                atoms[i][corner2z_col] += delz
                atoms[i][corner3x_col] += delx
                atoms[i][corner3y_col] += dely
                atoms[i][corner3z_col] += delz
            except (KeyError, IndexError, ValueError) as e:
                print(f"Error in owrap: {e}")
                continue

# --------------------------------------------------------------------
# Example Usage (for testing purposes)
# Uncomment the following lines to test the tdump3.py module

if __name__ == "__main__":
    t = tdump("dump.one")
    t.map(1, "id", 3, "x", 4, "y", 5, "z",
          6, "corner1x", 7, "corner1y", 8, "corner1z",
          9, "corner2x", 10, "corner2y", 11, "corner2z",
          12, "corner3x", 13, "corner3y", 14, "corner3z")
    while True:
        time = t.next()
        if time == -1:
            break
        print(f"Snapshot Time: {time}")
        _, box, atoms, bonds, tris, lines = t.viz(time, 1)
        print(f"Triangles: {tris}")
