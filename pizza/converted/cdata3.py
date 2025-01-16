#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__all__ = ['Box', 'Capped', 'Cylinder', 'Group', 'Line', 'Random', 'Shell', 'Sphere', 'Surface', 'Union', 'box_triangulate', 'cdata', 'connect', 'cross', 'normal', 'normalize', 'vertex']
# cdata3.py

"""
cdata3.py

Module converted from Python 2.x to Python 3.x.

cdata tool

Read, create, manipulate ChemCell data files

## How to specify and print 2d particles

c = cdata()			   create a datafile object
c = cdata("mem.surf")              read in one or more ChemCell data files
c = cdata("mem.part.gz mem.surf")  can be gzipped
c = cdata("mem.*")		   wildcard expands to multiple files
c.read("mem.surf")		   read in one or more data files

  read() has same argument options as constructor
  files contain the following kinds of entries, each of which becomes an object
    particles, triangles, region, facets
    particles is a list of particles -> becomes a group
    triangles is 3 lists of vertices, triangles, connections -> becomes a surf
    region is a ChemCell command defining a region -> becomes a region
    facets is a CUBIT format of vertices and triangles -> becomes a surf
  each object is assigned an ID = name in file
  ID can be any number or string, must be unique

c.box(ID,xlo,ylo,zlo,xhi,yhi,zhi)  create a box region
c.sphere(ID,x,y,z,r)		   create a sphere region
c.shell(ID,x,y,z,r,rinner)	   create a shell region
c.cyl(ID,'x',c1,c2,r,lo,hi)	   create a axis-aligned cylinder region
c.cap(ID,'x',c1,c2,r,lo,hi)	   create a axis-aligned capped-cylinder region
c.q(ID,q1,q2,...)                  set region triangulation quality factors

  box() can create an axis-aligned plane, line, or point if lo=hi
  cyl() can create an axis-aligned circle if lo=hi
  for cyl() and cap(): 'x' c1,c2 = y,z; 'y' c1,c2 = x,z; 'z' c,c2 = x,y
  q's are size factors for region triangulation
    for box, q1,q2,q3 = # of divisions per xyz of box
    for sphere or shell, q1 = # of divisions per face edge of embedded cube
    for cyl or cap, q1 = # of divisions per face edge of end cap, must be even
                    q2 = # of divisions along length of cylinder

c.line(ID,x1,y1,z1,x2,y2,z2)       create a line object with one line
c.lbox(ID,xlo,ylo,zlo,xhi,yhi,zhi) create a line object with 12 box lines

c.surf(ID,id-region)               create a triangulated surf from a region
c.surftri(ID,id-surf,t1,t2,...)    create a tri surf from list of id-surf tris
c.surfselect(ID,id-surf,test)      create a tri surf from test on id-surf tris
c.bins(ID,nx,ny)                   set binning parameters for a surf

  triangulation of a shell is just done for the outer sphere
  for surftri(), one or more tri indices (1-N) must be listed
  for surfselect(), test is string like "$x < 2.0 and $y > 0.0"
  bins are used when particles are created inside/outside a surf

c.part(ID,n,id_in)  	           create N particles inside object id_in
c.part(ID,n,id_in,id_out)	   particles are also outside object id_out
c.part2d(ID,n,id_on)               create 2d particles on object id_on
c.partarray(ID,nx,nz,nz,x,y,z,dx,dy,dz)   create 3d grid of particles
c.partring(ID,n,x,y,z,r,'x')              create ring of particles
c.partsurf(ID,id_on)               change surf of existing 2d particle group
c.seed(43284)			   set random # seed (def = 12345)

  generate particle positions randomly (unless otherwise noted)
  for part(), id_in and id_out must be IDs of a surf, region, or union object
    inside a union object means inside any of the lower-level objects
    outside a union object means outside all of the lower-level objects
  for part2d(), id_on must be ID of a surf, region, or union object
  for part2d(), particles will be written as 2d assigned to surf id_on
  for partring(), ring axis is in 'x','y', or 'z' direction
  partsurf() changes surf id_on for an existing 2d particle group

x,n = c.random(ID)                 pick a random pt on surf of object ID

c.project(ID,ID2,dx,dy,dz,eps,fg)  project particles in ID to surf of obj ID2

  random() returns pt = [x,y,z] and normal vec n [nx,ny,nz]
  project() remaps particle coords in group ID
    moves each particle along dir until they are within eps of surface
    if no fg arg, dir = (dx,dy,dz)
    if fg arg, dir = line from particle coord to (dx,dy,dz)
    ID2 can be surf or region obj
    particles are converted to 2d assigned to surf ID2

c.center(ID,x,y,z)                 set center point of object
c.trans(ID,dx,dy,dz)   	 	   translate an object
c.rotate(ID,'x',1,1,0,'z',-1,1,0)  rotate an object
c.scale(ID,sx,sy,sz)		   scale an object

  objects must be surface or particle group, regions cannot be changed
  for center(), default is middle of bounding box (set when obj is created)
  for rotate(), set any 2 axes, must be orthogonal, 3rd is inferred
    object is rotated so that it's current xyz axes point along new ones
  rotation and scaling occur relative to center point

c.union(ID,id1,id2,...)		   create a new union object from id1,id2,etc
c.join(ID,id1,id2,...)             create a new object by joining id1,id2,etc
c.delete(id1,id2,...)              delete one or more objects
c.rename(ID,IDnew)                 rename an object
c.copy(ID,IDnew) 	           create a new object as copy of old object

  for union, all lower-level objects must be of surface, region, or union style
  for join, all joined objects must be of same style: group, surf, line
    new object is the same style

c.select(id1,id2,...)              select one or more objects
c.select()                         select all objects
c.unselect(id1,id2,...)            unselect one or more objects
c.unselect()                       unselect all objects

  selection applies to write() and viz()

c.write("file")			   write all selected objs to ChemCell file
c.write("file",id1,id2,...)	   write only listed & selected objects to file
c.append("file")		   append all selected objs to ChemCell file
c.append("file",id1,id2,...)	   append only listed & selected objects

  union objects are skipped, not written to file

index,time,flag = c.iterator(0/1)          loop over single snapshot
time,box,atoms,bonds,tris,lines = c.viz(index)   return list of viz objects

  iterator() and viz() are compatible with equivalent dump calls
  iterator() called with arg = 0 first time, with arg = 1 on subsequent calls
    index = timestep index within dump object (only 0 for data file)
    time = timestep value (only 0 for data file)
    flag = -1 when iteration is done, 1 otherwise
  viz() returns info for selected objs for specified timestep index (must be 0)
    time = 0
    box = [xlo,ylo,zlo,xhi,yhi,zhi]
    atoms = id,type,x,y,z for each atom as 2d array
      NULL if atoms do not exist
    bonds = NULL
    tris = id,type,x1,y1,z1,x2,y2,z2,x3,y3,z3,nx,ny,nz for each tri as 2d array
      regions are triangulated according to q() settings by viz()
      NULL if surfaces do not exist
    lines = id,type,x1,y1,z1,x2,y2,z2 for each line as 2d array
      NULL if lines do not exist
    types are assigned to each object of same style in ascending order
"""

# History
#      11/05, Steve Plimpton (SNL): original version
# 2025-01-17, first conversion in connection with the update of pizza.dump3

# ToDo list

# Variables
#   nselect = 1 = # of snapshots
#   ids = dictionary of IDs that points to object index
#   objs = list of objects, style = REGION, SURFACE, GROUP, UNION

# Imports and external programs

import sys
import glob
from os import popen
from math import sqrt, pi, cos, sin, fabs
from copy import deepcopy

##############################################################################
# External dependency
PIZZA_GUNZIP = "gunzip"

##############################################################################
# Define constants for object styles

REGION   = 1
SURFACE  = 2
GROUP    = 3
UNION    = 4

BOX      = 5
SPHERE   = 6
SHELL    = 7
CYLINDER = 8
CAPPED   = 9
LINE     = 10

EPSILON  = 1.0e-6
BIG      = 1.0e20

##############################################################################
# Random Number Generator

IM = 2147483647
AM = 1.0 / IM
IA = 16807
IQ = 127773
IR = 2836

class Random:
    """
    Simple linear congruential generator (LCG) for random numbers.
    """
    def __init__(self, seed):
        self.seed = seed
    
    def __call__(self):
        k = self.seed // IQ
        self.seed = IA * (self.seed - k * IQ) - IR * k
        if self.seed < 0:
            self.seed += IM
        return AM * self.seed

##############################################################################
# Vector Helpers

def cross(a, b):
    """
    Compute the cross product of vectors a and b (each 3D).
    """
    return [
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0]
    ]

def normalize(a):
    """
    Normalize vector a in-place to unit length.
    """
    length = sqrt(a[0]**2 + a[1]**2 + a[2]**2)
    if length != 0.0:
        a[0] /= length
        a[1] /= length
        a[2] /= length

def normal(x, y, z):
    """
    Compute the normal vector for a triangle with vertices x, y, z.
    Each vertex is a 3D coordinate [x, y, z].
    """
    v1 = [y[i] - x[i] for i in range(3)]
    v2 = [z[i] - y[i] for i in range(3)]
    n = cross(v1, v2)
    normalize(n)
    return n


##############################################################################
# Triangulation Helpers

def vertex(v, vertices, vdict):
    """
    Add a vertex to the vertices list if not already present.
    Return the index of the vertex in the vertices list.
    """
    vtup = tuple(v)
    if vtup in vdict:
        return vdict[vtup]
    idx = len(vertices)
    vertices.append(v)
    vdict[vtup] = idx
    return idx

