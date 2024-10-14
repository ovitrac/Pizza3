#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__project__ = "Pizza3"
__author__ = "Olivier Vitrac, Han Chen"
__copyright__ = "Copyright 2023"
__credits__ = ["Olivier Vitrac","Han Chen"]
__license__ = "GPLv3"
__maintainer__ = "Olivier Vitrac"
__email__ = "olivier.vitrac@agroparistech.fr"
__version__ = "0.9972"


"""
===============================================
          pizza.group Class Manual
===============================================

## Introduction

The `group` class provides a Pythonic interface to manage groups of atoms in LAMMPS simulations through the Pizza.py toolkit. In LAMMPS, groups are fundamental for applying operations to subsets of atoms, such as assigning force fields, computing properties, or setting up constraints. The `group` class allows users to create, manipulate, and combine groups of atoms programmatically, mirroring the functionality of LAMMPS group commands within a Python environment.

Unlike the `pizza.region` class, which allows for dynamic geometrical definitions, the `group` class operates statically. This choice is due to the nature of atom groups in LAMMPS, which are snapshots of atom collections at a specific time, rather than dynamic entities that change over time.

## Overview

Groups are stored and managed via a collection of operations. Each operation represents a LAMMPS group command or a combination of groups using algebraic operations. The `group` class facilitates both the creation of basic groups and the combination of existing groups using union, intersection, and subtraction.

The class supports both high-level methods, which correspond directly to LAMMPS commands, and low-level methods for internal management of group operations.

---

## High-Level Methods

These methods correspond directly to LAMMPS group commands and allow for the creation and manipulation of groups based on various criteria.

### `region(group_name, regionID)`

- **Description**: Defines a group of atoms based on a specified region ID.
- **Usage**: `G.region('group_name', 'regionID')`
- **Example**:
  - In LAMMPS:
    ```lammps
    region myRegion block 0 10 0 10 0 10 units box
    group myGroup region myRegion
    ```
  - In Python:
    ```python
    G = group()
    G.region('myGroup', 'myRegion')
    ```

### `type(group_name, type_values)`

- **Description**: Selects atoms by their type and assigns them to a group.
- **Usage**: `G.type('group_name', type_values)`
- **Example**:
  - In LAMMPS:
    ```lammps
    group myGroup type 1 2
    ```
  - In Python:
    ```python
    G = group()
    G.type('myGroup', [1, 2])
    ```

### `id(group_name, id_values)`

- **Description**: Selects atoms by their IDs and assigns them to a group.
- **Usage**: `G.id('group_name', id_values)`
- **Example**:
  - In LAMMPS:
    ```lammps
    group myGroup id 1 2 3
    ```
  - In Python:
    ```python
    G = group()
    G.id('myGroup', [1, 2, 3])
    ```

### `variable(group_name, variable_name, expression, style="atom")`

- **Description**: Defines a group based on an atom-style variable expression.
- **Usage**: `G.variable('group_name', 'variable_name', 'expression', style='atom')`
- **Example**:
  - In LAMMPS:
    ```lammps
    variable myVar atom "x > 5"
    group myGroup variable myVar
    ```
  - In Python:
    ```python
    G = group()
    G.variable('myGroup', 'myVar', 'x > 5')
    ```

### `create(group_name)`

- **Description**: Creates a new empty group or clears an existing group.
- **Usage**: `G.create('group_name')`
- **Example**:
  - In LAMMPS:
    ```lammps
    group myGroup clear
    ```
  - In Python:
    ```python
    G = group()
    G.create('myGroup')
    ```

### Algebraic Operations

The `group` class supports algebraic operations between groups using the overloaded operators `+`, `-`, and `*` for union, subtraction, and intersection, respectively.

#### `union(group_name, *groups)`

- **Description**: Creates a new group by performing the union of specified groups.
- **Usage**: `G.union('new_group', *groups)`
- **Example**:
  - In LAMMPS:
    ```lammps
    group newGroup union group1 group2
    ```
  - In Python:
    ```python
    G.union('newGroup', 'group1', 'group2')
    ```

#### `intersect(group_name, *groups)`

- **Description**: Creates a new group by performing the intersection of specified groups.
- **Usage**: `G.intersect('new_group', *groups)`
- **Example**:
  - In LAMMPS:
    ```lammps
    group newGroup intersect group1 group2
    ```
  - In Python:
    ```python
    G.intersect('newGroup', 'group1', 'group2')
    ```

#### `subtract(group_name, *groups)`

- **Description**: Creates a new group by subtracting specified groups from the first group.
- **Usage**: `G.subtract('new_group', *groups)`
- **Example**:
  - In LAMMPS:
    ```lammps
    group newGroup subtract group1 group2
    ```
  - In Python:
    ```python
    G.subtract('newGroup', 'group1', 'group2')
    ```

### `evaluate(group_name, group_op)`

- **Description**: Evaluates complex group expressions involving algebraic operations and stores the result in a new group.
- **Usage**: `G.evaluate('new_group', group_op)`
- **Example**:
  ```python
  G = group()
  G.create('o1')
  G.create('o2')
  G.create('o3')
  complex_op = G['o1'] + G['o2'] + G['o3']
  G.evaluate('combinedGroup', complex_op)



Created on Wed Aug 16 16:25:19 2023

@author: olivi
"""

# Revision history
# 2023-08-17 RC with documentation, the script method is not implemented yet (to be done via G.code())
# 2023-08-18 consolidation of the GroupOperation mechanism (please still alpha version)
# 2023-09-01 the class GroupOperation has been removed and the collapse is carried within Operation to avoid unecessary complications [major release]
# 2024-10-04 code optimization
# 2024-10-07 implementation of dscript, script, pipescript
# 2024-10-08 code finalization (flexible initialization), updated documentation
# 2024-10-11 advanced indexing and scripting
# 2024-10-12 add copy and deepcopy features

# %% Dependencies
# pizza.group is independent of region and can performs only static operations.
# It is designed to be compatible with region via G.script()
import hashlib, random, string, copy
from pizza.script import span, pipescript
from pizza.dscript import dscript

# %% Private classes and functions

# Helper function that generates a random string of a specified length using uppercase and lowercase letters.
def generate_random_name(length=8):
    letters = string.ascii_letters  # 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join(random.choice(letters) for _ in range(length))

