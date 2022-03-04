#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

    The class script() and derived facilitate the coding in LAMMPS
    Each section is remplaced by a template as a class inherited from script()
    
    The class include two important attribues
        TEMPLATE is a string  efines between """ """ the LAMMPS code
        The variables used by TEMPLATE are stored in DEFINITIONS.
        DEFINITIONS is a scripdata() object accepting scalar, mathematical expressions, 
        text almost as in LAMMPS.
        
        Variables can be inherited between sections using + or += operator
        
    Toy example
        G = globalsection()
        print(G)
        c = initializesection()
        print(c)
        g = geometrysection()
        print(g)
        d = discretizationsection()
        print(d)
        b = boundarysection()
        print(b)
        i = interactionsection()
        print(i)
        t = integrationsection()
        print(t)
        d = dumpsection()
        print(d)
        s = statussection()
        print(s)
        r = runsection()
        print(r)
        
        # all sections as a single script
        myscript = G+c+g+d+b+i+t+d+s+r
        print("\n"*4,'='*80,'\n\n this is the full script\n\n','='*80,'\n')
        print(myscript.do())


Created on Sat Feb 19 11:00:43 2022

@author: olivi
"""

# INRAE\Olivier Vitrac - rev. 2022-02-19
# contact: olivier.vitrac@agroparistech.fr


# Revision history
# 2022-02-20 RC with documentation and 10 section templates
# 2022-02-21 add + += operators, expand help
# 2022-02-26 add USER to enable instance variables with higher precendence
# 2022-02-27 add write() method and overload & operator
# 2022-02-28 overload * (+ expansion) and ** (& expansion) operators
# 2022-03-01 expand lists (with space as separator) and tupples (with ,)
# 2022-03-02 first implementation of scriptobject(), object container pending
# 2022-03-03 extensions  of scriptobject() and scriptobjectgroup()
# 2022-03-04 finalization of scriptobject() and scriptobjectgroup()


# %% Dependencies
import types
from copy import copy as duplicate
# All forcefield parameters are stored à la Matlab in a structure
from forcefield import *
from private.struct import param,struct

# span vector into a single string
def span(vector,sep=" ",left="",right=""): return left+sep.join(map(str,vector))+right

# %% Top generic classes for storing script data and objects
# they are not intended to be used outside script data and objects

class scriptdata(param):
    """ 
        class of script parameters 
            Typical constructor:
                DEFINITIONS = scriptdata(
                    var1 = value1,
                    var2 = value2
                    )
        See script, struct, param to get review all methods attached to it
    """
    _type = "SD"
    _fulltype = "script data"
    _ftype = "definition"

     
# object data (for scripts)
class scriptobject(struct):
    """ 
        class of script object 
            OBJ = scriptobject(...)
            Implemented properties:
                beadtype=1,2,...
                name="short name"
                fullname = "comprehensive name"
                style = "smd"
                forcefield = any valid forcefield (default = rigidwall)
        
        group objects with OBJ1+OBJ2... into scriptobjectgroups
        
        objects can be compared and sorted based on beadtype and name
        
    """
    _type = "SO"
    _fulltype = "script object"
    _ftype = "propertie"
    
    def __init__(self, 
                 beadtype=1,
                 name="undefined",
                 fullname="",
                 style="smd",
                 forcefield=rigidwall,
                 groups=[]):
        if fullname=="":
            fullname = name + " object definition"
        super(scriptobject,self).__init__(
            name=name,
            fullname=fullname,
            style=style,
            forcefield=forcefield(beadtype=beadtype, userid=name),
            beadtype=beadtype)

    def __str__(self):
        """ string representation """
        return f"{self._fulltype} | type={self.beadtype} | name={self.name}"

        
    def __add__(self, SO):
        if isinstance(SO,scriptobject):
            if SO.name != self.name:
                if SO.beadtype == self.beadtype:
                   SO.beadtype =  self.beadtype+1
                return scriptobjectgroup(self,SO)
            else:
                raise ValueError('the object "%s" already exists' % SO.name)
        elif isinstance(SO,scriptobjectgroup):
            return scriptobjectgroup(self)+SO
        else:
            return ValueError("The object should a script object or its container")
        
    def __eq__(self, SO):
        return (self.beadtype == SO.beadtype) and (self.name == SO.name)

    def __ne__(self, SO):
        return (self.beadtype != SO.beadtype) or (self.name != SO.name)

    def __lt__(self, SO):
        return self.beadtype < SO.beadtype

    def __gt__(self, SO):
        return self.beadtype > SO.beadtype

    def __le__(self, SO):
        return self.beadtype <= SO.beadtype

    def __ge__(self, SO):
        return self.beadtype >= SO.beadtype
                    
        
# group of script objects  (special kind of list)
class scriptobjectgroup(struct):
    """ 
        class of script object group
            script object groups are built from script objects OBJ1, OBJ2,..
            GRP = scriptobjectgroup(OBJ1,OBJ2,...)
            GRP = OBJ1+OBJ2+...
            
        note: each beadtype occurs once in the group (if not an error message is generated)
            
        List of methods
            group(group=1,groupname="mygroup") returns a dictionary
            select([1,2,4]) selects objects with matching beadtypes
            
        List of properties
            converted data: list, str, zip, beadtype, name
            numeric: len, min, max, minmax
        
        Full syntax
            GRP.select([1,2]).group(groupname="test",group=1) returns
        {'test': {'group': 1, 'beadtype': [1, 2], 'name': ['a', 'b']}}
        
    """
    _type = "SOG"
    _fulltype = "script object group"
    _ftype = "object"
    
    def __init__(self,*SOgroup):
        """ SOG constructor """
        super(scriptobjectgroup,self).__init__()
        beadtypemax = 0
        names = []
        for k in range(len(SOgroup)):
            if isinstance(SOgroup[k],scriptobject):
                if SOgroup[k].beadtype<beadtypemax or SOgroup[k].beadtype==None:
                    beadtypemax +=1
                    SOgroup[k].beadtype = beadtypemax
                if SOgroup[k].name not in names:
                    self.setattr(SOgroup[k].name,SOgroup[k])
                    beadtypemax = SOgroup[k].beadtype
                else:
                    raise ValueError('the script object "%s" already exists' % SOgroup[k].name)
                names.append(SOgroup[k].name)
            else:
                raise ValueError("the argument #%d is not a script object")

    def __str__(self):
        """ string representation """
        return f"{self._fulltype} with {len(self)} {self._ftype}s ({span(self.beadtype)})"

    def __add__(self, SOgroup):
        """ overload + """
        beadlist = self.beadtype
        dup = duplicate(self)
        if isinstance(SOgroup,scriptobject):
            if SOgroup.name not in self.keys():
                if SOgroup.beadtype not in beadlist:
                    dup.setattr(SOgroup.name, SOgroup)
                    beadlist.append(SOgroup.beadtype)
                    return dup
                else:
                    raise ValueError('%s(beadtype=%d) is already in use, same beadtype' \
                                     % (SOgroup.name,SOgroup.beadtype))
            else:
                raise ValueError('the object "%s" is already in the list' % SOgroup.name)
        elif isinstance(SOgroup,scriptobjectgroup):
            for k in SOgroup.keys():
                if k not in dup.keys():
                    if SOgroup.getattr(k).beadtype not in beadlist:
                        dup.setattr(k,SOgroup.getattr(k))
                        beadlist.append(SOgroup.getattr(k).beadtype)
                    else:
                        raise ValueError('%s(beadtype=%d) is already in use, same beadtype' \
                                         % (k,SOgroup.getattr(k).beadtype))
                else:
                    raise ValueError('the object "%s" is already in the list' % k)
            return dup
        else:
            raise ValueError("the argument #%d is not a script object or a script object group")
    
    @property
    def list(self):
        """ convert into a list """
        return sorted(self)
    
    @property
    def zip(self):
        """ zip beadtypes and names """
        return [(self.getattr(k).beadtype,self.getattr(k).name) for k in self.keys()]
    
    @property
    def name(self):
        """ "return the list of names """
        return [x for _, x in sorted(self.zip)]
    
    @property
    def beadtype(self):
        """ returns the beads in the group """
        return sorted([self.getattr(k).beadtype for k in self.keys()])
    
    @property
    def str(self):
        return span(self.beadtype)
    
    @property
    def minmax(self):
        """ returns the min,max of beadtype """
        return self.min,self.max
    
    @property
    def min(self):
        """ returns the min of beadtype """
        return min(self.beadtype)
    
    @property
    def max(self):
        """ returns the max of beadtype """
        return max(self.beadtype)
    
    def group(self,groupname="undefined group",group=1):
        """ create a group with name """
        return {groupname: {"group":1, "beadtype":self.beadtype, "name":self.name}}
    
    def select(self,keeplist=None):
        """ select bead from a keep beadlist """
        if keeplist==None: keeplist = list(range(self.min,self.max+1))
        if not isinstance(keeplist,list): keeplist = [keeplist]
        dup = scriptobjectgroup()
        for b,n in self.zip:
            if b in keeplist:
                dup = dup + self.getattr(n)
        return dup
    

