#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Synopsis of `dforcefield` Class
===============================

The `dforcefield` class enables the dynamic creation and modification of forcefields at runtime,
in contrast to the static material customization approach used in the `forcefield` class.
Whereas the `forcefield` class relies on predefined material classes (e.g., in `pizza.generic`)
and supports inheritance to manage complex materials, `dforcefield` allows for flexible and
rapid creation of forcefields without a predefined library. This makes `dforcefield` ideal for
prototyping and experimenting with forcefield models.

The class seamlessly integrates both static and dynamic forcefields, which can be used interchangeably 
to define objects built with atoms, set the interactions between those objects, and generate the 
equivalent scripts. This flexibility enables users to choose between dynamic instances (`dforcefield`) 
and static classes (`forcefield`) for defining `scriptobject` interactions.

Moreover, dynamic forcefields can also be defined using methods from `generic` classes. These 
`generic` classes allow creating high-level forcefields dynamically, providing another layer of 
customization that can be combined with both static and dynamic forcefields.

Key Differences Between `forcefield`, `generic`, and `dforcefield`:
-------------------------------------------------------------------
- **`forcefield`**:
    - New materials are defined using classes, often within a material library (e.g., `pizza.generic`).
    - Supports inheritance to manage complex materials and extend functionality.
    - Primarily used for well-defined, library-based material management.
    
- **`generic`**:
    - Provides high-level forcefield definitions via methods that can be dynamically called.
    - These dynamic definitions can be used interchangeably with static forcefields.
    - Suitable for defining specialized forcefields on the fly without modifying the core library.

- **`dforcefield`**:
    - Enables dynamic definition of forcefields at runtime without needing a predefined library.
    - Ideal for rapid prototyping and testing new configurations on the fly.
    - Attributes like `parameters`, `beadtype`, and `userid` can be modified at runtime and 
      automatically injected into the base forcefield class for flexible interaction modeling.
    - Provides a method, `scriptobject()`, to create objects compatible with static forcefields.
    - Allows integrating high-level forcefield definitions from `generic` methods, enhancing
      dynamic forcefield customization.

Key Attributes:
---------------
- `base_class` (`forcefield`): The base forcefield class (e.g., `ulsph`) from which behavior
  is inherited.
- `parameters` (`parameterforcefield`): Stores interaction parameters that are dynamically
  injected into the `base_class`.
- `beadtype` (int): The bead type associated with the `dforcefield` instance, used in
  forcefield calculations.
- `userid` (str): A unique identifier for the forcefield instance, used in interaction commands.
- `name` (struct or str): A human-readable name for the `dforcefield` instance.
- `description` (struct or str): A brief description of the `dforcefield` instance.
- `version` (float): The version number of the `dforcefield` instance.

Key Methods:
------------
- `_inject_attributes()`: Injects `dforcefield` attributes (like `parameters`, `beadtype`, 
  and `userid`) into the `base_class` to ensure it operates with the correct attributes.
- `pair_style(printflag=True, raw=False)`: Delegates the pair style computation to the `base_class`, 
  ensuring it uses the current `dforcefield` attributes.
- `pair_diagcoeff(printflag=True, i=None, raw=False)`: Delegates diagonal pair coefficient 
  computation to the `base_class`, allowing bead type `i` to be overridden.
- `pair_offdiagcoeff(o=None, printflag=True, i=None, raw=False)`: Delegates off-diagonal pair coefficient 
  computation to the `base_class`, allowing bead type `i` and interacting forcefield `o` to be overridden.
- `scriptobject(beadtype=None, name=None, fullname=None, filename=None, group=None, style=None, USER=scriptdata())`: 
  Creates a `scriptobject` from the current `dforcefield` instance, making it compatible with static forcefields.
- `missingVariables(isimplicit_missing=True, output_aslist=False)`: Lists undefined variables in `parameters`, 
  identifying missing implicit definitions (e.g., `${varname}`).

