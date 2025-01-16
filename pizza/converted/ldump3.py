#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__all__ = ['Snap', 'ldump']
# ldump3.py

"""
ldump3.py

Module converted from Python 2.x to Python 3.x.

ldump tool

Read and process dump files with line segment information for visualization purposes.

## Usage

    l = ldump("dump.one")                  # Read one or more dump files
    l = ldump("dump.1 dump.2.gz")          # Can handle gzipped files
    l = ldump("dump.*")                     # Wildcard expands to multiple files
    l = ldump("dump.*", 0)                  # Two arguments: store filenames but don't read

    time = l.next()                         # Read next snapshot from dump files

    l.map(1, "id", 3, "x")                   # Assign names to atom columns

    time, box, atoms, bonds, tris, lines = l.viz(index)   # Return list of viz objects

      - `viz()` returns line info for the specified timestep index
      - Can also call as `viz(time, 1)` to find index of preceding snapshot
      - `atoms`, `bonds`, `tris`, `lines` contain respective information

    l.owrap(...)                            # Wrap lines to the same image as their atoms

      - `owrap()` is called by dump tool's `owrap()`
      - Useful for wrapping all molecule's atoms/lines the same so they are contiguous

## Notes

- Incomplete and duplicate snapshots are deleted.
- No column name assignment is performed unless explicitly mapped.
- `viz()` is tailored for visualization tools that require line segment information.

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
        natoms (int): Number of atoms (line segments) in the snapshot.
        xlo, xhi, ylo, yhi, zlo, zhi (float): Box bounds.
        atoms (numpy.ndarray or list): Array of atom (line segment) data.
    """
    def __init__(self):
        self.time = 0
        self.natoms = 0
        self.xlo = self.xhi = self.ylo = self.yhi = self.zlo = self.zhi = 0.0
        self.atoms = None

# --------------------------------------------------------------------
# ldump Class Definition

class ldump:
    """
    ldump class for reading and processing ChemCell dump files with line segment information.
    """
    
    # --------------------------------------------------------------------
    
    def __init__(self, *args):
        """
        Initialize the ldump object.
        
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
            raise Exception("No dump files specified for ldump.")
        
        words = args[0].split()
        self.flist = []
        for word in words:
            self.flist += glob.glob(word)
        
        if len(self.flist) == 0 and len(args) == 1:
            raise Exception("No ldump file specified.")
        
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
            raise Exception("Cannot read incrementally with current ldump configuration.")
    
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
            # Read number of atoms (line segments)
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
                # Read atom (line segment) data
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
            raise Exception("ldump map() requires pairs of mappings.")
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
    # Return list of lines to viz for snapshot isnap
    # If called with flag, then index is timestep, so convert to snapshot index
    
    def viz(self, index, flag=0):
        """
        Return line segment information for visualization.
        
        Parameters:
            index (int): Snapshot index or time stamp.
            flag (int): If 1, interpret index as time stamp.
        
        Returns:
            tuple: (time, box, atoms, bonds, tris, lines)
                   atoms, bonds, tris are None.
                   lines contain [id, type, x1, y1, z1, x2, y2, z2] for each line.
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
        
        # Retrieve column indices
        try:
            id_col = self.names["id"]
            type_col = self.names["type"]
            end1x_col = self.names["end1x"]
            end1y_col = self.names["end1y"]
            end2x_col = self.names["end2x"]
            end2y_col = self.names["end2y"]
        except KeyError as e:
            print(f"Column name {e} not mapped. Use l.map() to assign column names.")
            return (time, box, None, None, None, None)
        
        # Create line list
        lines = []
        for i in range(snap.natoms):
            atom = snap.atoms[i]
            try:
                bond_id = int(atom[id_col])
                bond_type = int(atom[type_col])
                end1x = float(atom[end1x_col])
                end1y = float(atom[end1y_col])
                end2x = float(atom[end2x_col])
                end2y = float(atom[end2y_col])
            except (IndexError, ValueError) as e:
                print(f"Error processing atom data: {e}")
                continue
            # Assuming z1 and z2 are zero since original code sets them to 0.0
            if end1x == 0.0 and end1y == 0.0 and end2x == 0.0 and end2y == 0.0:
                continue  # Skip lines with all zeros
            lines.append([bond_id, bond_type, end1x, end1y, 0.0, end2x, end2y, 0.0])
    
        return (time, box, None, None, None, lines)
    
    # --------------------------------------------------------------------
    # Wrap line end points associated with atoms through periodic boundaries
    # Invoked by dump() when it does an owrap() on its atoms
    
    def owrap(self, time, xprd, yprd, zprd, idsdump, atomsdump, iother, ix, iy, iz):
        """
        Wrap line end points associated with atoms through periodic boundaries.
        
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
            end1x_col = self.names["end1x"]
            end1y_col = self.names["end1y"]
            end2x_col = self.names["end2x"]
            end2y_col = self.names["end2y"]
        except KeyError as e:
            print(f"Column name {e} not mapped. Use l.map() to assign column names.")
            return
    
        try:
            isnap = self.findtime(time)
        except Exception as e:
            print(e)
            return
        snap = self.snaps[isnap]
        atoms = snap.atoms
    
        # idump = index of my line I in dump's atoms
        # jdump = atom J in dump's atoms that atom I was owrapped on
        # delx, dely = offset applied to atom I and thus to line I
    
        for i in range(snap.natoms):
            try:
                tag = int(atoms[i][id_col])
                idump = idsdump[tag]
                jdump = idsdump[int(atomsdump[idump][iother])]
                delx = (atomsdump[idump][ix] - atomsdump[jdump][ix]) * xprd
                dely = (atomsdump[idump][iy] - atomsdump[jdump][iy]) * yprd
                delz = (atomsdump[idump][iz] - atomsdump[jdump][iz]) * zprd
                atoms[i][end1x_col] += delx
                atoms[i][end1y_col] += dely
                atoms[i][end2x_col] += delx
                atoms[i][end2y_col] += dely
                # Assuming z-coordinates need to be handled if present
                # If not, the z-component remains unchanged
            except (KeyError, IndexError, ValueError) as e:
                print(f"Error in owrap: {e}")
                continue
    
# --------------------------------------------------------------------
# Example Usage (for testing purposes)
# Uncomment the following lines to test the ldump3.py module

if __name__ == "__main__":
    l = ldump("dump.one")
    l.map(1, "id", 3, "x", 4, "y", 5, "z", 6, "end1x", 7, "end1y", 8, "end2x", 9, "end2y")
    while True:
        time = l.next()
        if time == -1:
            break
        print(f"Snapshot Time: {time}")
        _, box, _, _, _, lines = l.viz(time, 1)
        print(f"Lines: {lines}")
