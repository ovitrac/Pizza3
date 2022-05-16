#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

    generic() is a forcefield class helper (surrogate class)
    genericdata() is a data container for generic()
    
    > The class helper enables to defines general RULES based on formula
    > and to store GLOBAL parameters in instances
    > Methods operates with LOCAL parameters according to the recommended precedence
      GLOBAL + LOCAL + RULES (consistency is managed internally by a code analysis)
    
    > A typical use
    
        # CREATE AN INSTANCE and set GLOBAL PARAMETERS
        mylibrary = mygenericclass(name="myclass",param1=...)
        # CALL THE METHODS FOR THIS INSTANCE
        FF = mylibrary.forcefield(beadtype=1, userid="myliquid")
    
    > A typical USER class (inherited from generic) would look like
    
        class mygenericclass(generic):

            # static properties shared between all instances
            _version = xxx
            _description = "............"
            RULES = genericdata(.........) # class rules (please do not change them)

            # constructor method (required) to create an instance
            def __init__(self,name="...",
                         type=None,
                         param1=...,
                         param2=...,
                         ...
                         USER=genericdata()):

                super().__init__()
                self.name, self.type = name, type
                self.GLOBAL = genericdata(
                    param1 = param1, # parameter specific to mygenericclass()
                    param2 = param2, # idem
                    ...
                    ) + USER    # USER enables a unique/default container to be used
            
            def myforcefield(self,
                             beadtype=1,   # if needed
                             userid = "",  # user id
                             p1=...,       # first parameter
                             p2=...,       # second parameter         
                         USER=genericdata()):
                
                self.LOCAL = genericdata(
                    p1=p1,
                    p2=p2
                    )
                # manage inheritance, defintion consistency
                CURRENT = self.GLOBAL+self.LOCAL+self.RULES
                return someforcefield(beadtype=beadtype, userid=userid, USER=CURRENT)            

Created on Fri May 13 22:06:30 2022

@author: olivi
"""

__project__ = "Pizza3"
__author__ = "Olivier Vitrac"
__copyright__ = "Copyright 2022"
__credits__ = ["Olivier Vitrac"]
__license__ = "GPLv3"
__maintainer__ = "Olivier Vitrac"
__email__ = "olivier.vitrac@agroparistech.fr"
__version__ = "0.45"

# INRAE\Olivier Vitrac - rev. 2022-02-13
# contact: olivier.vitrac@agroparistech.fr

# History
# 2022-05-13 draft version (fields are not reordered)
# 2022-05-16 splitting CORE and USER classes and extended help
# 2022-05-16 full implementation of pizza.private.struct.sortdefinitions() in parameterforcefield()

# %% CORE DEFINITIONS (please)

# imports
from pizza.forcefield import parameterforcefield, water

# genericdata() class // please do not motify
class genericdata(parameterforcefield):
    """ generic data class to be used along with pizza.generic """
    _type = "gendata"        # object type
    _fulltype = "generic data" # full name
    _ftype = "item"        # field name
    _maxdisplay = 80
    
# generic() class // pease do not modify
class generic:
    """ generic helper class """
    _version = 0.1
    _description = "generic helper for forcefield parameterization"
    RULES = genericdata()
    
    def __init__(self):
        self.name = None
        self.type = None
 
    def __repr__(self):
        """ representation of generic() """
        id = ""
        if self.type is not None: id = str(self.type)+":"
        if self.name is not None: id = id+str(self.name)
        if id !="": id = '"'+id+'"'
        idstr = '  generic helper: %s\n\t (class "%s")' % (id,self.__class__)
        print("%s" % idstr)
        if len(self.GLOBAL):
            print("  with GLOBAL data")
            self.GLOBAL.__repr__()
        return idstr

# %% USER SECTION    

# USERSMD is a class derived from generic()
class USERSMD(generic):
    """ class helper for the module LAMMPS.USERSMD """
    
    # specific tules (add formula, missing parameters will be provided by GLOBAL or LOCAL)
    RULES = genericdata(
        # list here default forcefield rules (USER can overload these rules)
        c0 = "${vmax}/${Ma}",
        q1 = "8*${nu}/(${c0}*${h})",
        Cp = 1.0,
        contact_stiffness = '2.5*${c0}^2*${rho}'
        )

    # constructor of USERSMD (note that USER can override all definitions)        
    def __init__(self, name=None, type=None, h=0.1, Ma=0.1, vmax=0.1, USER = genericdata()):
        """ generic helper constructor """
        super().__init__()
        self.name = name
        self.type = type
        self.GLOBAL = genericdata(
            # variables which apply to all forcefields
            h = h,
            Ma = Ma,
            vmax = vmax
            ) + USER
        
    # forcefield derived from pizza.forcefield.water()
    def newtonianfluid(self, beadtype=1, userid = "", rho=1000.0, nu = 1e-6, mu = None, USER = genericdata()):
        """
            newtonianfluid() returns a parameterized ULSPH forcefield
            with prescribed viscosity (mu [Pa.s] or nu in [m2/s])
            and density (rho).
            Based on recommendations of J. Comput. Phys 1997, 136, 214–226
        """
        self.LOCAL = genericdata(
            rho = rho,
            nu = nu, # note that that nu is preferred as it is independent of rho
            mu = mu # dynamic viscosity (dependent on rho)
            ) + USER
        if self.LOCAL.nu is None: self.LOCAL.nu = self.LOCAL.mu / self.LOCAL.rho
        if self.LOCAL.nu is None: raise(ValueError("bad kinematic viscosity value: nu [m2/s]"))
        if self.LOCAL.mu is None: self.LOCAL.mu = self.LOCAL.nu * self.LOCAL.rho
        if userid == "":
            userid = print("newtonianfluid rho=%0.4g [kg/m3] and nu=%0.4g [m2/s]" \
                           % (self.LOCAL.rho,self.LOCAL.nu))
        # this simple line with + 
        # manages inheritance (the las definition as always higher precendence)
        # sorts definitions to enable execution (struct.sortdefinitions())
        # (see pizza.forcefield.parameterforcefield())
        CURRENT = self.GLOBAL+self.LOCAL+self.RULES
        return water(beadtype=beadtype, userid=userid, USER=CURRENT)
        

# %% DEBUG  
# ===================================================   
# main()
# ===================================================   
# for debugging purposes (code called as a script)
# the code is called from here
# ===================================================
if __name__ == '__main__':
    mylibrary = USERSMD(name="currentsim",h=1)
    w = mylibrary.newtonianfluid(beadtype=1, userid="fluid")
    print("\n"*2,w)

        

    