# Class for binary and unary operators
class Operation:
    """
    Represents a LAMMPS group operation, allowing algebraic manipulation and code generation.

    ### Overview

    The `Operation` class models a group operation in LAMMPS (Large-scale Atomic/Molecular Massively
    Parallel Simulator), encapsulating an operator, its operands, a name, and the corresponding LAMMPS code.
    It supports algebraic operations between groups (union, intersection, subtraction) using the
    overloaded operators '+', '-', and '*', enabling users to build complex group expressions
    programmatically.

    ### Attributes

    - **operator (str)**: The operator applied to the operands. It can be:
        - A finalized LAMMPS operator: `'variable'`, `'byvariable'`, `'byregion'`, `'bytype'`, `'byid'`, `'create'`, `'clear'`,
          `'union'`, `'intersect'`, `'subtract'`.
        - An algebraic operator: `'+'`, `'-'`, `'*'`.
        - An empty string or `None` for operations without an explicit operator.

    - **operands (list)**: A list of operands for the operation. Operands can be:
        - Instances of `Operation`, representing nested operations.
        - Strings representing group names or other identifiers.
        - Integers or lists (e.g., atom types or IDs).

    - **name (str)**: The name of the operation, which can be manually set or auto-generated.
        - If not provided, a unique hash-based name is generated using the `generate_hashname` method.

    - **code (str)**: The LAMMPS code that this operation represents.
        - This is generated when the operation is finalized and corresponds to the actual command(s)
          that would be included in a LAMMPS input script.

    - **criteria (dict, optional)**: Criteria used to define the operation.
        - Useful for operations like `bytype`, `byregion`, `byid`, etc., where the criteria specify
          the selection parameters.

    ### Methods

    - `__init__(self, operator, operands, name="", code="", criteria=None)`:
        Initializes a new `Operation` instance with the given parameters.
        - **operator** (str): The operator applied to the operands.
        - **operands** (list or single operand): The operands for the operation.
        - **name** (str, optional): The name of the operation.
        - **code** (str, optional): The LAMMPS code representing the operation.
        - **criteria** (dict, optional): Criteria used to define the operation.

    - `append(self, operand)`:
        Appends a single operand to the operands list.

    - `extend(self, operands)`:
        Extends the operands list with multiple operands.

    - `is_unary(self)`:
        Checks if the `Operation` instance has exactly one operand.

    - `is_empty(self)`:
        Checks if the `Operation` instance has no operands.

    - `generateID(self)`:
        Generates an ID for the instance based on its operands or name.
        Used internally for generating unique names.

    - `generate_hashname(self, prefix="grp", ID=None)`:
        Generates a hash-based name for the instance.
        - **prefix** (str): A string prefix for the generated name.
        - **ID** (str, optional): An optional ID to include in the hash. If `None`, it is generated from operands.

    - `get_proper_operand(self)`:
        Returns the appropriate operand representation depending on whether the operation is finalized.

    - `_operate(self, other, operator)`:
        Combines the operation with another `Operation` instance using the specified operator.
        - **other** (`Operation`): The other operation to combine with.
        - **operator** (str): The operator to apply ('+', '-', '*').

    - `isfinalized(self)`:
        Checks if the operation has been finalized.
        - An operation is considered finalized if its operator is not one of the algebraic operators '+', '-', '*'.

    - `__add__(self, other)`:
        Overloads the '+' operator to support union of two `Operation` instances.

    - `__sub__(self, other)`:
        Overloads the '-' operator to support subtraction between two `Operation` instances.

    - `__mul__(self, other)`:
        Overloads the '*' operator to support intersection between two `Operation` instances.

    - `__repr__(self)`:
        Returns a detailed string representation of the operation, useful for debugging.

    - `__str__(self)`:
        Returns a concise string representation of the operation.

    - `script(self)`:
        Generates the LAMMPS code for this operation using `dscript` and `script` classes.
        - Returns a `script` object containing the LAMMPS code.

    ### Operator Overloading

    The `Operation` class overloads the following operators to enable algebraic manipulation:

    - **Addition (`+`)**:
        - Combines two operations using union.
        - Example: `op3 = op1 + op2`

    - **Subtraction (`-`)**:
        - Subtracts one operation from another.
        - Example: `op3 = op1 - op2`

    - **Multiplication (`*`)**:
        - Intersects two operations.
        - Example: `op3 = op1 * op2`

    ### Usage Example

    ```python
    # Create basic operations
    op1 = Operation('bytype', [1], name='group1')
    op2 = Operation('bytype', [2], name='group2')

    # Combine operations using algebraic operators
    combined_op = op1 + op2  # Union of group1 and group2

    # Initialize group manager
    G = group()
    G.add_operation(op1)
    G.add_operation(op2)

    # Evaluate the combined operation and store the result
    G.evaluate('combined_group', combined_op)

    # Access the generated LAMMPS code
    print(G.code())
    # Output:
    # group group1 type 1
    # group group2 type 2
    # group combined_group union group1 group2
    ```

    ### Notes

    - **Lazy Evaluation**:
        - Operations are combined and stored symbolically until they are evaluated.
        - The actual LAMMPS code is generated when the operation is finalized (e.g., via the `evaluate` method in the `group` class).

    - **Name Generation**:
        - If an operation's name is not provided, it is auto-generated using a hash of its operator and operands.
        - This ensures uniqueness and avoids naming conflicts.

    - **Criteria Attribute**:
        - The `criteria` attribute allows storing the parameters used to define operations.
        - Useful for debugging, documentation, or reconstructing operations.

    - **Finalization**:
        - An operation is finalized when it represents an actual LAMMPS command and has generated code.
        - Finalized operations are not further combined; instead, their names are used in subsequent operations.

    - **Integration with `dscript` and `script`**:
        - The `script` method generates the LAMMPS code for the operation using `dscript` and `script` classes.
        - Facilitates integration with script management tools and advanced scripting workflows.

    - **Error Handling**:
        - Methods include error checks to ensure operands are valid and operations are correctly formed.
        - Raises informative exceptions for invalid operations or unsupported types.

    ### Integration with Group Class

    The `Operation` class is designed to work closely with the `group` class, which manages a collection of operations and handles evaluation and code generation.

    - **Adding Operations**:
        - Use `group.add_operation(operation)` to add an `Operation` instance to a `group`.
    - **Evaluating Operations**:
        - Use `group.evaluate(group_name, operation)` to finalize an operation and generate LAMMPS code.
    - **Accessing Operations**:
        - Operations can be accessed via the `group` instance using indexing, attribute access, or methods.

    ### Additional Information

    - **String Representations**:
        - `__str__`: Provides a concise representation, useful for quick inspection.
        - `__repr__`: Provides a detailed representation, useful for debugging.

    - **Example of `__str__` Output**:
        - For an operation representing `group1 + group2`:
          ```python
          print(str(combined_op))
          # Output: <combined_group=[group1+group2]>
          ```

    - **Example of `__repr__` Output**:
        ```python
        print(repr(combined_op))
        # Output:
        # Operation Details:
        #   - Name: combined_group
        #   - Operator: +
        #   - Operands: group1, group2
        #   - LAMMPS Code:
        ```

    ### Examples

    **Defining Operations Based on Atom Types**

    ```python
    op1 = Operation('bytype', [1], name='type1')
    op2 = Operation('bytype', [2], name='type2')
    G.add_operation(op1)
    G.add_operation(op2)
    ```

    **Combining and Evaluating Operations**

    ```python
    combined_op = op1 + op2  # Union of 'type1' and 'type2'
    G.evaluate('all_types', combined_op)
    ```

    **Accessing Generated Code**

    ```python
    print(G.code())
    # Output:
    # group type1 type 1
    # group type2 type 2
    # group all_types union type1 type2
    ```

    **Using Criteria Attribute**

    ```python
    # Access criteria used to define an operation
    print(op1.criteria)
    # Output:
    # {'type': [1]}
    ```

    ### Important Notes

    - **Algebraic Operators vs. Finalized Operators**:
        - Algebraic operators ('+', '-', '*') are used for symbolic manipulation.
        - Finalized operators represent actual LAMMPS commands.

    - **Operator Precedence**:
        - When combining operations, consider the order of operations.
        - Use parentheses to ensure the desired evaluation order.

    - **Integration with Scripting Tools**:
        - The `script` method allows operations to be integrated into larger scripting workflows.
        - Supports advanced features like variable substitution and conditional execution.

    ### Conclusion

    The `Operation` class provides a powerful and flexible way to model and manipulate group operations in LAMMPS simulations. By supporting algebraic operations and integrating with script management tools, it enables users to build complex group definitions programmatically, enhancing productivity and reducing errors in simulation setup.

    """

    def __init__(self, operator, operands, name="", code="", criteria=None):
        """Initializes a new Operation instance with given parameters."""
        self.operator = operator
        self.operands = operands if isinstance(operands, list) else [operands]
        if not name:
            self.name = self.generate_hashname()
        else:
            self.name = name
        self.code = code
        self.criteria = criteria  # Store criteria for this operation

    def append(self, operand):
        """Appends a single operand to the operands list of the Operation instance."""
        self.operands.append(operand)

    def extend(self, operands):
        """Extends the operands list of the Operation instance with multiple operands."""
        self.operands.extend(operands)

    def is_unary(self):
        """Checks if the Operation instance has exactly one operand."""
        return len(self.operands) == 1

    def is_empty(self):
        """Checks if the Operation instance has no operands."""
        return len(self.operands) == 0

    def generateID(self):
        """Generates an ID for the Operation instance based on its operands or name."""
        # if self.operands:
        #     return "".join([str(op) for op in self.operands])
        # else:
        #     return self.name
        operand_ids = ''.join(op.name if isinstance(op, Operation) else str(op) for op in self.operands)
        return operand_ids

    def generate_hashname(self,prefix="grp",ID=None):
        """Generates an ID for the Operation instance based on its operands or name."""
        # if ID is None: ID = self.generateID()
        # s = self.operator+ID
        # return prefix+hashlib.sha256(s.encode()).hexdigest()[:6]
        if ID is None:
            ID = self.generateID()
        s = self.operator + ID
        return prefix + hashlib.sha256(s.encode()).hexdigest()[:6]

    def __repr__(self):
        """ detailed representation """
        operand_str = ', '.join(str(op) for op in self.operands)
        return (
            f"Operation Details:\n"
            f"  - Name: {self.name}\n"
            f"  - Operator: {self.operator}\n"
            f"  - Operands: {operand_str}\n"
            f"  - LAMMPS Code: {self.code}"
        )

    def __str__(self):
        """ string representation """
        operands = [str(op) for op in self.operands]
        operand_str = ', '.join(operands)
        if self.is_empty():
            return f"<{self.operator} {self.name}>"

        elif self.is_unary():
            return f"<{self.name}={self.operator}({operand_str})>"
        else:  # Polynary
            operator_symbol_mapping = {
                'union': '+',
                'intersect': '*',
                'subtract': '-'
            }
            operator_symbol = operator_symbol_mapping.get(self.operator, self.operator)
            formatted_operands = operator_symbol.join(operands)
            return f"<{self.name}=[{formatted_operands}]>"

    def isfinalized(self):
        """
        Checks whether the Operation instance is finalized.
        Returns:
        - bool: True if the Operation is finalized, otherwise False.
        Functionality:
        - An Operation is considered finalized if its operator is not
         one of the algebraic operators '+', '-', '*'.
        """
        return self.operator not in ('+', '-', '*')

    def __add__(self, other):
        """ overload + as union """
        return self._operate(other,'+')

    def __sub__(self, other):
        """ overload - as subtract """
        return self._operate(other,'-')

    def __mul__(self, other):
        """ overload * as intersect """
        return self._operate(other,'*')

    def get_proper_operand(self):
        # """
        # Returns the proper operand depending on whether the operation is finalized.
        # """
        # return span(self.operands) if not self.isfinalized() else self.name
        """
        Returns the proper operand depending on whether the operation is finalized.
        """
        if self.isfinalized():
            return self.name
        else:
            # Collect operand names
            operand_names = [
                op.name if isinstance(op, Operation) else str(op)
                for op in self.operands
            ]
            return span(operand_names)

    def _operate(self, other, operator):
        """
        Implements algebraic operations between self and other Operation instances.
    
        Parameters:
        - other (Operation): The other Operation instance to be operated with.
        - operator (str): The operation to be performed. Supported values are '+', '-', '*'.
    
        Returns:
        - Operation: A new Operation instance reflecting the result of the operation.
        """
        # Ensure other is also an instance of Operation
        if not isinstance(other, Operation):
            raise TypeError(f"Unsupported type: {type(other)}")
    
        # Map operator to prefix
        prefix_map = {'+': 'add', '-': 'sub', '*': 'mul'}
        prefix = prefix_map.get(operator, 'op')
    
        # Prepare operands list
        operands = []
    
        # Handle self
        if self.operator == operator and not self.isfinalized():
            operands.extend(self.operands)
        else:
            operands.append(self)
    
        # Handle other
        if other.operator == operator and not other.isfinalized():
            operands.extend(other.operands)
        else:
            operands.append(other)
    
        # Generate a new name
        name = self.generate_hashname(prefix=prefix, ID=self.generateID() + other.generateID())
    
        # Create a new Operation
        new_op = Operation(operator, operands, name=name)
        return new_op

    def script(self):
        """
        Generate the LAMMPS code using the dscript and script classes.
        
        Returns:
        - script onject: The LAMMPS code generated by this operation.
        """
        # Create a dscript object to store the operation code
        dscript_obj = dscript()
        # Use a dummy key for the dscript template
        dscript_obj["dummy"] = self.code
        # Convert the dscript object to a script object
        script_obj = dscript_obj.script()
        return script_obj





