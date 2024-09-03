#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================================================
PIZZA.DSCRIPT Module Documentation
================================================================================

The PIZZA.DSCRIPT module is designed to dynamically generate and manage pizza.scripts, 
especially for use with LAMMPS (Large-scale Atomic/Molecular Massively Parallel Simulator). 
The module allows you to create complex, parameterized scripts, manage multiple script 
sections, and concatenate scripts flexibly, supporting pipelines and advanced control 
over script execution and generation.

In shorts, use pizza.script to define codelets/scriptlets in maintainable libraries.
Prefer pizza.dscript to generate dynamically codelets/scriptlets directly in your code.
The output of pizza.dscript.script() is a full script instance, which can be managed
as standard pizza.scripts, combined with + | and added in pizza.pipescripts.


Goal:
-----
- Dynamically create and manage LAMMPS sections and scripts.
- Merge, manipulate, and execute multiple script sections with predefined or user-defined variables.
- Generate scripts with conditional sections and custom execution logic.

Key Classes:
------------
- `lambdaScriptdata`: Holds parameters and definitions for script execution.
- `lamdaScript`: Wraps a `dscript` object to generate a script instance from its contents.
- `dscript`: Manages and stores multiple script lines (as `ScriptTemplate` objects), 
             handles dynamic execution, and supports concatenation of script sections.

Practical Usage:
----------------
- Scripts can be combined dynamically.
- Variables in script templates are handled automatically, allowing flexible script execution.
- Concatenate multiple scripts, with automatic merging and non-overwriting of variables.

The concept of TEMPLATING is managed via shorthands

from dscript import dscript

        ```python
        # Create a dscript instance
        S = dscript(name="MyScript")
        
        # Define script sections
        S[0] = "instruction 1"
        S[1] = "${var1} + ${var2}"
        
        # Set definitions
        S.DEFINITIONS.var1 = "1"
        S.DEFINITIONS.var2 = "2"
        
        # Enable evaluation
        S[1].eval = True
        
        # Generate the script
        result = S.do()
        print(result)
        
        # convert it into pizza.script 
        s=S.script()
        rs = s.do()
        print(rs)
        ```

================================================================================
Production Example: Dynamic LAMMPS Script Generation Using `dscript` and `script`
================================================================================

This example illustrates how to dynamically generate and manage LAMMPS scripts 
using the `dscript` and `script` classes. The goal is to demonstrate the flexibility 
of these classes in handling script sections, overriding parameters, and generating 
a script with conditions and dynamic content.

Overview:
---------
    In this example, we:
    - Define global `DEFINITIONS` that hold script parameters.
    - Create a script template with multiple lines, each identified by a unique key.
    - Add conditions to script lines to control their inclusion based on the state of variables.
    - Overwrite `DEFINITIONS` at runtime to customize the script's behavior.
    - Generate and execute the script using the `do()` method.

Key Classes Used:
-----------------
    - `dscript`: Manages multiple script lines and their dynamic execution.
    - `lamdaScript`: Wraps a `dscript` object to generate a script instance from its contents.

Practical Steps:
----------------
    1. Initialize a `dscript` object and define global variables (DEFINITIONS).
    2. Create script lines using keys to identify each line.
    3. Apply conditions to script lines to control their execution.
    4. Overwrite or add new variables to `DEFINITIONS` at runtime.
    5. Generate the final script using `lamdaScript` and execute it.

