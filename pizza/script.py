
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
            p = pipescript(G)*4 # using the constructor pipescript()

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

__project__ = "Pizza3"
__author__ = "Olivier Vitrac"
__copyright__ = "Copyright 2022"
__credits__ = ["Olivier Vitrac"]
__license__ = "GPLv3"
__maintainer__ = "Olivier Vitrac"
__email__ = "olivier.vitrac@agroparistech.fr"
__version__ = "0.9996"



# INRAE\Olivier Vitrac - rev. 2024-11-25 (community)
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
# 2023-01-09 update __repr__() for scripts to show both DEFINITIONS and USER if verbose = True
# 2023-01-19 fix do() for pipescripts when the pipe has been already fully executed (statically)
# 2023-01-20 add picker() and possibility to get list indices in pipe
# 2023-01-26 add pipescript.join()
# 2023-01-27 add tmpwrite()
# 2023-01-27 use % instead of $ for lists in script.do(), in line with the new feature implemented in param.eval()
# 2023-01-31 fix the temporary file on Linux
# 2023-07-14 add and implement persistentfile and peristenfolder in scripts
# 2023-07-20 add header to script.tmpwrite()
# 2023-07-20 add a persident script.preview.clean copy
# 2023-08-17 fix span() when vector is "" or str
# 2024-04-16 fix the method tmpwrite(self) on windows with proper error handling
# 2024-04-18 fix scriptobjectgroup.script for empty and None filename
# 2024-09-01 script accepts persistentfolder=None for inheritance
# 2024-10-09 verbosity handling with script.do() and pscript.do() methods, remove_comments moved to script from dscript (circular reference)
# 2024-10-12 implement | for dscript objects
# 2024-10-14 finalization of dscript integration, improved doc
# 2024-10-18 add dscript() method to generate a dscript object from a pipescript
# 2024-10-19 script.do() convert literal \\n back to \n
# 2024-10-22 fix | for non-native pipescript objects
# 2024-11-12 add flexibility to remove_comments(), comment_chars="#%", continuation_marker="..."
# 2024-11-23 improve write and do() methods (the old pipescript.do() method is available as pipescript.do_legacy() )
# 2024-11-25 clear distinction between pipescript and scrupt headers


# %% Dependencies
import os, datetime, socket, getpass, tempfile, types
from copy import copy as duplicate
from copy import deepcopy as deepduplicate
from shutil import copy as copyfile


# All forcefield parameters are stored à la Matlab in a structure
from pizza.private.struct import param,struct
from pizza.forcefield import *


# span vector into a single string
def span(vector,sep=" ",left="",right=""):
    return left + (vector if isinstance(vector, str) else sep.join(map(str, vector))) + right if vector is not None else ""

# select elements from a list L based on indices as L(indices) in Matlab
def picker(L,indices): return [L[i] for i in indices if (i>=0 and i<len(L))]

# Get the location of the `tmp` directory, in a system-independent way.
get_tmp_location = lambda: tempfile.gettempdir()

# UTF-8 encoded Byte Order Mark (sequence: 0xef, 0xbb, 0xbf)
BOM_UTF8 = b'\xef\xbb\xbf'


# %% Private functions and classes
def remove_comments(content, split_lines=False, emptylines=False, comment_chars="#", continuation_marker="\\\\", remove_continuation_marker=False):
    """
    Removes comments from a single or multi-line string, handling quotes, escaped characters, and line continuation.
    
    Parameters:
    -----------
    content : str
        The input string, which may contain multiple lines. Each line will be processed 
        individually to remove comments, while preserving content inside quotes.
    split_lines : bool, optional (default: False)
        If True, the function will return a list of processed lines. If False, it will 
        return a single string with all lines joined by newlines.
    emptylines : bool, optional (default: False)
        If True, empty lines will be preserved in the output. If False, empty lines 
        will be removed from the output.
    comment_chars : str, optional (default: "#")
        A string containing characters to identify the start of a comment. 
        Any of these characters will mark the beginning of a comment unless within quotes.
    continuation_marker : str or None, optional (default: "\\\\")
        A string containing characters to indicate line continuation (use `\\` to specify).
        Any characters after the continuation marker are ignored as a comment. If set to `None`
        or an empty string, line continuation will not be processed.
    remove_continuation_marker : bool, optional (default: False)
        If True, the continuation marker itself is removed from the processed line, keeping
        only the characters before it. If False, the marker is retained as part of the line.
    
    Returns:
    --------
    str or list of str
        The processed content with comments removed. Returns a list of lines if 
        `split_lines` is True, or a single string if False.
    """
    def process_line(line):
        """Remove comments and handle line continuation within a single line while managing quotes and escapes."""
        in_single_quote = False
        in_double_quote = False
        escaped = False
        result = []
        
        i = 0
        while i < len(line):
            char = line[i]
            
            if escaped:
                result.append(char)
                escaped = False
                i += 1
                continue
            
            # Handle escape character within quoted strings
            if char == '\\' and (in_single_quote or in_double_quote):
                escaped = True
                result.append(char)
                i += 1
                continue
            
            # Toggle state for single and double quotes
            if char == "'" and not in_double_quote:
                in_single_quote = not in_single_quote
            elif char == '"' and not in_single_quote:
                in_double_quote = not in_double_quote
            
            # Check for line continuation marker if it's set and outside of quotes
            if continuation_marker and not in_single_quote and not in_double_quote:
                # Check if the remaining part of the line matches the continuation marker
                if line[i:].startswith(continuation_marker):
                    # Optionally remove the continuation marker
                    if remove_continuation_marker:
                        result.append(line[:i].rstrip())  # Keep everything before the marker
                    else:
                        result.append(line[:i + len(continuation_marker)].rstrip())  # Include the marker itself
                    return ''.join(result).strip()
            
            # Check for comment start characters outside of quotes
            if char in comment_chars and not in_single_quote and not in_double_quote:
                break  # Stop processing the line when a comment is found
            
            result.append(char)
            i += 1
        
        return ''.join(result).strip()

    # Split the input content into lines
    lines = content.split('\n')

    # Process each line, considering the emptylines flag
    processed_lines = []
    for line in lines:
        stripped_line = line.strip()
        if not stripped_line and not emptylines:
            continue  # Skip empty lines if emptylines is False
        if any(stripped_line.startswith(c) for c in comment_chars):
            continue  # Skip lines that are pure comments
        processed_line = process_line(line)
        if processed_line or emptylines:  # Only add non-empty lines if emptylines is False
            processed_lines.append(processed_line)

    if split_lines:
        return processed_lines  # Return list of processed lines
    else:
        return '\n'.join(processed_lines)  # Join lines back into a single string


# returns the metadata
def get_metadata():
    """Return a dictionary of explicitly defined metadata."""
    import pizza.script as script # Ensure script is imported to access its globals
    # Define the desired metadata keys
    metadata_keys = [
        "__project__",
        "__author__",
        "__copyright__",
        "__credits__",
        "__license__",
        "__maintainer__",
        "__email__",
        "__version__",
    ]
    # Filter only the desired keys from the module's variables
    return {key.strip("_"): getattr(script, key) for key in metadata_keys if hasattr(script, key)}