# %% core class (please derive this class when you use it, do not alter it)
class script():
    """ 
        core script class (flexible design)
        --------------------------------------
        
        The class script enables to generate dynamically LAMMPS sections
        "NONE","GLOBAL","INITIALIZE","GEOMETRY","DISCRETIZATION",
        "BOUNDARY","INTERACTIONS","INTEGRATION","DUMP","STATUS","RUN"
        
        
        # %% This the typical construction for a class
        class XXXXsection(script):
            "" " LAMMPS script: XXXX session "" "
            name = "XXXXXX"
            description = name+" section"
            position = 0
            section = 0
            userid = "example"
            version = 0.1
            
            DEFINITIONS = scriptdata(
                 value= 1,
            expression= "${value+1}",
                  text= "$my text"
                )
            
            TEMPLATE = "" "
        # :UNDEF SECTION:
        #   to be defined
        LAMMPS code with ${value}, ${expression}, ${text}
            "" "
        
        DEFINTIONS can be inherited from a previous section
        DEFINITIONS = previousection.DEFINTIONS + scriptdata(
                 value= 1,
            expression= "${value+1}",
                  text= "$my text"            
            )
        
        
        Recommandation: Split a large script into a small classes or actions
        An example of use could be: 
            move1 = translation(displacement=10)+rotation(angle=30)
            move2 = shear(rate=0.1)+rotation(angle=20)
            bigmove = move1+move2+move1
            script = bigmove.do() generates the script
        
        NOTE1: Use the print() and the method do() to get the script interpreted
        
        NOTE2: DEFINITIONS can be pretified using DEFINITIONS.generator()
        
        NOTE3: Variables can extracted from a template using TEMPLATE.scan()
        
        NOTE4: Scripts can be joined (from top down to bottom).
        The first definitions keep higher precedence. Please do not use
        a variable twice with different contents.
        
        myscript = s1 + s2 + s3 will propagate the definitions
        without overwritting previous values). myscript will be
        defined as s1 (same name, position, userid, etc.)
    
        myscript += s appends the script section s to myscript
        
        NOTE5: rules of precedence when script are concatenated
        The attributes from the class (name, description...) are kept from the left
        The values of the right overwrite all DEFINITIONS
        
        NOTE6: user variables (instance variables) can set with USER or at the construction
        myclass_instance = myclass(myvariable = myvalue)
        myclass_instance.USER.myvariable = myvalue
        
        NOTE7: how to change variables for all instances at once?
        In the example below, let x is a global variable (instance independent)
        and y a local variable (instance dependent)
        instance1 = myclass(y=1) --> y=1 in instance1
        instance2 = myclass(y=2) --> y=2 in instance2
        instance3.USER.y=3 --> y=3 in instance3
        instance1.DEFINITIONS.x = 10 --> x=10 in all instances (1,2,3)

        If x is also defined in the USER section, its value will be used        
        Setting instance3.USER.x = 30 will assign x=30 only in instance3
        
        NOTE8: if a the script is used with different values for a smae parameter
        use the operator & to concatenate the results instead of the script
        example: load(file="myfile1") & load(file="myfile2) & load(file="myfile3")+...
                                             
        NOTE9: lists (e.g., [1,2,'a',3] are expanded ("1 2 a 3")
               tuples (e.g. (1,2)) are expanded ("1,2")
               It is easier to read ["lost","ignore"] than "$ lost ignore"
        
        --------------------------[ FULL EXAMPLE ]-----------------------------

        # Import the class
        from pizza.script import *
        
        # Override the class globalsection
        class scriptexample(globalsection):
            description = "demonstrate commutativity of additions"
            verbose = True
            
            DEFINITIONS = scriptdata(
                X = 10,
                Y = 20,
                R1 = "${X}+${Y}",
                R2 = "${Y}+${X}"
                )
            TEMPLATE = "" "
            # Property of the addition
            ${R1} = ${X} + ${Y}
            ${R2} = ${Y} + ${X}
         "" "
            
        # derived from scriptexample, X and Y are reused
        class scriptexample2(scriptexample):
            description = "demonstrate commutativity of multiplications"
            verbose = True
            DEFINITIONS = scriptexample.DEFINITIONS + scriptdata(
                R3 = "${X} * ${Y}",
                R4 = "${Y} * ${X}",        
                )            
            TEMPLATE = "" "
            # Property of the multiplication
            ${R3} = ${X} * ${Y}
            ${R4} = ${Y} * ${X}
         "" "
        
        # call the first class and override the values X and Y
        s1 = scriptexample()
        s1.USER.X = 1  # method 1 of override
        s1.USER.Y = 2
        s1.do()
        # call the second class and override the values X and Y
        s2 = scriptexample2(X=1000,Y=2000) # method 2
        s2.do()
        # Merge the two scripts
        s = s1+s2
        print("this is my full script")
        s.description
        s.do()
        
        # The result for s1 is
            3 = 1 + 2
            3 = 2 + 1
        # The result for s2 is
            2000000 = 1000 * 2000
            2000000 = 2000 * 1000
        # The result for s=s1+s2 is
            # Property of the addition
            3000 = 1000 + 2000
            3000 = 2000 + 1000 
            # Property of the multiplication
            2000000 = 1000 * 2000
            2000000 = 2000 * 1000
    
    """
    type = "script"                         # type (class name)
    name = "empty script"                   # name
    description = "it is an empty script"   # description
    position = 0                            # 0 = root
    section = 0                             # section (0=undef)
    userid = "undefined"                    # user name
    version = 0.21                          # version
    verbose = False                         # set it to True to force verbosity
    _contact = ("INRAE\SAYFOOD\olivier.vitrac@agroparistech.fr",
                "INRAE\SAYFOOD\william.jenkinson@agroparistech.fr")
    
    SECTIONS = ["NONE","GLOBAL","INITIALIZE","GEOMETRY","DISCRETIZATION",
                "BOUNDARY","INTERACTIONS","INTEGRATION","DUMP","STATUS","RUN"]
   
    # Main class variables
    # These definitions are for instances
    DEFINITIONS = scriptdata()
    TEMPLATE = """
        # empty LAMMPS script
    """
    
    # constructor
    def __init__(self,**userdefinitions):
        """ constructor adding instance definitions stored in USER """
        self.USER = scriptdata(**userdefinitions)
    
    # print method for headers (static, no implicit argument)
    @staticmethod
    def printheader(txt,align="^",width=80,filler="~"):
        """ print header """
        if txt=="":
            print("\n"+filler*(width+6)+"\n")
        else:
            print(("\n{:"+filler+"{align}{width}}\n").format(' [ '+txt+' ] ', align=align, width=str(width)))
    
    # Display/representation method
    def __repr__(self):    
        """ disp method """
        stamp = f"{self.type}:{self.name}:{self.userid}"
        self.printheader(f"{stamp} | version={self.version}",filler="/")
        self.printheader("POSITION & DESCRIPTION",filler="-",align=">")
        print(f"     position: {self.position}")
        print(f"         role: {self.role} (section={self.section})")
        print(f"  description: {self.description}")
        self.printheader("DEFINITIONS",filler="-",align=">")
        print(self.DEFINITIONS)
        self.printheader("TEMPLATE",filler="-",align=">")
        if self.verbose:
            print(self.TEMPLATE)
            self.printheader("SCRIPT",filler="-",align=">")
        print(self.do(printflag=False))
        self.printheader("")
        return stamp

    # Extract attributes within the class
    def getallattributes(self):
        """ advanced method to get all attributes including class ones"""
        return {k: getattr(self, k) for k in dir(self) \
                if (not k.startswith('_')) and (not isinstance(getattr(self, k),types.MethodType))}
                   
    # Generate the script
    def do(self,printflag=True):
        """ generate the script """
        inputs = self.DEFINITIONS + self.USER
        for k in inputs.keys():
            if isinstance(inputs.getattr(k),list):
                inputs.setattr(k,"$ "+span(inputs.getattr(k)))
            elif isinstance(inputs.getattr(k),tuple):
                inputs.setattr(k,"$ "+span(inputs.getattr(k),sep=","))
        cmd = inputs.formateval(self.TEMPLATE)
        cmd = cmd.replace("[comment]",f"[position {self.position}:{self.userid}]")
        if printflag: print(cmd)
        return cmd
    
    # Return the role of the script (based on section)
    @property
    def role(self):
        """ convert section index into a role (section name) """
        if self.section in range(len(self.SECTIONS)):
            return self.SECTIONS[self.section]
        else:
            return ""

    # override +
    def __add__(self,s):
        """ overload addition operator """
        if isinstance(s,script):
            dup = duplicate(self)
            dup.DEFINITIONS = dup.DEFINITIONS + s.DEFINITIONS
            dup.USER = dup.USER + s.USER
            dup.TEMPLATE = "\n".join([dup.TEMPLATE,s.TEMPLATE])
            return dup
        raise TypeError("the second operand must a script object")

    # override +=
    def _iadd__(self,s):
        """ overload addition operator """
        if isinstance(s,script):
            self.DEFINITIONS = self.DEFINITIONS + s.DEFINITIONS
            self.USER = self.USER + s.USER
            self.TEMPLATE = "\n".join([self.TEMPLATE,s.TEMPLATE])
        else:
            raise TypeError("the second operand must a script object")
            
    # override &
    def __and__(self,s):
        """ overload and operator """
        if isinstance(s,script):
            dup = duplicate(self)
            dup.TEMPLATE = "\n".join([self.do(),s.do()])
            return dup
        raise TypeError("the second operand must a script object")
 
    # override *
    def __mul__(self,ntimes):
        """ overload * operator """
        if isinstance(ntimes, int) and ntimes>0:
           res = duplicate(self)
           if ntimes>1:
               for n in range(1,ntimes): res += self
           return res
        raise ValueError("multiplicator should be a strictly positive integer")

    def __pow__(self,ntimes):
        """ overload ** operator """
        if isinstance(ntimes, int) and ntimes>0:
           res = duplicate(self)
           if ntimes>1:
               for n in range(1,ntimes): res = res & self
           return res
        raise ValueError("multiplicator should be a strictly positive integer")
        
    # write file
    def write(self, file):
        f = open(file, "w")
        print(self.do(),file=f)
        f.close()
        
