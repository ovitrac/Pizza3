#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__project__ = "Pizza3"
__author__ = "Olivier Vitrac"
__copyright__ = "Copyright 2022"
__credits__ = ["Olivier Vitrac"]
__license__ = "GPLv3"
__maintainer__ = "Olivier Vitrac"
__email__ = "olivier.vitrac@agroparistech.fr"
__version__ = "0.35"

"""

    The class script() and derived facilitate the coding in LAMMPS
    Each section is remplaced by a template as a class inherited from script()
    
    The class include two important attribues:
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

    Additional classes: scriptobject(), scriptobjectgroup(), pipescript()
    They generate dynamic scripts from objects, collection of objects or scripts
    
    Variables (DEFINITIONS and USER) are stored in scriptdata() objects
    
    
    How the variables are stored and used.
         STATIC: set in the script class (with the attribute DEFINITIONS)
         GLOBAL: set in the instance of the script during construction
                 or within the USER scriptdata(). These values can be changed
                 at runtime but the values are overwritten if the script are 
                 combined with the operator +
          LOCAL: set (bypass) in the pipeline with the keyword USER[step]
          
    Example with pipelines:
        Build pipelines with:
            p = G | c | g # using the symbol pipe "|"
            p = p = pipescript(G)*4 # using the constructor pipescript()
            
                Pipeline with 4 scripts and
                D(STATIC:GLOBAL:LOCAL) DEFINITIONS
                  ------------:----------------------------------------
                  [-]  00: script:global:example with D(19: 0: 0)
                  [-]  01: script:global:example with D(19: 0: 0)
                  [-]  02: script:global:example with D(19: 0: 0)
                  [-]  03: script:global:example with D(19: 0: 0)
                  ------------:----------------------------------------        

    Change the GLOBAL variables for script with idx=0
        p.scripts[0].USER.a=1  # set a=1 for all scripts onwards
        p.scripts[0].USER.b=2  # set b=2
    Change the LOCAL variables for script with idx=0
        p.USER[0].a=10        # set a=10 for the script 00
                
                ------------:----------------------------------------
                [-]  00: script:global:example with D(19: 2: 1)
                [-]  01: script:global:example with D(19: 0: 0)
                [-]  02: script:global:example with D(19: 0: 0)
                [-]  03: script:global:example with D(19: 0: 0)
                ------------:----------------------------------------

    Summary of pipeline indexing and scripting
        p[i], p[i:j], p[[i,j]] copy pipeline segments
        LOCAL: p.USER[i],p.USER[i].variable modify the user space of only p[i]
        GLOBAL: p.scripts[i].USER.var to modify the user space from p[i] and onwards
        STATIC: p.scripts[i].DEFINITIONS
        p.rename(idx=range(2),name=["A","B"]), p.clear(idx=[0,3,4])
        p.script(), p.script(idx=range(5)), p[0:5].script()        

Created on Sat Feb 19 11:00:43 2022

@author: olivi
"""

# INRAE\Olivier Vitrac - rev. 2022-03-15
# contact: olivier.vitrac@agroparistech.fr


# Revision history
# 2022-02-20 RC with documentation and 10 section templates
# 2022-02-21 add + += operators, expand help
# 2022-02-26 add USER to enable instance variables with higher precendence
# 2022-02-27 add write() method and overload & operator
# 2022-02-28 overload * (+ expansion) and ** (& expansion) operators
# 2022-03-01 expand lists (with space as separator) and tupples (with ,)
# 2022-03-02 first implementation of scriptobject(), object container pending
# 2022-03-03 extensions of scriptobject() and scriptobjectgroup()
# 2022-03-04 consolidation of scriptobject() and scriptobjectgroup()
# 2022-03-05 [major update] scriptobjectgroup() can generate scripts for loading, setting groups and forcefields
# 2022-03-12 [major update] pipescript() enables to store scripts in dynamic pipelines
# 2022-03-15 implement a userspace within the pipeline
# 2022-03-15 fix scriptobject | pipescript, smooth and document syntaxes with pipescripts
# 2022-03-16 overload +=, *, several fixes and update help for pipescript
# 2022-03-18 modification to script method, \ttype specified for groups
# 2022-03-19 standardized pizza path

