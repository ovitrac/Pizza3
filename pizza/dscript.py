#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================================================
PIZZA.DSCRIPT Module Documentation
================================================================================

The **PIZZA.DSCRIPT** module is a versatile tool for dynamically generating and managing 
**pizza.scripts**, especially in conjunction with **LAMMPS** (Large-scale Atomic/Molecular 
Massively Parallel Simulator). This module provides powerful features to create complex, 
parameterized scripts, manage multiple sections, and flexibly concatenate scripts to form 
pipelines. It offers advanced control over script execution and generation.

Overview:
---------
- **pizza.script**: Use this to define reusable codelets or scriptlets stored in maintainable libraries.
- **pizza.dscript**: Use this to dynamically generate codelets or scriptlets directly in your code,
   allowing for flexible, runtime script generation.

The output of `pizza.dscript.script()` is a complete script instance, similar to a standard pizza.script. 
These scripts can be managed like any pizza.script, allowing you to combine them using the `+` or `|` 
operators and integrate them into **pizza.pipescripts** for building complex, multi-step workflows.

Key Features:
-------------
1. **Dynamic Script Generation**: 
   - `pizza.dscript` allows for the generation of scripts dynamically within your code. This means that codelets 
     and scriptlets can be constructed at runtime, offering flexibility in handling complex scenarios.
   
2. **Combining Scripts**: 
   - The generated scripts can be combined using operators like `+` or `|`, enabling you to merge multiple 
     script sections seamlessly. This is especially useful for creating modular scripts that can be 
     reused across different contexts or experiments.

3. **Saving and Loading Scripts**: 
   - `pizza.dscript.save()` and `pizza.dscript.load()` enable you to save and load complex scripts as text templates, 
     independent of both Python and LAMMPS. This functionality allows for the deployment of sophisticated scripts 
     without requiring the full script class libraries (commonly referred to as "workshops" in Pizza3).

4. **Leveraging AI for Rapid Template Generation**: 
   - You can even leverage Large Language Models (LLMs) to generate templates quickly. This feature allows for 
     automation and faster script generation, particularly useful for deploying templated workflows or codelets.

5. **Non-linear Execution**: 
   - It's important to note that **pizza.scripts** and **pizza.dscripts** are not directly equivalent to LAMMPS code.
     They can be executed statically and non-linearly, without needing LAMMPS to be involved. This makes the 
     framework particularly useful when managing large LAMMPS simulations that span multiple submodules.

Applications:
-------------
The **PIZZA.DSCRIPT** module is particularly useful when you need to:
- **Dynamically create and manage LAMMPS script sections**.
- **Merge, manipulate, and execute multiple script sections** with predefined or user-defined variables.
- **Generate scripts with conditional sections and custom execution logic**, enabling the handling of complex simulations 
  and workflows.

The modular nature of `pizza.dscript` makes it well-suited for scenarios where you need to reuse various submodules of 
LAMMPS code or mix them with pure Python logic for more advanced control.

Key Classes:
------------
- **`lambdaScriptdata`**: Holds parameters and definitions for script execution. This class encapsulates the data and 
  logic needed for the dynamic generation of script elements.
  
- **`lambdaScript`**: Wraps a `dscript` object to generate a `pizza.script instance` from its contents. This class 
  is essential for converting dynamically generated `dscript` objects into reusable, executable script instances.

- **`dscript`**: Manages and stores multiple script lines/items as `ScriptTemplate` objects, supporting dynamic execution 
  and the concatenation of script sections. The `dscript` class allows for flexible script construction and execution, 
  making it a core component for generating dynamic LAMMPS scripts.
  
Notes:
------
- **Script Composition**: Generated scripts can span several submodules, allowing for the reuse of script components 
  in different contexts. This feature enables a modular approach to script generation.
- **Execution Flexibility**: Since `pizza.dscript` scripts are not bound to LAMMPS directly, they can be executed 
  independently, making them highly flexible for preprocessing, debugging, or running custom logic within a 
  LAMMPS-related workflow.

Important Distinction between **PIZZA.DSCRIPT** and **PIZZA.SCRIPT**: (with possible evolution in the future)
---------------------------------------------------------------------
- **PIZZA.DSCRIPT** stores the DEFINITIONS in lambdaScriptdata objects based on pizza.private.struct.paramauto
  The practical consequence is that all variables should be within {} such as ${variable}.
  The definitions will be redordered to authorize execution
- **PIZZA.SCRIPT** stores the DEFINITIONS in Scriptdata objects based on pizza.private.struct.param
  The variables can be $myvar or ${myvar}. The definition order is important.
   

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


Chat GPT teaching instructions:
Copy and paste these instructions to teach chatGPT how to convert in LAMMPS code in pizza.dscript()
-----------------------------[ start here ]--------------------------------------------------
# DSCRIPT SAVE FILE Format Instructions:
Each DSCRIPT file begins with the line `# DSCRIPT SAVE FILE`. The file is divided into sections: Global Parameters, Definitions, Template, and Attributes.
1. Global Parameters Section: Enclosed in `{}` and contains key-value pairs where values can be integers, floats, strings, booleans, or lists. Example:
```
# GLOBAL PARAMETERS
{
    SECTIONS = ['SECTION1', 'SECTION2'],
    section = 0,
    position = 0,
    role = "dscript instance",
    description = "A description",
    userid = "dscript",
    version = 0.1,
    verbose = False
}
```
2. Definitions Section: Defines variables as key-value pairs, which can reference other variables using `${}`. Example:
```
# DEFINITIONS (number of definitions=X)
var1 = value1
var2 = "${var1}"
```
3. Template Section: Contains key-value pairs for blocks of script content. Single-line content is written as `key: value`. Multi-line content is enclosed in square brackets `[]`. Example:
```
# TEMPLATE (number of lines=X)
block1: command using ${var1}
block2: [
    multi-line command 1
    multi-line command 2
]
```
4. Attributes Section: Optional attributes are attached to each block as key-value pairs inside curly braces `{}`. Example:
```
# ATTRIBUTES (number of lines with explicit attributes=X)
block1: {facultative=True, eval=True}
```
Definitions can be dynamically substituted into the templates using `${}` notation, and the parser should handle both single-line and multi-line templates.
```
-----------------------------[ end here ]--------------------------------------------------



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
    - Create a script template with multiple lines/items, each identified by a unique key.
    - Add conditions to script lines/items to control their inclusion based on the state of variables.
    - Overwrite `DEFINITIONS` at runtime to customize the script's behavior.
    - Generate and execute the script using the `do()` method.

Key Classes Used:
-----------------
    - `dscript`: Manages multiple script lines and their dynamic execution.
    - `lamdaScript`: Wraps a `dscript` object to generate a script instance from its contents.

Practical Steps:
----------------
    1. Initialize a `dscript` object and define global variables (DEFINITIONS).
    2. Create script lines/items using keys to identify each line.
    3. Apply conditions to script lines/items to control their execution.
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
    
    # Save your script
    R.save("myscript.txt")
    
    # Load again your script
    Rcopy = dsave.load("myscript.txt")
    
More Compact Example:
---------------------
    # Initialization
    R2 = dscript(name="ProductionExample2")
    # Define global variables (DEFINITIONS) for the script
    R2.DEFINITIONS.dimension = 3
    R2.DEFINITIONS.units = "$si"
    R2.DEFINITIONS.boundary = ["sm", "sm", "sm"]
    R2.DEFINITIONS.atom_modify = ["map", "array"]
    R2.DEFINITIONS.comm_modify = ["vel", "yes"]
    R2.DEFINITIONS.neigh_modify = ["every", 10, "delay", 0, "check", "yes"]
    R2.DEFINITIONS.newton = "$off"
    R2.DEFINITIONS.atom_style = "$smd"
    # Define the script template with a multiple line syntax
    R2["code"] = "" "        
        % ${comment}
        dimension    ${dimension}
        units        ${units}
        boundary     ${boundary}
        atom_style   ${atom_style}
        atom_modify  ${atom_modify}
        comm_modify  ${comm_modify}
        neigh_modify ${neigh_modify}
        newton       ${newton}
    "" "    
    # Generate a script instance, overwriting the 'units' variable and adding a comment
    sR2 = R2.script(comment="$my first compact dscript")
    ssR2 = sR2.do()    
    # Print the generated script
    print(ssR2)

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


Load and Save features:
-----------------------
use dscript.load() and dscript.save() methods


DSCRIPT SAVE FILE Syntax:
--------------------------

A DSCRIPT SAVE FILE is a text-based representation of script instances that are dynamically loaded or saved. It consists of key sections that define global parameters, variables (definitions), script templates, and attributes. The file format is structured and flexible, allowing both minimal and extended configurations depending on the level of detail required.

### Minimal DSCRIPT File
A minimal DSCRIPT SAVE FILE includes the template section, which defines the script's core structure. The template assigns content to variables, which can then be dynamically evaluated and modified during script execution.

Example of a minimal DSCRIPT SAVE FILE:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DSCRIPT SAVE FILE

0: % ${comment}
dim: dimension    ${dimension}
unit: units        ${units}
bound: boundary     ${boundary}
astyle: atom_style   ${atom_style}
amod: atom_modify  ${atom_modify}
cmod: comm_modify  ${comm_modify}
nmod: neigh_modify ${neigh_modify}
newton: newton       ${newton}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Example of a compact DSCRIPT SAVE FILE:
    Note the position of the []
    Use % to keep comments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DSCRIPT SAVE FILE

mytemplate: [
    % ${comment}
    dimension    ${dimension}
    units        ${units}
    boundary     ${boundary}
    atom_style   ${atom_style}
    atom_modify  ${atom_modify}
    comm_modify  ${comm_modify}
    neigh_modify ${neigh_modify}
    newton       ${newton}
    ]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Required header**: The file must start with the line `# DSCRIPT SAVE FILE`. This is mandatory and serves to authenticate the file as a valid DSCRIPT file.
- **Template section**: Each line contains a variable key followed by the content. Variables (e.g., `${dimension}`) are placeholders that will be replaced during script execution. The format is `key: content`, where `key` is a unique identifier and `content` represents the script logic.

### Extended DSCRIPT File
An extended DSCRIPT file includes additional sections such as global parameters, definitions, templates, and attributes. These provide more control and flexibility over script behavior and configuration.

    Example of an extended DSCRIPT SAVE FILE:
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # DSCRIPT SAVE FILE
    # generated on 20XX-XX-XX on user@localhost
    
    #	name = "ProductionExample"
    #	path = "/your/path/ProductionExample.txt"
    
    # GLOBAL PARAMETERS
    {
        SECTIONS = ['DYNAMIC'],
        section = 0,
        position = 0,
        role = 'dscript instance',
        description = 'dynamic script',
        userid = 'dscript',
        version = 0.1,
        verbose = False
    }
    
    # DEFINITIONS (number of definitions=9)
    dimension=3
    units=$si
    boundary=['sm', 'sm', 'sm']
    atom_style=""
    atom_modify=['map', 'array']
    comm_modify=['vel', 'yes']
    neigh_modify=['every', 10, 'delay', 0, 'check', 'yes']
    newton=$off
    comment=${comment}
    
    # TEMPLATE (number of lines=9)
    0: % ${comment}
    dim: dimension    ${dimension}
    unit: units        ${units}
    bound: boundary     ${boundary}
    astyle: atom_style   ${atom_style}
    amod: atom_modify  ${atom_modify}
    cmod: comm_modify  ${comm_modify}
    nmod: neigh_modify ${neigh_modify}
    newton: newton       ${newton}
    
    # ATTRIBUTES (number of lines with explicit attributes=9)
    0:{facultative=False, eval=False, readonly=False, condition=None, condeval=False, detectvar=True}
    dim:{facultative=False, eval=False, readonly=False, condition=None, condeval=False, detectvar=True}
    unit:{facultative=False, eval=False, readonly=False, condition=None, condeval=False, detectvar=True}
    bound:{facultative=False, eval=False, readonly=False, condition=None, condeval=False, detectvar=True}
    astyle:{facultative=False, eval=False, readonly=False, condition='${atom_style}', condeval=False, detectvar=True}
    amod:{facultative=False, eval=False, readonly=False, condition=None, condeval=False, detectvar=True}
    cmod:{facultative=False, eval=False, readonly=False, condition=None, condeval=False, detectvar=True}
    nmod:{facultative=False, eval=False, readonly=False, condition=None, condeval=False, detectvar=True}
    newton:{facultative=False, eval=False, readonly=False, condition=None, condeval=False, detectvar=True}
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### Detailed Explanation of "DSCRIPT SAVE FILE" Sections:
1. **Global Parameters**:
   - Defined between `{...}` and describe the overall configuration of the script.
   - Common parameters include `SECTIONS`, `section`, `position`, `role`, `description`, `userid`, `version`, and `verbose`.
   - These parameters help control the behavior and structure of the script instance.

2. **Definitions**:
   - The `DEFINITIONS` section lists key-value pairs, where each key is a variable, and its value can be any valid Python data type (e.g., integers, strings, lists).
   - Example: `dimension=3`, `units=$si`, `boundary=['sm', 'sm', 'sm']`.
   - Variables starting with a `$` (e.g., `$si`) are typically placeholders or dynamic variables.

3. **Template**:
   - The `TEMPLATE` section defines the actual content of the script. Each line is in the format `key: content`, where `key` is a unique identifier, and `content` includes placeholders for variables (e.g., `${dimension}`).
   - Example: `dim: dimension    ${dimension}`.
   - The template is where variables from the `DEFINITIONS` section are substituted dynamically.

4. **Attributes**:
   - The `ATTRIBUTES` section defines the properties of each template entry. Each line associates a key with a dictionary of attributes (e.g., `facultative`, `eval`, `readonly`).
   - Example: `astyle:{facultative=False, eval=False, readonly=False, condition='${atom_style}', condeval=False, detectvar=True}`.
   - The attributes control how each template line behaves (e.g., whether it's evaluated, whether it depends on a condition, etc.).

### Adding Comments:
- Comments are added by starting a line with `#`. Comments can appear anywhere in the file, and they will be ignored during the loading process.
- Example:
    ```
    # This is a comment
    dim: dimension    ${dimension}  # Another comment
    ```
- Comments are typically used for documentation purposes within the DSCRIPT file, such as describing sections or explaining template logic.

### Imperative Components:
- **Header**: The line `# DSCRIPT SAVE FILE` must be present at the beginning of the file. It authenticates the file as a valid DSCRIPT file.
- **Template**: At least one template entry must be defined, as the template represents the main script content.

### Accessory Components:
- **Variable Substitution**: Variables (e.g., `${dimension}`) must be defined in the `DEFINITIONS` section to be substituted dynamically in the template content.
- **Attributes (Optional)**: Attributes are optional but provide more control over the template behavior when specified.
readonly=False, condition=None, condeval=False, detectvar=True}.

### Flexible structure
- **Global Parameters** can be defined anywhere but in a single block
- **Template** and **Attributes** lines can be mixed together.
                                                            