# %% Parent classes of script sessions (to be derived)
# navigate with the outline window

# %% Global section template
class globalsection(script):
    """ LAMMPS script: global session """
    name = "global"
    description = name+" section"
    position = 0
    section = 1
    userid = "example"
    version = 0.1
    
    DEFINITIONS = scriptdata(
  outputfile= "$dump.mouthfeel_v5_long    # from the project of the same name",
        tsim= "500000                     # may be too long",
     outstep= 10
        )
    
    MATERIALS = scriptdata(
         rho_saliva= "1000 # mass density saliva",
            rho_obj= "1300 # mass density solid objects",
                 c0= "10.0 # speed of sound for saliva",
                  E= "5*${c0}*${c0}*${rho_saliva} # Young's modulus for solid objects",
           Etongue1= "10*${E} # Young's modulus for tongue",
           Etongue2= "2*${Etongue1} # Young's modulus for tongue",
                 nu= "0.3 # Poisson ratio for solid objects",
        sigma_yield= "0.1*${E} # plastic yield stress for solid objects",
     hardening_food= "0 # plastic hardening parameter for solid food",
   hardening_tongue= "1 # plastic hardening parameter for solid tongue",
  contact_stiffness= "2.5*${c0}^2*${rho_saliva} # contact force amplitude",
       contact_wall= "100*${contact_stiffness} # contact with wall (avoid interpenetration)",
                 q1= "1.0 # artificial viscosity",
                 q2= "0.0 # artificial viscosity",
                 Hg= "10 # Hourglass control coefficient for solid objects",
                 Cp= "1.0 # heat capacity -- not used here"
                  )
    
    DEFINITIONS += MATERIALS # append MATERIALS data
    
    TEMPLATE = """
# :GLOBAL SECTION:
#   avoid to set variables in LAMMPS script
#   use DEFINITIONS field to set properties.
#   If you need to define them, use the following syntax


    # ####################################################################################################
    # # GLOBAL
    # ####################################################################################################
     variable outputfile string "${outputfile}"
     variable tsim equal ${tsim}
     variable outstep equal ${outstep}
    
    # ####################################################################################################
    # # MATERIAL PARAMETERS 
    # ####################################################################################################
    # variable        rho_saliva equal 1000 # mass density saliva
    # variable        rho_obj equal 1300 # mass density solid objects
    # variable        c0 equal 10.0 # speed of sound for saliva
    # variable        E equal 5*${c0}*${c0}*${rho_saliva} # Young's modulus for solid objects
    # variable        Etongue1 equal 10*${E} # Young's modulus for tongue 
    # variable        Etongue2 equal 2*${Etongue1} # Young's modulus for tongue 
    # variable        nu equal 0.3 # Poisson ratio for solid objects
    # variable        sigma_yield equal 0.1*${E} # plastic yield stress for solid objects
    # variable        hardening_food equal 0 # plastic hardening parameter for solid food
    # variable        hardening_tongue equal 1 # plastic hardening parameter for solid tongue
    # variable        contact_stiffness equal 2.5*${c0}^2*${rho_saliva} # contact force amplitude
    # variable        contact_wall equal 100*${contact_stiffness} # contact with wall (avoid interpenetration)
    # variable        q1 equal 1.0 # artificial viscosity
    # variable        q2 equal 0.0 # artificial viscosity
    # variable        Hg equal 10 # Hourglass control coefficient for solid objects
    # variable        Cp equal 1.0 # heat capacity -- not used here
    """
    