Usage Example:
--------------
    # Create a dynamic water forcefield using ulsph as the base class
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
    print(f"Water Cp: {dynamic_water.Cp}")
    dynamic_water.pair_style()  # Outputs the pair style command


    # Create a dynamic solidfood forcefield using tlsph as the base class
    dynamic_solidfood = dforcefield(
        base_class=tlsph,
        beadtype=2,
        userid="dynamic_solidfood",
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
    print(f"Solidfood parameters: {dynamic_solidfood.parameters}")
    dynamic_solidfood.pair_style()  # Outputs the pair style command
    
    # Create a new solidfood variant and save it
    new_food = dynamic_solidfood.copy(rho=2100, q1=4, E=1000, name="new food")
    new_food.save(overwrite=True)
    
    # Load the saved forcefield and compare
    loaded_food = dforcefield.load(new_food.userid + ".txt")
    new_food.compare(loaded_food, printflag=True)
    
    # Check for missing variables
    missing_vars = new_food.missingVariables()
    print(f"Missing variables: {missing_vars}")


    # Generate a forcefield from text
    ff_text = '''
    # DFORCEFIELD SAVE FILE
    
    # Forcefield attributes
    base_class="tlsph"
    beadtype = 2
    userid = dynamic_solidfood (copy)
    version = 0.1
    
    # Description of the forcefield
    description:{forcefield="LAMMPS:SMD - solid, liquid, rigid forcefields (continuum mechanics)", style="SMD:TLSPH - total Lagrangian for solids", material="dforcefield beads - SPH-like"}
    
    # Name of the forcefield
    name:{forcefield="LAMMPS:SMD", style="tlsph", material="new food"}
    
    # Parameters for the forcefield
    contact_scale = 1.5
    E = 1000
    nu = 0.3
    q2 = 0.0
    hardening = 0
    Hg = 10.0
    rho = 2100
    Cp = 1.0
    q1 = 4
    c0 = 10.0
    sigma_yield = 0.1*${E}
    contact_stiffness = 2.5*${c0}^2*${rho}
    '''
    
    # Parse the forcefield from text
    parsed_ff = dforcefield.parse(ff_text)
    print(parsed_ff.script)  # Outputs the raw content from the pair_* methods
    
    # Check missing variables
    missing_vars = parsed_ff.missingVariables()
    print(f"Missing variables: {missing_vars}")


    # *********************************************************************************************
    # Production Example: Scriptobject Creation and Combination
    # 
    # This example demonstrates the creation and combination of `scriptobject` instances from both
    # static forcefield classes and dynamic forcefield instances (via `dforcefield`).
    # 
    # Key Points:
    # ------------
    # 1. **Static and Dynamic Forcefields**: 
    #    - Scriptobjects can be created using static forcefields (e.g., `rigidwall`, `solidfood`, etc.)
    #      or dynamic forcefields generated from a `dforcefield` instance (e.g., `waterFF`).
    #    - Dynamic forcefields can either be passed directly to the `pizza.script.scriptobject()`
    #      constructor or instantiated through the `scriptobject` method of any `pizza.dforcefield` object.
    #
    # 2. **Combining Scriptobjects**: 
    #    - Scriptobjects can be combined using the `+` operator to create a collection of objects.
    #    - This collection of scriptobjects can then be scripted dynamically using the `script` property
    #      to generate their interaction definitions.
    #
    # 3. **Geometry Input**: 
    #    - Geometry for the scriptobjects can be provided either via an input file (using `filename`)
    #      or dynamically using `pizza.region.region()`.
    #
    # **********************************************************************************************
    
    from pizza.forcefield import rigidwall, solidfood, water
    
    # Create a dynamic forcefield for water with a specific density (rho=900) and beadtype=1
    waterFF = dforcefield(base_class="water", rho=900, beadtype=1)
    
    # Define water beads using the dforcefield instance's scriptobject method
    bwater = waterFF.scriptobject(name="water", group=["A", "D"], filename="mygeom")
    
    # Alternatively, define water beads by passing the dynamic forcefield directly to scriptobject
    bwater2 = scriptobject(name="water", group=["A", "D"], filename="mygeom", forcefield=waterFF)
    
    # Define other dummy beads using static forcefields
    b1 = scriptobject(name="bead 1", group=["A", "B", "C"], filename='myfile1', forcefield=rigidwall())
    b2 = scriptobject(name="bead 2", group=["B", "C"], filename='myfile1', forcefield=rigidwall())
    b3 = scriptobject(name="bead 3", group=["B", "D", "E"], forcefield=solidfood())
    b4 = scriptobject(name="bead 4", group="D", beadtype=1, filename="myfile2", forcefield=water())
    
    # Combine the scriptobjects into a collection using the '+' operator
    collection = bwater + b1 + b2 + b3 + b4
    
    # Generate the script for the interactions in the collection
    collection.script
    
    # Similarly, using the alternate water bead definition (bwater2)
    collection2 = bwater2 + b1 + b2 + b3 + b4
    collection2.script



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
__version__ = "0.992"



# INRAE\Olivier Vitrac - rev. 2024-09-21 (community)
# contact: olivier.vitrac@agroparistech.fr, han.chen@inrae.fr

# Revision history
# 2024-09-10 release candidate
# 2024-09-12 file management and parsing 
# 2024-09-14 major update fully compatible with scriptobject, script


# Dependencies
import os, sys, tempfile, getpass, socket
import re, string, random
import inspect, copy
from datetime import datetime
from pizza.private.struct import struct
from pizza.forcefield import forcefield, parameterforcefield
from pizza.script import scriptdata, scriptobject
from pizza.generic import generic, USERSMD


# %% Private Functions

def autoname(numChars=8):
    """ generate automatically names """
    return ''.join(random.choices(string.ascii_letters, k=numChars))  # Generates a random name of numChars letters

def remove_comments(content, split_lines=False):
    """
    Removes comments from a single or multi-line string. Handles quotes and escaped characters.
    
    Parameters:
    -----------
    content : str
        The input string, which may contain multiple lines. Each line will be processed 
        individually to remove comments, while preserving content inside quotes.
    split_lines : bool, optional (default: False)
        If True, the function will return a list of processed lines. If False, it will 
        return a single string with all lines joined by newlines.
    
    Returns:
    --------
    str or list of str
        The processed content with comments removed. Returns a list of lines if 
        `split_lines` is True, or a single string if False.
    """
    def process_line(line):
        """Remove comments from a single line while handling quotes and escapes."""
        in_single_quote = False
        in_double_quote = False
        escaped = False
        result = []
        
        for i, char in enumerate(line):
            if escaped:
                result.append(char)
                escaped = False
                continue
            
            if char == '\\':  # Handle escape character
                escaped = True
                result.append(char)
                continue
            
            # Toggle state for single and double quotes
            if char == "'" and not in_double_quote:
                in_single_quote = not in_single_quote
            elif char == '"' and not in_single_quote:
                in_double_quote = not in_double_quote
            
            # If we encounter a '#' and we're not inside quotes, it's a comment
            if char == '#' and not in_single_quote and not in_double_quote:
                break  # Stop processing the line when a comment is found
            
            result.append(char)
        
        return ''.join(result).strip()

    # Split the input content into lines
    lines = content.split('\n')

    # Process each line, skipping empty lines and those starting with #
    processed_lines = []
    for line in lines:
        stripped_line = line.strip()
        if not stripped_line or stripped_line.startswith('#'):
            continue  # Skip empty lines and lines that are pure comments
        processed_line = process_line(line)
        if processed_line:  # Only add non-empty lines
            processed_lines.append(process_line(line))

    if split_lines:
        return processed_lines  # Return list of processed lines
    else:
        return '\n'.join(processed_lines)  # Join lines back into a single string


# %% Main class
class dforcefield:
    """
The `dforcefield` class represents a dynamic extension of a base forcefield class. It allows for dynamic inheritance, 
delegation of methods, and flexible management of forcefield-specific attributes. The class supports the customization 
and injection of forcefield parameters at runtime, making it highly versatile for scientific simulations involving 
various forcefield models like `ulsph`, `tlsph`, and others.

Key Features:
-------------
    - Dynamic inheritance and delegation of base class methods.
    - Merging of `name` and `description` attributes, with automatic handling of overlapping fields.
    - Detection of variables used in `pair_style`, `pair_diagcoeff`, and `pair_offdiagcoeff` outputs.
    - Automatic handling of missing variables, including implicit variable detection and assignment.
    - Supports additional modules to be dynamically loaded for forcefield definitions.

Attributes:
-----------
    - `base_class` (forcefield): The base class for forcefield behavior, inherited from `forcefield` subclasses like `ulsph`.
    - `parameters` (parameterforcefield): Stores interaction parameters dynamically injected into the base class.
    - `beadtype` (int): The bead type identifier associated with the forcefield instance.
    - `userid` (str): A unique identifier for the forcefield instance.
    - `name` (struct or str): A human-readable name for the forcefield instance, merged with `description`.
    - `description` (struct or str): A brief description of the forcefield, merged with `name`.
    - `version` (float): Version number for the forcefield instance.

Methods:
--------
    ### High-Level Methods:
    These methods are primarily used for interacting with the `dforcefield` instance:
    
    - **`__init__`**: Initializes the dynamic forcefield with base class, parameters, and custom attributes.
    - **`pair_style`**: Delegates the pair style computation to the `base_class`.
    - **`pair_diagcoeff`**: Delegates diagonal pair coefficient computation to the `base_class`.
    - **`pair_offdiagcoeff`**: Delegates off-diagonal pair coefficient computation to the `base_class`.
    - **`save`**: Saves the forcefield instance to a file, with headers, attributes, and parameters.
    - **`load`**: Loads a `dforcefield` instance from a file and validates its format.
    - **`parse`**: Parses content of a forcefield file to create a new `dforcefield` instance.
    - **`copy`**: Creates a copy of the current instance, optionally overriding core attributes.
    - **`compare`**: Compares the current instance with another `dforcefield` instance, showing differences.
    - **`missingVariables`**: Lists undefined variables in `parameters`.
    - **`detectVariables`**: Detects variables in the `pair_style`, `pair_diagcoeff`, and `pair_offdiagcoeff` outputs.
    - **`to_dict`**: Serializes the forcefield instance into a dictionary.
    - **`from_dict`**: Creates a `dforcefield` instance from a dictionary of attributes.
    - **`reset`**: Resets the forcefield instance to its initial state.
    - **`validate`**: Validates the forcefield instance to ensure all required attributes are set.
    - **`base_repr`**: Returns the representation of the `base_class`.
    - **`script`**: Returns the raw outputs of pair methods as a script.
    - **scriptobject**: Method to return a scriptobject based on the current dforcefield instance.

    ### Low-Level Methods:
    These methods handle internal logic and lower-level operations:
    
    - **`_inject_attributes`**: Injects the dynamic attributes into the `base_class`.
    - **`__getattr__`**: Dynamically accesses attributes in `name`, `description`, `parameters`, or `base_class`.
    - **`__setattr__`**: Manages setting core and dynamic attributes.
    - **`_load_base_class`**: Dynamically loads the base class from a string name.
    - **`list_forcefield_subclasses`**: Lists all subclasses of `forcefield` including those from additional modules.
    - **`extract_default_parameters`**: Extracts default parameters from the base class or its ancestors.
    - **`dispmax`**: Truncates the display of long content for concise output.
    - **`__hasattr__`**: Checks if an attribute exists in the instance, parameters, or base class.
    - **`__contains__`**: Checks if an attribute exists in the instance or `parameters`.
    - **`__len__`**: Returns the number of parameters in the forcefield.
    - **`__iter__`**: Iterates over all keys, including those in `name`, `description`, `parameters`, and scalar attributes.
    - **`keys`**: Returns the keys from the merged `name`, `description`, and `parameters`.
    - **`values`**: Returns the values from the merged `name`, `description`, and `parameters`.
    - **`items`**: Returns an iterator of key-value pairs from `name`, `description`, and `parameters`.
    - **`merged_name_description`**: Merges `name` and `description` fields into a struct.
    - **`_get_available_forcefields`**: Retrieves a list of available forcefield subclasses.
    - **`__repr__`**: Custom representation of the `dforcefield` instance.
    - **`__str__`**: Returns a string representation of the `dforcefield` instance.
    - **`_convert_value`**: Converts a string value to the appropriate Python type.
    - **`_parse_global_params`**: Parses global parameters from the content between `{}`.
    - **`_parse_struct_block`**: Parses key-value pairs from `description` or `name` blocks.
    - **`__copy__`**: Creates a shallow copy of the `dforcefield` instance, copying only the attributes at the top level without duplicating nested objects.
    - **`__deepcopy__`**: Creates a deep copy of the `dforcefield` instance, fully duplicating all attributes, including nested objects, while leaving class references intact.


    
Example Usage:
--------------
    >>> dynamic_ff = dforcefield(ulsph, beadtype=1, userid="dynamic_water", USER=parameterforcefield(rho=1000))
    >>> dynamic_ff.pair_style()  # Uses attributes from the dforcefield instance
    lj/cut
    >>> dynamic_ff.compare(another_ff_instance, printflag=True)
    """


    # Display
    _maxdisplay = 40
    # Class attribute for the six specific attributes
    _dforcefield_specific_attributes = {'name', 'description', 'beadtype', 'userid', 'version', 'parameters'}
    # Class attribute: construction flag is True by default for all instances
    _in_construction = True
    RULES = parameterforcefield()  # Default empty RULES at the class level

    def __init__(self, base_class=None, beadtype=1, userid=None, USER=parameterforcefield(),
                 name=None, description=None, version=0.1, additional_modules=None,
                 GLOBAL=None, LOCAL=None, **kwargs):
        """
        Initialize a dynamic forcefield with default or custom values.
    
        Args:
            base_class (str or class): The base class to use (e.g., 'ulsph', tlsph, etc.) or the actual class.
            beadtype (int): The bead type identifier. Default is 1.
            userid (str): User ID for the material. Default is None.
            name (str): Human-readable name for the forcefield. Default is None.
            description (str): Description of the forcefield. Default is None.
            version (float): Version number for the forcefield. Default is 0.1.
            USER (parameterforcefield): Custom parameters to override defaults.
            additional_modules (module or list of modules): Additional modules to search for forcefields.
            GLOBAL (parameterforcefield): Global parameters to be used. Default is None.
            LOCAL (parameterforcefield): Local parameters to be used. Default is None.
            kwargs: Additional parameters passed to the base class.
        """
        
        # Initialize GLOBAL and LOCAL containers
        self.GLOBAL = GLOBAL if GLOBAL else parameterforcefield()
        self.LOCAL = LOCAL if LOCAL else parameterforcefield()
        self.RULES = parameterforcefield()  # Initialize RULES, to be populated later if applicable
    
        # Step 1a: Handle base_class, either a string or a class reference
        print(f"Initializing dforcefield with base_class: {base_class}")
        
        # Handle base_class loading (using additional_modules if needed)
        if isinstance(base_class, str):
            # Get available forcefields and short names mapping
            available_forcefields, short_name_mapping = self.list_forcefield_subclasses(
                printflag=False,
                additional_modules=additional_modules
            )
            # Check if the provided base_class name matches either the full or short name
            if base_class not in available_forcefields and base_class not in short_name_mapping:
                available_classes = ", ".join(short_name_mapping.keys())
                raise ValueError(
                    f"Invalid base_class: '{base_class}'. Must be one of the available forcefields: {available_classes}"
            )    
            # Use the full name from the short name if necessary
            # if base_class in short_name_mapping:
            #     base_class = short_name_mapping[base_class]
                
            # Load the base class or method
            base_class = dforcefield._load_base_class(base_class, additional_modules=additional_modules)
            
        # Ensure the base_class is valid
        if not (inspect.isclass(base_class) and issubclass(base_class, forcefield)) and not (
            callable(base_class) and hasattr(base_class, '__qualname__') and
            base_class.__qualname__.split('.')[0] in {cls.__name__ for cls in generic.__subclasses__()}
        ):
            raise ValueError(
                f"Invalid base_class: {base_class}. It must be a valid subclass of 'forcefield' or a callable forcefield method "
                f"from a 'generic' subclass."
        )
            
        # Step 1b: Initialize the base_class
        # If base_class is callable (like a method), call it to get an instance; otherwise, instantiate directly
        if callable(base_class):
            # Check if the base_class is a method of a generic subclass
            qualname = base_class.__qualname__.split('.')
            parent_class_name = qualname[0] if len(qualname) > 1 else None
            parent_class = next((cls for cls in generic.__subclasses__() if cls.__name__ == parent_class_name), None)
            
            if parent_class:
                # Instantiate the parent class and call the method on it
                parent_instance = parent_class()  # Create an instance of the parent class (e.g., USERSMD)
                self.base_class = base_class(parent_instance)  # Call the method with the instance context
            else:
                # Call the method directly if no parent class context is needed
                self.base_class = base_class()
        else:
            self.base_class = base_class()  # Instantiate the class if it's not a method  
    
        # Ensure the base_class is valid and handle classes and methods separately
        if inspect.isclass(base_class):
            # Step 2a: Extract default parameters from the base class
            extracted_info = self.extract_default_parameters(base_class, displayflag=True)
        elif callable(base_class) and hasattr(base_class, '__qualname__'):
            # If base_class is a method, extract the parent class name
            parent_class_name = base_class.__qualname__.split('.')[0]
            parent_class = next(
                (cls for cls in generic.__subclasses__() if cls.__name__ == parent_class_name), None
            )
            if parent_class is None:
                raise ValueError(f"Unable to find parent class '{parent_class_name}' for method '{base_class.__name__}'.")
            
            # Step 2b: Extract default parameters from the method within its parent class
            extracted_info = self.extract_default_parameters(parent_class, method_name=base_class.__name__, displayflag=True)
        else:
            raise ValueError(
                f"Invalid base_class: {base_class}. It must be a valid subclass of 'forcefield' or a callable forcefield method."
            )
    
        # Populate RULES, GLOBAL, and LOCAL if extracted
        self.RULES = extracted_info.get("RULES", parameterforcefield())
        self.GLOBAL = extracted_info.get("GLOBAL", parameterforcefield()) + self.GLOBAL
        self.LOCAL = extracted_info.get("LOCAL", parameterforcefield()) + self.LOCAL
    
        # Step 3: Initialize the base_class
        #self.base_class = base_class()  # Instantiate the base_class if it's callable
    
        # Step 4: Initialize name and description
        default_name = self.base_class.name  # Access base_class.name after ensuring it's properly set
        
        # Handling 'name'
        if name:
            if isinstance(name, str):
                name = default_name + struct(material=name)
            elif isinstance(name, struct):
                name = default_name + name
            else:
                raise TypeError(f"name must be of type str or struct, not {type(name)}")
        else:
            name = default_name + struct(material=self.__class__.__name__.lower())
        
        self.name = name
    
        # Handling 'description'
        default_description = self.base_class.description
        if description:
            if isinstance(description, str):
                description = default_description + struct(material=description)
            elif isinstance(description, struct):
                description = default_description + description
            else:
                raise TypeError(f"description must be of type parameterforcefield, not {type(description)}")
        else:
            description = default_description + struct(material=f"{self.__class__.__name__.lower()} beads - SPH-like")
    
        self.description = description
    
        # Step 5: Other properties and parameters
        self.userid = userid if userid else self.__class__.__name__.lower()
        self.version = version
        self.beadtype = beadtype
    
        # Ensure USER is of the correct type
        if not isinstance(USER, parameterforcefield):
            raise TypeError(f"USER must be of type parameterforcefield, not {type(USER)}")
    
        # Merge USER and kwargs into parameters
        # If no default parameters, proceed with user parameters
        if extracted_info["parameters"] is None:
            self.parameters = self.GLOBAL + self.LOCAL + self.RULES + USER + parameterforcefield(**kwargs)
        else:
            self.parameters = extracted_info["parameters"] + self.GLOBAL + self.LOCAL + self.RULES + USER + parameterforcefield(**kwargs)
        # After merging parameters, ensure USER is not part of it
        # if 'USER' in self.parameters:
        #     del self.parameters['USER']
                
        # End of construction
        self._in_construction = False
    
        # Inject dforcefield attributes into the base class
        self._inject_attributes()


    # New methods to access GLOBAL, LOCAL, and RULES

    def get_global(self):
        """Return the GLOBAL parameters for this dforcefield instance."""
        return self.GLOBAL

    def get_local(self):
        """Return the LOCAL parameters for this dforcefield instance."""
        return self.LOCAL

    def get_rules(self):
        """Return the RULES parameters for this dforcefield instance."""
        return self.RULES

    # Method to combine GLOBAL, LOCAL, and RULES
    def combine_parameters(self):
        """
        Combine GLOBAL, LOCAL, and RULES to get the current parameter configuration.
        """
        return self.GLOBAL + self.LOCAL + self.RULES
    
    # Other methods like _load_base_class, extract_default_parameters, etc., remain unchanged
    
    @classmethod
    def _load_base_class(cls, base_class_name, additional_modules=None):
        """
        Dynamically load the base class by its string name from the available forcefield subclasses 
        or additional modules.
        
        Args:
            base_class_name (str): The name of the forcefield class or method to load.
            additional_modules (list): Optional list of additional modules to search for the base class.
        
        Returns:
            class or function: The base class or function if found.
        """
        # Retrieve subclass information and short name mappings
        subclasses_info, short_name_mapping = cls.list_forcefield_subclasses(
            printflag=False, additional_modules=additional_modules
            )   
        print(f"Trying to load base_class: {base_class_name}")
    
        # Directly look for the exact name in the subclasses_info
        if base_class_name in subclasses_info:
            info = subclasses_info[base_class_name]
            if not info['loaded']:
                module_name = info['module']
                try:
                    print(f"Attempting to import module '{module_name}' and load '{base_class_name}'")
                    module = __import__(module_name, fromlist=[base_class_name])
                    target = getattr(module, base_class_name)
    
                    # Check if the target is a class or method
                    if inspect.isclass(target) and issubclass(target, forcefield):
                        return target
                    elif inspect.isfunction(target):
                        return target
                    else:
                        raise ValueError(f"Loaded target '{base_class_name}' is not a suitable forcefield class or method.")
                except (ImportError, AttributeError) as e:
                    available_classes = cls._get_available_forcefields()
                    raise ImportError(f"Failed to load the target '{base_class_name}' from module '{module_name}'. "
                                      f"Available forcefields: {available_classes}") from e
    
            # If already loaded, return the class directly
            return sys.modules[info['module']].__dict__.get(base_class_name)
    
        # If not found directly, check for nested methods within classes
        for key, info in subclasses_info.items():
            # Check if base_class_name is a method of a class
            if '.' in key and key.split('.')[-1] == base_class_name:
                parent_class_name = key.split('.')[0]
                if parent_class_name in subclasses_info:
                    # Load the parent class if it hasn't been loaded yet
                    parent_class_info = subclasses_info[parent_class_name]
                    if not parent_class_info['loaded']:
                        parent_class = cls._load_base_class(parent_class_name, additional_modules=additional_modules)
                    else:
                        # Directly access the parent class from the loaded module
                        module = sys.modules[parent_class_info['module']]
                        parent_class = getattr(module, parent_class_name)
                    
                    # Get the method from the loaded parent class
                    method = getattr(parent_class, base_class_name, None)
                    if method and callable(method):
                        return method
                    else:
                        raise ValueError(f"Method '{base_class_name}' was not found in the parent class '{parent_class_name}' or is not callable.")
    
        # If the target is a direct class but not a method or nested class, throw an appropriate error
        raise ValueError(f"Target '{base_class_name}' is not a recognized class or method. "
                         f"Available entries: {cls._get_available_forcefields()}")


    @classmethod
    def _get_available_forcefields(cls):
        """
        Retrieve the list of available forcefield subclasses.

        Returns:
            list: A list of available forcefield subclass names.
        """
        subclasses_info = cls.list_forcefield_subclasses(printflag=False)
        return list(subclasses_info.keys())


    @classmethod
    def extract_default_parameters(cls, base_class, method_name=None, displayflag=True):
        """
        Extract default parameters from the base class or its method by instantiating the class.
        
        If the base class is derived from `generic`, this function will also extract RULES, LOCAL, 
        and GLOBAL attributes if they are defined once the instance is created.
    
        Parameters:
        -----------
        base_class : class
            The base class from which to extract default parameterforcefield values or a method.
        method_name : str, optional
            The name of the method to call on the instance, if applicable (e.g., `newtonianfluid`).
        displayflag : bool, optional (default=True)
            If True, prints a message when no default parameters are found.
    
        Returns:
        --------
        dict
            A dictionary containing the default parameters extracted from the base class or method.
            Also includes RULES, LOCAL, and GLOBAL if applicable.
        """
        extracted_info = {
            "parameters": parameterforcefield(),
            "RULES": parameterforcefield(),
            "GLOBAL": parameterforcefield(),
            "LOCAL": parameterforcefield()
        }
    
        try:
            # Create an instance of the base class
            instance = base_class()
            
            # Extract parameters if the instance has them
            if hasattr(instance, 'parameters') and isinstance(instance.parameters, parameterforcefield):
                extracted_info["parameters"] = instance.parameters
            
            # Extract RULES, GLOBAL, and LOCAL if they exist
            for attr in ["RULES", "GLOBAL", "LOCAL"]:
                if hasattr(instance, attr) and isinstance(getattr(instance, attr), parameterforcefield):
                    extracted_info[attr] = getattr(instance, attr)
    
            # If a method is specified, call it to get additional parameters
            if method_name and hasattr(instance, method_name):
                method = getattr(instance, method_name)
                if callable(method):
                    try:
                        result = method()  # Call the method (ensure it returns the desired forcefield object)
                        if hasattr(result, 'parameters') and isinstance(result.parameters, parameterforcefield):
                            extracted_info["parameters"] = result.parameters
                    except Exception as e:
                        if displayflag:
                            print(f"Error calling method {method_name} on {base_class.__name__}: {str(e)}")
                            
        except TypeError as e:
            if displayflag:
                print(f"Could not instantiate {base_class.__name__}: {str(e)}")
    
        # If no parameters found or cannot instantiate the class, return None
        if displayflag and not extracted_info["parameters"]:
            print(f"No default parameters found in {base_class.__name__} or its ancestors.")
        
        return extracted_info

        
    def _inject_attributes(self):
        """Inject dforcefield attributes into the base class, bypassing __setattr__."""
        if not self._in_construction:  # Prevent injection during construction
            # Check if base_class is a class (not a method)
            if inspect.isclass(self.base_class):
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
        Shorthand for accessing parameters, base class attributes, or attributes in 'name' and 'description'.
        If an attribute exists in both 'name' and 'description', their contents are combined with a newline.
        """
        # Check if the attribute exists in the instance's __dict__
        if attr in self.__dict__:
            return self.__dict__[attr]
        # Check if the attribute exists in 'name' and 'description'
        name_attr = getattr(self.name, attr, None) if isinstance(self.name, struct) else None
        description_attr = getattr(self.description, attr, None) if isinstance(self.description, struct) else None
        # If the attribute exists in both 'name' and 'description', combine them with a newline
        if name_attr and description_attr:
            return [name_attr, description_attr]
        # If the attribute exists in 'name' only
        if name_attr:
            return name_attr
        # If the attribute exists in 'description' only
        if description_attr:
            return description_attr
        # Check if the attribute exists in 'parameters'
        if hasattr(self.parameters, attr):
            return getattr(self.parameters, attr)
        # Check if the attribute exists in the 'base_class'
        if hasattr(self.base_class, attr):
            return getattr(self.base_class, attr)
        # Raise an AttributeError if the attribute is not found
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attr}'")



    def __setattr__(self, attr, value):
        """
        Shorthand for setting attributes. Attributes specific to dforcefield are handled separately.
        New attributes are added to parameters if they are not part of the dforcefield-specific attributes.
        """
        # Handle internal attributes like _in_construction directly in the instance
        # and Check if the attribute is part of the dforcefield-specific attributes
        if hasattr(self.__class__, attr) or attr in self._dforcefield_specific_attributes:
            if attr=="parameters": 
                if not isinstance(value,parameterforcefield):
                    raise TypeError("parameters must be of type parameterforcefield, not of type {}".format(type(value)))                
                self.__dict__[attr] = self.detectVariables() + value # check that all variables are defined
            else:
                self.__dict__[attr] = value
            if not self._in_construction and attr in self._dforcefield_specific_attributes:
                self._inject_attributes()
        # Handle dynamic setting of attributes in parameters
        elif 'parameters' in self.__dict__:
            # Update parameters (existing or new attributes)
            setattr(self.parameters, attr, value)
            
            # Ensure injection occurs when parameters is updated
            if not self._in_construction:
                self._inject_attributes()
        else:
            # Fallback to default behavior if the attribute isn't part of parameters or specific attributes
            super().__setattr__(attr, value)

            
    def __hasattr__(self, attr):
        """Check if an attribute exists in the dforcefield instance, class, parameters, or the base class."""
        # Check for instance attribute
        if attr in self.__dict__:
            return True
        # Check for class attribute
        if hasattr(self.__class__, attr):
            return True
        # Check for parameters
        if attr in self.parameters.keys():
            return True
        # Check for attribute in base class
        if hasattr(self.base_class, attr):
            return True
        return False

            
    def __contains__(self, item):
        """Check if an attribute exists in the dforcefield instance or its parameters."""
        return item in self.keys()
    
    
    def __len__(self):
        """
        Return the number of parameters in the forcefield.
        This will use the len method of parameters.
        """
        return len(self.keys())
    
    
    @property
    def merged_name_description(self):
        """
        Return a struct containing the merged content of 'name' and 'description'.
        If an attribute exists in both, their values are combined into a list.
        """
        merged_data = {}
    
        # Add attributes from 'name' if it's a struct
        if isinstance(self.name, struct):
            merged_data.update(self.name.__dict__)
    
        # Add/merge attributes from 'description' if it's a struct
        if isinstance(self.description, struct):
            for key, value in self.description.__dict__.items():
                if key in merged_data:
                    # Combine the values into a list if the key already exists
                    existing_value = merged_data[key]
                    if not isinstance(existing_value, list):
                        existing_value = [existing_value]  # Convert to list if not already a list
                    merged_data[key] = existing_value + [value]  # Add the new value to the list
                else:
                    merged_data[key] = value
    
        # Return the merged struct
        return struct(**merged_data)



    def keys(self):
        """
        Return the keys of the merged struct, parameters, and scalar attributes.
        """
        keys_set = set(self.merged_name_description.__dict__.keys())
        keys_set.update(self.parameters.keys())
        keys_set.update(['version', 'userid', 'beadtype'])
        return list(keys_set)
    
    def values(self):
        """
        Return the values of the merged struct, parameters, and scalar attributes.
        """
        values_list = list(self.merged_name_description.__dict__.values())
        values_list.extend(self.parameters.values())
        values_list.extend([self.version, self.userid, self.beadtype])
        return values_list
    
    def items(self):
        """
        Return an iterator over (key, value) pairs from the merged struct, parameters, and scalar attributes.
        """
        # Yield items from merged struct
        for item in self.merged_name_description.__dict__.items():
            yield item
    
        # Yield items from parameters
        for item in self.parameters.items():
            yield item
    
        # Yield scalar attribute items
        yield ('version', self.version)
        yield ('userid', self.userid)
        yield ('beadtype', self.beadtype)
    
    def __iter__(self):
        """
        Iterate over all keys, including those in the merged struct, parameters, and scalar attributes.
        """
        for key in self.merged_name_description.__dict__:
            yield key
        for key in self.parameters:
            yield key
        yield 'version'
        yield 'userid'
        yield 'beadtype'
       
                
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
        for key, value in self.merged_name_description.items():
            # Check if the value is a list (when the field exists in both name and description)
            if isinstance(value, list):
                for idx, val in enumerate(value):
                    value_lines = self.dispmax(val).splitlines()
                    
                    # Apply {key:<20} to the first line of the first item in the list
                    if idx == 0:
                        name_table += f"  {key:<20}: {value_lines[0]}\n"
                    else:
                        name_table += f"  {'':<20}  {value_lines[0]}\n"  # Align subsequent items
                    # Handle multi-line values within each list item
                    for line in value_lines[1:]:
                        name_table += f"  {'':<20}  {line}\n"  # Indent the remaining lines
            else:
                # Handle non-list values
                value_lines = self.dispmax(value).splitlines()
                # Apply {key:<20} to the first line and indent the subsequent lines
                name_table += f"  {key:<20}: {value_lines[0]}\n"  # First line with key aligned
                for line in value_lines[1:]:
                    name_table += f"  {'':<20}  {line}\n"  # Indent the remaining lines
        # Evaluate all values of parameters
        tmp = self.parameters.eval()
        tmpkey= ""
        # Generate the parameters table dynamically (iterating over key-value pairs)
        parameters_table = sep+ "[ PARAMS (can be changed) ]\n"
        missing = 0
        for key, value in self.parameters.items():  # Assuming parameters is a class with __dict__
            parameters_table += f"  {key:<20}: {value}"  # Align the keys and values dynamically
            if isinstance(value,str):
                if value=="${"+key+"}":
                    parameters_table += "\t < implicit definition >\n"
                    missing += 1 
                else:
                    parameters_table += f"\n  {tmpkey:<20}= {self.dispmax(tmp.getattr(key))}\n"
            else:
                parameters_table += "\n"
        parameters_table += sep+f" >> {len(self.parameters)} definitions ({missing} missing)\n"
    
        # Combine the name and parameters table with a general instance representation
        print(f'\ndforcefield "{self.userid}" derived from "{base_class_name}"\n{name_table}{parameters_table}\n')
        return self.__str__()
    
    def base_repr(self):
        """Returns the representation of the base_class."""
        self.base_class.__repr__()
        return self.base_class.__str__()
    
    @property
    def script(self):
        """
        Return the raw content of the pair_* outputs combined into a single script-like format.
        
        Returns:
        --------
        str
            The raw outputs from pair_style, pair_diagcoeff, and pair_offdiagcoeff concatenated into a script.
        """
        # Get the raw outputs from the pair_* methods
        pair_style_output = self.pair_style(printflag=False, raw=True)
        pair_diagcoeff_output = self.pair_diagcoeff(printflag=False, raw=True)
        pair_offdiagcoeff_output = self.pair_offdiagcoeff(printflag=False, raw=True)
        
        # Combine the outputs into a script-like format
        script_content = "\n".join([
            "# Script output from dforcefield:",
            "# Pair style:",
            pair_style_output,
            "\n# Diagonal coefficients:",
            pair_diagcoeff_output,
            "\n# Off-diagonal coefficients:",
            pair_offdiagcoeff_output
        ])
        
        return script_content
        
    def __str__(self):
        base_class_name = self.base_class.__class__.__name__ if self.base_class else "None"
        return f"<dforcefield instance with base class: {base_class_name}, userid: {self.userid}, beadtype: {self.beadtype}>"
    
    def dispmax(self,content):
        """ optimize display """
        strcontent = str(content)
        if len(strcontent)>self._maxdisplay:
            nchar = round(self._maxdisplay/2)
            return strcontent[:nchar]+" [...] "+strcontent[-nchar:]
        else:
            return content

    def pair_style(self, printflag=True,raw=False):
        """Delegate pair_style to the base class, ensuring it uses the correct attributes."""
        return self.base_class.pair_style(printflag,raw)
    
    
    def pair_diagcoeff(self, printflag=True, i=None, raw=False):
        """Delegate pair_diagcoeff to the base class, ensuring it uses the correct attributes."""
        return self.base_class.pair_diagcoeff(printflag, i, raw)
    
    
    def pair_offdiagcoeff(self, o=None, printflag=True, i=None, raw=False):
        """Delegate pair_offdiagcoeff to the base class, ensuring it uses the correct attributes."""
        return self.base_class.pair_offdiagcoeff(o, printflag, i, raw)

    
    def __add__(self, other):
        """Concatenate dforcefield attributes if different, else keep the version of self."""
        if not isinstance(other, dforcefield):
            raise TypeError(f"Cannot concatenate {type(other)} with dforcefield.")
        
        if self.base_class != other.base_class:
            raise ValueError(f"Cannot concatenate dforcefield instances with different base classes ({self.base_class} != {other.base_class}).")
        
        # Concatenate name, description, beadtype, userid, and parameters if different, else keep self's version
        new_name = self.name if self.name == other.name else f"{self.name}_{other.name}"
        new_description = self.description if self.description == other.description else f"{self.description} + {other.description}"
        new_beadtype = self.beadtype if self.beadtype == other.beadtype else f"{self.beadtype}, {other.beadtype}"
        new_parameters = self.parameters + other.parameters  # Assuming parameters supports '+'
        new_userid = self.userid if self.userid == other.userid else f"{self.userid}_{other.userid}"
        
        # Keep the version from self
        new_version = self.version
        
        # Return a new dforcefield instance with concatenated attributes
        return dforcefield(
            base_class=self.base_class,
            beadtype=new_beadtype,
            userid=new_userid,
            name=new_name,
            description=new_description,
            version=new_version,
            USER=new_parameters,
        )
    
    def copy(self, beadtype=None, userid=None, name=None, description=None, version=None, USER=parameterforcefield(), **kwargs):
        """
        Create a new instance of dforcefield with the option to override the six attributes:
        beadtype, userid, name, description, version, USER.
        """
        # Use the current instance's values as defaults, and override if values are provided
        new_beadtype = beadtype if beadtype is not None else self.beadtype
        new_userid = userid if userid is not None else self.userid
        new_name = name if name is not None else self.name
        new_description = description if description is not None else self.description
        new_version = version if version is not None else self.version
        if new_userid == self.userid:
            new_userid = new_userid + " (copy)"
        # USER is computed by combining self.parameters + USER + parameterforcefield(**kwargs)
        new_parameters = self.parameters + USER
        # Create and return the new instance with overridden values
        return self.__class__(
            base_class=self.base_class.__class__,
            beadtype=new_beadtype,
            userid=new_userid,
            name=new_name,
            description=new_description,
            version=new_version,
            USER=new_parameters,
            **kwargs
        )
    
    def update(self, **kwargs):
        """
        Update multiple attributes of the dforcefield instance at once.
        
        Args:
            kwargs: Key-value pairs of attributes to update.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)


    def to_dict(self):
        """
        Serialize the dforcefield instance to a dictionary.
        
        Returns:
            dict: A dictionary containing all the attributes and their current values.
        Example:
            config = dynamic_water.to_dict()
            print(config)

        """
        data = {
            "name": self.name,
            "description": self.description,
            "beadtype": self.beadtype,
            "userid": self.userid,
            "version": self.version,
            "parameters": dict(self.parameters),
            "base_class": self.base_class.__class__.__name__
        }
        return data


    @classmethod
    def from_dict(cls, data):
        """
        Create a dforcefield instance from a dictionary.
        
        Args:
            data (dict): A dictionary containing the attributes to initialize the dforcefield.
        
        Returns:
            dforcefield: A new dforcefield instance.
        Example:
            config = {
                "name": "water_ff",
                "description": "water forcefield",
                "beadtype": 2,
                "userid": "water_sim",
                "version": 1.0,
                "parameters": {"rho": 1000, "sigma": 0.5},
                "base_class": "ulsph"
            }
            
            new_ff = dforcefield.from_dict(config)

        """
        base_class_name = data.pop("base_class", None)
        base_class = globals().get(base_class_name) if base_class_name else None
        return cls(base_class=base_class, **data)


    def reset(self):
        """
        Reset the dforcefield instance to its initial state, reapplying the default values.
        """
        self.__init__(self.base_class.__class__, beadtype=self.beadtype, userid=self.userid, 
                      name=self.name, description=self.description, version=self.version)
        
    def validate(self):
        """
        Validate the dforcefield instance to ensure all required attributes are set.
        
        Raises:
            ValueError: If any required attributes are missing or invalid.
        """
        required_fields = self._dforcefield_specific_attributes
        
        for field in required_fields:
            if not getattr(self, field):
                raise ValueError(f"{field} is required and not set.")
        
        print("Validation successful.")


    def compare(self, other, printflag=False):
        """
        Compare the current instance with another dforcefield instance.
        
        Args:
        -----
        other : dforcefield
            The other instance to compare.
        
        printflag : bool, optional (default: False)
            If True, prints a table showing all parameters, with differences marked by '*'.
        
        Returns:
        --------
        dict
            A dictionary showing differences between the two instances.
        
        Raises:
        -------
        TypeError: If the other object is not a dforcefield instance.
        
        Example:
        --------
        diffs = dynamic_water.compare(dynamic_salt)
        if printflag:
            Prints a comparison table with a type column and a legend at the end.
        """
        
        # Define abbreviations for types
        type_abbreviations = {
            str: 'STR',
            int: 'INT',
            float: 'FLT',
            bool: 'BOOL',
            list: 'LST',
            tuple: 'TPL',
            dict: 'DCT',
            None: 'NON',
            'missing': 'MIS'
        }
    
        def get_type_abbrev(value):
            """Return the abbreviation for the type of the value."""
            if value is None:
                return type_abbreviations[None]
            return type_abbreviations.get(type(value), 'UNK')  # Use 'UNK' for unknown types
    
        def format_simple_type(value):
            """Format a simple value (str, number, or bool) for display."""
            return self.dispmax(str(value))
    
        def format_iterable(value_self, value_other, key, comparison_table, difference):
            """Handle lists, tuples, and other iterable types."""
            max_length = max(len(value_self), len(value_other))
            for i in range(max_length):
                item_self = value_self[i] if i < len(value_self) else 'MISSING'
                item_other = value_other[i] if i < len(value_other) else 'MISSING'
                sub_difference = '*' if item_self != item_other else ' '
                comparison_table.append(
                    f"  {key if i == 0 else '':<15}: {sub_difference:^3}: {self.dispmax(str(item_self)):<30}: {get_type_abbrev(item_self):<5}: {self.dispmax(str(item_other)):<30}: {get_type_abbrev(item_other):<5}"
                )
    
        def format_dict_like(value_self, value_other, key, comparison_table, difference):
            """Handle dictionary-like objects (e.g., structs or dicts)."""
            comparison_table.append(f"  {key:<15}: {difference:^3}: ")
            comparison_table.append(f"  {'':<15}  {'Self':<30} {'Type':<5} {'Other':<30} {'Type':<5}")
            sub_sep = "  "+"-"*15+":"+"-"*3+":"+"-"*30+":"+"-"*5+":"+"-"*30+":"+"-"*5
            comparison_table.append(sub_sep)
            sub_keys = set(value_self.keys()).union(value_other.keys())
            for sub_key in sorted(sub_keys):
                sub_value_self = value_self.get(sub_key, 'MISSING')
                sub_value_other = value_other.get(sub_key, 'MISSING')
                sub_difference = '*' if sub_value_self != sub_value_other else ' '
                comparison_table.append(
                    f"  {sub_key:<15}: {sub_difference:^3}: {self.dispmax(str(sub_value_self)):<30}: {get_type_abbrev(sub_value_self):<5}: {self.dispmax(str(sub_value_other)):<30}: {get_type_abbrev(sub_value_other):<5}"
                )
            comparison_table.append(sub_sep)
    
        def format_complex_type(value_self, value_other, key, comparison_table, difference):
            """Handle complex types, expanding them into multiple lines."""
            value_self_lines = str(value_self).splitlines()
            value_other_lines = str(value_other).splitlines()
            max_lines = max(len(value_self_lines), len(value_other_lines))
            for i in range(max_lines):
                line_self = value_self_lines[i] if i < len(value_self_lines) else 'MISSING'
                line_other = value_other_lines[i] if i < len(value_other_lines) else 'MISSING'
                comparison_table.append(
                    f"  {key if i == 0 else '':<15}: {difference if i == 0 else ' ':^3}: {self.dispmax(line_self):<30}: {get_type_abbrev(line_self):<5}: {self.dispmax(line_other):<30}: {get_type_abbrev(line_other):<5}"
                )
    
        if not isinstance(other, dforcefield):
            raise TypeError("Can only compare with another dforcefield instance.")
        
        diffs = {}
        
        # Collect all keys from both instances
        all_keys = set(self.keys()).union(other.keys())
    
        # Iterate over all keys and compare the values
        for key in all_keys:
            value_self = getattr(self, key, None)
            value_other = getattr(other, key, None)
            
            if value_self != value_other:
                diffs[key] = {"self": value_self, "other": value_other}
    
        # If printflag is True, print the comparison in a table format
        if printflag:
            sep = "  "+"-"*15 + ":" + "-"*3 + ":" + "-"*30 + ":" + "-"*5 + ":" + "-"*30 + ":" + "-"*5
            header = f"\n  {'Attribute':<15}: {'*':^3}: {'Self':<30}: {'Type':<5}: {'Other':<30}: {'Type':<5}\n" + sep
            comparison_table = [header]
            
            # Iterate over all parameters and mark differences with '*'
            for key in sorted(all_keys):  # Sort keys for a cleaner output
                value_self = getattr(self, key, 'MISSING')
                value_other = getattr(other, key, 'MISSING')
                difference = '*' if value_self != value_other else ' '
                
                # Check if the value is a simple type (str, number, or bool)
                if isinstance(value_self, (str, int, float, bool)) and isinstance(value_other, (str, int, float, bool)):
                    comparison_table.append(
                        f"  {key:<15}: {difference:^3}: {format_simple_type(value_self):<30}: {get_type_abbrev(value_self):<5}: {format_simple_type(value_other):<30}: {get_type_abbrev(value_other):<5}"
                    )
                # Check if the value is a list or tuple
                elif isinstance(value_self, (list, tuple)) and isinstance(value_other, (list, tuple)):
                    format_iterable(value_self, value_other, key, comparison_table, difference)
                # Check if the value is a dictionary-like object
                elif hasattr(value_self, 'keys') and hasattr(value_other, 'keys'):
                    format_dict_like(value_self, value_other, key, comparison_table, difference)
                else:
                    # Handle other complex types
                    format_complex_type(value_self, value_other, key, comparison_table, difference)
            
            comparison_table.append(sep)
            # Add a legend for type abbreviations
            legend = "\nType Legend: " + ", ".join(f"{abbrev} = {('NoneType' if type_ is None else type_.__name__.upper())}" for type_, abbrev in type_abbreviations.items() if type_ != 'missing')

            comparison_table.append(legend)
            
            # Print the comparison table
            print("\n".join(comparison_table))
        
        return diffs
    


    def save(self, filename=None, foldername=None, overwrite=False):
        """
        Save the dforcefield instance to a file with a header, formatted content, and the base_class.
    
        Args:
        -----
        filename (str): The name of the file to save. Defaults to self.userid if not provided.
        foldername (str): The folder in which to save the file. Defaults to a temporary directory.
        overwrite (bool): Whether to overwrite the file if it already exists. Defaults to False.
    
        Raises:
        -------
        ValueError: If base_class is None or not a subclass of forcefield.
        FileExistsError: If the file already exists and overwrite is False.
    
        Notes:
        ------
        The file format follows a specific structure for saving forcefield attributes, base_class, 
        name, description, and parameters.
    
        Example Output: (without the comments)
        ---------------
        # DFORCEFIELD SAVE FILE
        base_class = "tlsph"
        beadtype = 1
        userid = "dynamic_water"
        version = 1.0
    
        description:{forcefield="LAMMPS:SMD", style="tlsph", material="water"}
        name:{forcefield="LAMMPS:SMD", material="water"}
    
        rho = 1000
        E = "5*${c0}^2*${rho}"
        nu = 0.3
        """
        
        # Use self.userid if filename is not provided
        if filename is None:
            filename = self.userid
    
        # Ensure the filename ends with '.txt'
        if not filename.endswith('.txt'):
            filename += '.txt'
        
        # Default folder to tempdir if foldername is not provided
        if foldername is None:
            foldername = tempfile.gettempdir()
        
        # Construct full path
        if not os.path.isabs(filename):
            filepath = os.path.join(foldername, filename)
        else:
            filepath = filename
        
        # Check if file already exists, raise exception if it does and overwrite is False
        if os.path.exists(filepath) and not overwrite:
            raise FileExistsError(f"The file '{filepath}' already exists.")
        
        # Header with current date, username, and host
        user = getpass.getuser()
        host = socket.gethostname()
        date = datetime.now().strftime('%Y-%m-%d')
        header = f"# DFORCEFIELD SAVE FILE\n# generated on {date} by {user}@{host}\n"
        header += f'#\tuserid = "{self.userid}"\n'
        header += f'#\tpath = "{filepath}"\n\n'
        
        # Open the file for writing
        with open(filepath, 'w') as f:
            # Write the header
            f.write(header)
    
            # Write beadtype, userid, and version with comments
            f.write("# Forcefield attributes\n")
            f.write(f'base_class="{self.base_class.__class__.__name__}"\n')
            f.write(f"beadtype = {self.beadtype}\n")
            f.write(f"userid = {self.userid}\n")
            f.write(f"version = {self.version}\n\n")
    
            # Write description with comment
            f.write("# Description of the forcefield\n")
            f.write("description:{")
            f.write(", ".join(f'{key}="{value}"' for key, value in self.description.items()))
            f.write("}\n\n")
    
            # Write name with comment
            f.write("# Name of the forcefield\n")
            f.write("name:{")
            f.write(", ".join(f'{key}="{value}"' for key, value in self.name.items()))
            f.write("}\n\n")
    
            # Write parameters with comment
            f.write("# Parameters for the forcefield\n")
            for key, value in self.parameters.items():
                f.write(f"{key} = {value}\n")
                
        # return filepath
        print(f"\nScript saved to {filepath}")
        
        return filepath



    @classmethod
    def load(cls, filename, foldername=None):
        """
        Load a dforcefield instance from a file with more control over the folder location and file validation.
    
        Args:
            filename (str): The name of the file to load. The '.txt' extension will be added if not present.
            foldername (str): The folder from which to load the file. Defaults to a temporary directory.
        
        Returns:
            dforcefield: A new dforcefield instance parsed from the file content.
        """
        # Step 0: Validate and construct filepath
        if not filename.endswith('.txt'):
            filename += '.txt'    
        if foldername is None:
            foldername = tempfile.gettempdir()
        if not os.path.isabs(filename):
            filepath = os.path.join(foldername, filename)
        else:
            filepath = filename
    
        # Check if file exists
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"The file '{filepath}' does not exist.")
    
        # Read the file contents
        with open(filepath, 'r') as f:
            content = f.read()
    
        # Extract the filename and name
        fname = os.path.basename(filepath)  # Extracts the filename (e.g., "forcefield.txt")
        name, _ = os.path.splitext(fname)   # Removes the extension, e.g., "forcefield"
    
        # Call the parse method to create a new dforcefield instance
        return cls.parse(content)


    @classmethod
    def parse(cls, content):
        """
        Parse the string content of a forcefield file to create a dforcefield instance.
    
        Parameters:
        -----------
        content : str
            The string content to be parsed.
        
        Returns:
        --------
        dforcefield
            A new `dforcefield` instance populated with the parsed content.
    
        Raises:
        -------
        ValueError
            If the content does not start with the correct magic line or if the format is invalid,
            or if base_class is not a valid subclass of forcefield.
        
        Notes:
        ------
        - Handles different sections including parameters, name, and description.
        - Accepts empty lines, comments, and the use of { } for attributes.
        """
        # Split the content into lines
        lines = content.splitlines()
        lines = [line for line in lines if line.strip()]  # Remove blank or empty lines
        # Raise an error if no content is left after removing blank lines
        if not lines:
            raise ValueError("File/Content is empty or only contains blank lines.")
    
        # Initialize containers for parsed data
        inside_global_params = False
        parameters = {}
        attributes = {}
        description = {}
        name = {}
        base_class = None
    
        # Step 1: Authenticate the file by checking the first line
        if not lines[0].strip().startswith("# DFORCEFIELD SAVE FILE"):
            raise ValueError("File/Content is not a valid DFORCEFIELD file.")
    
        # Step 2: Process each line dynamically
        for line in lines[1:]:
            stripped = line.strip()
    
            # Ignore empty lines and comments
            if not stripped or stripped.startswith("#"):
                continue
    
            # Remove trailing comments
            stripped = remove_comments(stripped)
    
            # Step 3: Detect base_class
            if stripped.startswith("base_class="):
                base_class_name = stripped.split("=", 1)[1].strip().strip('"')
                # Dynamically set the base class based on the string value (e.g., "tlsph")
                base_class = cls._load_base_class(base_class_name)
                if base_class is None or not issubclass(base_class, forcefield):
                    raise ValueError(f"Invalid base_class: '{base_class_name}' must be a subclass of forcefield.")
                continue
    
            # Step 4: Handle global parameters inside {...}
            if stripped.startswith("{"):
                inside_global_params = True
                global_params_content = stripped[stripped.index('{') + 1:].strip()
    
                if '}' in global_params_content:
                    global_params_content = global_params_content[:global_params_content.index('}')].strip()
                    inside_global_params = False
                    cls._parse_global_params(global_params_content.strip(), attributes)
                    global_params_content = ""  # Reset for the next block
                continue
    
            if inside_global_params:
                if stripped.endswith("}"):
                    global_params_content += " " + stripped[:stripped.index('}')].strip()
                    inside_global_params = False
                    cls._parse_global_params(global_params_content.strip(), attributes)
                    global_params_content = ""
                else:
                    global_params_content += " " + stripped
                continue
    
            # Step 5: Detect the start of name or description blocks
            if stripped.startswith("description:{"):
                desc_content = stripped.split("description:")[1].strip()[1:-1]
                cls._parse_struct_block(desc_content, description)
                continue
    
            if stripped.startswith("name:{"):
                name_content = stripped.split("name:")[1].strip()[1:-1]
                cls._parse_struct_block(name_content, name)
                continue
    
            # Step 6: Handle parameters in key=value format
            if "=" in stripped:
                key, value = stripped.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"')
                parameters[key] = cls._convert_value(value)
    
        # Step 7: Validate base_class and create a new dforcefield instance
        if base_class is None:
            raise ValueError("base_class must be specified and valid in the forcefield file.")
            
        # Step 8: Create and return the new dforcefield instance
        newFF = cls(
            base_class=base_class,
            beadtype=int(attributes.get('beadtype', 1)),
            userid=attributes.get('userid', "unknown"),
            name=struct(**name),
            description=struct(**description),
            version=float(attributes.get('version', 0.1)),
            USER=parameterforcefield(**parameters)
        )
                    
        # Step 9: detect variables in templates and propagates undefined variables
        dvars = newFF.detectVariables()
        newFF.parameters = dvars + newFF.parameters
        return newFF

    
    @classmethod
    def _parse_global_params(cls, content, global_params):
        """Parse global parameters from the accumulated content between {}."""
        lines = re.split(r',(?![^(){}\[\]]*[\)\}\]])', content)
        for line in lines:
            line = line.strip()
            match = re.match(r'([\w_]+)\s*=\s*(.+)', line)
            if match:
                key, value = match.groups()
                key = key.strip()
                value = value.strip()
                global_params[key] = cls._convert_value(value)
    


    @classmethod
    def _parse_struct_block(cls, content, struct_block):
        """
        Parse blocks like description or name with key=value pairs, handling commas inside quotes.
        
        Parameters:
        -----------
        content : str
            The content to parse, which contains key=value pairs.
        
        struct_block : dict
            A dictionary to store the parsed key-value pairs.
        """
        # Split on commas that are not inside quotes
        pairs = re.split(r',\s*(?![^"]*\"\s*,\s*[^"]*")', content)
        
        for pair in pairs:
            if '=' in pair:
                key, value = pair.split('=', 1)  # Ensure splitting only on the first '='
            struct_block[key.strip()] = value.strip().strip('"')


    
    @classmethod
    def _convert_value(cls, value):
        """Convert a string representation of a value to the appropriate Python type."""
        value = value.strip()
    
        # Boolean conversion
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
    
        # Handle quoted strings
        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
            return value[1:-1]
    
        # Handle lists
        if value.startswith('[') and value.endswith(']'):
            return eval(value)  # Using eval to parse lists safely in this controlled scenario
    
        # Handle numbers
        try:
            if '.' in value:
                return float(value)
            return int(value)
        except ValueError:
            return value


    def detectVariables(self):
        """
        Detects variables in the form ${variable} from the outputs of pair_style, pair_diagcoeff,
        and pair_offdiagcoeff.
        
        Returns:
        --------
        struct
            A struct containing the detected variable names that are not yet defined.
        """
        # Extract variables from pair_style, pair_diagcoeff, and pair_offdiagcoeff
        detected_vars = set()
    
        # Define a regex pattern to detect variables in the form ${variable}
        pattern = r'\$\{(\w+)\}'
    
        # Detect variables in pair_style output
        pair_style_output = self.pair_style(printflag=False, raw=True)
        detected_vars.update(re.findall(pattern, pair_style_output))
    
        # Detect variables in pair_diagcoeff output
        pair_diagcoeff_output = self.pair_diagcoeff(printflag=False, raw=True)
        detected_vars.update(re.findall(pattern, pair_diagcoeff_output))
    
        # Detect variables in pair_offdiagcoeff output
        pair_offdiagcoeff_output = self.pair_offdiagcoeff(printflag=False, raw=True)
        detected_vars.update(re.findall(pattern, pair_offdiagcoeff_output))
    
        # Convert the detected variables into a parameterforcefield() for further propagation
        return parameterforcefield(**{var: "${" + var + "}" for var in detected_vars})
    
    
    def missingVariables(self, isimplicit_missing=True, output_aslist=False):
        """
        List missing variables (undefined in parameters).
        
        Parameters:
        -----------
        isimplicit_missing : bool, optional (default: True)
            If True, variables defined implicitly as ${varname} in parameters are considered missing.
        
        output_aslist : bool, optional (default: False)
            If True, returns a list of missing variable names.
            If False, returns a parameterforcefield-like structure with implicit definitions.
        
        Returns:
        --------
        List of str or parameterforcefield
            If output_aslist is True, returns a list of variable names that are missing from the parameters.
            If output_aslist is False, returns a parameterforcefield-like structure with implicit definitions.
        """
        # Detect all variables used in the forcefield using detectVariables
        detected_vars = self.detectVariables()
    
        # Initialize missing variables
        missing_vars = []
    
        # Initialize a dictionary to store variables as parameterforcefield when output_aslist=False
        missing_vars_struct = {}
    
        # Iterate over detected variables and check if they are missing in parameters
        for varname in detected_vars.keys():
            if varname not in self.parameters:
                # If the variable is missing, add it to both the list and struct
                missing_vars.append(varname)
                missing_vars_struct[varname] = "${" + varname + "}"
            elif isimplicit_missing:
                # If the variable exists but is implicitly defined as ${varname}, treat it as missing
                param_value = self.parameters.getattr(varname)
                if param_value == "${" + varname + "}":
                    missing_vars.append(varname)
                    missing_vars_struct[varname] = "${" + varname + "}"
    
        # Return the result based on the output_aslist flag
        if output_aslist:
            return missing_vars
        else:
            return parameterforcefield(**missing_vars_struct)
    
    
    @classmethod
    def list_forcefield_subclasses(cls, printflag=True, additional_modules=None):
        """
        Class method to list all subclasses of the `forcefield` and `generic` classes, including their methods.
    
        Parameters:
        -----------
        printflag : bool, optional (default=True)
            If True, prints the subclasses of `forcefield`, `generic`, their load status, and their default parameters.
        additional_modules : module or list of modules, optional
            A module or list of additional modules to search for subclasses and methods.
    
        Returns:
        --------
        dict
            A dictionary where keys are class names or method names and values are dictionaries containing:
            - "loaded": Whether the class or method is already loaded in memory.
            - "module": The module path of the class or method.
            - "default_parameters": Extracted parameters, RULES, LOCAL, and GLOBAL from the class or method.
        dict
            A dictionary mapping short names to full names.
        """
        subclasses = set()
        classes_to_check = [forcefield, generic]  # Start with both forcefield and generic
    
        # Ensure additional_modules is a list, even if it's a single module
        if additional_modules is not None and not isinstance(additional_modules, list):
            additional_modules = [additional_modules]
    
        # Include classes from additional modules
        if additional_modules:
            for mod in additional_modules:
                for name, obj in inspect.getmembers(mod):
                    # Add classes that are subclasses of forcefield or generic
                    if inspect.isclass(obj) and (issubclass(obj, forcefield) or issubclass(obj, generic)) and obj not in {forcefield, generic}:
                        subclasses.add(obj)
                        classes_to_check.append(obj)
                    # Also add relevant high-level methods/functions that do not start with '_'
                    elif (inspect.isfunction(obj) or inspect.ismethod(obj)) and not name.startswith('_'):
                        # Check if the method belongs to a class derived from generic, not forcefield
                        parent_class_name = obj.__qualname__.split('.')[0]
                        parent_class = next((cls for cls in subclasses if cls.__name__ == parent_class_name), None)
                        if parent_class and issubclass(parent_class, generic) and not issubclass(parent_class, forcefield):
                            subclasses.add((parent_class, name, obj))  # Add (parent_class, method_name, function/method)
    
        # Traverse through all found subclasses
        while classes_to_check:
            parent_class = classes_to_check.pop()
            for subclass in parent_class.__subclasses__():
                subclasses.add(subclass)
                classes_to_check.append(subclass)
    
        # Prepare the output dictionary with load status flags and default parameters
        subclass_info = {}
        short_name_mapping = {}
    
        for subclass in subclasses:
            if inspect.isclass(subclass):
                class_name = subclass.__name__
                is_loaded = class_name in globals()  # Check if class is already loaded
    
                # Extract default parameters if they exist
                extracted_params = cls.extract_default_parameters(subclass, displayflag=False)
                num_defaults = len(extracted_params.get('parameters', {}).keys()) if extracted_params else None
    
                # Check if RULES, GLOBAL, and LOCAL are defined
                rules_defined = ''
                if extracted_params:
                    rules_defined += 'R' if extracted_params["RULES"] else '-'
                    rules_defined += 'G' if extracted_params["GLOBAL"] else '-'
                    rules_defined += 'L' if extracted_params["LOCAL"] else '-'
    
                # Add entry for the class
                subclass_info[class_name] = {
                    "loaded": is_loaded,
                    "module": subclass.__module__,
                    "num_defaults": num_defaults,
                    "rules_defined": rules_defined if rules_defined else '---'  # Display as '---' if none defined
                }
    
                # Map short name to full name
                short_name_mapping[class_name] = class_name
    
                # Inspect and add high-level methods from the class itself if not forcefield
                if not issubclass(subclass, forcefield):
                    for method_name, method in inspect.getmembers(subclass, predicate=inspect.isfunction):
                        if not method_name.startswith('_'):  # Skip private methods
                            method_full_name = f"{class_name}.{method_name}"
                            extracted_method_params = cls.extract_default_parameters(subclass, method_name=method_name, displayflag=False)
                            num_defaults = len(extracted_method_params.get('parameters', {}).keys()) if extracted_method_params else None
                            rules_defined = extracted_method_params.get("rules_defined", "---")
                            subclass_info[method_full_name] = {
                                "loaded": True,
                                "module": subclass.__module__,
                                "num_defaults": num_defaults,
                                "rules_defined": rules_defined
                            }
                            # Add method short name to mapping
                            short_name_mapping[method_name] = method_full_name
    
            else:
                # Handle function/method cases
                parent_class, func_name, func_obj = subclass
                is_loaded = func_name in globals() or parent_class.__module__ in sys.modules
                extracted_method_params = cls.extract_default_parameters(parent_class, method_name=func_name, displayflag=False)
                num_defaults = len(extracted_method_params.get('parameters', {}).keys()) if extracted_method_params else None
                rules_defined = extracted_method_params.get("rules_defined", "---")
                func_full_name = f"{parent_class.__name__}.{func_name}"
                subclass_info[func_full_name] = {
                    "loaded": is_loaded,
                    "module": parent_class.__module__,
                    "num_defaults": num_defaults,
                    "rules_defined": rules_defined
                }
                # Add function/method to short names
                short_name_mapping[func_name] = func_full_name
    
        # Optionally print the subclasses and their load status with parameter info
        if printflag:
            print("List of available forcefields and relevant methods:\n")
            print(f"{'Short Name':<15} {'Class/Method Name':<30} {'Module Path':<30} {'Status':<10} {'Default Params':<10} {'RULES':<5}")
            print("=" * 105)
            for short_name, class_name in sorted(short_name_mapping.items(), key=lambda x: x[0]):
                info = subclass_info[class_name]
                status = "Loaded" if info["loaded"] else "Not Loaded"
                num_defaults = info["num_defaults"] if info["num_defaults"] is not None else "None"
                rules_defined = info["rules_defined"]
                print(f"{short_name:<15} {class_name:<30} {info['module']:<30} {status:<10} {num_defaults:<10} {rules_defined:<5}")
            print(f"\nTotal number of forcefields and methods: {len(subclass_info)}")
    
        return subclass_info, short_name_mapping



    def scriptobject(self, beadtype=None, name=None, fullname=None, filename=None, group=None, style=None, USER=scriptdata()):
        """
        Method to return a scriptobject based on the current dforcefield instance.
        
        Parameters:
        ------------
        beadtype : int, optional
            The bead type identifier. Defaults to the instance's beadtype.
        
        name : str, optional
            A short name for the scriptobject. If not provided, uses 'forcefield' from self.name.
        
        fullname : str, optional
            A comprehensive name for the object. Defaults to "beads of type {self.beadtype} | object of forcefield: {self.name.forcefield}".
        
        group : list, optional
            A group of scriptobjects that this object belongs to. Defaults to an empty list.
        
        style : str, optional
            The style of the scriptobject. Defaults to `self.description.style` if available, otherwise "smd".
        
        USER : scriptdata, optional
            User-defined data for additional parameters. Defaults to a blank `scriptdata()` instance.
        
        Returns:
        --------
        scriptobject
            A scriptobject instance populated with the current `dforcefield` instance's attributes or provided arguments.
        """
        # Set defaults using instance attributes if parameters are None
        if beadtype is None:
            beadtype = self.beadtype
    
        # Extract a meaningful name from the forcefield's name structure
        if name is None:
            if isinstance(self.name, struct) and hasattr(self.name, 'material'):
                name = f"{self.name.material} bead"
            else:
                name = f"beadtype_{self.beadtype}"
    
        if fullname is None:
            fullname = f"beads of type {self.beadtype} | object of forcefield: {self.name.forcefield if isinstance(self.name, struct) and hasattr(self.name, 'forcefield') else 'unknown'}"
    
        if group is None:
            group = []
        
        # Use `self.description.style` as the default for style if it exists, otherwise fall back to "smd"
        if style is None:
            if isinstance(self.description, struct) and hasattr(self.description, 'style'):
                style = self.description.style
            else:
                style = "undefined style"
        
        # The current dforcefield instance behaves as the forcefield for the scriptobject
        forcefield = self
        
        # Apply any user-defined parameters to the forcefield
        forcefield.USER = USER
    
        # Create and return the scriptobject instance
        return scriptobject(
            beadtype=beadtype,
            name=name,
            fullname=fullname,
            filename=filename,
            style=style,
            forcefield=forcefield,  # Use the current dforcefield instance
            group=group,
            USER=USER
        )

    
    def __copy__(self):
        """
        Shallow copy method for dforcefield.
        
        Creates a shallow copy of the dforcefield instance, meaning that references
        to mutable objects like 'parameters' will not be deeply copied.
        """
        cls = self.__class__
        copie = cls.__new__(cls)
        
        # Copy the simple attributes
        copie.__dict__.update(self.__dict__)
        
        # Return the shallow copy
        return copie
    
    
    def __deepcopy__(self, memo):
        """
        Deep copy method for dforcefield.
        
        Creates a deep copy of the dforcefield instance, including its complex attributes
        like 'parameters'. This ensures that all mutable objects are fully copied, not just referenced.
        """
        cls = self.__class__
        copie = cls.__new__(cls)
        memo[id(self)] = copie
        
        # Recursively deep copy each attribute
        for k, v in self.__dict__.items():
            if k == "base_class":
                # The base_class should not be deeply copied; it's a class reference
                setattr(copie, k, self.base_class)
            else:
                # Deep copy other attributes
                setattr(copie, k, copy.deepcopy(v, memo))
        
        return copie # return copied instance


