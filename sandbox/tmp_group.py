   def eval(self, groupname, group_op):
        """
        Evaluates the expressions like o1+o2+o3-o4+o5+o6 and stores the result in a new group.

        Parameters:
        -----------
        groupname : str
            The name of the group that will store the result.
        group_op : GroupOperation or Operation
            The operation or group of operations to evaluate.
        """
        if isinstance(group_op, Operation):
            # For Operation, simply add it with the specified name
            group_op.name = groupname
            self.add_operation(group_op)

        elif isinstance(group_op, GroupOperation):
            # Start with the first operation
            result_group = group_op.operations[0].name

            # Iterate through the remaining operations in this GroupOperation
            for op in group_op.operations[1:]:
                if group_op.operator == '+':
                    self.union(groupname, result_group, op.name)
                elif group_op.operator == '-':
                    self.subtract(groupname, result_group, op.name)
                elif group_op.operator == '*':
                    self.intersect(groupname, result_group, op.name)
                result_group = groupname

        else:
            raise TypeError("Expected an instance of GroupOperation or Operation.")




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
    G.eval("debug",G.o1+G.o2+G.o3)
    print(repr(G))

# class for multiple heterogenerous operations
class GroupOperation:
    """
        class to represent a sequence of operations combined using a specific operator.

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

    def __init__(self, operation1, operation2, operator,name=""):
        # error check
        if not isinstance(operation1, (Operation, GroupOperation)) or not isinstance(operation2, (Operation, GroupOperation)):
            raise TypeError("Expected instances of Operation or GroupOperation.")
        # Check whether operation1 needs to be collapsed
        if isinstance(operation1, GroupOperation):
            if operation1.operator != operator:
                operation1 = self.collapse(operation1)

        # Check whether operation2 needs to be collapsed
        if isinstance(operation2, GroupOperation):
            if operation2.operator != operator:
                operation2 = self.collapse(operation2)
        # Store the (potentially collapsed) operations
        self.operations = [operation1, operation2]
        self.operator = operator if operator is not None else ""
        self.name = name if name else self.generate_hashname()
        self.flatten()

    def generate_hashname(self):
        """
            Generate a hash name by concatenating the names of all operations inside
            and hashing the result, keeping only the first 10 characters.
        """
        concatenated_names = self.operator.join(op.name for op in self.operations)
        return "GRP"+hashlib.sha256(concatenated_names.encode()).hexdigest()[:6]

    @staticmethod
    def collapse(group_operation):
        """
            Collapse a group of operations of the same kind
        """
        collapsed_name = group_operation.generate_hashname()
        available_names = group_operation.flatten_names()
        if group_operation.operator == '+':
            group.union(collapsed_name, available_names[0],*available_names[1:])
        elif group_operation.operator == '-':
            group.subtract(collapsed_name, available_names[0],*available_names[1:])
        elif group_operation.operator == '*':
            group.intersect(collapsed_name, available_names[0],*available_names[1:])
        return group._operations[-1]

    def flatten(self):
        """
        Recursively flattens this GroupOperation to reduce unnecessary nesting.
        """
        flat_operations = []
        for operation in self.operations:
            if isinstance(operation, GroupOperation):
                if operation.operator == self.operator:
                    flat_operations.extend(operation.operations)
                else:
                    flat_operations.append(operation)
            else:
                flat_operations.append(operation)
        return flat_operations

    def __add__(self, other):
        return GroupOperation(self, other, '+')

    def __sub__(self, other):
        return GroupOperation(self, other, '-')

    def __mul__(self, other):
        return GroupOperation(self, other, '*')

    def __repr__(self):
          return f"{self.name} = " + f" {self.operator} ".join(map(str, self.operations))


    def flatten_names(self):
        """
        Recursively collect the names of all Operation instances inside
        this GroupOperation, including any nested GroupOperation instances.
        """
        names = []
        for op in self.operations:
            if isinstance(op, GroupOperation):
                names.extend(op.flatten_names())
            else:
                names.append(op.name)
        return names


    def extend(self, new_operator, new_operation, force_collapse=False):
        """
        Extend the current GroupOperation with a new operation.
        If the new operator is different from the current operator,
        it merges the current operations into a single operation
        using the method corresponding to the current operator.

        Parameters:
        -----------
        new_operator : str
            The new operator to be applied. It can be '+' (union), '-' (subtract), or '*' (intersect).
        new_operation : Operation
            The new operation object to be added to this GroupOperation.
        force_collapse : bool
            Whether to force a collapse of the current operations into a single operation
            using the current operator, without adding a new operation.
        """
        if new_operator == self.operator:
            # If the new operator is the same, just add the new operation to this GroupOperation
            if isinstance(new_operation, GroupOperation) and new_operation.operator == self.operator:
                self.operations.extend(new_operation.operations)
            else:
                self.operations.append(new_operation)
        else:
            # If the new operator is different, start a new GroupOperation
            return GroupOperation(self, new_operation, new_operator)
