#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Synopsis of dforcefield Class
=============================

The `dforcefield` class enables the dynamic definition of forcefields at runtime, in contrast 
to the static material customization approach in the `forcefield` class. While the `forcefield` 
class relies on predefined material classes within a library (e.g., `pizza.generic`) and supports 
inheritance to manage complex materials, the `dforcefield` class allows the flexible and rapid 
creation of forcefields without requiring a predefined library. This makes `dforcefield` ideal 
for rapid prototyping and experimentation with forcefield models.

Key Differences Between `forcefield` and `dforcefield`:
-------------------------------------------------------
- **forcefield**: 
    - New materials are defined using classes within classes, often managed via a 
      material library (e.g., `pizza.generic`).
    - Supports inheritance to manage complex materials and extend forcefield functionality.
    - Primarily used for well-defined, library-based material management.
    
- **dforcefield**:
    - Enables the definition of forcefields dynamically at runtime, without the need 
      for a predefined library.
    - Ideal for rapid prototyping of forcefields and testing new configurations on the fly.
    - Attributes like `parameters`, `beadtype`, and `userid` can be modified at runtime 
      and automatically injected into the base forcefield class for flexible interaction modeling.

Key Attributes:
---------------
- `base_class` (forcefield): The base forcefield class (e.g., `ulsph`) from which the 
  forcefield behavior is inherited.
- `parameters` (parameterforcefield): Stores the parameters for interaction evaluations, 
  which are dynamically injected into the `base_class`.
- `beadtype` (int): The bead type associated with the `dforcefield` instance, used in 
  forcefield calculations.
- `userid` (str): A unique identifier for the forcefield instance, used in interaction commands.
- `name` (str): A human-readable name for the `dforcefield` instance.
- `description` (str): A brief description of the `dforcefield` instance.
- `version` (float): The version number of the `dforcefield` instance.

Key Methods:
------------
- `_inject_attributes()`: Injects `dforcefield` attributes (like `parameters`, `beadtype`, 
  and `userid`) into the `base_class` to ensure the base class operates with the correct 
  attributes.
- `pair_style(printflag=True)`: Delegates the pair style computation to the `base_class`, 
  ensuring it uses the current `dforcefield` attributes.
- `pair_diagcoeff(printflag=True, i=None)`: Delegates diagonal pair coefficient computation 
  to the `base_class`, with the option to override the bead type `i`.
- `pair_offdiagcoeff(o=None, printflag=True, i=None)`: Delegates off-diagonal pair coefficient 
  computation to the `base_class`, with the option to override the bead type `i` and 
  the interacting forcefield `o`.

Usage Example:
--------------
>>> # Create an instance of dforcefield with ulsph as the base class
>>> dynamic_water = dforcefield(ulsph, beadtype=1, userid="dynamic_water", USER=parameterforcefield(rho=1000))
>>> dynamic_water.pair_style()  # Outputs the pair style command using dforcefield's attributes
lj/cut
>>> dynamic_water.pair_diagcoeff()  # Outputs the diagonal pair coefficient command
diag_coeff_command
>>> dynamic_water.pair_offdiagcoeff()  # Outputs the off-diagonal pair coefficient command
offdiag_coeff_command

>>> # Update parameters and see changes reflected in the base class
>>> dynamic_water.parameters = parameterforcefield(rho=1200)
>>> dynamic_water.pair_style()  # Now reflects updated parameters
lj/cut


Created on Tue Sep 10 17:11:40 2024


Dependencies
------------
- Python 3.x
- LAMMPS
- Pizza3.pizza

Installation
------------
To use the Pizza3.pizza module, ensure that you have Python 3.x and LAMMPS installed. You can integrate the module into your project by placing the `region.py` file in your working directory or your Python path.

License
-------
This project is licensed under the terms of the GPLv3 license.

Contact
-------
For any queries or contributions, please contact the maintainer:
- Olivier Vitrac, Han Chen
- Email: olivier.vitrac@agroparistech.fr