# %% Initialize section template
class initializesection(script):
    """ LAMMPS script: global session """
    name = "initialize"
    description = name+" section"
    position = 1
    section = 2
    userid = "example"
    version = 0.1
    
    DEFINITIONS = scriptdata(
               units= "$ si",
           dimension= 2,
            boundary= "$ sm sm p",
          atom_style= "$smd",
  neigh_modify_every= 5,
  neigh_modify_delay= 0,
         comm_modify= "$ vel yes",
              newton= "$ off",
         atom_modify= "$ map array",
          comm_style= "$ tiled"
        )
    
    TEMPLATE = """
# :INITIALIZE SECTION:
#   initialize styles, dimensions, boundaries and communivation

    ####################################################################################################
    # INITIALIZE LAMMPS
    ####################################################################################################
    units           ${units}
    dimension       ${dimension}
    boundary        ${boundary}
    atom_style      ${atom_style}
    neigh_modify    every ${neigh_modify_every} delay ${neigh_modify_delay} check yes
    comm_modify     ${comm_modify}
    newton          ${newton}
    atom_modify     ${atom_modify}
    comm_style      ${comm_style}
    """
    
# %% Geometry section template
class geometrysection(script):
    """ LAMMPS script: global session """
    name = "geometry"
    description = name+" section"
    position = 2
    section = 3
    userid = "example"
    version = 0.1
    
    DEFINITIONS = scriptdata(
         l0= 0.05,
       hgap= "0.25        # gap to prevent direct contact at t=0 (too much enery)",
  hsmallgap= "0.1   # gap to prevent direct contact at t=0 (too much enery)",
       hto1= "0.8         # height of to1 (the tongue to1, note 1 not l)",
       hto2= "0.5         # height of to2 (the tongue to2)",
       rsph= "0.3         # radius of spherical food particles",
       lpar= "0.6         # size of prismatic particles ",
    yfloor1= "${hgap}  # bottom position of to1, position of the first floor",
     yroof1= "${yfloor1}+${hto1} # bottom position of to1, position of the first floor",
   yfloor2a= "${yroof1}+${hsmallgap}  # position of the second floor / level a",
    yroof2a= "${yfloor2a}+${lpar}      # position of the second floor / level a",
   yfloor2b= "${yroof2a}+${hsmallgap} # position of the second floor / level b",
    yroof2b= "${yfloor2b}+${lpar}      # position of the second floor / level b",
   yfloor2c= "${yfloor2a}+${rsph}     # position of the second floor / level c",
    yroof2c= "${yfloor2c}+${rsph}      # position of the second floor / level c",
   yfloor2d= "${yroof2c}+${rsph}+${hsmallgap} # position of the second floor / level d",
    yroof2d= "${yfloor2d}+${rsph}      # position of the second floor / level d",
    yfloor3= 5.0,
     yroof3= "${yfloor3}+${hto2} # bottom position of to1",
   yfloor3a= "${yfloor3}-0.6",
    yroof3a= "${yfloor3}",
    crunchl= "${yfloor3}-${yfloor2a}-0.8",
    crunchp= 3,
    crunchw= "2*pi/${crunchp}",
    crunchd= "2*(sin((${crunchp}*${crunchw})/4)^2)/${crunchw}",
    crunchv= "${crunchl}/${crunchd}"
        )
    
    TEMPLATE = """
# :GEOMETRY SECTION:
#   Build geometry (very specific example)

    ####################################################################################################
    # CREATE INITIAL GEOMETRY
    # note there are 4 groups (create_box 5 box)
    # groupID 1 = saliva
    # groupID 2 = food
    # groupID 3 = mouth walls
    # groupID 4 = tongue alike (part1)
    # groupID 5 = also tongue but palate infact (part2)
    ####################################################################################################
    # create simulation box, a mouth, and a saliva column
    region          box block 0 12 0 8 -0.01 0.01 units box
    create_box      5 box
    region          saliva1 block 0.25 1.8 1.25 3.5 EDGE EDGE units box
    region          saliva2 block 10 11.65 1.25 4 EDGE EDGE units box
    region          mouth block 0.15 11.85 0.15 8 -0.01 0.01 units box side out # mouth
    lattice         sq ${l0}
    create_atoms    1 region saliva1
    create_atoms    1 region saliva2
    group           saliva type 1
    create_atoms    3 region mouth
    group           mouth type 3
    
    print "Crunch distance:${crunchl}"  # 3.65
    print "Crunch distance:${crunchv}"  # 0.1147
    
    
    # bottom part of the tongue: to1 (real tongue)
    # warning: all displacements are relative to the bottom part
    region          to1 block 1 11 ${yfloor1} ${yroof1} EDGE EDGE units box
    region          to2part1 block 0.5 11.5 ${yfloor3} ${yroof3} EDGE EDGE units box
    region          to2part2 block 5.5 6 ${yfloor3a} ${yroof3a} EDGE EDGE units box
    region          to2 union 2 to2part1 to2part2
    create_atoms    4 region to1
    create_atoms    5 region to2
    group           tongue1 type 4
    group           tongue2 type 5
    
    # create some solid objects to be pushed around
    region          pr1 prism 2 2.6 ${yfloor2a} ${yroof2a} EDGE EDGE 0.3 0 0 units box
    region          bl1 block 3 3.6 ${yfloor2a} ${yroof2a} EDGE EDGE units box
    region          sp1 sphere 4.3 ${yfloor2c} 0 ${rsph} units box
    region          sp2 sphere 5 ${yfloor2c} 0 ${rsph} units box
    region          sp3 sphere 5.7 ${yfloor2c} 0 ${rsph} units box
    region          sp4 sphere 6.4 ${yfloor2c} 0 ${rsph} units box
    region          sp5 sphere 7.1 ${yfloor2c} 0 ${rsph} units box
    region          sp6 sphere 6.05 ${yfloor2d} 0 ${rsph} units box
    region          br2 block 3 3.6 ${yfloor2b} ${yroof2b} EDGE EDGE units box
    
    # fill the regions with atoms (note that atoms = smoothed hydrodynamics particles)
    create_atoms    2 region pr1
    create_atoms    2 region bl1
    create_atoms    2 region sp1
    create_atoms    2 region sp2
    create_atoms    2 region sp3
    create_atoms    2 region sp4
    create_atoms    2 region sp5
    create_atoms    2 region sp6
    create_atoms    2 region br2
    
    # atoms of objects are grouped with two id
    # fix apply only to groups
    group           solidfoods type 2
    group           tlsph type 2
    
    # group heavy
    group           allheavy type 1:4 


    """

    
