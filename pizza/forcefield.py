#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    --- forcefield methods for LAMMPS ---
    
    The superclass provides a collection of classes to define materials
    and forcefields. Note that the following hierarchy is used:
        > forcefield() is the top class (to be called directly)
        > customff(forcefield) defines a new forcefield so called customff
        > customstyle(customff) defines a pair-style applicable to customff
        > custommaterial(customstyle) defines a new material

    
    --- Material library (first implementations) ---
        
        w = water(beadtype=1, userid="fluid")
        w.parameters.Cp = 20
        print("\n"*2,w)

        f = solidfood(beadtype=2, userid="elastic")
        print("\n"*2,f)
        
        r = rigidwall(beadtype=3, userid="wall")
        print("\n"*2,r)

    
    --- Template to define a material ---
    
          class mymateral(myforcefield):
              userid = "short name"
              version = value
              def __init__(self, beadtype=1, userid=None):
                  super().__init__()
                  if userid!=None: self.userid = userid
                  self.name["material"] = "short of the material"
                  self.description["material"] = "full description"
                  self.beadtype = beadtype
                  self.parameters = parameterforcefield(
                      param1 = value1,
                      param2 = value2,
                      param3 = "math expression with ${param1, ${param2}"
                  )    

    
    --- Example of outputs | LAMMPS:SMD:tlsph:solidfood ---
        
        ========================== [ elastic | version=0.1 ] ===========================
        
          Bead of type 2 = [LAMMPS:SMD:tlsph:solidfood]
          -----------------:----------------------------------------
                        rho: 1000
                         c0: 10.0
                          E: 5*${c0}^2*${rho}
                         nu: 0.3
                         q1: 1.0
                         q2: 0.0
                         Hg: 10
                         Cp: 1.0
                sigma_yield: 0.1*${E}
                  hardening: 0
              contact_scale: 1.5
          contact_stiffness: 2.5*${c0}^2*${rho}
          -----------------:----------------------------------------
        forcefield object with 12 parameters
        
        ............................... [ description ] ................................
        
        	# 	LAMMPS:SMD - solid, liquid, rigid forcefields (continuum mechanics)
        	# 	SMD:TLSPH - total Langrangian for solids
        	# 	food beads - solid behavior
        
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ [ methods ] ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        replace FFi,FFj by your variable names <<<
        	To assign a type, use: FFi.beadtype = integer value
        	Use the methods FFi.pair_style() and FFi.pair_coeff(FFj)
        	Note for pairs: the caller object is i (FFi), the argument is j (FFj or j)
        
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ [ template ] ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        
            # [2:elastic] PAIR STYLE SMD
            pair_style      hybrid/overlay smd/ulsph *DENSITY_CONTINUITY *VELOCITY_GRADIENT *NO_GRADIENT_CORRECTION &
                                           smd/tlsph smd/hertz 1.5
            
        
            # [2:elastic x 2:elastic] Diagonal pair coefficient tlsph
            pair_coeff      2 2 smd/tlsph *COMMON 1000 500000.0 0.3 1.0 0.0 10 1.0 &
                            *STRENGTH_LINEAR_PLASTIC 50000.0 0 &
                            *EOS_LINEAR &
                            *END
            
        
            # [2:elastic x 1:none] Off-diagonal pair coefficient (generic)
            pair_coeff      2 1 smd/hertz 250000.0
            
        
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
    
    run this code by pressing <F5>
    