Production example (using last features)
------------------
```python
mydscriptfile = '''
            # GLOBAL DEFINITIONS (number of definitions=4)
            dumpfile = $dump.LAMMPS
            dumpdt = 50
            thermodt = 100
            runtime = 5000
            
            
            # TEMPLATES (number of items=24)
            
            # LOCAL DEFINITIONS for key '0'
            dimension = 3
            units = $si
            boundary = ['f', 'f', 'f']
            atom_style = $smd
            atom_modify = ['map', 'array']
            comm_modify = ['vel', 'yes']
            neigh_modify = ['every', 10, 'delay', 0, 'check', 'yes']
            newton = $off
            name = $SimulationBox
            
            0: [
                % --------------[ Initialization Header (helper) for "${name}"   ]--------------
                # set a parameter to None or "" to remove the definition
                dimension    ${dimension}
                units        ${units}
                boundary     ${boundary}
                atom_style   ${atom_style}
                atom_modify  ${atom_modify}
                comm_modify  ${comm_modify}
                neigh_modify ${neigh_modify}
                newton       ${newton}
                # ------------------------------------------
             ]
            
            # LOCAL DEFINITIONS for key '1'
            lattice_style = $sc
            lattice_scale = 0.0008271
            lattice_spacing = [0.0008271, 0.0008271, 0.0008271]
            
            1: [
                % --------------[ LatticeHeader 'helper' for "${name}"   ]--------------
                lattice ${lattice_style} ${lattice_scale} spacing ${lattice_spacing}
                # ------------------------------------------
             ]
            
            # LOCAL DEFINITIONS for key '2'
            xmin = -0.03
            xmax = 0.03
            ymin = -0.01
            ymax = 0.01
            zmin = -0.03
            zmax = 0.03
            nbeads = 3
            
            2: [
                % --------------[ Box Header 'helper' for "${name}"   ]--------------
                region box block ${xmin} ${xmax} ${ymin} ${ymax} ${zmin} ${zmax}
                create_box	${nbeads} box
                # ------------------------------------------
             ]
            
            # LOCAL DEFINITIONS for key '3'
            ID = $LowerCylinder
            style = $cylinder
            
            3: % variables to be used for ${ID} ${style}             ]
            
            # LOCAL DEFINITIONS for key '4'
            ID = $CentralCylinder
            
            4: % variables to be used for ${ID} ${style}
            
            # LOCAL DEFINITIONS for key '5'
            ID = $UpperCylinder
            
            5: % variables to be used for ${ID} ${style}
            
            # LOCAL DEFINITIONS for key '6'
            args = ['z', 0.0, 0.0, 36.27130939426913, 0.0, 6.045218232378189]
            side = ""
            move = ""
            rotate = ""
            open = ""
            ID = $LowerCylinder
            units = ""
            
            6: [
                % Create region ${ID} ${style} args ...  (URL: https://docs.lammps.org/region.html)
                # keywords: side, units, move, rotate, open
                # values: in|out, lattice|box, v_x v_y v_z, v_theta Px Py Pz Rx Ry Rz, integer
                region ${ID} ${style} ${args} ${side}${units}${move}${rotate}${open}
             ]
            
            # LOCAL DEFINITIONS for key '7'
            ID = $CentralCylinder
            args = ['z', 0.0, 0.0, 36.27130939426913, 6.045218232378189, 18.135654697134566]
            
            7: [
                % Create region ${ID} ${style} args ...  (URL: https://docs.lammps.org/region.html)
                # keywords: side, units, move, rotate, open
                # values: in|out, lattice|box, v_x v_y v_z, v_theta Px Py Pz Rx Ry Rz, integer
                region ${ID} ${style} ${args} ${side}${units}${move}${rotate}${open}
             ]
            
            # LOCAL DEFINITIONS for key '8'
            ID = $UpperCylinder
            args = ['z', 0.0, 0.0, 36.27130939426913, 18.135654697134566, 24.180872929512756]
            
            8: [
                % Create region ${ID} ${style} args ...  (URL: https://docs.lammps.org/region.html)
                # keywords: side, units, move, rotate, open
                # values: in|out, lattice|box, v_x v_y v_z, v_theta Px Py Pz Rx Ry Rz, integer
                region ${ID} ${style} ${args} ${side}${units}${move}${rotate}${open}
             ]
            
            # LOCAL DEFINITIONS for key '9'
            ID = $LowerCylinder
            beadtype = 1
            
            9: [
                % Create atoms of type ${beadtype} for ${ID} ${style} (https://docs.lammps.org/create_atoms.html)
                create_atoms ${beadtype} region ${ID}
             ]
            
            # LOCAL DEFINITIONS for key '10'
            ID = $CentralCylinder
            beadtype = 2
            
            10: [
                % Create atoms of type ${beadtype} for ${ID} ${style} (https://docs.lammps.org/create_atoms.html)
                create_atoms ${beadtype} region ${ID}
             ]
            
            # LOCAL DEFINITIONS for key '11'
            ID = $UpperCylinder
            beadtype = 3
            
            11: [
                % Create atoms of type ${beadtype} for ${ID} ${style} (https://docs.lammps.org/create_atoms.html)
                create_atoms ${beadtype} region ${ID}
             ]
            
            12: [
                # ===== [ BEGIN GROUP SECTION ] =====================================================================================
                group 	 lower 	type 	 1
                group 	 solid 	type 	 1 2 3
                group 	 fixed 	type 	 1
                group 	 middle 	type 	 2
                group 	 movable 	type 	 2 3
                group 	 upper 	type 	 3
                
                # ===== [ END GROUP SECTION ] =======================================================================================
                
                
                # [1:b1] PAIR STYLE SMD
                pair_style      hybrid/overlay smd/ulsph *DENSITY_CONTINUITY *VELOCITY_GRADIENT *NO_GRADIENT_CORRECTION &
                smd/tlsph smd/hertz 1.5
                
                # [1:b1 x 1:b1] Diagonal pair coefficient tlsph
                pair_coeff      1 1 smd/tlsph *COMMON 1000 10000.0 0.3 1.0 2.0 10.0 1000.0 &
                *STRENGTH_LINEAR_PLASTIC 1000.0 0 &
                *EOS_LINEAR &
                *END
                
                # [2:b2 x 2:b2] Diagonal pair coefficient tlsph
                pair_coeff      2 2 smd/tlsph *COMMON 1000 5000.0 0.3 1.0 2.0 10.0 1000.0 &
                *STRENGTH_LINEAR_PLASTIC 500.0 0 &
                *EOS_LINEAR &
                *END
                
                # [3:b3 x 3:b3] Diagonal pair coefficient tlsph
                pair_coeff      3 3 smd/tlsph *COMMON 1000 40000.0 0.3 1.0 2.0 10.0 1000.0 &
                *STRENGTH_LINEAR_PLASTIC 4000.0 0 &
                *EOS_LINEAR &
                *END
                
                # [1:b1 x 2:b2] Off-diagonal pair coefficient (generic)
                pair_coeff      1 2 smd/hertz 250.0000000000001
                
                # [1:b1 x 3:b3] Off-diagonal pair coefficient (generic)
                pair_coeff      1 3 smd/hertz 250.0000000000001
                
                # [2:b2 x 3:b3] Off-diagonal pair coefficient (generic)
                pair_coeff      2 3 smd/hertz 125.00000000000003
                
                # ===== [ END FORCEFIELD SECTION ] ==================================================================================
             ]
            
            13: [
                group all union lower middle upper
                group external subtract all middle
             ]
            
            14: velocity all set 0.0 0.0 0.0 units box
            15: fix fix_lower lower setforce 0.0 0.0 0.0
            16: fix move_upper upper move wiggle 0.0 0.0 ${amplitude} ${period} units box
            17: fix dtfix tlsph smd/adjust_dt ${dt}
            18: fix integration_fix tlsph smd/integrate_tlsph
            
            19: [
                compute S all smd/tlsph_stress
                compute E all smd/tlsph_strain
                compute nn all smd/tlsph_num_neighs
             ]
            
            20: [
                dump dump_id all custom ${dumpdt} ${dumpfile} id type x y z vx vy vz &
                c_S[1] c_S[2] c_S[4] c_nn &
                c_E[1] c_E[2] c_E[4] &
                vx vy vz
             ]
            
            21: dump_modify dump_id first yes
            
            22: [
                thermo ${thermodt}
                thermo_style custom step dt f_dtfix v_strain
             ]
            
            23: run ${runtime}
        '''
mydscript = dscript.parsesyntax(mydscriptfile,verbose=False,authentification=False)
mydscript[-1].definitions.runtime = 1000 # change local definitions of $runtime at the last step
print(mydscript.do(verbose=True))
```

Note that mydscript[-1].runtime = 1000 would have created the attribute runtime. Use definitions instead.

print(repr(mydscript[-1])) gives all details
--------------------------------------------------
Template Content | id:23        (1 line, 31 defs)   <--- all variables have be created also locally
--------------------------------------------------
run ${runtime}                                    
--------------------------------------------------
Detected Variable                  (1 / +1 / -0)
--------------------------------------------------
[+] runtime                                         <--- this runtime is a variable
--------------------------------------------------
Template Attributes                (7 attributes)
--------------------------------------------------
[ ] facultativ   [x] eval         [ ] readonly     
[ ] condition    [ ] condeval     [x] detectvar    
[x] runtime                                        <--- this runtime is an attribute


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
__version__ = "0.9983"



# INRAE\Olivier Vitrac - rev. 2024-11-08 (community)
# contact: olivier.vitrac@agroparistech.fr, han.chen@inrae.fr

# Revision history
# 2024-09-02 alpha version (compatibility issues with pizza.script)
# 2024-09-03 release candidate (fully compatible with pizza.script)
# 2024-09-04 load() and save() methods, improved documentation
# 2024-09-05 several fixes, add dscript.write(), dscript.parsesyntax()
# 2024-09-06 finalization of the block syntax between [], and its examples + documentation
# 2024-10-07 fix example
# 2024-10-09 remove_comments moved to script (to prevent circular reference)
# 2024-10-14 finalization of the integration with scripts
# 2024-10-17 fix __add__, improve repr()
# 2024-10-18 add add_dynamic_script() helper for adding a step to a dscript
# 2024-10-19 better file management 
# 2024-10-22 sophistication of ScriptTemplate to recognize defined variables at construction and to parse flags/conditions
# 2024-10-24 management of locl definitions in dscript.save() and dscript.parsesyntax()
# 2024-10-27 caching ScriptTemplate checks, improved dscript.save() methods
# 2024-10-28 less redundancy beyween local and global variables in dscript.save()
# 2024-10-07 new parsesyntax accepting [ ] at any position, improved doc, parsesyntax_legacy holds the old parser method
# 2024-10-08 fix single line templates


# Dependencies
import os, getpass, socket, time
import re, string, random, copy, hashlib
from datetime import datetime
from pizza.private.struct import paramauto
from pizza.script import script, scriptdata, pipescript, remove_comments, span

# %% Private Functions

def autoname(numChars=8):
    """ generate automatically names """
    return ''.join(random.choices(string.ascii_letters, k=numChars))  # Generates a random name of numChars letters