# %% Discretization section template
class discretizationsection(script):
    """ LAMMPS script: discretization session """
    name = "discretization"
    description = name+" section"
    position = 3
    section = 4
    userid = "example"
    version = 0.1
    
    # inherit properties from geometrysection
    DEFINITIONS = geometrysection.DEFINITIONS + scriptdata(
              h= "2.5*${l0} # SPH kernel diameter",
        vol_one= "${l0}^2 # initial particle volume for 2d simulation",
     rho_saliva= 1000,
        rho_obj= 1300,
           skin= "${h} # Verlet list range",
  contact_scale= 1.5
        )
    
    TEMPLATE = """
# :DISCRETIZATION SECTION:
#   discretization

    ####################################################################################################
    # DISCRETIZATION PARAMETERS
    ####################################################################################################
    set             group all diameter ${h}
    set             group all smd/contact/radius ${l0}
    set             group all volume  ${vol_one}
    set             group all smd/mass/density ${rho_saliva}
    set             group solidfoods smd/mass/density ${rho_obj}
    set             group tongue1 smd/mass/density ${rho_obj}
    set             group tongue2 smd/mass/density ${rho_obj}
    neighbor        ${skin} bin

    """

    
# %% Boundary section template
class boundarysection(script):
    """ LAMMPS script: boundary session """
    name = "boundary"
    description = name+" section"
    position = 4
    section = 5
    userid = "example"
    version = 0.1
    
    # inherit properties from geometrysection
    DEFINITIONS = geometrysection.DEFINITIONS + scriptdata(
        gravity = -9.81,
        vector = "$ 0 1 0"
        )
    
    TEMPLATE = """
# :BOUNDARY SECTION:
#   boundary section

    ####################################################################################################
    # DEFINE BOUNDARY CONDITIONS
    #
    # note that the the particles constituting the mouth are simply not integrated in time,
    # thus these particles never move. This is equivalent to a fixed displacement boundary condition.
    ####################################################################################################
    fix             gfix allheavy gravity ${gravity} vector ${vector} # add gravity
    
    
    ####################################################################################################
    # moving top "tongue" (to2)
    ####################################################################################################
    variable vmouth equal -${crunchv}*sin(${crunchw}*time)
    fix             move_fix_tongue2 tongue2 smd/setvel 0 v_vmouth 0

    """