"""


# INRAE\Olivier Vitrac - rev. 2022-02-13
# contact: olivier.vitrac@agroparistech.fr

# History
# 2022-02-12 early version
# 2022-02-13 release candidate

# %% Dependencies
import types, math  # import math to authorize all math expressions in parameters
# All forcefield parameters are stored à la Matlab in a structure
from private.struct import struct


# %% Parent class (not to be called directly)
# Note that some attributes are stored in the instances but in the class itself
#   recommendation 1: Recreate/derive a class when possible
#   recommendation 2: __dict__ list only properties in the instance,
#                     use getallattributes() to see all attributes

# wrapper of struct class (used to rename type and ftype)
class parameterforcefield(struct):
    """ class of forcefields parameters """
    # override
    type = "forcefield"
    ftype = "parameter"
    
    # magic constructor
    def __init__(self,**kwargs):
        """ constructor """
        super().__init__(**kwargs)
    
    # formateval (note that ^ is accepted in exponents to be compatible with LAMMPS)
    def formateval(self,s):
        """ evaluate strings, format method wrapper """
        tmp = struct()
        for key,value in self.__dict__.items():
            if isinstance(value,str):
                tmp.setattr(key, eval(tmp.format(value.replace("^","**"))))
            else:
                tmp.setattr(key, value)
        return tmp.format(s)  
    
# core class
class forcefield():
    """ core forcefield class (not to be called directly) """
    
    # Main attributes (instance independent)
    name = {"forcefield":"undefined", "style":"undefined", "material":"undefined"}
    description = {"forcefield":"missing", "style":"missing", "material":"missing"}
    beadtype = 1  # default bead type
    parameters = parameterforcefield() # empty parameters object
    userid = "undefined"
    version = 0

    # print method for headers (static, no implicit argument)
    @staticmethod
    def printheader(txt,align="^",width=80,filler="~"):
        """ print header """
        if txt=="":
            print("\n"+filler*(width+6)+"\n")
        else:
            print(("\n{:"+filler+"{align}{width}}\n").format(' [ '+txt+' ] ', align=align, width=str(width)))
    
    # Display/representation method
    # The method provides full help for the end-user
    def __repr__(self):
        """ disp method """
        stamp = self.name["forcefield"]+":"+self.name["style"]+":"+self.name["material"]
        self.printheader("%s | version=%0.3g" % (self.userid,self.version),filler="=")
        print("  Bead of type %d = [%s]" % (self.beadtype,stamp))
        print(self.parameters)
        self.printheader("description",filler=".")
        print("\t# \t%s" % self.description["forcefield"])
        print("\t# \t%s" % self.description["style"])
        print("\t# \t%s" % self.description["material"])
        self.printheader("methods")
        print("\t   >>> replace FFi,FFj by your variable names <<<")
        print("\tTo assign a type, use: FFi.beadtype = integer value")
        print("\tUse the methods FFi.pair_style() and FFi.pair_coeff(FFj)")
        print("\tNote for pairs: the caller object is i (FFi), the argument is j (FFj or j)")
        self.printheader("template")
        self.pair_style()
        self.pair_diagcoeff()
        self.pair_offdiagcoeff()
        self.printheader("")
        return stamp

    # Extract attributes within the class
    def getallattributes(self):
        """ advanced method to get all attributes including class ones"""
        return {k: getattr(self, k) for k in dir(self) \
                if (not k.startswith('_')) and (not isinstance(getattr(self, k),types.MethodType))}

    # Forcefield Methods: pair_style(), pair_coeff()
    # the substitution of LAMMPS variables is carried out with the method
    # parameters.format() method implemented in struct and inherited by parameterforcefield()
    def pair_style(self,printflag=True):
        """ return pair_style from FFi.pair_style()"""
        cmd = self.parameters.formateval(self.PAIR_STYLE)
        cmd = cmd.replace("[comment]","{comment}").format(comment=("[%d:%s]" % (self.beadtype,self.userid)))
        if printflag: print(cmd)
        return cmd
    
    def pair_diagcoeff(self,printflag=True,i=None):
        """ return diagonal pair_coeff from FFi.pair_diagcoeff(), FFi.pair_diagcoeff(i=override value) """
        if i==None: i = self.beadtype
        cmd = self.parameters.formateval(self.PAIR_DIAGCOEFF) % (i,i)
        cmd = cmd.replace("[comment]","{comment}").format(comment=("[%d:%s x %d:%s]" % (i,self.userid,i,self.userid)))
        if printflag: print(cmd)
        return cmd

    def pair_offdiagcoeff(self,o=None,printflag=True,i=None):
        """ return off-diagonal pair_coeff from FFi.pair_offdiagcoeff(FFj), FFi.pair_offdiagcoeff(FFj,i=override value) """
        if i==None:
            i = self.beadtype
        if o==None:
            j = i
            oname = "none"
        elif isinstance(o,forcefield):
            j = o.beadtype
            oname = o.userid
        elif isinstance(o,float) or isinstance(o,int):
            j = int(o)
            oname = o.userid
        else:
            raise IndexError("the first argument should be j or a forcefield object")
        if j==i:
            if i>1: j=i-1
            else: j=i+1
        cmd = self.parameters.formateval(self.PAIR_OFFDIAGCOEFF) % (i,j)
        cmd = cmd.replace("[comment]","{comment}").format(comment=("[%d:%s x %d:%s]" % (i,self.userid,j,oname)))
        if printflag: print(cmd)
        return cmd
    

# %% Forecefield library
# This section can be upgraded by the end-user according to the manual of each style
# numerical value shoud be declared with variable/parameter with the same syntax as in LAMMPS.
# Note that you can copy directly LAMMPS code between triple """ for templates
# Main templates are strings: PAIR_STYLE, PAIR_DIAGCOEFF, PAIR_OFFDIAGCOEFF
#
# ${param} represents the variable called "param", and whose value will be defined
# in the parameters section of the material class as parameters.param = value
#
# use {comment} to add an automatic comment
# %d in PAIR_COEFF represent place holder for corresponding beadtype
#
# The subsitutions are managed by the parent class forcefield().