# frames headers
def frame_header(
    lines,
    padding=2,
    style=1,
    corner_symbols=None,  # Can be a string or a tuple
    horizontal_symbol=None,
    vertical_symbol=None,
    empty_line_symbol=None,
    line_fill_symbol=None
):
    """
    Format the header content into an ASCII framed box with customizable properties.

    Parameters:
        lines (list or tuple): The lines to include in the header.
            - Empty strings "" are replaced with lines of `line_fill_symbol`.
            - None values are treated as empty lines.

        padding (int, optional): Number of spaces to pad on each side of the content. Default is 2.
        style (int, optional): Style index (1 to 6) for predefined frame styles. Default is 1.
        corner_symbols (str or tuple, optional): Symbols for the corners (top-left, top-right, bottom-left, bottom-right).
                                                 Can be a string (e.g., "+") for uniform corners.
        horizontal_symbol (str, optional): Symbol to use for horizontal lines.
        vertical_symbol (str, optional): Symbol to use for vertical lines.
        empty_line_symbol (str, optional): Symbol to use for empty lines inside the frame.
        line_fill_symbol (str, optional): Symbol to fill lines that replace empty strings.

    Returns:
        str: The formatted header as a string.

    Raises:
        ValueError: If the specified style is undefined.
    """

    # Predefined styles
    styles = {
        1: {
            "corner_symbols": ("+", "+", "+", "+"),
            "horizontal_symbol": "-",
            "vertical_symbol": "|",
            "empty_line_symbol": " ",
            "line_fill_symbol": "-"
        },
        2: {
            "corner_symbols": ("╔", "╗", "╚", "╝"),
            "horizontal_symbol": "═",
            "vertical_symbol": "║",
            "empty_line_symbol": " ",
            "line_fill_symbol": "═"
        },
        3: {
            "corner_symbols": (".", ".", "'", "'"),
            "horizontal_symbol": "-",
            "vertical_symbol": "|",
            "empty_line_symbol": " ",
            "line_fill_symbol": "-"
        },
        4: {
            "corner_symbols": ("#", "#", "#", "#"),
            "horizontal_symbol": "=",
            "vertical_symbol": "#",
            "empty_line_symbol": " ",
            "line_fill_symbol": "="
        },
        5: {
            "corner_symbols": ("┌", "┐", "└", "┘"),
            "horizontal_symbol": "─",
            "vertical_symbol": "│",
            "empty_line_symbol": " ",
            "line_fill_symbol": "─"
        },
        6: {
            "corner_symbols": (".", ".", ".", "."),
            "horizontal_symbol": ".",
            "vertical_symbol": ":",
            "empty_line_symbol": " ",
            "line_fill_symbol": "."
        }
    }

    # Validate style and set defaults
    if style not in styles:
        raise ValueError(f"Undefined style {style}. Valid styles are {list(styles.keys())}.")

    selected_style = styles[style]

    # Convert corner_symbols to a tuple of 4 values
    if isinstance(corner_symbols, str):
        corner_symbols = (corner_symbols,) * 4
    elif isinstance(corner_symbols, (list, tuple)) and len(corner_symbols) == 1:
        corner_symbols = tuple(corner_symbols * 4)
    elif isinstance(corner_symbols, (list, tuple)) and len(corner_symbols) == 2:
        corner_symbols = (corner_symbols[0], corner_symbols[1], corner_symbols[0], corner_symbols[1])
    elif corner_symbols is None:
        corner_symbols = selected_style["corner_symbols"]
    elif not isinstance(corner_symbols, (list, tuple)) or len(corner_symbols) != 4:
        raise ValueError("corner_symbols must be a string or a tuple/list of 1, 2, or 4 elements.")

    # Apply overrides or defaults
    horizontal_symbol = horizontal_symbol or selected_style["horizontal_symbol"]
    vertical_symbol = vertical_symbol or selected_style["vertical_symbol"]
    empty_line_symbol = empty_line_symbol or selected_style["empty_line_symbol"]
    line_fill_symbol = line_fill_symbol or selected_style["line_fill_symbol"]

    # Process lines: Replace "" with a placeholder, None with actual empty lines
    processed_lines = []
    max_content_width = 0
    for line in lines:
        if line == "":
            processed_lines.append("<LINE_FILL>")
        elif line is None:
            processed_lines.append(None)
        else:
            processed_line = str(line)
            processed_lines.append(processed_line)
            max_content_width = max(max_content_width, len(processed_line))

    # Adjust width for padding
    frame_width = max_content_width + padding * 2

    # Build the top border
    top_border = corner_symbols[0] + horizontal_symbol * frame_width + corner_symbols[1]

    # Process content lines
    framed_lines = [top_border]
    for line in processed_lines:
        if line is None:
            empty_line = vertical_symbol + empty_line_symbol * frame_width + vertical_symbol
            framed_lines.append(empty_line)
        elif line == "<LINE_FILL>":
            fill_line = vertical_symbol + line_fill_symbol * frame_width + vertical_symbol
            framed_lines.append(fill_line)
        else:
            line_content = line.center(frame_width)
            framed_line = vertical_symbol + line_content + vertical_symbol
            framed_lines.append(framed_line)

    # Build the bottom border
    bottom_border = corner_symbols[2] + horizontal_symbol * frame_width + corner_symbols[3]

    framed_lines.append(bottom_border)
    framed_lines.append("")  # Add an empty line at the end

    return "\n".join(framed_lines)