Example:
--------
    # Initialize the dscript object
    R = dscript(name="ProductionExample")
    
    # Define global variables (DEFINITIONS)
    R.DEFINITIONS.dimension = 3
    R.DEFINITIONS.units = "$si"
    R.DEFINITIONS.boundary = ["sm","sm","sm"]
    R.DEFINITIONS.atom_style = "$smd"
    R.DEFINITIONS.atom_modify = ["map","array"]
    R.DEFINITIONS.comm_modify = ["vel","yes"]
    R.DEFINITIONS.neigh_modify = ["every",10,"delay",0,"check","yes"]
    R.DEFINITIONS.newton = "$off"
    
    # Define the script template, with each line identified by a key
    R[0]        = "% ${comment}"
    R["dim"]    = "dimension    ${dimension}"  # Line identified as 'dim'
    R["unit"]   = "units        ${units}"      # Line identified as 'unit'
    R["bound"]  = "boundary     ${boundary}"
    R["astyle"] = "atom_style   ${atom_style}"
    R["amod"]   = "atom_modify  ${atom_modify}"
    R["cmod"]   = "comm_modify  ${comm_modify}"
    R["nmod"]   = "neigh_modify ${neigh_modify}"
    R["newton"] = "newton       ${newton}"
    
    # Apply a condition to the 'astyle' line; it will only be included if ${atom_style} is defined
    R["astyle"].condition = "${atom_style}"
    
    # Revise the DEFINITIONS, making ${atom_style} undefined
    R.DEFINITIONS.atom_style = ""
    
    # Generate a script instance, overwriting the 'units' variable and adding a comment
    sR = R.script(units="$lj",  # Use "$" to prevent immediate evaluation
                  comment="$my first dynamic script")
    
    # Execute the script to get the final content
    ssR = sR.do()
    
    # Print the generated script as text
    print(ssR)

Expected Output:
----------------
    Depending on the conditions and overwritten variables, the output script should 
    reflect the updated `DEFINITIONS` and the conditionally included lines.

For instance:
    - The line for `atom_style` will be omitted because `atom_style` is undefined.
    - The script will include the custom units and comment specified at runtime.


Some Comments:
--------------
    pizza.dscript does not not require the definition of modules, submodules and so on.
    For comparison, pizza.script requires managing directly classes

    Usage Example
    -------------
    ```python
    from pizza.script import script

    class scriptexample(script):
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

    s1 = scriptexample()
    s1.do()
    ```
  


Created on Mon Sep 2 09:38:51 2024

Dependencies
------------
- Python 3.x
- LAMMPS
- pizza3.pizza

Installation
------------
To use the REGION module, ensure that you have Python 3.x and LAMMPS installed. You can integrate the module into your project by placing the `region.py` file in your working directory or your Python path.

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
__version__ = "0.90"



# INRAE\Olivier Vitrac - rev. 2024-08-31 (community)
# contact: olivier.vitrac@agroparistech.fr, han.chen@inrae.fr

# Revision history
# 2024-09-02 alpha version (compatibility issues with pizza.script)
# 2024-09-03 release candidate (fully compatible with pizza.script)


# Dependencies
import re, string, random
from pizza.private.struct import paramauto
from pizza.script import script


# %% Low-level classes

class lambdaScriptdata(paramauto):
    """
    Class to manage lambda script parameters.
    
    This class holds definitions and variables used within the script templates. 
    These parameters are typically set up as global variables that can be accessed 
    by script sections for evaluation and substitution.

    Example Usage:
    --------------
    definitions = lambdaScriptdata(var1=10, var2="value")

    Attributes:
    -----------
    _type : str
        The type of the data ("LSD" by default).
    _fulltype : str
        Full type description of the lambda script data.
    _ftype : str
        Short description of the type (parameter definition).
    
    Methods:
    --------
    This class inherits methods from the `paramauto` class, which allows automatic 
    handling of parameters and script data.
    """
    
    _type = "LSD"
    _fulltype = "Lambda Script Parameters"
    _ftype = "parameter definition"