# %% Low-level Classes (wrappers for pizza.script)

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
    
    def __init__(self, _protection=False, _evaluation=True, sortdefinitions=False, **kwargs):
        """
        Constructor for lambdaScriptdata. It forces the parent's _returnerror parameter to False.
    
        Parameters:
        -----------
        _protection : bool, optional
            Whether to enable protection on the parameters (default: False).
        _evaluation : bool, optional
            Whether evaluation is enabled for the parameters (default: True).
        sortdefinitions : bool, optional
            Whether to sort definitions upon initialization (default: False).
        **kwargs : dict
            Additional keyword arguments for the parent class.
        """
        # Call the parent class constructor
        super().__init__(_protection=_protection, _evaluation=_evaluation, sortdefinitions=sortdefinitions, **kwargs)
        # Override the _returnerror attribute at the instance level
        self._returnerror = False


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
    
    def __init__(self, dscriptobj, persistentfile=True, persistentfolder=None,
                 printflag = False, verbose = True, softrun = True,
                 **userdefinitions):
        """
            Initialize a new `lambdaScript` instance.
            
            This constructor creates a `lambdaScript` object based on an existing `dscriptobj`, 
            providing options for persistent storage, verbose output, and user-defined configurations.
            A `lambdaScript` represents an anonymous or temporary script that can either preserve the 
            original script structure or partially evaluate variable definitions based on the `softrun` flag.
            
            Parameters
            ----------
            dscriptobj : dscript
                An existing `dscript` object to base the new instance on.
            persistentfile : bool, optional
                If `True`, the script will be saved to a persistent file. Defaults to `True`.
            persistentfolder : str or None, optional
                The folder where the persistent file will be saved. If `None`, a temporary location is used.
                Defaults to `None`.
            printflag : bool, optional
                If `True`, enables printing of the script details during execution. Defaults to `False`.
            verbose : bool, optional
                If `True`, provides detailed output during script initialization and execution. Defaults to `True`.
            softrun : bool, optional
                Determines whether a pre-execution run is carried out to partially evaluate and substitute variables.
                - If `True` (default), the variable definitions and original script content are preserved without full 
                  evaluation, meaning no substitution is carried out on the `dscript`'s templates or definitions.
                - If `False`, performs an initial evaluation phase that substitutes available variables and captures
                  the local definitions before creating the `lambdaScript` object.
            **userdefinitions
                Additional user-defined variables and configurations to be included in the `lambdaScript`.
            
            Raises
            ------
            TypeError
                If `dscriptobj` is not an instance of the `dscript` class.
            
            Example
            -------
            ```python
            existing_dscript = dscript(name="ExistingScript")
            ls = lambdaScript(existing_dscript, var3="3", softrun=False)
            ```
        """
        if not isinstance(dscriptobj, dscript):
            raise TypeError(f"The 'dscriptobj' object must be of class dscript not {type(dscriptobj).__name__}.")
        verbose = dscriptobj.verbose if verbose is None else dscriptobj.verbose
        super().__init__(persistentfile=persistentfile, persistentfolder=persistentfolder, printflag=printflag, verbose=verbose, **userdefinitions)
        self.name = dscriptobj.name
        self.SECTIONS = dscriptobj.SECTIONS
        self.section = dscriptobj.section
        self.position = dscriptobj.position
        self._role = dscriptobj.role  # Initialize an internal storage for the role
        self.description = dscriptobj.description
        self.userid = dscriptobj.userid
        self.version= dscriptobj.version
        self.verbose = verbose
        self.printflag = printflag
        self.DEFINITIONS = dscriptobj.DEFINITIONS
        if softrun:
            self.TEMPLATE,localdefinitions = dscriptobj.do(softrun=softrun,return_definitions=True)
            self.USER = localdefinitions + lambdaScriptdata(**self.USER)
        else:
            self.TEMPLATE = dscriptobj.do(softrun=softrun)
            self.USER = lambdaScriptdata(**self.USER)
        
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
     The `ScriptTemplate` class provides a mechanism to store, process, and dynamically substitute 
     variables within script content. This class supports handling flags and conditions, allowing 
     for flexible and conditional execution of parts of the script.
    
     Attributes:
     -----------
     default_attributes : dict (class-level)
         A dictionary containing the default flags for each `ScriptTemplate` object. These attributes 
         are applied when initializing the object or when no flags are specified in the content.
         Flags include:
         - facultative (bool): If True, the script line is optional and may be discarded if certain 
             conditions are not met. (default: False)
         - eval (bool): If True, the content is evaluated using `formateval`, which allows for variable 
             substitution during execution. (default: False)
         - readonly (bool): If True, the content cannot be modified after initialization. (default: False)
         - condition (str or None): A string that specifies a condition for executing the content.
             If the condition is not met, the script line is skipped. (default: None)
         - condeval (bool): If True, the `condition` attribute is evaluated dynamically using variables.
             (default: False)
         - detectvar (bool): If True, any variables in the content (e.g., `${varname}`) are automatically 
             detected and registered in the definitions. (default: True)
    
     Methods:
     --------
     __init__(self, content="", definitions=lambdaScriptdata(), userid=None, verbose=False, **kwargs):
         Initializes the `ScriptTemplate` object with script content, optional variable definitions, 
         and configurable attributes. Flags like `facultative`, `eval`, `readonly`, `condition`, 
         and others are set via content prefixes or passed directly as keyword arguments.
     
     parse_content(cls, content, verbose=False):
         A class method that parses content to detect special flags and condition tags, returning the 
         cleaned content and a dictionary of attributes (flags).
         
         The method processes the following flags and tags:
         - `!` : Sets `eval=True`, which forces evaluation of the content.
         - `?` : Sets `facultative=True`, marking the content as optional.
         - `^` : Sets `readonly=True`, preventing modifications to the content.
         - `~` : Sets `detectvar=False`, disabling automatic variable detection.
         - `[if:condition]` : Defines a condition for executing the script. If the condition is met, 
           the script will be executed. Conditions can include `;eval` to trigger evaluation.
    
         Parameters:
         -----------
         content : str
             The script content to be parsed. It may contain lines starting with special characters
             that set specific attributes for the script template.
    
         verbose : bool (default: False)
             If True, preserves comments and does not remove comment lines during parsing.
    
         Returns:
         --------
         cleaned_content : str
             The cleaned script content, with all flags and conditions removed.
         
         attributes : dict
             A dictionary of parsed attributes (flags) including:
             - facultative (bool): Indicates if the content is optional.
             - eval (bool): Specifies if the content should be evaluated for variable substitution.
             - readonly (bool): Prevents modifications to the content.
             - condition (str or None): Defines the condition for executing the script.
             - condeval (bool): If True, dynamically evaluates the condition.
             - detectvar (bool): If True, detects and registers variables in the content.
         
     detect_variables(self):
         Detects variables in the content using the pattern `${varname}`. It returns a list of 
         variable names found in the script.
    
     refreshvar(self):
         Ensures that any detected variables are added to the `definitions` if they are missing.
    
     __setattr__(self, name, value):
         Sets the value of an attribute. The method performs validation on specific attributes
         (e.g., `eval`, `readonly`, `facultative`, etc.) to ensure the correct data types are assigned.
    
     __getattr__(self, name):
         Retrieves the value of an attribute. If the attribute is not set, it returns the default 
         value from `default_attributes`.
            

    Example 1:
    ----------
    # Create a ScriptTemplate object with content and optional definitions
    line = ScriptTemplate("dimension    ${dimension}")

    # You can also pass in global definitions if needed
    global_definitions = lambdaScriptdata(dimension=3)
    line_with_defs = ScriptTemplate("dimension    ${dimension}", 
                                    definitions=global_definitions)

    After initialization, you can modify the line's attributes or use it as 
    part of a larger script managed by a `dscript` object.
    
    
     Example 2:
     ----------
     # Example of using flags and conditions in content
     
     line = ScriptTemplate("!velocity all set 0.0 0.0 0.0 units box")
     # This will automatically set `eval=True` due to the '!' flag.
    
     line_with_condition = ScriptTemplate("[if: ${condition};eval] fix upper move wiggle 0.0 0.0 1.0 1.0")
     # This content will only execute if `${condition}` is True, and `eval` will be applied to substitute variables.

    """
    
    # Class-level attribute for default flags
    default_attributes = {
        'facultative': False,
        'eval': False,
        'readonly': False,
        'condition': None,
        'condeval': False,
        'detectvar': True
    }
    
    def __init__(self, content="", definitions=lambdaScriptdata(), userid=None, verbose=False, **kwargs):
        """
        Initializes a new `ScriptTemplate` object.
        
        The constructor sets up a new script template with content, optional variable
        definitions, and a set of configurable attributes. This template is capable
        of dynamically substituting variables using a provided `lambdaScriptdata`
        object or internal definitions. You can also manage attributes like evaluation,
        facultative execution, and variable detection.
    
        Parameters:
        -----------
        content : str or list of str
            The content of the script template, which can be a single string or a list of strings.
            If a single string is provided, it will automatically be converted to a list of lines.
            This ensures consistent handling of multi-line content.
    
        definitions : lambdaScriptdata, optional
            A reference to a `lambdaScriptdata` object that contains global variable 
            definitions. These definitions will be used to substitute variables within the content.
            If `definitions` is not provided, variable substitution will rely on local 
            or inline definitions.
        
        verbose : flag (default value=False)
            If True the comments are preserved (applied when str is a string).
    
        **kwargs : 
            Additional keyword arguments to set specific attributes for the script line.
            These attributes control the behavior of the script template during evaluation 
            and execution. Any keyword argument passed here will update the default 
            attribute values.
    
                Default attributes (with default values):
            - facultative (False): 
                If True, the script line is optional and may be discarded if certain conditions are not met.
            - eval (False): 
                If True, the content will be evaluated using `formateval`, allowing variable 
                substitution during the execution.
            - readonly (False): 
                If True, the content of the script cannot be modified after initialization.
            - condition (None): 
                An optional condition that controls whether the content will be executed. 
                If the condition is not met, the script line will not be executed.
            - condeval (False): 
                If True, the `condition` attribute will be evaluated, allowing conditional 
                logic based on variable values.
            - detectvar (True): 
                If True, the content will automatically detect and register any variables 
                (such as `${varname}`) within the `definitions` for substitution.
        """
        

        # Initialize `_CACHE` with separate entries for each method
        self._CACHE = {
            'variables': {'result': None},
            'check_variables': {'result': None}
        }
        # Constructor
        self._content = content # # Store initial content
        self.definitions = definitions  # Reference to the DEFINITIONS object
        # Initialize attributes with default values
        self.attributes = self.default_attributes.copy()
        # Convert single string content to a list for consistent processing
        if content == "" or content is None:
            content = ""  # Set to empty string if None
        elif isinstance(content, str):
            # Interpret the content and extract any attribute flags (e.g. !, ?, etc.)
            content, self.attributes = self.parse_content(content, verbose=verbose)
            # Convert content to a list of strings
            if verbose:
                content = content.split('\n')  # All comments are preserved during construction
            else:
                content = remove_comments(content, split_lines=True)  # Split string by newlines into list of strings
        elif not isinstance(content, list) or not all(isinstance(item, str) for item in content):
            raise TypeError("The 'content' attribute must be a string or a list of strings.")
        # Assign content to the object
        self.content = content
        # Update attributes with any additional keyword arguments passed in
        self.attributes.update(kwargs)
        # Detect variables in the content
        detected_variables = self.detect_variables()
        # Automatically set `eval=True` if any detected variables are defined in `definitions`
        if detected_variables:
            for var in detected_variables:
                if var in self.definitions:
                    self.attributes['eval'] = True
                    break  # No need to continue checking once we know eval should be set
        # Assign userid (optional)
        self.userid = userid if userid is not None else autoname(3)


    def _calculate_content_hash(self, content):
        """Generate hash for content."""
        return hashlib.md5("\n".join(content).encode()).hexdigest() if isinstance(content, list) else hashlib.md5(content.encode()).hexdigest()

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, new_content):
        """Set content and reinitialize cache if the content has changed."""
        new_content_hash = self._calculate_content_hash(new_content)
        if new_content_hash != self._content_hash:
            self._content = new_content
            self._content_hash = new_content_hash
            self._invalidate_cache()  # Reset cache only if content changes


    def _update_content(self, value):
        """Helper to set _content and _content_hash, refreshing cache as necessary."""
        # Check if content modification is allowed based on readonly attribute
        if getattr(self, 'attributes', {}).get('readonly', False):
            raise AttributeError("Cannot modify content. It is read-only.")
        # Validate and process content as either a string or list of strings
        if isinstance(value, str):
            value = remove_comments(value, split_lines=True)
        elif not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            raise TypeError("The 'content' attribute must be a string or a list of strings.")
        # Set _content and calculate hash
        super().__setattr__('_content', value)
        new_hash = hash(tuple(value))
        # If hash changes, reset cache
        if new_hash != getattr(self, '_content_hash', None):
            super().__setattr__('_content_hash', new_hash)
            self._invalidate_cache()  # Invalidate cache due to content change
            self.refreshvar()  # Refresh variables based on new content

    def _invalidate_cache(self):
        """Reset all cache entries."""
        # Check if _CACHE is initialized
        if not hasattr(self, '_CACHE'):
            self._CACHE = {
                'variables': {'result': None},
                'check_variables': {'result': None}
            }
        for entry in self._CACHE.values():
            entry['result'] = None


    @classmethod
    def parse_content(cls, content, verbose=False):
        """
        Parse the content string and return:
        1. Cleaned content (without flags or condition tags).
        2. A dictionary of attributes (flags) initialized with default values.

        Parameters:
        -----------
        content : str
            The content string to be parsed.

        Returns:
        --------
        cleaned_content : str
            The cleaned content with all flag prefixes and condition tags removed.
        attributes : dict
            A dictionary of attributes (flags) set based on the content prefixes.
        """
        attributes = cls.default_attributes.copy()

        # Handle empty content
        if not content.strip():  # Empty string or whitespace-only
            return "", attributes

        idx = 0
        cleaned_content = []

        # If content is a single string, split it into lines
        if isinstance(content, str):
            content = content.split('\n')

        # Remove leading and trailing empty lines
        while content and content[0].strip() == '':
            content.pop(0)
        while content and content[-1].strip() == '':
            content.pop()

        # Process each remaining line to detect flags and conditions
        for line in content:
            idx = 0
            line = line.strip()  # Trim any leading/trailing whitespace

            # Parse flags and conditions only at the beginning of the line
            while idx < len(line):
                ch = line[idx]
                if ch == '!':
                    attributes['eval'] = True
                    idx += 1
                elif ch == '?':
                    attributes['facultative'] = True
                    idx += 1
                elif ch == '^':
                    attributes['readonly'] = True
                    idx += 1
                elif ch == '~':
                    attributes['detectvar'] = False
                    idx += 1
                elif line.startswith('[if:', idx):
                    # Parse condition
                    end_idx = line.find(']', idx)
                    if end_idx == -1:
                        raise ValueError("Unclosed '[if:]' tag in content")
                    cond_str = line[idx + 4:end_idx]
                    if ';eval' in cond_str:
                        attributes['condeval'] = True
                        cond_str = cond_str.replace(';eval', '')
                    attributes['condition'] = cond_str.strip()
                    idx = end_idx + 1
                else:
                    break  # No more flags or conditions, process the rest of the line

                # Skip any whitespace after flags or conditions
                while idx < len(line) and line[idx] in (' ', '\t'):
                    idx += 1

            # Append the cleaned line (without flags or condition tags)
            cleaned_content.append(line[idx:].strip())

        # Join the cleaned lines back into a single string
        cleaned_content = '\n'.join(cleaned_content)

        return cleaned_content, attributes



    def __str__(self):
        num_attrs = len(self.attributes)  # All attributes count
        return f"1 line/block, {num_attrs} attributes"


    def __repr__(self):
      # Template content section
      total_lines = len(self.content)
      total_variables = len(self.definitions)
      line_word = "lines" if total_lines > 1 else "line"
      variable_word = "defs" if total_variables > 1 else "def"
      content_label = "Template Content"
      content_label += "" if self.userid == "" else f" | id:{self.userid}"
      available_space = 50 - len(content_label) - 1
      repr_str = "-" * 50 + "\n"
      repr_str += f"{content_label}{('(' + str(total_lines) + ' ' + line_word + ', ' + str(total_variables) + ' ' + variable_word + ')').rjust(available_space)}\n"
      repr_str += "-" * 50 + "\n"
    
      if total_lines < 1:
          repr_str += "< empty content >\n"
      elif total_lines <= 12:
          # If content has 12 or fewer lines, display all lines
          for line in self.content:
              truncated_line = (line[:18] + '[...]' + line[-18:]) if len(line) > 40 else line
              repr_str += f"{truncated_line:<50}\n"
      else:
          # Display first three lines, middle three lines, and last three lines
          for line in self.content[:3]:
              truncated_line = (line[:18] + '[...]' + line[-18:]) if len(line) > 40 else line
              repr_str += f"{truncated_line:<50}\n"
          repr_str += "\t\t[...]\n"
          mid_start = total_lines // 2 - 1
          mid_end = mid_start + 3
          for line in self.content[mid_start:mid_end]:
              truncated_line = (line[:18] + '[...]' + line[-18:]) if len(line) > 40 else line
              repr_str += f"{truncated_line:<50}\n"
          repr_str += "\t\t[...]\n"
          for line in self.content[-3:]:
              truncated_line = (line[:18] + '[...]' + line[-18:]) if len(line) > 40 else line
              repr_str += f"{truncated_line:<50}\n"
    
      # Detected Variables section in 3-column format
      detected_variables = self.detect_variables()
      if detected_variables:
          repr_str += "-" * 50 + "\n"
          # Count the number of defined and missing variables
          defined_variables = set(self.definitions.keys()) if self.definitions else set()
          variable_word = 'Variables' if len(detected_variables) > 1 else 'Variable'
          detected_set = set(detected_variables)
          missing_variables = detected_set - defined_variables
          defined_count = len(detected_set & defined_variables)
          missing_count = len(missing_variables)
          total_variables = len(detected_set)
          repr_str += f"Detected {variable_word}{('(' + str(total_variables) + ' / +' + str(defined_count) + ' / -' + str(missing_count) + ')').rjust(50 - len('Detected Variables') - 1)}\n"
          repr_str += "-" * 50 + "\n"
    
          # Display variables with status:
          # [+] for defined variables with values other than "${varname}"
          # [-] for defined variables with default values "${varname}"
          # [ ] for undefined variables
          for i in range(0, len(detected_variables), 3):
              var_set = detected_variables[i:i+3]
              line = ""
              for var in var_set:
                  var_name = (var[:10] + ' ') if len(var) > 10 else var.ljust(11)
                  if var in defined_variables:
                      # Check if it's set to its default value (i.e., "${varname}")
                      if self.definitions[var] == f"${{{var}}}":
                          flag = '[-]'
                      else:
                          flag = '[+]'
                  else:
                      flag = '[ ]'
                  line += f"{flag} {var_name}  "
              repr_str += f"{line}\n"
    
      # Attribute section in 3 columns
      repr_str += "-" * 50 + "\n"
      repr_str += f"Template Attributes{('(' + str(len(self.attributes)) + ' attributes)').rjust(50 - len('Template Attributes') - 1)}\n"
      repr_str += "-" * 50 + "\n"
    
      # Create a compact three-column layout for attributes with checkboxes
      attr_items = [(attr, '[x]' if value else '[ ]') for attr, value in self.attributes.items() if attr != 'definitions']
      for i in range(0, len(attr_items), 3):
          attr_set = attr_items[i:i+3]
          line = ""
          for attr, value in attr_set:
              attr_name = (attr[:10] + ' ') if len(attr) > 10 else attr.ljust(11)
              line += f"{value} {attr_name}  "
          repr_str += f"{line}\n"
    
      return repr_str


    def __setattr__(self, name, value):
        # Handle specific attributes with validation
        if name in ['facultative', 'eval', 'readonly']:
            if not isinstance(value, bool):
                raise TypeError(f"The '{name}' attribute must be a Boolean, not {type(value).__name__}.")
        elif name == 'condition':
            if not isinstance(value, str) and value is not None:
                raise TypeError(f"The 'condition' attribute must be a string or None, not {type(value).__name__}.")
        elif name == 'content':
            # Use helper to manage content updates and cache invalidation
            self._update_content(value)
            return  # Exit to avoid further processing since _update_content handles the setting
        elif name == 'definitions':
            if not isinstance(value, (lambdaScriptdata, scriptdata)) and value is not None:
                raise TypeError(f"The 'definitions' must be a lambdaScriptdata or scriptdata, not {type(value).__name__}.")
    
        # Set attributes directly for key fields and avoid recursion
        if name in ['userid', 'attributes', 'definitions', '_content', '_content_hash']:
            super().__setattr__(name, value)
        else:
            # Ensure 'attributes' is initialized before updating
            if not hasattr(self, 'attributes') or self.attributes is None:
                self.attributes = {}
            self.attributes[name] = value


    def __getattr__(self, name):
        """
        Handles attribute retrieval, checking the following in order:
        1. If 'name' is in default_attributes, return the value from attributes if it exists, 
           otherwise return the default value from default_attributes.
        2. If 'name' is 'content', return the content (or an empty string if content is not set).
        3. If 'name' exists in the attributes dictionary, return its value.
        4. If attributes itself exists in __dict__, return the value from attributes if 'name' is found.
        5. If all previous checks fail, raise an AttributeError indicating that 'name' is not found.
        """
        # Ensure '_CACHE' is always accessible without a KeyError
        if name == '_CACHE':
            # Initialize _CACHE if it does not exist
            if '_CACHE' not in self.__dict__:
                self.__dict__['_CACHE'] = {
                    'variables': {'result': None},
                    'check_variables': {'result': None}
                }
            return self.__dict__['_CACHE']  # Access _CACHE directly
        # Step 1: Check if 'name' is a valid attribute in default_attributes
        if name in self.default_attributes:
            # Directly access __dict__ to avoid recursive lookup
            attributes = self.__dict__.get('attributes', {})
            return attributes.get(name, self.default_attributes[name])
        # Step 2: Special case for 'content'
        if name == 'content':
            # Directly access __dict__ to avoid recursion
            return self.__dict__.get('_content', "")
        # Step 3: Check if 'name' exists in 'attributes' and return its value directly
        attributes = self.__dict__.get('attributes', {})
        if name in attributes:
            return attributes[name]
        # Step 4: Check if 'attributes' exists in __dict__ and retrieve 'name' if present
        if 'attributes' in self.__dict__ and name in self.__dict__['attributes']:
            return self.__dict__['attributes'][name]
        # Step 5: If none of the above conditions are met, raise an AttributeError
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")



    
    def do(self, protected=True, softrun=False):
        """
        Executes or prepares the script template content based on its attributes and the softrun flag.

        Parameters
        ----------
        protected : bool, optional
            If `True` (default), variable evaluation uses a protected environment, preventing changes 
            to global definitions or system attributes during execution.
        softrun : bool, optional
            Determines if the script is evaluated in a preliminary mode:
            - If `True`, returns the script content without full evaluation, allowing for a preview or 
              an initial capture of local definitions without substitution of variables.
            - If `False` (default), processes the script with full evaluation, applying all substitutions 
              defined in `definitions`.

        Returns
        -------
        str
            The processed or original script content as a single string. 
            - Returns an empty string if `facultative` is set to `True`, or if `condition` is `False` 
              and does not satisfy any specified evaluation requirements.
        
        Notes
        -----
        - `facultative`: If `True`, the method returns an empty string, effectively skipping execution.
        - `condition`: If specified, this attribute is evaluated to decide whether the content is processed 
          (default `True` if `condition` is `None`). If `condeval` is `True`, the condition itself undergoes 
          evaluation using Python's `eval`.
        - `eval`: If `True` and `softrun` is `False`, performs evaluation for variable substitution on the 
          content lines, transforming variables based on the `definitions`.
        """

        # If 'facultative' is set to True, return an empty string immediately
        if self.attributes.get("facultative", False):
            return ""

        # Evaluate condition if present
        cond = True
        if self.attributes.get("condition") is not None:
            condition_expr = self.definitions.formateval(self.attributes["condition"], protected)
            cond = eval(condition_expr) if self.attributes.get("condeval", False) else condition_expr

        # Process based on softrun flag
        if softrun:
            return "\n".join(self.content) if cond else ""

        # Perform full processing when softrun is False
        if cond:
            if self.attributes.get("eval", False):
                return "\n".join([self.definitions.formateval(line, protected) for line in self.content])
            else:
                return "\n".join(self.content)

        return ""


    
    def detect_variables(self):
        """
        Detects variables in the content of the template using the pattern r'\$\{(\w+)\}'.

        Returns:
        --------
        list
            A list of unique variable names detected in the content.
        """
        # Check cache first
        cache_entry = self._CACHE['variables']         
        if cache_entry['result'] is not None:
            return cache_entry['result']
        # Detect variables if cache miss or content changed
        variable_pattern = re.compile(r'\$\{(\w+)\}')
        detected_vars = {variable for line in self.content for variable in variable_pattern.findall(line)}
        # Cache the result and return output
        cache_entry['result'] = list(detected_vars)
        return cache_entry['result']



    def refreshvar(self):
        """
        Detects variables in the content and adds them to definitions if needed.
        This method ensures that variables like ${varname} are correctly detected
        and added to the definitions if they are missing.
        """
        if self.attributes["detectvar"] and isinstance(self.content, list) and self.definitions:
            variables = self.detect_variables()
            for varname in variables:
                if varname not in self.definitions:
                    self.definitions.setattr(varname, "${" + varname + "}")


    def check_variables(self, verbose=True, seteval=True):
        """
        Checks for undefined variables in the ScriptTemplate instance.

        Parameters:
        -----------
        verbose : bool, optional, default=True
            If True, prints information about variables for the template.
            Shows [-] if the variable is set to its default value, [+] if it is defined, and [ ] if it is undefined.

        seteval : bool, optional, default=True
            If True, sets the `eval` attribute to True if at least one variable is defined or set to its default value.

        Returns:
        --------
        out : dict
            A dictionary with lists of default variables, set variables, and undefined variables:
            - "defaultvalues": Variables set to their default value (${varname}).
            - "setvalues": Variables defined with a specific value.
            - "undefined": Variables that are undefined.
        """
        # Check cache first
        cache_entry = self._CACHE['check_variables']
        if cache_entry['result'] is not None:
            return cache_entry['result']
        # Main
        out = {"defaultvalues": [], "setvalues": [], "undefined": []}        
        detected_vars = self.detect_variables()
        defined_vars = set(self.definitions.keys()) if self.definitions else set()
        set_values, default_values, undefined_vars = [], [], []
        if verbose:
            print(f"\nTEMPLATE {self.userid} variables:")
        for var in detected_vars:
            if var in defined_vars:
                if self.definitions[var] == f"${{{var}}}":  # Check for default value
                    default_values.append(var)
                    if verbose:
                        print(f"[-] {var}")  # Variable is set to its default value
                else:
                    set_values.append(var)
                    if verbose:
                        print(f"[+] {var}")  # Variable is defined with a specific value
            else:
                undefined_vars.append(var)
                if verbose:
                    print(f"[ ] {var}")  # Variable is not defined
        # If seteval is True, set eval to True if at least one variable is defined or set to its default
        if seteval and (set_values or default_values):
            self.attributes['eval'] = True  # Set eval in the attributes dictionary
        # Update the output dictionary
        out["defaultvalues"].extend(default_values)
        out["setvalues"].extend(set_values)
        out["undefined"].extend(undefined_vars)
        # update Cache and return output
        cache_entry['result'] = out
        return out


    def is_variable_defined(self, var_name):
        """
        Checks if a specified variable is defined (either as a default value or a set value).
    
        Parameters:
        -----------
        var_name : str
            The name of the variable to check.
    
        Returns:
        --------
        bool
            True if the variable is defined (either as a default or a set value), False if not.
    
        Raises:
        -------
        ValueError
            If `var_name` is invalid or undefined in the template.
        """
        if not isinstance(var_name, str):
            raise ValueError("Variable name must be a string.")
        
        variable_status = self.check_variables(verbose=False, seteval=False)
        
        # Check if the variable is in default values or set values
        if var_name in variable_status["defaultvalues"] or var_name in variable_status["setvalues"]:
            return True
        else:
            raise ValueError(f"Variable '{var_name}' is undefined in the template.")
    
    
    def is_variable_set_value_only(self, var_name):
        """
        Checks if a specified variable is defined and set to a specific (non-default) value.
    
        Parameters:
        -----------
        var_name : str
            The name of the variable to check.
    
        Returns:
        --------
        bool
            True if the variable is defined with a set (non-default) value, False if not.
    
        Raises:
        -------
        ValueError
            If `var_name` is invalid or not defined in the template.
        """
        if not isinstance(var_name, str):
            raise ValueError("Variable name must be a string.")
        
        variable_status = self.check_variables(verbose=False, seteval=False)
        
        # Check if the variable is in set values only (not default values)
        if var_name in variable_status["setvalues"]:
            return True
        elif var_name in variable_status["defaultvalues"]:
            return False  # Defined but only at its default value
        else:
            raise ValueError(f"Variable '{var_name}' is undefined in the template.")


class dscript:
    """
    dscript: A Dynamic Script Management Class

    The `dscript` class is designed to manage and dynamically generate multiple
    lines/items of a script, typically for use with LAMMPS or similar simulation tools.
    Each line in the script is represented as a `ScriptTemplate` object, and the
    class provides tools to easily manipulate, concatenate, and execute these
    script lines/items.

    Key Features:
    -------------
    - **Dynamic Script Generation**: Define and manage script lines/items dynamically,
      with variables that can be substituted at runtime.
    - **Conditional Execution**: Add conditions to script lines/items so they are only
      included if certain criteria are met.
    - **Script Concatenation**: Combine multiple script objects while maintaining
      control over variable precedence and script structure.
    - **User-Friendly Access**: Easily access and manipulate script lines/items using
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
        returns a new `dscript` object with lines/items reordered accordingly.

    __setitem__(self, key, value):
        Adds or updates a script line. If the value is an empty list, the
        corresponding script line is removed.

    __delitem__(self, key):
        Deletes a script line by its key.

    __contains__(self, key):
        Checks if a key exists in the script. Allows usage of `in` keyword.

    __iter__(self):
        Returns an iterator over the script lines/items, allowing for easy iteration
        through all lines/items in the `TEMPLATE`.

    __len__(self):
        Returns the number of script lines/items currently stored in the `TEMPLATE`.

    keys(self):
        Returns the keys of the `TEMPLATE` dictionary.

    values(self):
        Returns the `ScriptTemplate` objects stored as values in the `TEMPLATE`.

    items(self):
        Returns the keys and `ScriptTemplate` objects from the `TEMPLATE` as pairs.

    __str__(self):
        Returns a human-readable summary of the script, including the number
        of lines/items and total attributes. Shortcut: `str(S)`.

    __repr__(self):
        Provides a detailed string representation of the entire `dscript` object,
        including all script lines/items and their attributes. Useful for debugging.

    reorder(self, order):
        Reorders the script lines/items based on a given list of indices, creating a
        new `dscript` object with the reordered lines/items.

    get_content_by_index(self, index, do=True, protected=True):
        Returns the processed content of the script line at the specified index,
        with variables substituted based on the definitions and conditions applied.

    get_attributes_by_index(self, index):
        Returns the attributes of the script line at the specified index.
        
    add_dynamic_script(self, key, content="", definitions=None, verbose=None, **USER):
        Add a dynamic script step to the `dscript` object.

    createEmptyVariables(self, vars):
        Creates new variables in `DEFINITIONS` if they do not already exist.
        Accepts a single variable name or a list of variable names.

    do(self, printflag=None, verbose=None):
        Executes all script lines/items in the `TEMPLATE`, concatenating the results,
        and handling variable substitution. Returns the full script as a string.

    script(self, **userdefinitions):
        Generates a `lamdaScript` object from the current `dscript` object,
        applying any additional user definitions provided.

    pipescript(self, printflag=None, verbose=None, **USER):
        Returns a `pipescript` object by combining script objects for all keys
        in the `TEMPLATE`. Each key in `TEMPLATE` is handled separately, and
        the resulting scripts are combined using the `|` operator.

    save(self, filename=None, foldername=None, overwrite=False):
        Saves the current script instance to a text file in a structured format.
        Includes metadata, global parameters, definitions, templates, and attributes.

    write(scriptcontent, filename=None, foldername=None, overwrite=False):
        Writes the provided script content to a specified file in a given folder,
        with a header added if necessary, ensuring the correct file format.

    load(cls, filename, foldername=None, numerickeys=True):
        Loads a script instance from a text file, restoring the content, definitions,
        templates, and attributes. Handles parsing and variable substitution based on
        the structure of the file.

    parsesyntax(cls, content, numerickeys=True):
        Parses a script instance from a string input, restoring the content, definitions,
        templates, and attributes. Handles parsing and variable substitution based on the
        structure of the provided string, ensuring the correct format and key conversions
        when necessary.

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
        A dictionary storing script lines/items, with keys to identify each line.
    DEFINITIONS : lambdaScriptdata
        Stores the variables and parameters used within the script lines/items.
    """

    # Class variable to list attributes that should not be treated as TEMPLATE entries
    construction_attributes = {'name', 'SECTIONS', 'section', 'position', 'role', 'description',
                               'userid', 'version', 'verbose', 'printflag', 'DEFINITIONS', 'TEMPLATE'
                               }
    
    def __init__(self,  name=None,
                        SECTIONS = ["DYNAMIC"],
                        section = 0,
                        position = None,
                        role = "dscript instance",
                        description = "dynamic script",
                        userid = "dscript",
                        version = 0.1,
                        printflag = False,
                        verbose = False,
                        **userdefinitions
                        ):
        """
        Initializes a new `dscript` object.

        The constructor sets up a new `dscript` object, which allows you to 
        define and manage a script composed of multiple lines/items. Each line is 
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

        After initialization, you can start adding script lines/items and defining variables.
        """
        
        if name is None:
            self.name = autoname()
        else:
            self.name = name
        self.SECTIONS = SECTIONS if isinstance(SECTIONS,(list,tuple)) else [SECTIONS]
        self.section = section
        self.position = position if position is not None else 0
        self.role = role
        self.description = description
        self.userid = userid
        self.version = version
        self.verbose = verbose
        self.printflag = printflag
        self.DEFINITIONS = lambdaScriptdata(**userdefinitions)
        self.TEMPLATE = {}


    def __getattr__(self, attr):
        # During construction phase, we only access the predefined attributes
        if 'TEMPLATE' not in self.__dict__:
            if attr in self.__dict__:
                return self.__dict__[attr]
            raise AttributeError(f"'dscript' object has no attribute '{attr}'")
        
        # If TEMPLATE is initialized and attr is in TEMPLATE, return the corresponding ScriptTemplate entry
        if attr in self.TEMPLATE:
            return self.TEMPLATE[attr]

        # Fall back to internal __dict__ attributes if not in TEMPLATE
        if attr in self.__dict__:
            return self.__dict__[attr]

        raise AttributeError(f"'dscript' object has no attribute '{attr}'")
        
        
    def __setattr__(self, attr, value):
        # Handle internal attributes during the construction phase
        if 'TEMPLATE' not in self.__dict__:
            self.__dict__[attr] = value
            return

        # Handle construction attributes separately (name, TEMPLATE, USER)
        if attr in self.construction_attributes:
            self.__dict__[attr] = value
        # If TEMPLATE exists, and the attribute is intended for it, update TEMPLATE
        elif 'TEMPLATE' in self.__dict__:
            # Convert the value to a ScriptTemplate if needed, and update the template
            if attr in self.TEMPLATE:
                # Modify the existing ScriptTemplate object for this attribute
                if isinstance(value, str):
                    self.TEMPLATE[attr].content = value
                elif isinstance(value, dict):
                    self.TEMPLATE[attr].attributes.update(value)
            else:
                # Create a new entry if it does not exist
                self.TEMPLATE[attr] = ScriptTemplate(content=value,definitions=self.DEFINITIONS,verbose=self.verbose,userid=attr)
        else:
            # Default to internal attributes
            self.__dict__[attr] = value
            

    def __getitem__(self, key):
        """
        Implements index-based retrieval, slicing, or reordering for dscript objects.
    
        Parameters:
        -----------
        key : int, slice, list, or str
            - If `key` is an int, returns the corresponding template at that index.
              Supports negative indices to retrieve templates from the end.
            - If `key` is a slice, returns a new `dscript` object containing the templates in the specified range.
            - If `key` is a list, reorders the TEMPLATE based on the list of indices or keys.
            - If `key` is a string, treats it as a key and returns the corresponding template.
    
        Returns:
        --------
        dscript or ScriptTemplate : Depending on the type of key, returns either a new dscript object (for slicing or reordering)
                                    or a ScriptTemplate object (for direct key access).
        """
        # Handle list-based reordering
        if isinstance(key, list):
            return self.reorder(key)
    
        # Handle slicing
        elif isinstance(key, slice):
            new_dscript = dscript(name=f"{self.name}_slice_{key.start}_{key.stop}")
            keys = list(self.TEMPLATE.keys())
            for k in keys[key]:
                new_dscript.TEMPLATE[k] = self.TEMPLATE[k]
            return new_dscript
    
        # Handle integer indexing with support for negative indices
        elif isinstance(key, int):
            keys = list(self.TEMPLATE.keys())
            if key in self.TEMPLATE:  # Check if the integer exists as a key
                return self.TEMPLATE[key]
            if key < 0:  # Support negative indices
                key += len(keys)
            if key < 0 or key >= len(keys):  # Check for index out of range
                raise IndexError(f"Index {key - len(keys)} is out of range")
            # Return the template corresponding to the integer index
            return self.TEMPLATE[keys[key]]
    
        # Handle key-based access (string keys)
        elif isinstance(key, str):
            if key in self.TEMPLATE:
                return self.TEMPLATE[key]
            raise KeyError(f"Key '{key}' does not exist in TEMPLATE.")


    def __setitem__(self, key, value):
        if (value == []) or (value is None):
            # If the value is an empty list, delete the corresponding key
            del self.TEMPLATE[key]
        else:
            # Otherwise, set the key to the new ScriptTemplate
            self.TEMPLATE[key] = ScriptTemplate(value, definitions=self.DEFINITIONS, verbose=self.verbose, userid=key)

    def __delitem__(self, key):
        del self.TEMPLATE[key]

    def __iter__(self):
        return iter(self.TEMPLATE.items())

    # def keys(self):
    #     return self.TEMPLATE.keys()

    # def values(self):
    #     return (s.content for s in self.TEMPLATE.values())
    
    def __contains__(self, key):
        return key in self.TEMPLATE
    
    def __len__(self):
        return len(self.TEMPLATE)

    def items(self):
        return ((key, s.content) for key, s in self.TEMPLATE.items())

    def __str__(self):
        num_TEMPLATE = len(self.TEMPLATE)
        total_attributes = sum(len(s.attributes) for s in self.TEMPLATE.values())
        return f"{num_TEMPLATE} TEMPLATE, {total_attributes} attributes"

    def __repr__(self):
        """Representation of dscript object with additional properties."""
        repr_str = f"dscript object ({self.name})\n"
        # Add description, role, and version at the beginning
        repr_str += f"id: {self.userid}\n" if self.userid else ""
        repr_str += f"Descr: {self.description}\n" if self.description else ""
        repr_str += f"Role: {self.role} (v. {self.version})\n"
        repr_str += f'SECTIONS {span(self.SECTIONS,",","[","]")} | index: {self.section} | position: {self.position}\n'
        repr_str += f"\n\n\twith {len(self.TEMPLATE)} TEMPLATE"
        repr_str += "s" if len(self.TEMPLATE)>1 else ""
        repr_str += f" (with {len(self.DEFINITIONS)} DEFINITIONS)\n\n"
        # Add TEMPLATE information
        c = 0
        for k, s in self.TEMPLATE.items():
            head = f"|  idx: {c} |  key: {k}  |"
            dashes = (50 - len(head)) // 2
            repr_str += "-" * 50 + "\n"
            repr_str += f"{'<' * dashes}{head}{'>' * dashes}\n{repr(s)}\n"
            c += 1
        return repr_str

    def keys(self):
        """Return the keys of the TEMPLATE."""
        return self.TEMPLATE.keys()
    
    def values(self):
        """Return the ScriptTemplate objects in TEMPLATE."""
        return self.TEMPLATE.values()
    
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
        """
        Returns the content of the ScriptTemplate at the specified index.
        
        Parameters:
        -----------
        index : int
            The index of the template in the TEMPLATE dictionary.
        do : bool, optional (default=True)
            If True, the content will be processed based on conditions and evaluation flags.
        protected : bool, optional (default=True)
            Controls whether variable evaluation is protected (e.g., prevents overwriting certain definitions).
        
        Returns:
        --------
        str or list of str
            The content of the template after processing, or an empty string if conditions or evaluation flags block it.
        """
        key = list(self.TEMPLATE.keys())[index]
        s = self.TEMPLATE[key].content
        att = self.TEMPLATE[key].attributes        
        # Return an empty string if the facultative attribute is True and do is True
        if att["facultative"] and do:
            return ""
        # Evaluate the condition (if any)
        if att["condition"] is not None:
            cond = eval(self.DEFINITIONS.formateval(att["condition"], protected))
        else:
            cond = True
        # If the condition is met, process the content
        if cond:
            # Apply formateval only if the eval attribute is True and do is True
            if att["eval"] and do:
                if isinstance(s, list):
                    # Apply formateval to each item in the list if s is a list
                    return [self.DEFINITIONS.formateval(line, protected) for line in s]
                else:
                    # Apply formateval to the single string content
                    return self.DEFINITIONS.formateval(s, protected)
            else:
                return s  # Return the raw content if no evaluation is needed
        elif do:
            return ""  # Return an empty string if the condition is not met and do is True
        else:
            return s  # Return the raw content if do is False


    def get_attributes_by_index(self, index):
        """ Returns the attributes of the ScriptTemplate at the specified index."""
        key = list(self.TEMPLATE.keys())[index]
        return self.TEMPLATE[key].attributes
    
    
    def __add__(self, other):
        """
        Concatenates two dscript objects, creating a new dscript object that combines
        the TEMPLATE and DEFINITIONS of both. This operation avoids deep copying 
        of definitions by creating a new lambdaScriptdata instance from the definitions.
    
        Parameters:
        -----------
        other : dscript
            The other dscript object to concatenate with the current one.
    
        Returns:
        --------
        result : dscript
            A new dscript object with the concatenated TEMPLATE and merged DEFINITIONS.
    
        Raises:
        -------
        TypeError:
            If the other object is not an instance of dscript, script, pipescript
        """
        if isinstance(other, dscript):
            # Step 1: Merge global DEFINITIONS from both self and other
            result = dscript(name=self.name+"+"+other.name,**(self.DEFINITIONS + other.DEFINITIONS))
            # Step 2: Start by copying the TEMPLATE from self (no deepcopy for performance reasons)
            result.TEMPLATE = self.TEMPLATE.copy()
            # Step 3: Ensure that the local definitions for `self.TEMPLATE` are properly copied
            for key, value in self.TEMPLATE.items():
                result.TEMPLATE[key].definitions = lambdaScriptdata(**self.TEMPLATE[key].definitions)
            # Step 4: Track the next available index if keys need to be created
            next_index = len(result.TEMPLATE)
            # Step 5: Add items from the other dscript object, updating or generating new keys as needed
            for key, value in other.TEMPLATE.items():
                if key in result.TEMPLATE:
                    # If key already exists in result, assign a new unique index
                    while next_index in result.TEMPLATE:
                        next_index += 1
                    new_key = next_index
                else:
                    # Use the original key if it doesn't already exist
                    new_key = key
                # Copy the TEMPLATE's content and definitions from `other`
                result.TEMPLATE[new_key] = value
                # Merge the local TEMPLATE definitions from `other`
                result.TEMPLATE[new_key].definitions = lambdaScriptdata(**other.TEMPLATE[key].definitions)    
            return result
        elif isinstance(other,script):
            return self.script() + script
        elif isinstance(other,pipescript):
            return self.pipescript() | script
        else:
            raise TypeError(f"Cannot concatenate 'dscript' with '{type(other).__name__}'")

    
    def __call__(self, *keys):
        """
        Extracts subobjects from the dscript based on the provided keys.
    
        Parameters:
        -----------
        *keys : one or more keys that correspond to the `TEMPLATE` entries.
    
        Returns:
        --------
        A new `dscript` object that contains only the selected script lines/items, along with
        the relevant definitions and attributes from the original object.
        """
        # Create a new dscript object to store the extracted sub-objects
        result = dscript(name=f"{self.name}_subobject")
        # Copy the TEMPLATE entries corresponding to the provided keys
        for key in keys:
            if key in self.TEMPLATE:
                result.TEMPLATE[key] = self.TEMPLATE[key]
            else:
                raise KeyError(f"Key '{key}' not found in TEMPLATE.")
        # Copy the DEFINITIONS from the current object
        result.DEFINITIONS = copy.deepcopy(self.DEFINITIONS)
        # Copy other relevant attributes
        result.SECTIONS = self.SECTIONS[:]
        result.section = self.section
        result.position = self.position
        result.role = self.role
        result.description = self.description
        result.userid = self.userid
        result.version = self.version
        result.verbose = self.verbose
        result.printflag = self.printflag
    
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

    
    def do(self, printflag=None, verbose=None, softrun=False, return_definitions=False):
        """
        Executes or previews all `ScriptTemplate` instances in `TEMPLATE`, concatenating the results.
        Includes optional headers and footers based on verbosity settings and allows for a preliminary run with `softrun`.
        Can also return accumulated definitions across all templates if `return_definitions=True`.

        Parameters
        ----------
        printflag : bool, optional
            If `True`, enables print output during execution. If `None`, uses the instance's default print flag.
        verbose : bool, optional
            If `True`, includes headers and footers in the output. If `None`, uses the instance's verbosity setting.
        softrun : bool, optional
            If `True`, executes the script in a preliminary mode, bypassing full variable substitution for a preview
            of the content. If `False` (default), performs full processing of templates.
        return_definitions : bool, optional
            If `True`, returns a tuple where the second element contains all accumulated definitions across templates.
            Default is `False`, returning only the concatenated output.

        Returns
        -------
        str or tuple
            The concatenated output of all `ScriptTemplate` instances, including optional headers, footers,
            and execution summary details based on verbosity. If `return_definitions=True`, returns a tuple of
            (output, accumulated_definitions).

        Notes
        -----
        - Each `ScriptTemplate` in `TEMPLATE` is processed individually with its own `do()` method.
        - `softrun` allows for a preliminary content preview, which is useful for validating script structure or 
          gathering local definitions without substituting variables.
        - Verbose mode provides headers, footers, and a summary of processed and ignored items.
        """
        printflag = self.printflag if printflag is None else printflag
        verbose = self.verbose if verbose is None else verbose
        header = f"# --------------[ TEMPLATE \"{self.name}\" ]--------------" if verbose else ""
        footer = "# --------------------------------------------" if verbose else ""
        
        # Initialize output, counters, and optional definitions accumulator
        output = [header]
        non_empty_lines = 0
        ignored_lines = 0
        accumulated_definitions = lambdaScriptdata() if return_definitions else None
        
        for key, template in self.TEMPLATE.items():
            # Process each template with softrun if enabled, otherwise use full processing
            result = template.do(softrun=softrun)
            if result:
                # Apply comment removal based on verbosity
                final_result = result if verbose else remove_comments(result)
                output.append(final_result)
                non_empty_lines += 1
                
                # Accumulate definitions if return_definitions is enabled
                if return_definitions:
                    accumulated_definitions += template.definitions
            else:
                ignored_lines += 1

        # Add footer summary if verbose
        nel_word = 'items' if non_empty_lines > 1 else 'item'
        il_word = 'items' if ignored_lines > 1 else 'item'
        footer += f"\n# ---> Total {nel_word}: {non_empty_lines} - Ignored {il_word}: {ignored_lines}" if verbose else ""
        output.append(footer)
        
        # Concatenate output and determine return type based on return_definitions
        output_content = "\n".join(output)
        return (output_content, accumulated_definitions) if return_definitions else output_content


    
    def script(self,printflag=None,verbose=None,**USER):
        """
        returns the corresponding script
        """
        printflag = self.printflag if printflag is None else printflag
        verbose = self.verbose if verbose is None else verbose
        return lamdaScript(self,persistentfile=True, persistentfolder=None,
                           printflag=printflag, verbose=verbose,
                           **USER)
    
    def pipescript(self, *keys, printflag=None, verbose=None, **USER):
        """
        Returns a pipescript object by combining script objects corresponding to the given keys.
        
        Parameters:
        -----------
        *keys : one or more keys that correspond to the `TEMPLATE` entries.
        printflag : bool, optional
            Whether to enable printing of additional information.
        verbose : bool, optional
            Whether to run in verbose mode for debugging or detailed output.
        **USER : dict, optional
            Additional user-defined variables to pass into the script.
    
        Returns:
        --------
        A `pipescript` object that combines the script objects generated from the selected 
        dscript subobjects.
        """
        # Start with an empty pipescript
        # combined_pipescript = None
        # # Iterate over the provided keys to extract corresponding subobjects
        # for key in keys:
        #     # Extract the dscript subobject for the given key
        #     sub_dscript = self(key)
        #     # Convert the dscript subobject to a script object, passing USER, printflag, and verbose
        #     script_obj = sub_dscript.script(printflag=printflag, verbose=verbose, **USER)
        #     # Combine script objects into a pipescript object
        #     if combined_pipescript is None:
        #         combined_pipescript = pipescript(script_obj)  # Initialize pipescript
        #     else:
        #         combined_pipescript = combined_pipescript | script_obj  # Use pipe operator
        # if combined_pipescript is None:
        #     ValueError('The conversion to pipescript from {type{self}} falled')
        # return combined_pipescript
        combined_pipescript = None
        
        # Loop over all keys in TEMPLATE and combine them
        for key in self.keys():
            # Create a new dscript object with only the current key in TEMPLATE
            focused_dscript = dscript(name=f"{self.name}:{key}")
            focused_dscript.TEMPLATE[key] = self.TEMPLATE[key]
            focused_dscript.TEMPLATE[key].definitions = scriptdata(self.TEMPLATE[key].definitions)
            focused_dscript.DEFINITIONS = scriptdata(**self.DEFINITIONS)
            focused_dscript.SECTIONS = self.SECTIONS[:]
            focused_dscript.section = self.section
            focused_dscript.position = self.position
            focused_dscript.role = self.role
            focused_dscript.description = self.description
            focused_dscript.userid = self.userid
            focused_dscript.version = self.version
            focused_dscript.verbose = self.verbose
            focused_dscript.printflag = self.printflag
    
            # Convert the focused dscript object to a script object
            script_obj = focused_dscript.script(printflag=printflag, verbose=verbose, **USER)
    
            # Combine the script objects into a pipescript object using the pipe operator
            if combined_pipescript is None:
                combined_pipescript = pipescript(script_obj)  # Initialize pipescript
            else:
                combined_pipescript = combined_pipescript | pipescript(script_obj)  # Use pipe operator
    
        if combined_pipescript is None:
            ValueError('The conversion to pipescript from {type{self}} falled')
        return combined_pipescript



    # Generator -- added on 2024-10-17
    # -----------
    def generator(self):
        """
        Returns
        -------
        STR
            generated code corresponding to dscript (using dscript syntax/language).

        """
        return self.save(generatoronly=True)


    # Save Method -- added on 2024-09-04
    # -----------
    def save(self, filename=None, foldername=None, overwrite=False, generatoronly=False, onlyusedvariables=True):
        """
        Save the current script instance to a text file.
    
        Parameters
        ----------
        filename : str, optional
            The name of the file to save the script to. If not provided, `self.name` is used.
            The extension ".txt" is automatically appended if not included.
    
        foldername : str, optional
            The directory where the file will be saved. If not provided, it defaults to the system's
            temporary directory. If the filename does not include a full path, this folder will be used.
    
        overwrite : bool, default=True
            Whether to overwrite the file if it already exists. If set to False, an exception is raised
            if the file exists.
    
        generatoronly : bool, default=False
            If True, the method returns the generated content string without saving to a file.
    
        onlyusedvariables : bool, default=True
            If True, local definitions are only saved if they are used within the template content. 
            If False, all local definitions are saved, regardless of whether they are referenced in 
            the template.
    
        Raises
        ------
        FileExistsError
            If the file already exists and `overwrite` is set to False.
    
        Notes
        -----
        - The script is saved in a plain text format, and each section (global parameters, definitions,
          template, and attributes) is written in a structured format with appropriate comments.
        - If `self.name` is used as the filename, it must be a valid string that can serve as a file name.
        - The file structure follows the format:
            # DSCRIPT SAVE FILE
            # generated on YYYY-MM-DD on user@hostname
            
            # GLOBAL PARAMETERS
            { ... }
            
            # DEFINITIONS (number of definitions=...)
            key=value
            
            # TEMPLATES (number of items=...)
            key: template_content
            
            # ATTRIBUTES (number of items with explicit attributes=...)
            key:{attr1=value1, attr2=value2, ...}
        """
        # At the beginning of the save method
        start_time = time.time()  # Start the timer
        
        if not generatoronly:
            # Use self.name if filename is not provided
            if filename is None:
                filename = span(self.name, sep="\n")
            
            # Ensure the filename ends with '.txt'
            if not filename.endswith('.txt'):
                filename += '.txt'
            
            # Construct the full path
            if foldername in [None, ""]:  # Handle cases where foldername is None or an empty string
                filepath = os.path.abspath(filename)
            else:
                filepath = os.path.join(foldername, filename)
            
            # Check if the file already exists, and raise an exception if it does and overwrite is False
            if os.path.exists(filepath) and not overwrite:
                raise FileExistsError(f"The file '{filepath}' already exists.")
    
        # Header with current date, username, and host
        user = getpass.getuser()
        host = socket.gethostname()
        date = datetime.now().strftime('%Y-%m-%d')
        header = f"# DSCRIPT SAVE FILE\n# generated on {date} on {user}@{host}\n"
        if generatoronly:
            header += 'dynamic code generation (no file)\n'
        else:
            header += f'\n#\tname = "{self.name}"\n'
            header += f'\n#\tpath = "{filepath}"\n\n'
        
        # Global parameters in strict Python syntax
        global_params = "# GLOBAL PARAMETERS (8 parameters)\n"
        global_params += "{\n"
        global_params += f"    SECTIONS = {self.SECTIONS},\n"
        global_params += f"    section = {self.section},\n"
        global_params += f"    position = {self.position},\n"
        global_params += f"    role = {self.role!r},\n"
        global_params += f"    description = {self.description!r},\n"
        global_params += f"    userid = {self.userid!r},\n"
        global_params += f"    version = {self.version},\n"
        global_params += f"    verbose = {self.verbose}\n"
        global_params += "}\n"
        
        # Initialize definitions with self.DEFINITIONS
        allvars = self.DEFINITIONS
    
        # Temporary dictionary to track global variable information
        global_var_info = {}
    
        # Loop over each template item to detect and record variable usage and overrides
        # Loop over each template item to detect and record variable usage and overrides
        for template_index, (key, script_template) in enumerate(self.TEMPLATE.items()):
            # Detect variables used in this template
            used_variables = script_template.detect_variables()
        
            # Check each variable used in this template
            for var in used_variables:
                # Determine if the variable is defined in global_var_info and initialize tracking if not
                if var not in global_var_info:
                    global_value = getattr(allvars, var, None)
                    local_value = getattr(script_template.definitions, var, None)
                    is_global = var in allvars  # Flag to track if the variable was originally global
                    is_default = is_global and (
                        global_value is None or global_value == "" or global_value == f"${{{var}}}"
                    )
        
                    # Initialize tracking information
                    global_var_info[var] = {
                        "value": global_value,       # Initial value from allvars if exists
                        "is_default": is_default,    # Check if it’s set to a default value
                        "first_use": template_index, # First time the variable is used in a template
                        "override_index": template_index if is_global and local_value != global_value else None,
                        "is_global": is_global       # Track if the variable originates as global
                    }
                else:
                    # Update the override_index only if it's not set and the local value differs from global
                    global_value = global_var_info[var]["value"]
                    local_value = getattr(script_template.definitions, var, None)
                    
                    if (
                        global_var_info[var]["override_index"] is None  # Ensure we only set the first override
                        and local_value != global_value  # Local value must differ from global
                    ):
                        global_var_info[var]["override_index"] = template_index
        
        # Prepare the global definitions for output, filtering based on usage and overrides
        # Count only global values that meet criteria for being printed
        filtered_globals = {
            var: info for var, info in global_var_info.items()
            if info["is_global"] and info["first_use"] is not None and (
                info["override_index"] is None or info["first_use"] < info["override_index"]
            )
        }
        
        # Generate the definitions output based on filtered globals
        definitions = f"\n# GLOBAL DEFINITIONS (number of definitions={len(filtered_globals)})\n"
        for var, info in filtered_globals.items():
            if info["is_default"]:
                definitions += f"{var} = ${{{var}}}  # value assumed to be defined outside this DSCRIPT file\n"
            else:
                value = info["value"]
                if value in ["", None]:
                    definitions += f'{var} = ""\n'
                elif isinstance(value, str):
                    safe_value = value.replace('\\', '\\\\').replace('\n', '\\n')
                    definitions += f"{var} = {safe_value}\n"
                else:
                    definitions += f"{var} = {value}\n"

        # Template (number of lines/items)
        printsinglecontent = False
        template = f"\n# TEMPLATES (number of items={len(self.TEMPLATE)})\n"
        for key, script_template in self.TEMPLATE.items():
            # Get local template definitions and detected variables
            template_vars = script_template.definitions
            used_variables = script_template.detect_variables()
            islocal = False
            # Temporary dictionary to accumulate variables to add to allvars
            valid_local_vars = lambdaScriptdata()
            # Write template-specific definitions only if they meet the updated conditions
            for var in template_vars.keys():
                # Conditions for adding a variable to the local template and to `allvars`
                if (var in used_variables or not onlyusedvariables) and (
                    script_template.is_variable_set_value_only(var) and
                    (var not in allvars or getattr(template_vars, var) != getattr(allvars, var))
                ):
                    # Start local definitions section if this is the first local variable for the template
                    if not islocal:
                        template += f"\n# LOCAL DEFINITIONS for key '{key}'\n"
                        islocal = True
                    # Retrieve and process the variable value
                    value = getattr(template_vars, var)
                    if value in ["", None]:
                        template += f'{var} = ""\n'  # Set empty or None values as ""
                    elif isinstance(value, str):
                        safe_value = value.replace('\\', '\\\\').replace('\n', '\\n')
                        template += f"{var} = {safe_value}\n"
                    else:
                        template += f"{var} = {value}\n"
                    # Add the variable to valid_local_vars for selective update of allvars
                    valid_local_vars.setattr(var, value)
            # Update allvars only with filtered, valid local variables
            allvars += valid_local_vars
    
            # Write the template content
            if isinstance(script_template.content, list):
                if len(script_template.content) == 1:
                    # Single-line template saved as a single line
                    content_str = script_template.content[0].strip()
                    template += "" if printsinglecontent else "\n"
                    template += f"{key}: {content_str}\n"
                    printsinglecontent = True
                else:
                    content_str = '\n    '.join(script_template.content)
                    template += f"\n{key}: [\n    {content_str}\n ]\n"
                    printsinglecontent = False
            else:
                template += "" if printsinglecontent else "\n"
                template += f"{key}: {script_template.content}\n"
                printsinglecontent = True
    
        # Attributes (number of lines/items with explicit attributes)
        attributes = f"# ATTRIBUTES (number of items with explicit attributes={len(self.TEMPLATE)})\n"
        for key, script_template in self.TEMPLATE.items():
            attr_str = ", ".join(f"{attr_name}={repr(attr_value)}"
                                 for attr_name, attr_value in script_template.attributes.items())
            attributes += f"{key}:{{{attr_str}}}\n"
        
        # Combine all sections into one content
        content = header + "\n" + global_params + "\n" + definitions + "\n" + template + "\n" + attributes + "\n"
        
        # Append footer information to the content
        non_empty_lines = sum(1 for line in content.splitlines() if line.strip())  # Count non-empty lines
        execution_time = time.time() - start_time  # Calculate the execution time in seconds        
        footer = f"\n# Footer: Non-empty lines of content = {non_empty_lines}\n"
        footer += f"# Execution time (seconds): {execution_time:.4f}\n"
        content += footer  # Add the footer to the content
        
        if generatoronly:
            return content
        else:
            # Write the content to the file
            with open(filepath, 'w') as f:
                f.write(content)        
            print(f"\nScript saved to {filepath}")
            return filepath

        
        
    # Write Method -- added on 2024-09-05
    # ------------
    @staticmethod
    def write(scriptcontent, filename=None, foldername=None, overwrite=False):
        """
        Writes the provided script content to a specified file in a given folder, with a header if necessary.
    
        Parameters
        ----------
        scriptcontent : str
            The content to be written to the file.
        
        filename : str, optional
            The name of the file. If not provided, `self.name` will be used. The extension `.txt` will be appended if not already present.
        
        foldername : str, optional
            The folder where the file will be saved. If not provided, the system's temporary directory is used.
        
        overwrite : bool, optional
            If False (default), raises a `FileExistsError` if the file already exists. If True, the file will be overwritten if it exists.
    
        Raises
        ------
        FileExistsError
            If the file already exists and `overwrite` is set to False.
        
        Notes
        -----
        - The first line of the file will be a header (`# DSCRIPT SAVE FILE`). If this header does not already exist in `scriptcontent`, it will be added.
        - The header also includes the current date, username, hostname, the value of `self.name`, and the full file path.
        """
    
        # Generate a random name if filename is not provided
        if filename is None:
            filename = autoname(8)  # Generates a random name of 8 letters
    
        # Ensure the filename ends with '.txt'
        if not filename.endswith('.txt'):
            filename += '.txt'
    
        # Handle foldername and relative paths
        if foldername is None or foldername == "":
            # If foldername is empty or None, use current working directory for relative paths
            if not os.path.isabs(filename):
                filepath = os.path.join(os.getcwd(), filename)
            else:
                filepath = filename  # If filename is absolute, use it directly
        else:
            # If foldername is provided and filename is not absolute, use foldername
            if not os.path.isabs(filename):
                filepath = os.path.join(foldername, filename)
            else:
                filepath = filename
    
        # Check if file already exists, raise exception if it does and overwrite is False
        if os.path.exists(filepath) and not overwrite:
            raise FileExistsError(f"The file '{filepath}' already exists.")
    
        # Prepare header if not already present
        if not scriptcontent.startswith("# DSCRIPT SAVE FILE"):
            fname = os.path.basename(filepath)  # Extracts the filename (e.g., "myscript.txt")
            name, _ = os.path.splitext(fname)   # Removes the extension, e.g., "myscript
            user = getpass.getuser()
            host = socket.gethostname()
            date = datetime.now().strftime('%Y-%m-%d')
            header = f"# DSCRIPT SAVE FILE\n# written on {date} by {user}@{host}\n"
            header += f'\n#\tname = "{name}"\n'
            header += f'\n#\tpath = "{filepath}"\n\n'
            scriptcontent = header + scriptcontent
    
        # Write the content to the file
        with open(filepath, 'w') as file:
            file.write(scriptcontent)
    
        return filepath   


    # Load Method and its Parsing Rules -- added on 2024-09-04
    # ---------------------------------
    @classmethod
    def load(cls, filename, foldername=None, numerickeys=True):
        """
        Load a script instance from a text file.
    
        Parameters
        ----------
        filename : str
            The name of the file to load the script from. If the filename does not end with ".txt",
            the extension is automatically appended.
        
        foldername : str, optional
            The directory where the file is located. If not provided, it defaults to the system's
            temporary directory. If the filename does not include a full path, this folder will be used.
    
        numerickeys : bool, default=True
            If True, numeric string keys in the template section are automatically converted into integers.
            For example, the key "0" would be converted into the integer 0.
    
        Returns
        -------
        dscript
            A new `dscript` instance populated with the content of the loaded file.
    
        Raises
        ------
        ValueError
            If the file does not start with the correct DSCRIPT header or the file format is invalid.
        
        FileNotFoundError
            If the specified file does not exist.
    
        Notes
        -----
        - The file is expected to follow the same structured format as the one produced by the `save()` method.
        - The method processes global parameters, definitions, template lines/items, and attributes. If the file
          includes numeric keys as strings (e.g., "0", "1"), they can be automatically converted into integers
          if `numerickeys=True`.
        - The script structure is dynamically rebuilt, and each section (global parameters, definitions,
          template, and attributes) is correctly parsed and assigned to the corresponding parts of the `dscript`
          instance.
        """
        
        # Step 0 validate filepath
        if not filename.endswith('.txt'):
            filename += '.txt'
        
        # Handle foldername and relative paths
        if foldername is None or foldername == "":
            # If the foldername is empty or None, use current working directory for relative paths
            if not os.path.isabs(filename):
                filepath = os.path.join(os.getcwd(), filename)
            else:
                filepath = filename  # If filename is absolute, use it directly
        else:
            # If foldername is provided and filename is not absolute, use foldername
            if not os.path.isabs(filename):
                filepath = os.path.join(foldername, filename)
            else:
                filepath = filename
        
        if not os.path.exists(filepath):
            raise FileExistsError(f"The file '{filepath}' does not exist.")
        
        # Read the file contents
        with open(filepath, 'r') as f:
            content = f.read()
    
        # Call parsesyntax to parse the file content
        fname = os.path.basename(filepath)  # Extracts the filename (e.g., "myscript.txt")
        name, _ = os.path.splitext(fname)   # Removes the extension, e.g., "myscript
        return cls.parsesyntax(content, name, numerickeys)
    


    # Load Method and its Parsing Rules -- added on 2024-09-04
    # ---------------------------------
    @classmethod
    def parsesyntax(cls, content, name=None, numerickeys=True, verbose=False, authentification=True):
        """
        Parse a DSCRIPT script from a string content.
    
        Parameters
        ----------
        content : str
            The string content of the DSCRIPT script to be parsed.
    
        name : str, optional
            The name of the dscript project. If `None`, a random name is generated.
    
        numerickeys : bool, default=True
            If `True`, numeric string keys in the template section are automatically converted into integers.
    
        verbose : bool, default=False
            If `True`, the parser will output warnings for unrecognized lines outside of blocks.
            
        authentification : bool, default=True
            If `True`, the parser is expected that the first non empty line is # DSCRIPT SAVE FILE
    
        Returns
        -------
        dscript
            A new `dscript` instance populated with the content of the loaded file.
    
        Raises
        ------
        ValueError
            If content does not start with the correct DSCRIPT header or the file format is invalid.
    
        Notes
        -----
        **DSCRIPT SAVE FILE FORMAT**
    
        This script syntax is designed for creating dynamic and customizable input files, where variables, templates, 
        and control attributes can be defined in a flexible manner.
    
        **Mandatory First Line:**
    
        Every DSCRIPT file must begin with the following line:
    
        ```plaintext
        # DSCRIPT SAVE FILE
        ```
    
        **Structure Overview:**
    
        1. **Global Parameters Section (Optional):**
    
            - This section defines global script settings, enclosed within curly braces `{}`.
            - Properties include:
                - `SECTIONS`: List of section names to be considered (e.g., `["DYNAMIC"]`).
                - `section`: Current section index (e.g., `0`).
                - `position`: Current script position in the order.
                - `role`: Defines the role of the script instance (e.g., `"dscript instance"`).
                - `description`: A short description of the script (e.g., `"dynamic script"`).
                - `userid`: Identifier for the user (e.g., `"dscript"`).
                - `version`: Script version (e.g., `0.1`).
                - `verbose`: Verbosity flag, typically a boolean (e.g., `False`).
    
            **Example:**
    
            ```plaintext
            {
                SECTIONS = ['INITIALIZATION', 'SIMULATION']  # Global script parameters
            }
            ```
    
        2. **Definitions Section:**
    
            - Variables are defined in Python-like syntax, allowing for dynamic variable substitution.
            - Variables can be numbers, strings, or lists, and they can include placeholders using `$` 
              to delay execution or substitution.
    
            **Example:**
    
            ```plaintext
            d = 3                               # Define a number
            periodic = "$p"                     # '$' prevents immediate evaluation of 'p'
            units = "$metal"                    # '$' prevents immediate evaluation of 'metal'
            dimension = "${d}"                  # Variable substitution
            boundary = ['p', 'p', 'p']          # List with a mix of variables and values
            atom_style = "$atomic"              # String variable with delayed evaluation
            ```
    
        3. **Templates Section:**
    
            - This section provides a mapping between keys and their corresponding commands or instructions.
            - The templates reference variables defined in the **Definitions** section or elsewhere.
            - **Syntax:**
    
                ```plaintext
                KEY: INSTRUCTION
                ```
    
                where:
                - `KEY` can be numeric or alphanumeric.
                - `INSTRUCTION` represents a command template, often referring to variables using `${variable}` notation.
    
            **Example:**
    
            ```plaintext
            units: units ${units}               # Template uses the 'units' variable
            dim: dimension ${dimension}         # Template for setting the dimension
            bound: boundary ${boundary}         # Template for boundary settings
            lattice: lattice ${lattice}         # Lattice template
            ```
    
        4. **Attributes Section:**
    
            - Each template line can have customizable attributes to control behavior and conditions.
            - Default attributes include:
                - `facultative`: If `True`, the line is optional and can be removed if needed.
                - `eval`: If `True`, the line will be evaluated with Python's `eval()` function.
                - `readonly`: If `True`, the line cannot be modified later in the script.
                - `condition`: An expression that must be satisfied for the line to be included.
                - `condeval`: If `True`, the condition will be evaluated using `eval()`.
                - `detectvar`: If `True`, this creates variables in the **Definitions** section if they do not exist.
    
            **Example:**
    
            ```plaintext
            units: {facultative=False, eval=False, readonly=False, condition="${units}", condeval=False, detectvar=True}
            dim: {facultative=False, eval=False, readonly=False, condition=None, condeval=False, detectvar=True}
            ```
    
        **Note on Multiple Definitions**
    
        This example demonstrates how variables defined in the **Definitions** section are handled for each template.
        Each template retains its own snapshot of the variable definitions at the time it is created, ensuring that templates
        can use different values for the same variable if redefined.
    
        **Example:**
    
        ```plaintext
        # DSCRIPT SAVE FILE
    
        # Definitions
        var = 10
    
        # Template key1
        key1: Template content with ${var}
    
        # Definitions
        var = 20
    
        # Template key2
        key2: Template content with ${var}
    
        # Template key3
        key3:[
            this is an undefined variable ${var31}
            this is another undefined variable ${var32}
            this variable is defined  ${var}
        ]
        ```
    
        **Parsing and Usage:**
    
        ```python
        # Parse content using parsesyntax()
        ds = dscript.parsesyntax(content)
    
        # Accessing templates and their variables
        print(ds.TEMPLATE['key1'].text)  # Output: Template content with 10
        print(ds.TEMPLATE['key2'].text)  # Output: Template content with 20
        ```
    
        **Handling Undefined Variables:**
    
        Variables like `${var31}` and `${var32}` in `key3` are undefined. The parser will handle them based on your substitution logic or raise an error if they are required.
    
        **Important Notes:**
    
        - The parser processes the script sequentially. Definitions must appear before the templates that use them.
        - Templates capture the variable definitions at the time they are parsed. Redefining a variable affects only subsequent templates.
        - Comments outside of blocks are allowed and ignored by the parser.
        - Content within templates is treated as-is, allowing for any syntax required by the target system (e.g., LAMMPS commands).
        
        
    **Advanced Example**

        Here's a more advanced example demonstrating the use of global definitions, local definitions, templates, and how to parse and render the template content.
    
        ```python
        content = '''
            # GLOBAL DEFINITIONS
            dumpfile = $dump.LAMMPS
            dumpdt = 50
            thermodt = 100
            runtime = 5000
    
            # LOCAL DEFINITIONS for step '0'
            dimension = 3
            units = $si
            boundary = ['f', 'f', 'f']
            atom_style = $smd
            atom_modify = ['map', 'array']
            comm_modify = ['vel', 'yes']
            neigh_modify = ['every', 10, 'delay', 0, 'check', 'yes']
            newton = $off
            name = $SimulationBox
    
            # This is a comment line outside of blocks
            # ------------------------------------------
    
            0: [    % --------------[ Initialization Header (helper) for "${name}" ]--------------
                # set a parameter to None or "" to remove the definition
                dimension    ${dimension}
                units        ${units}
                boundary     ${boundary}
                atom_style   ${atom_style}
                atom_modify  ${atom_modify}
                comm_modify  ${comm_modify}
                neigh_modify ${neigh_modify}
                newton       ${newton}
                # ------------------------------------------
             ]
        '''
        # Parse the content
        ds = dscript.parsesyntax(content, verbose=True, authentification=False)
    
        # Access and print the rendered template
        print("Template 0 content:")
        print(ds.TEMPLATE[0].do())
        ```
    
        **Explanation:**
    
        - **Global Definitions:** Define variables that are accessible throughout the script.
        - **Local Definitions for Step '0':** Define variables specific to a particular step or template.
        - **Template Block:** Identified by `0: [ ... ]`, it contains the content where variables will be substituted.
        - **Comments:** Lines starting with `#` are comments and are ignored by the parser outside of template blocks.
    
        **Expected Output:**
    
        ```
        Template 0 content:
        # --------------[ Initialization Header (helper) for "SimulationBox" ]--------------
        # set a parameter to None or "" to remove the definition
        dimension    3
        units        si
        boundary     ['f', 'f', 'f']
        atom_style   smd
        atom_modify  ['map', 'array']
        comm_modify  ['vel', 'yes']
        neigh_modify ['every', 10, 'delay', 0, 'check', 'yes']
        newton       off
        # ------------------------------------------
        ```
    
        **Notes:**
    
        - The `do()` method renders the template, substituting variables with their defined values.
        - Variables like `${dimension}` are replaced with their corresponding values defined in the local or global definitions.
        - The parser handles comments and blank lines appropriately, ensuring they don't interfere with the parsing logic.

        
        """

        # Split the content into lines
        lines = content.splitlines()
        if not lines:
            raise ValueError("File/Content is empty or only contains blank lines.")
    
        # Initialize containers
        global_params = {}
        definitions = lambdaScriptdata()
        template = {}
        attributes = {}
    
        # State variables
        inside_global_params = False
        global_params_content = ""
        inside_template_block = False
        current_template_key = None
        current_template_content = []
    
        # Step 1: Authenticate the file
        if authentification:
            auth_line_found = False
            max_header_lines = 10
            for idx, line in enumerate(lines[:max_header_lines]):
                stripped_line = line.strip()
                if not stripped_line:
                    continue
                if stripped_line.startswith("# DSCRIPT SAVE FILE"):
                    auth_line_found = True
                    header_end_idx = idx
                    break
                elif stripped_line.startswith("#") or stripped_line.startswith("%"):
                    continue
                else:
                    raise ValueError(f"Unexpected content before authentication line (# DSCRIPT SAVE FILE) at line {idx + 1}:\n{line}")
            if not auth_line_found:
                raise ValueError("File/Content is not a valid DSCRIPT file.")
    
            # Remove header lines
            lines = lines[header_end_idx + 1:]
    
            # Initialize line number
            line_number = header_end_idx + 1
            last_successful_line = line_number - 1
        else:
            # No authentication required
            line_number = 0  # Start from the first line
            last_successful_line = 0
    
        # Process each line
        for idx, line in enumerate(lines):
            line_number += 1  # Increment line number at the start
            line_content = line.rstrip('\n')
    
            # Remove trailing comments
            stripped_no_comments = remove_comments(line_content)
    
            # Ignore empty lines
            if not stripped_no_comments.strip():
                continue
    
            # If the original line is a comment line, skip it
            if line_content.strip().startswith("#") or line_content.strip().startswith("%"):
                continue
    
            stripped = stripped_no_comments.strip()
    
            # Handle template blocks
            if inside_template_block:
                if stripped == ']':
                    # End of the template block
                    content = '\n'.join(current_template_content)
                    template[current_template_key] = ScriptTemplate(
                        content,
                        definitions=lambdaScriptdata(**definitions.__dict__),
                        verbose=verbose,
                        userid=current_template_key)
                    template[current_template_key].refreshvar()
                    inside_template_block = False
                    current_template_key = None
                    current_template_content = []
                    last_successful_line = line_number
                else:
                    # Accumulate all lines, including comments and indentation
                    current_template_content.append(line_content)
                continue
    
            # Handle global parameters inside {...}
            if inside_global_params:
                global_params_content += ' ' + stripped
                if '}' in stripped:
                    inside_global_params = False
                    # Parse the global parameters
                    cls._parse_global_params(global_params_content.strip(), global_params)
                    global_params_content = ""
                    last_successful_line = line_number
                continue
    
            # Handle start of global parameters
            if stripped.startswith('{') and not inside_global_params:
                if '}' in stripped:
                    # Single-line global parameters
                    global_params_content = stripped
                    cls._parse_global_params(global_params_content.strip(), global_params)
                    global_params_content = ""
                    last_successful_line = line_number
                else:
                    # Multi-line global parameters
                    inside_global_params = True
                    global_params_content = stripped
                continue
    
            # Handle attributes
            attribute_match = re.match(r'^(\w+)\s*:\s*\{(.+)\}', stripped)
            if attribute_match:
                key, attr_content = attribute_match.groups()
                attributes[key] = {}
                cls._parse_attributes(attributes[key], attr_content.strip())
                last_successful_line = line_number
                continue
    
            # Handle start of template block
            template_block_match = re.match(r'^(\w+)\s*:\s*\[', stripped)
            if template_block_match:
                current_template_key = template_block_match.group(1)
                # Check if the line ends with ']'
                if stripped.endswith(']'):
                    # Single-line template block
                    content_inside_brackets = stripped[stripped.index('[') + 1:stripped.rindex(']')].strip()
                    template[current_template_key] = ScriptTemplate(
                        content_inside_brackets,
                        definitions=lambdaScriptdata(**definitions.__dict__),
                        verbose=verbose,
                        userid=current_template_key)
                    template[current_template_key].refreshvar()
                    current_template_key = None
                    last_successful_line = line_number
                else:
                    # Multi-line template block
                    remainder = line_content[line_content.index('[') + 1:]
                    current_template_content = [remainder]
                    inside_template_block = True
                continue
    
            # Handle definitions
            definition_match = re.match(r'^(\w+)\s*=\s*(.+)', stripped)
            if definition_match:
                key, value = definition_match.groups()
                definitions.setattr(key, cls._convert_value(value))
                last_successful_line = line_number
                continue
    
            # Handle single-line templates
            template_match = re.match(r'^(\w+)\s*:\s*(.+)', stripped)
            if template_match:
                key, content = template_match.groups()
                template[key] = ScriptTemplate(
                    content.strip(),
                    definitions=lambdaScriptdata(**definitions.__dict__),
                    verbose=verbose,
                    userid=key)
                template[key].refreshvar()
                last_successful_line = line_number
                continue
    
            # Unrecognized line
            if verbose:
                print(f"Warning: Unrecognized line at {line_number}: {line_content}")
            last_successful_line = line_number  # Update last successful line even if we skip
            continue
    
        # Apply attributes to templates
        for key in attributes:
            if key in template:
                for attr_name, attr_value in attributes[key].items():
                    setattr(template[key], attr_name, attr_value)
            else:
                raise ValueError(f"Attributes found for undefined template key: {key}")
    
        # Create and return new instance
        if name is None:
            name = autoname(8)
        instance = cls(
            name=name,
            SECTIONS=global_params.get('SECTIONS', ['DYNAMIC']),
            section=global_params.get('section', 0),
            position=global_params.get('position', 0),
            role=global_params.get('role', 'dscript instance'),
            description=global_params.get('description', 'dynamic script'),
            userid=global_params.get('userid', 'dscript'),
            version=global_params.get('version', 0.1),
            verbose=global_params.get('verbose', False)
        )
    
        # Convert numeric string keys to integers if numerickeys is True
        if numerickeys:
            numeric_template = {}
            for key, value in template.items():
                if key.isdigit():
                    numeric_template[int(key)] = value
                else:
                    numeric_template[key] = value
            template = numeric_template
    
        # Set definitions and template
        instance.DEFINITIONS = definitions
        instance.TEMPLATE = template
    
        # Refresh variables
        instance.set_all_variables()
    
        # Check variables
        instance.check_all_variables(verbose=False)
    
        # Return the new instance
        return instance
    
    
    @classmethod
    def parsesyntax_legacy(cls, content, name=None, numerickeys=True):
        """
        Parse a script from a string content.
        [ ------------------------------------------------------]
        [ Legacy parsesyntax method for backward compatibility. ]
        [ ------------------------------------------------------]
    
        Parameters
        ----------
        content : str
            The string content of the script to be parsed.
        
        name : str
            The name of the dscript project (if None, it is set randomly)
        
        numerickeys : bool, default=True
            If True, numeric string keys in the template section are automatically converted into integers.

        Returns
        -------
        dscript
            A new `dscript` instance populated with the content of the loaded file.
    
        Raises
        ------
        ValueError
            If content does not start with the correct DSCRIPT header or the file format is invalid.
            
        Notes
        -----
        - The file is expected to follow the same structured format as the one produced by the `save()` method.
        - The method processes global parameters, definitions, template lines/items, and attributes. If the file
          includes numeric keys as strings (e.g., "0", "1"), they can be automatically converted into integers
          if `numerickeys=True`.
        - The script structure is dynamically rebuilt, and each section (global parameters, definitions,
          template, and attributes) is correctly parsed and assigned to the corresponding parts of the `dscript`
          instance.
          
          
        PIZZA.DSCRIPT SAVE FILE FORMAT
        -------------------------------
        This script syntax is designed for creating dynamic and customizable input files, where variables, templates, 
        and control attributes can be defined in a flexible manner. 
        
        ### Mandatory First Line:
        Every DSCRIPT file must begin with the following line:
            # DSCRIPT SAVE FILE
        
        ### Structure Overview:
        
        1. **Global Parameters Section (Optional):**
            - This section defines global script settings, enclosed within curly braces `{ }`.
            - Properties include:
                - `SECTIONS`: List of section names to be considered (e.g., `["DYNAMIC"]`).
                - `section`: Current section index (e.g., `0`).
                - `position`: Current script position in the order.
                - `role`: Defines the role of the script instance (e.g., `"dscript instance"`).
                - `description`: A short description of the script (e.g., `"dynamic script"`).
                - `userid`: Identifier for the user (e.g., `"dscript"`).
                - `version`: Script version (e.g., `0.1`).
                - `verbose`: Verbosity flag, typically a boolean (e.g., `False`).
        
            Example:
            ```
            {
                SECTIONS = ['INITIALIZATION', 'SIMULATION']  # Global script parameters
            }
            ```
        
        2. **Definitions Section:**
            - Variables are defined in Python-like syntax, allowing for dynamic variable substitution.
            - Variables can be numbers, strings, or lists, and they can include placeholders using `$` 
              to delay execution or substitution.
        
            Example:
            ```
            d = 3                               # Define a number
            periodic = "$p"                     # '$' prevents immediate evaluation of 'p'
            units = "$metal"                    # '$' prevents immediate evaluation of 'metal'
            dimension = "${d}"                  # Variable substitution
            boundary = ['p', 'p', 'p']  # List with a mix of variables and values
            atom_style = "$atomic"              # String variable with delayed evaluation
            ```
        
        3. **Templates Section:**
            - This section provides a mapping between keys and their corresponding commands or instructions. 
            - The templates reference variables defined in the **Definitions** section or elsewhere. 
            - Syntax: 
                ```
                KEY: INSTRUCTION
                ```
                where:
                - `KEY` can be numeric or alphanumeric.
                - `INSTRUCTION` represents a command template, often referring to variables using `${variable}` notation.
        
            Example:
            ```
            units: units ${units}               # Template uses the 'units' variable
            dim: dimension ${dimension}         # Template for setting the dimension
            bound: boundary ${boundary}         # Template for boundary settings
            lattice: lattice ${lattice}         # Lattice template
            ```
        
        4. **Attributes Section:**
            - Each template line can have customizable attributes to control behavior and conditions.
            - Default attributes include:
                - `facultative`: If `True`, the line is optional and can be removed if needed.
                - `eval`: If `True`, the line will be evaluated with Python's `eval()` function.
                - `readonly`: If `True`, the line cannot be modified later in the script.
                - `condition`: An expression that must be satisfied for the line to be included.
                - `condeval`: If `True`, the condition will be evaluated using `eval()`.
                - `detectvar`: If `True`, this creates variables in the **Definitions** section if they do not exist.
        
            Example:
            ```
            units: {facultative=False, eval=False, readonly=False, condition="${units}", condeval=False, detectvar=True}
            dim: {facultative=False, eval=False, readonly=False, condition=None, condeval=False, detectvar=True}
            ```
            
        Note on multiple definitions
        -----------------------------
        This example demonstrates how variables defined in the `Definitions` section are handled for each template.
        Each template retains its own snapshot of the variable definitions at the time it is created, ensuring that templates
        can use different values for the same variable if redefined.
        
        content = "" "
        # DSCRIPT SAVE FILE
        
        # Definitions
        var = 10
        
        # Template ky1
        key1: Template content with ${var}
        
        # Definitions
        var = 20
        
        # Template key2
        key2: Template content with ${var}
        
        # Template key3
        key3:[
            this is an underfined variable ${var31}
            this is an another underfined variable ${var32}
            this variables is defined  ${var}
            ]
        
        "" "
        
        # Parse content using parsesyntax()
        ds = dscript.parsesyntax(content)
        
        # Key1 should use the first definition of 'var' (10)
        print(ds.key1.definitions.var)  # Output: Template content with 10

        # Key2 should use the updated definition of 'var' (20)
        print(ds.key2.definitions.var)  # Output: Template content with 10
            
        
        """
        
        # Split the content into lines
        lines = content.splitlines()
        lines = [line for line in lines if line.strip()]  # Remove blank or empty lines
        # Raise an error if no content is left after removing blank lines
        if not lines:
            raise ValueError("File/Content is empty or only contains blank lines.")

        # Initialize containers for global parameters, definitions, templates, and attributes
        global_params = {}
        definitions = lambdaScriptdata()
        template = {}
        attributes = {}

        # State variables to handle multi-line global parameters and attributes
        inside_global_params = False
        inside_attributes = False
        current_attr_key = None  # Ensure this is properly initialized
        global_params_content = ""
        inside_template_block = False  # Track if we are inside a multi-line template
        current_template_key = None    # Track the current template key
        current_template_content = []  # Store lines for the current template content
        
        # Step 1: Authenticate the file
        if not lines[0].strip().startswith("# DSCRIPT SAVE FILE"):
            raise ValueError("File/Content is not a valid DSCRIPT file.")

        # Step 2: Process each line dynamically
        for line in lines[1:]:
            stripped = line.strip()

            # Ignore empty lines and comments
            if not stripped or stripped.startswith("#"):
                continue
            
            # Remove trailing comments
            stripped = remove_comments(stripped)

            # Step 3: Handle global parameters inside {...}
            if stripped.startswith("{"):
                # Found the opening {, start accumulating global parameters
                inside_global_params = True
                # Remove the opening { and accumulate the remaining content
                global_params_content = stripped[stripped.index('{') + 1:].strip()
                
                # Check if the closing } is also on the same line
                if '}' in global_params_content:
                    global_params_content = global_params_content[:global_params_content.index('}')].strip()
                    inside_global_params = False  # We found the closing } on the same line
                    # Now parse the global parameters block
                    cls._parse_global_params(global_params_content.strip(), global_params)
                    global_params_content = ""  # Reset for the next block
                continue

            if inside_global_params:
                # Accumulate content until the closing } is found
                if stripped.endswith("}"):
                    # Found the closing }, accumulate and process the entire block
                    global_params_content += " " + stripped[:stripped.index('}')].strip()
                    inside_global_params = False  # Finished reading global parameters block
                    
                    # Now parse the entire global parameters block
                    cls._parse_global_params(global_params_content.strip(), global_params)
                    global_params_content = ""  # Reset for the next block if necessary
                else:
                    # Continue accumulating if } is not found
                    global_params_content += " " + stripped
                continue
            
            # Step 4: Detect the start of a multi-line template block inside [...]
            if not inside_template_block:
                template_match = re.match(r'(\w+)\s*:\s*\[', stripped)
                if template_match:
                    current_template_key = template_match.group(1)  # Capture the key
                    inside_template_block = True
                    current_template_content = []  # Reset content list
                    continue
            
            # If inside a template block, accumulate lines until we find the closing ]
            if inside_template_block:
                if stripped == "]":
                    # End of the template block, join the content and store it
                    template[current_template_key] = ScriptTemplate(
                        current_template_content, 
                        definitions=lambdaScriptdata(**definitions),  # Clone current global definitions
                        verbose=True, 
                        userid=current_template_key
                        )
                    template[current_template_key].refreshvar()
                    inside_template_block = False
                    current_template_key = None
                    current_template_content = []
                else:
                    # Accumulate the current line (without surrounding spaces)
                    current_template_content.append(stripped)
                continue

            # Step 5: Handle attributes inside {...}
            if inside_attributes and stripped.endswith("}"):
                # Finish processing attributes for the current key
                cls._parse_attributes(attributes[current_attr_key], stripped[:-1])  # Remove trailing }
                inside_attributes = False
                current_attr_key = None
                continue

            if inside_attributes:
                # Continue accumulating attributes
                cls._parse_attributes(attributes[current_attr_key], stripped)
                continue

            # Step 6: Determine if the line is a definition, template, or attribute
            definition_match = re.match(r'(\w+)\s*=\s*(.+)', stripped)
            template_match = re.match(r'(\w+)\s*:\s*(?!\s*\{.*\}\s*$)(.+)', stripped) # template_match = re.match(r'(\w+)\s*:\s*(?!\{)(.+)', stripped)
            attribute_match = re.match(r'(\w+)\s*:\s*\{\s*(.+)\s*\}', stripped)       # attribute_match = re.match(r'(\w+)\s*:\s*\{(.+)\}', stripped)

            if definition_match:
                # Line is a definition (key=value)
                key, value = definition_match.groups()
                definitions.setattr(key,cls._convert_value(value))

            elif template_match and not inside_template_block:
                # Line is a template (key: content)
                key, content = template_match.groups()
                template[key] = ScriptTemplate(
                    content,
                    definitions=lambdaScriptdata(**definitions),  # Clone current definitions
                    verbose=True,
                    userid=current_template_key)
                template[key].refreshvar()

            elif attribute_match:
                # Line is an attribute (key:{attributes...})
                current_attr_key, attr_content = attribute_match.groups()
                attributes[current_attr_key] = {}
                cls._parse_attributes(attributes[current_attr_key], attr_content)
                inside_attributes = not stripped.endswith("}")

        # Step 7: Validation and Reconstruction
        # Make sure there are no attributes without a template entry
        for key in attributes:
            if key not in template:
                raise ValueError(f"Attributes found for undefined template key: {key}")
            # Apply attributes to the corresponding template object
            for attr_name, attr_value in attributes[key].items():
                setattr(template[key], attr_name, attr_value)

        # Step 7: Create and return a new dscript instance
        if name is None:
            name = autoname(8)
        instance = cls(
            name = name,
            SECTIONS=global_params.get('SECTIONS', ['DYNAMIC']),
            section=global_params.get('section', 0),
            position=global_params.get('position', 0),
            role=global_params.get('role', 'dscript instance'),
            description=global_params.get('description', 'dynamic script'),
            userid=global_params.get('userid', 'dscript'),
            version=global_params.get('version', 0.1),
            verbose=global_params.get('verbose', False)
        )

       
        # Convert numeric string keys to integers if numerickeys is True
        if numerickeys:
            numeric_template = {}
            for key, value in template.items():
                # Check if the key is a numeric string
                if key.isdigit():
                    numeric_template[int(key)] = value
                else:
                    numeric_template[key] = value
            template = numeric_template

        # Set definitions and template
        instance.DEFINITIONS = definitions
        instance.TEMPLATE = template

        # Refresh variables (ensure that variables are detected and added to definitions)
        instance.set_all_variables()

        # Check eval
        instance.check_all_variables(verbose=False)
        
        # return the new instance
        return instance
    

    @classmethod
    def _parse_global_params(cls, content, global_params):
        """Parses global parameters from the accumulated content between {}."""
        # Split by commas, ignoring any commas inside brackets, parentheses, or quotes
        lines = re.split(r',(?![^(){}\[\]]*[\)\}\]])', content)
        for line in lines:
            line = line.strip()  # Remove leading/trailing whitespace
            # Ensure it's a valid key-value pair
            match = re.match(r'([\w_]+)\s*=\s*(.+)', line)
            if match:
                key, value = match.groups()
                key = key.strip()
                value = value.strip()
                # Convert the value to the appropriate type and store in global_params
                global_params[key] = cls._convert_value(value)

    @classmethod
    def _parse_attributes(cls, attr_dict, content):
        """Parses attributes from the content inside {attribute=value,...}."""
        attr_pairs = re.findall(r'(\w+)\s*=\s*([^,]+)', content)
        for attr_name, attr_value in attr_pairs:
            attr_dict[attr_name] = cls._convert_value(attr_value)

    @classmethod
    def _convert_value(cls, value):
        """Converts a string representation of a value to the appropriate Python type."""
        value = value.strip()

        # Boolean conversion
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False

        # Handle quoted strings
        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
            return value[1:-1]

        # Handle lists (Python syntax inside the file)
        if value.startswith('[') and value.endswith(']'):
            return eval(value)  # Using eval to parse lists safely in this controlled scenario

        # Handle numbers
        try:
            if '.' in value:
                return float(value)
            return int(value)
        except ValueError:
            # Return the value as-is if it doesn't match other types
            return value

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
            setattr(copie, k, copy.deepcopy(v, memo))
        return copie
    
    def detect_all_variables(self):
        """
        Detects all variables across all templates in the dscript object.
        
        This method iterates through all ScriptTemplate objects in the dscript and
        collects variables from each template using the detect_variables method.
    
        Returns:
        --------
        list
            A sorted list of unique variables detected in all templates.
        """
        all_variables = set()  # Use a set to avoid duplicates
        # Iterate through all templates in the dscript object
        for template_key, template in self.TEMPLATE.items():
            # Ensure the template is a ScriptTemplate and has the detect_variables method
            if isinstance(template, ScriptTemplate):
                detected_vars = template.detect_variables()
                all_variables.update(detected_vars)  # Add the detected variables to the set    
        return sorted(all_variables)  # Return a sorted list of unique variables
    
    def add_dynamic_script(self, key, content="", userid=None, definitions=None, verbose=None, **USER):
        """
        Add a dynamic script step to the dscript object.

        Parameters:
        -----------
        key : str
            The key for the dynamic script (usually an index or step identifier).
        content : str or list of str, optional
            The content (template) of the script step.
        definitions : lambdaScriptdata, optional
            The merged variable space (STATIC + GLOBAL + LOCAL).
        verbose : bool, optional
            If None, self.verbose will be used. Controls verbosity of the template.
        USER : dict
            Additional user variables that override the definitions for this step.
        """
        if definitions is None:
            definitions = lambdaScriptdata()
        if verbose is None:
            verbose = self.verbose
        # Create a new ScriptTemplate and add it to the TEMPLATE
        self.TEMPLATE[key] = ScriptTemplate(
            content=content,
            definitions=self.DEFINITIONS+definitions,
            verbose=verbose,
            userid = key if userid is None else userid,
            **USER
        )    
        


    def check_all_variables(self, verbose=True, seteval=True, output=False):
        """
        Checks for undefined variables for each TEMPLATE key in the dscript object.

        Parameters:
        -----------
        verbose : bool, optional, default=True
            If True, prints information about variables for each TEMPLATE key.
            Shows [-] if the variable is set to its default value, [+] if it is defined, and [ ] if it is undefined.
        
        seteval : bool, optional, default=True
            If True, sets the `eval` attribute to True if at least one variable is defined or set to its default value.
        
        output : bool, optional, default=False
            If True, returns a dictionary with lists of default variables, set variables, and undefined variables.

        Returns:
        --------
        out : dict, optional
            If `output=True`, returns a dictionary with the following structure:
            - "defaultvalues": List of variables set to their default value (${varname}).
            - "setvalues": List of variables defined with values other than their default.
            - "undefined": List of variables that are undefined.
        """
        out = {"defaultvalues": [], "setvalues": [], "undefined": []}

        for key in self.TEMPLATE:
            template = self.TEMPLATE[key]
            # Call the check_variables method of ScriptTemplate for each TEMPLATE key
            result = template.check_variables(verbose=verbose, seteval=seteval)
            
            # Update the output dictionary if needed
            out["defaultvalues"].extend(result["defaultvalues"])
            out["setvalues"].extend(result["setvalues"])
            out["undefined"].extend(result["undefined"])

        if output:
            return out


    def set_all_variables(self):
        """
        Ensures that all variables in the templates are added to the global definitions
        with default values if they are not already defined.
        """
        for key, script_template in self.TEMPLATE.items():
            # Check and update the global definitions with template-specific variables
            for var in script_template.detect_variables():
                if var not in self.DEFINITIONS:
                    # Add undefined variables with their default value
                    self.DEFINITIONS.setattr(var, f"${{{var}}}")  # Set default as ${varname}


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
    
    # Add script lines/items with placeholders for variables
    S[3] = "instruction .... with substitution rules ${v1}+${var2}"
    S['alpha'] = "another script template ${v3}"
    
    # Set a custom attribute for a specific line
    S[3].attribute1 = True
    
    # Reorder script lines/items
    T = S[[1,0]]
    
    # Define global variables in DEFINITIONS
    S.DEFINITIONS.a = 1
    S.DEFINITIONS.b = 2
    
    # Update a script line and enable evaluation of its content
    S[0] = "$a+$b"
    S[0].eval = True
    
    # Set a line as mandatory (not facultative)
    S[3].facultative = False
    
    # Access and print the content of specific script lines/items
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
    R[0]        = "% ${comment}"               # line/item can be identied by numbers/names
    R["dim"]    = "dimension    ${dimension}"  # line/item identified as 'dim'
    R["unit"]   = "units        ${units}"      # line/item identified as 'unit'
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
    
    # Save the current script
    R.save(overwrite=True)
    
    # Load again the same script and show the script
    T = dscript.load(R.name)
    print(repr(T))
    ssT = R.script(units="$lj",  # Use "$" to prevent immediate evaluation
                  comment="$my second dynamic script").do()
    print(ssT)
    
    # ========================================================
    # DSCRIPT SAVE FILE: Example: LAMMPS generic code
    #   This example is intended to illustrate the syntax
    #   Note that the script below does not include the header.
    #   It will be added with the write method
    # ========================================================
 
    # The script is defined here within a string
    # note that the first line should be: # DSCRIPT SAVE FILE
    myscript = """# DSCRIPT SAVE FILE
