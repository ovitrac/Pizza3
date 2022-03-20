# -*- coding: utf-8 -*-

"""
    RASTER method to generate LAMMPS input files (in 2D for this version)
    
    Generate a raster area
        R = raster()
        R = raster(width=200, height=200, dpi=300)
        
    Set objects (rectangle, circle, triangle, diamond...)
        R.rectangle(1,24,2,20,name='rect1')
        R.rectangle(60,80,50,81,name='rect2',beadtype=2,angle=40)
        R.rectangle(50,50,10,10,mode="center",angle=45,beadtype=1)
        R.circle(45,20,5,name='C1',beadtype=3)
        R.circle(35,10,5,name='C2',beadtype=3)
        
        R.circle(15,30,10,name='p1',beadtype=4,shaperatio=0.2,angle=-30)
        R.circle(12,40,8,name='p2',beadtype=4,shaperatio=0.2,angle=20)
        R.circle(12,80,22,name='p3',beadtype=4,shaperatio=1.3,angle=20)
        
        R.triangle(85,20,10,name='T1',beadtype=5,angle=20)
        R.diamond(85,35,5,name='D1',beadtype=5,angle=20)
        R.pentagon(50,35,5,name='P1',beadtype=5,angle=90)
        R.hexagon(47,85,12,name='H1',beadtype=5,angle=90)

    List simple objects
        R.list()
        R.get("p1")
        R.p1
        R.C1
        
    List objects in a collection
        R.C1.get("p1") 
        R.C1.p1 shows the object p1 in the collection C1

    Build objects and show them 
        R.plot()
        R.show()
        
    Show and manage labels
        R.show(extra="label",contour=True)
        R.label("rect003")
        R.unlabel('rect1')
        
    Manage objects, update and show
    
    Get the image and convert the image to text
        I = R.numeric()
        T = R.string()
        R.print()
        
    Create a pizza.dump3.dump object
        X = R.data()
        X=R.data(scale=(1,1),center=(0,0))
        X.write("/tmp/myfile")
        
    More advanced features enable object copy, duplication along a path
    Contruction of scattered particles
    See: copyalongpath(), scatter(), emulsion()
    
    Examples follow in the __main__ section
        
"""

# INRAE\Olivier Vitrac - rev. 2022-02-13
# contact: olivier.vitrac@agroparistech.fr

# History
# 2022-02-05 first alpha version
# 2022-02-06 RC for 2D
# 2022-02-08 add count(), update the display method
# 2022-02-10 add figure(), newfigure(), count()
# 2022-02-11 improve display, add data()
# 2022-02-12 major release, fully compatible with pizza.data3.data
# 2022-02-13 the example (<F5>) has been modified R.plot() should precedes R.list()
# 2022-02-28 update write files for SMD, add scale and center to R.data()
# 2022-03-02 fix data(): xlo and ylow (beads should not overlap the boundary), scale radii, volumes
# 2022-03-20 major update, add collection, duplication, translation, scatter, emulsion

# %% Imports and private library
from copy import copy as duplicate
from copy import deepcopy as deepduplicate
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as path
import matplotlib.patches as patches
from pizza.data3 import data as data3
from pizza.private.struct import struct

def _rotate(x0,y0,xc,yc,angle):
    angle = np.pi * angle / 180.0
    x1 = (x0 - xc)*np.cos(angle) - (y0 - yc)*np.sin(angle) + xc
    y1 = (x0 - xc)*np.sin(angle) + (y0 - yc)*np.cos(angle) + yc
    return x1, y1

def _extents(f):
    halftick = ( f[1] - f[0] ) / 2
    return [f[0] - halftick, f[-1] + halftick]

# wrapper of imagesc (note that the origin is bottom left)
# usage: data = np.random.randn(5,10)
#        imagesc(data)
def imagesc(im,x=None,y=None):
    if x==None: x=np.arange(1,np.shape(im)[1]+1)
    if y==None: y=np.arange(1,np.shape(im)[0]+1)
    plt.imshow(im, extent=_extents(x) + _extents(y), 
               aspect="auto", origin="lower", interpolation="none")

# helper for parametric functions
def linear(xmin=10,ymin=10,xmax=80,ymax=80,n=5):
    """ XY = linear(xmin,ymin,xmax,ymax,n) """
    return np.linspace(xmin,xmax,n), np.linspace(ymin,ymax,n)