# BEGIN PAIR-STYLE FORCEFIELD ===========================
class smd(forcefield):
    """ SMD forcefield """
    
    # forcefield documentation
    def __init__(self):
        super().__init__()
        self.name["forcefield"] = "LAMMPS:SMD"
        self.description["forcefield"] = "LAMMPS:SMD - solid, liquid, rigid forcefields (continuum mechanics)"
    
    # forcefield definition (LAMMPS code between triple """)
    PAIR_STYLE = """
    # [comment] PAIR STYLE SMD
    pair_style      hybrid/overlay smd/ulsph *DENSITY_CONTINUITY *VELOCITY_GRADIENT *NO_GRADIENT_CORRECTION &
                                   smd/tlsph smd/hertz ${contact_scale}
    """
# END PAIR-STYLE FORCEFIELD ===========================


# BEGIN PAIR-COEFF FORCEFIELD ===========================
class ulsph(smd):
    """ SMD:ULSPH forcefield (updated Lagrangian) """
    
    # style documentation
    def __init__(self):
        super().__init__()
        self.name["style"] = "ulsph"
        self.description["style"] = "SMD:ULSPH - updated Langrangian for fluids - SPH-like"

    # style definition (LAMMPS code between triple """)
    PAIR_DIAGCOEFF = """
    # [comment] Pair diagonal coefficient ulsph
    pair_coeff      %d %d smd/ulsph *COMMON ${rho} ${c0} ${q1} ${Cp} 0 &
                    *EOS_TAIT ${taitexponent} &
                    *END
    """
    PAIR_OFFDIAGCOEFF = """
    # [comment] Off-diagonal pair coefficient (generic)
    pair_coeff      %d %d smd/hertz ${contact_stiffness}
    """
# END PAIR-COEFF FORCEFIELD ===========================


# BEGIN PAIR-COEFF FORCEFIELD ===========================
class tlsph(smd):
    """ SMD:TLSPH forcefield (updated Lagrangian) """
    
    # style documentation
    def __init__(self):
        super().__init__()
        self.name["style"] = "tlsph"
        self.description["style"] = "SMD:TLSPH - total Langrangian for solids"

    # style definition (LAMMPS code between triple """)
    PAIR_DIAGCOEFF = """
    # [comment] Diagonal pair coefficient tlsph
    pair_coeff      %d %d smd/tlsph *COMMON ${rho} ${E} ${nu} ${q1} ${q2} ${Hg} ${Cp} &
                    *STRENGTH_LINEAR_PLASTIC ${sigma_yield} ${hardening} &
                    *EOS_LINEAR &
                    *END
    """
    PAIR_OFFDIAGCOEFF = """
    # [comment] Off-diagonal pair coefficient (generic)
    pair_coeff      %d %d smd/hertz ${contact_stiffness}
    """
# END PAIR-COEFF FORCEFIELD ===========================


# BEGIN PAIR-COEFF FORCEFIELD ===========================
class none(smd):
    """ SMD:TLSPH forcefield (updated Lagrangian) """
    
    # style documentation
    def __init__(self):
        super().__init__()
        self.name["style"] = "none"
        self.description["style"] = "no interactions"

    # style definition (LAMMPS code between triple """)
    PAIR_DIAGCOEFF = """
    # [comment] Diagonal pair coefficient tlsph
    pair_coeff      %d %d none
    """
    PAIR_OFFDIAGCOEFF = """
    # [comment] Off-diagonal pair coefficient (generic)
    pair_coeff      %d %d none
    """
