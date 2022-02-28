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

    List objects
        R.list()
        R.get("p1")

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


# %% Imports and private library
from copy import copy as duplicate
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as path
import matplotlib.patches as patches
from pizza.data3 import data as data3

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


# %% raster class
class raster:
    """ raster class for LAMMPS SMD 
    
    Constructor
    
        R = raster(width=100,height=100)
        scale and center are only used with R.data()
    
    Graphical objects
        
        R.rectangle(xleft,xright,ybottom,ytop [, beadtype=1,mode="lower", angle=0, ismask=False])
        R.rectangle(xcenter,ycenter,width,height [, beadtype=1,mode="center", angle=0, ismask=False])
        R.circle(xcenter,ycenter,radius [, beadtype=1,shaperatio=1, angle=0, ismask=False], resolution=20, shiftangle=0)
        R.triangle(...)
        R.diamond(...)
        R.pentagon(...)
        R.hexagon(...)
        
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

    Generate an input data object
        X = R.data() or X=R.data(scale=(1,1),center=(0,0))
        X.write("/tmp/myfile")
    
    """
    
    # CONSTRUCTOR ---------------------------- 
    def __init__(self,width=100,height=100,name="default raster"):
        """ initialize raster """
        self.name = name
        self.width = width
        self.height = height
        self.xcenter= width/2
        self.ycenter = height/2
        self.objects = {}
        self.nobjects = 0    # total number of objects (alive)
        self.nbeads = 0
        self.counter = {"triangle":0,
                        "diamond":0,
                        "rectangle":0,
                        "pentagon":0,
                        "hexagon":0,
                        "circle":0,
                        "all":0}
        self.fontsize = 10   # font size for labels
        self.imbead = np.zeros((height,width),dtype=np.int8)
        self.imobj = np.zeros((height,width),dtype=np.int8)
        self.hfig = [] # figure handle
        self.dpi = 200
        # generic SMD properties (to be rescaled)
        self.volume = 1
        self.mass = 1
        self.radius = 1.5
        self.contactradius = 0.5
        self.velocities = [0,0,0]
        self.forces =[0,0,0]
        
    # DATA ---------------------------- 
    def data(self,scale=(1,1),center=(0,0)):
        """
        data(scale=(scalex,scaley),center=(centerx,centery))
        return a pizza.data object  """
        if not isinstance(scale,tuple) or len(scale)!=2:
            raise ValueError("scale must be tuple (scalex,scaley)")
        if not isinstance(center,tuple) or len(scale)!=2:
            raise ValueError("center must be tuple (centerx,centery)")
        n = self.length()
        i,j = self.imbead.nonzero() # x=j+0.5 y=i+0.5
        X = data3()  # empty pizza.data3.data object
        X.title = self.name + "(raster)"
        X.headers = {'atoms': n,
                      'atom types': self.count()[-1][0],
                      'xlo xhi': ((0.5-center[0])*scale[0], (self.width-0.5-center[0])*scale[0]),
                      'ylo yhi': ((0.5-center[1])*scale[1], (self.height-0.5-center[1])*scale[1]),
                      'zlo zhi': (0, 0.5*np.sqrt(scale[0]*scale[1]))}
        # [ATOMS] section
        X.append('Atoms',list(range(1,n+1)),True,"id")      # id
        X.append('Atoms',self.imbead[i,j],True,"type")      # Type
        X.append('Atoms',1,True,"mol")                      # mol
        X.append('Atoms',self.volume,False,"c_vol")         # c_vol
        X.append('Atoms',self.mass,False,"mass")            # mass
        X.append('Atoms',self.radius,False,"radius")        # radius
        X.append('Atoms',self.contactradius,False,"c_contact_radius") # c_contact_radius
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
        X.flist = ["%dx%d raster (%s)" % (self.width,self.height,self.name)]
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
        
    # GET ---------------------------- 
    def get(self,name):
        """ returns the object """
        if name in self.objects:
            return self.objects[name]
        else:
            raise ValueError('the object "%s" does not exist, use list()' % name)
        
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
        typlist = [self.objects[o].beadtype for o in self.names()]
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
        R.clear()
        R.plot()
        R.show(extra="label")
        
    # VALID method
    def valid(self,x,y):
        """ validation of coordinates """
        return min(self.width,max(0,round(x))),min(self.width,max(0,round(y)))


    # RECTANGLE ----------------------------     
    def rectangle(self,a,b,c,d,
                  mode="lowerleft",name=None,angle=0,
                  beadtype=None,ismask=False):
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
            R.xcenter = (a+b)/2
            R.ycenter = (c+d)/2
            R.vertices = [
                _rotate(a,c,R.xcenter,R.ycenter,angle),
                _rotate(b,c,R.xcenter,R.ycenter,angle),
                _rotate(b,d,R.xcenter,R.ycenter,angle),
                _rotate(a,d,R.xcenter,R.ycenter,angle),
                _rotate(a,c,R.xcenter,R.ycenter,angle)
                ] # anti-clockwise, closed (last point repeated)
        elif mode == "center":
            R.xcenter = a
            R.ycenter = b
            R.vertices = [
                _rotate(a-c/2,b-d/2,R.xcenter,R.ycenter,angle),
                _rotate(a+c/2,b-d/2,R.xcenter,R.ycenter,angle),
                _rotate(a+c/2,b+d/2,R.xcenter,R.ycenter,angle),
                _rotate(a-c/2,b+d/2,R.xcenter,R.ycenter,angle),
                _rotate(a-c/2,b-d/2,R.xcenter,R.ycenter,angle)
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
        R.polygon = path.Path(R.vertices,R.codes,closed=True)
        R.polygon2plot = path.Path(R.polygon.vertices+ np.array([1,1]),R.codes,closed=True)
        R.xmin, R.ymin = self.valid(
            min([R.vertices[k][0] for k in range(R.nvertices)]),
            min([R.vertices[k][1] for k in range(R.nvertices)])
            )
        R.xmax, R.ymax = self.valid(
            max([R.vertices[k][0] for k in range(R.nvertices)]),
            max([R.vertices[k][1] for k in range(R.nvertices)])
            )
        R.width = R.xmax - R.xmin
        R.height = R.ymax - R.ymin
        R.angle = angle
        # store the object
        self.objects[name] = R
        self.nobjects += 1

        
    # CIRCLE ----------------------------     
    def circle(self,xc,yc,radius,
                  name=None,shaperatio=1,angle=0,beadtype=None,ismask=False,
                  resolution=20,shiftangle=0):
        """ 
        circle object (or any regular polygon)
            circle(xcenter,ycenter,radius [, beadtype=1,shaperatio=1, angle=0, ismask=False], resolution=20, shiftangle=0)
        """
        # object creation
        self.counter["all"] += 1
        if resolution==3:
            self.counter["triangle"] += 1
            G = Triangle((self.counter["all"],self.counter["triangle"]))
        elif resolution==4:
            self.counter["diamond"] += 1
            G = Diamond((self.counter["all"],self.counter["diamond"]))
        elif resolution==5:
            self.counter["pentagon"] += 1
            G = Pentagon((self.counter["all"],self.counter["pentagon"]))
        elif resolution==6:
            self.counter["hexagon"] += 1
            G = Hexagon((self.counter["all"],self.counter["hexagon"]))
        else:
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
        G.xcenter, G.ycenter, G.radius = xc, yc, radius
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
        G.polygon = path.Path(G.vertices,G.codes,closed=True)
        G.polygon2plot = path.Path(G.polygon.vertices+ np.array([1,1]),G.codes,closed=True)
        G.xmin, G.ymin = self.valid(
            min([G.vertices[k][0] for k in range(G.nvertices)]),
            min([G.vertices[k][1] for k in range(G.nvertices)])
            )
        G.xmax, G.ymax = self.valid(
            max([G.vertices[k][0] for k in range(G.nvertices)]),
            max([G.vertices[k][1] for k in range(G.nvertices)])
            )
        G.width = G.xmax - G.xmin
        G.height = G.ymax - G.ymin
        G.angle, G.shaperatio = angle, shaperatio
        # store the object
        self.objects[name] = G
        self.nobjects += 1
  

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # =========== pseudo methods connected to circle() ===========
    # TRIANGLE, DIAMOND, PENTAGON, HEXAGON, -----------------------     
    def triangle(self,xc,yc,radius,name=None,
                 shaperatio=1,angle=0,beadtype=None,ismask=False,shiftangle=0):
        self.circle(xc,yc,radius,name=name,shaperatio=shaperatio,resolution=3,
           angle=angle,beadtype=beadtype,ismask=ismask,shiftangle=0)
        
    def diamond(self,xc,yc,radius,name=None,
                 shaperatio=1,angle=0,beadtype=None,ismask=False,shiftangle=0):
         self.circle(xc,yc,radius,name=name,shaperatio=shaperatio,resolution=4,
            angle=angle,beadtype=beadtype,ismask=ismask,shiftangle=0)
        
    def pentagon(self,xc,yc,radius,name=None,
                 shaperatio=1,angle=0,beadtype=None,ismask=False,shiftangle=0):
         self.circle(xc,yc,radius,name=name,shaperatio=shaperatio,resolution=5,
            angle=angle,beadtype=beadtype,ismask=ismask,shiftangle=0)
        
    def hexagon(self,xc,yc,radius,name=None,
                 shaperatio=1,angle=0,beadtype=None,ismask=False,shiftangle=0):
         self.circle(xc,yc,radius,name=name,shaperatio=shaperatio,resolution=6,
            angle=angle,beadtype=beadtype,ismask=ismask,shiftangle=0)
        
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # label method ---------------------------- 
    def label(self,name,ax=plt.gca(),contour=True,edgecolor="orange",facecolor="none",linewidth=2):
        """ label """
        self.figure()
        if name in self.objects:
            if not self.objects[name].islabelled:
                if contour:
                    patch = patches.PathPatch(self.objects[name].polygon2plot,
                                              facecolor=facecolor,
                                              edgecolor=edgecolor,
                                              lw=linewidth)
                    self.objects[name].hlabel["contour"] = \
                        ax.add_patch(patch)
                else:
                    self.objects[name].hlabel["contour"] = None
                self.objects[name].hlabel["text"] = \
                plt.text(self.objects[name].xcenter,
                         self.objects[name].ycenter,
                         "%s\n(t=$%d$,$n_p$=%d)" % (name, self.objects[name].beadtype,self.objects[name].nbeads),
                         horizontalalignment = "center",
                         verticalalignment = "center_baseline",
                         fontsize=self.fontsize
                         )
                plt.show()
                self.objects[name].islabelled = True
        else:
            raise ValueError("%d is not a valid name (use list()) to list valid objects" % name)
   
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
                if self.objects[o].alike == "circle":
                    j,i = np.meshgrid( 
                        range(self.objects[o].xmin-1,self.objects[o].xmax+1),
                        range(self.objects[o].ymin-1,self.objects[o].ymax+1))
                    points = np.vstack((j.flatten(),i.flatten())).T
                    npoints = points.shape[0]
                    inside = self.objects[o].polygon.contains_points(points)
                    for k in range(npoints):
                        if inside[k] and \
                            points[k,0]>=0 and \
                            points[k,0]<self.width and \
                            points[k,1]>=0 and \
                            points[k,1]<self.height :
                                self.imbead[points[k,1],points[k,0]] = self.objects[o].beadtype
                                self.imobj[points[k,1],points[k,0]] = self.objects[o].index
                                self.objects[o].nbeads += 1
                else:
                    raise ValueError("Not yet implemented")
                # store it as plotted
                self.objects[o].isplotted = True
                if not self.objects[o].ismask:
                    self.nbeads += self.objects[o].nbeads


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
    
# %% PRIVATE SUB-CLASSES
# Use the equivalent method of raster() to call these constructors
# counter[0] is the overall index (total number of objects created)
# counter[1] is the index of objects of this type (total number of objects created for this class)

class Rectangle:
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
        
    def __repr__(self):
        print("%s - %s object" % (self.name, self.kind))
        print("\trange x = [%0.4g %0.4g]" % (self.xmin,self.xmax))
        print("\trange y = [%0.4g %0.4g]" % (self.ymin,self.ymax))
        print("\tcenter = [%0.4g %0.4g]" % (self.xcenter,self.ycenter))
        print("\tangle = %0.4g" % self.angle)
        return "%s object: %s (beadtype=%d)" % (self.kind,self.name,self.beadtype)

class Circle:
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
        
    def __repr__(self):
        print("%s - %s object" % (self.name,self.kind) )
        print("\trange x = [%0.4g %0.4g]" % (self.xmin,self.xmax))
        print("\trange y = [%0.4g %0.4g]" % (self.ymin,self.ymax))
        print("\tcenter = [%0.4g %0.4g]" % (self.xcenter,self.ycenter))
        print("\tradius = %0.4g" % self.radius)
        print("\tshaperatio = %0.4g" % self.shaperatio)
        print("\tangle = %0.4g" % self.angle)
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

# %% debug section - generic code to test methods (press F5)
# ===================================================   
# main()
# ===================================================   
# for debugging purposes (code called as a script)
# the code is called from here
# ===================================================
if __name__ == '__main__':
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
    