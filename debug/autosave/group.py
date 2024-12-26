#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__project__ = "Pizza3"
__author__ = "Olivier Vitrac, Han Chen"
__copyright__ = "Copyright 2023"
__credits__ = ["Olivier Vitrac","Han Chen"]
__license__ = "GPLv3"
__maintainer__ = "Olivier Vitrac"
__email__ = "olivier.vitrac@agroparistech.fr"
__version__ = "0.61"


"""

===============================================
          pizza.group Class Manual
===============================================

-- SYNOPSIS --
The `group` class in Python is designed to interact with LAMMPS groups, allowing users to create, modify, and manage groups of atoms in a LAMMPS simulation. In LAMMPS, groups are used to assign a set of atoms to a named group, which can then be referred to in other commands. The `group` class provides a Python interface to these functionalities.

The groups are stored and managed via a collection of operations in atoms.

pizza.group() execute all operations statically and cannot be used dynamically as pizza.region. This choice was imposed
by the nature of the groups, which represent atoms and not complex geometries, which need additional parameterization.


------------------
High-Level Methods
------------------

'region(group, regionID)'
  - Description: Set a group of atoms based on a regionID.
  - Usage: G.region('group_name', 'regionID')
  - LAMMPS Example:
      region myRegion block 0 10 0 10 0 10 units box
      group myGroup region myRegion

'type(group, typevalues)'
  - Description: Select atoms by type and store them in group.
  - Usage: G.type('group_name', 'type_values')
  - LAMMPS Example:
      group myGroup type 1 2

'id(group, idvalues)'
  - Description: Select atoms by id and store them in group.
  - Usage: G.id('group_name', 'id_values')
  - LAMMPS Example:
      group myGroup id 1 2 3

'union(group, group1, *othergroups)'
  - Description: Union of multiple groups.
  - Usage: G.union('new_group', 'group1', 'group2', ...)
  - LAMMPS Example:
      group newGroup union group1 group2

'intersect(group, group1, *othergroups)'
  - Description: Intersection of multiple groups.
  - Usage: G.intersect('new_group', 'group1', 'group2', ...)
  - LAMMPS Example:
      group newGroup intersect group1 group2

'subtract(group, group1, *othergroups)'
  - Description: Subtract multiple groups from a group.
  - Usage: G.subtract('new_group', 'group1', 'group2', ...)
  - LAMMPS Example:
      group newGroup subtract group1 group2

'eval(groupname, group_op)'
  - Description: Evaluates group operations like 'o1+o2+o3-o4' and stores the result in a new group.
  - Usage: G.eval('new_group', group_op)

-----------------
Low-Level Methods
-----------------

'list()'
  - Description: Return the list of all operations.
  - Usage: G.list()

'find(name)'
  - Description: Find and return the index of an operation based on the group name.
  - Usage: G.find('operation_name')

'delete(name)'
  - Description: Delete a stored operation based on its name.
  - Usage: G.delete('operation_name')

'copy(source_name, new_name)'
  - Description: Copy a stored operation to a new operation with a different name.
  - Usage: G.copy('source_operation', 'new_operation')

'rename(old_name, new_name)'
  - Description: Rename a stored operation.
  - Usage: G.rename('old_operation_name', 'new_operation_name')

'reindex(name, new_idx)'
  - Description: Change the index of a stored operation.
  - Usage: G.reindex('operation_name', new_index)


This short manual includes method descriptions, expected parameters, and examples of usage for each method in the `group` class, separated into high-level (which directly correspond to LAMMPS commands) and low-level methods (which manipulate the internal `_operations` attribute of the `group` class).



==============================================
pizza.group Class Manual with LAMMPS Examples
==============================================

------------------
High-Level Methods
------------------

'region(group, regionID)'
  Description: Set a group of atoms based on a regionID.
  Usage: G.region('group_name', 'regionID')
  Examples:
    In LAMMPS:
      region myRegion block 0 10 0 10 0 10 units box
      group myGroup region myRegion
    In Python with this group class:
      G = group()
      G.region('myGroup', 'myRegion')


-----------------
Low-Level Methods
-----------------

'list()'
  Description: Return the list of all operations.
  Usage: G.list()
  Examples:
    G = group()
    G.region('myGroup', 'myRegion')
    print(G.list())  # Output: ['myGroup']

'find(name)'
  Description: Find and return the index of an operation based on the group name.
  Usage: G.find('operation_name')
  Examples:
    G = group()
    G.region('myGroup', 'myRegion')
    print(G.find('myGroup'))  # Output: 0

'delete(name)'
  Description: Delete a stored operation based on its name.
  Usage: G.delete('operation_name')
  Examples:
    G = group()
    G.region('myGroup', 'myRegion')
    G.delete('myGroup')
    print(G.list())  # Output: []

'copy(source_name, new_name)'
  Description: Copy a stored operation to a new operation with a different name.
  Usage: G.copy('source_operation', 'new_operation')
  Examples:
    G = group()
    G.region('myGroup', 'myRegion')
    G.copy('myGroup', 'copiedGroup')
    print(G.list())  # Output: ['myGroup', 'copiedGroup']

'rename(old_name, new_name)'
  Description: Rename a stored operation.
  Usage: G.rename('old_operation_name', 'new_operation_name')
  Examples:
    G = group()
    G.region('myGroup', 'myRegion')
    G.rename('myGroup', 'renamedGroup')
    print(G.list())  # Output: ['renamedGroup']

'reindex(name, new_idx)'
  Description: Change the index of a stored operation.
  Usage: G.reindex('operation_name', new_index)
  Examples:
    G = group()
    G.region('myGroup1', 'myRegion1')
    G.region('myGroup2', 'myRegion2')
    G.reindex('myGroup1', 1)
    print(G.list())  # Output: ['myGroup2', 'myGroup1']



This short manual includes method descriptions, expected parameters, and examples of usage for each method in the `group` class, separated into high-level (which directly correspond to LAMMPS commands) and low-level methods (which manipulate the internal `_operations` attribute of the `group` class). The examples demonstrate how you can use the `group` class to manage groups of atoms and operations in a Python script, mimicking some of the functionalities you would have in a LAMMPS script.


## Notes:

- The `group` class is designed to be a Pythonic interface to LAMMPS group functionalities.
- The actual implementation needs to communicate with a running LAMMPS simulation, which may require additional code and setup via pizza.


## Comment on Sept 2nd, 2023

On September 2nd, a re-evaluation of the `pizza.group.GroupOperation()` and `pizza.group.Operation()` classes was initiated to simplify their complexities. The existing architecture mandated a convoluted process for collapsing operations, making it cumbersome to manage. To address this, the concept of finalized and non-finalized operations was introduced.

Finalized operations are those explicitly invoked, like union, intersection, identification, and region, executed directly via the `pizza.group` methods. Non-finalized operations, in contrast, are intermediary steps that are automatically generated when evaluating expressions that use overloaded operators such as `+`, `-`, and `*`. For instance, in an expression like `o1 + o2 + o3 - (o4 + o5) + (o6 * o7)`, the operations formed between the operands are non-finalized.

This refactoring streamlines the handling of both types of operations, thus eliminating the need for an intricate collapse mechanism. It offers a more intuitive and efficient way to manage operations within the `pizza.group` framework.

Here the output for o1 + o2 + o3 - (o4 + o5) + (o6 * o7)

| Idx |     Name    | Operator  |           Operands           |
|-----|-------------|-----------|------------------------------|
|  0  |          o1 |    create |                              |
|  1  |          o2 |    create |                              |
|  2  |          o3 |    create |                              |
|  3  |          o4 |    create |                              |
|  4  |          o5 |    create |                              |
|  5  |          o6 |    create |                              |
|  6  |          o7 |    create |                              |
|  7  |   addae928c |     union |        ('o1', 'o2', 'o3')    |
|  8  |   add22d686 |     union |           ('o4', 'o5')       |
|  9  |   subb3d152 |  subtract | ('addae928c', 'add22d686')   |
| 10  |   mul48e45f | intersect |           ('o6', 'o7')       |
| 11  |      debug  |     union | ('subb3d152', 'mul48e45f')   |


---



Created on Wed Aug 16 16:25:19 2023

@author: olivi
"""

