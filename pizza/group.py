#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__project__ = "Pizza3"
__author__ = "Olivier Vitrac, Han Chen"
__copyright__ = "Copyright 2023"
__credits__ = ["Olivier Vitrac","Han Chen"]
__license__ = "GPLv3"
__maintainer__ = "Olivier Vitrac"
__email__ = "olivier.vitrac@agroparistech.fr"
__version__ = "0.60"


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

---



Created on Wed Aug 16 16:25:19 2023

@author: olivi
"""

# Revision history
# 17/08/2023 RC with documentation, the script method is not implemented yet (to be done via G.code())

# %% Dependencies
# pizza.group is independent of region and can performs only static operations.
# It is designed to be compatible with region via G.script()
import hashlib
from pizza.script import script, span

# %% Private classes

# class for multiple heterogenerous operations
class GroupOperation:
    """
        A class to represent a sequence of operations combined using specific operators.

        Attributes
        ----------
            operations : list of Operation or GroupOperation
                The list of operations involved in this GroupOperation.
            operators : list of str
                The list of operators used to combine the operations.
                Operators are represented as strings, e.g., '+', '-', '*'.

        Methods
        -------
            __init__(operation1, operation2, operator):
                Initialize a GroupOperation instance with two Operation or GroupOperation instances and an operator.
            __add__(other):
                Overloads the '+' operator to support adding two GroupOperation or Operation instances.
            __sub__(other):
                Overloads the '-' operator to support subtracting two GroupOperation or Operation instances.
            __mul__(other):
                Overloads the '*' operator to support multiplying two GroupOperation or Operation instances.

    """

    def __init__(self, operation1, operation2, operator):
        if not isinstance(operation1, (Operation, GroupOperation)) or not isinstance(operation2, (Operation, GroupOperation)):
            raise TypeError("Expected instances of Operation or GroupOperation.")

        self.operations = []
        self.operators = []

        if isinstance(operation1, GroupOperation):
            self.operations.extend(operation1.operations)
            self.operators.extend(operation1.operators)
        else:
            self.operations.append(operation1)

        self.operators.append(operator)

        if isinstance(operation2, GroupOperation):
            self.operations.extend(operation2.operations)
            self.operators.extend(operation2.operators)
        else:
            self.operations.append(operation2)

    def __add__(self, other):
        return GroupOperation(self, other, '+')

    def __sub__(self, other):
        return GroupOperation(self, other, '-')

    def __mul__(self, other):
        return GroupOperation(self, other, '*')

    def __repr__(self):
        return ' '.join([str(self.operations[i]) + (' ' + self.operators[i] if i < len(self.operators) else '')
                         for i in range(len(self.operations))])



# Class for binary and unary operators
class Operation:
    """
        Represents a single LAMMPS operation, which consists of an operator, operands, a name, and a code.

        Attributes
        ----------
            operator (str): The operator for this operation
                (e.g., 'variable','region','type','id','create','clear','empty','union','intersect','subtact','eval')
                (oveloaded operators: 'add', 'sub', 'mul').
            operand1 (any): The first operand for this operation.
            operand2 (any): The second operand for this operation.
            name (str): The name of this operation, which can be manually set or auto-generated.
            code (str): The LAMMPS code that this operation represents.

        Methods
        -------
            generate_hashname():
                Generate a hash name for the operation.
            __add__(other):
                Overloads the '+' operator to support adding two Operation instances.
            __sub__(other):
                Overloads the '-' operator to support subtracting two Operation instances.
            __mul__(other):
                Overloads the '*' operator to support multiplying two Operation instances.
    """

    def __init__(self, operator, operand1, operand2, name="",code=""):
        self.operator = operator
        self.operand1 = operand1
        self.operand2 = operand2
        if name == "":
            self.name = self.generate_hashname()
        else:
            self.name = name
        self.code = code

    def generate_hashname(self):
        s = self.operator + str(self.operand1) + str(self.operand2)
        return hashlib.sha256(s.encode()).hexdigest()[:6]

    def __repr__(self):
        return f"{self.name}: {self.operator} {self.operand1} {self.operand2}"

    def __add__(self, other):
        return GroupOperation(self, other, '+')

    def __sub__(self, other):
        return GroupOperation(self, other, '-')

    def __mul__(self, other):
        return GroupOperation(self, other, '*')


# %% Main class group
class group:

    def __init__(self):
        self._operations = []

    def __str__(self):
        return f"Number of operations stored: {len(self._operations)}"

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
        headers = ["Idx", "Name", "Operation", "Operand 1", "Operand 2"]
        column_widths = [max(len(headers[0]), idx_width)] + [len(header) for header in headers[1:]]

        for op in self._operations:
            cells = [op.name, op.operator, op.operand1, op.operand2]
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
            formatted_name = self.format_cell_content(op.name, column_widths[1])
            formatted_operator = self.format_cell_content(op.operator, column_widths[2])
            formatted_operand1 = self.format_cell_content(span(op.operand1), column_widths[3])
            formatted_operand2 = self.format_cell_content(span(op.operand2), column_widths[4])

            table += f"| {formatted_idx:^{column_widths[0]}} | {formatted_name:^{column_widths[1]}} | "
            table += f"{formatted_operator:^{column_widths[2]}} | "
            table += f"{formatted_operand1:^{column_widths[3]}} | {formatted_operand2:^{column_widths[4]}} |\n"
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
        """ returns the index of an operation based on the group name """
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

    def delete(self, name):
        """
        Deletes a stored operation based on its name.

        Parameters:
        name: str
            Name of the operation to delete

        Usage:
        G.delete('operation_name')
        """
        idx = self.find(name)
        if idx is not None:
            del self._operations[idx]
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
            copied_operation = self._operations[idx].clone()
            copied_operation.name = new_name
            self._operations.append(copied_operation)
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
            self._operations[idx].name = new_name
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
        if idx is not None and 0 <= new_idx < len(self._operations):
            op = self._operations.pop(idx)
            self._operations.insert(new_idx, op)
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
                return self._operations[idx]
            else:
                raise KeyError(f"Operation {key} not found.")
        elif isinstance(key, int):
            if 0 <= key < len(self._operations):
                return self._operations[key]
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
            return self._operations[idx]
        else:
            raise AttributeError(f"Operation {operation_name} not found.")

    def add_operation(self, operation):
        """ add an operation """
        if operation.name in self.list():
            raise ValueError("Operation name must be unique.")
        self._operations.append(operation)

    # --------- LAMMPS methods

    def variable(self, group, variable, expression, style="atom"):
        """
            set a group of atoms based on the result of an expression stored in variable
            G.variable(group,variablename,expression,style)
            default style = "atom"
        """
        lammps_code = f"variable {variable} {style} \"{expression}\"\ngroup {group} variable {variable}"
        op = Operation("variable", variable, expression, name=group, code=lammps_code)
        self.add_operation(op)

    def region(self, group, regionID):
        """
            set a group of atoms based on a regionID
            G.region(group,regionID)
        """
        lammps_code = f"group {group} region {regionID}"
        self.add_operation(Operation("region", regionID, None, name=group, code=lammps_code))

    def type(self, group, typevalues):
        """
            select atoms by type and store them in group
            G.type(group,typevalues)
        """
        lammps_code = f"group {group} type {span(typevalues)}"
        self.add_operation(Operation("type", typevalues, None, name=group, code=lammps_code))

    def id(self, group, idvalues):
        """
            select atoms by id and store them in group
            G.id(group,idvalues)
        """
        lammps_code = f"group {group} id {span(idvalues)}"
        self.add_operation(Operation("id", idvalues, None, name=group, code=lammps_code))

    def create(self, group):
        """
            create group
            G.create(group)
        """
        lammps_code = f"# dummy creation of {group}"
        self.add_operation(Operation("create", None, None, name=group, code=lammps_code))

    def clear(self, group):
        """
            clear group
            G.clear(group)
        """
        lammps_code = f"group {group} clear"
        self.add_operation(Operation("clear", None, None, name=group, code=lammps_code))

    def empty(self, group):
        """
            empty group
            G.empty(group)
        """
        lammps_code = f"group {group} empty"
        self.add_operation(Operation("empty", None, None, name=group, code=lammps_code))

    def union(self, group, group1, *othergroups):
        """
            union group1, group2, group3 and store the result in group
            G.union(group, group1, group2, group3,...)
        """
        lammps_code = f"group {group} union {group1} " + span(othergroups)
        self.add_operation(Operation("union", group1, othergroups, name=group, code=lammps_code))

    def intersect(self, group, group1, *othergroups):
        """
            intersect group1, group2, group3 and store the result in group
            G.intersect(group, group1, group2, group3,...)
        """
        lammps_code = f"group {group} intersect {group1} " + span(othergroups)
        self.add_operation(Operation("intersect", group1, othergroups, name=group, code=lammps_code))

    def subtract(self, group, group1, *othergroups):
        """
            substract group2, group3 to group1 and store the result in group
            G.subtact(group, group1, group2, group3,...)
        """
        lammps_code = f"group {group} subtract {group1} " + span(othergroups)
        self.add_operation(Operation("subtract", group1, othergroups, name=group, code=lammps_code))

    def eval(self, groupname, group_op):
        """
            Evaluates the o1+o2+o3-o4 and stores the result in a new group.
        """
        if not isinstance(group_op, GroupOperation):
            raise TypeError("Expected an instance of GroupOperation.")

        group1 = group_op.operations[0].name
        for op, group2 in zip(group_op.operators, group_op.operations[1:]):
            if op == '+':
                self.union(groupname, group1, group2.name)
            elif op == '-':
                self.subtract(groupname, group1, group2.name)
            elif op == '*':
                self.intersect(groupname, group1, group2.name)
            group1 = groupname




# %% debug section - generic code to test methods (press F5)
if __name__ == '__main__':

    # Example Usage
    G = group()
    G.variable("groupname","variablename","myexpression myexpression myexpression myexpression and again 1234")
    print(G.disp("groupname"))

    G.region("regiongroup","myregionID")
    print(G.disp("regiongroup"))

    G.union("uniongroup","group1","group2","group3")
    print(G.disp("uniongroup"))

    # Advanced Usage
    G = group()
    G.create('op1')
    G.create('op2')
    G.eval("op12",G.op1+G.op2)