# Global Parameters:
# ------------------
# Define general settings for the script class.
# This section is not mandatory.
# Properties are defined within { }
# They include
#       SECTIONS = ["DYNAMIC"] # the considered section names
#       section = 0            # the current section index,
#       position = 0           # the script  position order,
#       role = "dscript instance",
#       description = "dynamic script",
#       userid = "dscript",
#       version = 0.1,
#       verbose = False
{ # a line starting with { indicates the begining of the section
    SECTIONS = ['INITIALIZATION', 'SIMULATION'], # this is a comment
    section=0, position=0 } # note the closing } is mandatory

# DEFINITIONS (Define general settings for the script.)
# -----------
# All variables are defined in a Python way

d = 3                        # d is a number and equals 3
units = "$lj"                # $ is used to block immediate execution in a string
periodic = "$p"              # $ is used to block immediate execution in a string
dimension = "${d}"           # d is a variable
boundary = ["p", "p", "p"]   # this a list (Python syntax)
atom_style = "$atomic"
lattice = ["fcc", 3.52]       # this a list (Python syntax)
region = ["box", "block", 0, 10, 0, 10, 0, 10] # this a list (Python syntax)
create_box = [1, "box"]
create_atoms = [1, "box"]
mass = 1.0
pair_style = ["lj/cut", 2.5]
pair_coeff = [1, 1, 1.0, 1.0, 2.5]
velocity = ["all", "create", 300.0, 12345]
fix = [1, "all", "nve"]
run = 1000
timestep = 0.001
thermo = 100

