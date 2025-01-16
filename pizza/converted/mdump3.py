#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__all__ = ['Snap', 'eselect', 'mdump', 'normal', 'tselect']
# mdump3.py

"""
mdump3.py

Module converted from Python 2.x to Python 3.x.

mdump tool

Read, write, and manipulate mesh dump files for visualization purposes.

## Usage

    m = mdump("mesh.one")                          # Read one or more mesh dump files
    m = mdump("mesh.1 mesh.2.gz")                  # Can handle gzipped files
    m = mdump("mesh.*")                             # Wildcard expands to multiple files
    m = mdump("mesh.*", 0)                          # Two arguments: store filenames but don't read

    time = m.next()                                 # Read next snapshot from dump files

    m.map(2, "temperature")                         # Assign names to element value columns

    m.tselect.all()                                 # Select all timesteps
    m.tselect.one(N)                                # Select only timestep N
    m.tselect.none()                                # Deselect all timesteps
    m.tselect.skip(M)                               # Select every Mth step
    m.tselect.test("$t >= 100 and $t < 10000")      # Select matching timesteps
    m.delete()                                      # Delete non-selected timesteps

    m.eselect.all()                                 # Select all elements in all steps
    m.eselect.all(N)                                # Select all elements in one step
    m.eselect.test("$id > 100 and $type == 2")      # Select matching elements in all steps
    m.eselect.test("$id > 100 and $type == 2", N)  # Select matching elements in one step

    t = m.time()                                     # Return vector of selected timestep values
    fx, fy, ... = m.vecs(1000, "fx", "fy", ...)     # Return vector(s) for timestep N

    index, time, flag = m.iterator(0/1)             # Loop over mesh dump snapshots
    time, box, atoms, bonds, tris, lines = m.viz(index)  # Return list of viz objects
    nodes, elements, nvalues, evalues = m.mviz(index)    # Return list of mesh viz objects
    m.etype = "color"                               # Set column returned as "type" by viz

    m.owrap(...)                                    # Wrap lines to the same image as their atoms

      - `owrap()` is called by dump tool's `owrap()`
      - Useful for wrapping all molecule's atoms/lines the same so they are contiguous

## Notes

- Incomplete and duplicate snapshots are deleted.
- No column name assignment or unscaling is performed unless explicitly mapped.
- `viz()` and `mviz()` are tailored for visualization tools that require mesh and element information.
- `owrap()` ensures periodic boundary conditions are maintained for line segments.

## History

- 11/06, Steve Plimpton (SNL): original version
- 12/09, David Hart (SNL): allow use of NumPy or Numeric
- 2025-01-17, INRAE\Olivier Vitrac conversion 

## Dependencies

- Python 3.x
- `numpy` library (fallback to `Numeric` if `numpy` is not available)
"""