# descriptor for callable script
class CallableScript:
    """
    A descriptor that allows the method Interactions to be accessed both as a property and as a callable function.

    This class enables a method to behave like a property when accessed without parentheses,
    returning a function that can be called with default parameters. It also allows the method
    to be called directly with optional parameters, providing flexibility in usage.

    Attributes:
    -----------
    func : function
        The original function that is decorated, which will be used for both property access
        and direct calls.

    Methods:
    --------
    __get__(self, instance, owner)
        Returns a lambda function to call the original function with default parameters
        when accessed as a property.

    __call__(self, instance, printflag=False, verbosity=2)
        Allows the original function to be called directly with specified parameters.
    """
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        # When accessed as a property, return a lambda that calls the original function
        return lambda printflag=False, verbosity=2, verbose=None: self.func(instance, printflag=printflag, verbosity=verbosity, verbose=verbose)

    def __call__(self, instance, printflag=False, verbosity=2, verbose=None):
        # Allow calling the function directly with specified parameters
        return self.func(instance, printflag=printflag, verbosity=verbosity)




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
    scriptobject: A Class for Managing Script Objects in LAMMPS

    The `scriptobject` class is designed to represent individual objects in LAMMPS scripts, 
    such as beads, atoms, or other components. Each object is associated with a `forcefield` 
    instance that defines the physical interactions of the object, and the class supports 
    a variety of properties for detailed object definition. Additionally, `scriptobject` 
    instances can be grouped together and compared based on their properties, such as 
    `beadtype` and `name`.

    Key Features:
    -------------
    - **Forcefield Integration**: Each `scriptobject` is associated with a `forcefield` 
      instance, allowing for customized physical interactions. Forcefields can be passed 
      via the `USER` keyword for dynamic parameterization.
    - **Grouping**: Multiple `scriptobject` instances can be combined into a 
      `scriptobjectgroup` using the `+` operator, allowing for complex collections of objects.
    - **Object Comparison**: `scriptobject` instances can be compared and sorted based on 
      their `beadtype` and `name`, enabling efficient organization and manipulation of objects.
    - **Piping and Execution**: Supports the pipe (`|`) operator, allowing `scriptobject` 
      instances to be used in script pipelines alongside other script elements.

    Practical Use Cases:
    --------------------
    - **Object Definition in LAMMPS**: Use `scriptobject` to represent individual objects in 
      a simulation, including their properties and associated forcefields.
    - **Forcefield Parameterization**: Pass customized parameters to the forcefield via the 
      `USER` keyword to dynamically adjust the physical interactions.
    - **Grouping and Sorting**: Combine multiple objects into groups, or sort them based 
      on their properties (e.g., `beadtype`) for easier management in complex simulations.
    
    Methods:
    --------
    __init__(self, beadtype=1, name="undefined", fullname="", filename="", style="smd", 
             forcefield=rigidwall(), group=[], USER=scriptdata()):
        Initializes a new `scriptobject` with the specified properties, including `beadtype`, 
        `name`, `forcefield`, and optional `group`.

    __str__(self):
        Returns a string representation of the `scriptobject`, showing its `beadtype` and `name`.

    __add__(self, SO):
        Combines two `scriptobject` instances or a `scriptobject` with a `scriptobjectgroup`. 
        Raises an error if the two objects have the same `name` or if the second operand is not 
        a valid `scriptobject` or `scriptobjectgroup`.

    __or__(self, pipe):
        Overloads the pipe (`|`) operator to integrate the `scriptobject` into a pipeline.

    __eq__(self, SO):
        Compares two `scriptobject` instances, returning `True` if they have the same 
        `beadtype` and `name`.

    __ne__(self, SO):
        Returns `True` if the two `scriptobject` instances differ in either `beadtype` or `name`.

    __lt__(self, SO):
        Compares the `beadtype` of two `scriptobject` instances, returning `True` if the 
        left object's `beadtype` is less than the right object's.

    __gt__(self, SO):
        Compares the `beadtype` of two `scriptobject` instances, returning `True` if the 
        left object's `beadtype` is greater than the right object's.

    __le__(self, SO):
        Returns `True` if the `beadtype` of the left `scriptobject` is less than or equal to 
        the right `scriptobject`.

    __ge__(self, SO):
        Returns `True` if the `beadtype` of the left `scriptobject` is greater than or equal 
        to the right `scriptobject`.

    Attributes:
    -----------
    beadtype : int
        The type of bead or object, used for distinguishing between different types in the simulation.
    name : str
        A short name for the object, useful for quick identification.
    fullname : str
        A comprehensive name for the object. If not provided, defaults to the `name` with "object definition".
    filename : str
        The path to the file containing the input data for the object.
    style : str
        The style of the object (e.g., "smd" for smoothed dynamics).
    forcefield : forcefield
        The forcefield instance associated with the object, defining its physical interactions.
    group : list
        A list of other `scriptobject` instances that are grouped with this object.
    USER : scriptdata
        A collection of user-defined variables for customizing the forcefield or other properties.
    
    Original Content:
    -----------------
    The `scriptobject` class enables the definition of objects within LAMMPS scripts, providing:
    - **Beadtype and Naming**: Objects are distinguished by their `beadtype` and `name`, allowing 
      for comparison and sorting based on these properties.
    - **Forcefield Support**: Objects are linked to a forcefield instance, and user-defined forcefield 
      parameters can be passed through the `USER` keyword.
    - **Group Management**: Multiple objects can be grouped together using the `+` operator, forming 
      a `scriptobjectgroup`.
    - **Comparison Operators**: Objects can be compared based on their `beadtype` and `name`, using 
      standard comparison operators (`==`, `<`, `>`, etc.).
    - **Pipelines**: `scriptobject` instances can be integrated into pipelines, supporting the `|` 
      operator for use in sequential script execution.
    
    Example Usage:
    --------------
    ```
    from pizza.scriptobject import scriptobject, rigidwall, scriptdata
    
    # Define a script object with custom properties
    obj1 = scriptobject(beadtype=1, name="bead1", forcefield=rigidwall(USER=scriptdata(param1=10)))
    
    # Combine two objects into a group
    obj2 = scriptobject(beadtype=2, name="bead2")
    group = obj1 + obj2
    
    # Print object information
    print(obj1)
    print(group)
    ```
    
    The output will be:
    ```
    script object | type=1 | name=bead1
    scriptobjectgroup containing 2 objects
    ```
    
    OVERVIEW
    --------------

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
    scriptobjectgroup: A Class for Managing Groups of Script Objects in LAMMPS

    The `scriptobjectgroup` class is designed to represent a group of `scriptobject` instances, 
    such as beads or atoms in a simulation. This class allows users to group objects together 
    based on their properties (e.g., beadtype, name), and provides tools to generate scripts 
    that define interactions, groups, and forcefields for these objects in LAMMPS.

    Key Features:
    -------------
    - **Group Management**: Objects can be combined into a group, where each `beadtype` occurs 
      once. The class ensures that objects are uniquely identified by their `beadtype` and `name`.
    - **Dynamic Properties**: The group’s properties (e.g., `beadtype`, `name`, `groupname`) 
      are dynamically calculated, ensuring that the group reflects the current state of the objects.
    - **Script Generation**: Provides methods to generate scripts based on the group's objects, 
      including interaction forcefields and group definitions.
    - **Interaction Accumulation**: Automatically accumulates and updates all forcefield 
      interactions for the objects in the group.

    Practical Use Cases:
    --------------------
    - **LAMMPS Group Definitions**: Define groups of objects for use in LAMMPS simulations, 
      based on properties like `beadtype` and `groupname`.
    - **Forcefield Management**: Automatically manage and update interaction forcefields for 
      objects in the group.
    - **Script Generation**: Generate LAMMPS-compatible scripts that include group definitions, 
      input file handling, and interaction forcefields.

    Methods:
    --------
    __init__(self, *SOgroup):
        Initializes a new `scriptobjectgroup` with one or more `scriptobject` instances.

    __str__(self):
        Returns a string representation of the `scriptobjectgroup`, showing the number of objects 
        in the group and their `beadtypes`.

    __add__(self, SOgroup):
        Combines two `scriptobjectgroup` instances or a `scriptobject` with an existing group, 
        ensuring that `beadtype` values are unique.

    __or__(self, pipe):
        Overloads the pipe (`|`) operator to integrate the group into a pipeline.

    select(self, beadtype=None):
        Selects and returns a subset of the group based on the specified `beadtype`.

    script(self, printflag=False, verbosity=2, verbose=None):
        Generates a script based on the current collection of objects, including input file 
        handling, group definitions, and interaction forcefields.

    interactions(self, printflag=False, verbosity=2, verbose=None):
        Updates and accumulates all forcefields for the objects in the group.

    group_generator(self, name=None):
        Generates and returns a `group` object, based on the existing group structure.

    Properties:
    -----------
    - list : Converts the group into a sorted list of objects.
    - zip : Returns a sorted list of tuples containing `beadtype`, `name`, `group`, and `filename` 
      for each object.
    - n : Returns the number of objects in the group.
    - beadtype : Returns a list of the `beadtypes` for all objects in the group.
    - name : Returns a list of the `names` for all objects in the group.
    - groupname : Returns a list of all group names (synonyms).
    - filename : Returns a dictionary mapping filenames to the objects that use them.
    - str : Returns a string representation of the group's `beadtypes`.
    - min : Returns the minimum `beadtype` in the group.
    - max : Returns the maximum `beadtype` in the group.
    - minmax : Returns a tuple of the minimum and maximum `beadtypes` in the group.
    - forcefield : Returns the interaction forcefields for the group.

    Original Content:
    -----------------
    The `scriptobjectgroup` class enables the collection and management of multiple 
    `scriptobject` instances, providing the following functionalities:
    - **Group Creation**: Groups are automatically formed by combining individual objects 
      using the `+` operator. Each `beadtype` occurs only once in the group, and errors are 
      raised if an object with the same `name` or `beadtype` already exists.
    - **Dynamic Properties**: Properties such as `beadtype`, `name`, `groupname`, and `filename` 
      are dynamically calculated, reflecting the current state of the objects.
    - **Forcefield Handling**: Forcefields are automatically managed for the objects in the group, 
      including diagonal and off-diagonal terms for pair interactions.
    - **Script Generation**: Scripts are generated to define the interactions, groups, and 
      input file handling for LAMMPS.

    Example Usage:
    --------------
    ```
    from pizza.scriptobject import scriptobject, scriptobjectgroup, rigidwall, solidfood, water

    # Define some script objects
    b1 = scriptobject(name="bead 1", group=["A", "B", "C"], filename='myfile1', forcefield=rigidwall())
    b2 = scriptobject(name="bead 2", group=["B", "C"], filename='myfile1', forcefield=rigidwall())
    b3 = scriptobject(name="bead 3", group=["B", "D", "E"], forcefield=solidfood())
    b4 = scriptobject(name="bead 4", group="D", beadtype=1, filename="myfile2", forcefield=water())

    # Combine objects into a group
    collection = b1 + b2 + b3 + b4

    # Select a subset of objects and generate a script
    grp_typ1 = collection.select(1)
    grpB = collection.group.B
    script12 = collection.select([1, 2]).script()
    ```

    Output:
    ```
    script object group with 4 objects (1 2 3 4)
    script
    ```

    OVERVIEW:
    --------------


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
    _propertyasattribute = True

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
                dup.getattr(n).USER = self.getattr(n).USER
                dup.getattr(n).forcefield = self.getattr(n).forcefield
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

    @CallableScript
    def interactions(self, printflag=False, verbosity=2, verbose=None):
        """ update and accumulate all forcefields """
        verbosity = 0 if verbose is False else verbosity
        FF = []
        for b in self.beadtype:
            selection = deepduplicate(self.select(b)[0])
            selection.forcefield.beadtype = selection.beadtype
            selection.forcefield.userid = selection.name
            FF.append(selection.forcefield)
        # initialize interactions with pair_style
        TEMPLATE = "\n# ===== [ BEGIN FORCEFIELD SECTION ] "+"="*80 if verbosity>0 else ""
        TEMPLATE = FF[0].pair_style(verbose=verbosity>0)
        # pair diagonal terms
        for i in range(len(FF)):
            TEMPLATE += FF[i].pair_diagcoeff(verbose=verbosity>0)
        # pair off-diagonal terms
        for j in range(1,len(FF)):
            for i in range(0,j):
                TEMPLATE += FF[i].pair_offdiagcoeff(o=FF[j],verbose=verbosity>0)
        # end
        TEMPLATE += "\n# ===== [ END FORCEFIELD SECTION ] "+"="*82+"\n"  if verbosity>0 else ""
        return FF,TEMPLATE

    @property
    def forcefield(self):
        """ interaction forcefields """
        FF,_ = self.interactions
        return FF

    @CallableScript
    def script(self, printflag=False, verbosity=2, verbose=None):
        """
            Generate a script based on the current collection of script objects

            Parameters:
            -----------
            printflag : bool, optional, default=False
                If True, prints the generated script.
            verbosity (int, optional): Controls the level of detail in the generated script.
                - 0: Minimal output, no comments.
                - 1: Basic comments for run steps.
                - 2: Detailed comments with additional information.
                Default is 2
            
            Returns:
            --------
            script
                The generated script describing the interactions between script objects.
        """
        TEMPFILES = ""
        isfirst = True
        files_added = False
        verbosity = 0 if verbose is False else verbosity
        if self.filename:
            for fn, cfn in self.filename.items():
                if fn and cfn:
                    if not files_added:
                        files_added = True
                        TEMPFILES += "\n# ===== [ BEGIN INPUT FILES SECTION ] " + "=" * 79 + "\n" if verbosity>0 else ""
                    TEMPFILES += span(cfn, sep=", ", left="\n# load files for objects: ", right="\n") if verbosity>1 else ""
                    if isfirst:
                        isfirst = False
                        TEMPFILES += f"\tread_data {fn}\n"  # First file, no append
                    else:
                        TEMPFILES += f"\tread_data {fn} add append\n"  # Subsequent files, append
        # define groups
        TEMPGRP = "\n# ===== [ BEGIN GROUP SECTION ] "+"="*85 + "\n" if verbosity>0 else ""
        for g in self.group:
            TEMPGRP += f'\n\t#\tDefinition of group {g.groupid}:{g.groupidname}\n' if verbosity>1 else ""
            TEMPGRP += f'\t#\t={span(g.name,sep=", ")}\n' if verbosity>1 else ""
            TEMPGRP += f'\t#\tSimilar groups: {span(g.groupname,sep=", ")}\n' if verbosity>1 else ""
            TEMPGRP += f'\tgroup \t {g.groupidname} \ttype \t {span(g.beadtype)}\n'
        TEMPGRP += "\n# ===== [ END GROUP SECTION ] "+"="*87+"\n\n" if verbosity>0 else ""
        # define interactions
        _,TEMPFF = self.interactions(printflag=printflag, verbosity=verbosity)
        # chain strings into a script
        tscript = script(printflag=False,verbose=verbosity>1)
        tscript.name = "scriptobject script"        # name
        tscript.description = str(self)             # description
        tscript.userid = "scriptobject"             # user name
        tscript.TEMPLATE = TEMPFILES+TEMPGRP+TEMPFF
        if verbosity==0:
            tscript.TEMPLATE = remove_comments(tscript.TEMPLATE)
        if printflag:
            repr(tscript)
        return tscript
    
    def group_generator(self, name=None):
        """
        Generate and return a group object.
    
        This method creates a new `group` object, optionally with a specified name.
        If no name is provided, it generates a default name based on the current 
        instance's `name` attribute, formatted with the `span` function. The method
        then iterates through the existing groups in `self.group`, adding each group
        to the new `group` object based on its `groupidname` and `beadtype`.
    
        Parameters:
        -----------
        name : str, optional
            The name for the generated group object. If not provided, a default name
            is generated based on the current instance's `name`.
    
        Returns:
        --------
        group
            A newly created `group` object with criteria set based on the existing groups.
        """
        from pizza.group import group
    
        # Use the provided name or generate a default name using the span function
        G = group(name=name if name is not None else span(self.name, ",", "[", "]"))
        
        # Add criteria for each group in self.group
        for g in self.group:
            G.add_group_criteria(g.groupidname, type=g.beadtype)
        
        return G