# TEMPLATE:
# ---------
# Provide a template for how these parameters should be formatted or used in the script.
#  The general syntax is:
#      KEY: INSTRUCTION
#      KEY can be numeric, alphanumeric
#      INSTRUCTION can be any LAMMPS command involving variables defined in the DEFINITION section or elsewhere
units: units ${units}     # key = units, template = units ${units}
dim: dimension ${dimension}
bound: boundary ${boundary}
astyle: atom_style ${atom_style}
lattice: lattice ${lattice}
region: region ${region}
create_box: create_box ${create_box}
create_atoms: create_atoms ${create_atoms}
mass: mass ${mass}
pair_style: pair_style ${pair_style}
pair_coeff: pair_coeff ${pair_coeff}
velocity: velocity ${velocity}
fix: fix ${fix}
run: run ${run}
timestep: timestep ${timestep}
thermo: thermo ${thermo}

# Attributes:
# -----------
# Each template line can have attributes (here default attributes, but the user can add more)
# Default value between ()
#   facultative = True or (False) (remove the template line if True)
#   eval = True or (False) (evaluate the template line with eval() if True)
#   readonly True or (False) (prevent any subsequent modification() if True)
#   condition = any expression with variables
#   condeval = True or (False) (evaluate the condition with eval() if True)
#   detectvar = (True) or False (create variables in DEFINITIONS if True)
units: {facultative=False, eval=False, readonly=False, condition="${units}", condeval=False, detectvar=True}
dim: {facultative=False, eval=False, readonly=False, condition=None, condeval=False, detectvar=True}
    """
    
    # write myscript to disk
    myscriptfile = dscript.write(myscript)
    print(f"DSCRIPT SAVE FILE: {myscriptfile}")
    
    # load the script as a dscript object
    myS = dscript.load(myscriptfile)
    
    # generate the corresponding script
    myS.units.do()
    smyS = myS.script()
    
    # Ececute the script and print it
    ssmyS = smyS.do()
    print(ssmyS)
    
    # The conversion of a string into a script
    # can be mediated via dscript.parsesyntax()
    # without using a temporary file
    mytemplate = dscript.parsesyntax(myscript).script()
    mytemplatetxt = mytemplate.do()
    print(mytemplatetxt)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#       Beyond this line, the previous examples are tested with the new compact syntax
#       enabling to define a template-block with a single key/tag.
#       The intent is to accelerate scripting and readability.
#
#       IMPORTANT
#           In DSCRIPT SAVE FILE, a block uses a new syntax between square brackets "[]"
#               # TEMPLATE (number of items=1)
#               code: [
#               % ${comment}
#               dimension    ${dimension}
#               units        ${units}
#               boundary     ${boundary}
#               atom_style   ${atom_style}
#               atom_modify  ${atom_modify}
#               comm_modify  ${comm_modify}
#               neigh_modify ${neigh_modify}
#               newton       ${newton}
#     ]
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#
    # =====================================================
    # Production Example version 2: compact version
    #   using multiple lines/items template
    # =====================================================

    R2 = dscript(name="ProductionExample2")
        
    # Define global variables (DEFINITIONS) for the script
    R2.DEFINITIONS.dimension = 3
    R2.DEFINITIONS.units = "$si"
    R2.DEFINITIONS.boundary = ["sm", "sm", "sm"]
    R2.DEFINITIONS.atom_modify = ["map", "array"]
    R2.DEFINITIONS.comm_modify = ["vel", "yes"]
    R2.DEFINITIONS.neigh_modify = ["every", 10, "delay", 0, "check", "yes"]
    R2.DEFINITIONS.newton = "$off"
    
    # Define the script template, associating each line with a key
    R2["code"] = """        
    % ${comment}               # this comment will be preserved as it starts with %
    dimension    ${dimension}  # this comment will be deleted
    units        ${units}
    boundary     ${boundary}
    atom_style   ${atom_style}
    atom_modify  ${atom_modify}
    comm_modify  ${comm_modify}
    neigh_modify ${neigh_modify}
    newton       ${newton}
    """
    
    # Add missing defintion
    R2.DEFINITIONS.atom_style = "$smd"        
    
    # Generate a script instance, overwriting the 'units' variable and adding a comment
    sR2 = R2.script(units="$lj",  # Use "$" to prevent immediate evaluation
                   comment="$my first dynamic script")
    ssR2 = sR2.do()
    
    # Print the generated script
    print(ssR2)
    
    # Save the current script
    R2.save(overwrite=True)
    
    # Load again the same script and show the script
    T2 = dscript.load(R2.name)
    print(repr(T2))
    ssT2 = R2.script(units="$lj",  # Use "$" to prevent immediate evaluation
                  comment="$my second dynamic script").do()
    print(ssT2)
        
    # ========================================================
    # DSCRIPT SAVE FILE: compact version
    # ========================================================
 
    # The script is defined here within a string
    # note that the first line should be: # DSCRIPT SAVE FILE
    
    myscript2 = """# DSCRIPT SAVE FILE
    