# %% Dependencies
import types
from copy import copy as duplicate
from copy import deepcopy as deepduplicate
import datetime, os, socket, getpass

# All forcefield parameters are stored à la Matlab in a structure
from pizza.forcefield import *
from pizza.private.struct import param,struct

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
                filename = "/path/to/your/inputfile"
                style = "smd"
                forcefield = any valid forcefield instance (default = rigidwall())
        
        note: use a forcefield instance with the keywork USER to pass user FF parameters
        examples:   rigidwall(USER=scriptdata(...))
                    solidfood(USER==scriptdata(...))
                    water(USER==scriptdata(...))
        
        group objects with OBJ1+OBJ2... into scriptobjectgroups
        
        objects can be compared and sorted based on beadtype and name
        
    """
    _type = "SO"
    _fulltype = "script object"
    _ftype = "propertie"
    
    def __init__(self, 
                 beadtype = 1,
                 name = "undefined",
                 fullname="",
                 filename="",
                 style="smd",
                 forcefield=rigidwall(),
                 group=[],
                 USER = scriptdata()
                 ):
        if fullname=="": fullname = name + " object definition"
        if not isinstance(group,list): group = [group]
        forcefield.beadtype = beadtype
        forcefield.userid = name
        forcefield.USER = USER
        super(scriptobject,self).__init__(
              beadtype = beadtype,
                  name = name,
              fullname = fullname,
              filename = filename,
                 style = style,
            forcefield = forcefield,
                 group = group,
                  USER = USER
                 )

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
        
    def __or__(self, pipe):
        """ overload | or for pipe """
        if isinstance(pipe,(pipescript,script,scriptobject,scriptobjectgroup)):
            return pipescript(self) | pipe
        else:
            raise ValueError("the argument must a pipescript, a scriptobject or a scriptobjectgroup")
        
    def __eq__(self, SO):
        return isinstance(SO,scriptobject) and (self.beadtype == SO.beadtype) \
            and (self.name == SO.name)

    def __ne__(self, SO):
        return not isinstance(SO,scriptobject) or (self.beadtype != SO.beadtype) or (self.name != SO.name)

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
            struct() converts data as structure
            select([1,2,4]) selects objects with matching beadtypes
            
        List of properties (dynamically calculated)
            converted data: list, str, zip, beadtype, name, groupname, group, filename
            numeric: len, min, max, minmax
            forcefield related: interactions, forcefield
            script: generate the script (load,group,forcefield)
        
        Full syntax (toy example)
        
    b1 = scriptobject(name="bead 1",group = ["A", "B", "C"],filename='myfile1',forcefield=rigidwall())
    b2 = scriptobject(name="bead 2", group = ["B", "C"],filename = 'myfile1',forcefield=rigidwall())
    b3 = scriptobject(name="bead 3", group = ["B", "D", "E"],forcefield=solidfood())
    b4 = scriptobject(name="bead 4", group = "D",beadtype = 1,filename="myfile2",forcefield=water())
    
        note: beadtype are incremented during the collection (effect of order)
            
            # generate a collection, select a typ 1 and a subgroup, generate the script for 1,2
            
            collection = b1+b2+b3+b4
            grp_typ1 = collection.select(1)
            grpB = collection.group.B
            script12 = collection.select([1,2]).script
        
        note: collection.group.B returns a strcture with 6 fields
        -----------:----------------------------------------
            groupid: 2 <-- automatic group numbering
        groupidname: B <-- group name
          groupname: ['A', 'B', 'C', 'D', 'E'] <--- snonyms
           beadtype: [1, 2, 3] <-- beads belonging to B
               name: ['bead 1', 'bead 2', 'bead 3'] <-- their names
                str: group B 1 2 3 <-- LAMMPS syntax
        -----------:----------------------------------------
        
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
                if SOgroup.beadtype in beadlist and \
                  (SOgroup.beadtype==None or SOgroup.beadtype==self.min):
                      SOgroup.beadtype = self.max+1
                if SOgroup.beadtype not in beadlist:
                    dup.setattr(SOgroup.name, SOgroup)
                    beadlist.append(SOgroup.beadtype)
                    return dup
                else:
                    raise ValueError('%s (beadtype=%d) is already in use, same beadtype' \
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
                        raise ValueError('%s (beadtype=%d) is already in use, same beadtype' \
                                         % (k,SOgroup.getattr(k).beadtype))
                else:
                    raise ValueError('the object "%s" is already in the list' % k)
            return dup
        else:
            raise ValueError("the argument #%d is not a script object or a script object group")
    
    def __or__(self, pipe):
        """ overload | or for pipe """
        if isinstance(pipe,(pipescript,script,scriptobject,scriptobjectgroup)):
            return pipescript(self) | pipe
        else:
            raise ValueError("the argument must a pipescript, a scriptobject or a scriptobjectgroup")

    @property
    def list(self):
        """ convert into a list """
        return sorted(self)
    
    @property
    def zip(self):
        """ zip beadtypes and names """
        return sorted( \
            [(self.getattr(k).beadtype,self.getattr(k).name,self.getattr(k).group,self.getattr(k).filename) \
            for k in self.keys()])

    @property
    def n(self):
        """ returns the number of bead types """
        return len(self)

    @property
    def beadtype(self):
        """ returns the beads in the group """
        return [x for x,_,_,_ in self.zip]
        
    @property
    def name(self):
        """ "return the list of names """
        return [x for _,x,_,_ in self.zip]
    
    @property
    def groupname(self):
        """ "return the list of groupnames """
        grp = []
        for _,_,glist,_ in self.zip:
            for g in glist:
                if g not in grp: grp.append(g)
        return grp    

    @property
    def filename(self):
        """ "return the list of names as a dictionary """
        files = {}
        for _,n,_,fn in self.zip:
            if fn != "": 
                if fn not in files:
                    files[fn] = [n]
                else:
                    files[fn].append(n)
        return files
    
    @property
    def str(self):
        return span(self.beadtype)

    def struct(self,groupid=1,groupidname="undef"):
        """ create a group with name """
        return struct(
                groupid = groupid,
            groupidname = groupidname,
              groupname = self.groupname, # meaning is synonyms
               beadtype = self.beadtype,
                   name = self.name,
                    str = "group %s %s" % (groupidname, span(self.beadtype))
               )
    
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
    
    def select(self,beadtype=None):
        """ select bead from a keep beadlist """
        if beadtype==None: beadtype = list(range(self.min,self.max+1))
        if not isinstance(beadtype,(list,tuple)): beadtype = [beadtype]
        dup = scriptobjectgroup()
        for b,n,_,_ in self.zip:
            if b in beadtype:
                dup = dup + self.getattr(n)
        return dup
    
    @property
    def group(self):
        """ build groups from group (groupname contains synonyms) """
        groupdef = struct()
        gid = 0
        bng = self.zip
        for g in self.groupname:
            gid +=1
            b =[x for x,_,gx,_ in bng if g in gx]
            groupdef.setattr(g,self.select(b).struct(groupid = gid, groupidname = g))
        return groupdef
    
    @property
    def interactions(self):
        """ update and accumulate all forcefields """
        FF = []
        for b in self.beadtype:
            selection = duplicate(self.select(b)[0])
            selection.forcefield.beadtype = selection.beadtype
            selection.forcefield.userid = selection.name
            FF.append(selection.forcefield)
        # initialize interactions with pair_style
        TEMPLATE = "\n# ===== [ BEGIN FORCEFIELD SECTION ] "+"="*80 + \
            FF[0].pair_style()
        # pair diagonal terms
        for i in range(len(FF)):
            TEMPLATE += FF[i].pair_diagcoeff()
        # pair off-diagonal terms
        for j in range(1,len(FF)):
            for i in range(0,j):
                TEMPLATE += FF[i].pair_offdiagcoeff(FF[j])
        # end
        TEMPLATE += "\n# ===== [ END FORCEFIELD SECTION ] "+"="*82+"\n"
        return FF,TEMPLATE
    
    @property
    def forcefield(self):
        """ interaction forcefields """
        FF,_ = self.interactions
        return FF
    
    @property
    def script(self):
        """ basic scripting from script objects """
        # load data when needed and comment which object
        TEMPFILES = ""
        isfirst = True
        if self.filename !={}:
            TEMPFILES = "\n# ===== [ BEGIN INPUT FILES SECTION ] "+"="*79 + "\n"
            for fn,cfn in self.filename.items():
                TEMPFILES += span(cfn,sep=", ",left="\n# load files for objects: ",right="\n")
                if isfirst:
                    isfirst = False
                    TEMPFILES += f"\tread_data {fn}\n"
                else:
                    TEMPFILES += f"\tread_data {fn} add append\n"
            TEMPFILES += "\n# ===== [ END INPUT FILES SECTION ] "+"="*81+"\n\n"
        # define groups
        TEMPGRP = "\n# ===== [ BEGIN GROUP SECTION ] "+"="*85 + "\n"
        for g in self.group:
            TEMPGRP += f'\n\t#\tDefinition of group {g.groupid}:{g.groupidname}\n'
            TEMPGRP += f'\t#\t={span(g.name,sep=", ")}\n'
            TEMPGRP += f'\t#\tSimilar groups: {span(g.groupname,sep=", ")}\n'
            TEMPGRP += f'\tgroup \t {g.groupidname} \ttype \t {span(g.beadtype)}\n'
        TEMPGRP += "\n# ===== [ END GROUP SECTION ] "+"="*87+"\n\n"
        # define interactions
        _,TEMPFF = self.interactions
        # chain strings into a script
        tscript = script()
        tscript.name = "scriptobject script"        # name
        tscript.description = str(self)             # description
        tscript.userid = "scriptobject"             # user name
        tscript.TEMPLATE = TEMPFILES+TEMPGRP+TEMPFF
        return tscript