# %% DEBUG
# ===================================================
# main()
# ===================================================
# for debugging purposes (code called as a script)
# the code is called from here
# ============================
if __name__ == '__main__':
    
#     # ---------------------------------------------------------------
#     # The examples below reconstruct dynamycally the FF:
#     #       * water from pizza.forcefield.water()
#     #       * solidfood from pizza.forcefield.solidfood()
#     #       * salt from pizza.forcefield.saltTLSPH()
#     #       * rigidwall from pizza.forcefield.rigidwall()
#     # ---------------------------------------------------------------
    
#     # List available forcefields
#     dforcefield.list_forcefield_subclasses(printflag=True,additional_modules=None) # we could add other modules
    
#     # We reuse a high-level forcefield
#     mywater = dforcefield(
#         base_class="water",
#         userid = "my customized water",
#         rho = 900,
#         q1 = 0.1
#         )
    
#     # Test dynamic water class using ulsph as the base class
#     dynamic_water = dforcefield(
#         base_class='ulsph',
#         beadtype=1,
#         userid="dynamic_water",
#         USER=parameterforcefield(
#             rho=1000,
#             c0=10.0,
#             q1=1.0,
#             Cp=1.0,
#             taitexponent=7,
#             contact_scale=1.5,
#             contact_stiffness="2.5*${c0}^2*${rho}"
#         )
#     )
#     print(f"Water parameters: {dynamic_water.parameters}")
#     print(f"Water name: {dynamic_water.name}")
#     print(f"Water Cp: {dynamic_water.Cp}")
#     dynamic_water
    