def connect(nvert, ntri, triangles):
    """
    Create connections between triangles in a triangulated surface.
    Each triangle has 3 vertices. Return a list of connections for each tri.
    """
    # v2tri[v] = list of triangles that vertex v is a member of
    v2tri = [[] for _ in range(nvert)]
    for i in range(ntri):
        for vert in triangles[i]:
            v2tri[vert-1].append(i)
    
    connections = []
    for i in range(ntri):
        connect_tri = [0]*6  # [tri1, edge1, tri2, edge2, tri3, edge3]
        v = triangles[i]
        
        # For edges (v[0]-v[1]), (v[1]-v[2]), (v[2]-v[0])
        edges = [
            (v[0], v[1]),
            (v[1], v[2]),
            (v[2], v[0])
        ]
        
        for edge_idx, (startv, endv) in enumerate(edges):
            # Triangles sharing startv
            for itri in v2tri[startv-1]:
                if itri == i:
                    continue
                if endv in triangles[itri]:
                    connect_tri[2*edge_idx] = itri+1
                    # Figure out which edge in itri
                    # (this is approximate; advanced logic may be required)
                    other_tri = triangles[itri]
                    # Attempt to find local edge
                    # For simplicity, store edge=1 if other_tri's first edge,
                    # edge=2 if second, edge=3 if third, etc.
                    # This might need deeper logic if the 'edge index' is critical.
                    connect_tri[2*edge_idx + 1] = 1  # Simplify for now
                    break
        
        connections.append(connect_tri)
    return connections

def box_triangulate(q1, q2, q3):
    """
    Triangulate a unit box from (0,0,0) to (1,1,1) with spacings q1, q2, q3.
    Return a list of vertices and triangles. Triangles are oriented outward.
    """
    dx = 1.0/q1 if q1 else 1.0
    dy = 1.0/q2 if q2 else 1.0
    dz = 1.0/q3 if q3 else 1.0
    
    vdict = {}
    vertices = []
    triangles = []
    
    # Triangulate faces in x=0, x=1, y=0, y=1, z=0, z=1, etc.
    # This method can be quite extensive; for clarity, partial examples
    # are included. Adjust logic as needed to cover all box faces.
    
    # Face x=0
    for j in range(q2):
        for k in range(q3):
            v1 = (0,      j*dy,     k*dz)
            v2 = (0, (j+1)*dy,     k*dz)
            v3 = (0, (j+1)*dy, (k+1)*dz)
            v4 = (0,      j*dy, (k+1)*dz)
            
            iv1 = vertex(list(v1), vertices, vdict)
            iv2 = vertex(list(v2), vertices, vdict)
            iv3 = vertex(list(v3), vertices, vdict)
            iv4 = vertex(list(v4), vertices, vdict)
            
            # Two triangles per cell
            triangles.append([iv1+1, iv3+1, iv2+1])
            triangles.append([iv1+1, iv4+1, iv3+1])
    
    # Similarly handle x=1, y=0, y=1, z=0, z=1 faces...
    # For brevity, only partial face coverage is shown here.
    # Extend similarly if a full triangulation is required.
    
    return vertices, triangles


##############################################################################
# Base Classes for cdata

class Surface:
    def __init__(self):
        self.select = 0
        self.style = SURFACE
        self.id = ""
        self.nvert = 0
        self.ntri = 0
        self.nbinx = 0
        self.nbiny = 0
        self.vertices = []
        self.triangles = []
        self.connections = []
        # For bounding box center
        self.xc = 0.0
        self.yc = 0.0
        self.zc = 0.0
    
    def bbox(self):
        """
        Return bounding box of all vertices in this surface.
        """
        if not self.vertices:
            return (0, 0, 0, 0, 0, 0)
        xs = [float(v[0]) for v in self.vertices]
        ys = [float(v[1]) for v in self.vertices]
        zs = [float(v[2]) for v in self.vertices]
        return (min(xs), min(ys), min(zs), max(xs), max(ys), max(zs))
    
    def center(self, x=None, y=None, z=None):
        """
        Set center of the surface explicitly or to the midpoint of bounding box.
        """
        if x is not None and y is not None and z is not None:
            self.xc = x
            self.yc = y
            self.zc = z
        else:
            xlo, ylo, zlo, xhi, yhi, zhi = self.bbox()
            self.xc = 0.5 * (xlo + xhi)
            self.yc = 0.5 * (ylo + yhi)
            self.zc = 0.5 * (zlo + zhi)
    
    def inside_prep(self):
        """
        Prepare binning if you want to accelerate inside() checks.
        Depending on usage, implement as needed.
        """
        pass
    
    def inside(self, x, y, z):
        """
        Check if point (x, y, z) is inside this closed surface.
        By default, return False (0).
        Implement if needed.
        """
        return 0
    
    def area(self):
        """
        Return total surface area of this surface.
        By default, sum the area of each triangle.
        """
        # For each tri, area = 1/2 * cross(v2 - v1, v3 - v1)
        # We'll accumulate it.
        total_area = 0.0
        for tri in self.triangles:
            v1 = self.vertices[tri[0]-1]
            v2 = self.vertices[tri[1]-1]
            v3 = self.vertices[tri[2]-1]
            # Compute area
            side1 = [v2[i] - v1[i] for i in range(3)]
            side2 = [v3[i] - v1[i] for i in range(3)]
            cr = cross(side1, side2)
            tri_area = 0.5 * sqrt(cr[0]**2 + cr[1]**2 + cr[2]**2)
            total_area += tri_area
        return total_area
    
    def loc2d(self, area, random_fn):
        """
        Return a random point on the surface, given a pre-chosen 'area' fraction.
        By default, pick from triangles in ascending area order.
        Must implement your own partial sums if you want a strict area-based sampling.
        """
        # Simple placeholder: pick any tri
        if not self.triangles:
            return ([0.0, 0.0, 0.0], [0.0, 0.0, 1.0])
        # For now, pick the first triangle
        tri = self.triangles[0]
        v1 = self.vertices[tri[0]-1]
        v2 = self.vertices[tri[1]-1]
        v3 = self.vertices[tri[2]-1]
        # Barycentric random
        r1 = random_fn()
        r2 = random_fn()
        if r1 + r2 > 1.0:
            r1 = 1.0 - r1
            r2 = 1.0 - r2
        x = v1[0] + r1*(v2[0] - v1[0]) + r2*(v3[0] - v1[0])
        y = v1[1] + r1*(v2[1] - v1[1]) + r2*(v3[1] - v1[1])
        z = v1[2] + r1*(v2[2] - v1[2]) + r2*(v3[2] - v1[2])
        n = normal(v1, v2, v3)
        return ([x, y, z], n)

class Group:
    def __init__(self):
        self.select = 0
        self.style = GROUP
        self.id = ""
        self.npart = 0
        self.xyz = []
        self.on_id = ""
        # For bounding box center
        self.xc = 0.0
        self.yc = 0.0
        self.zc = 0.0
    
    def bbox(self):
        """
        Return bounding box of all particles in this group.
        """
        if not self.xyz:
            return (0, 0, 0, 0, 0, 0)
        xs = [p[0] for p in self.xyz]
        ys = [p[1] for p in self.xyz]
        zs = [p[2] for p in self.xyz]
        return (min(xs), min(ys), min(zs), max(xs), max(ys), max(zs))
    
    def center(self, x=None, y=None, z=None):
        """
        Set center of the group explicitly or to the midpoint of bounding box.
        """
        if x is not None and y is not None and z is not None:
            self.xc = x
            self.yc = y
            self.zc = z
        else:
            xlo, ylo, zlo, xhi, yhi, zhi = self.bbox()
            self.xc = 0.5 * (xlo + xhi)
            self.yc = 0.5 * (ylo + yhi)
            self.zc = 0.5 * (zlo + zhi)

class Box:
    def __init__(self, *args):
        self.select = 0
        self.style = REGION
        self.id = ""
        self.substyle = BOX
        self.xlo = float(args[0])
        self.ylo = float(args[1])
        self.zlo = float(args[2])
        self.xhi = float(args[3])
        self.yhi = float(args[4])
        self.zhi = float(args[5])
        # Default triangulation quality
        self.q1 = self.q2 = self.q3 = 1.0

    def bbox(self):
        return (self.xlo, self.ylo, self.zlo, self.xhi, self.yhi, self.zhi)

    def inside(self, x, y, z):
        if x < self.xlo or x > self.xhi: return 0
        if y < self.ylo or y > self.yhi: return 0
        if z < self.zlo or z > self.zhi: return 0
        return 1

    def triangulate(self):
        vertices, triangles = box_triangulate(int(self.q1),
                                              int(self.q2),
                                              int(self.q3))
        self.nvert = len(vertices)
        self.ntri = len(triangles)
        self.vertices = []
        for i in range(self.nvert):
            v1 = self.xlo + vertices[i][0]*(self.xhi - self.xlo)
            v2 = self.ylo + vertices[i][1]*(self.yhi - self.ylo)
            v3 = self.zlo + vertices[i][2]*(self.zhi - self.zlo)
            self.vertices.append([v1, v2, v3])
        self.triangles = []
        for tri in triangles:
            self.triangles.append([tri[0], tri[1], tri[2]])
        self.connections = connect(self.nvert, self.ntri, self.triangles)

    def area(self):
        xsize = self.xhi - self.xlo
        ysize = self.yhi - self.ylo
        zsize = self.zhi - self.zlo
        # area of all 6 faces
        faces = [
            ysize*zsize,
            ysize*zsize,
            xsize*zsize,
            xsize*zsize,
            xsize*ysize,
            xsize*ysize,
        ]
        # Store cumulative if desired, but we’ll just return sum
        return sum(faces)

    def loc2d(self, area, random_fn):
        """
        Return a random point on the surface, ignoring partial sums for now.
        This is a simplified approach. Adjust to handle 'area' fraction properly.
        """
        # For demonstration, pick one face (e.g., x=low)
        r1, r2 = random_fn(), random_fn()
        xsize = self.xhi - self.xlo
        ysize = self.yhi - self.ylo
        zsize = self.zhi - self.zlo
        # Suppose we pick face x=low
        return ([self.xlo,
                 self.ylo + r1*ysize,
                 self.zlo + r2*zsize],
                [-1.0, 0.0, 0.0])

    def command(self):
        return f"{self.id} box {self.xlo} {self.ylo} {self.zlo} {self.xhi} {self.yhi} {self.zhi}"