class lamdaScript(script):

    """
    lamdaScript
    ===========

    The `lamdaScript` class is a specialized subclass of `script` that acts as a wrapper
    for generating script objects from `dscript` instances. It facilitates the creation
    of scripts with persistent storage options and user-defined configurations.

    Attributes
    ----------
    name : str
        The name of the script.
    SECTIONS : list
        Inherited list of script sections from the `script` class.
    position : int
        The position index of the script section.
    role : str
        The role of the script section, derived from its position.
    description : str
        A brief description of the script.
    userid : str
        The user ID associated with the script.
    version : float
        The version of the script.
    verbose : bool
        Flag to enable verbose output.
    DEFINITIONS : scriptdata
        Definitions of variables used in the script.
    USER : lambdaScriptdata
        User-defined variables specific to `lamdaScript`.
    TEMPLATE : dict
        A dictionary of script templates.

    Methods
    -------
    do()
        Generates the complete LAMMPS script by processing all script sections.

    Special Methods
    ----------------
    __contains__(key)
        Allows checking if a specific section exists using the `in` keyword.
    __str__()
        Returns the string representation of the script.

    Usage Example
    -------------
    ```python
    from dscript import lamdaScript, dscript

    # Create an existing dscript instance
    existing_dscript = dscript(name="ExistingScript")
    existing_dscript.role = "Custom Role"

    # Create a lamdaScript instance based on the existing dscript
    ls = lamdaScript(existing_dscript)
    print(ls.role)  # Outputs: "Custom Role"
    ```
    """
    name = ""
    
    def __init__(self, dscriptobj, persistentfile=True, persistentfolder=None, **userdefinitions):
        """
        Initialize a new `lamdaScript` instance.
        
        This constructor creates a `lamdaScript` object based on an existing `dscriptobj`, allowing for persistent storage options and user-defined configurations.
        
        Parameters
        ----------
        dscriptobj : dscript
            An existing `dscript` object to base the new instance on.
        persistentfile : bool, optional
            If `True`, the script will be saved to a persistent file. Defaults to `True`.
        persistentfolder : str or None, optional
            The folder where the persistent file will be saved. If `None`, a temporary location is used. Defaults to `None`.
        **userdefinitions
            Additional user-defined variables and configurations.
        
        Raises
        ------
        TypeError
            If `dscriptobj` is not an instance of the `dscript` class.
        
        Example
        -------
        ```python
        existing_dscript = dscript(name="ExistingScript")
        ls = lamdaScript(existing_dscript, var3="3")
        ```
        """
        if not isinstance(dscriptobj, dscript):
            raise TypeError(f"The 'dscriptobj' object must be of class dscript not {type(dscriptobj).__name__}.")
        super().__init__(persistentfile, persistentfolder, **userdefinitions)
        self.name = dscriptobj.name
        self.SECTIONS = dscriptobj.SECTIONS
        self.section = dscriptobj.section
        self.position = dscriptobj.position
        self._role = dscriptobj.role  # Initialize an internal storage for the role
        self.description = dscriptobj.description
        self.userid = dscriptobj.userid
        self.version= dscriptobj.version
        self.verbose = dscriptobj.verbose
        self.DEFINITIONS = dscriptobj.DEFINITIONS
        self.USER = lambdaScriptdata(**self.USER)
        self.TEMPLATE = dscriptobj.do()
        
    @property
    def role(self):
        """Override the role property to include a setter."""
        # If _role is set, return it; otherwise, use the inherited logic
        if self._role is not None:
            return self._role
        elif self.section in range(len(self.SECTIONS)):
            return self.SECTIONS[self.section]
        else:
            return ""

    @role.setter
    def role(self, value):
        """Allow setting the role."""
        self._role = value    