#     # Test dynamic solidfood class using tlsph as the base class
#     dynamic_solidfood = dforcefield(
#         base_class='tlsph',
#         beadtype=2,
#         userid="dynamic_solidfood",
#         #USER=parameterforcefield( #<--- note that USER is not used in this case
#             rho=1000,
#             c0=10.0,
#             E="5*${c0}^2*${rho}",
#             nu=0.3,
#             q1=1.0,
#             q2=0.0,
#             Hg=10.0,
#             Cp=1.0,
#             sigma_yield="0.1*${E}",
#             hardening=0,
#             contact_scale=1.5,
#             contact_stiffness="2.5*${c0}^2*${rho}"
#         #)
#     )
#     print(f"Solidfood parameters: {dynamic_solidfood.parameters}")
#     print(f"Solidfood name: {dynamic_solidfood.name}")
#     repr(dynamic_solidfood)
    
#     # Test dynamic saltTLSPH class using tlsph as the base class
#     dynamic_salt = dforcefield(
#         base_class='tlsph',
#         beadtype=3,
#         userid="dynamic_salt",
#         USER=parameterforcefield(
#             rho=1000,
#             c0=10.0,
#             E="5*${c0}^2*${rho}",
#             nu=0.3,
#             q1=1.0,
#             q2=0.0,
#             Hg=10.0,
#             Cp=1.0,
#             sigma_yield="0.1*${E}",
#             hardening=0,
#             contact_scale=1.5,
#             contact_stiffness="2.5*${c0}^2*${rho}"
#         )
#     )
#     print(f"Salt TLSPH parameters: {dynamic_salt.parameters}")
#     print(f"Salt TLSPH name: {dynamic_salt.name}")
#     repr(dynamic_salt)
    