# %% raster class
class raster:
    """ raster class for LAMMPS SMD 
    
    Constructor
    
        R = raster(width=100,height=100...)

        Extra properties
            dpi, fontsize
        
        additional properties for R.data()
            scale, center : full scaling
            mass, volume, radius, contactradius, velocities, forces: bead scaling
            filename
        
        List of available properties: default values
        
                   name: "default raster"
                  width: 100
                 height: 100
                    dpi: 200
               fontsize: 10
                   mass: 1
                 volume: 1
                 radius: 1.5
          contactradius: 0.5
             velocities: [0, 0, 0]
                 forces: [0, 0, 0]
               filename: ["%dx%d raster (%s)" % (self.width,self.height,self.name)]
    
    Graphical objects
        
        R.rectangle(xleft,xright,ybottom,ytop [, beadtype=1,mode="lower", angle=0, ismask=False])
        R.rectangle(xcenter,ycenter,width,height [, beadtype=1,mode="center", angle=0, ismask=False])
        R.circle(xcenter,ycenter,radius [, beadtype=1,shaperatio=1, angle=0, ismask=False], resolution=20, shiftangle=0)
        R.triangle(...)
        R.diamond(...)
        R.pentagon(...)
        R.hexagon(...)
        
        note: use fake=True to generate an object without inserting it
        
        R.collection(...) generates collection of existing or fake objects
        R.object.copy(...) enables to copy an object
        
    Display methods (precedence affects the result)
        R.plot()
        R.show(), R.show(extra="label",contour=True,what="beadtype" or "objindex")
        R.show(extra="labels")
        R.list()
        R.get("object")
        R.print()
        R.label("object")
        R.unlabel("object")
        R.figure()
        R.newfigure(dpi=300)
        
        R.numeric()
        R.string(), R.string(what="beadtype" or "objindex"))
        R.names()
        R.print()
        
    Clear and delete
        R.clear()
        R.clear("all")
        R.delete("object")

    Copy objects
        R.copyalongpath(....)
        R.scatter()

    Generate an input data object
        X = R.data() or X=R.data(scale=(1,1),center=(0,0))
        X.write("/tmp/myfile")
    
    """
    
    # CONSTRUCTOR ---------------------------- 
    def __init__(self,
                 # raster properties
                 name="default raster",
                 width=100,
                 height=100,
                 # printing and display
                 dpi=200,
                 fontsize=10,
                 # for data conversion
                 mass=1,
                 volume=1,
                 radius=1.5,
                 contactradius=0.5,
                 velocities=[0,0,0],
                 forces=[0,0,0],
                 filename=""
                 ):
        
        """ initialize raster """
        self.name = name
        self.width = width
        self.height = height
        self.xcenter= width/2
        self.ycenter = height/2
        self.objects = {}
        self.nobjects = 0    # total number of objects (alive)
        self.nbeads = 0
        self.counter = { "triangle":0,
                          "diamond":0,
                        "rectangle":0,
                         "pentagon":0,
                          "hexagon":0,
                           "circle":0,
                       "collection":0,
                              "all":0
                    }
        self.fontsize = 10   # font size for labels
        self.imbead = np.zeros((height,width),dtype=np.int8)
        self.imobj = np.zeros((height,width),dtype=np.int8)
        self.hfig = [] # figure handle
        self.dpi = dpi
        # generic SMD properties (to be rescaled)
        self.volume = volume
        self.mass = mass
        self.radius = radius
        self.contactradius = contactradius
        self.velocities = velocities
        self.forces =forces
        
        if filename == "":
            self.filename = ["%dx%d raster (%s)" % (self.width,self.height,self.name)]
        else:
            self.filename = filename
        

    # DATA ---------------------------- 
    def data(self,scale=(1,1),center=(0,0)):
        """
        data(scale=(scalex,scaley),center=(centerx,centery))
        return a pizza.data object  """
        if not isinstance(scale,tuple) or len(scale)!=2:
            raise ValueError("scale must be tuple (scalex,scaley)")
        if not isinstance(center,tuple) or len(scale)!=2:
            raise ValueError("center must be tuple (centerx,centery)")
        scalez = np.sqrt(scale[0]*scale[1])
        scalevol = scale[0]*scale[1]*scalez
        n = self.length()
        i,j = self.imbead.nonzero() # x=j+0.5 y=i+0.5
        X = data3()  # empty pizza.data3.data object
        X.title = self.name + "(raster)"
        X.headers = {'atoms': n,
                      'atom types': self.count()[-1][0],
                      'xlo xhi': ((0.0-center[0])*scale[0], (self.width-0.0-center[0])*scale[0]),
                      'ylo yhi': ((0.0-center[1])*scale[1], (self.height-0.0-center[1])*scale[1]),
                      'zlo zhi': (0, scalez)}
        # [ATOMS] section
        X.append('Atoms',list(range(1,n+1)),True,"id")       # id
        X.append('Atoms',self.imbead[i,j],True,"type")       # Type
        X.append('Atoms',1,True,"mol")                       # mol
        X.append('Atoms',self.volume*scalevol,False,"c_vol") # c_vol
        X.append('Atoms',self.mass*scalevol,False,"mass")    # mass
        X.append('Atoms',self.radius*scalez,False,"radius")         # radius
        X.append('Atoms',self.contactradius*scalez,False,"c_contact_radius") # c_contact_radius
        X.append('Atoms',(j+0.5-center[0])*scale[0],False,"x")        # x
        X.append('Atoms',(i+0.5-center[1])*scale[1],False,"y")        # y
        X.append('Atoms',0,False,"z")                                 # z
        X.append('Atoms',(j+0.5-center[0])*scale[0],False,"x0")       # x0
        X.append('Atoms',(i+0.5-center[1])*scale[1],False,"y0")       # y0
        X.append('Atoms',0,False,"z0")                                # z0
        # [VELOCITIES] section
        X.append('Velocities',list(range(1,n+1)),True,"id") # id
        X.append('Velocities',self.velocities[0],False,"vx") # vx
        X.append('Velocities',self.velocities[1],False,"vy") # vy
        X.append('Velocities',self.velocities[2],False,"vz") # vz
        # pseudo-filename        
        X.flist = self.filename
        return X
     
    # LENGTH ---------------------------- 
    def length(self,t=None,what="beadtype"):
        """ returns the total number of beads length(type,"beadtype") """
        if what == "beadtype":
            num = self.imbead
        elif what == "objindex":
            num = self.imobj
        else:
            raise ValueError('"beadtype" and "objindex" are the only acceptable values')
        if t==None:
            return np.count_nonzero(num>0)
        else:
            return np.count_nonzero(num==t)
        
    # NUMERIC ---------------------------- 
    def numeric(self):
        """ retrieve the image as a numpy.array """
        return self.imbead, self.imobj

    # STRING ---------------------------- 
    def string(self,what="beadtype"):
        """ convert the image as ASCII strings """
        if what == "beadtype":
            num = np.flipud(duplicate(self.imbead))
        elif what == "objindex":
            num = np.flipud(duplicate(self.imobj))
        else:
            raise ValueError('"beadtype" and "objindex" are the only acceptable values')
        num[num>0] = num[num>0] + 65
        num[num==0] = 32
        num = list(num)
        return ["".join(map(chr,x)) for x in num]
        
    # GET -----------------------------
    def get(self,name):
        """ returns the object """
        if name in self.objects:
            return self.objects[name]
        else:
            raise ValueError('the object "%s" does not exist, use list()' % name)

    # GETATTR --------------------------
    def __getattr__(self,key):
        """ get attribute override """
        return self.get(key)
        
    # CLEAR ---------------------------- 
    def clear(self,what="nothing"):
        """ clear the plotting area, use clear("all")) to remove all objects """
        self.imbead = np.zeros((self.height,self.width),dtype=np.int8)
        self.imobj = np.zeros((self.height,self.width),dtype=np.int8)
        for o in self.names():
            if what=="all":
                self.delete(o)
            else:
                self.objects[o].isplotted = False
                self.objects[o].islabelled = False
                if not self.objects[o].ismask:
                    self.nbeads -= self.objects[o].nbeads
                self.objects[o].nbeads = 0  # number of beads (plotted)
        self.figure()
        plt.cla()
        self.show()

    # DISP method ---------------------------- 
    def __repr__(self):
        """ display method """
        ctyp = self.count() # count objects (not beads)
        print("-"*40)
        print('RASTER area "%s" with %d objects' % (self.name,self.nobjects))
        print("-"*40)
        print("<- grid size ->")
        print("\twidth: %d" % self.width)
        print("\theight: %d" % self.height)
        print("<- bead types ->")
        nbt = 0
        if len(ctyp):
            for i,c in enumerate(ctyp):
                nb = self.length(c[0])
                nbt += nb
                print("\t type=%d (%d objects, %d beads)" % (c[0],c[1],nb))
        else:
            print("\tno bead assigned")
        print("-"*40)
        return "RASTER AREA %d x %d with %d objects (%d types, %d beads)." % \
        (self.width,self.height,self.nobjects,len(ctyp),nbt)

    # count method ---------------------------- 
    def count(self):
        """ count objects by type """
        typlist = []
        for  o in self.names():
            if isinstance(self.objects[o].beadtype,list):
                typlist += self.objects[o].beadtype
            else:
                typlist.append(self.objects[o].beadtype)
        utypes = list(set(typlist))
        c = []
        for t in utypes:
            c.append((t,typlist.count(t)))
        return c

    # NAMES method ---------------------------- 
    def names(self):
        """ return the names of objects sorted as index """
        namesunsorted=namessorted=list(self.objects.keys())
        nobj = len(namesunsorted)
        for iobj in range(nobj):
            namessorted[self.objects[namesunsorted[iobj]].index-1] = namesunsorted[iobj]
        return namessorted
        
    # LIST method ---------------------------- 
    def list(self):
        """ list objects """
        fmt = "%%%ss:" % max(10,max([len(n) for n in self.names()])+2)
        print("RASTER with %d objects" % self.nobjects)
        for o in self.objects.keys():
            print(fmt % self.objects[o].name,"%-10s" % self.objects[o].kind,
                  "(beadtype=%d,object index=[%d,%d], n=%d)" % \
                      (self.objects[o].beadtype,
                       self.objects[o].index,
                       self.objects[o].subindex,
                       self.objects[o].nbeads))
            
    # EXIST method ---------------------------- 
    def exist(self,name):
        """ exist object """
        return name in self.objects
    
    # DELETE method ---------------------------- 
    def delete(self,name):
        """ delete object """
        if name in self.objects: 
            if not self.objects[name].ismask:
                self.nbeads -= self.objects[name].nbeads
            del self.objects[name]
            self.nobjects -= 1
        else:
            raise ValueError("%d is not a valid name (use list()) to list valid objects" % name)
        self.clear()
        self.plot()
        self.show(extra="label")
        
    # VALID method
    def valid(self,x,y):
        """ validation of coordinates """
        return min(self.width,max(0,round(x))),min(self.height,max(0,round(y)))
    
    # frameobj method
    def frameobj(self,obj):
        """ frame coordinates by taking into account translation """
        xmin, ymin = self.valid(obj.xmin-1, obj.ymin-1)
        xmax, ymax = self.valid(obj.xmax+1, obj.ymax+1)
        return xmin, ymin, xmax, ymax

    # RECTANGLE ----------------------------     
    def rectangle(self,a,b,c,d,
                  mode="lowerleft",name=None,angle=0,
                  beadtype=None,ismask=False,fake=False):
        """ 
        rectangle object
            rectangle(xleft,xright,ybottom,ytop [, beadtype=1,mode="lower", angle=0, ismask=False])
            rectangle(xcenter,ycenter,width,height [, beadtype=1,mode="center", angle=0, ismask=False])
        """
        # object creation
        self.counter["all"] += 1
        self.counter["rectangle"] += 1
        R = Rectangle((self.counter["all"],self.counter["rectangle"]))
        if name != None:
            if self.exist(name):
                print('RASTER:: the object "%s" is overwritten',name)
                self.delete(name)
            R.name = name
        else:
            name = R.name
        if beadtype != None: R.beadtype = int(np.floor(beadtype))
        if ismask: R.beadtype = 0
        R.ismask = R.beadtype==0
        # build vertices
        if mode == "lowerleft":
            R.xcenter0 = (a+b)/2
            R.ycenter0 = (c+d)/2
            R.vertices = [
                _rotate(a,c,R.xcenter0,R.ycenter0,angle),
                _rotate(b,c,R.xcenter0,R.ycenter0,angle),
                _rotate(b,d,R.xcenter0,R.ycenter0,angle),
                _rotate(a,d,R.xcenter0,R.ycenter0,angle),
                _rotate(a,c,R.xcenter0,R.ycenter0,angle)
                ] # anti-clockwise, closed (last point repeated)
        elif mode == "center":
            R.xcenter0 = a
            R.ycenter0 = b
            R.vertices = [
                _rotate(a-c/2,b-d/2,R.xcenter0,R.ycenter0,angle),
                _rotate(a+c/2,b-d/2,R.xcenter0,R.ycenter0,angle),
                _rotate(a+c/2,b+d/2,R.xcenter0,R.ycenter0,angle),
                _rotate(a-c/2,b+d/2,R.xcenter0,R.ycenter0,angle),
                _rotate(a-c/2,b-d/2,R.xcenter0,R.ycenter0,angle)
                ]
        else:
            raise ValueError('"%s" is not a recognized mode, use "lowerleft" (default) and "center" instead')
        # build path object and range
        R.codes =    [ path.Path.MOVETO,
                     path.Path.LINETO,
                     path.Path.LINETO,
                     path.Path.LINETO,
                     path.Path.CLOSEPOLY
                    ]
        R.nvertices = len(R.vertices)-1
        R.xmin0, R.ymin0, R.xmax0, R.ymax0 = R.corners()        
        R.xmin0, R.ymin0 = self.valid(R.xmin0,R.ymin0)
        R.xmax0, R.ymax0 = self.valid(R.xmax0,R.ymax0)
        R.angle = angle
        # store the object (if not fake)
        if fake:
            self.counter["all"] -= 1
            self.counter["rectangle"] -= 1
            return R
        else:
            self.objects[name] = R
            self.nobjects += 1
            return None

        
    # CIRCLE ----------------------------     
    def circle(self,xc,yc,radius,
                  name=None,shaperatio=1,angle=0,beadtype=None,ismask=False,
                  resolution=20,shiftangle=0,fake=False):
        """ 
        circle object (or any regular polygon)
            circle(xcenter,ycenter,radius [, beadtype=1,shaperatio=1, angle=0, ismask=False], resolution=20, shiftangle=0)
        """
        # object creation
        self.counter["all"] += 1
        if resolution==3:
            typ = "triangle"
            self.counter["triangle"] += 1
            G = Triangle((self.counter["all"],self.counter["triangle"]))
        elif resolution==4:
            typ = "diamond"
            self.counter["diamond"] += 1
            G = Diamond((self.counter["all"],self.counter["diamond"]))
        elif resolution==5:
            typ = "pentagon"
            self.counter["pentagon"] += 1
            G = Pentagon((self.counter["all"],self.counter["pentagon"]))
        elif resolution==6:
            typ = "hexagon"
            self.counter["hexagon"] += 1
            G = Hexagon((self.counter["all"],self.counter["hexagon"]))
        else:
            typ = "circle"
            self.counter["circle"] += 1
            G = Circle((self.counter["all"],self.counter["circle"]),resolution=resolution)
        if name != None:
            if self.exist(name):
                print('RASTER:: the object "%s" is overwritten',name)
                self.delete(name)
            G.name = name
        else:
            name = G.name
        if beadtype != None: G.beadtype = int(np.floor(beadtype))
        if ismask: G.beadtype = 0
        G.ismask = G.beadtype==0
        # build vertices
        th = np.linspace(0,2*np.pi,G.resolution+1) +shiftangle*np.pi/180
        xgen = xc + radius * np.cos(th)
        ygen = yc + radius * shaperatio * np.sin(th)
        G.xcenter0, G.ycenter0, G.radius = xc, yc, radius
        G.vertices, G.codes = [], []
        for i in range(G.resolution+1):
            G.vertices.append(_rotate(xgen[i],ygen[i],xc,yc,angle))
            if i==0:
                G.codes.append(path.Path.MOVETO)
            elif i==G.resolution:
                G.codes.append(path.Path.CLOSEPOLY)        
            else:
                G.codes.append(path.Path.LINETO)
        G.nvertices = len(G.vertices)-1
        # build path object and range
        G.xmin0, G.ymin0, G.xmax0, G.ymax0 = G.corners()
        G.xmin0, G.ymin0 = self.valid(G.xmin0,G.ymin0)
        G.xmax0, G.ymax0 = self.valid(G.xmax0,G.ymax0)
        G.angle, G.shaperatio = angle, shaperatio
        # store the object
        if fake:
            self.counter["all"] -= 1
            self.counter[typ] -= 1
            return G
        else:
            self.objects[name] = G
            self.nobjects += 1
            return None
 
    
    # COLLECTION ----------------------------
    def collection(self,*obj,
                   name=None,
                   beadtype=None,
                   ismask=None,
                   translate = [0.0,0.0],
                   fake = False,
                   **kwobj):
        """
            collection of objects:
                collection(draftraster,name="mycollect" [,beadtype=1,ismask=True]
                collection(name="mycollect",newobjname1 = obj1, newobjname2 = obj2...)
        """ 
        self.counter["all"] += 1
        self.counter["collection"] += 1
        C = Collection((self.counter["all"],self.counter["collection"]))
        # name
        if name != None:
            if self.exist(name):
                print('RASTER:: the object "%s" is overwritten',name)
                self.delete(name)
            C.name = name
        else:
            name = C.name
        # build the collection
        C.collection = collection(*obj,**kwobj)
        xmin = ymin = +1e99
        xmax = ymax = -1e99
        # apply modifications (beadtype, ismask)
        for o in C.collection.keys():
            tmp = C.collection.getattr(o)
            tmp.translate[0] += translate[0]
            tmp.translate[1] += translate[1]
            xmin, xmax = min(xmin,tmp.xmin), max(xmax,tmp.xmax)
            ymin, ymax = min(ymin,tmp.ymin), max(ymax,tmp.ymax)
            if beadtype != None: tmp.beadtype = beadtype
            if ismask != None: tmp.ismask = ismask
            C.collection.setattr(o,tmp)
        C.xmin, C.xmax, C.ymin, C.ymax = xmin, xmax, ymin, ymax
        C.width, C.height = xmax-xmin, ymax-ymin
        if fake:
            return C
        else:
            self.objects[name] = C
            self.nobjects += 1
            return None
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # =========== pseudo methods connected to circle() ===========
    # TRIANGLE, DIAMOND, PENTAGON, HEXAGON, -----------------------     
    def triangle(self,xc,yc,radius,name=None,
                 shaperatio=1,angle=0,beadtype=None,ismask=False,shiftangle=0,fake=False):
        """
        triangle object 
            triangle(xcenter,ycenter,radius [, beadtype=1,shaperatio=1, angle=0, ismask=False]
        """
        self.circle(xc,yc,radius,name=name,shaperatio=shaperatio,resolution=3,
           angle=angle,beadtype=beadtype,ismask=ismask,shiftangle=0,fake=fake)
        
    def diamond(self,xc,yc,radius,name=None,
                 shaperatio=1,angle=0,beadtype=None,ismask=False,shiftangle=0,fake=False):
        """
        diamond object 
            diamond(xcenter,ycenter,radius [, beadtype=1,shaperatio=1, angle=0, ismask=False]
        """
        self.circle(xc,yc,radius,name=name,shaperatio=shaperatio,resolution=4,
            angle=angle,beadtype=beadtype,ismask=ismask,shiftangle=0,fake=fake)
        
    def pentagon(self,xc,yc,radius,name=None,
                 shaperatio=1,angle=0,beadtype=None,ismask=False,shiftangle=0,fake=False):
        """
        pentagon object 
            pentagon(xcenter,ycenter,radius [, beadtype=1,shaperatio=1, angle=0, ismask=False]
        """
        self.circle(xc,yc,radius,name=name,shaperatio=shaperatio,resolution=5,
            angle=angle,beadtype=beadtype,ismask=ismask,shiftangle=0,fake=fake)
        
    def hexagon(self,xc,yc,radius,name=None,
                 shaperatio=1,angle=0,beadtype=None,ismask=False,shiftangle=0,fake=False):
        """
        hexagon object 
            hexagon(xcenter,ycenter,radius [, beadtype=1,shaperatio=1, angle=0, ismask=False]
        """
        self.circle(xc,yc,radius,name=name,shaperatio=shaperatio,resolution=6,
            angle=angle,beadtype=beadtype,ismask=ismask,shiftangle=0,fake=fake)
        
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # label method ---------------------------- 
    def label(self,name,**fmt):
        """
            label:
                label(name [, contour=True,edgecolor="orange",facecolor="none",linewidth=2, ax=plt.gca()])
        """
        self.figure()
        if name in self.objects:
            if not self.objects[name].islabelled:
                if self.objects[name].alike == "mixed":
                    for o in self.objects[name].collection:
                        self.labelobj(o,**fmt)
                else:
                    self.labelobj(self.objects[name],**fmt)
                plt.show()
                self.objects[name].islabelled = True
        else:
            raise ValueError("%d is not a valid name (use list()) to list valid objects" % name)
            
    # label object method -----------------------------
    def labelobj(self,obj,contour=True,edgecolor="orange",facecolor="none",linewidth=2,ax=plt.gca()):
        """
            labelobj:
                labelobj(obj [, contour=True,edgecolor="orange",facecolor="none",linewidth=2, ax=plt.gca()])
        """
        if contour:
            patch = patches.PathPatch(obj.polygon2plot,
                                      facecolor=facecolor,
                                      edgecolor=edgecolor,
                                      lw=linewidth)
            obj.hlabel["contour"] = ax.add_patch(patch)
        else:
            obj.hlabel["contour"] = None
        obj.hlabel["text"] = \
        plt.text(obj.xcenter,
                 obj.ycenter,
                 "%s\n(t=$%d$,$n_p$=%d)" % (obj.name, obj.beadtype,obj.nbeads),
                 horizontalalignment = "center",
                 verticalalignment = "center_baseline",
                 fontsize=self.fontsize
                 )
        
   
    def unlabel(self,name):
        """ unlabel """
        if name in self.objects:
            if  self.objects[name].islabelled:
                self.objects[name].hlabel["contour"].remove()
                self.objects[name].hlabel["text"].remove()
                self.objects[name].hlabel = {'contour':[], 'text':[]}
                self.objects[name].islabelled = False
        else:
            raise ValueError("%d is not a valid name (use list()) to list valid objects" % name)
        

    # PLOT method ---------------------------- 
    def plot(self):
        """ plot """
        for o in self.objects:
            if not self.objects[o].isplotted:
                if self.objects[o].alike == "mixed":
                    for o2 in self.objects[o].collection:
                        self.plotobj(o2)    
                else:
                    self.plotobj(self.objects[o])
                # store it as plotted
                self.objects[o].isplotted = True
                if not self.objects[o].ismask:
                    self.nbeads += self.objects[o].nbeads


    # PLOTobj method (static) -----------------------
    def plotobj(self,obj):
        """ plotobj(obj) """
        if obj.alike == "circle":
            xmin, ymin, xmax, ymax = self.frameobj(obj)
            j,i = np.meshgrid(range(xmin,xmax), range(ymin,ymax))
            points = np.vstack((j.flatten(),i.flatten())).T
            npoints = points.shape[0]
            inside = obj.polygon.contains_points(points)
            for k in range(npoints):
                if inside[k] and \
                    points[k,0]>=0 and \
                    points[k,0]<self.width and \
                    points[k,1]>=0 and \
                    points[k,1]<self.height :
                        self.imbead[points[k,1],points[k,0]] = obj.beadtype
                        self.imobj[points[k,1],points[k,0]] = obj.index
                        obj.nbeads += 1
        else:
            raise ValueError("This object type is notimplemented")        

    # SHOW method ---------------------------- 
    def show(self,extra="none",contour=True,what="beadtype"):
        """ show method: show(extra="label",contour=True,what="beadtype") """
        self.figure()
        if what=="beadtype":
            imagesc(self.imbead)
        elif what == "objindex":
            imagesc(self.imobj)
        else:
            raise ValueError('"beadtype" and "objindex" are the only acceptable values')        
        if extra == "label":
            ax = plt.gca()
            for o in self.names():
                if not self.objects[o].ismask:
                    self.label(o,ax=ax,contour=contour)
            ax.set_title("raster area: %s \n (n=%d, $n_p$=%d)" %\
                      (self.name,self.length(),self.nbeads) )
            plt.show()
            
    # SHOW method ---------------------------- 
    def print(self,what="beadtype"):
        """ print method """
        txt = self.string(what=what)
        for i in range(len(txt)):
            print(txt[i],end="\n")
         
            
    # FIGURE method ---------------------------- 
    def figure(self):
        """ set the current figure """
        if self.hfig==[] or not plt.fignum_exists(self.hfig.number):
            self.newfigure()
        plt.figure(self.hfig.number)
    
    # NEWFIGURE method ---------------------------- 
    def newfigure(self):
        """ create a new figure (dpi=200) """
        self.hfig = plt.figure(dpi=self.dpi)
        
    # COPY OBJECT ALONG a contour -----------------
    def copyalongpath(self,obj,
                      name="path",
                  beadtype=None,
                      path=linear,
                      xmin=10,
                      ymin=10,
                      xmax=70,
                      ymax=90,
                         n=7):
        """
        
        The method enable to copy an existing object (from the current raster,
        from another raster or a fake object) amp,g 
        
        Parameters
        ----------
        obj : real or fake object
            the object to be copied.
        name : string, optional
            the name of the object collection. The default is "path".
        beadtype : integet, optional
            type of bead (can override existing value). The default is None.
        path : function, optional
            parametric function returning x,y. The default is linear.
            x is between xmin and xmax, and y between ymin, ymax
        xmin : int64 or float, optional
            left x corner position. The default is 10.
        ymin : int64 or float, optional
            bottom y corner position. The default is 10.
        xmax : int64 or float, optional
            right x corner position. The default is 70.
        ymax : int64 or float, optional
            top y corner position. The default is 90.
        n : integet, optional
            number of copies. The default is 7.

        Returns
        -------
        None.

        """
        x,y = path(xmin=xmin,ymin=ymin,xmax=xmax,ymax=ymax,n=n)
        btyp = obj.beadtype if beadtype == None else beadtype
        collect = {}
        for i in range(n):
            nameobj = "%s_%s_%02d" % (name,obj.name,i)
            x[i], y[i] = self.valid(x[i], y[i])
            translate = [ x[i]-obj.xcenter, y[i]-obj.ycenter ]
            collect[nameobj] = obj.copy(translate=translate,
                                        name=nameobj,
                                        beadtype=btyp)
        self.collection(**collect,name=name)
     

    # SCATTER -------------------------------
    def scatter(self,
                 E,
                 name="emulsion",
                 beadtype=1,
                 ismask = False
                 ):
        """
        

        Parameters
        ----------
        E : scatter or emulsion object
            codes for x,y and r.
        name : string, optional
            name of the collection. The default is "emulsion".
        beadtype : integer, optional
            for all objects. The default is 1.
        ismask : logical, optional
            Set it to true to force a mask. The default is False.

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
                nameobj = "glob%02d" % i
                collect[nameobj] = self.circle(E.x[i],E.y[i],E.r[i],
                            name=nameobj,beadtype=beadtype,ismask=ismask,fake=True)
            self.collection(**collect,name=name)
        else:
            raise TypeError("the first argument must be an emulsion object")
            
            
# %% PRIVATE SUB-CLASSES
# Use the equivalent methods of raster() to call these constructors
#   raster.rectangle, raster.circle, raster.triangle... raster.collection
#
# Two counters are used for automatic naming
#   counter[0] is the overall index (total number of objects created)
#   counter[1] is the index of objects of this type (total number of objects created for this class)
#
#   Overview:
#       genericpolygon --> Rectancle, Circle
#       Circle --> Triangle, Diamond, Pentagon, Hexagon
#       Collection --> graphical object for collections (many properties are dynamic)
#       struct --> collection is the low-level class container of Collection

class genericpolygon:
    """ generic polygon methods """
    
    @property
    def xcenter(self):
        """ xcenter with translate """
        return self.xcenter0 + self.translate[0]
    @property
    def ycenter(self):
        """ xcenter with translate """
        return self.ycenter0 + self.translate[1]
    @property
    def xmin(self):
        """ xleft position """
        return self.xmin0 + self.translate[0]
    @property
    def xmax(self):
        """ xright position """
        return self.xmax0 + self.translate[0]
    @property
    def ymin(self):
        """ yleft position """
        return self.ymin0 + self.translate[1]
    @property
    def ymax(self):
        """ yright position """
        return self.ymax0 + self.translate[1]
    @property
    def width(self):
        """ oibject width range """
        return self.xmax - self.xmin
    @property
    def height(self):
        """ oibject height range """
        return self.ymax - self.ymin

    @property
    def polygon(self):
        """ 
        R.polygon = path.Path(R.vertices,R.codes,closed=True)
        """
        v = self.vertices
        if self.translate != None:
            vtmp = list(map(list,zip(*v)))
            for i in range(len(vtmp[0])):
                vtmp[0][i] += self.translate[0]
                vtmp[1][i] += self.translate[1]
            v = list(zip(*vtmp))
        return path.Path(v,self.codes,closed=True)

    @property
    def polygon2plot(self):
        """
        R.polygon2plot = path.Path(R.polygon.vertices+ np.array([1,1]),R.codes,closed=True)
        """
        return path.Path(self.polygon.vertices+ np.array([1,1]),self.codes,closed=True)

    def corners(self):
        """ returns xmin, ymin, xmax, ymax """
        return min([self.vertices[k][0] for k in range(self.nvertices)])+self.translate[0], \
               min([self.vertices[k][1] for k in range(self.nvertices)])+self.translate[1], \
               max([self.vertices[k][0] for k in range(self.nvertices)])+self.translate[0], \
               max([self.vertices[k][1] for k in range(self.nvertices)])+self.translate[1]
               
    def copy(self,translate=None,beadtype=None,name=""):
        """ returns a copy of the graphical object """
        if self.alike != "mixed":
            dup = deepduplicate(self)
            if translate != None: # applies translation
                dup.translate[0] += translate[0] 
                dup.translate[1] += translate[1]
            if beadtype != None: # update beadtype
                dup.beadtype = beadtype
            if name != "": # update name
                dup.name = name
            return dup
        else:
            raise ValueError("collections cannot be copied, regenerate the collection instead")


class Rectangle(genericpolygon):
    """ Rectangle class """
    def __init__(self,counter):
        self.name = "rect%03d" % counter[1]
        self.kind = "rectangle"     # kind of object
        self.alike = "circle"       # similar object for plotting
        self.beadtype = 1           # bead type
        self.nbeads = 0             # number of beads
        self.ismask = False         # True if beadtype == 0
        self.isplotted = False      # True if plotted
        self.islabelled = False     # True if labelled
        self.resolution = None      # resolution is undefined
        self.hlabel = {'contour':[], 'text':[]}
        self.index = counter[0]
        self.subindex = counter[1]
        self.translate = [0.0,0.0]  # modification used when an object is duplicated
        
    def __repr__(self):
        """ display for rectangle class """
        print("%s - %s object" % (self.name, self.kind))
        print("\trange x = [%0.4g %0.4g]" % (self.xmin,self.xmax))
        print("\trange y = [%0.4g %0.4g]" % (self.ymin,self.ymax))
        print("\tcenter = [%0.4g %0.4g]" % (self.xcenter,self.ycenter))
        print("\tangle = %0.4g" % self.angle)
        print("\ttranslate = [%0.4g %0.4g]" % (self.translate[0],self.translate[1]))        
        return "%s object: %s (beadtype=%d)" % (self.kind,self.name,self.beadtype)
    

class Circle(genericpolygon):
    """ Circle class """
    def __init__(self,counter,resolution=20):
        self.name = "circ%03d" % counter[1]
        self.kind = "circle"         # kind of object
        self.alike = "circle"        # similar object for plotting
        self.resolution = resolution # default resolution
        self.beadtype = 1            # bead type
        self.nbeads = 0              # number of beads
        self.ismask = False          # True if beadtype == 0
        self.isplotted = False       # True if plotted
        self.islabelled = False      # True if labelled
        self.hlabel = {'contour':[], 'text':[]}
        self.index = counter[0]
        self.subindex = counter[1]
        self.translate = [0.0,0.0]   # modification used when an object is duplicated

        
    def __repr__(self):
        """ display circle """
        print("%s - %s object" % (self.name,self.kind) )
        print("\trange x = [%0.4g %0.4g]" % (self.xmin,self.xmax))
        print("\trange y = [%0.4g %0.4g]" % (self.ymin,self.ymax))
        print("\tcenter = [%0.4g %0.4g]" % (self.xcenter,self.ycenter))
        print("\tradius = %0.4g" % self.radius)
        print("\tshaperatio = %0.4g" % self.shaperatio)
        print("\tangle = %0.4g" % self.angle)
        print("\ttranslate = [%0.4g %0.4g]" % (self.translate[0],self.translate[1]))        
        return "%s object: %s (beadtype=%d)" % (self.kind, self.name,self.beadtype)

class Triangle(Circle):
    """ Triangle class """
    def __init__(self,counter):
        super().__init__(counter,resolution=3)
        self.name = "tri%03d" % counter[1]
        self.kind = "triangle"     # kind of object


class Diamond(Circle):
    """ Diamond class """
    def __init__(self,counter):
        super().__init__(counter,resolution=4)
        self.name = "diam%03d" % counter[1]
        self.kind = "diamond"     # kind of object


class Pentagon(Circle):
    """ Pentagon class """
    def __init__(self,counter):
        super().__init__(counter,resolution=5)
        self.name = "penta%03d" % counter[1]
        self.kind = "pentagon"     # kind of object


class Hexagon(Circle):
    """ Hexagon class """
    def __init__(self,counter):
        super().__init__(counter,resolution=6)
        self.name = "hex%03d" % counter[1]
        self.kind = "Hexagon"     # kind of object
        
class collection(struct):
    """ collection class container (not to be called directly) """
    _type = "collect"               # object type
    _fulltype = "Collections"    # full name
    _ftype = "collection"        # field name
    def __init__(self,*obj,**kwobj):
        # store the objects with their alias
        super().__init__(**kwobj)
        # store objects with their real names
        for o in obj:
            if isinstance(o,raster):
                s = struct.dict2struct(o.objects)
                list_s = s.keys()
                for i in range(len(list_s)): self.setattr(list_s[i], s[i].copy())
            elif o!=None:
                self.setattr(o.name, o.copy())

class Collection:
    """ Collection object """
    def __init__(self,counter):
        self.name = "collect%03d" % counter[1]
        self.kind = "collection"    # kind of object
        self.alike = "mixed"        # similar object for plotting
        self.nbeads = 0             # number of beads
        self.ismask = False         # True if beadtype == 0
        self.isplotted = False      # True if plotted
        self.islabelled = False     # True if labelled
        self.resolution = None      # resolution is undefined
        self.hlabel = {'contour':[], 'text':[]}
        self.index = counter[0]
        self.subindex = counter[1]
        self.collection = collection()
        self.translate = [0.0,0.0]
        
    def __repr__(self):
        keylengths = [len(key) for key in self.collection.keys()]
        width = max(10,max(keylengths)+2)
        fmt = "%%%ss:" % width
        line = ( fmt % ('-'*(width-2)) ) + ( '-'*(min(40,width*5)) )
        print("%s - %s object" % (self.name, self.kind))
        print(line)
        print("\trange x = [%0.4g %0.4g]" % (self.xmin,self.xmax))
        print("\trange y = [%0.4g %0.4g]" % (self.ymin,self.ymax))
        print("\tcenter = [%0.4g %0.4g]" % self.xycenter)
        print("\ttranslate = [%0.4g %0.4g]" % (self.translate[0],self.translate[1]))
        print(line,'  name: type "original name" [centerx centery] [translatex translatey]',line,sep="\n")
        for key,value in self.collection.items():
            print(fmt % key,value.kind,
                  '"%s"' % value.name,
                  "[%0.4g %0.4g]" % (value.xcenter,value.ycenter),
                  "[%0.4g %0.4g]" % (value.translate[0],value.translate[1]))
        print(line)
        return "%s object: %s (beadtype=[%s])" % (self.kind,self.name,", ".join(map(str,self.beadtype)))

    # GET -----------------------------
    def get(self,name):
        """ returns the object """
        if name in self.collection:
            return self.collection.getattr(name)
        else:
            raise ValueError('the object "%s" does not exist, use list()' % name)

    # GETATTR --------------------------
    def __getattr__(self,key):
        """ get attribute override """
        return self.get(key)
    
    @property
    def xycenter(self):
        """ returns the xcenter and ycenter of  the collection """
        sx = sy = 0
        n = len(self.collection)
        for o in self.collection:
            sx += o.xcenter
            sy += o.ycenter
        return sx/n, sy/n
    
    @property
    def xcenter(self):
        """ returns xcenter """
        xc,_ = self.xycenter
        
    @property
    def ycenter(self):
        """ returns ycenter """
        _,yc = self.xycenter
        
    @property
    def beadtype(self):
        """ returns the xcenter and ycenter of the collection """
        b = []
        for o in self.collection:
            if o.beadtype not in b:
                b.append(o.beadtype)
        if len(b)==0:
            return 1
        else:
            return b
        

# %% scatter class and emulsion class
#    Simplified scatter and emulsion generator

class scatter():
    """ generic top scatter class """
    def __init__(self):
        """
        The scatter class provides an easy constructor
        to distribute in space objects according to their
        positions x,y and size r (radius).
        
        The class is used to derive emulsions.

        Returns
        -------
        None.

        """
        self.x, self.y, self.r = np.array([],dtype=int), np.array([],dtype=int), np.array([],dtype=int)
        
    @property
    def n(self):
        return len(self.x)
    
    def pairdist(self,x,y):
        """ pair distance to the surface of all disks/spheres """
        if self.n==0:
            return np.Inf
        else:
            return np.floor(np.sqrt((x-self.x)**2+(y-self.y)**2)-self.r)

class emulsion(scatter):
    """ emulsion generator """
    
    def __init__(self, xmin=10, ymin=10, xmax=90, ymax=90, 
                 maxtrials=1000, forcedinsertion=True):
        """
        

        Parameters
        ----------
        The insertions are performed between xmin,ymin and xmax,ymax
        xmin : int64 or real, optional
            x left corner. The default is 10.
        ymin : int64 or real, optional
            y bottom corner. The default is 10.
        xmax : int64 or real, optional
            x right corner. The default is 90.
        ymax : int64 or real, optional
            y top corner. The default is 90.
        maxtrials : integer, optional
            Maximum of attempts for an object. The default is 1000.
        forcedinsertion : logical, optional
            Set it to true to force the next insertion. The default is True.

        Returns
        -------
        None.

        """
        super().__init__()
        self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax
        self.width = xmax-xmin
        self.height = ymax-ymin
        self.maxtrials = maxtrials
        self.forcedinsertion = forcedinsertion

    def __repr__(self):
        print(f" Emulsion object\n\t{self.width}x{self.height} starting at x={self.xmin}, y={self.ymin}")        
        print(f"\tcontains {self.n} insertions")
        print("\tmaximum insertion trials:", self.maxtrials)
        print("\tforce next insertion if previous fails:", self.forcedinsertion)
        return f"emulsion with {self.n} insertions"

        
    def walldist(self,x,y):
        """ shortest distance to the wall """
        return min(abs(x-self.xmin),abs(y-self.ymin),abs(x-self.xmax),abs(y-self.ymax))

    def dist(self,x,y):
        """ shortest distance of the center (x,y) to the wall or any object"""
        return np.minimum(np.min(self.pairdist(x,y)),self.walldist(x,y))
    
    def accepted(self,x,y,r):
        """ acceptation criterion """
        return self.dist(x,y)>r
    
    def rand(self):
        """ random position x,y  """
        return  np.round(np.random.uniform(low=self.xmin,high=self.xmax)), \
                np.round(np.random.uniform(low=self.ymin,high=self.ymax))
     
    def insertone(self,r):
        """ insert one object of radius r """
        attempt, success = 0, False
        while not success and attempt<self.maxtrials:
            x,y = self.rand()
            success = self.accepted(x,y,r)
        if success:
            self.x = np.append(self.x,x)
            self.y = np.append(self.y,y)
            self.r = np.append(self.r,r)
        return success

    def insertion(self,rlist):
        """ insert a list of objects """
        rlist.sort(reverse=True)
        ntodo = len(rlist)
        n = nsuccess = 0
        stop = False
        while not stop:
            n += 1
            success = self.insertone(rlist[n-1])
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
# %% basic example

    plt.close("all")
    R = raster()
    R.rectangle(1,24,2,20,name='rect1')
    R.rectangle(60,80,50,81,name='rect2',beadtype=2,angle=40)
    R.rectangle(50,50,10,10,mode="center",angle=45,beadtype=1)
    R.circle(45,20,5,name='C1',beadtype=3)
    R.circle(35,10,5,name='C2',beadtype=3)
    
    R.circle(15,30,10,name='p1',beadtype=4,shaperatio=0.2,angle=-30)
    R.circle(12,40,8,name='p2',beadtype=4,shaperatio=0.2,angle=20)
    R.circle(12,80,22,name='p3',beadtype=4,shaperatio=1.3,angle=20)
    
    R.triangle(85,20,10,name='T1',beadtype=5,angle=20)
    R.diamond(85,35,5,name='D1',beadtype=5,angle=20)
    R.pentagon(50,35,5,name='P1',beadtype=5,angle=90)
    R.hexagon(47,85,12,name='H1',beadtype=5,angle=90)
    
    R.label("rect003")
    R.plot()
    R.list()
    R.show()
    
    R.clear()
    R.show()
    R.plot()
    R.show(extra="label")
    R.label("rect003")
    R.unlabel('rect1')
    
    X=R.data()
    
# %% another example    
    S = raster(width=1000,height=1000)
    S.rectangle(150,850,850,1000,name="top",beadtype=1)
    S.rectangle(150,850,0,150,name="bottom",beadtype=2)
    S.circle(500,500,480,name="mask",ismask=True,resolution=500)
    S.triangle(250,880,80,name='tooth1',angle=60,beadtype=1)
    S.triangle(750,880,80,name='tooth2',angle=-0,beadtype=1)
    S.circle(500,200,300,name="tongue",beadtype=5,shaperatio=0.3,resolution=300)
    S.rectangle(500,450,320,320,name="food",mode="center",beadtype=3)
    S.plot()
    S.show(extra="label",contour=False)
    

    
# %% advanced example
    #plt.close("all")
    draft = raster()
    draft.rectangle(1,24,2,20,name='rect1'),
    draft.rectangle(60,80,50,81,name='rect2',beadtype=2,angle=40),
    draft.rectangle(50,50,10,10,mode="center",angle=45,beadtype=1),
    draft.circle(45,20,5,name='C1',beadtype=3),
    draft.circle(35,10,5,name='C2',beadtype=3),
    draft.circle(10,10,2,name="X",beadtype=4)

    A = raster()
    A.collection(draft,name="C1",beadtype=1,translate=[10,30])
    A.__repr__()
    A.objects
    A.plot()
    A.show(extra="label")
    A.objects
    
    B = raster()
    #B.collection(X=draft.X,beadtype=1,translate=[50,50])
    B.copyalongpath(draft.X,name="PX",beadtype=2,
                    path=linear,
                     xmin=10,
                     ymin=10,
                     xmax=70,
                     ymax=90,
                        n=20)
    B.plot()
    B.show(extra="label")
    
    
# %% emulsion example
    e = emulsion()
    e.insertion([10,20,2,4,5,5,10,12,2,8,6,6,5,5,1,2,4,4,4,4,4])
    C = raster()
    C.scatter(e,name="emulsion",beadtype=2)
    C.plot()
    C.show()