# %% script core class
# note: please derive this class when you use it, do not alter it
class script:
    """
    script: A Core Class for Flexible LAMMPS Script Generation

    The `script` class provides a flexible framework for generating dynamic LAMMPS
    script sections. It supports various LAMMPS sections such as "GLOBAL", "INITIALIZE",
    "GEOMETRY", "INTERACTIONS", and more, while allowing users to define custom sections
    with variable definitions, templates, and dynamic evaluation of script content.

    Key Features:
    -------------
    - **Dynamic Script Generation**: Easily define and manage script sections,
      using templates and definitions to dynamically generate LAMMPS-compatible scripts.
    - **Script Concatenation**: Combine multiple script sections while managing
      variable precedence and ensuring that definitions propagate as expected.
    - **Flexible Variable Management**: Separate `DEFINITIONS` for static variables and
      `USER` for user-defined variables, with clear rules for inheritance and precedence.
    - **Operators for Advanced Script Handling**: Use `+`, `&`, `>>`, `|`, and `**` operators
      for script merging, static execution, right-shifting of definitions, and more.
    - **Pipeline Support**: Integrate scripts into pipelines, with full support for
      staged execution, variable inheritance, and reordering of script sections.

    Practical Use Cases:
    --------------------
    - **LAMMPS Automation**: Automate the generation of complex LAMMPS scripts by defining
      reusable script sections with variables and templates.
    - **Multi-Step Simulations**: Manage multi-step simulations by splitting large scripts
      into smaller, manageable sections and combining them as needed.
    - **Advanced Script Control**: Dynamically modify script behavior by overriding variables
      or using advanced operators to concatenate, pipe, or merge scripts.

    Methods:
    --------
    __init__(self, persistentfile=True, persistentfolder=None, printflag=False, verbose=False, **userdefinitions):
        Initializes a new `script` object, with optional user-defined variables
        passed as `userdefinitions`.

    do(self, printflag=None, verbose=None):
        Generates the LAMMPS script based on the current configuration, evaluating
        templates and definitions to produce the final output.

    script(self, idx=None, printflag=True, verbosity=2, verbose=None, forced=False):
        Generate the final LAMMPS script from the pipeline or a subset of the pipeline.

    add(self, s):
        Overloads the `+` operator to concatenate script objects, merging definitions
        and templates while maintaining variable precedence.

    and(self, s):
        Overloads the `&` operator for static execution, combining the generated scripts
        of two script objects without merging their definitions.

    __mul__(self, ntimes):
        Overloads the `*` operator to repeat the script `ntimes`, returning a new script
        object with repeated sections.

    __pow__(self, ntimes):
        Overloads the `**` operator to concatenate the script with itself `ntimes`,
        similar to the `&` operator, but repeated.

    __or__(self, pipe):
        Overloads the pipe (`|`) operator to integrate the script into a pipeline,
        returning a `pipescript` object.

    write(self, file, printflag=True, verbose=False):
        Writes the generated script to a file, including headers with metadata.

    tmpwrite(self):
        Writes the script to a temporary file, creating both a full version and a clean
        version without comments.

    printheader(txt, align="^", width=80, filler="~"):
        Static method to print formatted headers, useful for organizing output.

    __copy__(self):
        Creates a shallow copy of the script object.

    __deepcopy__(self, memo):
        Creates a deep copy of the script object, duplicating all internal variables.

    Additional Features:
    --------------------
    - **Customizable Templates**: Use string templates with variable placeholders
      (e.g., `${value}`) to dynamically generate script lines.
    - **Static and User-Defined Variables**: Manage global `DEFINITIONS` for static
      variables and `USER` variables for dynamic, user-defined settings.
    - **Advanced Operators**: Leverage a range of operators (`+`, `>>`, `|`, `&`) to
      manipulate script content, inherit definitions, and control variable precedence.
    - **Verbose Output**: Control verbosity to include detailed comments and debugging
      information in generated scripts.

    Original Content:
    -----------------
    The `script` class supports LAMMPS section generation and variable management with
    features such as:
    - **Dynamic Evaluation of Scripts**: Definitions and templates are evaluated at runtime,
      allowing for flexible and reusable scripts.
    - **Inheritance of Definitions**: Variable definitions can be inherited from previous
      sections, allowing for modular script construction.
    - **Precedence Rules for Variables**: When scripts are concatenated, definitions from
      the left take precedence, ensuring that the first defined values are preserved.
    - **Instance and Global Variables**: Instance variables are set via the `USER` object,
      while global variables (shared across instances) are managed in `DEFINITIONS`.
    - **Script Pipelines**: Scripts can be integrated into pipelines for sequential execution
      and dynamic variable propagation.
    - **Flexible Output Formats**: Lists are expanded into space-separated strings, while
      tuples are expanded with commas, making the output more readable.

    Example Usage:
    --------------
    ```
    from pizza.script import script, scriptdata
    
    class example_section(script):
        DEFINITIONS = scriptdata(
            X = 10,
            Y = 20,
            result = "${X} + ${Y}"
        )
        TEMPLATE = "${result} = ${X} + ${Y}"
    
    s1 = example_section()
    s1.USER.X = 5
    s1.do()
    ```

    The output for `s1.do()` will be:
    ```
    25 = 5 + 20
    ```

    With additional sections, scripts can be concatenated and executed as a single
    entity, with inheritance of variables and customizable behavior.


        --------------------------------------
           OVERVIEW ANDE DETAILED FEATURES
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
    
    # metadata
    metadata = get_metadata()               # retrieve all metadata
    
    type = "script"                         # type (class name)
    name = "empty script"                   # name
    description = "it is an empty script"   # description
    position = 0                            # 0 = root
    section = 0                             # section (0=undef)
    userid = "undefined"                    # user name
    version = metadata["version"]           # version
    license = metadata["license"]
    email = metadata["email"]               # email
    
    verbose = False                         # set it to True to force verbosity
    _contact = ("INRAE\SAYFOOD\olivier.vitrac@agroparistech.fr",
                "INRAE\SAYFOOD\william.jenkinson@agroparistech.fr",
                "INRAE\SAYFOOD\han.chen@inrae.fr")

    SECTIONS = ["NONE","GLOBAL","INITIALIZE","GEOMETRY","DISCRETIZATION",
                "BOUNDARY","INTERACTIONS","INTEGRATION","DUMP","STATUS","RUN"]

    # Main class variables
    # These definitions are for instances
    DEFINITIONS = scriptdata()
    TEMPLATE = """
        # empty LAMMPS script
    """

    # constructor
    def __init__(self,persistentfile=True,
                 persistentfolder = None,
                 printflag = False,
                 verbose = False,
                 **userdefinitions):
        """ constructor adding instance definitions stored in USER """
        if persistentfolder is None: persistentfolder = get_tmp_location()
        self.persistentfile = persistentfile
        self.persistentfolder = persistentfolder
        self.printflag = printflag # for internal operations
        self.verbose = verbose     # for internal operations
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
            self.DEFINITIONS.__repr__()
        else:
            print("too many definitions: ",self.DEFINITIONS)
        if self.verbose:
            self.printheader("USER",filler="-",align=">")
            self.USER.__repr__()
            self.printheader("TEMPLATE",filler="-",align=">")
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
    def do(self,printflag=None,verbose=None):
        """ 
        Generate the LAMMPS script based on the current configuration.
    
        This method generates a LAMMPS-compatible script from the templates and definitions
        stored in the `script` object. The generated script can be displayed, returned,
        and optionally include comments for debugging or clarity.
    
        Parameters:
        - printflag (bool, optional): If True, the generated script is printed to the console.
                                      Default is True.
        - verbose (bool, optional): If True, comments and additional information are included
                                    in the generated script. If False, comments are removed.
                                    Default is True.
    
        Returns:
        - str: The generated LAMMPS script.
    
        Method Behavior:
        - The method first collects all key-value pairs from `DEFINITIONS` and `USER` objects,
          which store the configuration data for the script.
        - Lists and tuples in the collected data are formatted into a readable string with proper
          separators (space for lists, comma for tuples) and prefixed with a '%' to indicate comments.
        - The generated command template is formatted and evaluated using the collected data.
        - If `verbose` is set to False, comments in the generated script are removed.
        - The script is then printed if `printflag` is True.
        - Finally, the formatted script is returned as a string.
    
        Example Usage:
        --------------
        >>> s = script()
        >>> s.do(printflag=True, verbose=True)
        units           si
        dimension       3
        boundary        f f f
        # Additional script commands...
        
        >>> s.do(printflag=False, verbose=False)
        'units si\ndimension 3\nboundary f f f\n# Additional script commands...'
    
        Notes:
        - Comments are indicated in the script with '%' or '#'.
        - The [position {self.position}:{self.userid}] marker is inserted for tracking
          script sections or modifications.
        """
        printflag = self.printflag if printflag is None else printflag
        verbose = self.verbose if verbose is None else verbose
        inputs = self.DEFINITIONS + self.USER
        for k in inputs.keys():
            if isinstance(inputs.getattr(k),list):
                inputs.setattr(k,"% "+span(inputs.getattr(k)))
            elif isinstance(inputs.getattr(k),tuple):
                inputs.setattr(k,"% "+span(inputs.getattr(k),sep=","))
        cmd = inputs.formateval(self.TEMPLATE)
        cmd = cmd.replace("[comment]",f"[position {self.position}:{self.userid}]")
        if not verbose: cmd=remove_comments(cmd)
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
        from pizza.dscript import dscript
        if isinstance(s,script):
            dup = duplicate(self)
            dup.DEFINITIONS = dup.DEFINITIONS + s.DEFINITIONS
            dup.USER = dup.USER + s.USER
            dup.TEMPLATE = "\n".join([dup.TEMPLATE,s.TEMPLATE])
            return dup
        elif isinstance(s,pipescript):
            return pipescript(self) | s
        elif isinstance(s,dscript):
            return self + s.script()
        raise TypeError(f"the second operand in + must a script object not {type(s)}")

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
            raise TypeError(f"the second operand in >> must a script object not {type(s)}")

    # override &
    def __and__(self,s):
        """ overload and operator """
        if isinstance(s,script):
            dup = duplicate(self)
            dup.TEMPLATE = "\n".join([self.do(printflag=False,verbose=False),s.do(printflag=False,verbose=False)])
            return dup
        raise TypeError(f"the second operand in & must a script object not {type(s)}")

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
        from pizza.dscript import dscript
        if isinstance(pipe, dscript):
            rightarg = pipe.pipescript(printflag=False,verbose=False)
        else:
            rightarg = pipe
        if isinstance(rightarg,(pipescript,script,scriptobject,scriptobjectgroup)):
            return pipescript(self) | rightarg
        else:
            raise ValueError("the argument in | must a pipescript, a scriptobject or a scriptobjectgroup not {type(s)}")


    def header(self, verbosity=None, style=2):
        """
        Generate a formatted header for the script file.

        Parameters:
            verbosity (bool, optional): If specified, overrides the instance's `verbose` setting.
                                        Defaults to the instance's `verbose`.
            style (int from 1 to 6, optional): ASCII style to frame the header (default=2)

        Returns:
            str: A formatted string representing the script's metadata and initialization details.
                 Returns an empty string if verbosity is False.

        The header includes:
            - Script version, license, and contact email.
            - User ID and the number of initialized definitions.
            - Current system user, hostname, and working directory.
            - Persistent filename and folder path.
            - Timestamp of the header generation.
        """
        verbosity = self.verbose if verbosity is None else verbosity
        if not verbosity:
            return ""

        # Prepare the header content
        lines = [
            f"PIZZA.SCRIPT FILE v{script.version} | License: {script.license} | Email: {script.email}",
            "",
            f"<{str(self)}>",
            f"Initialized with {len(self.USER)} definitions | Verbosity: {verbosity}",
            f"Persistent file: \"{self.persistentfile}\" | Folder: \"{self.persistentfolder}\"",
            "",
            f"Generated on: {getpass.getuser()}@{socket.gethostname()}:{os.getcwd()}",
            f"{datetime.datetime.now().strftime('%A, %B %d, %Y at %H:%M:%S')}",
        ]

        # Use the shared method to format the header
        return frame_header(lines,style=style)


    # write file
    def write(self, file, printflag=True, verbose=False, overwrite=False, style=2):
        """Write the script to a file.
        
        Parameters:
            - file (str): The file path where the script will be saved.
            - printflag (bool): Flag to enable/disable printing of details.
            - verbose (bool): Flag to enable/disable verbose mode.
            - overwrite (bool): Whether to overwrite the file if it already exists.
            - style (int, optional): 
                Defines the ASCII frame style for the header.
                Valid values are integers from 1 to 6, corresponding to predefined styles:
                    1. Basic box with `+`, `-`, and `|`
                    2. Double-line frame with `╔`, `═`, and `║`
                    3. Rounded corners with `.`, `'`, `-`, and `|`
                    4. Thick outer frame with `#`, `=`, and `#`
                    5. Box drawing characters with `┌`, `─`, and `│`
                    6. Minimalist dotted frame with `.`, `:`, and `.`
                Default is `2` (frame with rounded corners).
            
        Raises:
            FileExistsError: If the file already exists and overwrite is False.
        """
        if os.path.exists(file) and not overwrite:
            raise FileExistsError(f"The file '{file}' already exists. Use overwrite=True to overwrite it.")
        if os.path.exists(file) and overwrite and verbose:
            print(f"Warning: Overwriting the existing file '{file}'.")
        cmd = self.do(printflag=printflag, verbose=verbose)
        with open(file, "w") as f:
            print(self.header(verbosity=verbose,style=style), "\n", file=f)
            print(cmd, file=f)


    def tmpwrite(self, verbose=False, style=1):
        """
        Write the script to a temporary file and create optional persistent copies.
    
        Parameters:
            verbose (bool, optional): Controls verbosity during script generation. Defaults to False.
    
        The method:
            - Creates a temporary file for the script, with platform-specific behavior:
                - On Windows (`os.name == 'nt'`), the file is not automatically deleted.
                - On other systems, the file is temporary and deleted upon closure.
            - Writes a header and the script content into the temporary file.
            - Optionally creates a persistent copy in the `self.persistentfolder` directory:
                - `script.preview.<suffix>`: A persistent copy of the temporary file.
                - `script.preview.clean.<suffix>`: A clean copy with comments and empty lines removed.
            - Handles cleanup and exceptions gracefully to avoid leaving orphaned files.
            - style (int, optional): 
                Defines the ASCII frame style for the header.
                Valid values are integers from 1 to 6, corresponding to predefined styles:
                    1. Basic box with `+`, `-`, and `|`
                    2. Double-line frame with `╔`, `═`, and `║`
                    3. Rounded corners with `.`, `'`, `-`, and `|`
                    4. Thick outer frame with `#`, `=`, and `#`
                    5. Box drawing characters with `┌`, `─`, and `│`
                    6. Minimalist dotted frame with `.`, `:`, and `.`
                Default is `1` (basic box).
    
        Returns:
            TemporaryFile: The temporary file handle (non-Windows systems only).
            None: On Windows, the file is closed and not returned.
    
        Raises:
            Exception: If there is an error creating or writing to the temporary file.
        """
        try:
            # OS-specific temporary file behavior
            if os.name == 'nt':  # Windows
                ftmp = tempfile.NamedTemporaryFile(mode="w+b", prefix="script_", suffix=".txt", delete=False)
            else:  # Other platforms
                ftmp = tempfile.NamedTemporaryFile(mode="w+b", prefix="script_", suffix=".txt")
    
            # Generate header and content
            header = (
                f"# TEMPORARY PIZZA.SCRIPT FILE\n"
                f"# {'-' * 40}\n"
                f"{self.header(verbosity=verbose, style=style)}"
            )
            content = (
                header
                + "\n# This is a temporary file (it will be deleted automatically)\n\n"
                + self.do(printflag=False, verbose=verbose)
            )
    
            # Write content to the temporary file
            ftmp.write(BOM_UTF8 + content.encode('utf-8'))
            ftmp.seek(0)  # Reset file pointer to the beginning
    
        except Exception as e:
            # Handle errors gracefully
            ftmp.close()
            os.remove(ftmp.name)  # Clean up the temporary file
            raise Exception(f"Failed to write to or handle the temporary file: {e}") from None
    
        print("\nTemporary File Header:\n", header, "\n")
        print("A temporary file has been generated here:\n", ftmp.name)
    
        # Persistent copy creation
        if self.persistentfile:
            ftmpname = os.path.basename(ftmp.name)
            fcopyname = os.path.join(self.persistentfolder, f"script.preview.{ftmpname.rsplit('_', 1)[1]}")
            copyfile(ftmp.name, fcopyname)
            print("A persistent copy has been created here:\n", fcopyname)
    
            # Create a clean copy without empty lines or comments
            with open(ftmp.name, "r") as f:
                lines = f.readlines()
            bom_utf8_str = BOM_UTF8.decode("utf-8")
            clean_lines = [
                line for line in lines
                if line.strip() and not line.lstrip().startswith("#") and not line.startswith(bom_utf8_str)
            ]
            fcleanname = os.path.join(self.persistentfolder, f"script.preview.clean.{ftmpname.rsplit('_', 1)[1]}")
            with open(fcleanname, "w") as f:
                f.writelines(clean_lines)
            print("A clean copy has been created here:\n", fcleanname)
    
            # Handle file closure for Windows
            if os.name == 'nt':
                ftmp.close()
                return None
            else:
                return ftmp

            
    # Note that it was not the original intent to copy scripts
    def __copy__(self):
        """ copy method """
        cls = self.__class__
        copie = cls.__new__(cls)
        copie.__dict__.update(self.__dict__)
        return copie

    def __deepcopy__(self, memo):
        """ deep copy method """
        cls = self.__class__
        copie = cls.__new__(cls)
        memo[id(self)] = copie
        for k, v in self.__dict__.items():
            setattr(copie, k, deepduplicate(v, memo))
        return copie


# %% pipe script
class pipescript:
    """
    pipescript: A Class for Managing Script Pipelines

    The `pipescript` class stores scripts in a pipeline where multiple scripts,
    script objects, or script object groups can be combined and executed
    sequentially. Scripts in the pipeline are executed using the pipe (`|`) operator,
    allowing for dynamic control over execution order, script concatenation, and
    variable management.

    Key Features:
    -------------
    - **Pipeline Construction**: Create pipelines of scripts, combining multiple
      script objects, `script`, `scriptobject`, or `scriptobjectgroup` instances.
      The pipe operator (`|`) is overloaded to concatenate scripts.
    - **Sequential Execution**: Execute all scripts in the pipeline in the order
      they were added, with support for reordering, selective execution, and
      clearing of individual steps.
    - **User and Definition Spaces**: Manage local and global user-defined variables
      (`USER` space) and static definitions for each script in the pipeline.
      Global definitions apply to all scripts in the pipeline, while local variables
      apply to specific steps.
    - **Flexible Script Handling**: Indexing, slicing, reordering, and renaming
      scripts in the pipeline are supported. Scripts can be accessed, replaced,
      and modified like array elements.

    Practical Use Cases:
    --------------------
    - **LAMMPS Script Automation**: Automate the generation of multi-step simulation
      scripts for LAMMPS, combining different simulation setups into a single pipeline.
    - **Script Management**: Combine and manage multiple scripts, tracking user
      variables and ensuring that execution order can be adjusted easily.
    - **Advanced Script Execution**: Perform partial pipeline execution, reorder
      steps, or clear completed steps while maintaining the original pipeline structure.

    Methods:
    --------
    __init__(self, s=None):
        Initializes a new `pipescript` object, optionally starting with a script
        or script-like object (`script`, `scriptobject`, `scriptobjectgroup`).

    setUSER(self, idx, key, value):
        Set a user-defined variable (`USER`) for the script at the specified index.

    getUSER(self, idx, key):
        Get the value of a user-defined variable (`USER`) for the script at the
        specified index.

    clear(self, idx=None):
        Clear the execution status of scripts in the pipeline, allowing them to
        be executed again.

    do(self, idx=None, printflag=True, verbosity=2, verbose=None, forced=False):
        Execute the pipeline or a subset of the pipeline, generating a combined
        LAMMPS-compatible script.

    script(self, idx=None, printflag=True, verbosity=2, verbose=None, forced=False):
        Generate the final LAMMPS script from the pipeline or a subset of the pipeline.

    rename(self, name="", idx=None):
        Rename the scripts in the pipeline, assigning new names to specific
        indices or all scripts.

    write(self, file, printflag=True, verbosity=2, verbose=None):
        Write the generated script to a file.
        
    dscript(self, verbose=None, **USER)
        Convert the current pipescript into a dscript object

    Static Methods:
    ---------------
    join(liste):
        Combine a list of `script` and `pipescript` objects into a single pipeline.

    Additional Features:
    --------------------
    - **Indexing and Slicing**: Use array-like indexing (`p[0]`, `p[1:3]`) to access
      and manipulate scripts in the pipeline.
    - **Deep Copy Support**: The pipeline supports deep copying, preserving the
      entire pipeline structure and its scripts.
    - **Verbose and Print Options**: Control verbosity and printing behavior for
      generated scripts, allowing for detailed output or minimal script generation.

    Original Content:
    -----------------
    The `pipescript` class supports a variety of pipeline operations, including:
    - Sequential execution with `cmd = p.do()`.
    - Reordering pipelines with `p[[2, 0, 1]]`.
    - Deleting steps with `p[[0, 1]] = []`.
    - Accessing local and global user space variables via `p.USER[idx].var` and
      `p.scripts[idx].USER.var`.
    - Managing static definitions for each script in the pipeline.
    - Example usage:
      ```
      p = pipescript()
      p | i
      p = G | c | g | d | b | i | t | d | s | r
      p.rename(["G", "c", "g", "d", "b", "i", "t", "d", "s", "r"])
      cmd = p.do([0, 1, 4, 7])
      sp = p.script([0, 1, 4, 7])
      ```
    - Scripts in the pipeline are executed sequentially, and definitions propagate
      from left to right. The `USER` space and `DEFINITIONS` are managed separately
      for each script in the pipeline.

    OVERVIEW
    -----------------
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

            join joins a list (static method)
                p = pipescript.join([p1,p2,s3,s4])


            Pending: mechanism to store LAMMPS results (dump3) in the pipeline
    """

    def __init__(self,s=None, name=None):
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
            raise TypeError("The operand should be a pipescript")

    def __iadd__(self,s):
        """ overload += as pipe without copy """
        if isinstance(s,pipescript):
            return self | s      # + or | are synonyms
        else:
            raise TypeError("The operand should be a pipescript")

    def __mul__(self,ntimes):
        """ overload * as multiple pipes with copy """
        if isinstance(self,pipescript):
            res = deepduplicate(self)
            if ntimes>1:
                for n in range(1,ntimes): res += self
            return res
        else:
            raise TypeError("The operand should be a pipescript")


    def __or__(self, s):
        """ Overload | pipe operator in pipescript """
        leftarg = deepduplicate(self)  # Make a deep copy of the current object
        # Local import only when dscript type needs to be checked
        from pizza.dscript import dscript
        # Convert rightarg to pipescript if needed
        if isinstance(s, dscript):
            rightarg = s.pipescript(printflag=False,verbose=False)  # Convert the dscript object to a pipescript
            native = False
        elif isinstance(s,(script,scriptobject,scriptobjectgroup)):
            rightarg = pipescript(s)  # Convert the script-like object into a pipescript
            rightname = str(s)
            native = False
        elif isinstance(s,pipescript):
            rightarg = s
            native = True
        else:
            raise TypeError(f"The operand should be a pipescript, dscript, script, scriptobject, or scriptobjectgroup not {type(s)}")
        # Native piping
        if native:
            leftarg.listscript = leftarg.listscript + rightarg.listscript
            leftarg.listUSER = leftarg.listUSER + rightarg.listUSER
            leftarg.name = leftarg.name + rightarg.name
            for i in range(len(rightarg)): 
                rightarg.executed[i] = False
            leftarg.executed = leftarg.executed + rightarg.executed
            return leftarg
        # Piping for non-native objects (dscript or script-like objects)
        else:
            # Loop through all items in rightarg and concatenate them
            for i in range(rightarg.n):
                leftarg.listscript.append(rightarg.listscript[i])
                leftarg.listUSER.append(rightarg.listUSER[i])
                leftarg.name.append(rightarg.name[i])
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
        elif isinstance(idx,list):
            dup.listscript = picker(dup.listscript,idx)
            dup.listUSER = picker(dup.listUSER,idx)
            dup.name = picker(dup.name,idx)
            dup.executed = picker(dup.executed,idx)
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



    def do(self, idx=None, printflag=True, verbosity=2, verbose=None, forced=False):
        """
        Execute the pipeline or a part of the pipeline and generate the LAMMPS script.
    
        Parameters:
            idx (list, range, or int, optional): Specifies which steps of the pipeline to execute.
            printflag (bool, optional): Whether to print the script for each step. Default is True.
            verbosity (int, optional): Level of verbosity for the output.
            verbose (bool, optional): Override for verbosity. If False, sets verbosity to 0.
            forced (bool, optional): If True, forces the pipeline to regenerate all scripts.
    
        Returns:
            str: Combined LAMMPS script for the specified pipeline steps.
            
            Execute the pipeline or a part of the pipeline and generate the LAMMPS script.
        
            This method processes the pipeline of script objects, executing each step to generate
            a combined LAMMPS-compatible script. The execution can be done for the entire pipeline 
            or for a specified range of indices. The generated script can include comments and 
            metadata based on the verbosity level.       
            
        
        Method Workflow:
            - The method first checks if there are any script objects in the pipeline.
              If the pipeline is empty, it returns a message indicating that there is nothing to execute.
            - It determines the start and stop indices for the range of steps to execute.
              If idx is not provided, it defaults to executing all steps from the last executed position.
            - If a specific index or list of indices is provided, it executes only those steps.
            - The pipeline steps are executed in order, combining the scripts using the 
              >> operator for sequential execution.
            - The generated script includes comments indicating the current run step and pipeline range,
              based on the specified verbosity level.
            - The final combined script is returned as a string.
        
        Example Usage:
        --------------
            >>> p = pipescript()
            >>> # Execute the entire pipeline
            >>> full_script = p.do()
            >>> # Execute steps 0 and 2 only
            >>> partial_script = p.do([0, 2])
            >>> # Execute step 1 with minimal verbosity
            >>> minimal_script = p.do(idx=1, verbosity=0)
        
            Notes:
            - The method uses modular arithmetic to handle index wrapping, allowing 
              for cyclic execution of pipeline steps.
            - If the pipeline is empty, the method returns the string "# empty pipe - nothing to do".
            - The globalscript is initialized or updated with each step's script, 
              and the USER definitions are accumulated across the steps.
            - The command string self.cmd is updated with the generated script for 
              each step in the specified range.
        
            Raises:
            - None: The method does not raise exceptions directly, but an empty pipeline will 
                    result in the return of "# empty pipe - nothing to do".
        """
        verbosity = 0 if verbose is False else verbosity
        if len(self) == 0:
            return "# empty pipe - nothing to do"
            
        # Check if not all steps are executed or if there are gaps
        not_all_executed = not all(self.executed[:self.nrun])  # Check up to the last executed step

        # Determine pipeline range
        total_steps = len(self)
        if self.globalscript is None or forced or not_all_executed:
            start = 0
            self.cmd = ""
        else:
            start = self.nrun
            self.cmd = self.cmd.rstrip("\n") + "\n\n"
    
        if idx is None:
            idx = range(start, total_steps)
        if isinstance(idx, int):
            idx = [idx]
        if isinstance(idx, range):
            idx = list(idx)
    
        idx = [i % total_steps for i in idx]
        start, stop = min(idx), max(idx)
    
        # Prevent re-executing already completed steps
        if not forced:
            idx = [step for step in idx if not self.executed[step]]
    
        # Execute pipeline steps
        for step in idx:
            step_wrapped = step % total_steps
    
            # Combine scripts
            if step_wrapped == 0:
                self.globalscript = self.listscript[step_wrapped]
            else:
                self.globalscript = self.globalscript >> self.listscript[step_wrapped]
    
            # Step label
            step_name = f"<{self.name[step]}>"
            step_label = f"# [{step+1} of {total_steps} from {start}:{stop}] {step_name}"
    
            # Get script content for the step
            step_output = self.globalscript.do(printflag=printflag, verbose=verbosity > 1)
    
            # Add comments and content
            if step_output.strip():
                self.cmd += f"{step_label}\n{step_output.strip()}\n\n"
            elif verbosity > 0:
                self.cmd += f"{step_label} :: no content\n\n"
    
            # Update USER definitions
            self.globalscript.USER += self.listUSER[step]
            self.executed[step] = True
    
        # Clean up and finalize script
        self.cmd = self.cmd.replace("\\n", "\n").strip()  # Remove literal \\n and extra spaces
        self.cmd += "\n"  # Ensure trailing newline
        return remove_comments(self.cmd) if verbosity == 0 else self.cmd


    def do_legacy(self, idx=None, printflag=True, verbosity=2, verbose=None, forced=False):
        """
        Execute the pipeline or a part of the pipeline and generate the LAMMPS script.
    
        This method processes the pipeline of script objects, executing each step to generate
        a combined LAMMPS-compatible script. The execution can be done for the entire pipeline 
        or for a specified range of indices. The generated script can include comments and 
        metadata based on the verbosity level.
    
        Parameters:
        - idx (list, range, or int, optional): Specifies which steps of the pipeline to execute.
                                               If None, all steps from the current position to 
                                               the end are executed. A list of indices can be
                                               provided to execute specific steps, or a single
                                               integer can be passed to execute a specific step.
                                               Default is None.
        - printflag (bool, optional): If True, the generated script for each step is printed 
                                      to the console. Default is True.
        - verbosity (int, optional): Controls the level of detail in the generated script.
                                     - 0: Minimal output, no comments.
                                     - 1: Basic comments for run steps.
                                     - 2: Detailed comments with additional information.
                                     Default is 2.
        - forced (bool, optional): If True, all scripts are regenerated 
        
        Returns:
        - str: The combined LAMMPS script generated from the specified steps of the pipeline.
    
        Method Workflow:
        - The method first checks if there are any script objects in the pipeline.
          If the pipeline is empty, it returns a message indicating that there is nothing to execute.
        - It determines the start and stop indices for the range of steps to execute.
          If idx is not provided, it defaults to executing all steps from the last executed position.
        - If a specific index or list of indices is provided, it executes only those steps.
        - The pipeline steps are executed in order, combining the scripts using the 
          >> operator for sequential execution.
        - The generated script includes comments indicating the current run step and pipeline range,
          based on the specified verbosity level.
        - The final combined script is returned as a string.
    
        Example Usage:
        --------------
        >>> p = pipescript()
        >>> # Execute the entire pipeline
        >>> full_script = p.do()
        >>> # Execute steps 0 and 2 only
        >>> partial_script = p.do([0, 2])
        >>> # Execute step 1 with minimal verbosity
        >>> minimal_script = p.do(idx=1, verbosity=0)
    
        Notes:
        - The method uses modular arithmetic to handle index wrapping, allowing 
          for cyclic execution of pipeline steps.
        - If the pipeline is empty, the method returns the string "# empty pipe - nothing to do".
        - The globalscript is initialized or updated with each step's script, 
          and the USER definitions are accumulated across the steps.
        - The command string self.cmd is updated with the generated script for 
          each step in the specified range.
    
        Raises:
        - None: The method does not raise exceptions directly, but an empty pipeline will 
                result in the return of "# empty pipe - nothing to do".
        """

        verbosity = 0 if verbose is False else verbosity
        if len(self)>0:
            # ranges
            ntot = len(self)
            stop = ntot-1
            if (self.globalscript == None) or (self.globalscript == []) or not self.executed[0] or forced:
                start = 0
                self.cmd = ""
            else:
                start = self.nrun
            if start>stop: return self.cmd
            if idx is None: idx = range(start,stop+1)
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
                if verbosity>0:
                    self.cmd += "\n\n#\t --- run step [%d/%d] --- [%s]  %20s\n" % \
                            (j,ntot-1,name.center(50,"="),"pipeline [%d]-->[%d]" %(start,stop))
                else:
                    self.cmd +="\n"
                self.globalscript.USER = self.globalscript.USER + self.listUSER[j]
                self.cmd += self.globalscript.do(printflag=printflag,verbose=verbosity>1)
                self.executed[i] = True
            self.cmd = self.cmd.replace("\\n", "\n") # remove literal \\n if any (dscript.save add \\n)
            return remove_comments(self.cmd) if verbosity==0 else self.cmd
        else:
            return "# empty pipe - nothing to do"


    def script(self,idx=None, printflag=True, verbosity=2, verbose=None, forced=False, style=4):
        """
            script the pipeline or parts of the pipeline
                s = p.script()
                s = p.script([0,2])
                
        Parameters:
        - idx (list, range, or int, optional): Specifies which steps of the pipeline to execute.
                                               If None, all steps from the current position to 
                                               the end are executed. A list of indices can be
                                               provided to execute specific steps, or a single
                                               integer can be passed to execute a specific step.
                                               Default is None.
        - printflag (bool, optional): If True, the generated script for each step is printed 
                                      to the console. Default is True.
        - verbosity (int, optional): Controls the level of detail in the generated script.
                                     - 0: Minimal output, no comments.
                                     - 1: Basic comments for run steps.
                                     - 2: Detailed comments with additional information.
                                     Default is 2.
        - forced (bool, optional): If True, all scripts are regenerated 
        - style (int, optional): 
            Defines the ASCII frame style for the header.
            Valid values are integers from 1 to 6, corresponding to predefined styles:
                1. Basic box with `+`, `-`, and `|`
                2. Double-line frame with `╔`, `═`, and `║`
                3. Rounded corners with `.`, `'`, `-`, and `|`
                4. Thick outer frame with `#`, `=`, and `#`
                5. Box drawing characters with `┌`, `─`, and `│`
                6. Minimalist dotted frame with `.`, `:`, and `.`
            Default is `4` (thick outer frame).
        
        """
        verbosity=0 if verbose is False else verbosity
        s = script(printflag=printflag, verbose=verbosity>0)
        s.name = "pipescript"
        s.description = "pipeline with %d scripts" % len(self)
        if len(self)>1:
            s.userid = self.name[0]+"->"+self.name[-1]
        elif len(self)==1:
            s.userid = self.name[0]
        else:
            s.userid = "empty pipeline"
        s.TEMPLATE = self.header(verbosity=verbosity, style=style) + "\n" +\
            self.do(idx, printflag=printflag, verbosity=verbosity, verbose=verbose, forced=forced)
        s.DEFINITIONS = duplicate(self.globalscript.DEFINITIONS)
        s.USER = duplicate(self.globalscript.USER)
        return s

    @staticmethod
    def join(liste):
        """
            join a combination scripts and pipescripts within a pipescript
                p = pipescript.join([s1,s2,p3,p4,p5...])
        """
        if not isinstance(liste,list):
            raise ValueError("the argument should be a list")
        ok = True
        for i in range(len(liste)):
            ok = ok and isinstance(liste[i],(script,pipescript))
            if not ok:
                raise ValueError(f"the entry [{i}] should be a script or pipescript")
        if len(liste)<1:
            return liste
        out = liste[0]
        for i in range(1,len(liste)):
            out = out | liste[i]
        return out
    
    # Note that it was not the original intent to copy pipescripts
    def __copy__(self):
        """ copy method """
        cls = self.__class__
        copie = cls.__new__(cls)
        copie.__dict__.update(self.__dict__)
        return copie

    def __deepcopy__(self, memo):
        """ deep copy method """
        cls = self.__class__
        copie = cls.__new__(cls)
        memo[id(self)] = copie
        for k, v in self.__dict__.items():
            setattr(copie, k, deepduplicate(v, memo))
        return copie 

    # write file
    def write(self, file, printflag=True, verbosity=2, verbose=None, overwrite=False):
       """
       Write the combined script to a file.
   
       Parameters:
           file (str): The file path where the script will be saved.
           printflag (bool): Flag to enable/disable printing of details.
           verbosity (int): Level of verbosity for the script generation.
           verbose (bool or None): If True, enables verbose mode; if None, defaults to the instance's verbosity.
           overwrite (bool): Whether to overwrite the file if it already exists. Default is False.
   
       Raises:
           FileExistsError: If the file already exists and overwrite is False.
   
       Notes:
           - This method combines the individual scripts within the `pipescript` object
             and saves the resulting script to the specified file.
           - If `overwrite` is False and the file exists, an error is raised.
           - If `verbose` is True and the file is overwritten, a warning is displayed.
       """
       # Generate the combined script
       myscript = self.script(printflag=printflag, verbosity=verbosity, verbose=verbose, forced=True)
   
       # Call the script's write method with the overwrite parameter
       myscript.write(file, printflag=printflag, verbose=verbose, overwrite=overwrite)

        
    def dscript(self, name=None, verbose=None, **USER):
        """
        Convert the current pipescript object to a dscript object.
        
        This method merges the STATIC, GLOBAL, and LOCAL variable spaces from each step
        in the pipescript into a single dynamic script per step in the dscript.
        Each step in the pipescript is transformed into a dynamic script in the dscript,
        where variable spaces are combined using the following order:
        
        1. STATIC: Definitions specific to each script in the pipescript.
        2. GLOBAL: User variables shared across steps from a specific point onwards.
        3. LOCAL: User variables for each individual step.
        
        Parameters:
        -----------
        verbose : bool, optional
            Controls verbosity of the dynamic scripts in the resulting dscript object.
            If None, the verbosity setting of the pipescript will be used.
        
        **USER : scriptobjectdata(), optional
            Additional user-defined variables that can override existing static variables
            in the dscript object or be added to it.
        
        Returns:
        --------
        outd : dscript
            A dscript object that contains all steps of the pipescript as dynamic scripts.
            Each step from the pipescript is added as a dynamic script with the same content
            and combined variable spaces.
        """
        # Local imports
        from pizza.dscript import dscript, ScriptTemplate, lambdaScriptdata
    
        # Adjust name
        if name is None:
            if isinstance(self.name, str):
                name = self.name
            elif isinstance(self.name, list):
                name = (
                    self.name[0] if len(self.name) == 1 else self.name[0] + "..." + self.name[-1]
                )
    
        # Create the dscript container with the pipescript name as the userid
        outd = dscript(userid=name, verbose=self.verbose, **USER)
    
        # Initialize static merged definitions
        staticmerged_definitions = lambdaScriptdata()
    
        # Loop over each step in the pipescript
        for i, script in enumerate(self.listscript):
            # Merge STATIC, GLOBAL, and LOCAL variables for the current step
            static_vars = script.DEFINITIONS
            global_vars = self.scripts[i].USER
            local_vars = self.USER[i]
    
            # Copy all static variables to local_static_updates and remove matching variables from staticmerged_definitions
            local_static_updates = lambdaScriptdata(**static_vars)
            for var, value in static_vars.items():
                if var in staticmerged_definitions and getattr(staticmerged_definitions, var) == value:
                    delattr(local_static_updates, var)
    
            # Accumulate unique static variables into staticmerged_definitions
            staticmerged_definitions.update(**static_vars) # += static_vars
    
            # Merge global and local variables for dynamic definitions
            merged_definitions = global_vars + local_vars
    
            # Create the dynamic script for this step using the method in dscript
            key_name = i  # Use the index 'i' as the key in TEMPLATE
            content = script.TEMPLATE
    
            # Use the helper method in dscript to add this dynamic script
            outd.add_dynamic_script(
                key=key_name,
                content=content,
                definitions = local_static_updates + merged_definitions,
                verbose=self.verbose if verbose is None else verbose,
                userid=self.name[i]
            )
    
            # Set eval=True only if variables are detected in the template
            if outd.TEMPLATE[key_name].detect_variables():
                outd.TEMPLATE[key_name].eval = True
    
        # Assign the accumulated static merged definitions along with USER variables to outd.DEFINITIONS
        outd.DEFINITIONS = staticmerged_definitions + lambdaScriptdata(**USER)
    
        return outd


    def header(self, verbosity=None, style=4):
        """
        Generate a formatted header for the pipescript file.

        Parameters:
            verbosity (bool, optional): If specified, overrides the instance's `verbose` setting.
                                        Defaults to the instance's `verbose`.
            style (int from 1 to 6, optional): ASCII style to frame the header (default=4)

        Returns:
            str: A formatted string representing the pipescript object.
                 Returns an empty string if verbosity is False.

        The header includes:
            - Total number of scripts in the pipeline.
            - The verbosity setting.
            - The range of scripts from the first to the last script.
            - All enclosed within an ASCII frame that adjusts to the content.
        """
        verbosity = self.verbose if verbosity is None else verbosity
        if not verbosity:
            return ""

        # Prepare the header content
        lines = [
            f"PIPESCRIPT with {self.n} scripts | Verbosity: {verbosity}",
            "",
            f"From: <{str(self.scripts[0])}> To: <{str(self.scripts[-1])}>",
        ]

        # Use the shared method to format the header
        return frame_header(lines,style=style)



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

    # example for debugging
    # from pizza.region import region
    # R = region(name="my region")
    # R.ellipsoid(0,0,0,1,1,1,name="E2",side="out",move=["left","${up}*3",None],up=0.1)
    # R.E2.VARIABLES.left = '"swiggle(%s,%s,%s)"%(${a},${b},${c})'
    # R.E2.VARIABLES.a="${b}-5"
    # R.E2.VARIABLES.b=5
    # R.E2.VARIABLES.c=100
    # code2 = R.E2.do()
    # p = R.E2.script
    # code = p.do(0)

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