#     # Test dynamic rigidwall class using none as the base class
#     dynamic_rigidwall = dforcefield(
#         base_class='none',  # Assuming a class `none` exists
#         beadtype=4,
#         userid="dynamic_rigidwall",
#         USER=parameterforcefield(
#             rho=3000,
#             c0=10.0,
#             contact_scale=1.5,
#             contact_stiffness="2.5*${c0}^2*${rho}"
#         )
#     )
#     print(f"Rigidwall parameters: {dynamic_rigidwall.parameters}")
#     print(f"Rigidwall name: {dynamic_rigidwall.name}")
#     repr(dynamic_rigidwall)


#     # create a new food and save it on disk
#     newfood = dynamic_solidfood.copy(rho=2100,q1=4,E=1000,name="new food")
#     repr(newfood)
#     newfood.base_repr()
#     fname = newfood.save(overwrite=True)
    
#     # load again the same file
#     newfood2 = dforcefield.load(fname)
    
#     # compare the content
#     newfood.compare(newfood2,printflag=True)
    
#     # note that the variables are automatically identified and added to parameters if missing 
#     newfood.parameters = parameterforcefield(a=1,b=2)
#     missingvars = newfood.missingVariables()
#     print('updated newfood:\n')
#     repr(newfood)
#     print('missing variables in updated newfood:\n')
#     repr(missingvars)
    
