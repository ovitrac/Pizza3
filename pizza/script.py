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
        


Created on Sat Feb 19 11:00:43 2022

@author: olivi
"""

# INRAE\Olivier Vitrac - rev. 2022-02-19
# contact: olivier.vitrac@agroparistech.fr


# Revision history
# 2022/02/20 RC with documentation and 10 section templates

# %% Dependencies
import types
# All forcefield parameters are stored à la Matlab in a structure
from private.struct import param


# %% Parent class (not to be called directly)
# container of script definitions
class scriptdata(param):
    """ class of script parameters """
    _type = "SD"
    _fulltype = "script data"
    _ftype = "definition"
     
# core class (please derive this class when you use it, do not alter it)
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
        
        Use the print() and the method do() to get the script interpreted
        
        DEFINITIONS can be pretified using DEFINITIONS.generator()
        
        Variables can extracted from a template using TEMPLATE.scan()
        
        
    """
    type = "script"                         # type (class name)
    name = "empty script"                   # name
    description = "it is an empty script"   # description
    position = 0                            # 0 = root
    section = 0                             # section (0=undef)
    userid = "undefined"                    # user name
    version = 0                             # version
    verbose = False                         # set it to True to force verbosity            
    
    SECTIONS = ["NONE","GLOBAL","INITIALIZE","GEOMETRY","DISCRETIZATION",
                "BOUNDARY","INTERACTIONS","INTEGRATION","DUMP","STATUS","RUN"]
    DEFINITIONS = scriptdata()
    TEMPLATE = """
        # empty LAMMPS script
    """
    
    
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
        cmd = self.DEFINITIONS.formateval(self.TEMPLATE)
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
    
    DEFINITIONS += MATERIALS # apprend MATERIALS data
    
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
    """ LAMMPS script: XXXX session """
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