# Revision history
# 2023-08-17 RC with documentation, the script method is not implemented yet (to be done via G.code())
# 2023-08-18 consolidation of the GroupOperation mechanism (please still alpha version)
# 2023-09-01 the class GroupOperation has been removed and the collapse is carried within Operation to avoid unecessary complications [major release]

# %% Dependencies
# pizza.group is independent of region and can performs only static operations.
# It is designed to be compatible with region via G.script()
import hashlib
from pizza.script import script, span

# %% Private classes
# Class for binary and unary operators
class Operation:
    """
        Represents a single LAMMPS operation, which consists of an operator, operands, a name, and a code.

        Attributes
        ----------
        operator (str): The operator applied to the operands.
                        It can be a finalized operator 'variable','region','type','id',
                        'create','clear','empty','union','intersect','subtact','eval'
                        It Can be '+', '-', '*' or empty.

        operands (list): A list of operands for the operation.

        name (str): The name of this operation, which can be manually set or auto-generated.

        code (str): The LAMMPS code that this operation represents.


        Methods
        -------
        __init__(self, operator, operands, name="", code="")
            Initializes a new Operation instance.
        append(self, operand)
            Appends a single operand to the operands list.
        extend(self, operands)
            Extends the operands list with multiple operands.
        is_unary(self)
            Checks if the Operation instance has exactly one operand.
        is_empty(self)
            Checks if the Operation instance has no operands.
        generateID(self)
            Generates an ID for the instance based on its operands or name.
        generate_hashname(self, prefix="grp", ID=None)
            Generates a hash-based name for the instance.
        _operate(self, other, operator)
            Combines the operation with another Operation instance
            using the specified operator.
        _eval(self, group_name)
            Evaluates the operation and stores it in the Group.
        isfinalized(self)
            Checks if the operation has been finalized.
        __add__(other):
            Overloads the '+' operator to support adding two Operation instances.
        __sub__(other):
            Overloads the '-' operator to support subtracting two Operation instances.
        __mul__(other):
            Overloads the '*' operator to support multiplying two Operation instances.
    """

    def __init__(self, operator, operands, name="",code=""):
        """Initializes a new Operation instance with given parameters."""
        self.operator = operator
        self.operands = operands if isinstance(operands, list) else [operands]
        if (name == "") or name is None:
            self.name = self.generate_hashname()
        else:
            self.name = name
        self.code = code

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
        if self.operands:
            return "".join([str(op) for op in self.operands])
        else:
            return self.name

    def generate_hashname(self,prefix="grp",ID=None):
        """Generates an ID for the Operation instance based on its operands or name."""
        if ID is None: ID = self.generateID()
        s = self.operator+ID
        return prefix+hashlib.sha256(s.encode()).hexdigest()[:6]

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
        return self.operator not in ['+', '-', '*']

    def eval(self, group_name):
        """
        Evaluates and finalizes the Operation, updating it with a new state.

        Parameters:
        - group_name (str): The name of the group in which to store the final operation.

        Functionality:
        - Executes the operation based on the current algebraic operator and
          updates the attributes accordingly.
        - If the operation is already finalized, a ValueError is raised.
        - Uses group (assumed to be an instance of Group) to perform union,
          subtraction, or intersection, depending on the operator.

        Exception Handling:
        - Raises a ValueError if the operation is already finalized or if
          an unknown operator is used.
        """
        if not self.isfinalized():
            if self.operator == '+':
                group.union(group_name, *self.operands)
            elif self.operator == '-':
                group.subtract(group_name, *self.operands)
            elif self.operator == '*':
                group.intersect(group_name, *self.operands)
            else:
                raise ValueError(f"Unknown operator: {self.operator}")
            # Retrieve the newly created operation from Group
            new_op = group.get_by_name(group_name)
            # Update the current instance with attributes of the new operation
            self.__dict__.update(new_op.__dict__)
            # At this point, self should be considered finalized
        else:
            raise ValueError("Operation is already finalized.")

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
        """
        Returns the proper operand depending on whether the operation is finalized.
        """
        return span(self.operands) if not self.isfinalized() else self.name

    def _operate(self, other, operator):
        """
        Implements algebraic operations between self and other Operation instances.

        Parameters:
        - other (Operation): The other Operation instance to be operated with.
        - operator (str): The operation to be performed. Supported values are '+', '-', '*'.

        Returns:
        - Operation: A new or modified Operation instance reflecting the result of the operation.

        Functionality:
        - Verifies that the 'other' parameter is an instance of the Operation class.
        - Utilizes a map to link algebraic symbols ('+', '-', '*') to their respective
          operation types ('add', 'sub', 'mul').
        - Adheres to four specific cases to handle different combinations of operators:

          Case A: When neither self nor other have operators.
          - Generates a new Operation that contains both as operands.

          Case B: When either self or other (or both) have the same operator as the
          current operation or no operators.
          - Extends the operands of the Operation instance that has a matching operator.
          - If one of the instances has no operator, it becomes an operand of the other.

          Case C: When both self and other have the same operator.
          - Extends the operands of self with the operands of other.

          Default Case: When no cases match.
          - Finalizes the existing Operations if they are not yet finalized.
          - Creates a new intermediate Operation combining both.

        Exception Handling:
        - Raises a TypeError if 'other' is not an instance of Operation.
        """

        # Ensure other is also an instance of Operation
        if not isinstance(other, Operation):
            raise TypeError(f"Unsupported type: {type(other)}")
        prefix_map = {'+': 'add', '-': 'sub', '*': 'mul'}
        # Case A
        if (self.operator in ["", None]) and (other.operator in ["", None]):
            name = self.generate_hashname(prefix=prefix_map[operator])
            new_op = Operation(operator, [self.get_proper_operand(), other.get_proper_operand()], name=name)
            return new_op
        # Case B (Revised #1)
        if (self.operator in [operator, "", None]) or (other.operator in [operator, "", None]):
            if self.operator == operator:
                self.operands.append(other.get_proper_operand())
                return self
            elif other.operator == operator:
                other.operands.append(self.get_proper_operand())
                return other
            else:
                # Whichever has an empty operator becomes part of the other operation
                if self.operator in ["", None]:
                    other.operands.append(self.get_proper_operand())
                    return other
                else:
                    self.operands.append(other.get_proper_operand())
                    return self
        # Case C
        if self.operator == operator and other.operator == operator:
            self.operands.extend(other.operands)
            return self
        # Default case: finalize existing operations and create a new intermediate one
        else:
            self.eval(self.name) if not self.isfinalized() else None
            other.eval(other.name) if not other.isfinalized() else None
            name = self.generate_hashname(prefix=prefix_map[operator],ID=self.generateID()+other.generateID())
            new_op = Operation(operator, [self.get_proper_operand(), other.get_proper_operand()], name=name)
            return new_op