#     # compare the content
#     newfood.compare(newfood2,printflag=True)
    
#     # check the parser
#     content = """
# # DFORCEFIELD SAVE FILE
# base_class="tlsph"
# beadtype = 1
# userid = "dynamic_water"
# version = 1.0

# description:{forcefield="LAMMPS:SMD", style="tlsph", material="water"}
# name:{forcefield="LAMMPS:SMD", material="water"}

# rho = 1000
# E = "5*${c0}^2*${rho}"
# nu = 0.3
# """
#     parsed_forcefield = dforcefield.parse(content)
#     print(parsed_forcefield.script)
    
#     # create a script object
#     obj = parsed_forcefield .scriptobject(group="A")
    
    
#     # *********************************************************************************************
#     # Production Example: Scriptobject Creation and Combination
#     # 
#     # This example demonstrates the creation and combination of `scriptobject` instances from both
#     # static forcefield classes and dynamic forcefield instances (via `dforcefield`).
#     # 
#     # Key Points:
#     # ------------
#     # 1. **Static and Dynamic Forcefields**: 
#     #    - Scriptobjects can be created using static forcefields (e.g., `rigidwall`, `solidfood`, etc.)
#     #      or dynamic forcefields generated from a `dforcefield` instance (e.g., `waterFF`).
#     #    - Dynamic forcefields can either be passed directly to the `pizza.script.scriptobject()`
#     #      constructor or instantiated through the `scriptobject` method of any `pizza.dforcefield` object.
#     #
#     # 2. **Combining Scriptobjects**: 
#     #    - Scriptobjects can be combined using the `+` operator to create a collection of objects.
#     #    - This collection of scriptobjects can then be scripted dynamically using the `script` property
#     #      to generate their interaction definitions.
#     #
#     # 3. **Geometry Input**: 
#     #    - Geometry for the scriptobjects can be provided either via an input file (using `filename`)
#     #      or dynamically using `pizza.region.region()`.
#     #
#     # **********************************************************************************************
    
    from pizza.forcefield import rigidwall, solidfood, water
    
    # Create a dynamic forcefield for water with a specific density (rho=900) and beadtype=1
    waterFF = dforcefield(base_class="water", rho=900, beadtype=1)
    
    # Define water beads using the dforcefield instance's scriptobject method
    bwater = waterFF.scriptobject(name="water", group=["A", "D"], filename="mygeom")
    
    # Alternatively, define water beads by passing the dynamic forcefield directly to scriptobject
    bwater2 = scriptobject(name="water", group=["A", "D"], filename="mygeom", forcefield=waterFF)
    
    # Define other dummy beads using static forcefields
    b1 = scriptobject(name="bead 1", group=["A", "B", "C"], filename='myfile1', forcefield=rigidwall())
    b2 = scriptobject(name="bead 2", group=["B", "C"], filename='myfile1', forcefield=rigidwall())
    b3 = scriptobject(name="bead 3", group=["B", "D", "E"], forcefield=solidfood())
    b4 = scriptobject(name="bead 4", group="D", beadtype=1, filename="myfile2", forcefield=water())
    
    # Combine the scriptobjects into a collection using the '+' operator
    collection = bwater + b1 + b2 + b3 + b4
    
    # Generate the script for the interactions in the collection
    collection.script
    
    # Similarly, using the alternate water bead definition (bwater2)
    collection2 = bwater2 + b1 + b2 + b3 + b4
    collection2.script


    # *********************************************************************************************
    # Example: Using Dynamic Forcefields from `pizza.generic` alongside `forcefield` Classes
    #
    # This example illustrates how to use dynamic forcefields defined within `pizza.generic` 
    # and integrate them seamlessly with existing `forcefield` classes for simulation scripting.
    #
    # Key Points:
    # ------------
    # 1. **Dynamic Forcefields via Generic Classes**:
    #    - The `generic` module allows defining new forcefields dynamically through high-level methods
    #      (e.g., `newtonianfluid` from `USERSMD`) without predefining them as static classes.
    #    - Forcefields can be dynamically instantiated using the `dforcefield` class and linked to 
    #      these high-level methods via `additional_modules`.
    #
    # 2. **Integration with Existing Forcefields**:
    #    - `dforcefield` instances created from `generic` methods are fully compatible with other 
    #      static forcefield classes (e.g., `rigidwall`, `solidfood`).
    #    - Scriptobjects created from these dynamic instances can be combined and scripted like 
    #      any other forcefield-derived objects.
    #
    # 3. **Workflow**:
    #    - Specify the additional modules where the high-level forcefield definitions reside (e.g., `generic`).
    #    - Initialize the `dforcefield` with the specific method name (e.g., `newtonianfluid`) to dynamically create 
    #      the forcefield.
    #    - Use the created dynamic forcefield instance to define scriptobjects and combine them with others 
    #      in a collection for interactive scripting.
    #
    # *********************************************************************************************
    
    from pizza.forcefield import rigidwall, solidfood, water
    from pizza.generic import generic
    
    # Step 1: Specify the additional module(s) where USERSMD and its methods are located
    additional_modules = [generic]  # Can also be a string like "generic" if import resolves correctly
    
    # Step 2: Initialize a dynamic forcefield using `newtonianfluid` from USERSMD via additional_modules
    dynamic_ff = dforcefield(
        base_class="newtonianfluid",  # Use the name of the function from USERSMD
        beadtype=6,
        userid="fluid_instance",
        additional_modules=additional_modules,
    )
    
    # Display the dynamic forcefield instance
    print("\nDynamic dforcefield instance based on generic.newtonianfluid:\n")
    repr(dynamic_ff)
    
    # Define a scriptobject using the dynamic forcefield instance
    bwater3 = dynamic_ff.scriptobject(name="water_newtonian", group=["A", "D"], filename="mygeomXX")
    
    # Combine this scriptobject with an existing collection
    collection3 = collection2 + bwater3
    
    # Generate the script for the interactions in the new collection
    collection3.script