"""

__project__ = "Pizza3"
__author__ = "Olivier Vitrac, Han Chen, Joseph Fine"
__copyright__ = "Copyright 2024"
__credits__ = ["Olivier Vitrac", "Han Chen", "Joseph Fine"]
__license__ = "GPLv3"
__maintainer__ = "Olivier Vitrac"
__email__ = "olivier.vitrac@agroparistech.fr"
__version__ = "0.99"



# INRAE\Olivier Vitrac - rev. 2024-09-10 (community)
# contact: olivier.vitrac@agroparistech.fr, han.chen@inrae.fr

# Revision history
# 2024-09-10 release candidate


# Dependencies
from pizza.private.struct import struct
from pizza.forcefield import parameterforcefield, forcefield, tlsph, ulsph, none


# %% Main class
class dforcefield:
    """
        The `dforcefield` class is a dynamic extension of a base forcefield class, enabling 
        inheritance and delegation of methods while dynamically managing forcefield-specific 
        attributes. This class is designed to integrate with a variety of forcefield models, 
        such as `ulsph`, and provides mechanisms for updating parameters, bead types, and user 
        identifiers at runtime.
        
        Attributes:
        -----------
        base_class : forcefield
            An instance of a forcefield subclass (e.g., `ulsph`), representing the base class
            from which forcefield behavior and methods are inherited.
        
        parameters : parameterforcefield
            An instance of `parameterforcefield` that stores the parameters for evaluating 
            interaction commands, which are dynamically injected into the base class.
        
        beadtype : int
            The bead type associated with the current `dforcefield` instance, which can be used 
            to override the bead type used in forcefield calculations.
        
        userid : str
            A unique identifier for the forcefield instance, used in interaction commands to 
            distinguish between different forcefield objects.
        
        name : str
            A human-readable name for the current forcefield instance.
        
        description : str
            A brief description of the forcefield instance.
        
        version : float
            The version number associated with the forcefield instance.
        
        Methods:
        --------
        _inject_attributes():
            Inject the attributes of the `dforcefield` instance (such as `parameters`, 
            `beadtype`, `userid`, etc.) into the base class. This ensures that the base class 
            operates with the correct data at all times.
            
        pair_style(printflag=True):
            Delegate the pair style computation to the `base_class`, ensuring that the 
            current attributes of the `dforcefield` instance are used.
        
        pair_diagcoeff(printflag=True, i=None):
            Delegate the diagonal pair coefficient computation to the `base_class`, ensuring 
            that the current attributes of the `dforcefield` instance are used. The bead type 
            can be overridden by passing the `i` parameter.
        
        pair_offdiagcoeff(o=None, printflag=True, i=None):
            Delegate the off-diagonal pair coefficient computation to the `base_class`, ensuring 
            that the current attributes of the `dforcefield` instance are used. The bead type 
            `i` and the interacting forcefield `o` can be overridden.
            
        __setattr__(attr, value):
            Override the default attribute setter to dynamically inject attributes into 
            the `base_class` whenever certain attributes (`parameters`, `beadtype`, `userid`, etc.) 
            are updated in the `dforcefield` instance.
        
        __getattr__(attr):
            If an attribute is not found in the `dforcefield` instance, this method checks if it 
            exists in the `parameters` object or the `base_class`, and returns it if found. This 
            allows for seamless access to attributes that may be part of the base forcefield model 
            or dynamically managed in `parameters`.
        
        Notes:
        ------
        - The `dforcefield` class is designed to wrap and extend existing forcefield models like 
          `ulsph`. It allows for dynamic inheritance, meaning that attributes like `parameters`, 
          `beadtype`, and `userid` can be modified at runtime and automatically propagated to 
          the base forcefield class.
        - Attribute injection ensures that whenever a relevant attribute in `dforcefield` is 
          updated, the corresponding attributes in the `base_class` are updated as well.
        - Methods such as `pair_style()`, `pair_diagcoeff()`, and `pair_offdiagcoeff()` are 
          dynamically delegated to the `base_class`, but operate using the attributes injected 
          from the `dforcefield` instance.
        
        Example Usage:
        --------------
        >>> # Create an instance of dforcefield using ulsph as the base class
        >>> dynamic_water = dforcefield(ulsph, beadtype=1, userid="dynamic_water", USER=parameterforcefield(rho=1000))
        >>> dynamic_water.pair_style()  # Delegates to ulsph.pair_style(), using dforcefield's attributes
        lj/cut
        >>> dynamic_water.pair_diagcoeff()  # Delegates to ulsph.pair_diagcoeff(), using dforcefield's attributes
        diag_coeff_command
        >>> dynamic_water.pair_offdiagcoeff()  # Delegates to ulsph.pair_offdiagcoeff(), using dforcefield's attributes
        offdiag_coeff_command
        
        >>> # Update parameters and see the changes reflected in the base class
        >>> dynamic_water.parameters = parameterforcefield(rho=1200)
        >>> dynamic_water.pair_style()  # Now uses updated parameters
        lj/cut
    """

    
    def __init__(self, base_class=None, beadtype=1, userid=None, USER=parameterforcefield(), **kwargs):
        """
        Dynamic forcefield class with dynamic base class inheritance and shorthand parameter access.
        Args:
            base_class (class): The base class to use (e.g., ulsph, tlsph, etc.).
            beadtype (int): The bead type identifier.
            userid (str): User ID for the material.
            USER (parameterforcefield): Custom parameters to override defaults.
            kwargs: Additional parameters passed to the base class.
        """
        # Ensure base_class is defined
        if base_class is None:
            raise ValueError("base_class must be defined (e.g., ulsph, tlsph).")
            
       # Ensure base_class is a valid subclass of forcefield
        if base_class is None or not issubclass(base_class, forcefield):
            raise ValueError("base_class must be a subclass of forcefield (e.g., ulsph, tlsph, none).")
            
        # Temporary flag to prevent injection during construction
        self._in_construction = True
            
        # Initialize base class without passing arguments if it doesn't accept any
        self.base_class = base_class() if callable(base_class) else None
        
        # Dynamically inherit name, description, etc.
        self.name = base_class.name + struct(material=self.__class__.__name__.lower())
        self.description = base_class.description + struct(material=f"{self.__class__.__name__.lower()} beads - SPH-like")
        self.userid = userid if userid else self.__class__.__name__.lower()
        self.version = 0.1
        
        # Initialize beadtype and parameters
        self.beadtype = beadtype
        self.parameters = USER
        
        # End of construction, enable injection
        self._in_construction = False
        
        # Inject dforcefield attributes into the base class
        self._inject_attributes()
        
        
    def _inject_attributes(self):
        """Inject dforcefield attributes into the base class, bypassing __setattr__."""
        if not self._in_construction:  # Prevent injection during construction
            self.base_class.__dict__.update({
                'name': self.name,
                'description': self.description,
                'beadtype': self.beadtype,
                'userid': self.userid,
                'version': self.version,
                'parameters': self.parameters
        })
            

    def __getattr__(self, attr):
        """
        Shorthand for accessing parameters or base class attributes. 
        If an attribute is not found in the instance, check in self.parameters.
        """
        if attr in self.__dict__:
            return self.__dict__[attr]
        elif hasattr(self.parameters, attr):  # Check if the attribute exists in parameters
            return getattr(self.parameters, attr)
        elif hasattr(self.base_class, attr):  # Check if the attribute exists in the base class
            return getattr(self.base_class, attr)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attr}'")


    def __setattr__(self, attr, value):
        """
        Shorthand for setting parameters. If setting an attribute that exists in self.parameters,
        update the parameters object instead.
        """
        # Handle setting of base attributes like name, description, beadtype, parameters, userid, version
        if attr in {'name', 'description', 'beadtype', 'parameters', 'userid', 'version'}:
            self.__dict__[attr] = value
            # Update the base_class after setting the attribute
            self._inject_attributes()
        # Handle setting of parameter attributes dynamically
        elif 'parameters' in self.__dict__ and attr in self.parameters:
            setattr(self.parameters, attr, value)
        else:
            super().__setattr__(attr, value)
        # If construction is finished, inject attributes into the base class
        if not self._in_construction and attr in {'name', 'description', 'beadtype', 'parameters', 'userid', 'version'}:
            self._inject_attributes()
            
                
    def __repr__(self):
        """
        Custom __repr__ method that indicates it is a dforcefield instance and provides information
        about the base class, name, and parameters dynamically.
        """
        base_class_name = self.base_class.__class__.__name__ if self.base_class else "None"
        # Generate the name table dynamically (iterating over key-value pairs)
        sep = "  "+"-"*20+":"+"-"*30
        name_table = sep + "[ BEADTYPE (can be changed) ]\n"
        key = "beadtype"
        name_table += f"  {key:<20}: {self.beadtype}\n"
        name_table += sep + "[ FF CLASS (cannot be changed) ]\n"
       # Generate the name table dynamically (iterating over key-value pairs)
        for key, value in self.name.items():
            name_table += f"  {key:<20}: {value}\n"  # Align the keys and values dynamically
        # Generate the parameters table dynamically (iterating over key-value pairs)
        parameters_table = sep+ "[ PARAMS (can be changed) ]\n"
        for key, value in self.parameters.items():  # Assuming parameters is a class with __dict__
            parameters_table += f"  {key:<20}: {value}\n"  # Align the keys and values dynamically
        parameters_table += sep+f" >> {len(self.parameters)} definitions\n"
    
        # Combine the name and parameters table with a general instance representation
        print(f'\ndforcefield "{self.userid}" derived from "{base_class_name}"\n{name_table}{parameters_table}\n')
        print(' which reads as forcefield script:\n')
        self.base_class.__repr__()
        return self.__str__()
    
        
    def __str__(self):
        base_class_name = self.base_class.__class__.__name__ if self.base_class else "None"
        return f"<dforcefield instance with base class: {base_class_name}, userid: {self.userid}, beadtype: {self.beadtype}>"
    

    def pair_style(self, printflag=True):
        """Delegate pair_style to the base class, ensuring it uses the correct attributes."""
        return self.base_class.pair_style(printflag)
    
    
    def pair_diagcoeff(self, printflag=True, i=None):
        """Delegate pair_diagcoeff to the base class, ensuring it uses the correct attributes."""
        return self.base_class.pair_diagcoeff(printflag, i)
    
    
    def pair_offdiagcoeff(self, o=None, printflag=True, i=None):
        """Delegate pair_offdiagcoeff to the base class, ensuring it uses the correct attributes."""
        return self.base_class.pair_offdiagcoeff(o, printflag, i)

# %% DEBUG
# ===================================================
# main()
# ===================================================
# for debugging purposes (code called as a script)
# the code is called from here
# ============================
if __name__ == '__main__':
    
    # ---------------------------------------------------------------
    # The examples below reconstruct dynamycally the FF:
    #       * water from pizza.forcefield.water()
    #       * solidfood from pizza.forcefield.solidfood()
    #       * salt from pizza.forcefield.saltTLSPH()
    #       * rigidwall from pizza.forcefield.rigidwall()
    # ---------------------------------------------------------------
    
    # Test dynamic water class using ulsph as the base class
    dynamic_water = dforcefield(
        base_class=ulsph,
        beadtype=1,
        userid="dynamic_water",
        USER=parameterforcefield(
            rho=1000,
            c0=10.0,
            q1=1.0,
            Cp=1.0,
            taitexponent=7,
            contact_scale=1.5,
            contact_stiffness="2.5*${c0}^2*${rho}"
        )
    )
    print(f"Water parameters: {dynamic_water.parameters}")
    print(f"Water name: {dynamic_water.name}")
    print(f"Water Cp: {dynamic_water.Cp}")
    dynamic_water
    
    # Test dynamic solidfood class using tlsph as the base class
    dynamic_solidfood = dforcefield(
        base_class=tlsph,
        beadtype=2,
        userid="dynamic_solidfood",
        USER=parameterforcefield(
            rho=1000,
            c0=10.0,
            E="5*${c0}^2*${rho}",
            nu=0.3,
            q1=1.0,
            q2=0.0,
            Hg=10.0,
            Cp=1.0,
            sigma_yield="0.1*${E}",
            hardening=0,
            contact_scale=1.5,
            contact_stiffness="2.5*${c0}^2*${rho}"
        )
    )
    print(f"Solidfood parameters: {dynamic_solidfood.parameters}")
    print(f"Solidfood name: {dynamic_solidfood.name}")
    repr(dynamic_solidfood)
    
    # Test dynamic saltTLSPH class using tlsph as the base class
    dynamic_salt = dforcefield(
        base_class=tlsph,
        beadtype=3,
        userid="dynamic_salt",
        USER=parameterforcefield(
            rho=1000,
            c0=10.0,
            E="5*${c0}^2*${rho}",
            nu=0.3,
            q1=1.0,
            q2=0.0,
            Hg=10.0,
            Cp=1.0,
            sigma_yield="0.1*${E}",
            hardening=0,
            contact_scale=1.5,
            contact_stiffness="2.5*${c0}^2*${rho}"
        )
    )
    print(f"Salt TLSPH parameters: {dynamic_salt.parameters}")
    print(f"Salt TLSPH name: {dynamic_salt.name}")
    repr(dynamic_salt)
    
    # Test dynamic rigidwall class using none as the base class
    dynamic_rigidwall = dforcefield(
        base_class=none,  # Assuming a class `none` exists
        beadtype=4,
        userid="dynamic_rigidwall",
        USER=parameterforcefield(
            rho=3000,
            c0=10.0,
            contact_scale=1.5,
            contact_stiffness="2.5*${c0}^2*${rho}"
        )
    )
    print(f"Rigidwall parameters: {dynamic_rigidwall.parameters}")
    print(f"Rigidwall name: {dynamic_rigidwall.name}")
    repr(dynamic_rigidwall)