# %% Main Classes
class ScriptTemplate:
    """
    ScriptTemplate: A Single Line Script Representation with Attributes

    The `ScriptTemplate` class is used to represent a single line in a script, 
    along with its associated attributes and conditions. This class allows for 
    dynamic management of individual script lines, including the evaluation of 
    variables and conditional execution.

    Key Features:
    -------------
    - **Flexible Line Management**: Manage a single line of a script, including 
      the content and associated attributes such as conditions for execution.
    - **Variable Substitution**: Automatically identify and manage variables 
      within the script line, allowing for dynamic substitution at runtime.
    - **Conditional Execution**: Define conditions that determine whether the 
      script line should be included in the final script output.

    Practical Use Cases:
    --------------------
    - **Single Line Control**: Control and manipulate individual lines within 
      a larger script, especially in dynamically generated scripts.
    - **Custom Conditions**: Apply custom conditions to script lines to include 
      or exclude them based on specific criteria.
    - **Dynamic Variable Handling**: Automatically detect and manage variables 
      within the script line.

    Example:
    --------
    # Create a ScriptTemplate object with some content
    line = ScriptTemplate("dimension    ${dimension}")

    # Set an attribute
    line.facultative = True

    # Print the line with attributes
    print(line)

    Attributes:
    -----------
    content : str
        The actual content of the script line. Variables within the content 
        are identified using the ${varname} syntax and can be substituted 
        dynamically.
    facultative : bool
        Indicates whether the script line is optional. If True, the line may 
        be excluded from the final script output based on certain conditions.
    eval : bool
        Determines if the line's content should be evaluated (i.e., variables 
        substituted) during script execution. If False, the content remains 
        unchanged.
    readonly : bool
        If True, the script line is read-only and cannot be modified once set. 
        This is useful for locking certain lines to prevent further changes.
    definitions : lambdaScriptdata, optional
        A reference to the `lambdaScriptdata` object that holds the global 
        definitions for the script. This is used for variable substitution 
        within the script line.
    """
    
    def __init__(self, content, definitions=None):
        """
        Initializes a new `ScriptTemplate` object.

        The constructor sets up a new script line with its content and optional 
        global definitions for variable substitution. The `ScriptTemplate` 
        allows you to manage the script line's attributes and dynamically 
        substitute variables.

        Parameters:
        -----------
        content : str
            The content of the script line. This string can include variables 
            in the format ${varname}, which will be substituted based on the 
            `definitions` provided.
        definitions : lambdaScriptdata, optional
            A reference to a `lambdaScriptdata` object that contains global 
            variable definitions. If provided, it will be used to substitute 
            variables within the content.
            
        Methods:
        --------
        __init__(self, content, definitions=None):
            Initializes a new `ScriptTemplate` object.
    
        __str__(self):
            Returns a summary of the script line, indicating the number of attributes.
            Shortcut: `str(line)`.
    
        __repr__(self):
            Provides a detailed, tabulated string representation of the script line, 
            showing the content, attributes, and evaluated result if applicable.
            Useful for debugging and detailed inspection.
    
        __setattr__(self, name, value):
            Sets an attribute for the script line. Enforces type checking for 
            specific attributes (`facultative`, `eval`, `readonly`). Automatically 
            detects and adds variables to definitions when `content` is set.
    
        __getattr__(self, name):
            Retrieves the value of an attribute. Returns None if the attribute 
            does not exist.
    
        do(self, protected=True):
            Returns the processed content of the script line, with variables 
            substituted based on the definitions and conditions applied. 
            If the line is facultative and the condition is not met, an empty 
            string is returned.

        Example:
        --------
        # Create a ScriptTemplate object with content and optional definitions
        line = ScriptTemplate("dimension    ${dimension}")

        # You can also pass in global definitions if needed
        global_definitions = lambdaScriptdata(dimension=3)
        line_with_defs = ScriptTemplate("dimension    ${dimension}", 
                                        definitions=global_definitions)

        After initialization, you can modify the line's attributes or use it as 
        part of a larger script managed by a `dscript` object.
        """
        
        self.attributes = {
            'facultative': False,  # Default attribute (if True the content is discarded)
            'eval': False,         # Default attribute (the content is not evaluated with formateval)
            'readonly': False,     # Default attribute (keep it False at the initialization, if not the content cannot be set)
            'condition': None,     # Default condition (None means no condition)
            'condeval': False,     # Default condition (if True, eval is applied)
            'detectvar':True       # Default condition (if True, automatically detect variables)
        }
        self.definitions = definitions  # Reference to the DEFINITIONS object
        self.content = content      # order is important in constructor (content should be last)

    def __str__(self):
        num_attrs = len(self.attributes)  # All attributes count
        return f"1 line, {num_attrs} attributes"

    def __repr__(self):
        repr_str = f"{'Template Content':<50}\n"
        repr_str += "-" * 50 + "\n"
        # Truncate the content if necessary
        truncated_line = (self.content[:18] + '[...]' + self.content[-18:]) if len(self.content) > 40 else self.content
        repr_str += f"{truncated_line:<50}\n"
        if (self.definitions is not None) and isinstance(content,str) and self.attributes["eval"]:
            repr_str += f"= {self.definitions.formateval(self.content,True):<50}\n"

        # Add attributes
        repr_str += f"\n{'Template Attributes':<20} {'Value':<30}\n"
        repr_str += "-" * 50 + "\n"
        for attr, value in self.attributes.items():
            if attr == 'definitions':
                continue
            repr_str += f"{attr:<20} {str(value):<30}\n"
        return repr_str

    def __setattr__(self, name, value):
        if name in ['facultative',"eval","readonly"]:
            if not isinstance(value, bool):
                raise TypeError(f"The '{name}' attribute must be a Boolean, not {type(value).__name__}.")
        elif name == 'condition':
            if not isinstance(value, str) and value is not None:
                raise TypeError(f"The 'condition' attribute must be a string or None, not {type(value).__name__}.")
        elif name == 'content':
            if not isinstance(value, str):
                raise TypeError(f"The 'content' attribute must be a string, not {type(value).__name__}.")
            elif self.attributes['readonly']:
                raise AttributeError("Cannot modify content. It is read-only.")  
        elif name =="definitions":
            if (not isinstance(value,lambdaScriptdata)) and (value is not None):
                raise TypeError(f"The 'definitions' must be a lambdaScriptdata, not {type(value).__name__}.")
        # If the name is 'content' or 'attributes', handle as usual
        if name in ['content', 'attributes', 'definitions']:
            super().__setattr__(name, value)
            # If the name is 'content', process the content for variables
            if name == 'content' and self.attributes["detectvar"] and isinstance(value, str) and self.definitions is not None:
                # Find all occurrences of ${varname}
                variables = re.findall(r'\$\{(\w+)\}', value)
                # Add each variable to definitions if not already present
                for varname in variables:
                    if varname not in self.definitions:
                        self.definitions.setattr(varname, "${" + varname + "}")
        else:
            self.attributes[name] = value

    def __getattr__(self, name):
        if name == 'content':
            return super().__getattr__(name)
        return self.attributes.get(name, None)
    
    def do(self, protected=True):
        """Executes the script template, processing its content based on the attributes."""
        if self.attributes["facultative"]:
            return ""
        if self.attributes["condition"] is not None:
            cond = self.definitions.formateval(self.attributes["condition"],protected)
            if self.attributes["condeval"]:
                cond = eval(cond)
        else:
            cond = True
        if cond:
            if self.attributes["eval"]:
                return self.definitions.formateval(self.content,protected)
            else:
                return self.content
        else:
            return ""