# Global Parameters:
# ------------------
{ # a line starting with { indicates the begining of the section
    SECTIONS = ['INITIALIZATION', 'SIMULATION'], # this is a comment
    section=0, position=0 } # note the closing } is mandatory

# DEFINITIONS (Define general settings for the script.)
# -----------
d = 3                        # d is a number and equals 3
units = "$lj"                # $ is used to block immediate execution in a string
periodic = "$p"              # $ is used to block immediate execution in a string
dimension = "${d}"           # d is a variable
boundary = ["p", "p", "p"]   # this a list (Python syntax)
atom_style = "$atomic"
lattice = ["fcc", 3.52]       # this a list (Python syntax)
region = ["box", "block", 0, 10, 0, 10, 0, 10] # this a list (Python syntax)
create_box = [1, "box"]
create_atoms = [1, "box"]
mass = 1.0
pair_style = ["lj/cut", 2.5]
pair_coeff = [1, 1, 1.0, 1.0, 2.5]
velocity = ["all", "create", 300.0, 12345]
fix = [1, "all", "nve"]
run = 1000
timestep = 0.001
thermo = 100

# TEMPLATE:
# ---------
mytemplate1: [
    # you can add comments inside templates   
    units ${units}     # whereever you need
    dimension ${dimension}
    boundary ${boundary}
    atom_style ${atom_style}
    lattice ${lattice}
    region ${region}
    create_box ${create_box}
    create_atoms ${create_atoms}
    mass ${mass}
    pair_style ${pair_style}
    pair_coeff ${pair_coeff}
    ]