# History
#   11/06, Steve Plimpton (SNL): original version
#   12/09, David Hart (SNL): allow use of NumPy or Numeric
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
    Represents a single snapshot from a mesh dump file.
    
    Attributes:
        time (int): Time stamp of the snapshot.
        tselect (int): 0 or 1 indicating if this snapshot is selected.
        nselect (int): Number of selected elements in this snapshot.
        nflag (int): 0 or 1 indicating if this snapshot has nodal coordinates.
        eflag (int): 0 or 1-4 indicating the type of elements (tri, tet, square, cube).
        nvalueflag (int): 0 or 1 indicating if this snapshot has nodal values.
        evalueflag (int): 0 or 1 indicating if this snapshot has element values.
        xlo, xhi, ylo, yhi, zlo, zhi (float): Box bounds.
        nodes (numpy.ndarray): Array of node data.
        elements (numpy.ndarray): Array of element data.
        nvalues (numpy.ndarray): Array of node values.
        evalues (numpy.ndarray): Array of element values.
        eselect (numpy.ndarray): Array indicating selected elements.
    """
    def __init__(self):
        self.time = 0
        self.tselect = 0
        self.nselect = 0
        self.nflag = 0
        self.eflag = 0
        self.nvalueflag = 0
        self.evalueflag = 0
        self.xlo = self.xhi = self.ylo = self.yhi = self.zlo = self.zhi = 0.0
        self.nodes = None
        self.elements = None
        self.nvalues = None
        self.evalues = None
        self.eselect = None

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
# Time selection class

class tselect:
    """
    Time selection class for selecting timesteps in mdump.
    """
    
    def __init__(self, data):
        self.data = data
    
    # --------------------------------------------------------------------
    
    def all(self):
        """
        Select all timesteps.
        """
        data = self.data
        for snap in data.snaps:
            snap.tselect = 1
        data.nselect = len(data.snaps)
        data.eselect.all()
        print(f"{data.nselect} snapshots selected out of {data.nsnaps}")
    
    # --------------------------------------------------------------------
    
    def one(self, n):
        """
        Select only timestep N.
        
        Parameters:
            n (int): Timestep to select.
        """
        data = self.data
        for snap in data.snaps:
            snap.tselect = 0
        try:
            i = data.findtime(n)
            data.snaps[i].tselect = 1
            data.nselect = 1
            data.eselect.all()
            print(f"{data.nselect} snapshots selected out of {data.nsnaps}")
        except Exception as e:
            print(e)
    
    # --------------------------------------------------------------------
    
    def none(self):
        """
        Deselect all timesteps.
        """
        data = self.data
        for snap in data.snaps:
            snap.tselect = 0
        data.nselect = 0
        print(f"{data.nselect} snapshots selected out of {data.nsnaps}")
    
    # --------------------------------------------------------------------
    
    def skip(self, M):
        """
        Select every Mth step.
        
        Parameters:
            M (int): Interval for selecting timesteps.
        """
        data = self.data
        count = M - 1
        for snap in data.snaps:
            if not snap.tselect:
                continue
            count += 1
            if count == M:
                count = 0
                continue
            snap.tselect = 0
            data.nselect -= 1
        data.eselect.all()
        print(f"{data.nselect} snapshots selected out of {data.nsnaps}")
    
    # --------------------------------------------------------------------
    
    def test(self, teststr):
        """
        Select timesteps based on a Python Boolean expression.
        
        Parameters:
            teststr (str): Boolean expression using $t for timestep value.
                           Example: "$t >= 100 and $t < 10000"
        """
        data = self.data
        snaps = data.snaps
        # Replace $t with snaps[i].time and compile the command
        teststr_replaced = teststr.replace("$t", "snap.time")
        cmd = f"flag = {teststr_replaced}"
        try:
            ccmd = compile(cmd, '', 'single')
        except Exception as e:
            print(f"Error compiling test string: {e}")
            return
        for snap in snaps:
            if not snap.tselect:
                continue
            try:
                exec(ccmd, {"snap": snap})
                if not flag:
                    snap.tselect = 0
                    data.nselect -= 1
            except Exception as e:
                print(f"Error executing test string on timestep {snap.time}: {e}")
        data.eselect.all()
        print(f"{data.nselect} snapshots selected out of {data.nsnaps}")

# --------------------------------------------------------------------
# Element selection class

class eselect:
    """
    Element selection class for selecting elements within timesteps in mdump.
    """
    
    def __init__(self, data):
        self.data = data
    
    # --------------------------------------------------------------------
    
    def all(self, *args):
        """
        Select all elements in all steps or in one specified step.
        
        Parameters:
            *args: If provided, selects all elements in the specified timestep.
                   Example: all(N) selects all elements in timestep N.
        """
        data = self.data
        if len(args) == 0:
            # Select all elements in all selected timesteps
            for snap in data.snaps:
                if not snap.tselect:
                    continue
                if snap.eflag:
                    snap.eselect[:] = 1
                    snap.nselect = snap.nelements
        else:
            # Select all elements in one specified timestep
            try:
                n = args[0]
                i = data.findtime(n)
                snap = data.snaps[i]
                if snap.eflag:
                    snap.eselect[:] = 1
                    snap.nselect = snap.nelements
            except Exception as e:
                print(e)
        print(f"Elements selected. Total selected elements: {data.eselect.count_selected()}")
    
    # --------------------------------------------------------------------
    
    def test(self, teststr, *args):
        """
        Select elements based on a Python Boolean expression.
        
        Parameters:
            teststr (str): Boolean expression using $ for element attributes.
                           Example: "$id > 100 and $type == 2"
            *args: If provided, applies the test to elements in the specified timestep.
        """
        data = self.data
        snaps = data.snaps
        # Replace $var with snap.elements[i][var_index]
        pattern = r"\$\w+"
        matches = re.findall(pattern, teststr)
        for match in matches:
            name = match[1:]
            if name not in data.names:
                print(f"Unknown column name: {name}")
                return
            column = data.names[name]
            teststr = teststr.replace(match, f"snap.elements[i][{column}]")
        cmd = f"flag = {teststr}"
        try:
            ccmd = compile(cmd, '', 'single')
        except Exception as e:
            print(f"Error compiling test string: {e}")
            return
        
        if len(args) == 0:
            # Apply test to all selected timesteps
            for snap in snaps:
                if not snap.tselect:
                    continue
                for i in range(snap.nelements):
                    if not snap.eselect[i]:
                        continue
                    try:
                        exec(ccmd, {"snap": snap, "i": i})
                        if not flag:
                            snap.eselect[i] = 0
                            snap.nselect -= 1
                    except Exception as e:
                        print(f"Error executing test string on element {i} in timestep {snap.time}: {e}")
            print(f"Elements selected. Total selected elements: {data.eselect.count_selected()}")
        else:
            # Apply test to a specific timestep
            try:
                n = args[0]
                i = data.findtime(n)
                snap = snaps[i]
                if not snap.tselect:
                    print(f"Timestep {n} is not selected.")
                    return
                for j in range(snap.nelements):
                    if not snap.eselect[j]:
                        continue
                    try:
                        exec(ccmd, {"snap": snap, "i": j})
                        if not flag:
                            snap.eselect[j] = 0
                            snap.nselect -= 1
                    except Exception as e:
                        print(f"Error executing test string on element {j} in timestep {snap.time}: {e}")
                print(f"Elements selected. Total selected elements in timestep {n}: {snap.nselect}")
            except Exception as e:
                print(e)

# --------------------------------------------------------------------
# ldump Class Definition

class mdump:
    """
    mdump class for reading, writing, and manipulating mesh dump files.
    """
    
    # --------------------------------------------------------------------
    
    def __init__(self, *args):
        """
        Initialize the mdump object.
        
        Parameters:
            *args: Variable length argument list.
                   - If one argument, it's the list of files to read.
                   - If two arguments, the second argument indicates incremental reading.
        """
        self.snaps = []
        self.nsnaps = 0
        self.nselect = 0
        self.names = {}
        self.tselect = tselect(self)
        self.eselect = eselect(self)
        self.etype = ""
        
        # flist = list of all dump file names
        if len(args) == 0:
            raise Exception("No dump files specified for mdump.")
        
        words = args[0].split()
        self.flist = []
        for word in words:
            self.flist += glob.glob(word)
        
        if len(self.flist) == 0 and len(args) == 1:
            raise Exception("No dump file specified.")
        
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
    
        # Sort all node, element, nvalue, evalue arrays by ID
        for snap in self.snaps:
            if snap.nflag and snap.nodes is not None:
                array = snap.nodes
                ids = array[:, 0]
                ordering = np.argsort(ids)
                for i in range(array.shape[1]):
                    array[:, i] = np.take(array[:, i], ordering)
            if snap.eflag and snap.elements is not None:
                array = snap.elements
                ids = array[:, 0]
                ordering = np.argsort(ids)
                for i in range(array.shape[1]):
                    array[:, i] = np.take(array[:, i], ordering)
            if snap.nvalueflag and snap.nvalues is not None:
                array = snap.nvalues
                ids = array[:, 0]
                ordering = np.argsort(ids)
                for i in range(array.shape[1]):
                    array[:, i] = np.take(array[:, i], ordering)
            if snap.evalueflag and snap.evalues is not None:
                array = snap.evalues
                ids = array[:, 0]
                ordering = np.argsort(ids)
                for i in range(array.shape[1]):
                    array[:, i] = np.take(array[:, i], ordering)
    
        # Reference definitions of nodes and elements in previous timesteps
        self.reference()
        
        self.nsnaps = len(self.snaps)
        print(f"read {self.nsnaps} snapshots")
    
        # Select all timesteps and elements
        self.tselect.all()
    
    # --------------------------------------------------------------------
    # Read the next snapshot from the list of files (incremental reading)
    
    def next(self):
        """
        Read the next snapshot in incremental mode.
        
        Returns:
            int: Time stamp of the snapshot read, or -1 if no snapshots left.
        """
        if not self.increment:
            raise Exception("Cannot read incrementally with current mdump configuration.")
    
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
            snap.tselect = 1
            snap.nselect = snap.nelements
            if snap.eflag:
                snap.eselect = np.ones(snap.nelements, dtype=int)
            self.nsnaps += 1
            self.nselect += 1
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
            snap.time = int(line.strip())
            # Read snapshot type
            line = f.readline()
            if not line:
                return None
            if "NUMBER OF NODES" in line:
                snap.nflag = 1
            elif "NUMBER OF TRIANGLES" in line:
                snap.eflag = 1
            elif "NUMBER OF TETS" in line:
                snap.eflag = 2
            elif "NUMBER OF SQUARES" in line:
                snap.eflag = 3
            elif "NUMBER OF CUBES" in line:
                snap.eflag = 4
            elif "NUMBER OF NODE VALUES" in line:
                snap.nvalueflag = 1
            elif "NUMBER OF ELEMENT VALUES" in line:
                snap.evalueflag = 1
            else:
                raise Exception("Unrecognized snapshot type in dump file.")
            # Read number of nodes/elements/values
            line = f.readline()
            if not line:
                return None
            n = int(line.strip())
    
            if snap.eflag:
                snap.eselect = np.zeros(n, dtype=int)
    
            if snap.nflag:
                # Read box bounds
                f.readline()  # Read past header
                words = f.readline().split()
                snap.xlo, snap.xhi = float(words[0]), float(words[1])
                words = f.readline().split()
                snap.ylo, snap.yhi = float(words[0]), float(words[1])
                words = f.readline().split()
                snap.zlo, snap.zhi = float(words[0]), float(words[1])
                
            f.readline()  # Read past another header
    
            if n:
                # Read node/element/value data
                words = f.readline().split()
                ncol = len(words)
                data = []
                data.append([float(value) for value in words])
                for _ in range(1, n):
                    words = f.readline().split()
                    if not words:
                        break
                    data.append([float(value) for value in words])
                values = np.array(data, dtype=float)
            else:
                values = None
    
            if snap.nflag:
                snap.nodes = values
                snap.nnodes = n
            elif snap.eflag:
                snap.elements = values
                snap.nelements = n
                snap.eselect = np.zeros(n, dtype=int)  # Initialize element selection
            elif snap.nvalueflag:
                snap.nvalues = values
                snap.nnvalues = n
            elif snap.evalueflag:
                snap.evalues = values
                snap.nevalues = n
            return snap
        except Exception as e:
            print(f"Error reading snapshot: {e}")
            return None
    
    # --------------------------------------------------------------------
    # Map atom column names
    
    def map(self, *pairs):
        """
        Assign names to element value columns.
        
        Parameters:
            *pairs: Pairs of (column_number, "column_name")
                   Example: map(2, "temperature")
        """
        if len(pairs) % 2 != 0:
            raise Exception("mdump map() requires pairs of mappings.")
        for i in range(0, len(pairs), 2):
            col_num = pairs[i]
            col_name = pairs[i + 1]
            self.names[col_name] = col_num - 1  # Zero-based indexing
    
    # --------------------------------------------------------------------
    # Delete unselected snapshots
    
    def delete(self):
        """
        Delete non-selected snapshots.
        """
        ndel = 0
        selected_snaps = []
        for snap in self.snaps:
            if snap.tselect:
                selected_snaps.append(snap)
            else:
                ndel += 1
        self.snaps = selected_snaps
        self.nsnaps = len(self.snaps)
        self.nselect = sum(snap.tselect for snap in self.snaps)
        print(f"{ndel} snapshots deleted")
        print(f"{self.nsnaps} snapshots remaining")
    
    # --------------------------------------------------------------------
    # Sort snapshots by time stamp
    
    def sort(self, *args):
        """
        Sort snapshots by ID in all selected timesteps or one specified timestep.
        
        Parameters:
            *args: If provided, sorts elements in the specified timestep.
        """
        if len(args) == 0:
            print("Sorting selected snapshots ...")
            if "id" not in self.names:
                print("Column 'id' not mapped. Use m.map() to assign column names.")
                return
            id_col = self.names["id"]
            for snap in self.snaps:
                if snap.tselect:
                    self.sort_one(snap, id_col)
        else:
            try:
                n = args[0]
                i = self.findtime(n)
                if "id" not in self.names:
                    print("Column 'id' not mapped. Use m.map() to assign column names.")
                    return
                id_col = self.names["id"]
                self.sort_one(self.snaps[i], id_col)
            except Exception as e:
                print(e)
    
    # --------------------------------------------------------------------
    # Sort a single snapshot by ID column
    
    def sort_one(self, snap, id_col):
        """
        Sort elements in a single snapshot by ID column.
        
        Parameters:
            snap (Snap): The snapshot to sort.
            id_col (int): The column index for 'id'.
        """
        if snap.elements is not None:
            array = snap.elements
            ids = array[:, id_col]
            ordering = np.argsort(ids)
            for i in range(array.shape[1]):
                array[:, i] = np.take(array[:, i], ordering)
    
    # --------------------------------------------------------------------
    # Return list of selected snapshot time stamps
    
    def time(self):
        """
        Get a list of all selected snapshot time stamps.
        
        Returns:
            list: List of time stamps.
        """
        return [snap.time for snap in self.snaps if snap.tselect]
    
    # --------------------------------------------------------------------
    # Extract vector(s) of values for selected elements at chosen timestep
    
    def vecs(self, n, *columns):
        """
        Extract vector(s) of values for selected elements at a specific timestep.
        
        Parameters:
            n (int): Timestep to extract vectors from.
            *columns (str): Column names to extract.
        
        Returns:
            list: List of vectors corresponding to the specified columns.
        """
        try:
            snap = self.snaps[self.findtime(n)]
        except Exception as e:
            print(e)
            return []
        if not snap.evalueflag:
            raise Exception("Snapshot has no element values.")
        
        if len(columns) == 0:
            raise Exception("No columns specified.")
        
        column_indices = []
        for name in columns:
            if name not in self.names:
                print(f"Unknown column name: {name}")
                return []
            column_indices.append(self.names[name])
        
        values = []
        for col in column_indices:
            vec = []
            for i in range(snap.nelements):
                if snap.eselect[i]:
                    vec.append(snap.evalues[i][col])
            values.append(vec)
        
        if len(values) == 1:
            return values[0]
        else:
            return values
    
    # --------------------------------------------------------------------
    # Sort snapshots on time stamp
    # (Replaced by sort method using key=lambda x: x.time)
    
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
    # Delete successive snapshots with duplicate time stamp
    # If have same timestamp, combine them if internal flags are different
    
    def cull(self):
        """
        Remove duplicate snapshots based on time stamps and merge their data.
        """
        i = 1
        while i < len(self.snaps):
            if self.snaps[i].time == self.snaps[i-1].time:
                if self.snaps[i].nflag and not self.snaps[i-1].nflag:
                    self.snaps[i-1].nflag = 1
                    self.snaps[i-1].nnodes = self.snaps[i].nnodes
                    self.snaps[i-1].nodes = self.snaps[i].nodes
                    self.snaps[i-1].xlo = self.snaps[i].xlo
                    self.snaps[i-1].xhi = self.snaps[i].xhi
                    self.snaps[i-1].ylo = self.snaps[i].ylo
                    self.snaps[i-1].yhi = self.snaps[i].yhi
                    self.snaps[i-1].zlo = self.snaps[i].zlo
                    self.snaps[i-1].zhi = self.snaps[i].zhi
                elif self.snaps[i].eflag and not self.snaps[i-1].eflag:
                    self.snaps[i-1].eflag = self.snaps[i].eflag
                    self.snaps[i-1].nelements = self.snaps[i].nelements
                    self.snaps[i-1].elements = self.snaps[i].elements
                    self.snaps[i-1].eselect = self.snaps[i].eselect
                elif self.snaps[i].nvalueflag and not self.snaps[i-1].nvalueflag:
                    self.snaps[i-1].nvalueflag = 1
                    self.snaps[i-1].nnvalues = self.snaps[i].nnvalues
                    self.snaps[i-1].nvalues = self.snaps[i].nvalues
                elif self.snaps[i].evalueflag and not self.snaps[i-1].evalueflag:
                    self.snaps[i-1].evalueflag = 1
                    self.snaps[i-1].nevalues = self.snaps[i].nevalues
                    self.snaps[i-1].evalues = self.snaps[i].evalues
                del self.snaps[i]
            else:
                i += 1
    
    # --------------------------------------------------------------------
    # Ensure every snapshot has node and element connectivity info
    # If not, point it at the most recent snapshot that does
    
    def reference(self):
        """
        Ensure every snapshot has node and element connectivity information by referencing previous snapshots.
        """
        for i in range(len(self.snaps)):
            if not self.snaps[i].nflag:
                for j in range(i, -1, -1):
                    if self.snaps[j].nflag:
                        self.snaps[i].nflag = self.snaps[j].nflag
                        self.snaps[i].nnodes = self.snaps[j].nnodes
                        self.snaps[i].nodes = self.snaps[j].nodes
                        self.snaps[i].xlo = self.snaps[j].xlo
                        self.snaps[i].xhi = self.snaps[j].xhi
                        self.snaps[i].ylo = self.snaps[j].ylo
                        self.snaps[i].yhi = self.snaps[j].yhi
                        self.snaps[i].zlo = self.snaps[j].zlo
                        self.snaps[i].zhi = self.snaps[j].zhi
                        break
            if not self.snaps[i].nflag:
                raise Exception("No nodal coordinates found in previous snapshots.")
            if not self.snaps[i].eflag:
                for j in range(i, -1, -1):
                    if self.snaps[j].eflag:
                        self.snaps[i].eflag = self.snaps[j].eflag
                        self.snaps[i].nelements = self.snaps[j].nelements
                        self.snaps[i].elements = self.snaps[j].elements
                        self.snaps[i].eselect = self.snaps[j].eselect
                        break
            if not self.snaps[i].eflag:
                raise Exception("No element connections found in previous snapshots.")
    
    # --------------------------------------------------------------------
    # Iterate over selected snapshots
    
    def iterator(self, flag):
        """
        Iterator method compatible with equivalent dump calls.
        
        Parameters:
            flag (int): 0 for first call, 1 for subsequent calls.
        
        Returns:
            tuple: (index, time, flag)
                   index (int): Index within dump object (0 to # of snapshots)
                   time (int): Timestep value
                   flag (int): -1 when iteration is done, 1 otherwise
        """
        if flag == 0:
            self.iterate = -1  # Initialize iteration
        self.iterate += 1
        if self.iterate >= self.nsnaps:
            return (0, 0, -1)
        snap = self.snaps[self.iterate]
        if not snap.tselect:
            return self.iterator(1)
        return (self.iterate, snap.time, 1)
    
    # --------------------------------------------------------------------
    # Return list of viz objects for a snapshot
    
    def viz(self, index, flag=0):
        """
        Return mesh visualization information for a snapshot.
        
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
        if self.etype == "":
            type_col = -1
        else:
            if self.etype not in self.names:
                print(f"Unknown etype column: {self.etype}")
                type_col = -1
            else:
                type_col = self.names[self.etype]
    
        atoms = None
        bonds = None
    
        tris = []
        nodes = snap.nodes
        for i in range(snap.nelements):
            if not snap.eselect[i]:
                continue
            element = snap.elements[i]
            if snap.evalueflag:
                evalue = snap.evalues[i]
            else:
                evalue = None
    
            # Process based on element type
            if snap.eflag == 1:
                # Triangle
                try:
                    v1 = nodes[int(element[2]) - 1][2:5].tolist()
                    v2 = nodes[int(element[3]) - 1][2:5].tolist()
                    v3 = nodes[int(element[4]) - 1][2:5].tolist()
                except IndexError:
                    print(f"Error accessing nodes for element {i} in timestep {time}.")
                    continue
                list_vertices = v1 + v2 + v3
                n = normal(list_vertices[0:3], list_vertices[3:6], list_vertices[6:9])
                if type_col == -1:
                    tris.append([int(element[0]), int(element[1])] + list_vertices + n)
                else:
                    tris.append([int(element[0]), int(evalue[type_col])] + list_vertices + n)
    
            elif snap.eflag == 2:
                # Tetrahedron - convert to 4 triangles
                try:
                    v1 = nodes[int(element[2]) - 1][2:5].tolist()
                    v2 = nodes[int(element[3]) - 1][2:5].tolist()
                    v3 = nodes[int(element[4]) - 1][2:5].tolist()
                    v4 = nodes[int(element[5]) - 1][2:5].tolist()
                except IndexError:
                    print(f"Error accessing nodes for element {i} in timestep {time}.")
                    continue
                tris_data = [
                    v1 + v2 + v4,
                    v2 + v3 + v4,
                    v1 + v4 + v3,
                    v1 + v3 + v2
                ]
                for tri_vertices in tris_data:
                    n = normal(tri_vertices[0:3], tri_vertices[3:6], tri_vertices[6:9])
                    if type_col == -1:
                        tris.append([int(element[0]), int(element[1])] + tri_vertices + n)
                    else:
                        tris.append([int(element[0]), int(evalue[type_col])] + tri_vertices + n)
    
            elif snap.eflag == 3:
                # Square - convert to 2 triangles
                try:
                    v1 = nodes[int(element[2]) - 1][2:5].tolist()
                    v2 = nodes[int(element[3]) - 1][2:5].tolist()
                    v3 = nodes[int(element[4]) - 1][2:5].tolist()
                    v4 = nodes[int(element[5]) - 1][2:5].tolist()
                except IndexError:
                    print(f"Error accessing nodes for element {i} in timestep {time}.")
                    continue
                tris_data = [
                    v1 + v2 + v3,
                    v1 + v3 + v4
                ]
                for tri_vertices in tris_data:
                    n = normal(tri_vertices[0:3], tri_vertices[3:6], tri_vertices[6:9])
                    if type_col == -1:
                        tris.append([int(element[0]), int(element[1])] + tri_vertices + n)
                    else:
                        tris.append([int(element[0]), int(evalue[type_col])] + tri_vertices + n)
    
            elif snap.eflag == 4:
                # Cube - convert to 12 triangles
                try:
                    v1 = nodes[int(element[2]) - 1][2:5].tolist()
                    v2 = nodes[int(element[3]) - 1][2:5].tolist()
                    v3 = nodes[int(element[4]) - 1][2:5].tolist()
                    v4 = nodes[int(element[5]) - 1][2:5].tolist()
                    v5 = nodes[int(element[6]) - 1][2:5].tolist()
                    v6 = nodes[int(element[7]) - 1][2:5].tolist()
                    v7 = nodes[int(element[8]) - 1][2:5].tolist()
                    v8 = nodes[int(element[9]) - 1][2:5].tolist()
                except IndexError:
                    print(f"Error accessing nodes for element {i} in timestep {time}.")
                    continue
                tris_data = [
                    # Lower z face
                    v1 + v3 + v2,
                    v1 + v4 + v3,
                    # Upper z face
                    v5 + v6 + v7,
                    v5 + v7 + v8,
                    # Lower y face
                    v1 + v2 + v6,
                    v1 + v6 + v5,
                    # Upper y face
                    v4 + v7 + v3,
                    v4 + v8 + v7,
                    # Lower x face
                    v1 + v8 + v4,
                    v1 + v5 + v8,
                    # Upper x face
                    v2 + v3 + v7,
                    v2 + v7 + v6
                ]
                for tri_vertices in tris_data:
                    n = normal(tri_vertices[0:3], tri_vertices[3:6], tri_vertices[6:9])
                    if type_col == -1:
                        tris.append([int(element[0]), int(element[1])] + tri_vertices + n)
                    else:
                        tris.append([int(element[0]), int(evalue[type_col])] + tri_vertices + n)
        
        # Lines are not used in viz for mesh dumps
        lines = []
    
        return (time, box, atoms, bonds, tris, lines)
    
    # --------------------------------------------------------------------
    # Return lists of node/element info for snapshot isnap
    # If called with flag, then index is timestep, so convert to snapshot index
    
    def mviz(self, index, flag=0):
        """
        Return mesh visualization information for a snapshot, including nodes and elements.
        
        Parameters:
            index (int): Snapshot index or time stamp.
            flag (int): If 1, interpret index as time stamp.
        
        Returns:
            tuple: (time, box, nodes, elements, nvalues, evalues)
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
        nodes = []
        elements = []
        nvalues = []
        evalues = []
        
        if snap.nflag and snap.nodes is not None:
            for node in snap.nodes:
                nodes.append([int(node[0]), int(node[1]), node[2], node[3], node[4]])
        if snap.eflag and snap.elements is not None:
            for elem in snap.elements:
                elements.append([int(elem[0]), int(elem[1])] + elem[2:].tolist())
        if snap.nvalueflag and snap.nvalues is not None:
            for nval in snap.nvalues:
                nvalues.append([int(nval[0]), int(nval[1])] + nval[2:].tolist())
        if snap.evalueflag and snap.evalues is not None:
            for eval in snap.evalues:
                evalues.append([int(eval[0]), int(eval[1])] + eval[2:].tolist())
        
        return (time, box, nodes, elements, nvalues, evalues)
    
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
            print(f"Column name {e} not mapped. Use m.map() to assign column names.")
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
    
        for i in range(snap.nelements):
            try:
                tag = int(atoms[i][id_col])
                idump = idsdump[tag]
                jdump = idsdump[int(atomsdump[idump][iother])]
                delx = (atomsdump[idump][ix] - atomsdump[jdump][ix]) * xprd
                dely = (atomsdump[idump][iy] - atomsdump[jdump][iy]) * yprd
                delz = (atomsdump[idump][iz] - atomsdump[jdump][iz]) * zprd
                # Assuming z-coordinates need to be handled if present
                # If not, the z-component remains unchanged
                # Here, only x and y are being wrapped
                atoms[i][end1x_col] += delx
                atoms[i][end1y_col] += dely
                atoms[i][end2x_col] += delx
                atoms[i][end2y_col] += dely
            except (KeyError, IndexError, ValueError) as e:
                print(f"Error in owrap: {e}")
                continue

# --------------------------------------------------------------------
# Example Usage (for testing purposes)
# Uncomment the following lines to test the mdump3.py module

if __name__ == "__main__":
    m = mdump("mesh.one")
    m.map(2, "temperature")
    m.tselect.all()
    while True:
        time = m.next()
        if time == -1:
            break
        print(f"Snapshot Time: {time}")
        _, box, nodes, elements, nvalues, evalues = m.viz(time, 1)
        print(f"Nodes: {nodes}")
        print(f"Elements: {elements}")