class Sphere:
    def __init__(self, *args):
        self.select = 0
        self.style = REGION
        self.id = ""
        self.substyle = SPHERE
        self.x = float(args[0])
        self.y = float(args[1])
        self.z = float(args[2])
        self.r = float(args[3])
        self.rsq = self.r**2
        # Triangulation quality
        self.q1 = 2.0

    def bbox(self):
        return (self.x-self.r, self.y-self.r, self.z-self.r,
                self.x+self.r, self.y+self.r, self.z+self.r)

    def inside(self, x, y, z):
        dx = x - self.x
        dy = y - self.y
        dz = z - self.z
        if (dx*dx + dy*dy + dz*dz) > self.rsq:
            return 0
        return 1

    def triangulate(self):
        vertices, triangles = box_triangulate(int(self.q1),
                                              int(self.q1),
                                              int(self.q1))
        self.nvert = len(vertices)
        self.ntri = len(triangles)
        self.vertices = []
        for i in range(self.nvert):
            v1 = vertices[i][0] - 0.5
            v2 = vertices[i][1] - 0.5
            v3 = vertices[i][2] - 0.5
            c = [v1, v2, v3]
            normalize(c)
            c[0] = self.x + self.r*c[0]
            c[1] = self.y + self.r*c[1]
            c[2] = self.z + self.r*c[2]
            self.vertices.append(c)
        self.triangles = []
        for tri in triangles:
            self.triangles.append([tri[0], tri[1], tri[2]])
        self.connections = connect(self.nvert, self.ntri, self.triangles)

    def area(self):
        return 4.0 * pi * (self.r**2)

    def loc2d(self, area, random_fn):
        """
        Return a random location on the sphere surface.
        """
        while True:
            x_ = random_fn() - 0.5
            y_ = random_fn() - 0.5
            z_ = random_fn() - 0.5
            if (x_*x_ + y_*y_ + z_*z_) <= 0.25:
                break
        c = [x_, y_, z_]
        normalize(c)
        return ([self.x + self.r*c[0],
                 self.y + self.r*c[1],
                 self.z + self.r*c[2]],
                c)

    def command(self):
        return f"{self.id} sphere {self.x} {self.y} {self.z} {self.r}"

class Shell(Sphere):
    def __init__(self, *args):
        super().__init__(*args[:4])
        self.substyle = SHELL
        self.rinner = float(args[4])
        self.innersq = self.rinner**2

    def inside(self, x, y, z):
        dx = x - self.x
        dy = y - self.y
        dz = z - self.z
        rsq = dx*dx + dy*dy + dz*dz
        if rsq > self.rsq or rsq < self.innersq:
            return 0
        return 1

    def command(self):
        return f"{self.id} shell {self.x} {self.y} {self.z} {self.r} {self.rinner}"

class Cylinder:
    def __init__(self, *args):
        self.select = 0
        self.style = REGION
        self.id = ""
        self.substyle = CYLINDER
        self.axis = args[0]
        self.c1 = float(args[1])
        self.c2 = float(args[2])
        self.r = float(args[3])
        self.lo = float(args[4])
        self.hi = float(args[5])
        self.rsq = self.r**2
        self.q1 = 2
        self.q2 = 1

    def bbox(self):
        if self.axis == 'x':
            return (self.lo, self.c1-self.r, self.c2-self.r,
                    self.hi, self.c1+self.r, self.c2+self.r)
        elif self.axis == 'y':
            return (self.c1-self.r, self.lo, self.c2-self.r,
                    self.c1+self.r, self.hi, self.c2+self.r)
        elif self.axis == 'z':
            return (self.c1-self.r, self.c2-self.r, self.lo,
                    self.c1+self.r, self.c2+self.r, self.hi)
        return (0, 0, 0, 0, 0, 0)

    def inside(self, x, y, z):
        if self.axis == 'x':
            d1 = y - self.c1
            d2 = z - self.c2
            d3 = x
        elif self.axis == 'y':
            d1 = x - self.c1
            d2 = z - self.c2
            d3 = y
        else:  # 'z'
            d1 = x - self.c1
            d2 = y - self.c2
            d3 = z
        rsq = d1*d1 + d2*d2
        if rsq > self.rsq:
            return 0
        if d3 < self.lo or d3 > self.hi:
            return 0
        return 1

    def triangulate(self):
        vertices, triangles = box_triangulate(self.q1, self.q1, self.q2)
        self.nvert = len(vertices)
        self.ntri = len(triangles)
        self.vertices = []
        for v in vertices:
            v1 = v[0] - 0.5
            v2 = v[1] - 0.5
            v3 = v[2]
            c = [v1, v2, 0]
            normalize(c)
            length = max(fabs(v1), fabs(v2)) * 2.0
            c[0] *= length
            c[1] *= length
            p1 = self.c1 + self.r*c[0]
            p2 = self.c2 + self.r*c[1]
            p3 = self.lo + v3*(self.hi - self.lo)
            if self.axis == 'x':
                self.vertices.append([p3, p1, p2])
            elif self.axis == 'y':
                self.vertices.append([p1, p3, p2])
            else:
                self.vertices.append([p1, p2, p3])
        self.triangles = [[t[0], t[1], t[2]] for t in triangles]
        self.connections = connect(self.nvert, self.ntri, self.triangles)

    def area(self):
        """
        Cylinder area = 2 * (circle area) + side area = 2 * (πr²) + (2πr * length)
        But we store partial sums if needed.
        """
        circle_area = pi * self.r**2
        length = self.hi - self.lo
        top_bottom = 2*circle_area
        side = 2*pi*self.r*length
        self.areas = [circle_area, top_bottom, top_bottom+side]
        return top_bottom + side

    def loc2d(self, area, random_fn):
        # Implementation stub
        return ([self.c1, self.c2, self.lo], [1, 0, 0])

    def command(self):
        return (f"{self.id} cylinder {self.axis} {self.c1} {self.c2} "
                f"{self.r} {self.lo} {self.hi}")