class dscript:
    """
    dscript: A Dynamic Script Management Class

    The `dscript` class is designed to manage and dynamically generate multiple 
    lines of a script, typically for use with LAMMPS or similar simulation tools. 
    Each line in the script is represented as a `ScriptTemplate` object, and the 
    class provides tools to easily manipulate, concatenate, and execute these 
    script lines.

    Key Features:
    -------------
    - **Dynamic Script Generation**: Define and manage script lines dynamically, 
      with variables that can be substituted at runtime.
    - **Conditional Execution**: Add conditions to script lines so they are only 
      included if certain criteria are met.
    - **Script Concatenation**: Combine multiple script objects while maintaining 
      control over variable precedence and script structure.
    - **User-Friendly Access**: Easily access and manipulate script lines using 
      familiar Python constructs like indexing and iteration.

    Practical Use Cases:
    --------------------
    - **Custom LAMMPS Scripts**: Generate complex simulation scripts with varying 
      parameters based on dynamic conditions.
    - **Automation**: Automate the creation of scripts for batch processing, 
      simulations, or other repetitive tasks.
    - **Script Management**: Manage and version-control different script sections 
      and configurations easily.
      
    Methods:
    --------
    __init__(self, name=None):
        Initializes a new `dscript` object with an optional name.

    __getitem__(self, key):
        Retrieves a script line by its key. If a list of keys is provided, 
        returns a new `dscript` object with lines reordered accordingly.

    __setitem__(self, key, value):
        Adds or updates a script line. If the value is an empty list, the 
        corresponding script line is removed.

    __delitem__(self, key):
        Deletes a script line by its key.

    __contains__(self, key):
        Checks if a key exists in the script. Allows usage of `in` keyword.

    __iter__(self):
        Returns an iterator over the script lines, allowing for easy iteration 
        through all lines in the `TEMPLATE`.

    __len__(self):
        Returns the number of script lines currently stored in the `TEMPLATE`.

    __str__(self):
        Returns a human-readable summary of the script, including the number 
        of lines and total attributes. Shortcut: `str(S)`.

    __repr__(self):
        Provides a detailed string representation of the entire `dscript` object, 
        including all script lines and their attributes. Useful for debugging.

    reorder(self, order):
        Reorders the script lines based on a given list of indices, creating a 
        new `dscript` object with the reordered lines.

    get_content_by_index(self, index, do=True, protected=True):
        Returns the processed content of the script line at the specified index, 
        with variables substituted based on the definitions and conditions applied.

    get_attributes_by_index(self, index):
        Returns the attributes of the script line at the specified index.

    createEmptyVariables(self, vars):
        Creates new variables in `DEFINITIONS` if they do not already exist. 
        Accepts a single variable name or a list of variable names.

    script(self, **userdefinitions):
        Generates a `lamdaScript` object from the current `dscript` object, 
        applying any additional user definitions provided.

    do(self):
        Executes all script lines in the `TEMPLATE`, concatenating the results, 
        and handling variable substitution. Returns the full script as a string.

    Example:
    --------
    # Create a dscript object
    R = dscript(name="MyScript")

    # Define global variables (DEFINITIONS)
    R.DEFINITIONS.dimension = 3
    R.DEFINITIONS.units = "$si"

    # Add script lines
    R[0] = "dimension    ${dimension}"
    R[1] = "units        ${units}"

    # Generate and print the script
    sR = R.script()
    print(sR.do())

    Attributes:
    -----------
    name : str
        The name of the script, useful for identification.
    TEMPLATE : dict
        A dictionary storing script lines, with keys to identify each line.
    DEFINITIONS : lambdaScriptdata
        Stores the variables and parameters used within the script lines.
    """
    
    def __init__(self,  name=None,
                        SECTIONS = ["DYNAMIC"],
                        section = 0,
                        position = None,
                        role = "dscript instance",
                        description = "dynamic script",
                        userid = "dscript",
                        version = 0.1,
                        verbose = False):
        """
        Initializes a new `dscript` object.

        The constructor sets up a new `dscript` object, which allows you to 
        define and manage a script composed of multiple lines. Each line is 
        stored in the `TEMPLATE` dictionary, and variables used in the script 
        are stored in `DEFINITIONS`.

        Parameters:
        -----------
        name : str, optional
            The name of the script. If no name is provided, a random name will 
            be generated automatically. The name is useful for identifying the 
            script, especially when managing multiple scripts.

        Example:
        --------
        # Create a dscript object with a specific name
        R = dscript(name="ExampleScript")

        # Or create a dscript object with a random name
        R = dscript()

        After initialization, you can start adding script lines and defining variables.
        """
        
        if name is None:
            self.name = ''.join(random.choices(string.ascii_letters, k=8))  # Generates a random name of 8 letters
        else:
            self.name = name
        self.SECTIONS = SECTIONS
        self.section = section
        self.position = position if position is not None else 0
        self.role = role
        self.description = description
        self.userid = userid
        self.version = version
        self.verbose = verbose
        self.DEFINITIONS = lambdaScriptdata()
        self.TEMPLATE = {}

    def __getitem__(self, key):
        if isinstance(key, list):
            # If key is a list, reorder the TEMPLATE based on the list of indices
            return self.reorder(key)
        else:
            # Otherwise, treat key as a normal index or key
            return self.TEMPLATE[key]

    def __setitem__(self, key, value):
        if (value == []) or (value is None):
            # If the value is an empty list, delete the corresponding key
            del self.TEMPLATE[key]
        else:
            # Otherwise, set the key to the new ScriptTemplate
            self.TEMPLATE[key] = ScriptTemplate(value, definitions=self.DEFINITIONS)

    def __delitem__(self, key):
        del self.TEMPLATE[key]

    def __iter__(self):
        return iter(self.TEMPLATE.items())

    def keys(self):
        return self.TEMPLATE.keys()
    
    def __contains__(self, key):
        return key in self.TEMPLATE
    
    def __len__(self):
        return len(self.TEMPLATE)

    def values(self):
        return (s.content for s in self.TEMPLATE.values())

    def items(self):
        return ((key, s.content) for key, s in self.TEMPLATE.items())

    def __str__(self):
        num_TEMPLATE = len(self.TEMPLATE)
        total_attributes = sum(len(s.attributes) for s in self.TEMPLATE.values())
        return f"{num_TEMPLATE} TEMPLATE, {total_attributes} attributes"

    def __repr__(self):
        repr_str = f"dscript object with {len(self.TEMPLATE)} TEMPLATE:\n"
        c = 0
        for k, s in self.TEMPLATE.items():
            repr_str += f"\n[{c} | Template Key: {k} ]\n{repr(s)}\n"
            c += 1
        return repr_str
    
    def reorder(self, order):
        """Reorder the TEMPLATE lines according to a list of indices."""
        # Get the original items as a list of (key, value) pairs
        original_items = list(self.TEMPLATE.items())
        # Create a new dictionary with reordered scripts, preserving original keys
        new_scripts = {original_items[i][0]: original_items[i][1] for i in order}
        # Create a new dscript object with reordered scripts
        reordered_script = dscript()
        reordered_script.TEMPLATE = new_scripts
        return reordered_script
    
    def get_content_by_index(self, index, do=True, protected=True):
        """ Returns the content of the ScriptTemplate at the specified index."""
        key = list(self.TEMPLATE.keys())[index]
        s = self.TEMPLATE[key].content
        att = self.TEMPLATE[key].attributes
        if att["facultative"] and do:
            return ""
        if att["condition"] is not None:
            cond = eval(self.DEFINITIONS.formateval(att["condition"],protected))
        else:
            cond = True
        if cond:
            if att["eval"] and do:
                return self.DEFINITIONS.formateval(s,protected)
            else:
                return s
        elif do:
            return ""
        else:
            return s

    def get_attributes_by_index(self, index):
        """ Returns the attributes of the ScriptTemplate at the specified index."""
        key = list(self.TEMPLATE.keys())[index]
        return self.TEMPLATE[key].attributes
    
    def __add__(self, other):
        """Concatenates two dscript objects."""
        if not isinstance(other, dscript):
            raise TypeError(f"Cannot concatenate 'dscript' with '{type(other).__name__}'")
        # Create a new dscript to store the result
        result = dscript()
        # Start by copying the current TEMPLATE to the result
        result.TEMPLATE = self.TEMPLATE.copy()
        # Track the next available index if keys need to be created
        next_index = len(result.TEMPLATE)
        # Add each item from the other dscript
        for key, value in other.TEMPLATE.items():
            if key in result.TEMPLATE:
                # If key is already used, assign a new key starting from 0 and incrementing
                while next_index in result.TEMPLATE:
                    next_index += 1
                result.TEMPLATE[next_index] = value
            else:
                result.TEMPLATE[key] = value        
        return result
    
    def createEmptyVariables(self, vars):
        """
        Creates empty variables in DEFINITIONS if they don't already exist.
        
        Parameters:
        -----------
        vars : str or list of str
            The variable name or list of variable names to be created in DEFINITIONS.
        """
        if isinstance(vars, str):
            vars = [vars]  # Convert single variable name to list for uniform processing
        for varname in vars:
            if varname not in self.DEFINITIONS:
                self.DEFINITIONS.setattr(varname,"${" + varname + "}")
    
    def do(self):
        """
        Executes all ScriptTemplate instances in TEMPLATE and concatenates the results.
        Includes a pretty header and footer.
        """
        header = f"# --------------[ TEMPLATE \"{self.name}\" ]--------------"
        footer = "# --------------------------------------------"
        output = [header]
        non_empty_lines = 0
        ignored_lines = 0
        for key, s in self.TEMPLATE.items():
            result = s.do()
            if result:  # Only count and include non-empty results
                output.append(result)
                non_empty_lines += 1
            else:
                ignored_lines += 1
        footer += f"\n# ---> Total lines: {non_empty_lines} - Ignored lines {ignored_lines}"
        output.append(footer)
        return "\n".join(output)
    
    def script(self,**USER):
        """
        returns the corresponding script
        """
        return lamdaScript(self,persistentfile=True, persistentfolder=None,**USER)