# %% script core class
# note: please derive this class when you use it, do not alter it
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
        
        NOTE8: if a the script is used with different values for a same parameter
        use the operator & to concatenate the results instead of the script
        example: load(file="myfile1") & load(file="myfile2) & load(file="myfile3")+...
                                             
        NOTE9: lists (e.g., [1,2,'a',3] are expanded ("1 2 a 3")
               tuples (e.g. (1,2)) are expanded ("1,2")
               It is easier to read ["lost","ignore"] than "$ lost ignore"
        
        NOTE 10: New operators >> and || extend properties
            + merge all scripts but overwrite definitions
            & execute statically script content
            >> pass only DEFINITIONS but not TEMPLATE to the right
            | pipe execution such as in Bash, the result is a pipeline
            
        NOTE 11: Scripts in pipelines are very flexible, they support
        full indexing à la Matlab, including staged executions
            method do(idx) generates the script corresponding to indices idx
            method script(idx) generates the corresponding script object
        
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
    version = 0.40                          # version
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
    
    # String representation
    def __str__(self):
        """ string representation """
        return f"{self.type}:{self.name}:{self.userid}"

    # Display/representation method
    def __repr__(self):    
        """ disp method """
        stamp = str(self)
        self.printheader(f"{stamp} | version={self.version}",filler="/")
        self.printheader("POSITION & DESCRIPTION",filler="-",align=">")
        print(f"     position: {self.position}")
        print(f"         role: {self.role} (section={self.section})")
        print(f"  description: {self.description}")
        self.printheader("DEFINITIONS",filler="-",align=">")
        if len(self.DEFINITIONS)<15:
            self.DEFINITIONS
        else:
            print("too many definitions: ",self.DEFINITIONS)
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
            
    # override >>
    def __rshift__(self,s):
        """ overload right  shift operator (keep only the last template) """
        if isinstance(s,script):
            dup = duplicate(self)
            dup.DEFINITIONS = dup.DEFINITIONS + s.DEFINITIONS
            dup.USER = dup.USER + s.USER
            dup.TEMPLATE = s.TEMPLATE
            return dup
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

    # override **
    def __pow__(self,ntimes):
        """ overload ** operator """
        if isinstance(ntimes, int) and ntimes>0:
           res = duplicate(self)
           if ntimes>1:
               for n in range(1,ntimes): res = res & self
           return res
        raise ValueError("multiplicator should be a strictly positive integer")
    
    # pipe scripts
    def __or__(self,pipe):
        """ overload | or for pipe """
        if isinstance(pipe,(pipescript,script,scriptobject,scriptobjectgroup)):
            return pipescript(self) | pipe
        else:
            raise ValueError("the argument must a pipescript, a scriptobject or a scriptobjectgroup")
    
    # header
    @staticmethod
    def header():
        return   f"# Automatic LAMMPS script (version {script.version})\n" + \
                 f"# {getpass.getuser()}@{socket.gethostname()}:{os.getcwd()}\n" + \
                 f'# {datetime.datetime.now().strftime("%c")}\n\n'
    
    # write file
    def write(self, file):
        f = open(file, "w")
        print(script.header(),"\n"*3,file=f)
        print(self.do(),file=f)
        f.close()

# %% pipe script
class pipescript():
    """
        Pipescript class stores scripts in pipelines
            By assuming: s0, s1, s2... scripts, scriptobject or scriptobjectgroup
            p = s0 | s1 | s2 generates a pipe script
            
            Example of pipeline:
          ------------:----------------------------------------
          [-]  00: G with (0>>0>>19) DEFINITIONS
          [-]  01: c with (0>>0>>10) DEFINITIONS
          [-]  02: g with (0>>0>>26) DEFINITIONS
          [-]  03: d with (0>>0>>19) DEFINITIONS
          [-]  04: b with (0>>0>>28) DEFINITIONS
          [-]  05: i with (0>>0>>49) DEFINITIONS
          [-]  06: t with (0>>0>>2) DEFINITIONS
          [-]  07: d with (0>>0>>19) DEFINITIONS
          [-]  08: s with (0>>0>>1) DEFINITIONS
          [-]  09: r with (0>>0>>20) DEFINITIONS
          ------------:----------------------------------------
        Out[35]: pipescript containing 11 scripts with 8 executed[*]
        
        note: XX>>YY>>ZZ represents the number of stored variables
             and the direction of propagation (inheritance from left)
             XX: number of definitions in the pipeline USER space
             YY: number of definitions in the script instance (frozen in the pipeline)
             ZZ: number of definitions in the script (frozen space)
            
            pipelines are executed sequentially (i.e. parameters can be multivalued)
                cmd = p.do()
                fullscript = p.script()
                
            pipelines are indexed
                cmd = p[[0,2]].do()
                cmd = p[0:2].do()
                cmd = p.do([0,2])
                
            pipelines can be reordered
                q = p[[2,0,1]]
                
            steps can be deleted
                p[[0,1]] = []
                
            clear all executions with
                p.clear()
                p.clear(idx=1,2)
                
            local USER space can be accessed via
            (affects only the considered step)
                p.USER[0].a = 1
                p.USER[0].b = [1 2]
                p.USER[0].c = "$ hello world"
                
            global USER space can accessed via
            (affects all steps onward)
                p.scripts[0].USER.a = 10
                p.scripts[0].USER.b = [10 20]
                p.scripts[0].USER.c = "$ bye bye"

            static definitions
                p.scripts[0].DEFINITIONS
                
            steps can be renamed with the method rename()
                
            syntaxes are à la Matlab:
                p = pipescript()
                p | i
                p = collection | G
                p[0]
                q = p | p
                q[0] = []
                p[0:1] = q[0:1]
                p = G | c | g | d | b | i | t | d | s | r
                p.rename(["G","c","g","d","b","i","t","d","s","r"])
                cmd = p.do([0,1,4,7])
                sp = p.script([0,1,4,7])
                r = collection | p

            Pending: mechanism to store LAMMPS results (dump3) in the pipeline                
    """
    
    def __init__(self,s=None):
        """ constructor """
        self.globalscript = None
        self.listscript = []
        self.listUSER = []
        self.verbose = True # set it to False to reduce verbosity
        self.cmd = ""
        if isinstance(s,script): 
            self.listscript = [duplicate(s)]
            self.listUSER = [scriptdata()]
        elif isinstance(s,scriptobject):
            self.listscript = [scriptobjectgroup(s).script]
            self.listUSER = [scriptdata()]
        elif isinstance(s,scriptobjectgroup):
            self.listscript = [s.script]
            self.listUSER = [scriptdata()]
        else:
            ValueError("the argument should be a scriptobject or scriptobjectgroup")
        if s != None:
            self.name = [str(s)]
            self.executed = [False]
        else:
            self.name = []
            self.executed = []

    def setUSER(self,idx,key,value):
        """ 
            setUSER sets USER variables
            setUSER(idx,varname,varvalue)
        """
        if isinstance(idx,int) and (idx>=0) and (idx<self.n):
            self.listUSER[idx].setattr(key,value)
        else:
            raise IndexError(f"the index in the pipe should be comprised between 0 and {len(self)-1}")
        
    def getUSER(self,idx,key):
        """ 
            getUSER get USER variable
            getUSER(idx,varname)
        """
        if isinstance(idx,int) and (idx>=0) and (idx<self.n):
            self.listUSER[idx].getattr(key)
        else:
            raise IndexError(f"the index in the pipe should be comprised between 0 and {len(self)-1}")

    @property
    def USER(self):
        """
            p.USER[idx].var returns the value of the USER variable var
            p.USER[idx].var = val assigns the value val to the USER variable var
        """
        return self.listUSER  # override listuser
    
    @property
    def scripts(self):
        """
            p.scripts[idx].USER.var returns the value of the USER variable var
            p.scripts[idx].USER.var = val assigns the value val to the USER variable var
        """
        return self.listscript # override listuser

    def __add__(self,s):
        """ overload + as pipe with copy """
        if isinstance(s,pipescript):
            dup = deepduplicate(self)
            return dup | s      # + or | are synonyms
        else:
            raise ValueError("the operand must be a pipescript")

    def __iadd__(self,s):
        """ overload += as pipe without copy """
        if isinstance(s,pipescript):
            return self | s      # + or | are synonyms
        else:
            raise ValueError("the operand must be a pipescript")

    def __mul__(self,ntimes):
        """ overload * as multiple pipes with copy """
        if isinstance(self,pipescript):
            res = deepduplicate(self)
            if ntimes>1:
                for n in range(1,ntimes): res += self
            return res
        else:
            raise ValueError("the operand must be a pipescript")
                        
    def __or__(self,s):
        """ overload | pipe """
        leftarg = deepduplicate(self)
        if isinstance(s,pipescript):
            leftarg.listscript = leftarg.listscript + s.listscript
            leftarg.listUSER = leftarg.listUSER + s.listUSER
            leftarg.name = leftarg.name + s.name
            for i in range(len(s)): s.executed[i] = False
            leftarg.executed = leftarg.executed + s.executed
            return leftarg
        if isinstance(s,(script,scriptobject,scriptobjectgroup)):
            rightarg = pipescript(s)
            rightname = str(s)
        else:
            ValueError("the operand should be a script, a script object or scriptobjectgroup")
        if rightarg.n>0:
            leftarg.listscript.append(rightarg.listscript[0])
            leftarg.listUSER.append(rightarg.listUSER[0])
            leftarg.name.append(rightname)
            leftarg.executed.append(False)
        return leftarg
        
    def __str__(self):
        """ string representation """
        return f"pipescript containing {self.n} scripts with {self.nrun} executed[*]"

    def __repr__(self):
        """ display method """
        line = "  "+"-"*12+":"+"-"*40
        if self.verbose:
            print("","Pipeline with %d scripts and" % self.n,
                  "D(STATIC:GLOBAL:LOCAL) DEFINITIONS",line,sep="\n")
        else:
            print(line)
        for i in range(len(self)):
            if self.executed[i]:
                state = "*"
            else:
                state = "-"
            print("%10s" % ("[%s]  %02d:" % (state,i)),
                  self.name[i],"with D(%2d:%2d:%2d)" % (
                       len(self.listscript[i].DEFINITIONS),
                       len(self.listscript[i].USER),
                       len(self.listUSER[i])                 )
                  )
        if self.verbose:
            print(line,"::: notes :::","p[i], p[i:j], p[[i,j]] copy pipeline segments",
                  "LOCAL: p.USER[i],p.USER[i].variable modify the user space of only p[i]",
                  "GLOBAL: p.scripts[i].USER.var to modify the user space from p[i] and onwards",
                  "STATIC: p.scripts[i].DEFINITIONS",
                  'p.rename(idx=range(2),name=["A","B"]), p.clear(idx=[0,3,4])',
                  "p.script(), p.script(idx=range(5)), p[0:5].script()","",sep="\n")
        else:
             print(line)   
        return str(self)        

    def __len__(self):
        """ len() method """
        return len(self.listscript)
        
    @property
    def n(self):
        """ number of scripts """
        return len(self)
    
    @property
    def nrun(self):
        """ number of scripts executed continuously from origin """
        n, nmax  = 0, len(self)
        while n<nmax and self.executed[n]: n+=1
        return n
    
    def __getitem__(self,idx):
        """ return the ith or slice element(s) of the pipe  """
        dup = deepduplicate(self)
        if isinstance(idx,slice):
            dup.listscript = dup.listscript[idx]
            dup.listUSER = dup.listUSER[idx]
            dup.name = dup.name[idx]
            dup.executed = dup.executed[idx]                    
        elif isinstance(idx,int):
            if idx<len(self):
                dup.listscript = dup.listscript[idx:idx+1]
                dup.listUSER = dup.listUSER[idx:idx+1]
                dup.name = dup.name[idx:idx+1]
                dup.executed = dup.executed[idx:idx+1]
            else:
                raise IndexError(f"the index in the pipe should be comprised between 0 and {len(self)-1}")
        else:
            raise IndexError("the index needs to be a slice or an integer")
        return dup
    
    def __setitem__(self,idx,s):
        """ 
            modify the ith element of the pipe
                p[4] = [] removes the 4th element
                p[4:7] = [] removes the elements from position 4 to 6
                p[2:4] = p[0:2] copy the elements 0 and 1 in positions 2 and 3
                p[[3,4]]=p[0]
        """
        if isinstance(s,(script,scriptobject,scriptobjectgroup)):
            dup = pipescript(s)
        elif isinstance(s,pipescript):
            dup = s
        elif s==[]:
            dup = []
        else:
            raise ValueError("the value must be a pipescript, script, scriptobject, scriptobjectgroup")
        if len(s)<1: # remove (delete)
            if isinstance(idx,slice) or idx<len(self):
                del self.listscript[idx]
                del self.listUSER[idx]
                del self.name[idx]
                del self.executed[idx]
            else:
                raise IndexError("the index must be a slice or an integer")
        elif len(s)==1: # scalar
            if isinstance(idx,int):
                if idx<len(self):
                    self.listscript[idx] = dup.listscript[0]
                    self.listUSER[idx] = dup.listUSER[0]
                    self.name[idx] = dup.name[0]
                    self.executed[idx] = False
                elif idx==len(self):
                    self.listscript.append(dup.listscript[0])
                    self.listUSER.append(dup.listUSER[0])
                    self.name.append(dup.name[0])
                    self.executed.append(False)
                else:
                    raise IndexError(f"the index must be ranged between 0 and {self.n}")
            elif isinstance(idx,list):
                for i in range(len(idx)):
                    self.__setitem__(idx[i], s) # call as a scalar
            elif isinstance(idx,slice):
                for i in range(*idx.indices(len(self)+1)):
                    self.__setitem__(i, s)
            else:
                raise IndexError("unrocognized index value, the index should be an integer or a slice")
        else: # many values
            if isinstance(idx,list): # list call à la Matlab
                if len(idx)==len(s):
                    for i in range(len(s)):
                        self.__setitem__(idx[i], s[i]) # call as a scalar
                else:
                    raise IndexError(f"the number of indices {len(list)} does not match the number of values {len(s)}")                    
            elif isinstance(idx,slice):
                ilist = list(range(*idx.indices(len(self)+len(s))))
                self.__setitem__(ilist, s) # call as a list
            else:
                raise IndexError("unrocognized index value, the index should be an integer or a slice")
                
    def rename(self,name="",idx=None):
        """ 
            rename scripts in the pipe
                p.rename(idx=[0,2,3],name=["A","B","C"])
        """
        if isinstance(name,list):
            if len(name)==len(self) and idx==None:
                self.name = name
            elif len(name) == len(idx):
                for i in range(len(idx)):
                    self.rename(name[i],idx[i])
            else:
                IndexError(f"the number of indices {len(idx)} does not match the number of names {len(name)}")
        elif idx !=None and idx<len(self) and name!="":
            self.name[idx] = name
        else:
            raise ValueError("provide a non empty name and valid index")
            
    def clear(self,idx=None):
        if len(self)>0:
            if idx==None:
                for i in range(len(self)):
                    self.clear(i)
            else:
                if isinstance(idx,(range,list)):
                    for i in idx:
                        self.clear(idx=i)
                elif isinstance(idx,int) and idx<len(self):
                    self.executed[idx] = False
                else:
                    raise IndexError(f"the index should be ranged between 0 and {self.n-1}")
            if not self.executed[0]:
                self.globalscript = None
                self.cmd = ""
                

    def do(self,idx=None):
        """
            execute the pipeline or part of the pipeline
                cmd = p.do()
                cmd = p.do([0,2])
        """
        if len(self)>0:
            # ranges
            ntot = len(self)
            stop = ntot-1
            if (self.globalscript == None) or (self.globalscript == []) or not self.executed[0]:
                start = 0
                self.cmd = ""
            else:
                start = self.nrun
            if idx == None: idx = range(start,stop+1)
            if isinstance(idx,range): idx = list(idx)
            if isinstance(idx,int): idx = [idx]
            start,stop = min(idx),max(idx)
            # do
            for i in idx:
                j = i % ntot
                if j==0:
                    self.globalscript = self.listscript[j]
                else:
                    self.globalscript = self.globalscript >> self.listscript[j]
                name = "  "+self.name[i]+"  "
                self.cmd += "\n\n#\t --- run step [%d/%d] --- [%s]  %20s\n" % \
                        (j,ntot-1,name.center(50,"="),"pipeline [%d]-->[%d]" %(start,stop))
                self.globalscript.USER = self.globalscript.USER + self.listUSER[j]
                self.cmd += self.globalscript.do()
                self.executed[i] = True
            return self.cmd
        else:
            return "# empty pipe - nothing to do"    
            

    def script(self,idx=None):
        """
            execute the pipeline or parts of the pipeline
                s = p.script()
                s = p.script([0,2])
        """
        s = script()
        s.name = "pipescript"
        s.description = "pipeline with %d scripts" % len(self)
        if len(self)>1:
            s.userid = self.name[0]+"->"+self.name[-1]
        elif len(self)==1:
            s.userid = self.name[0]            
        else:
            s.userid = "empty pipeline"
        s.TEMPLATE = script.header()+self.do(idx)
        s.DEFINITIONS = duplicate(self.globalscript.DEFINITIONS)
        s.USER = duplicate(self.globalscript.USER)
        return s
        
        
# %% Child classes of script sessions (to be derived)
# navigate with the outline tab through the different classes
#   globalsection()
#   initializesection()
#   geometrysection()
#   discretizationsection()
#   interactionsection()
#   integrationsection()
#   dumpsection()
#   statussection()
#   runsection()

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

    # example of scriptobject()
    b1 = scriptobject(name="bead 1",group = ["A", "B", "C"],filename='myfile1',forcefield=rigidwall())
    b2 = scriptobject(name="bead 2", group = ["B", "C"],filename = 'myfile1',forcefield=rigidwall())
    b3 = scriptobject(name="bead 3", group = ["B", "D", "E"],forcefield=solidfood())
    b4 = scriptobject(name="bead 4", group = "D",beadtype = 1,filename="myfile2",forcefield=water())

    collection = b1+b2+b3+b4
    grp_typ1 = collection.select(1)
    grpB = collection.group.B
    
    collection.interactions
    
    # main example of script()
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
    
    # # all sections as a single script
    myscript = G+c+g+d+b+i+t+d+s+r
    p = pipescript()
    p | i
    p = collection | G
    p | i
    p[0]
    q = p | p
    q[0] = []
    p[0:1] = q[0:1]
    print("\n"*4,'='*80,'\n\n this is the full script\n\n','='*80,'\n')
    print(myscript.do())
    
    # pipe full demo
    p = G | c | g | d | b | i | t | d | s | r
    p.rename(["G","c","g","d","b","i","t","d","s","r"])
    cmd = p.do([0,1,4,7])
    sp = p.script([0,1,4,7])
    r = collection | p
    p[0:2]=p[0]*2