# %% Interactions section template
class interactionsection(script):
    """ LAMMPS script: interaction session """
    name = "interactions"
    description = name+" section"
    position = 5
    section = 6
    userid = "example"
    version = 0.1
    
    DEFINITIONS = globalsection.DEFINITIONS + \
                  geometrysection.DEFINITIONS + \
                  discretizationsection.DEFINITIONS
    
    TEMPLATE = """
# :INTERACTIONS SECTION:
#   Please use forcefield() to make a robust code

    ####################################################################################################
    # INTERACTION PHYSICS / MATERIAL MODEL
    # 3 different pair styles are used:
    #     - updated Lagrangian SPH for saliva
    #     - total Lagrangian SPH for solid objects
    #     - a repulsive Hertzian potential for contact forces between different physical bodies
    ####################################################################################################
    pair_style      hybrid/overlay smd/ulsph *DENSITY_CONTINUITY *VELOCITY_GRADIENT *NO_GRADIENT_CORRECTION &
                                   smd/tlsph smd/hertz ${contact_scale}
    pair_coeff      1 1 smd/ulsph *COMMON ${rho_saliva} ${c0} ${q1} ${Cp} 0 &
                    *EOS_TAIT 7.0 &
                    *END
    pair_coeff      2 2 smd/tlsph *COMMON ${rho_obj} ${E} ${nu} ${q1} ${q2} ${Hg} ${Cp} &
                    *STRENGTH_LINEAR_PLASTIC ${sigma_yield} ${hardening_food} &
                    *EOS_LINEAR &
                    *END
    pair_coeff      4 4 smd/tlsph *COMMON ${rho_obj} ${Etongue1} ${nu} ${q1} ${q2} ${Hg} ${Cp} &
                    *STRENGTH_LINEAR_PLASTIC ${sigma_yield} ${hardening_tongue} &
                    *EOS_LINEAR &
                    *END
    pair_coeff      5 5 smd/tlsph *COMMON ${rho_obj} ${Etongue2} ${nu} ${q1} ${q2} ${Hg} ${Cp} &
                    *STRENGTH_LINEAR_PLASTIC ${sigma_yield} ${hardening_tongue} &
                    *EOS_LINEAR &
                    *END
    
    pair_coeff      3 3 none   # wall-wall
    pair_coeff      1 2 smd/hertz ${contact_stiffness} # saliva-food
    pair_coeff      1 3 smd/hertz ${contact_wall} # saliva-wall
    pair_coeff      2 3 smd/hertz ${contact_wall} # food-wall
    pair_coeff      2 2 smd/hertz ${contact_stiffness} # food-food
    # add 4 (to1)
    pair_coeff      1 4 smd/hertz ${contact_stiffness} # saliva-tongue1
    pair_coeff      2 4 smd/hertz ${contact_stiffness} # food-tongue1
    pair_coeff      3 4 smd/hertz ${contact_wall} # wall-tongue1
    pair_coeff      4 4 smd/hertz ${contact_stiffness} # tongue1-tongue1
    # add 5 (to2)
    pair_coeff      1 5 smd/hertz ${contact_stiffness} # saliva-tongue2
    pair_coeff      2 5 smd/hertz ${contact_stiffness} # food-tongue2
    pair_coeff      3 5 smd/hertz ${contact_wall} # wall-tongue2
    pair_coeff      4 5 smd/hertz ${contact_stiffness} # tongue1-tongue2
    pair_coeff      5 5 smd/hertz ${contact_stiffness} # tongue2-tongue2

    """
    