# %% debug section - generic code to test methods (press F5)
# ===================================================
# main()
# ===================================================
# for debugging purposes (code called as a script)
# the code is called from here
# ===================================================
if __name__ == '__main__':

    # Usage example
    # -------------
    # Initialize a dscript object
    S = dscript()
    
    # Add script lines with placeholders for variables
    S[3] = "instruction .... with substitution rules ${v1}+${var2}"
    S['alpha'] = "another script template ${v3}"
    
    # Set a custom attribute for a specific line
    S[3].attribute1 = True
    
    # Reorder script lines
    T = S[[1,0]]
    
    # Define global variables in DEFINITIONS
    S.DEFINITIONS.a = 1
    S.DEFINITIONS.b = 2
    
    # Update a script line and enable evaluation of its content
    S[0] = "$a+$b"
    S[0].eval = True
    
    # Set a line as mandatory (not facultative)
    S[3].facultative = False
    
    # Access and print the content of specific script lines
    print(S[3])       # Outputs: instruction .... with substitution rules ${v1}+${var2}
    print(S['alpha']) # Outputs: another script template ${v3}
    
    # Access and print custom attributes
    print(S[3].attribute1)  # Outputs: True
    
    # Iterate through all script lines, printing their keys and content
    for key, content in S.items():
        print(f"Key: {key}, Content: {content}")
    
    # Retrieve and evaluate the content of a script line by its index
    S.get_content_by_index(0, False)  # Retrieve without evaluation
    S.get_content_by_index(0)         # Retrieve with evaluation
    
    # Access attributes of a specific script line by index
    S.get_attributes_by_index(0)
    
    # Apply conditions to the execution of a script line
    S[0].condition = "$a>1"
    S[0].condeval = True
    S.get_content_by_index(2)  # Condition not met, may result in an empty string
    
    # Update the condition and evaluate again
    S[0].condition = "$a>0"
    S[0].do()  # Executes and evaluates the line content
    
    # Create multiple variables in DEFINITIONS if they don't already exist
    S.createEmptyVariables(["a", "b", "c", "d", "e"])
    
    # Access and print all current definitions
    S.DEFINITIONS
    
    
    # =====================================================
    # Production Example: LAMMPS Header Initialization
    #   closely related to pizza.region.LammpsHeaderInit
    # =====================================================
    # Initialize a dscript object with a custom name
    R = dscript(name="ProductionExample")
    
    # Define global variables (DEFINITIONS) for the script
    R.DEFINITIONS.dimension = 3
    R.DEFINITIONS.units = "$si"
    R.DEFINITIONS.boundary = ["sm", "sm", "sm"]
    R.DEFINITIONS.atom_style = "$smd"
    R.DEFINITIONS.atom_modify = ["map", "array"]
    R.DEFINITIONS.comm_modify = ["vel", "yes"]
    R.DEFINITIONS.neigh_modify = ["every", 10, "delay", 0, "check", "yes"]
    R.DEFINITIONS.newton = "$off"
    
    # Define the script template, associating each line with a key
    R[0]        = "% ${comment}"               # lines can be identied by numbers/names
    R["dim"]    = "dimension    ${dimension}"  # Line identified as 'dim'
    R["unit"]   = "units        ${units}"      # Line identified as 'unit'
    R["bound"]  = "boundary     ${boundary}"
    R["astyle"] = "atom_style   ${atom_style}"
    R["amod"]   = "atom_modify  ${atom_modify}"
    R["cmod"]   = "comm_modify  ${comm_modify}"
    R["nmod"]   = "neigh_modify ${neigh_modify}"
    R["newton"] = "newton       ${newton}"
    
    # Apply a condition to the 'astyle' line
    # it will only be included if ${atom_style} is defined
    R["astyle"].condition = "${atom_style}"
    
    # Update DEFINITIONS to unset the atom_style variable
    R.DEFINITIONS.atom_style = ""
    
    # Generate a script instance, overwriting the 'units' variable and adding a comment
    sR = R.script(units="$lj",  # Use "$" to prevent immediate evaluation
                  comment="$my first dynamic script")
    
    # Execute the script to generate the final content
    ssR = sR.do()
    
    # Print the generated script
    print(ssR)