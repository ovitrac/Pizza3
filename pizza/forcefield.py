#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Synopsis of forcefield Class
============================

The `forcefield` class defines the core behavior for managing inter-particle interactions 
in molecular dynamics simulations or similar physics-based models. It provides methods 
to calculate interaction parameters, including pair styles, diagonal pair coefficients, 
and off-diagonal pair coefficients, which are crucial for forcefield models.

Key Attributes:
---------------
- `PAIR_STYLE` (str): Defines the pair style command for the forcefield interactions.
- `PAIR_DIAGCOEFF` (str): Defines the command for calculating diagonal pair coefficients.
- `PAIR_OFFDIAGCOEFF` (str): Defines the command for calculating off-diagonal pair coefficients.
- `parameters` (parameterforcefield): Stores the parameters used for interaction evaluations.
- `beadtype` (int): The bead type used in the forcefield model.
- `userid` (str): A unique identifier for the forcefield instance.

Key Methods:
------------
- `pair_style(printflag=True)`: Returns the pair style command based on the current 
  `parameters`, `beadtype`, and `userid`.
- `pair_diagcoeff(printflag=True, i=None)`: Returns the diagonal pair coefficient command 
  based on the current bead type `i` and `userid`. The bead type can be overridden.
- `pair_offdiagcoeff(o=None, printflag=True, i=None)`: Returns the off-diagonal pair 
  coefficient command for interactions between two bead types or forcefield objects. 
  The bead type `i` and the interacting forcefield `o` can be specified or overridden.



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
                  self.name.material"] = "short of the material"
                  self.description.material"] = "full description"
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

__project__ = "Pizza3"
__author__ = "Olivier Vitrac"
__copyright__ = "Copyright 2022"
__credits__ = ["Olivier Vitrac"]
__license__ = "GPLv3"
__maintainer__ = "Olivier Vitrac"
__email__ = "olivier.vitrac@agroparistech.fr"
__version__ = "0.99"


# INRAE\Olivier Vitrac - rev. 2022-09-10
# contact: olivier.vitrac@agroparistech.fr

# History
# 2022-02-12 early version
# 2022-02-13 release candidate
# 2022-02-20 made compatible with the update private.struct.py
# 2022-02-28 fix class inheritance with mutable type, update is carried with + and struct()
# 2022-03-02 fix off-diagonal order for i,j
# 2022-03-19 standardized pizza path
# 2022-04-16 add saltTLSPH() forcefield in the material library, and document it better
# 2022-05-16 force sortdefintions for + and += with parameterforcefield()
# 2022-05-17 direct use of pizza.private.struct.paramauto()
# 2023-07-25 fix forcefield (deepduplicate instead of duplicate)
# 2024-09-10 updated documentation for pizza.forcefield (to be read along with pizza.dforcefield)

# %% Dependencies
import types
# All forcefield parameters are stored à la Matlab in a structure
from pizza.private.struct import struct,paramauto


# %% Parent class (not to be called directly)
# Note that some attributes are stored in the instances but in the class itself
#   recommendation 1: Recreate/derive a class when possible
#   recommendation 2: __dict__ list only properties in the instance,
#                     use getallattributes() to see all attributes

# container of forcefield parameters
class parameterforcefield(paramauto):
    """ class of forcefields parameters, derived from param
        note that conctanating two forcefields force them
        to to be sorted
    """
    _type = "FF"
    _fulltype = "forcefield"
    _ftype = "parameter"
    _maxdisplay = 80


