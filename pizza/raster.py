# -*- coding: utf-8 -*-

"""
    RASTER method to generate LAMMPS input files (in 2D for this version)
    
    Generate a raster area
        R = raster()
        R = raster(width=200, height=200)
        
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
        R.show(extra="label")
        R.label("rect003")
        R.unlabel('rect1')
        
    Manage objects, update and show
    
    Get the image and convert the image to text
        I = R.numeric()
        T = R.string()
        R.print()
        
"""

# INRAE\Olivier Vitrac - rev. 2022-02-06
# contact: olivier.vitrac@agroparistech.fr

# History
# 2022-02-05 first alpha version
# 2022-02-06 RC for 2D




# %% Imports and private library
from copy import copy as duplicate
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as path
import matplotlib.patches as patches

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
    
    Graphical objects
        
        R.rectangle(xleft,xright,ybottom,ytop [, beadtype=1,mode="lower", angle=0, ismask=False])
        R.rectangle(xcenter,ycenter,width,height [, beadtype=1,mode="center", angle=0, ismask=False])
        R.circle(xcenter,ycenter,radius [, beadtype=1,shaperatio=1, angle=0, ismask=False], resolution=20, shiftangle=0)
        R.triangle(...)
        R.diamond(...)
        R.pentagon(...)
        R.hexagon(...)
        
    Display methods (order is omportant)
        R.plot()
        R.show()
        R.show(extra="labels")
        R.list()
        R.get("object")
        R.print()
        R.label("object")
        R.unlabel("object")
        
    Clear and delete
        R.clear()
        R.clear("all")
        R.delete("object")

    """
    
    # CONSTRUCTOR ---------------------------- 
    def __init__(self,width=100,height=100):
        """ initialize raster """
        self.width = width
        self.height = height
        self.xcenter= width/2
        self.ycenter = height/2
        self.objects = {}
        self.nobjects = 0    # total number of objects (alive)
        self.counter = {"triangle":0,
                        "diamond":0,
                        "rectangle":0,
                        "pentagon":0,
                        "hexagon":0,
                        "circle":0}
        self.fontsize = 12   # font size for labels
        self.im = np.zeros((height,width),dtype=np.int8)
        
    # NUMERIC ---------------------------- 
    def numeric(self):
        """ retrieve the image as a numpy.array """
        return self.im

    # STRING ---------------------------- 
    def string(self):
        """ convert the image as ASCII strings """
        num = np.flipud(duplicate(self.im));
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
        self.im = np.zeros((self.height,self.width),dtype=np.int8)
        for o in self.names():
            if what=="all":
                self.delete(o)
            else:
                self.objects[o].isplotted = False
                self.objects[o].islabelled = False
        plt.cla()
        self.show()

    # DISP method ---------------------------- 
    def __repr__(self):
       """ display method """
       print("RASTER area with %d objects" % self.nobjects)
       print("\twidth: %d" % self.width)
       print("\theihgt: %d" % self.height)
       return "RASTER AREA %d x %d with %d objects." % \
        (self.width,self.height,self.nobjects)


    # NAMES method ---------------------------- 
    def names(self):
        return list(self.objects.keys())
        
    # LIST method ---------------------------- 
    def list(self):
        """ list objects """
        fmt = "%%%ss:" % max(10,max([len(n) for n in self.names()])+2)
        print("RASTER with %d objects" % self.nobjects)
        for o in self.objects.keys():
            print(fmt % self.objects[o].name,self.objects[o].kind,
                  "(beadtype=%d)" % self.objects[o].beadtype)
            
    # EXIST method ---------------------------- 
    def exist(self,name):
        """ exist object """
        return name in self.objects
    
    # DELETE method ---------------------------- 
    def delete(self,name):
        """ delete object """
        if name in self.objects: 
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
        self.counter["rectangle"] += 1
        R = Rectangle(self.counter["rectangle"])
        if name != None:
            if self.exist(name):
                print('RASTER:: the object "%s" is overwritten',name)
                self.delete(name)
            R.name = name
        else:
            name = R.name
        if beadtype != None: R.beadtype = np.floor(beadtype)
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
        if resolution==3:
            self.counter["triangle"] += 1
            G = Triangle(self.counter["triangle"])
        elif resolution==4:
            self.counter["diamond"] += 1
            G = Diamond(self.counter["diamond"])
        elif resolution==5:
            self.counter["pentagon"] += 1
            G = Pentagon(self.counter["pentagon"])
        elif resolution==6:
            self.counter["hexagon"] += 1
            G = Hexagon(self.counter["hexagon"])
        else:
            self.counter["circle"] += 1
            G = Circle(self.counter["circle"],resolution=resolution)
        if name != None:
            if self.exist(name):
                print('RASTER:: the object "%s" is overwritten',name)
                self.delete(name)
            G.name = name
        else:
            name = G.name
        if beadtype != None: G.beadtype = np.floor(beadtype)
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
    def label(self,name,ax=plt.gca(),edgecolor="orange",facecolor="none",linewidth=2):
        """ label """
        if name in self.objects:
            if not self.objects[name].islabelled:
                patch = patches.PathPatch(self.objects[name].polygon2plot,
                                          facecolor=facecolor,
                                          edgecolor=edgecolor,
                                          lw=linewidth)
                self.objects[name].hlabel["contour"] = \
                    ax.add_patch(patch)
                self.objects[name].hlabel["text"] = \
                plt.text(self.objects[name].xcenter,
                         self.objects[name].ycenter,
                         "%s\n(%d)" % (name, self.objects[name].beadtype),
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
                                self.im[points[k,1],points[k,0]] = self.objects[o].beadtype
                else:
                    raise ValueError("Not yet implemented")
                # store it as plotted
                self.objects[o].isplotted = True


    # SHOW method ---------------------------- 
    def show(self,extra="none"):
        """ show method """
        imagesc(self.im)
        if extra == "label":
            ax = plt.gca()
            for o in self.names():
                self.label(o,ax=ax)
            plt.show()
            
    # SHOW method ---------------------------- 
    def print(self):
        """ print method """
        txt = self.string()
        for i in range(len(txt)):
            print(txt[i],end="\n")
        
# %% sub-classes
class Rectangle:
    """ Rectangle class """
    def __init__(self,counter):
        self.name = "rect%03d" % counter
        self.kind = "rectangle"     # kind of object
        self.alike = "circle"       # similar object for plotting
        self.beadtype = 1           # bead type
        self.ismask = False         # True if beadtype == 0
        self.isplotted = False      # True if plotted
        self.islabelled = False     # True if labelled
        self.resolution = None      # resolution is undefined
        self.hlabel = {'contour':[], 'text':[]}
        
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
        self.name = "circ%03d" % counter
        self.kind = "circle"         # kind of object
        self.alike = "circle"        # similar object for plotting
        self.resolution = resolution # default resolution
        self.beadtype = 1            # bead type
        self.ismask = False          # True if beadtype == 0
        self.isplotted = False       # True if plotted
        self.islabelled = False      # True if labelled
        self.hlabel = {'contour':[], 'text':[]}
        
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
        super().__init__(0,resolution=3)
        self.name = "tri%03d" % counter
        self.kind = "triangle"     # kind of object


class Diamond(Circle):
    """ Diamond class """
    def __init__(self,counter):
        super().__init__(0,resolution=4)
        self.name = "diam%03d" % counter
        self.kind = "diamond"     # kind of object


class Pentagon(Circle):
    """ Pentagon class """
    def __init__(self,counter):
        super().__init__(0,resolution=5)
        self.name = "penta%03d" % counter
        self.kind = "pentagon"     # kind of object


class Hexagon(Circle):
    """ Hexagon class """
    def __init__(self,counter):
        super().__init__(0,resolution=6)
        self.name = "hex%03d" % counter
        self.kind = "Hexagon"     # kind of object

# %%        
# ===================================================   
# main()
# ===================================================   
# for debugging purposes (code called as a script)
# the code is called from here
# ===================================================
if __name__ == '__main__':
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
    R.list()
    R.plot()
    R.show()
    
    R.clear()
    R.show()
    R.plot()
    R.show(extra="label")
    R.label("rect003")
    R.unlabel('rect1')