mytemplate2: [
    velocity ${velocity}
    fix ${fix}
    run ${run}
    timestep ${timestep}
    thermo ${thermo}
    ]

# Attributes:
# -----------
mytemplate1: {facultative=False, eval=False, readonly=False, condition="${units}", condeval=False, detectvar=True}
mytemplate2: {facultative=False, eval=False, readonly=False, condition="", condeval=False, detectvar=True}
    """
    
    # write myscript to disk
    myscriptfile2 = dscript.write(myscript2)
    print(f"DSCRIPT SAVE FILE: {myscriptfile2}")
    
    # load the script as a dscript object
    myS2 = dscript.load(myscriptfile2)
    
    # generate the corresponding script
    smyS2 = myS2.script()
    
    # Ececute the script and print it
    ssmyS2 = smyS2.do()
    print(ssmyS2)
    
    # The conversion of a string into a script
    # can be mediated via dscript.parsesyntax()
    # without using a temporary file
    mytemplate2 = dscript.parsesyntax(myscript2).script()
    mytemplatetxt2 = mytemplate2.do()
    print(mytemplatetxt2)
    
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #                                        ADVANCED EXAMPLE
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ################################################################################
        # This Python script demonstrates the conversion of a LAMMPS input script 
        # for a TLSPH (Total Lagrangian Smoothed Particle Hydrodynamics) simulation 
        # into a `dscript` object. The `dscript` format allows for flexible manipulation 
        # of variables, templates, and simulation parameters using Python.
        #
        # Example use case:
        # - The script simulates elongation of a 2D strip of a linear elastic material 
        #   by pulling its ends apart, using LAMMPS USER.SMD package.
        # - The units are set to GPa / mm / ms, and material properties such as 
        #   Young’s modulus, Poisson’s ratio, and density are defined.
        # - The geometry, boundary conditions, material model, and output settings 
        #   are set up dynamically.
        #
        # Sections in the script:
        # 1. **INITIALIZE**: Initializes the LAMMPS environment and sets simulation settings.
        # 2. **CREATE_GEOMETRY**: Defines the initial particle geometry and region.
        # 3. **DISCRETIZATION**: Defines parameters for discretization and particle properties.
        # 4. **BOUNDARY_CONDITIONS**: Sets velocity conditions to pull the strip's top and bottom edges.
        # 5. **PHYSICS**: Specifies the interaction physics and material model using the USER.SMD package.
        # 6. **OUTPUT**: Configures stress, strain, and neighbor computations for output.
        # 7. **STATUS_OUTPUT**: Defines how stress and strain are calculated and output.
        # 8. **RUN**: Executes the simulation for a specified number of steps.
        #
        # The main variables such as Young’s modulus (E), Poisson’s ratio (nu), and density (rho) 
        # are added to the `DEFINITIONS` section for dynamic use in the script.
        #
        # The `TEMPLATE` section organizes each block of the LAMMPS script under different keys 
        # (e.g., "initialize", "create", "discretization"), allowing easy manipulation or modification 
        # of individual parts of the script through Python code.
        #
        # This approach facilitates parameter sweeps, automatic adjustments of simulation inputs, 
        # and easy reconfiguration of simulation settings, making it suitable for high-throughput 
        # or iterative simulations in LAMMPS.
        #
        # The script can be saved, loaded, or executed in Python as a `dscript` object, providing 
        # a robust tool for dynamic LAMMPS input file generation and manipulation.
        ################################################################################
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    
    # This flexible approach enables dynamic manipulation of simulation parameters.
    # The full TLSPH template is defined as a multi-line script in DSCRIPT format.
    # The following template was automatically generated by ChatGPT based on the 
    # original LAMMPS TLSPH simulation script for elongating a 2D strip of linear 
    # elastic material by pulling its ends apart. 
    # 
    # Key variables (such as Young's modulus, Poisson's ratio, and mass density) 
    # have been added to the DEFINITIONS section for dynamic substitution in the 
    # template.
    #
    # Read the synopsis of this module to learn how to instruct ChatGPT to generate 
    # such templates.
    
    TLSPH_template = """# DSCRIPT SAVE FILE