# core class
class forcefield():
    """
    The `forcefield` class represents the core implementation of a forcefield model, 
    defining interaction parameters and coefficients for simulations. This class provides
    methods to handle pair styles, diagonal pair coefficients, and off-diagonal pair coefficients,
    which are essential for simulating inter-particle interactions in molecular dynamics or 
    other physics-based simulations.

    Attributes:
    -----------
    PAIR_STYLE : str
        The default pair style command for the forcefield interactions.
        
    PAIR_DIAGCOEFF : str
        The default command for calculating diagonal pair coefficients.

    PAIR_OFFDIAGCOEFF : str
        The default command for calculating off-diagonal pair coefficients.

    parameters : parameterforcefield
        An instance of `parameterforcefield` that stores the parameters for 
        evaluating interaction commands.

    beadtype : int
        The bead type associated with the current forcefield instance.
        
    userid : str
        A unique identifier for the forcefield instance, used in interaction commands.
    
    Methods:
    --------
    pair_style(printflag=True):
        Generate and return the pair style command based on the current parameters,
        beadtype, and userid.

    pair_diagcoeff(printflag=True, i=None):
        Generate and return the diagonal pair coefficients based on the current parameters,
        beadtype, and userid. The bead type `i` can be overridden with an optional argument.

    pair_offdiagcoeff(o=None, printflag=True, i=None):
        Generate and return the off-diagonal pair coefficients between two different 
        bead types or forcefield objects. The bead type `i` can be overridden, and the 
        interaction with another forcefield object `o` can also be specified.
    
    Notes:
    ------
    - This class is intended to be extended by specific forcefield types such as `ulsph`.
    - The parameters used in the interaction commands are dynamically evaluated using 
      the `parameterforcefield` class, which provides the required values during runtime.
    """

    # Main attributes (instance independent)
    name = struct(forcefield="undefined", style="undefined", material="undefined")
    description = struct(forcefield="missing", style="missing", material="missing")
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
        stamp = self.name.forcefield+":"+self.name.style+":"+self.name.material
        self.printheader("%s | version=%0.3g" % (self.userid,self.version),filler="=")
        print("  Bead of type %d = [%s]" % (self.beadtype,stamp))
        print(self.parameters)
        self.printheader("description",filler=".")
        print("\t# \t%s" % self.description.forcefield)
        print("\t# \t%s" % self.description.style)
        print("\t# \t%s" % self.description.material)
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
        """
        Generate and return the pair style command for the current forcefield instance.
        
        The method evaluates the pair style based on the interaction parameters stored 
        in the `parameters` attribute, and formats the command using the bead type 
        (`beadtype`) and user identifier (`userid`).
        
        Parameters:
        -----------
        printflag : bool, optional, default=True
            If True, the generated pair style command will be printed to the console.
        
        Returns:
        --------
        str
            The formatted pair style command string.
        """
        cmd = self.parameters.formateval(self.PAIR_STYLE)
        cmd = cmd.replace("[comment]","{comment}").format(comment=("[%d:%s]" % (self.beadtype,self.userid)))
        if printflag: print(cmd)
        return cmd
    

    def pair_diagcoeff(self,printflag=True,i=None):
        """
        Generate and return the diagonal pair coefficients for the current forcefield instance.

        This method evaluates the diagonal pair coefficients based on the interaction 
        parameters, the bead type (`beadtype`), and the user identifier (`userid`).
        The bead type `i` can be overridden by passing it as an argument.

        Parameters:
        -----------
        printflag : bool, optional, default=True
            If True, the generated diagonal pair coefficient command will be printed to the console.
        i : int, optional
            The bead type to be used for evaluating the diagonal pair coefficients. If not provided, 
            the current bead type of the instance (`self.beadtype`) will be used.

        Returns:
        --------
        str
            The formatted diagonal pair coefficient command string.
            diagonal pair_coeff from FFi.pair_diagcoeff(), FFi.pair_diagcoeff(i=override value)
        """
        if i==None: i = self.beadtype
        cmd = self.parameters.formateval(self.PAIR_DIAGCOEFF) % (i,i)
        cmd = cmd.replace("[comment]","{comment}").format(comment=("[%d:%s x %d:%s]" % (i,self.userid,i,self.userid)))
        if printflag: print(cmd)
        return cmd
    

    def pair_offdiagcoeff(self,o=None,printflag=True,i=None):
        """
        Generate and return the off-diagonal pair coefficients for the current forcefield instance.

        This method evaluates the off-diagonal pair coefficients between two different bead types 
        or forcefield objects, and formats the command using the interaction parameters, bead type, 
        and user identifier. The bead type `i` can be overridden, and the interaction with another 
        forcefield object `o` can also be specified.

        Parameters:
        -----------
        o : forcefield or int, optional
            The second forcefield object or bead type to be used for calculating off-diagonal 
            pair coefficients. If not provided, the method will assume interactions between 
            beads of the same type.
        printflag : bool, optional, default=True
            If True, the generated off-diagonal pair coefficient command will be printed to the console.
        i : int, optional
            The bead type to be used for the current forcefield instance. If not provided, 
            the current bead type of the instance (`self.beadtype`) will be used.

        Returns:
        --------
        str
            The formatted off-diagonal pair coefficient command string.
            off-diagonal pair_coeff from FFi.pair_offdiagcoeff(FFj), FFi.pair_offdiagcoeff(FFj,i=override value)

        Raises:
        -------
        IndexError
            If the first argument `o` is not a forcefield object or an integer.
        """
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
        cmd = self.parameters.formateval(self.PAIR_OFFDIAGCOEFF) % (min(i,j),max(j,i))
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
    name = forcefield.name + struct(forcefield="LAMMPS:SMD")
    description = forcefield.description + struct(forcefield="LAMMPS:SMD - solid, liquid, rigid forcefields (continuum mechanics)")

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
    name = smd.name + struct(style="ulsph")
    description = smd.description + struct(style="SMD:ULSPH - updated Langrangian for fluids - SPH-like")

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
    """ SMD:TLSPH forcefield (total Lagrangian) """
    name = smd.name + struct(syle="tlsph")
    description = smd.description + struct(style="SMD:TLSPH - total Langrangian for solids")

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
    name = smd.name + struct(style="none")
    description = smd.description + struct(style="no interactions")

    # style definition (LAMMPS code between triple """)
    PAIR_DIAGCOEFF = """
    # [comment] Diagonal pair coefficient tlsph
    pair_coeff      %d %d none
    """
    PAIR_OFFDIAGCOEFF = """
    # [comment] Off-diagonal pair coefficient (generic)
    pair_coeff      %d %d smd/hertz ${contact_stiffness}
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
#           self.name.material"] = "short of the material"
#           self.description.material"] = "full description"
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
    """ water material (smd:ulsph): generic water model
            water()
            water(beadtype=index, userid="myfluid", USER=...)

            override any propery with USER.parameter (set only the parameters you want to override)
                USER.rho: density in kg/m3 (default=1000)
                USER.c0: speed of the sound in m/s (default=10.0)
                USER.q1: standard artificial viscosity linear coefficient (default=1.0)
                USER.Cp: heat capacity of material -- not used here (default=1.0)
                USER.contact_scale: scaling coefficient for contact (default=1.5)
                USER.contact_stiffness: contact stifness in Pa (default="2.5*${c0}^2*${rho}")
    """
    name = ulsph.name + struct(material="water")
    description = ulsph.description + struct(material="water beads - SPH-like")
    userid = 'water'
    version = 0.1

    # constructor (do not forgert to include the constuctor)
    def __init__(self, beadtype=1, userid=None, USER=parameterforcefield()):
        """ water forcefield:
            water(beadtype=index, userid="myfluid") """
        if userid!=None: self.userid = userid
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
            ) + USER # update with user properties if any

# END MATERIAL: WATER ==========================================


# BEGIN MATERIAL: SOLID FOOD ========================================
class solidfood(tlsph):
    """ solidfood material (smd:tlsph): model solid food object
            solidfood()
            solidfood(beadtype=index, userid="myfood", USER=...)

            override any propery with USER.property=value (set only the parameters you want to override)
                USER.rho: density in kg/m3 (default=1000)
                USER.c0: speed of the sound in m/s (default=10.0)
                USER.E: Young's modulus in Pa (default="5*${c0}^2*${rho}")
                USER.nu: Poisson ratio (default=0.3)
                USER.q1: standard artificial viscosity linear coefficient (default=1.0)
                USER.q2: standard artificial viscosity quadratic coefficient (default=0)
                USER.Hg: hourglass control coefficient (default=10.0)
                USER.Cp: heat capacity of material -- not used here (default=1.0)
                USER.sigma_yield: plastic yield stress in Pa (default="0.1*${E}")
                USER.hardening: hardening parameter (default=0)
                USER.contact_scale: scaling coefficient for contact (default=1.5)
                USER.contact_stiffness: contact stifness in Pa (default="2.5*${c0}^2*${rho}")
    """
    name = tlsph.name + struct(material="solidfood")
    description = tlsph.description + struct(material="food beads - solid behavior")
    userid = 'solidfood'
    version = 0.1

    # constructor (do not forgert to include the constuctor)
    def __init__(self, beadtype=1, userid=None, USER=parameterforcefield()):
        """ food forcefield:
            solidfood(beadtype=index, userid="myfood") """
        # super().__init__()
        if userid!=None: self.userid = userid
        self.beadtype = beadtype
        self.parameters = parameterforcefield(
            # food-food interactions
            rho = 1000,
            c0 = 10.0,
            E = "5*${c0}^2*${rho}",
            nu = 0.3,
            q1 = 1.0,
            q2 = 0.0,
            Hg = 10.0,
            Cp = 1.0,
            sigma_yield = "0.1*${E}",
            hardening = 0,
            # hertz contacts
            contact_scale = 1.5,
            contact_stiffness = "2.5*${c0}^2*${rho}"
            ) + USER # update with user properties if any

# END MATERIAL: SOLID FOOD ==========================================


# BEGIN MATERIAL: SALT TLSPH ========================================
class saltTLSPH(tlsph):
    """ SALTLSPH (smd:tlsph): ongoing "salting" beadtype for rheology control
            saltTLSPH()
            saltTLSPH(beadtype=index, userid="salt", USER=...)

            override any property with USER.property = value
    """
    name = tlsph.name + struct(material="solidfood")
    description = tlsph.description + struct(material="food beads - solid behavior")
    userid = '"salt"'
    version = 0.1

    # constructor (do not forgert to include the constuctor)
    def __init__(self, beadtype=1, userid=None, USER=parameterforcefield()):
        """ saltTLSPH forcefield:
            saltTLSPH(beadtype=index, userid="salt") """
        # super().__init__()
        if userid!=None: self.userid = userid
        self.beadtype = beadtype
        self.parameters = parameterforcefield(
            # food-food interactions
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
            ) + USER # update with user properties if any

# END MATERIAL: SOLID FOOD ==========================================



# BEGIN MATERIAL: RIGID WALLS ========================================
class rigidwall(none):
    """ rigid walls (smd:none):
            rigidwall()
            rigidwall(beadtype=index, userid="wall", USER=...)

            override any propery with USER.parameter (set only the parameters you want to override)
                USER.rho: density in kg/m3 (default=3000)
                USER.c0: speed of the sound in m/s (default=10.0)
                USER.contact_scale: scaling coefficient for contact (default=1.5)
                USER.contact_stiffness: contact stifness in Pa (default="2.5*${c0}^2*${rho}")
    """
    name = none.name + struct(material="walls")
    description = none.description + struct(material="rigid walls")
    userid = 'solidfood'
    version = 0.1

    # constructor (do not forgert to include the constuctor)
    def __init__(self, beadtype=1, userid=None, USER=parameterforcefield()):
        """ rigidwall forcefield:
            rigidwall(beadtype=index, userid="mywall") """
        # super().__init__()
        if userid!=None: self.userid = userid
        self.beadtype = beadtype
        self.parameters = parameterforcefield(
            rho = 3000,
            c0 = 10.0,
            contact_stiffness = '2.5*${c0}^2*${rho}',
            contact_scale = 1.5
            ) + USER # update with user properties if any


# END MATERIAL: RIGID WALLS ==========================================


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