# END PAIR-COEFF FORCEFIELD ===========================


        
# %% Material library
# template:
#   class mymateral(myforcefield):
#       userid = "short name"
#       version = value
#       def __init__(self, beadtype=1, userid=None):
#           super().__init__()
#           if userid!=None: self.userid = userid
#           self.name["material"] = "short of the material"
#           self.description["material"] = "full description"
#           self.beadtype = beadtype
#           self.parameters = parameterforcefield(
#               param1 = value1,
#               param2 = value2,
#               param3 = "math expression with ${param1, ${param2}"
#           )
#
# ATTENTION: ${param1} and ${param2} cannot be used in an expression
#            if they do not have been prealably defined

# BEGIN MATERIAL: WATER ========================================
class water(ulsph):
    """ water material (smd:ulsph): use water() or water(beadtype=index, userid="myfluid") """
    
    userid = 'water'
    version = 0.1
    
    # constructor (do not forgert to include the constuctor)
    def __init__(self, beadtype=1, userid=None):
        """ water forcefield: water(beadtype=index, userid="myfluid") """
        super().__init__()
        if userid!=None: self.userid = userid
        self.name["material"] = "water"
        self.description["material"] = "water beads - SPH-like"
        self.beadtype = beadtype
        self.parameters = parameterforcefield(
            # water-water interactions
            rho = 1000,
            c0 = 10.0,
            q1 = 1.0,
            Cp = 1.0,
            taitexponent = 7,
            # hertz contacts
            contact_scale = 1.5,
            contact_stiffness = '2.5*${c0}^2*${rho}'
            )
        
# END MATERIAL: WATER ==========================================


# BEGIN MATERIAL: SOLID FOOD ========================================
class solidfood(tlsph):
    """ solidfood material (smd:tlsph): use food() or solidfood(beadtype=index, userid="myfood") """
    
    userid = 'solidfood'
    version = 0.1
    
    # constructor (do not forgert to include the constuctor)
    def __init__(self, beadtype=1, userid=None):
        """ food forcefield: solidfood(beadtype=index, userid="myfood") """
        super().__init__()
        if userid!=None: self.userid = userid
        self.name["material"] = "solidfood"
        self.description["material"] = "food beads - solid behavior"
        self.beadtype = beadtype
        self.parameters = parameterforcefield(
            # water-water interactions
            rho = 1000,
            c0 = 10.0,
            E = '5*${c0}^2*${rho}',
            nu = 0.3,
            q1 = 1.0,
            q2 = 0.0,
            Hg = 10,
            Cp = 1.0,
            sigma_yield = '0.1*${E}',
            hardening = 0,
            # hertz contacts
            contact_scale = 1.5,
            contact_stiffness = '2.5*${c0}^2*${rho}'
            )
        
# END MATERIAL: SOLID FOOD ==========================================



# BEGIN MATERIAL: SOLID FOOD ========================================
class rigidwall(none):
    """ rigid walls (smd:none): use rigidwalls() or solidfood(beadtype=index, userid="myfood") """
    
    userid = 'solidfood'
    version = 0.1
    
    # constructor (do not forgert to include the constuctor)
    def __init__(self, beadtype=1, userid=None):
        """ food forcefield: solidfood(beadtype=index, userid="mywall") """
        super().__init__()
        if userid!=None: self.userid = userid
        self.name["material"] = "walls"
        self.description["material"] = "rigid walls"
        self.beadtype = beadtype
        self.parameters = parameterforcefield(
            contact_scale = 1.5
            )

        
# END MATERIAL: SOLID FOOD ==========================================
# %% DEBUG  
# ===================================================   
# main()
# ===================================================   
# for debugging purposes (code called as a script)
# the code is called from here
# ===================================================
if __name__ == '__main__':
    w = water(beadtype=1, userid="fluid")
    w.parameters.Cp = 20
    print("\n"*2,w)
    f = solidfood(beadtype=2, userid="elastic")
    print("\n"*2,f)
    r = rigidwall(beadtype=3, userid="wall")
    print("\n"*2,r)