# TENSILE SUMULATION
####################################################################################################
#
# TLSPH example: elongate a 2d strip of a linear elastic material py pulling its ends apart
#
# unit sytem: GPa / mm / ms
#
####################################################################################################
# Source: 
# GLOBAL PARAMETERS
{
    SECTIONS = ['INITIALIZE', 'CREATE_GEOMETRY', 'DISCRETIZATION', 'BOUNDARY_CONDITIONS', 'PHYSICS', 'OUTPUT', 'RUN'],
    section = 0,
    position = 0,
    role = "dscript instance",
    description = "Advanced example based on ChatGPT translation",
    userid = "ChatGPT",
    version = 1.0,
    verbose = False
}

# DEFINITIONS (number of definitions=12)
E=1.0              # Young's modulus
nu=0.3             # Poisson ratio
rho=1.0            # Initial mass density
q1=0.06            # Artificial viscosity linear coefficient
q2=0.0             # Artificial viscosity quadratic coefficient
hg=10.0            # Hourglass control coefficient
cp=1.0             # Heat capacity
l0=1.0             # Lattice spacing
h=2.01 * ${l0}     # SPH smoothing kernel radius
vol_one=${l0}**2   # Volume of one particle (unit thickness)
vel0=0.005         # Pull velocity
skin=${h}          # Verlet list range

# TEMPLATE (number of lines=8)
initialize: [
    dimension 2
    units si
    boundary sm sm p
    atom_style smd
    atom_modify map array
    comm_modify vel yes
    neigh_modify every 10 delay 0 check yes
    newton off
]

# set region dimensions
boxlength = 10  # variables can be defined and changed any time (only the last definition is retained)
boxdepth =  0.1 # variables can be defined and changed any time (only the last definition is retained)

create: [
    lattice sq ${l0}
    region box block ${boxlength} ${boxlength} ${boxlength} ${boxlength} ${boxdepth} ${boxdepth} units box
    create_box 1 box
    create_atoms 1 box
    group tlsph type 1
]

discretization: [
    neighbor ${skin} bin
    set group all volume ${vol_one}
    set group all smd_mass_density ${rho}
    set group all diameter ${h}
]

boundary_conditions: [
    region top block EDGE EDGE 9.0 EDGE EDGE EDGE units box
    region bot block EDGE EDGE EDGE 9.1 EDGE EDGE units box
    group top region top
    group bot region bot
    variable vel_up equal ${vel0} * (1.0 exp(0.01 * time))
    variable vel_down equal v_vel_up
    fix veltop_fix top smd/setvelocity 0 v_vel_up 0
    fix velbot_fix bot smd/setvelocity 0 v_vel_down 0
]

physics: [
    pair_style smd/tlsph
    pair_coeff 1 1 *COMMON ${rho} ${E} ${nu} ${q1} ${q2} ${hg} ${cp} &
    *STRENGTH_LINEAR &
    *EOS_LINEAR &
    *END
]

output: [
    compute S all smd/tlsph_stress
    compute E all smd/tlsph_strain
    compute nn all smd/tlsph_num_neighs
    dump dump_id all custom 10 dump.LAMMPS id type x y z vx vy vz &
    c_S[1] c_S[2] c_S[4] c_nn &
    c_E[1] c_E[2] c_E[4] &
    vx vy vz
    dump_modify dump_id first yes
]

# add filename
outputfilename = "$stress_strain.dat" # variables can be defined and changed any time

status_output: [
    variable stress equal 0.5 * (f_velbot_fix[2] - f_veltop_fix[2]) / 20
    variable length equal xcm(top,y) - xcm(bot,y)
    variable strain equal (v_length - ${length}) / ${length}
    fix stress_curve all print 10 "${strain} ${stress}" file ${outputfilename} screen no
    thermo 100
    thermo_style custom step dt f_dtfix v_strain
]

# add runtime
runtime = 2000  # variables can be defined and changed any time

# single liner template
run_simulation: run ${runtime}

# change runtime
runtime = 2500  # variables can be defined and changed any time (only the last definition is retained)


# ATTRIBUTES (number of lines with explicit attributes=0)

    """
    
    TLSPH = dscript.parsesyntax(TLSPH_template)  # this is a dscript instance
    TLSPH_script = TLSPH.script()                # this is a script instance
    TLSPH.code = TLSPH_script.do()               # this is the corresponding LAMMPS code
    print(TLSPH.code)
    # Note that some definitions are missing since they are calculated by LAMMPS during the simulation
    # It includes: stress, strain, length
    repr(TLSPH.DEFINITIONS)