# %% Time integration section template
class integrationsection(script):
    """ LAMMPS script: time integration session """
    name = "time integration"
    description = name+" section"
    position = 6
    section = 7
    userid = "example"
    version = 0.1
    
    DEFINITIONS = scriptdata(
              dt = 0.1,
   adjust_redius = "$ 1.01 10 15"
        )
    
    TEMPLATE = """
# :INTEGRATION SECTION:
#   Time integration conditions

    fix             dtfix tlsph smd/adjust_dt ${dt} # dynamically adjust time increment every step
    fix             integration_fix_water saliva smd/integrate_ulsph adjust_radius ${adjust_redius}
    fix             integration_fix_solids solidfoods smd/integrate_tlsph
    fix             integration_fix_tongue1 tongue1 smd/integrate_tlsph
    fix             integration_fix_tongue2 tongue2 smd/integrate_tlsph
    
    """

    
# %% Dump section template
class dumpsection(script):
    """ LAMMPS script: dump session """
    name = "dump"
    description = name+" section"
    position = 7
    section = 8
    userid = "example"
    version = 0.1
    
    DEFINITIONS = globalsection().DEFINITIONS
    
    TEMPLATE = """
# :DUMP SECTION:
#   Dump configuration

    ####################################################################################################
    # SPECIFY TRAJECTORY OUTPUT
    ####################################################################################################
    compute         eint all smd/internal/energy
    compute         contact_radius all smd/contact/radius
    compute         S solidfoods smd/tlsph/stress
    compute         nn saliva smd/ulsph/num/neighs
    compute         epl solidfoods smd/plastic/strain
    compute         vol all smd/vol
    compute         rho all smd/rho
    
    dump            dump_id all custom ${outstep} ${outputfile} id type x y &
                    fx fy vx vy c_eint c_contact_radius mol &
                    c_S[1] c_S[2] c_S[4] mass radius c_epl c_vol c_rho c_nn proc
    dump_modify     dump_id first yes
    
    """

    