# %% Main class group
class group:
    """
    A class for managing LAMMPS group operations and generating LAMMPS scripts.

    ### Overview

    The `group` class provides an object-oriented interface to define and manage
    groups of atoms in LAMMPS simulations. Groups in LAMMPS are collections of
    atoms that can be manipulated together, allowing users to apply fixes,
    compute properties, or perform operations on specific subsets of atoms.

    This class allows you to create, combine, and manipulate groups using
    algebraic operations (union, intersection, subtraction), and to generate
    the corresponding LAMMPS commands. It also provides methods to output the
    group commands as scripts, which can be integrated into LAMMPS input files.

    ### Key Features

    - **Create and Manage Groups**: Define new groups based on atom types,
      regions, IDs, or variables.
    - **Flexible Group Creation**: Create multiple groups at once and define groups
      using concise criteria through the `add_group_criteria` method.
    - **Algebraic Operations**: Combine groups using union (`+`), intersection (`*`),
      and subtraction (`-`) operations.
    - **Subindexing with Callable Syntax**: Retrieve multiple group operations
      by calling the `group` instance with names or indices.
    - **Script Generation**: Generate LAMMPS script lines for group definitions,
      which can be output as scripts or pipelines.
    - **Dynamic Evaluation**: Evaluate complex group expressions and store the
      resulting operations.
    - **Integration with Scripting Tools**: Convert group operations into
      `dscript` or `pipescript` objects for advanced script management.

    ### LAMMPS Context

    In LAMMPS (Large-scale Atomic/Molecular Massively Parallel Simulator),
    groups are fundamental for specifying subsets of atoms for applying
    operations like forces, fixes, and computes. The `group` command in LAMMPS
    allows users to define groups based on various criteria such as atom IDs,
    types, regions, and variables.

    This `group` class abstracts the complexity of managing group definitions
    and operations, providing a high-level interface to define and manipulate
    groups programmatically.

    ### Usage Examples

    **Creating Multiple Groups at Once**

    ```python
    # Create groups 'o1', 'o2', 'o3', 'o4' upon instantiation
    G = group(group_names=['o1', 'o2', 'o3', 'o4'])
    ```

    **Defining Groups Based on Criteria**

    ```python
    G = group()
    G.add_group_criteria('lower', type=[1])
    G.add_group_criteria('central', region='central_cyl')
    G.add_group_criteria('new_group', create=True)
    G.add_group_criteria('upper', clear=True)
    G.add_group_criteria('subtract_group', subtract=['group1', 'group2'])
    ```

    **Defining a Group Based on a Variable**

    ```python
    G = group()
    G.variable('myVar', 'x > 5')          # Assign a variable
    G.byvariable('myGroup', 'myVar')      # Define group based on the variable
    ```

    **Using `add_group_criteria` with Variable**

    ```python
    G.add_group_criteria('myGroup', variable={'name': 'myVar', 'expression': 'x > 5'})
    ```

    **Defining Groups Using a Dictionary**

    ```python
    group_definitions = {
        'group1': {'type': [1, 2]},
        'group2': {'region': 'my_region'},
        'group3': {'variable': {'name': 'var1', 'expression': 'x > 5'}},
        'group4': {'union': ['group1', 'group2']},
    }
    G.add_group_criteria(group_definitions)
    ```

    **Accessing Groups and Performing Operations**

    ```python
    # Access groups via attribute-style or item-style access
    op1 = G.group1
    op2 = G['group2']

    # Combine groups using algebraic operations
    complex_op = op1 + op2 - G.group3

    # Evaluate the operation and store the result
    G.evaluate('combined_group', complex_op)
    ```

    **Subindexing with Callable Syntax**

    ```python
    # Retrieve multiple operations by names or indices
    subG = G('group1', 2, 'group3')  # Retrieves 'group1', third operation, and 'group3'

    # Display the names of operations in subG
    operation_names = [op.name for op in subG._operations]
    print(operation_names)  # Output: ['group1', 'group3', 'group3']

    # Generate the LAMMPS script for the subgroup
    script_content = subG.code()
    print(script_content)
    ```

    **Generating LAMMPS Script**

    ```python
    script_content = G.code()
    print(script_content)
    ```

    ### Class Methods

    #### Initialization and Setup

    - `__init__(self, name=None, groups=None, group_names=None, printflag=False, verbose=True)`: Initializes a new `group` instance.
      - `name` (str): Optional name for the group instance.
      - `groups` (dict): Dictionary of group definitions to create upon initialization.
      - `group_names` (list): List of group names to create empty groups upon initialization.
      - `printflag` (bool): If True, enables printing of script generation.
      - `verbose` (bool): If True, enables verbose output.

    - `create_groups(self, *group_names)`: Creates multiple new groups with the given names.

    - `add_group_criteria(self, *args, **kwargs)`: Adds group(s) based on criteria.
      - Supports two usages:
        - `add_group_criteria(group_name, **criteria)`: Adds a single group.
        - `add_group_criteria(group_definitions)`: Adds multiple groups from a dictionary.

    #### Group Creation Methods

    - `create(self, group_name)`: Creates a new empty group with the given name.
    - `bytype(self, group_name, type_values)`: Defines a group based on atom types.
    - `byid(self, group_name, id_values)`: Defines a group based on atom IDs.
    - `byregion(self, group_name, region_name)`: Defines a group based on a region.
    - `variable(self, variable_name, expression, style="atom")`: Assigns an expression to a LAMMPS variable.
    - `byvariable(self, group_name, variable_name)`: Defines a group based on a variable.
    - `clear(self, group_name)`: Clears an existing group.

    #### Algebraic Operations

    - `union(self, group_name, *groups)`: Performs a union of the specified groups.
    - `intersect(self, group_name, *groups)`: Performs an intersection of the specified groups.
    - `subtract(self, group_name, *groups)`: Subtracts groups from the first group.
    - `evaluate(self, group_name, group_op)`: Evaluates a group operation and stores the result.

    #### Access and Manipulation

    - `__getitem__(self, key)`: Allows accessing operations by name or index.
    - `__getattr__(self, operation_name)`: Enables attribute-style access to operations.
    - `__call__(self, *keys)`: Returns a new `group` instance containing specified operations.
      - **Parameters**:
        - `*keys` (str or int): One or more names or indices of operations to retrieve.
      - **Returns**:
        - `group`: A new `group` instance containing the specified operations.
      - **Example**:
        ```python
        subG = G('group1', 1, 'group3')  # Retrieves 'group1', second operation, and 'group3'
        ```
    - `list(self)`: Returns a list of all operation names.
    - `find(self, name)`: Finds the index of an operation based on its name.
    - `disp(self, name)`: Displays the content of an operation.
    - `delete(self, name)`: Deletes an operation by name.
    - `copy(self, source_name, new_name)`: Copies an existing operation to a new name.
    - `rename(self, old_name, new_name)`: Renames an existing operation.
    - `reindex(self, name, new_idx)`: Changes the index of an operation.

    #### Script Generation

    - `code(self)`: Returns the generated LAMMPS commands as a string.
    - `dscript(self, name=None)`: Generates a `dscript` object containing the group's commands.
    - `script(self, name=None)`: Generates a script object containing the group's commands.
    - `pipescript(self)`: Generates a `pipescript` object containing each group's command as a separate script in a pipeline.

    ### Operator Overloading

    - **Addition (`+`)**: Union of groups.
    - **Subtraction (`-`)**: Subtraction of groups.
    - **Multiplication (`*`)**: Intersection of groups.

    These operators are overloaded in the `Operation` class and can be used to combine group operations.

    ### Internal Functionality

    The class maintains a list `_operations`, which stores all the group operations
    defined. Each operation is an instance of the `Operation` class, which represents
    a LAMMPS group command along with its operands and operator.

    ### Subindexing with Callable Syntax

    The `group` class allows you to retrieve multiple operations by calling the
    instance with names or indices:

    - `__call__(self, *keys)`: Returns a new `group` instance containing the specified operations.
      - **Parameters**:
        - `*keys` (str or int): One or more names or indices of operations to retrieve.
      - **Returns**:
        - `group`: A new `group` instance containing the specified operations.
      - **Example**:
        ```python
        subG = G('group1', 1, 'group3')  # Retrieves 'group1', second operation, and 'group3'
        ```
      - **Notes**:
        - Indices are 0-based integers.
        - Duplicate operations are avoided in the new `group` instance.

    ### Integration with Scripts

    The `group` class integrates with `dscript` and `pipescript` classes to allow
    advanced script management:

    - **`dscript`**: A dynamic script management class that handles script lines
      with variable substitution and conditional execution.
    - **`pipescript`**: Manages a pipeline of scripts, allowing sequential execution
      and advanced variable space management.

    ### Important Notes

    - **Operator Overloading**: The class overloads the `+`, `-`, and `*` operators
      for the `Operation` class to perform union, subtraction, and intersection
      respectively.
    - **Flexible Group Creation**: Groups can be created upon instantiation or added later using concise methods.
    - **Variable Assignment and Group Definition**: When defining groups based on variables, variable assignment and group creation are handled separately.
    - **Subindexing with `__call__`**: The `__call__` method allows you to retrieve multiple operations and create subgroups.
    - **Error Handling**: The class includes robust error checking and provides informative error messages.
    - **Lazy Evaluation**: Group operations are stored and only evaluated when
      the `evaluate` method is called.
    - **Name Management**: The class ensures that group names are unique within
      the instance to prevent conflicts.

    ### Conclusion

    The `group` class simplifies the management of groups in LAMMPS simulations,
    allowing for clear and maintainable code when dealing with complex group
    operations. By providing high-level abstractions, operator overloading,
    subindexing capabilities, and integration with script management tools,
    it enhances productivity and reduces the potential for errors in simulation setup.
    """

    
    def __init__(self, name=None, groups=None, group_names=None, printflag=False, verbose=True):
        self._in_construction = True  # Indicate that the object is under construction
        if not name:
            name = generate_random_name()
        self._name = name
        self._operations = []
        self.printflag = printflag
        self.verbose = verbose
        self._in_construction = False  # Set the flag to indicate construction is finished

        # Create groups based on provided parameters
        if groups:
            if not isinstance(groups, dict):
                raise TypeError("Parameter 'groups' must be a dictionary.")
            self.add_group_criteria(groups)
        if group_names:
            if not isinstance(group_names, (list, tuple)):
                raise TypeError("Parameter 'group_names' must be a list or tuple of group names.")
            self.create_groups(*group_names)
            
            
    def create_groups(self, *group_names):
        for group_name in group_names:
            if not isinstance(group_name, str):
                raise TypeError(f"Group name must be a string, got {type(group_name)}")
            self.create(group_name)
            

    def __str__(self):
        return f'Group "{self._name}" with {len(self._operations)} operations\n'

    def format_cell_content(self, content, max_width):
        content = str(content) if content is not None else ''
        if len(content) > max_width:
            start = content[: (max_width - 5) // 2]
            end = content[-((max_width - 5) // 2):]
            content = f"{start} ... {end}"
        return content

    def __repr__(self):
        max_width_guess = 20
        idx_width = len(str(len(self._operations) - 1))
        headers = ["Idx", "Name", "Operator", "Operands"]
        column_widths = [max(len(headers[0]), idx_width)] + [len(header) for header in headers[1:]]

        for op in self._operations:
            cells = [op.name, op.operator, span(op.operands)]
            for i, cell_content in enumerate(cells):
                cell_width = len(str(cell_content)) if cell_content is not None else 0
                column_widths[i + 1] = min(max(column_widths[i + 1], cell_width), max_width_guess)

        table = "\n| "
        for header, width in zip(headers, column_widths):
            table += f"{header:^{width}} | "
        table += "\n|"
        # Adapting horizontal separators to match the size of the columns
        for width in column_widths:
            table += "-" * (width + 2) + "|"
        table += "\n"
        for idx, op in enumerate(self._operations):
            formatted_idx = str(idx).rjust(idx_width)
            formatted_name = str(op.name).rjust(column_widths[1])
            formatted_operator = str(op.operator).rjust(column_widths[2])
            formatted_operands = str(span(op.operands)).rjust(column_widths[3])
            table += f"| {formatted_idx:^{column_widths[0]}} | {formatted_name:^{column_widths[1]}} | "
            table += f"{formatted_operator:^{column_widths[2]}} | "
            table += f"{formatted_operands:^{column_widths[3]}} |\n"
        table += f"\n{str(self)}"

        return table


    def __len__(self):
        """ return the number of stored operations """
        return len(self._operations)

    def list(self):
        """ return the list of all operations """
        return [op.name for op in self._operations]
    

    def code(self):
        """
            Joins the `code` attributes of all stored `operation` objects with '\n'.
        """
        return '\n'.join([op.code for op in self._operations])

    def find(self, name):
        """Returns the index of an operation based on its name."""
        if '_operations' in self.__dict__:
            for i, op in enumerate(self._operations):
                if op.name == name:
                    return i
        return None

    def disp(self, name):
        """ display the content of an operation """
        idx = self.find(name)
        if idx is not None:
            return self._operations[idx].__repr__()
        else:
            return "Operation not found"

    def clearall(self):
        """ clear all operations """
        self._operations = []

    def delete(self, name):
        """
        Deletes one or more stored operations based on their names.
    
        Parameters:
        -----------
        name : str, list, or tuple
            The name(s) of the operation(s) to delete. If a list or tuple is provided, 
            all specified operations will be deleted.
    
        Usage:
        ------
        G.delete('operation_name')
        G.delete(['operation1', 'operation2'])
        G.delete(('operation1', 'operation2'))
        
        Raises:
        -------
        ValueError
            If any of the specified operations are not found.
        """
        # Handle a single string, list, or tuple
        if isinstance(name, (list, tuple)):
            not_found = []
            for n in name:
                idx = self.find(n)
                if idx is not None:
                    del self._operations[idx]
                else:
                    not_found.append(n)
            # If any names were not found, raise an exception
            if not_found:
                raise ValueError(f"Operation(s) {', '.join(not_found)} not found.")
        elif isinstance(name, str):
            idx = self.find(name)
            if idx is not None:
                del self._operations[idx]
            else:
                raise ValueError(f"Operation {name} not found.")
        else:
            raise TypeError("The 'name' parameter must be a string, list, or tuple.")

    def copy(self, source_name, new_name):
        """
        Copies a stored operation to a new operation with a different name.

        Parameters:
        source_name: str
            Name of the source operation to copy
        new_name: str
            Name of the new operation

        Usage:
        G.copy('source_operation', 'new_operation')
        """
        idx = self.find(source_name)
        if idx is not None:
            copied_operation = self._operations[idx].clone()
            copied_operation.name = new_name
            self.add_operation(copied_operation)
        else:
            raise ValueError(f"Operation {source_name} not found.")

    def rename(self, old_name, new_name):
        """
        Rename a stored operation.

        Parameters:
        old_name: str
            Current name of the operation
        new_name: str
            New name to assign to the operation

        Usage:
        G.rename('old_operation', 'new_operation')
        """
        idx = self.find(old_name)
        if idx is not None:
            if new_name == old_name:
                raise ValueError("The new name should be different from the previous one.")
            elif new_name in self.list():
                raise ValueError("Operation name must be unique.")
            self._operations[idx].name = new_name
        else:
            raise ValueError(f"Operation '{old_name}' not found.")

    def reindex(self, name, new_idx):
        """
        Change the index of a stored operation.

        Parameters:
        name: str
            Name of the operation to reindex
        new_idx: int
            New index for the operation

        Usage:
        G.reindex('operation_name', 2)
        """
        idx = self.find(name)
        if idx is not None and 0 <= new_idx < len(self._operations):
            op = self._operations.pop(idx)
            self._operations.insert(new_idx, op)
        else:
            raise ValueError(f"Operation '{name}' not found or new index {new_idx} out of range.")

    # ------------- indexing and attribute overloading

    def __getitem__(self, key):
        """
            Enable shorthand for G.operations[G.find(operation_name)] using G[operation_name],
            or accessing operation by index using G[index].
        """
        if isinstance(key, str):
            idx = self.find(key)
            if idx is not None:
                return self._operations[idx]
            else:
                raise KeyError(f"Operation '{key}' not found.")
        elif isinstance(key, int):
            if -len(self._operations) <= key < len(self._operations):
                return self._operations[key]
            else:
                raise IndexError("Operation index out of range.")
        else:
            raise TypeError("Key must be an operation name (string) or index (integer).")
            

    def __getattr__(self, name):
        """
        Allows accessing operations via attribute-style notation.
        If the attribute is one of the core attributes, returns it directly.
        For other attributes, searches for an operation with a matching name
        in the _operations list.
    
        Parameters:
        -----------
        name : str
            The name of the attribute or operation to access.
    
        Returns:
        --------
        The value of the attribute if it's a core attribute, or the operation
        associated with the specified name if found in _operations.
    
        Raises:
        -------
        AttributeError
            If the attribute or operation is not found.
        """
        # Handle core attributes directly
        if name in {'_name', '_operations', 'printflag', 'verbose'}:
            # Use object.__getattribute__ to avoid recursion
            return object.__getattribute__(self, name)
        # Search for the operation in _operations
        elif '_operations' in self.__dict__:
            for op in self._operations:
                if op.name == name:
                    return op
        # If not found, raise an AttributeError
        raise AttributeError(f"Attribute or operation '{name}' not found.")
            
                
    def __setattr__(self, name, value):
        """
        Allows deletion of an operation via 'G.operation_name = []' after construction.
        During construction, attributes are set normally.
        """
        if getattr(self, '_in_construction', True):
            # During construction, set attributes normally
            super().__setattr__(name, value)
        else:
            # After construction
            if isinstance(value, list) and len(value) == 0:
                # Handle deletion syntax
                idx = self.find(name)
                if idx is not None:
                    del self._operations[idx]
                else:
                    raise AttributeError(f"Operation '{name}' not found for deletion.")
            else:
                # Set attribute normally
                super().__setattr__(name, value)
                
                
    def _get_subobject(self, key):
        """
        Retrieves a subobject based on the provided key.
    
        Parameters:
        -----------
        key : str or int
            The key used to retrieve the subobject.
    
        Returns:
        --------
        Operation
            The operation corresponding to the key.
    
        Raises:
        -------
        KeyError
            If the key is not found.
        IndexError
            If the index is out of range.
        TypeError
            If the key is not a string or integer.
        """
        if isinstance(key, str):
            # If key is a string, treat it as a group name
            for operation in self._operations:
                if operation.name == key:
                    return operation
            raise KeyError(f"No operation found with name '{key}'.")
        elif isinstance(key, int):
            # If key is an integer, treat it as an index (0-based)
            if 0 <= key < len(self._operations):
                return self._operations[key]
            else:
                raise IndexError(f"Index {key} is out of range.")
        else:
            raise TypeError("Key must be a string or integer.")

    
    def __call__(self, *keys):
        """
        Allows subindexing of the group object using callable syntax with multiple keys.

        Parameters:
        -----------
        *keys : str or int
            One or more keys used to retrieve subobjects or perform subindexing.

        Returns:
        --------
        group
            A new group instance containing the specified operations.

        Example:
        --------
        subG = G('a', 1, 'c')  # Retrieves operations 'a', second operation, and 'c'
        """
        selected_operations = []
        for key in keys:
            operation = self._get_subobject(key)
            selected_operations.append(operation)
        
        # Create a new group instance with the selected operations
        new_group = group(name=f"{self._name}_subgroup", printflag=self.printflag, verbose=self.verbose)
        new_group._operations = selected_operations
        return new_group


    def operation_exists(self,operation_name):
        """
            Returns true if "operation_name" exists
            To be used by Operation, not by end-user, which should prefer find()
        """
        return any(op.name == operation_name for op in self._operations)

    def get_by_name(self,operation_name):
        """
            Returns the operation matching "operation_name"
            Usage: group.get_by_name("operation_name")
            To be used by Operation, not by end-user, which should prefer getattr()
        """
        for op in self._operations:
            if op.name == operation_name:
                return op
        raise AttributeError(f"Operation with name '{operation_name}' not found.")

    def add_operation(self,operation):
        """ add an operation """
        if operation.name in self.list():
            raise ValueError(f"The operation '{operation.name}' already exists.")
        else:
            self._operations.append(operation)

    # --------- LAMMPS methods

    def variable(self, variable_name, expression, style="atom"):
        """
        Assigns an expression to a LAMMPS variable.
    
        Parameters:
        - variable_name (str): The name of the variable to be assigned.
        - expression (str): The expression to assign to the variable.
        - style (str): The type of variable (default is "atom").
        """
        if not isinstance(variable_name, str):
            raise TypeError(f"Variable name must be a string, got {type(variable_name)}")
        if not isinstance(expression, str):
            raise TypeError(f"Expression must be a string, got {type(expression)}")
        if not isinstance(style, str):
            raise TypeError(f"Style must be a string, got {type(style)}")
    
        lammps_code = f"variable {variable_name} {style} \"{expression}\""
        op = Operation("variable", [variable_name, expression], code=lammps_code)
        self.add_operation(op)
        
    
    def byvariable(self, group_name, variable_name):
        """
        Sets a group of atoms based on a variable.
    
        Parameters:
        - group_name: str, the name of the group.
        - variable_name: str, the name of the variable to define the group.
        """
        if not isinstance(group_name, str):
            raise TypeError(f"Group name must be a string, got {type(group_name)}")
        if not isinstance(variable_name, str):
            raise TypeError(f"Variable name must be a string, got {type(variable_name)}")
    
        lammps_code = f"group {group_name} variable {variable_name}"
        op = Operation("byvariable", [variable_name], name=group_name, code=lammps_code)
        self.add_operation(op)


    def byregion(self, group_name, region_name):
        """
            set a group of atoms based on a regionID
            G.region(group_name,regionID)
        """
        lammps_code = f"group {group_name} region {region_name}"
        criteria = {"region": region_name}
        op = Operation("byregion", [region_name], name=group_name, code=lammps_code, criteria=criteria)
        self.add_operation(op)

    def bytype(self,  group_name, type_values):
        """
            select atoms by type and store them in group
            G.type(group_name,type_values)
        """
        if not isinstance(type_values, (list, tuple)):
            type_values = [type_values]
        lammps_code = f"group {group_name} type {span(type_values)}"
        criteria = {"type": type_values}
        op = Operation("bytype", type_values, name=group_name, code=lammps_code, criteria=criteria)
        self.add_operation(op)

    def byid(self, group_name, id_values):
        """
            select atoms by id and store them in group
            G.id(group_name,id_values)
        """
        if not isinstance(id_values, (list, tuple)):
            id_values = [id_values]
        lammps_code = f"group {group_name} id {span(id_values)}"
        criteria = {"id": id_values}
        op = Operation("byid", id_values, name=group_name, code=lammps_code, criteria=criteria)
        self.add_operation(op)

    def create(self, group_name):
        """
            create group
            G.create(group_name)
        """
        lammps_code = f"group {group_name} clear"
        criteria = {"clear": True}
        op = Operation("create", [], name=group_name, code=lammps_code, criteria=criteria)
        self.add_operation(op)

    def clear(self, group_name):
        """
            clear group
            G.clear(group_name)
        """
        lammps_code = f"group {group} clear"
        criteria = {"clear": True}
        op = Operation("clear", [], name=group_name, code=lammps_code, criteria=criteria)
        self.add_operation(op)


    def union(self,group_name, *groups):
        """
        Union group1, group2, group3 and store the result in group_name.
        Example usage:
        group.union(group_name, group1, group2, group3,...)
        """
        lammps_code = f"group {group_name} union {span(groups)}"
        criteria = {"union": groups}
        op = Operation("union", groups, name=group_name, code=lammps_code, criteria=criteria)
        self.add_operation(op)


    def intersect(self,group_name, *groups):
        """
        Intersect group1, group2, group3 and store the result in group_name.
        Example usage:
        group.intersect(group_name, group1, group2, group3,...)
        """
        lammps_code = f"group {group_name} intersect {span(groups)}"
        criteria = {"intersect": groups}
        op = Operation("intersect", groups, name=group_name, code=lammps_code, criteria=criteria)
        self.add_operation(op)
        

    def subtract(self,group_name, *groups):
        """
        Subtract group2, group3 from group1 and store the result in group_name.
        Example usage:
        group.subtract(group_name, group1, group2, group3,...)
        """
        lammps_code = f"group {group_name} subtract {span(groups)}"
        criteria = {"subtract": groups}
        op = Operation("subtract", groups, name=group_name, code=lammps_code, criteria=criteria)
        self.add_operation(op)


    def evaluate(self, group_name, group_op):
        """
        Evaluates the operation and stores the result in a new group.
        Expressions could combine +, - and * like o1+o2+o3-o4+o5+o6

        Parameters:
        -----------
        groupname : str
            The name of the group that will store the result.
        group_op : Operation
            The operation to evaluate.
        """
        if not isinstance(group_op, Operation):
            raise TypeError("Expected an instance of Operation.")
    
        if group_name in self.list():
            raise ValueError(f"The operation '{group_name}' already exists.")
    
        # If the operation is already finalized, no need to evaluate
        if group_op.isfinalized():
            if group_op.name != group_name:
                # If names differ, create a copy with the new name
                self.copy(group_op.name, group_name)
            return
    
        # Recursively evaluate operands
        operand_names = []
        for op in group_op.operands:
            if isinstance(op, Operation):
                if op.isfinalized():
                    # Use existing finalized operation name
                    operand_names.append(op.name)
                else:
                    # Generate a unique name if the operation doesn't have one
                    if not op.name:
                        op.name = op.generate_hashname()
                    # Recursively evaluate the operand operation
                    self.evaluate(op.name, op)
                    operand_names.append(op.name)
            else:
                operand_names.append(str(op))
    
        # Call the appropriate method based on the operator
        if group_op.operator == '+':
            self.union(group_name, *operand_names)
            group_op.operator = 'union'
        elif group_op.operator == '-':
            self.subtract(group_name, *operand_names)
            group_op.operator = 'subtract'
        elif group_op.operator == '*':
            self.intersect(group_name, *operand_names)
            group_op.operator = 'intersect'
        else:
            raise ValueError(f"Unknown operator: {group_op.operator}")
    
        # Update the operation
        group_op.name = group_name
        # Get the last added operation
        finalized_op = self._operations[-1]
        group_op.code = finalized_op.code
        group_op.operands = operand_names
    
        # Add the operation to the group's _operations if not already added
        if group_op.name not in self.list():
            self._operations.append(group_op)
            
            
    def add_group_criteria(self, *args, **kwargs):
        """
        Adds group(s) using existing methods based on key-value pairs.
    
        Supports two usages:
        1. add_group_criteria(group_name, **criteria)
        2. add_group_criteria(group_definitions)
    
        Parameters:
        - group_name (str): The name of the group.
        - **criteria: Criteria for group creation.
    
        OR
    
        - group_definitions (dict): A dictionary where keys are group names and values are criteria dictionaries.
    
        Raises:
        - TypeError: If arguments are invalid.
    
        Usage:
        - G.add_group_criteria('group_name', type=[1,2])
        - G.add_group_criteria({'group1': {'type': [1]}, 'group2': {'region': 'regionID'}})
        """
        if len(args) == 1 and isinstance(args[0], dict):
            # Called with group_definitions dict
            group_definitions = args[0]
            for group_name, criteria in group_definitions.items():
                self.add_group_criteria_single(group_name, **criteria)
        elif len(args) == 1 and isinstance(args[0], str):
            # Called with group_name and criteria
            group_name = args[0]
            if not kwargs:
                raise ValueError(f"No criteria provided for group '{group_name}'.")
            self.add_group_criteria_single(group_name, **kwargs)
        else:
            raise TypeError("Invalid arguments. Use add_group_criteria(group_name, **criteria) or add_group_criteria(group_definitions).")

    
    def add_group_criteria_single(self, group_name, **criteria):
        """
        Adds a single group based on criteria.
    
        Parameters:
        - group_name (str): The name of the group.
        - **criteria: Criteria for group creation.
    
        Raises:
        - TypeError: If group_name is not a string.
        - ValueError: If no valid criteria are provided or if criteria are invalid.
        
        
        Example (advanced):
            G = group()
            group_definitions = {
                'myGroup': {
                    'variable': {
                        'name': 'myVar',
                        'expression': 'x > 5',
                        'style': 'atom'
                    }
                }
            }
            G.add_group_criteria(group_definitions)
            print(G.code())
            
        Expected output
            variable myVar atom "x > 5"
            group myGroup variable myVar
        """
        if not isinstance(group_name, str):
            raise TypeError(f"Group name must be a string, got {type(group_name)}")
    
        if not criteria:
            raise ValueError(f"No criteria provided for group '{group_name}'.")
    
        if "type" in criteria:
            type_values = criteria["type"]
            if not isinstance(type_values, (list, tuple, int)):
                raise TypeError("Type values must be an integer or a list/tuple of integers.")
            self.bytype(group_name, type_values)
    
        elif "region" in criteria:
            region_name = criteria["region"]
            if not isinstance(region_name, str):
                raise TypeError("Region name must be a string.")
            self.byregion(group_name, region_name)
    
        elif "id" in criteria:
            id_values = criteria["id"]
            if not isinstance(id_values, (list, tuple, int)):
                raise TypeError("ID values must be an integer or a list/tuple of integers.")
            self.byid(group_name, id_values)
    
        elif "variable" in criteria:
            var_info = criteria["variable"]
            if not isinstance(var_info, dict):
                raise TypeError("Variable criteria must be a dictionary.")
            required_keys = {'name', 'expression'}
            if not required_keys.issubset(var_info.keys()):
                missing = required_keys - var_info.keys()
                raise ValueError(f"Variable criteria missing keys: {missing}")
            var_name = var_info['name']
            expression = var_info['expression']
            style = var_info.get('style', 'atom')
    
            # First, assign the variable
            self.variable(var_name, expression, style)
    
            # Then, create the group based on the variable
            self.byvariable(group_name, var_name)
    
        elif "union" in criteria:
            groups = criteria["union"]
            if not isinstance(groups, (list, tuple)):
                raise TypeError("Union groups must be a list or tuple of group names.")
            self.union(group_name, *groups)
    
        elif "intersect" in criteria:
            groups = criteria["intersect"]
            if not isinstance(groups, (list, tuple)):
                raise TypeError("Intersect groups must be a list or tuple of group names.")
            self.intersect(group_name, *groups)
    
        elif "subtract" in criteria:
            groups = criteria["subtract"]
            if not isinstance(groups, (list, tuple)):
                raise TypeError("Subtract groups must be a list or tuple of group names.")
            self.subtract(group_name, *groups)
    
        elif "create" in criteria and criteria["create"]:
            self.create(group_name)
    
        elif "clear" in criteria and criteria["clear"]:
            self.clear(group_name)
    
        else:
            raise ValueError(f"No valid criterion provided for group '{group_name}'.")



    
    def get_group_criteria(self, group_name):
        """
        Retrieve the criteria that define a group. Handles group_name as a string or number.
        
        Parameters:
        - group_name: str or int, the name or number of the group.
        
        Returns:
        - dict or str: The criteria used to define the group, or a message if defined by multiple criteria.
        
        Raises:
        - ValueError: If the group does not exist.
        """
        # Check if group_name exists in _operations
        if group_name not in self._operations:
            raise ValueError(f"Group '{group_name}' does not exist.")
        
        # Retrieve all operations related to the group directly from _operations
        operations = self._operations[group_name]
        
        if not operations:
            raise ValueError(f"No operations found for group '{group_name}'.")
    
        criteria = {}
        for op in operations:
            if op.criteria:
                criteria.update(op.criteria)
        
        # If multiple criteria, return a message
        if len(criteria) > 1:
            return f"Group '{group_name}' is defined by multiple criteria: {criteria}"
        
        return criteria



    def dscript(self, name=None, printflag=None, verbose=None):
        """
        Generates a dscript object containing the group's LAMMPS commands.

        Parameters:
        - name (str): Optional name for the script object.
        - printflag (bool, default=False): print on the current console if True
        - verbose (bool, default=True): keep comments if True

        Returns:
        - dscript: A dscript object containing the group's code.
        """
        if name is None:
            name = self._name
        printflag = self.printflag if printflag is None else printflag
        verbose = self.verbose if verbose is None else verbose

        # Create a new dscript object
        dscript_obj = dscript(name=name,printflag=printflag, verbose=verbose)

        # Add each line of the group's code to the script object
        for idx, op in enumerate(self._operations):
            # Use the index as the key for the script line
           dscript_obj[idx] = op.code

        return dscript_obj
        
    
    def script(self, name=None, printflag=None, verbose=None):
        """
        Generates a script object containing the group's LAMMPS commands.
        
        Parameters:
        - name (str): Optional name for the script object.
        - printflag (bool, default=False): print on the current console if True
        - verbose (bool, default=True): keep comments if True

        Returns:
        - script: A script object containing the group's code.
        """
        if name is None:
            name = self._name
        printflag = self.printflag if printflag is None else printflag
        verbose = self.verbose if verbose is None else verbose
            
        script_obj = self.dscript(name=name,printflag=printflag, verbose=verbose).script(printflag=printflag, verbose=verbose)
        return script_obj
    
    
    def pipescript(self, printflag=None, verbose=None):
        """
        Generates a pipescript object containing the group's LAMMPS commands.
                
        Parameters:
        - printflag (bool, default=False): print on the current console if True
        - verbose (bool, default=True): keep comments if True

        Returns:
        - pipescript: A pipescript object containing the group's code lines as individual scripts in the pipeline.
        """
        printflag = self.printflag if printflag is None else printflag
        verbose = self.verbose if verbose is None else verbose
        # Create a list to hold script objects
        script_list = []

        # For each operation, create a script object and add it to the list
        for op in self._operations:
            # Create a dscript object with the code line
            dscript_obj = dscript(printflag=printflag, verbose=verbose)
            dscript_obj["dummy"] = op.code

            # Convert the dscript to a script object
            script_obj = dscript_obj.script(printflag=printflag, verbose=verbose)

            # Add the script object to the list
            script_list.append(script_obj)

        # Use the static method 'join' to create a pipescript from the list
        if script_list:
            pipe_obj = pipescript.join(script_list)
        else:
            pipe_obj = pipescript()

        return pipe_obj

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
            setattr(copie, k, copy.deepcopy(v, memo))
        return copie 

# %% debug section - generic code to test methods (press F5)
if __name__ == '__main__':

    # Example Usage
    G = group()
    G.variable("groupname","variablename","myexpression myexpression myexpression myexpression and again 1234")
    print(G.disp("groupname"))

    G.byregion("regiongroup","myregionID")
    print(G.disp("regiongroup"))

    G.union("uniongroup","group1","group2","group3")
    print(G.disp("uniongroup"))
    
    # LAMMPS example
    #     group myGroup region myRegion
    #     group typeGroup type 1 2
    #     variable myVar atom "x + y"
    #     group varGroup variable myVar
    #     group unionGroup union myGroup typeGroup
    # Assuming Operation class is properly defined and includes necessary methods
    G0 = group()
    G0.byregion('myGroup', 'myRegion')
    G0.bytype('typeGroup', [1, 2])
    G0.variable('myVar', 'x + y')
    G0.byvariable('varGroup', 'myVar')
    # Perform group operations
    union_op = G0['myGroup'] + G0['typeGroup']
    G0.evaluate('unionGroup', union_op)
    # Generate LAMMPS script
    print(G0.code())
    

    # Advanced Usage
    G = group()
    G.create_groups('o1', 'o2', 'o3', 'o4')
    G.create('o5')
    G.create('o6')
    G.create('o7')
    G.evaluate("debug0",G.o1+G.o2+G.o3 + G.o4 + (G.o5 +G.o6) + G.o7)
    G.evaluate("debug1",G.o1+G.o2)
    G.evaluate("debug2",G.o1+G.o2+G.o3-(G.o4+G.o5)+(G.o6*G.o7))
    print(repr(G))
    
    # Example to prepare workshop
    G = group()
    G.add_group_criteria("lower", type=[1])
    G.add_group_criteria("central", region="central_cyl")
    G.add_group_criteria("new_group", create=True)
    G.add_group_criteria("upper", clear=True)
    G.add_group_criteria("subtract_group", subtract=["group1", "group2"])

    