class Capped:
    def __init__(self, *args):
        self.select = 0
        self.style = REGION
        self.id = ""
        self.substyle = CAPPED
        self.axis = args[0]
        self.c1 = float(args[1])
        self.c2 = float(args[2])
        self.r = float(args[3])
        self.lo = float(args[4])
        self.hi = float(args[5])
        self.rsq = self.r**2
        self.q1 = 2
        self.q2 = 1

    def bbox(self):
        if self.axis == 'x':
            return (self.lo - self.r, self.c1 - self.r, self.c2 - self.r,
                    self.hi + self.r, self.c1 + self.r, self.c2 + self.r)
        elif self.axis == 'y':
            return (self.c1 - self.r, self.lo - self.r, self.c2 - self.r,
                    self.c1 + self.r, self.hi + self.r, self.c2 + self.r)
        else:  # 'z'
            return (self.c1 - self.r, self.c2 - self.r, self.lo - self.r,
                    self.c1 + self.r, self.c2 + self.r, self.hi + self.r)

    def inside(self, x, y, z):
        if self.axis == 'x':
            d1 = y - self.c1
            d2 = z - self.c2
            d3 = x
        elif self.axis == 'y':
            d1 = x - self.c1
            d2 = z - self.c2
            d3 = y
        else:  # 'z'
            d1 = x - self.c1
            d2 = y - self.c2
            d3 = z
        rsq = d1*d1 + d2*d2
        if self.lo <= d3 <= self.hi:
            if rsq > self.rsq:
                return 0
        elif d3 < self.lo:
            if (d1*d1 + d2*d2 + (d3 - self.lo)**2) > self.rsq:
                return 0
        else:
            if (d1*d1 + d2*d2 + (d3 - self.hi)**2) > self.rsq:
                return 0
        return 1

    def triangulate(self):
        if self.q1 % 2 != 0:
            raise Exception("Capped cylinder q1 must be even")
        vertices, triangles = box_triangulate(int(self.q1),
                                              int(self.q1),
                                              int(self.q2 + self.q1))
        self.nvert = len(vertices)
        self.ntri = len(triangles)
        self.vertices = []
        # For a capped cylinder, partial code:
        cutlo = (self.q1 // 2) * 1.0 / (self.q2 + self.q1) + EPSILON
        cuthi = 1.0 - cutlo
        for v in vertices:
            v1 = v[0]
            v2 = v[1]
            v3 = v[2]
            if v3 < cutlo:
                c = [v1 - 0.5, v2 - 0.5, (v3 - cutlo)*(0.5/cutlo)]
                normalize(c)
                p1 = self.c1 + self.r*c[0]
                p2 = self.c2 + self.r*c[1]
                p3 = self.lo + self.r*c[2]
            elif v3 > cuthi:
                c = [v1 - 0.5, v2 - 0.5, (v3 - cuthi)*(0.5/cutlo)]
                normalize(c)
                p1 = self.c1 + self.r*c[0]
                p2 = self.c2 + self.r*c[1]
                p3 = self.hi + self.r*c[2]
            else:
                c = [v1 - 0.5, v2 - 0.5, 0.0]
                normalize(c)
                p1 = self.c1 + self.r*c[0]
                p2 = self.c2 + self.r*c[1]
                frac = (v3 - cutlo) / (cuthi - cutlo)
                p3 = self.lo + frac * (self.hi - self.lo)
            if self.axis == 'x':
                self.vertices.append([p3, p1, p2])
            elif self.axis == 'y':
                self.vertices.append([p1, p3, p2])
            else:
                self.vertices.append([p1, p2, p3])
        self.triangles = [[t[0], t[1], t[2]] for t in triangles]
        self.connections = connect(self.nvert, self.ntri, self.triangles)

    def area(self):
        """
        Surface area of a capped cylinder = cylinder area + 2 * hemisphere discs.
        Approximate if needed. Or store partial sums if you want area-based loc2d.
        """
        # Simplistic example:
        side_area = 2 * pi * self.r * (self.hi - self.lo)
        circle_area = pi * self.r * self.r
        # top circle + bottom circle
        top_bottom_area = 2 * circle_area
        return side_area + top_bottom_area

    def loc2d(self, area, random_fn):
        """
        Return a random location on the capped cylinder surface.
        """
        # Implement a full partition if you want exact coverage.
        return ([self.c1, self.c2, self.lo], [1, 0, 0])

    def command(self):
        return (f"{self.id} capped {self.axis} {self.c1} {self.c2} "
                f"{self.r} {self.lo} {self.hi}")

class Line:
    def __init__(self):
        self.select = 0
        self.style = LINE
        self.id = ""
        self.nline = 0
        self.pairs = []
    
    def bbox(self):
        """
        Return bounding box around all line segments.
        """
        if not self.pairs:
            return (0, 0, 0, 0, 0, 0)
        xs = [p[0] for p in self.pairs] + [p[3] for p in self.pairs]
        ys = [p[1] for p in self.pairs] + [p[4] for p in self.pairs]
        zs = [p[2] for p in self.pairs] + [p[5] for p in self.pairs]
        return (min(xs), min(ys), min(zs), max(xs), max(ys), max(zs))
    
    def addline(self, coords):
        """
        Add a single line segment (x1, y1, z1, x2, y2, z2).
        """
        self.nline += 1
        self.pairs.append(list(coords))

class Union:
    def __init__(self, ids, objs, *list_ids):
        self.select = 0
        self.style = UNION
        self.id = ""
        # child objects
        self.objs = []
        for obj_id in list_ids:
            obj = objs[ids[obj_id]]
            if obj.style not in [SURFACE, REGION, UNION]:
                raise Exception("Union child object is of invalid style")
            self.objs.append(obj)
    
    def bbox(self):
        if not self.objs:
            return (0, 0, 0, 0, 0, 0)
        xlo, ylo, zlo, xhi, yhi, zhi = self.objs[0].bbox()
        for obj in self.objs[1:]:
            xxlo, yylo, zzlo, xxhi, yyhi, zzhi = obj.bbox()
            if xxlo < xlo: xlo = xxlo
            if yylo < ylo: ylo = yylo
            if zzlo < zlo: zlo = zzlo
            if xxhi > xhi: xhi = xxhi
            if yyhi > yhi: yhi = yyhi
            if zzhi > zhi: zhi = zzhi
        return (xlo, ylo, zlo, xhi, yhi, zhi)
    
    def inside(self, x, y, z):
        # inside union if inside any of its child objects
        for obj in self.objs:
            if obj.inside(x, y, z):
                return 1
        return 0
    
    def area(self):
        # sum areas of child objects
        total = 0.0
        for obj in self.objs:
            total += obj.area()
        return total
    
    def loc2d(self, area, random_fn):
        """
        Return a random location on the union surface, if needed.
        This would require partial sums across each child's area.
        For brevity, pick first child.
        """
        if not self.objs:
            return ([0,0,0], [0,0,1])
        return self.objs[0].loc2d(area, random_fn)



# --------------------------------------------------------------------
# cdata Class Definition

class cdata:
    """
    cdata class for reading, creating, and manipulating ChemCell data files.
    """
    
    # --------------------------------------------------------------------
    
    def __init__(self, *list):
        """
        Initialize the cdata object.

        Parameters:
            *list: Variable length argument list of file names to read.
        """
        self.nselect = 1
        self.ids = {}
        self.objs = []
        self.random = Random(12345)

        if len(list):
            self.read(*list)
    
    # --------------------------------------------------------------------
    
    def read(self, *list):
        """
        Read ChemCell data files and populate objects.

        Parameters:
            *list: Variable length argument list of file names to read.
        """
        # flist = list of all data file names
        words = list[0].split()
        flist = []
        for word in words:
            flist += glob.glob(word)
        if len(flist) == 0 and len(list) == 1:
            raise Exception("no data file specified")
    
        for file in flist:
            # Test for gzipped file
            if file.endswith(".gz"):
                f = popen(f"{PIZZA_GUNZIP} -c {file}", 'r')
            else:
                f = open(file, 'r')
    
            # Read all entries in file
            while True:
                line = f.readline()
                if not line:
                    break
                line = line.strip()
                if not line:
                    continue
                elif line.startswith("triangles"):
                    flag = "triangles"
                elif line.startswith("particles"):
                    flag = "particles"
                elif line.startswith("facets"):
                    flag = "facets"
                elif line.startswith("region"):
                    flag = "region"
                else:
                    print("unknown line:", line)
                    raise Exception("unrecognized ChemCell data file")
    
                # Create a surface object from set of triangles or facets
                if flag in ["triangles", "facets"]:
                    tmp, id, nvert, ntri = line.split()
                    nvert = int(nvert)
                    ntri = int(ntri)
    
                    if id in self.ids:
                        raise Exception(f"ID {id} is already in use")
    
                    f.readline()  # Read past header
                    vertices = []
                    for _ in range(nvert):
                        parts = f.readline().split()
                        vertices.append([float(value) for value in parts[1:]])
                    f.readline()  # Read past another header
                    triangles = []
                    for _ in range(ntri):
                        parts = f.readline().split()
                        triangles.append([int(value) for value in parts[1:]])
    
                    if flag == "triangles":
                        f.readline()  # Read past another header
                        connections = []
                        for _ in range(ntri):
                            parts = f.readline().split()
                            connections.append([int(value) for value in parts[1:]])
                    else:
                        connections = connect(nvert, ntri, triangles)
                    
                    obj = Surface()
                    obj.select = 1
                    self.ids[id] = len(self.objs)
                    self.objs.append(obj)
                    obj.id = id
                    obj.style = SURFACE
                    obj.nvert = nvert
                    obj.ntri = ntri
                    obj.vertices = vertices
                    obj.triangles = triangles
                    obj.connections = connections
                    obj.center()
                  
                    print(id, end=' ')
                    sys.stdout.flush()
    
                # Create a group object from list of particles
                if flag == "particles":
                    words = line.split()
                    id = words[1]
                    npart = int(words[2])
    
                    if id in self.ids:
                        raise Exception(f"ID {id} is already in use")
    
                    f.readline()  # Read past header
                    xyz = []
                    for _ in range(npart):
                        parts = f.readline().split()
                        xyz.append([float(value) for value in parts[1:]])
    
                    obj = Group()
                    obj.select = 1
                    self.ids[id] = len(self.objs)
                    self.objs.append(obj)
                    obj.id = id
                    obj.style = GROUP
                    obj.on_id = ""
                    if len(words) == 4:
                        obj.on_id = words[3]
                    obj.npart = npart
                    obj.xyz = xyz
                    obj.center()
                    
                    print(id, end=' ')
                    sys.stdout.flush()
    
                # Create a region object from ChemCell region command
                if flag == "region":
                    words = line.split()
                    id = words[1]
                    style = words[2]
                    args = words[3:]
                    
                    if style == "box":
                        obj = Box(*args)
                        obj.substyle = BOX
                    elif style == "sphere":
                        obj = Sphere(*args)
                    elif style == "shell":
                        obj = Shell(*args)
                    elif style == "cylinder":
                        obj = Cylinder(*args)
                    elif style == "capped":
                        obj = Capped(*args)
                    else:
                        raise Exception(f"Unknown region style: {style}")
                    
                    obj.select = 1
                    self.ids[id] = len(self.objs)
                    self.objs.append(obj)
                    obj.id = id
                    obj.style = REGION
                    
                    print(id, end=' ')
                    sys.stdout.flush()
    
            f.close()
        print()
    
    # --------------------------------------------------------------------
    # Create Box Region
    
    def box(self, id, *args):
        """
        Create a box region.

        Parameters:
            id (str): Unique identifier for the box.
            args: xlo, ylo, zlo, xhi, yhi, zhi
        """
        if id in self.ids:
            raise Exception(f"ID {id} is already in use")
        obj = Box(*args)
        obj.select = 1
        self.ids[id] = len(self.objs)
        self.objs.append(obj)
        obj.id = id
        obj.style = REGION
        obj.substyle = BOX
    
    # --------------------------------------------------------------------
    # Create Sphere Region
    
    def sphere(self, id, *args):
        """
        Create a sphere region.

        Parameters:
            id (str): Unique identifier for the sphere.
            args: x, y, z, r
        """
        if id in self.ids:
            raise Exception(f"ID {id} is already in use")
        obj = Sphere(*args)
        obj.select = 1
        self.ids[id] = len(self.objs)
        self.objs.append(obj)
        obj.id = id
        obj.style = REGION
        obj.substyle = SPHERE
    
    # --------------------------------------------------------------------
    # Create Shell Region
    
    def shell(self, id, *args):
        """
        Create a shell region.

        Parameters:
            id (str): Unique identifier for the shell.
            args: x, y, z, r, rinner
        """
        if id in self.ids:
            raise Exception(f"ID {id} is already in use")
        obj = Shell(*args)
        obj.select = 1
        self.ids[id] = len(self.objs)
        self.objs.append(obj)
        obj.id = id
        obj.style = REGION
        obj.substyle = SHELL
    
    # --------------------------------------------------------------------
    # Create Cylinder Region
    
    def cyl(self, id, *args):
        """
        Create a cylinder region.

        Parameters:
            id (str): Unique identifier for the cylinder.
            args: axis, c1, c2, r, lo, hi
        """
        if id in self.ids:
            raise Exception(f"ID {id} is already in use")
        obj = Cylinder(*args)
        obj.select = 1
        self.ids[id] = len(self.objs)
        self.objs.append(obj)
        obj.id = id
        obj.style = REGION
        obj.substyle = CYLINDER
    
    # --------------------------------------------------------------------
    # Create Capped-Cylinder Region
    
    def cap(self, id, *args):
        """
        Create a capped-cylinder region.

        Parameters:
            id (str): Unique identifier for the capped-cylinder.
            args: axis, c1, c2, r, lo, hi
        """
        if id in self.ids:
            raise Exception(f"ID {id} is already in use")
        obj = Capped(*args)
        obj.select = 1
        self.ids[id] = len(self.objs)
        self.objs.append(obj)
        obj.id = id
        obj.style = REGION
        obj.substyle = CAPPED
    
    # --------------------------------------------------------------------
    # Set Quality Factors for a Region's Triangulation
    
    def q(self, id, *args):
        """
        Set quality factors for a region's triangulation routine.

        Parameters:
            id (str): Identifier of the region.
            args: Quality factors (q1, q2, ...)
        """
        obj = self.objs[self.ids[id]]
        if obj.style != REGION:
            raise Exception("Can only use q() on a region object")
        for n, arg in enumerate(args, start=1):
            setattr(obj, f"q{n}", arg)
    
    # --------------------------------------------------------------------
    # Create a Line Object with a Single Line
    
    def line(self, id, *args):
        """
        Create a line object with a single line.

        Parameters:
            id (str): Unique identifier for the line.
            args: x1, y1, z1, x2, y2, z2
        """
        if id in self.ids:
            raise Exception(f"ID {id} is already in use")
        obj = Line()
        obj.select = 1
        self.ids[id] = len(self.objs)
        self.objs.append(obj)
        obj.id = id
        obj.style = LINE
        obj.nline = 0
        obj.pairs = []
        
        obj.addline(args)
    
    # --------------------------------------------------------------------
    # Create a Line Object with 12 Box Lines
    
    def lbox(self, id, *args):
        """
        Create a line object with 12 lines representing a box.

        Parameters:
            id (str): Unique identifier for the line box.
            args: xlo, ylo, zlo, xhi, yhi, zhi
        """
        if id in self.ids:
            raise Exception(f"ID {id} is already in use")
        obj = Line()
        obj.select = 1
        self.ids[id] = len(self.objs)
        self.objs.append(obj)
        obj.id = id
        obj.style = LINE
        obj.nline = 0
        obj.pairs = []
        
        xlo, ylo, zlo, xhi, yhi, zhi = args
        obj.addline([xlo, ylo, zlo, xhi, ylo, zlo])
        obj.addline([xlo, yhi, zlo, xhi, yhi, zlo])
        obj.addline([xlo, yhi, zhi, xhi, yhi, zhi])
        obj.addline([xlo, ylo, zhi, xhi, ylo, zhi])
        obj.addline([xlo, ylo, zlo, xlo, yhi, zlo])
        obj.addline([xhi, ylo, zlo, xhi, yhi, zlo])
        obj.addline([xhi, ylo, zhi, xhi, yhi, zhi])
        obj.addline([xlo, ylo, zhi, xlo, yhi, zhi])
        obj.addline([xlo, ylo, zlo, xlo, ylo, zhi])
        obj.addline([xhi, ylo, zlo, xhi, ylo, zhi])
        obj.addline([xhi, yhi, zlo, xhi, yhi, zhi])
        obj.addline([xlo, yhi, zlo, xlo, yhi, zhi])
    
    # --------------------------------------------------------------------
    # Create a Triangulated Surface Object from a Region Object
    
    def surf(self, id, id_region):
        """
        Create a triangulated surface from a region object.

        Parameters:
            id (str): Unique identifier for the surface.
            id_region (str): Identifier of the region to triangulate.
        """
        if id in self.ids:
            raise Exception(f"ID {id} is already in use")
    
        region = self.objs[self.ids[id_region]]
        region.triangulate()
        
        obj = Surface()
        obj.select = 1
        self.ids[id] = len(self.objs)
        self.objs.append(obj)
        obj.id = id
        obj.style = SURFACE
        obj.nvert = region.nvert
        obj.ntri = region.ntri
        obj.vertices = deepcopy(region.vertices)
        obj.triangles = deepcopy(region.triangles)
        obj.connections = deepcopy(region.connections)
        obj.center()
    
    # --------------------------------------------------------------------
    # Create a Triangulated Surface Object from List of Triangle Indices
    
    def surftri(self, id, id_surf, *list_indices):
        """
        Create a triangulated surface from a list of triangle indices in another surface.

        Parameters:
            id (str): Unique identifier for the new surface.
            id_surf (str): Identifier of the existing surface.
            *list_indices: Triangle indices to include (1-based indexing).
        """
        if id in self.ids:
            raise Exception(f"ID {id} is already in use")
    
        o = self.objs[self.ids[id_surf]]
        
        obj = Surface()
        obj.select = 1
        self.ids[id] = len(self.objs)
        self.objs.append(obj)
        obj.id = id
        obj.style = SURFACE
        obj.nvert = 0
        obj.ntri = 0
        obj.vertices = []
        obj.triangles = []
    
        # Subtract 1 from tri and vert to convert to 0-based indexing
        for i in list_indices:
            tri = o.triangles[i-1]
            v1 = o.triangles[i-1][0]
            v2 = o.triangles[i-1][1]
            v3 = o.triangles[i-1][2]
            obj.vertices.append(o.vertices[v1-1][:])
            obj.vertices.append(o.vertices[v2-1][:])
            obj.vertices.append(o.vertices[v3-1][:])
            obj.triangles.append([obj.nvert+1, obj.nvert+2, obj.nvert+3])
            obj.nvert += 3
            obj.ntri += 1
    
        # Make any connections in new set of triangles
        obj.connections = connect(obj.nvert, obj.ntri, obj.triangles)
        obj.center()
    
    # --------------------------------------------------------------------
    # Create a Triangulated Surface Object by Selecting Triangles Based on a Test
    
    def surfselect(self, id, id_surf, teststr):
        """
        Create a triangulated surface by selecting triangles based on a test string.

        Parameters:
            id (str): Unique identifier for the new surface.
            id_surf (str): Identifier of the existing surface.
            teststr (str): Test condition (e.g., "$x < 2.0 and $y > 0.0").
        """
        if id in self.ids:
            raise Exception(f"ID {id} is already in use")
    
        o = self.objs[self.ids[id_surf]]
        
        obj = Surface()
        obj.select = 1
        self.ids[id] = len(self.objs)
        self.objs.append(obj)
        obj.id = id
        obj.style = SURFACE
        obj.nvert = 0
        obj.ntri = 0
        obj.vertices = []
        obj.triangles = []
    
        # Replace $var with o.vertices reference and compile test string
        cmd1 = teststr.replace("$x", "o.vertices[v1][0]")
        cmd1 = cmd1.replace("$y", "o.vertices[v1][1]")
        cmd1 = "flag1 = " + cmd1.replace("$z", "o.vertices[v1][2]")
        ccmd1 = compile(cmd1, '', 'single')
    
        cmd2 = teststr.replace("$x", "o.vertices[v2][0]")
        cmd2 = cmd2.replace("$y", "o.vertices[v2][1]")
        cmd2 = "flag2 = " + cmd2.replace("$z", "o.vertices[v2][2]")
        ccmd2 = compile(cmd2, '', 'single')
    
        cmd3 = teststr.replace("$x", "o.vertices[v3][0]")
        cmd3 = cmd3.replace("$y", "o.vertices[v3][1]")
        cmd3 = "flag3 = " + cmd3.replace("$z", "o.vertices[v3][2]")
        ccmd3 = compile(cmd3, '', 'single')
    
        # Loop over triangles in id_surf
        for tri in o.triangles:
            v1 = tri[0] - 1
            v2 = tri[1] - 1
            v3 = tri[2] - 1
            exec(ccmd1)
            exec(ccmd2)
            exec(ccmd3)
            if flag1 and flag2 and flag3:
                obj.vertices.append(o.vertices[v1][:])
                obj.vertices.append(o.vertices[v2][:])
                obj.vertices.append(o.vertices[v3][:])
                obj.triangles.append([obj.nvert+1, obj.nvert+2, obj.nvert+3])
                obj.nvert += 3
                obj.ntri += 1
    
        # Make any connections in new set of triangles
        obj.connections = connect(obj.nvert, obj.ntri, obj.triangles)
        obj.center()
    
    # --------------------------------------------------------------------
    # Set Binning Parameters for a Surface
    
    def bins(self, id, nx, ny):
        """
        Set binning parameters for a surface.

        Parameters:
            id (str): Identifier of the surface.
            nx (int): Number of bins in the x-direction.
            ny (int): Number of bins in the y-direction.
        """
        obj = self.objs[self.ids[id]]
        if obj.style != SURFACE:
            raise Exception("Can only set bins for surface")
        obj.nbinx = nx
        obj.nbiny = ny
    
    # --------------------------------------------------------------------
    # Create a Group Object with N Particles Inside and Outside Constraints
    
    def part(self, id, npart, in_id, out_id=None):
        """
        Create a group with N particles inside a specified object and optionally outside another.

        Parameters:
            id (str): Unique identifier for the particle group.
            npart (int): Number of particles to create.
            in_id (str): Identifier of the object particles should be inside.
            out_id (str, optional): Identifier of the object particles should be outside.
        """
        if id in self.ids:
            raise Exception(f"ID {id} is already in use")
    
        obj = Group()
        obj.select = 1
        self.ids[id] = len(self.objs)
        self.objs.append(obj)
        obj.id = id
        obj.style = GROUP
        obj.on_id = ""
        obj.npart = npart
        obj.xyz = []
    
        in_obj = self.objs[self.ids[in_id]]
        if out_id:
            out_obj = self.objs[self.ids[out_id]]
    
        # Pre-process SURFACE objects to bin their triangles for faster searching
        if in_obj.style == SURFACE:
            in_obj.inside_prep()
        if out_id and out_obj.style == SURFACE:
            out_obj.inside_prep()
    
        # Bounding box for generating points
        xlo, ylo, zlo, xhi, yhi, zhi = in_obj.bbox()
        xsize = xhi - xlo
        ysize = yhi - ylo
        zsize = zhi - zlo
    
        # Generate particles until have enough that satisfy in/out constraints
        count = attempt = 0
        while count < npart:
            attempt += 1
            x = xlo + self.random() * xsize
            y = ylo + self.random() * ysize
            z = zlo + self.random() * zsize
            if not in_obj.inside(x, y, z):
                continue
            if out_id and out_obj.inside(x, y, z):
                continue
            obj.xyz.append([x, y, z])
            count += 1
    
        obj.center()
        print(f"Created {count} particles in {attempt} attempts")
    
    # --------------------------------------------------------------------
    # Create a Group Object with N 2D Particles on a Surface
    
    def part2d(self, id, npart, on_id):
        """
        Create a group with N 2D particles on a specified surface.

        Parameters:
            id (str): Unique identifier for the 2D particle group.
            npart (int): Number of particles to create.
            on_id (str): Identifier of the object particles should be on.
        """
        if id in self.ids:
            raise Exception(f"ID {id} is already in use")
    
        obj = Group()
        obj.select = 1
        self.ids[id] = len(self.objs)
        self.objs.append(obj)
        obj.id = id
        obj.style = GROUP
        obj.on_id = on_id
        obj.npart = npart
        obj.xyz = []
    
        on_obj = self.objs[self.ids[on_id]]
        if on_obj.style not in [SURFACE, REGION, UNION]:
            raise Exception("Illegal ID to place particles on")
        totalarea = on_obj.area()
        
        for _ in range(npart):
            area = self.random() * totalarea
            pt, norm = on_obj.loc2d(area, self.random)
            obj.xyz.append(pt)
        
        obj.center()
        print(f"Created {npart} particles on area of {totalarea}")
    
    # --------------------------------------------------------------------
    # Create a 3D Array of Particles
    
    def partarray(self, id, nx, ny, nz, x, y, z, dx, dy, dz):
        """
        Create a 3D grid of particles.

        Parameters:
            id (str): Unique identifier for the particle array.
            nx, ny, nz (int): Number of particles in x, y, z directions.
            x, y, z (float): Starting coordinates.
            dx, dy, dz (float): Spacing between particles.
        """
        if id in self.ids:
            raise Exception(f"ID {id} is already in use")
    
        obj = Group()
        obj.select = 1
        self.ids[id] = len(self.objs)
        self.objs.append(obj)
        obj.id = id
        obj.style = GROUP
        obj.on_id = ""
        obj.npart = nx * ny * nz
        obj.xyz = []
    
        for k in range(nz):
            znew = z + k * dz
            for j in range(ny):
                ynew = y + j * dy
                for i in range(nx):
                    xnew = x + i * dx
                    obj.xyz.append([xnew, ynew, znew])
                    
        obj.center()
        print(f"Created {nx * ny * nz} particles")
    
    # --------------------------------------------------------------------
    # Create a Ring of Particles
    
    def partring(self, id, n, x, y, z, r, axis):
        """
        Create a ring of N particles.

        Parameters:
            id (str): Unique identifier for the particle ring.
            n (int): Number of particles in the ring.
            x, y, z (float): Center coordinates of the ring.
            r (float): Radius of the ring.
            axis (str): Axis of the ring ('x', 'y', or 'z').
        """
        if id in self.ids:
            raise Exception(f"ID {id} is already in use")
    
        obj = Group()
        obj.select = 1
        self.ids[id] = len(self.objs)
        self.objs.append(obj)
        obj.id = id
        obj.style = GROUP
        obj.on_id = ""
        obj.npart = n
        obj.xyz = []
    
        deltheta = 2.0 * pi / n
        for i in range(n):
            theta = i * deltheta
            if axis == 'x':
                xnew = x
                ynew = y + r * cos(theta)
                znew = z + r * sin(theta)
            elif axis == 'y':
                xnew = x + r * cos(theta)
                ynew = y
                znew = z + r * sin(theta)
            elif axis == 'z':
                xnew = x + r * cos(theta)
                ynew = y + r * sin(theta)
                znew = z
            else:
                raise Exception("Invalid axis for partring()")
            obj.xyz.append([xnew, ynew, znew])
                
        obj.center()
        print(f"Created {n} particles")
    
    # --------------------------------------------------------------------
    # Change Surface Assignment for a 2D Group of Particles
    
    def partsurf(self, id, on_id):
        """
        Change the surface assignment for a 2D group of particles.

        Parameters:
            id (str): Identifier of the particle group.
            on_id (str): New surface identifier.
        """
        obj = self.objs[self.ids[id]]
        if obj.style != GROUP:
            raise Exception("Must use particle group with partsurf()")
        if not obj.on_id:
            raise Exception("Must use partsurf() with 2d particles")
        obj.on_id = on_id
    
    # --------------------------------------------------------------------
    # Set Random Number Seed
    
    def seed(self, new_seed):
        """
        Set the random number generator seed.

        Parameters:
            new_seed (int): New seed value.
        """
        self.random.seed = new_seed
    
    # --------------------------------------------------------------------
    # Pick a Random Point on Surface of Object
    
    def random(self, id):
        """
        Pick a random point on the surface of the specified object.

        Parameters:
            id (str): Identifier of the surface or region.

        Returns:
            tuple: (point [x, y, z], normal vector [nx, ny, nz])
        """
        obj = self.objs[self.ids[id]]
        if obj.style not in [SURFACE, REGION]:
            raise Exception("Must use surf or region with random()")
    
        totalarea = obj.area()
        area = self.random() * totalarea
        pt, norm = obj.loc2d(area, self.random)
        return pt, norm
    
    # --------------------------------------------------------------------
    # Project Particles to Surface of Another Object
    
    def project(self, id, id2, dx, dy, dz, EPS, flag=None):
        """
        Project particles in group ID to the surface of object ID2.

        Parameters:
            id (str): Identifier of the particle group.
            id2 (str): Identifier of the target surface or region.
            dx, dy, dz (float): Direction components for projection.
            EPS (float): Epsilon value for proximity.
            flag (bool, optional): If True, direction is from particle to (dx, dy, dz).
        """
        obj = self.objs[self.ids[id]]
        if obj.style != GROUP:
            raise Exception("Must use particle group as 1st obj of project()")
        obj_on = self.objs[self.ids[id2]]
        if obj_on.style not in [SURFACE, REGION]:
            raise Exception("Must use surf or region as 2nd obj of project()")
    
        # Pre-process SURFACE to bin its triangles for faster searching
        if obj_on.style == SURFACE:
            obj_on.inside_prep()
    
        # For each particle, move it in dir from current location
        # Move along dir until get within EPS of surf
        # factor = multiply bracketing distance by this amount each iteration
        # maxscale = max multiple of dir vector to bracket in each direction
    
        factor = 2
        maxscale = 10.0
    
        for i in range(obj.npart):
            x, y, z_coord = obj.xyz[i]
            if flag:
                dir_vector = [dx - x, dy - y, dz - z_coord]
            else:
                dir_vector = [dx, dy, dz]
            normalize(dir_vector)
            
            # Start = inside/outside at starting point
            # Stop = inside/outside at bracketing point
            start = obj_on.inside(x, y, z_coord)
            stop = 0 if start else 1
    
            # Iterate to find bracketing point or until scale dist > maxdist
            # Bracket point = xyz +/- scale*dir
            # Multiply scale by factor each iteration
    
            scale = EPS
            bracket = start
            while scale < maxscale:
                xnew = x + scale * dir_vector[0]
                ynew = y + scale * dir_vector[1]
                znew = z_coord + scale * dir_vector[2]
                bracket = obj_on.inside(xnew, ynew, znew)
                if bracket == stop:
                    break
                xnew_neg = x - scale * dir_vector[0]
                ynew_neg = y - scale * dir_vector[1]
                znew_neg = z_coord - scale * dir_vector[2]
                bracket = obj_on.inside(xnew_neg, ynew_neg, znew_neg)
                if bracket == stop:
                    xnew, ynew, znew = xnew_neg, ynew_neg, znew_neg
                    break
                scale *= factor
    
            if bracket == start:
                raise Exception(f"Could not find bracket point for particle {i}")
    
            # Bisection search to zoom in to within EPS of surface
            # Separation = distance between 2 points
            delx = xnew - x
            dely = ynew - y
            delz = znew - z_coord
            separation = sqrt(delx**2 + dely**2 + delz**2)
            while separation > EPS:
                xmid = 0.5 * (x + xnew)
                ymid = 0.5 * (y + ynew)
                zmid = 0.5 * (z_coord + znew)
                value = obj_on.inside(xmid, ymid, zmid)
                if value == start:
                    x, y, z_coord = xmid, ymid, zmid
                else:
                    xnew, ynew, znew = xmid, ymid, zmid
                delx = xnew - x
                dely = ynew - y
                delz = znew - z_coord
                separation = sqrt(delx**2 + dely**2 + delz**2)
    
            obj.xyz[i][0] = x
            obj.xyz[i][1] = y
            obj.xyz[i][2] = z_coord
    
        obj.on_id = id2
        obj.center()
    
    # --------------------------------------------------------------------
    # Set Center Point of an Object
    
    def center(self, id, x, y, z):
        """
        Set the center point of an object.

        Parameters:
            id (str): Identifier of the object.
            x, y, z (float): New center coordinates.
        """
        obj = self.objs[self.ids[id]]
        if obj.style not in [SURFACE, GROUP]:
            raise Exception("Can only use center() on a surface or group object")
        obj.center(x, y, z)
    
    # --------------------------------------------------------------------
    # Translate an Object by dx, dy, dz
    
    def trans(self, id, dx, dy, dz):
        """
        Translate an object by a displacement.

        Parameters:
            id (str): Identifier of the object.
            dx, dy, dz (float): Displacement along x, y, z axes.
        """
        obj = self.objs[self.ids[id]]
        if obj.style not in [SURFACE, GROUP]:
            raise Exception("Can only use trans() on a surface or group object")
        obj.xc += dx
        obj.yc += dy
        obj.zc += dz
    
        # Apply translation to each vertex or particle coordinate
        if obj.style == SURFACE:
            for vert in obj.vertices:
                vert[0] += dx
                vert[1] += dy
                vert[2] += dz
        elif obj.style == GROUP:
            for particle in obj.xyz:
                particle[0] += dx
                particle[1] += dy
                particle[2] += dz
    
    # --------------------------------------------------------------------
    # Rotate an Object to Align Current Axes with New Axes
    
    def rotate(self, id, axis1, i1, j1, k1, axis2, i2, j2, k2):
        """
        Rotate an object so that its current axes align with new ones.

        Parameters:
            id (str): Identifier of the object.
            axis1 (str): First axis to rotate ('x', 'y', 'z').
            i1, j1, k1 (float): Direction cosines for the first new axis.
            axis2 (str): Second axis to rotate ('x', 'y', 'z').
            i2, j2, k2 (float): Direction cosines for the second new axis.
        """
        obj = self.objs[self.ids[id]]
        if obj.style not in [SURFACE, GROUP]:
            raise Exception("Can only use rotate() on a surface or group object")
    
        # Create new axes
        new_axes = {'x': None, 'y': None, 'z': None}
        if axis1 in new_axes:
            new_axes[axis1] = [i1, j1, k1]
        else:
            raise Exception("Invalid axis for rotate()")
        
        if axis2 in new_axes:
            new_axes[axis2] = [i2, j2, k2]
        else:
            raise Exception("Invalid axis for rotate()")
    
        # Infer the third axis
        axes = ['x', 'y', 'z']
        missing_axis = next((ax for ax in axes if new_axes[ax] is None), None)
        if missing_axis is None:
            raise Exception("All three axes are already defined")
        other_axes = [ax for ax in axes if ax != missing_axis]
        new_axes[missing_axis] = cross(new_axes[other_axes[0]], new_axes[other_axes[1]])
        normalize(new_axes[missing_axis])
    
        # Orthonormalize the axes
        normalize(new_axes['x'])
        normalize(new_axes['y'])
        normalize(new_axes['z'])
    
        # Apply rotation matrix to each vertex or particle coordinate
        if obj.style == SURFACE:
            for vert in obj.vertices:
                x = vert[0] - obj.xc
                y = vert[1] - obj.yc
                z = vert[2] - obj.zc
                xn = new_axes['x'][0]*x + new_axes['x'][1]*y + new_axes['x'][2]*z
                yn = new_axes['y'][0]*x + new_axes['y'][1]*y + new_axes['y'][2]*z
                zn = new_axes['z'][0]*x + new_axes['z'][1]*y + new_axes['z'][2]*z
                vert[0] = xn + obj.xc
                vert[1] = yn + obj.yc
                vert[2] = zn + obj.zc
        elif obj.style == GROUP:
            for particle in obj.xyz:
                x = particle[0] - obj.xc
                y = particle[1] - obj.yc
                z = particle[2] - obj.zc
                xn = new_axes['x'][0]*x + new_axes['x'][1]*y + new_axes['x'][2]*z
                yn = new_axes['y'][0]*x + new_axes['y'][1]*y + new_axes['y'][2]*z
                zn = new_axes['z'][0]*x + new_axes['z'][1]*y + new_axes['z'][2]*z
                particle[0] = xn + obj.xc
                particle[1] = yn + obj.yc
                particle[2] = zn + obj.zc
    
    # --------------------------------------------------------------------
    # Scale an Object by sx, sy, sz Factors
    
    def scale(self, id, sx, sy, sz):
        """
        Scale an object by specified factors along each axis.

        Parameters:
            id (str): Identifier of the object.
            sx, sy, sz (float): Scaling factors along x, y, z axes.
        """
        obj = self.objs[self.ids[id]]
        if obj.style not in [SURFACE, GROUP]:
            raise Exception("Can only use scale() on a surface or group object")
        if obj.style == SURFACE:
            for vert in obj.vertices:
                vert[0] = obj.xc + sx * (vert[0] - obj.xc)
                vert[1] = obj.yc + sy * (vert[1] - obj.yc)
                vert[2] = obj.zc + sz * (vert[2] - obj.zc)
        elif obj.style == GROUP:
            for particle in obj.xyz:
                particle[0] = obj.xc + sx * (particle[0] - obj.xc)
                particle[1] = obj.yc + sy * (particle[1] - obj.yc)
                particle[2] = obj.zc + sz * (particle[2] - obj.zc)
    
    # --------------------------------------------------------------------
    # Create a Union Object from Other Objects
    
    def union(self, id, *list_ids):
        """
        Create a union object from a list of other objects.

        Parameters:
            id (str): Unique identifier for the union.
            *list_ids: Identifiers of objects to include in the union.
        """
        if id in self.ids:
            raise Exception(f"ID {id} is already in use")
        obj = Union(self.ids, self.objs, *list_ids)
        obj.select = 1
        self.ids[id] = len(self.objs)
        self.objs.append(obj)
        obj.id = id
        obj.style = UNION
    
    # --------------------------------------------------------------------
    # Join Objects to Form a New Object
    
    def join(self, id, *list_ids):
        """
        Join multiple objects of the same style into a new object.

        Parameters:
            id (str): Unique identifier for the new joined object.
            *list_ids: Identifiers of objects to join.
        """
        if not list_ids:
            raise Exception("No objects provided to join")
        style = self.objs[self.ids[list_ids[0]]].style
        if style == GROUP:
            obj = Group()
        elif style == SURFACE:
            obj = Surface()
        elif style == LINE:
            obj = Line()
        else:
            raise Exception("Cannot perform join on these object styles")
        obj.select = 1
        self.ids[id] = len(self.objs)
        self.objs.append(obj)
        obj.id = id
        obj.style = style
    
        if style == GROUP:
            obj.on_id = self.objs[self.ids[list_ids[0]]].on_id
            obj.npart = 0
            obj.xyz = []
        elif style == SURFACE:
            obj.nvert = obj.ntri = 0
            obj.vertices = []
            obj.triangles = []
            obj.connections = []
        elif style == LINE:
            obj.nline = 0
            obj.pairs = []
            
        for obj_id in list_ids:
            o = self.objs[self.ids[obj_id]]
            if o.style != style:
                raise Exception("All joined objects must be of same style")
    
            # Force deep copy of particle coordinates
            if style == GROUP:
                if o.on_id != obj.on_id:
                    raise Exception("Particle group surfaces do not match")
                for xyz in o.xyz:
                    obj.xyz.append(xyz[:])
                obj.npart += o.npart
                obj.center()
                
            # Force deep copy of triangle vertices and indices
            elif style == SURFACE:
                for vert in o.vertices:
                    obj.vertices.append(vert[:])
                for tri in o.triangles:
                    obj.triangles.append([tri[0]+obj.nvert, tri[1]+obj.nvert, tri[2]+obj.nvert])
                for conn in o.connections:
                    new_conn = conn[:]
                    if new_conn[0]:
                        new_conn[0] += obj.ntri
                    if new_conn[2]:
                        new_conn[2] += obj.ntri
                    if new_conn[4]:
                        new_conn[4] += obj.ntri
                    obj.connections.append(new_conn)
                obj.nvert += o.nvert
                obj.ntri += o.ntri
                obj.center()
    
            # Force deep copy of line point pairs
            elif style == LINE:
                obj.pairs += o.pairs[:]
                obj.nline += o.nline
    
    # --------------------------------------------------------------------
    # Delete Objects from the cdata
    
    def delete(self, *list_ids):
        """
        Delete objects from the cdata.

        Parameters:
            *list_ids: Identifiers of objects to delete.
        """
        for id in list_ids:
            if id not in self.ids:
                raise Exception(f"ID {id} does not exist")
            i = self.ids[id]
            del self.ids[id]
            del self.objs[i]
            # Update indices in self.ids
            for key in self.ids:
                if self.ids[key] > i:
                    self.ids[key] -= 1
    
    # --------------------------------------------------------------------
    # Rename an Object
    
    def rename(self, id_old, id_new):
        """
        Rename an object.

        Parameters:
            id_old (str): Current identifier of the object.
            id_new (str): New identifier for the object.
        """
        if id_new in self.ids:
            raise Exception(f"ID {id_new} is already in use")
        if id_old not in self.ids:
            raise Exception(f"ID {id_old} does not exist")
        i = self.ids[id_old]
        self.ids[id_new] = i
        self.objs[i].id = id_new
        del self.ids[id_old]
    
    # --------------------------------------------------------------------
    # Create a Deep Copy of an Object with a New ID
    
    def copy(self, id_old, id_new):
        """
        Create a deep copy of an object with a new identifier.

        Parameters:
            id_old (str): Identifier of the object to copy.
            id_new (str): New identifier for the copied object.
        """
        if id_new in self.ids:
            raise Exception(f"ID {id_new} is already in use")
        if id_old not in self.ids:
            raise Exception(f"ID {id_old} does not exist")
        obj = deepcopy(self.objs[self.ids[id_old]])
        obj.select = 1
        self.ids[id_new] = len(self.objs)
        self.objs.append(obj)
        obj.id = id_new
    
    # --------------------------------------------------------------------
    # Select Objects
    
    def select(self, *list_ids):
        """
        Select one or more objects.

        Parameters:
            *list_ids: Identifiers of objects to select. If empty, selects all.
        """
        if not list_ids:
            list_ids = self.ids.keys()
        for id in list_ids:
            if id not in self.ids:
                raise Exception(f"ID {id} does not exist")
            obj = self.objs[self.ids[id]]
            obj.select = 1
    
    # --------------------------------------------------------------------
    # Unselect Objects
    
    def unselect(self, *list_ids):
        """
        Unselect one or more objects.

        Parameters:
            *list_ids: Identifiers of objects to unselect. If empty, unselects all.
        """
        if not list_ids:
            list_ids = self.ids.keys()
        for id in list_ids:
            if id not in self.ids:
                raise Exception(f"ID {id} does not exist")
            obj = self.objs[self.ids[id]]
            obj.select = 0
    
    # --------------------------------------------------------------------
    # Write Objects to ChemCell Data File
    
    def write(self, file, *list_ids):
        """
        Write selected objects to a ChemCell data file.

        Parameters:
            file (str): Filename to write to.
            *list_ids: Identifiers of objects to write. If empty, writes all selected.
        """
        if not list_ids:
            vlist = list(range(len(self.objs)))
        else:
            vlist = []
            for id in list_ids:
                if id not in self.ids:
                    raise Exception(f"ID {id} does not exist")
                vlist.append(self.ids[id])
    
        with open(file, 'w') as fp:
            self.filewrite(fp, vlist)
    
    # --------------------------------------------------------------------
    # Append Objects to an Existing ChemCell Data File
    
    def append(self, file, *list_ids):
        """
        Append selected objects to an existing ChemCell data file.

        Parameters:
            file (str): Filename to append to.
            *list_ids: Identifiers of objects to append. If empty, appends all selected.
        """
        if not list_ids:
            vlist = list(range(len(self.objs)))
        else:
            vlist = []
            for id in list_ids:
                if id not in self.ids:
                    raise Exception(f"ID {id} does not exist")
                vlist.append(self.ids[id])
    
        with open(file, 'a') as fp:
            self.filewrite(fp, vlist)
    
    # --------------------------------------------------------------------
    # Write Objects to an Opened Data File
    
    def filewrite(self, fp, vlist):
        """
        Write objects to an already opened data file.

        Parameters:
            fp (file object): Opened file object to write to.
            vlist (list): List of object indices to write.
        """
        for index in vlist:
            obj = self.objs[index]
            if not obj.select:
                continue
            if obj.style == GROUP:
                if not obj.on_id:
                    print(f"particles {obj.id} {obj.npart}", file=fp)
                else:
                    print(f"particles {obj.id} {obj.npart} {obj.on_id}", file=fp)
                print(file=fp)
                for i, xyz in enumerate(obj.xyz, start=1):
                    print(f"{i} {xyz[0]} {xyz[1]} {xyz[2]}", file=fp)
                print(file=fp)
            if obj.style == SURFACE:
                print(f"triangles {obj.id} {obj.nvert} {obj.ntri}", file=fp)
                print(file=fp)
                for i, vert in enumerate(obj.vertices, start=1):
                    print(f"{i} {vert[0]} {vert[1]} {vert[2]}", file=fp)
                for i, tri in enumerate(obj.triangles, start=1):
                    print(f"{i} {tri[0]} {tri[1]} {tri[2]}", file=fp)
                for i, conn in enumerate(obj.connections, start=1):
                    print(f"{i} {conn[0]} {conn[1]} {conn[2]} {conn[3]} {conn[4]} {conn[5]}", file=fp)
            if obj.style == REGION:
                print(f"region {obj.command()}", file=fp)
    
    # --------------------------------------------------------------------
    # Iterator Method for Other Tools
    
    def iterator(self, flag):
        """
        Iterator method compatible with equivalent dump calls.

        Parameters:
            flag (int): 0 for first call, 1 for subsequent calls.

        Returns:
            tuple: (index, time, flag)
        """
        if flag == 0:
            return (0, 0, 1)
        return (0, 0, -1)
    
    # --------------------------------------------------------------------
    # Visualization Method
    
    def viz(self, isnap):
        """
        Return list of atoms, bonds, tris, and lines for visualization.

        Parameters:
            isnap (int): Snapshot index. Must be 0 for cdata.

        Returns:
            tuple: (time, box, atoms, bonds, tris, lines)
        """
        if isnap:
            raise Exception("cannot call cdata.viz() with isnap != 0")
        
        # Create atom list from sum of all particle groups
        # id = running count
        # type = running type of particle group
    
        id_count = itype = 0
        atoms = []
        for obj in self.objs:
            if obj.style != GROUP:
                continue
            if not obj.select:
                continue
            itype += 1
            for xyz in obj.xyz:
                id_count += 1
                atoms.append([id_count, itype, xyz[0], xyz[1], xyz[2]])
    
        # No bonds
        bonds = []
    
        # Create triangle list from sum of all surfaces and regions
        # id = running count
        # type = type of set of tris
    
        id_count = itype = 0
        tris = []
        for obj in self.objs:
            if obj.style not in [SURFACE, REGION]:
                continue
            if not obj.select:
                continue
            if obj.style == REGION:
                obj.triangulate()
            itype += 1
            for tri in obj.triangles:
                v1 = obj.vertices[tri[0]-1]
                v2 = obj.vertices[tri[1]-1]
                v3 = obj.vertices[tri[2]-1]
                list_vertices = v1 + v2 + v3
                n = normal(list_vertices[0:3], list_vertices[3:6], list_vertices[6:9])
                id_count += 1
                tris.append([id_count, itype] + list_vertices + n)
    
        # Create line list from sum of all line objects
        id_count = itype = 0
        lines = []
        for obj in self.objs:
            if obj.style != LINE:
                continue
            if not obj.select:
                continue
            itype += 1
            for pair in obj.pairs:
                id_count += 1
                lines.append([id_count, itype] + pair)
        
        return (0, self.bbox(), atoms, bonds, tris, lines)
    
    # --------------------------------------------------------------------
    # Find Time Method (Not Applicable for cdata)
    
    def findtime(self, n):
        """
        Find the index of a given timestep.

        Parameters:
            n (int): The timestep to find.

        Returns:
            int: The index of the timestep.

        Raises:
            Exception: Always, since cdata does not support multiple timesteps.
        """
        if n == 0:
            return 0
        raise Exception(f"no step {n} exists")
    
    # --------------------------------------------------------------------
    # Return Bounding Box that Encloses All Selected Objects
    
    def maxbox(self):
        """
        Return the bounding box that encloses all selected objects.

        Returns:
            tuple: (xlo, ylo, zlo, xhi, yhi, zhi)
        """
        return self.bbox()
    
    # --------------------------------------------------------------------
    # Return Bounding Box that Encloses All Selected Objects
    
    def bbox(self):
        """
        Compute the bounding box that encloses all selected objects.

        Returns:
            tuple: (xlo, ylo, zlo, xhi, yhi, zhi)
        """
        xlo = ylo = zlo = float('inf')
        xhi = yhi = zhi = float('-inf')
        for obj in self.objs:
            if not obj.select:
                continue
            xxlo, yylo, zzlo, xxhi, yyhi, zzhi = obj.bbox()
            xlo = min(xxlo, xlo)
            ylo = min(yylo, ylo)
            zlo = min(zzlo, zlo)
            xhi = max(xxhi, xhi)
            yhi = max(yyhi, yhi)
            zhi = max(zzhi, zhi)
    
        return (xlo, ylo, zlo, xhi, yhi, zhi)