# %% Status section template
class statussection(script):
    """ LAMMPS script: status session """
    name = "status"
    description = name+" section"
    position = 8
    section = 9
    userid = "example"
    version = 0.1
    
    DEFINITIONS = scriptdata(
        thermo = 100
        )
    
    TEMPLATE = """
# :STATUS SECTION:
#   Status configuration

    ####################################################################################################
    # STATUS OUTPUT
    ####################################################################################################
    compute         alleint all reduce sum c_eint
    variable        etot equal pe+ke+c_alleint+f_gfix # total energy of the system
    thermo          ${thermo}
    thermo_style    custom step ke pe v_etot c_alleint f_dtfix dt
    thermo_modify   lost ignore

    """
    
    
# %% Run section template
class runsection(script):
    """ LAMMPS script: run session """
    name = "run"
    description = name+" section"
    position = 9
    section = 10
    userid = "example"
    version = 0.1
    
    DEFINITIONS = globalsection.DEFINITIONS + scriptdata(
        balance = "$ 500 0.9 rcb"
        )
    
    TEMPLATE = """
# :RUN SECTION:
#   run configuration

    ####################################################################################################
    # RUN SIMULATION
    ####################################################################################################
    fix             balance_fix all balance ${balance} # load balancing for MPI
    run             ${tsim}
    """
    
# %% DEBUG  
# ===================================================   
# main()
# ===================================================   
# for debugging purposes (code called as a script)
# the code is called from here
# ===================================================
if __name__ == '__main__':
    """
        a=scriptobject(name="a"); b=scriptobject(name="b");
        scriptobjectgroup(a)
        c=a+b
        d = scriptobject(name="d",beadtype=3)
        e = a +b +d
        e.select(1)
        
    """
    
    G = globalsection()
    print(G)
    c = initializesection()
    print(c)
    g = geometrysection()
    print(g)
    d = discretizationsection()
    print(d)
    b = boundarysection()
    print(b)
    i = interactionsection()
    print(i)
    t = integrationsection()
    print(t)
    d = dumpsection()
    print(d)
    s = statussection()
    print(s)
    r = runsection()
    print(r)
    
    # all sections as a single script
    myscript = G+c+g+d+b+i+t+d+s+r
    print("\n"*4,'='*80,'\n\n this is the full script\n\n','='*80,'\n')
    print(myscript.do())