# %% Main class group
class group:

    _operations = []

    def __str__(self):
        return f"Number of operations stored: {len(group._operations)}"

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

        table = "| "
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

        return table


    def __len__(self):
        """ return the number of stored operations """
        return len(self._operations)

    @staticmethod
    def list():
        """ return the list of all operations """
        return [op.name for op in group._operations]

    def code(self):
        """
            Joins the `code` attributes of all stored `operation` objects with '\n'.
        """
        return '\n'.join([op.code for op in group._operations])

    @staticmethod
    def find(name):
        """ returns the index of an operation based on the group name """
        for i, op in enumerate(group._operations):
            if op.name == name:
                return i
        return None

    def disp(self, name):
        """ display the content of an operation """
        idx = group.find(name)
        if idx is not None:
            return group._operations[idx].__repr__()
        else:
            return "Operation not found"

    def clearall(self):
        """ clear all operations """
        group._operations = []

    @staticmethod
    def delete(name):
        """
        Deletes a stored operation based on its name.

        Parameters:
        name: str
            Name of the operation to delete

        Usage:
        G.delete('operation_name')
        """
        idx = group.find(name)
        if idx is not None:
            del group._operations[idx]
        else:
            raise ValueError(f"Operation {name} not found.")

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
            copied_operation = group._operations[idx].clone()
            copied_operation.name = new_name
            group._operations.append(copied_operation)
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
            if new_name==old_name:
                raise ValueError("The new name should be different from the previous one")
            elif new_name in self.list():
                raise ValueError("Operation name must be unique.")
            group._operations[idx].name = new_name
        else:
            raise ValueError(f"Operation {old_name} not found.")

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
        if idx is not None and 0 <= new_idx < len(group._operations):
            op = group._operations.pop(idx)
            group._operations.insert(new_idx, op)
        else:
            raise ValueError(f"Operation {name} not found or new index {new_idx} out of range.")

    # ------------- indexing and attribute overloading

    def __getitem__(self, key):
        """
            Enable shorthand for G.operations[G.find(operation_name)] using G[operation_name],
            or accessing operation by index using G[index].
        """
        if isinstance(key, str):
            idx = self.find(key)
            if idx is not None:
                return group._operations[idx]
            else:
                raise KeyError(f"Operation {key} not found.")
        elif isinstance(key, int):
            if -len(group._operations) <= key < len(group._operations):
                return group._operations[key]
            else:
                raise IndexError("Operation index out of range.")
        else:
            raise TypeError("Key must be an operation name (string) or index (integer).")

    def __getattr__(self, operation_name):
        """
            Enables shorthand for G.operations[G.find(operation_name)],
            accessible via attribute-style notation like G.op1
        """
        if operation_name in self.__dict__:
            return self.__dict__[operation_name]
        idx = self.find(operation_name)
        if idx is not None:
            return group._operations[idx]
        else:
            raise AttributeError(f"Operation {operation_name} not found.")

    @staticmethod
    def operation_exists(operation_name):
        """
            Returns true if "operation_name" exists
            To be used by Operation, not by end-user, which should prefer find()
        """
        return any(op.name == operation_name for op in group._operations)

    @staticmethod
    def get_by_name(operation_name):
        """
            Returns the operation matching "operation_name"
            Usage: group.get_by_name("operation_name")
            To be used by Operation, not by end-user, which should prefer getattr()
        """
        for op in group._operations:
            if op.name == operation_name:
                return op
        raise AttributeError(f"Operation with name {operation_name} not found.")

    @staticmethod
    def add_operation(operation):
        """ add an operation """
        if operation.name in group.list():
            print(f"the operation {operation.name} is not created as it already exists")
            #raise ValueError("Operation name must be unique.")
        else:
            group._operations.append(operation)

    # --------- LAMMPS methods

    def variable(self, group, variable, expression, style="atom"):
        """
            set a group of atoms based on the result of an expression stored in variable
            G.variable(group,variablename,expression,style)
            default style = "atom"
        """
        lammps_code = f"variable {variable} {style} \"{expression}\"\ngroup {group} variable {variable}"
        op = Operation("variable", [variable, expression], name=group, code=lammps_code)
        self.add_operation(op)

    def region(self, group, regionID):
        """
            set a group of atoms based on a regionID
            G.region(group,regionID)
        """
        lammps_code = f"group {group} region {regionID}"
        self.add_operation(Operation("region", [regionID], name=group, code=lammps_code))

    def type(self, group, typevalues):
        """
            select atoms by type and store them in group
            G.type(group,typevalues)
        """
        lammps_code = f"group {group} type {span(typevalues)}"
        self.add_operation(Operation("type", [typevalues], name=group, code=lammps_code))

    def id(self, group, idvalues):
        """
            select atoms by id and store them in group
            G.id(group,idvalues)
        """
        lammps_code = f"group {group} id {span(idvalues)}"
        self.add_operation(Operation("id", [idvalues], name=group, code=lammps_code))

    def create(self, group):
        """
            create group
            G.create(group)
        """
        lammps_code = f"# dummy creation of {group}"
        self.add_operation(Operation("create", [], name=group, code=lammps_code))

    def clear(self, group):
        """
            clear group
            G.clear(group)
        """
        lammps_code = f"group {group} clear"
        self.add_operation(Operation("clear", [], name=group, code=lammps_code))

    def empty(self, group):
        """
            empty group
            G.empty(group)
        """
        lammps_code = f"group {group} empty"
        self.add_operation(Operation("empty", [], name=group, code=lammps_code))

    @staticmethod
    def union(group_name, *groups):
        """
        Union group1, group2, group3 and store the result in group_name.
        Example usage:
        group.union(group_name, group1, group2, group3,...)
        """
        lammps_code = f"group {group_name} union " + span(groups)
        group.add_operation(Operation("union", groups, name=group_name, code=lammps_code))

    @staticmethod
    def intersect(group_name, *groups):
        """
        Intersect group1, group2, group3 and store the result in group_name.
        Example usage:
        group.intersect(group_name, group1, group2, group3,...)
        """
        lammps_code = f"group {group_name} intersect " + span(groups)
        group.add_operation(Operation("intersect", groups, name=group_name, code=lammps_code))

    @staticmethod
    def subtract(group_name, *groups):
        """
        Subtract group2, group3 from group1 and store the result in group_name.
        Example usage:
        group.subtract(group_name, group1, group2, group3,...)
        """
        lammps_code = f"group {group_name} subtract " + span(groups)
        group.add_operation(Operation("subtract", groups, name=group_name, code=lammps_code))


    def eval(self, groupname, group_op):
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
        if groupname:
            group_op.name = groupname
        if not group_op.isfinalized():
            group_op = group_op.eval(groupname)
        return group_op




# %% debug section - generic code to test methods (press F5)
if __name__ == '__main__':

    # Example Usage
    # G = group()
    # G.variable("groupname","variablename","myexpression myexpression myexpression myexpression and again 1234")
    # print(G.disp("groupname"))

    # G.region("regiongroup","myregionID")
    # print(G.disp("regiongroup"))

    # G.union("uniongroup","group1","group2","group3")
    # print(G.disp("uniongroup"))

    # Advanced Usage
    G = group()
    G.create('o1')
    G.create('o2')
    G.create('o3')
    G.create('o4')
    G.create('o5')
    G.create('o6')
    G.create('o7')
    #G.eval("debug",G.o1+G.o2+G.o3 + G.o4 + (G.o5 +G.o6) + G.o7)
    G.eval("debug",G.o1+G.o2+G.o3-(G.o4+G.o5)+(G.o6*G.o7))
    print(repr(G))0
