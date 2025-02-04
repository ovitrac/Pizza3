## **Mathematical Notations and Capabilities in `param()`**

The `param()` class extends the `struct` class and allows **dynamic evaluation** of expressions, **implicit calculations**, and **NumPy-style operations**. Instances of this class are iterable and can be managed using a Matlab-like syntax.

*Note: Matlab inputs are also enabled as shorthands.*

### Manage dependencies
It is mandatory to import NumPy as `np` (internal convention) if NumPy arrays are defined in strings.
The following snippet also shows how to check the current working directory (if needed)


```python
# assuming that cwd is Pizza3/ main folder
# check it with :
'''
# control snippet
import os
current_dir = os.getcwd()
print(current_dir)
'''
import numpy as np
from pizza.private.mstruct import param

def prettyprint(var, value):
    """Display the variable's name, its value, and its type after evaluation."""
    print(f"{var} = {value} (type: {type(value).__name__})")
```

### **1. Overview**
The `param()` class uses fields/attributes to store values and expressions. Fields define variables, which can be
accessed with the syntax `${var}`. For instance, if you create an instance as `p = param(var=value, ...)`, then:

- `p.var` returns the value of `${var}`.
- `p.var = value` assigns or changes the value.
- `p("var")` returns the evaluated value of `${var}` considering the current context.

Expressions are defined as strings. An expression can represent either a valid mathematical expression or an abstract
string used for templating. Unlike Python's built-in `eval()` function, the context determines whether the result is
numeric or remains a string. Vectorial calculus is enabled by using the shorthand `@{matrix}` instead of `${matrix}`.

Interpolation (substitution) and evaluation are performed in the following order:
- **Direct interpolation/substitution:** e.g., `"the content of var is ${var}"`.
- **Local evaluation with a text result:** e.g., `"the sum of variables ${var1+var2}"`, `"the third value is ${var[2]}"`,
  or `"the sum is ${sum(var)}"`.
- **Full evaluation with a numeric result:** e.g., `"${var}"`, `"@{vector}.T"`, or `"@{matrix1} @ @{matrix2}"`.
- **Mixed evaluation in a list:** e.g., `["var=${myvar}"`, `"sum=${mylist}"`, `"@{matrix1} @ @{matrix2}"]`.

If a complete evaluation is not possible, the final result is stored with 4 significant digits by default (the precision can be increased if needed).

Expressions must combine only operators (`+`, `*`, `**`, etc.), built-in functions (`sum`, `prod`, etc.), mathematical functions (`sin`, `pi`, etc.), and NumPy functions (prefixed with `np.`) and operators (`@`, `.T`). Some statistics functions are also available.

Variables can be defined as strings (e.g., `"1.0"`) or as numbers (`1.0` for float or int), and they can be scalar or complex. When using text expressions, it is possible to define matrices and n-dimensional arrays using Matlab (`$[1 2 3; 4 5 6]`), NumPy (`$[[1,2,3];[4,5,6]]`), or hybrid notations (`$[[1 2 3; 4 5 6],[7 8 9; 10 11 12]]`).
Theoretically, variables can be any Matlab type (including class instances), though in practice lists or NumPy nd-arrays are recommended. Matlab and hybrid shorthands have been implemented for 1D vectors (row or column) up to 4D arrays, including expansions (e.g., `"$[1:10]"` or `"$[1:0.5:10]"`).

⚠️ **Warning:** Variables are evaluated in the order they are defined; use the `paramauto()` class instead if the order needs to be guessed or resolved. In contrast to Python f-strings, where expressions are dynamically re-evaluated, changing one field/variable in a `param` instance affects all others. Use the method `s = p.eval()` (or equivalently `s = p()`) to convert a dynamic `param` instance into a static structure `s`.

If an error occurs during evaluation, the evaluated value is replaced by an error message.

Instances of `param` are iterable and can be managed as lists or collections (e.g., using `p[5]`, `p[1:10:2]`, `p[[0,3,8]]`).

Multiple `param` instances can be merged together using the `+` operator:
    
    pmerged = poriginal + pupdate

### **2. Define variables**
- **Basic syntax:** Create an instance with `p = param()` and then define variables as:
  
      p.var = value
      p.var = "value"
      p.var = "expression"
  
- You can also initialize variables directly: `p = param(var1=..., var2=...)`.
- Accessing a variable: `p.var` or `getattr(p, "var")` returns the raw value of `${var}`.
- To obtain a static structure, use `s = p()` or `s = p.eval()`.
- Evaluate specific variables with `p("var1", "var2", ...)`.
- Prefix a string with `$` to designate it as a literal (i.e., not an expression).
- For debugging evaluation issues, use `p = param(debug=True)`.
- **Avoid** using a variable named `${e}` to prevent confusion with `exp(1)`.

**Literal expressions**

For legacy support, literal expressions can be defined either by:
- Adding the prefix `$` to the expression (e.g., `"$ab"`), or
- Placing the expression inside a list (e.g., `["ab"]`).

The latest versions of `param()` can automatically detect literals that cannot be evaluated.


**Literal Expressions Example**
This example demonstrates how to use literal expressions with `param()`:
- `line1`: A raw string that escapes `${a}` to prevent substitution.
- `line2`: A list of strings.
- `line3`: A string that interpolates a value from `line2`.
- `ab`: A variable holding the literal `"AB"`.
- `line4`: A literal expression where the `$` prefix preserves the literal value of `ab`.
- `line5`: A plain string `"ab"`.
- `line6`: A string `"sin(x)"` that will not generate an error.
- `line7`: An expression `"${sin(x)}"` which will generate an error since `x` is not defined.

The evaluated static structure is obtained by calling `l()`.


```python
l = param()
l.line1 = r"\${a}+1"        # escape `${a}` to prevent its substitution
l.line2 = ["a","b"]
l.line3 = 'The first letter in {line2} is "${line2[0]}"'
l.ab = "AB"
l.line4 = "$ab"
l.line5 = "ab"
l.line6 = "sin(x)" # it will not generate an error
l.line7 = "${sin(x)}" # it will generate an error since x is not defined
print('The values of l:')
print(repr(l))
print('\nthe static content of l')
s = l() # equivalent to s = p.eval()
s
```

    The values of l:
      -------------:----------------------------------------
              line1: \${a}+1
                   = ${a}+1
              line2: ['a', 'b']
                   = ['a', 'b']
              line3: The first letter in  [...] e2} is "${line2[0]}"
                   = The first letter in ['a', 'b'] is "a"
                 ab: AB
                   = AB
              line4: $ab
                   = ab
              line5: ab
                   = ab
              line6: sin(x)
                   = sin(x)
              line7: ${sin(x)}
                   = <Error: Variable or function 'x' is not defined>
      -------------:----------------------------------------
    parameter list (param object) with 8 definitions
    
    the static content of l
      -------------:----------------------------------------
              line1: ${a}+1
              line2: ['a', 'b']
              line3: The first letter in ['a', 'b'] is "a"
                 ab: AB
              line4: ab
              line5: ab
              line6: sin(x)
              line7: <Error: Variable or  [...]  'x' is not defined>
      -------------:----------------------------------------
    




    structure (struct object) with 8 fields



**Numeric examples**
This example demonstrates basic numeric assignments:
- `p.a` is assigned the float `10.0`.
- `p.b` is assigned the string `"10"`, representing the number 10.
- `p.c` is assigned a literal string `"$10"` (thus it is not interpreted as a number).
- `p.d` is defined as a Python list of numbers.
- `p.f` is created by converting `p.d` into a NumPy array (as a row vector).


```python
p = param()                    # initialize param. Note that can use also `p = param(a=..., b=...)`
p.a = 10.0                     # number 10 as float
p.b = "10"                     # number 10 stored as a string
p.c = "$10"                    # characters "1" and "0" (not a number)
p.d  = [1.0, 0.2, 0.03, 0.004] # Python list
p.f  = np.array([p.d])         # Converts a as row vector
```

### **3. Interpolation and local evaluation**

This section demonstrates the interpolation and local evaluation capabilities:

- **Simple interpolation/substitution:** `${var}` is replaced by its content.
- **Mathematical expressions:** Expressions within `${}` are evaluated in place.
- **Local evaluation:** Supports scalars, lists, NumPy arrays, and expressions.
- **Indexing:** Use `${var[i]}` or `${var[I,j]}` to index into arrays or matrices.
- **Escaping:** Use `\${...}` to prevent execution of the interpolation.

✅ **Supported Operations**
- Indexing of lists and arrays.
- Mathematical operations using operators like `+`, `-`, `*`, `/`.`**`

✅ **Supported Mathematical Functions**
- Built-in functions: `abs`, `round`, `min`, `max`, `sum`, `divmod`.
- Functions from the `math` module such as `pi`, `e`, `nan`, `inf`.
- NumPy functions (with the `np.` prefix) and operators such as `@` and `.T`.
- Statistics functions: `gauss`, `uniform`, `randint`, `choice`.


#### **Scalar evaluations Example**
The following examples show scalar evaluations:
- `p.g` evaluates an expression that retrieves `d[1]` and adds `b`.
- `p.h` evaluates an expression combining an element from the NumPy array `f` and an element from `d`.
- `p.i` demonstrates that the notation `${d}[1] + ${b}` is equivalent to a global evaluation.
- `p.j` uses a similar pattern for matrix operations but mixing outer indexing is not recommended.

*Note: It is recommended not to mix global and local expressions (especially for indexing with NumPy arrays).*


```python
p.g = "${d[1]}+${b}"           # Retrieves `a[1]` = 0.2 and add 10 `0.2 + 10`
p.h = "${f[0,1]} + ${d[0]}"    # Evaluates as `0.2 + 1.0`
p.i = "${d}[1]+${b}"           # This notation also works but via global evaluation (equivalent to c for the part `${a}[1]`) `0.2 + 10`
p.j = "${f}[0,1] + ${d}[0]"    # However, it should be avoided with implicit NumPy arrays (see below)
# à la Matlab practice, type the variable to see its content
p # alternatively use repr(p)
```

      -------------:----------------------------------------
                  a: 10.0
                  b: 10
                   = 10
                  c: $10
                   = 10
                  d: [1.0, 0.2, 0.03, 0.004]
                   = [1.0, 0.2, 0.03, 0.004]
                  f: [1 0.2 0.03 0.004] (double)
                  g: ${d[1]}+${b}
                   = 10.2
                  h: ${f[0,1]} + ${d[0]}
                   = 1.2
                  i: ${d}[1]+${b}
                   = 10.2
                  j: ${f}[0,1] + ${d}[0]
                   = [[1.0, 0.2, 0.03, 0. [...] 0.2, 0.03, 0.004][0]
      -------------:----------------------------------------
    




    parameter list (param object) with 9 definitions



**Evaluation and Display of Scalar Evaluations**
The following code evaluates all expressions (using `p()`) and displays:
- The equivalence between inner and outer indexing for lists.
- The differences for NumPy arrays, where only the first value (`h`) is numeric.
- A warning to avoid using outer indexing outside of `${...}`.


```python
# evaluate all expressions and store them in s
s = p() # equivalent to s = p.eval() 
# c and e are equivalent
print("Inner and outer indexing are similar for list")
repr(p("g","i")) # show the evaluation of c and e
print('All values are numeric (float)')
prettyprint("g",s.g)
prettyprint("i",s.i)
# d and f are not equivalent
print("\n","Inner and outer indexing are not similar for NumPy arrays")
repr(p("h","j")) # show the evaluation of d and f
print("only the first value (h) is numeric")
prettyprint("h",s.h)
prettyprint("j",s.j)
print('avoid using outer indexing and keep it within "{}"')
```

    Inner and outer indexing are similar for list
      -------------:----------------------------------------
                  g: 10.2
                  i: 10.2
      -------------:----------------------------------------
    All values are numeric (float)
    g = 10.2 (type: float)
    i = 10.2 (type: float)
    
     Inner and outer indexing are not similar for NumPy arrays
      -------------:----------------------------------------
                  h: 1.2
                  j: [[1.0, 0.2, 0.03, 0. [...] 0.2, 0.03, 0.004][0]
      -------------:----------------------------------------
    only the first value (h) is numeric
    h = 1.2 (type: float)
    j = [[1.0, 0.2, 0.03, 0.004]][0,1] + [1.0, 0.2, 0.03, 0.004][0] (type: str)
    avoid using outer indexing and keep it within "{}"
    

#### **List and Nested Evaluations**
This section demonstrates that variables can hold multiple values and that results are stored in lists:

*Note: the special character `!` can be placed in front of expressions using lists as results (e.g., `"!["${myvar}",${sum(myvar)+offset}]"` to force recursive execution if it is not guessed internally.*

**Text Example**

In the following example, `q.units` is a literal string (with the `$` prefix).

- `q.a` is a list containing a literal string and another literal.
- `q.b` uses interpolation to reference `units`.
- `q.c` shows a string with both interpolation and an escaped placeholder.


```python
q = param()
q.units = "$si"                # literal string (no interpolation)
q.a = ["units","$lj"] 
q.b = ["units","${units}"]
q.c = "the ${a[0]} are ${units} as defined with \\${units}"
q
```

      -------------:----------------------------------------
              units: $si
                   = si
                  a: ['units', '$lj']
                   = ['units', 'lj']
                  b: ['units', '${units}']
                   = ['units', 'si']
                  c: the ${a[0]} are ${un [...] fined with \${units}
                   = the units are si as  [...] efined with ${units}
      -------------:----------------------------------------
    




    parameter list (param object) with 4 definitions



**Text/Numeric Evaluation Example**
This example mixes text and numeric evaluations:
- `r.a` is a numeric list.
- `r.b` is provided as a string that represents a list with param expressions.
- `r.c` uses the `!` prefix to force recursive evaluation of expressions in lists.
- `r.d` and `r.e` combine expressions from other list entries.
- `r.f` is a list containing a mixture of expressions and literal values.


```python
r = param()
r.a = [0,1,2]                   # this list is numeric and is already in Python
r.b = '[1,2,"test","${a[1]}"]'  # this list combines param expressions
r.c = '![1,2,"test","${a[1]}"]' # the `!` to force recursive evaluation of expressions in lists
r.d = "${b[3]}*10"              # the expressions can be combined together
r.e = "${c[3]}*10"              # the expressions can be combined together
r.f = ["${a[1]+a[2]}*3", 1,2,"test","${a[1]}", "${a[1]+a[2]}", "${1+2}", "b"]
r
```

      -------------:----------------------------------------
                  a: [0, 1, 2]
                   = [0, 1, 2]
                  b: [1,2,"test","${a[1]}"]
                   = [1, 2, 'test', '1']
                  c: ![1,2,"test","${a[1]}"]
                   = [1, 2, 'test', 1]
                  d: ${b[3]}*10
                   = 10
                  e: ${c[3]}*10
                   = 10
                  f: ['${a[1]+a[2]}*3', 1 [...] 2]}', '${1+2}', 'b']
                   = [9, 1, 2, 'test', 1, 3, 3, 'b']
      -------------:----------------------------------------
    




    parameter list (param object) with 6 definitions



**Additional Numeric Example**

This example defines a param instance `t` with parameters `o` and `p`. Then:
- `t.a` is constructed as a list containing `${o}` and `${p}`.
- `t.b` computes the sum of the elements in `a`.
- `t.c` calculates the maximum surface area using `pi` and the maximum value in `a`.


```python
t = param(o=10,p=100)
t.a = "[${o},${p}]"
t.b = "the sum of a is ${sum(a)}"
t.c = "the maximum surface area is ${pi*max(a)**2}"
t
```

      -------------:----------------------------------------
                  o: 10
                  p: 100
                  a: [${o},${p}]
                   = [10, 100]
                  b: the sum of a is ${sum(a)}
                   = the sum of a is 110
                  c: the maximum surface  [...] a is ${pi*max(a)**2}
                   = the maximum surface  [...] s 31415.926535897932
      -------------:----------------------------------------
    




    parameter list (param object) with 5 definitions



#### 4. **Mathematical shorthands for vectors, matrices, 3D and 4D arrays**
Lists cannot be directly used as vectors and must be converted into NumPy arrays before performing vectorized operations.
The `param()` class offers several shorthands to seamlessly manipulate arrays using text expressions:

- **1D:** `$[1 2 3]` → `np.atleast_2d(np.array([1,2,3]))`
- **2D:** `$[[1 2],[3 4]]` → `np.array([[1,2],[3,4]])`
- **3D:** `$[[[1 2],[3 4]],[[5 6],[7 8]]]` → `np.array([[[1,2],[3,4]],[[5,6],[7,8]]])`
- **4D:** `$[[[[1 2]]]]` → `np.array([[[[1,2]]]])`

**Variable References:**
- `@{var}` is equivalent to `np.atleast_2d(np.array(${var}))`.

**Transpose:**
- Use `@{var}.T` to transpose.

**Function Application:**
- Apply a function to a vector with: `np.foo(@var)`.

**Slicing:**
- `${var[:,0]}` converts a slice into a list.
- `@{var}[:,0]` preserves the slice as a NumPy array.

**Matlab Notations Supported:**
- Automatic row vector expansion using `$[start:stop]` or `$[start:step:stop]`.
- Spaces can be used to separate values row-wise.
- Semicolons (`;`) separate rows.

**Examples:**
- `$[1, 2  ${var1} ; 4, 5  ${var2}]` is equivalent to `$[[1,2,${var1}],[4,5,${var2}]]`
- `$[1;2; 3]` becomes `$[[1],[2],[3]]`
- `[[-0.5, 0.5;-0.5, 0.5],[ -0.5,  0.5; -0.5,  0.5]]` becomes `$[[[-0.5,0.5],[-0.5,0.5]],[[-0.5,0.5],[-0.5,0.5]]]`
- `$[[1,2;3,4],[5,6; 7,8]]` becomes `$[[[1,2],[3,4]],[[5,6],[7,8]]]`
- `$[1, 2, 3; 4, 5, 6]` becomes `$[[1,2,3],[4,5,6]]`

**Simple Definitions Example**

This example demonstrates simple definitions using Matlab-style notations:
- `e.a` uses `$[1:3]` to create the vector `[1, 2, 3]`.
- `e.b` uses `$[1;2;3]` to create a column vector `[[1],[2],[3]]`.
- `e.c` uses `$[0.1:0.1:0.9]` to create the vector `[0.1, 0.2, ..., 0.9]`.
- `e.d` defines a 2D matrix with `$[1 2 3; 4 5 6]`.


```python
e = param()
e.a = "$[1:3]"           # Becomes `[1, 2, 3]`
e.b = "$[1;2;3]"         # Becomes `[[1];[2];[3]]`
e.c = "$[0.1:0.1:0.9]"   # `[0.1, 0.2, 0.3, ..., 0.9]`
e.d = "$[1 2 3; 4 5 6]"  # `[[1,2,3], [4,5,6]]`
e
```

      -------------:----------------------------------------
                  a: $[1:3]
                   = [1 2 3] (int32)
                  b: $[1;2;3]
                   = [1 2 3]T (int32)
                  c: $[0.1:0.1:0.9]
                   = [0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9] (double)
                  d: $[1 2 3; 4 5 6]
                   = [2×3 int32]
      -------------:----------------------------------------
    




    parameter list (param object) with 4 definitions



**Matrix Operations Example**

This example illustrates simple matrix operations:
- `m.a` is a list of numeric values.
- `m.b` is a NumPy array created from `m.a` (as a row vector).
- `m.c` computes `m.a * 2` (element-wise multiplication for a list).
- `m.d` computes `m.b * 2` (element-wise multiplication for a NumPy array).
- `m.e` is the transpose of `m.b`.
- `m.f` performs matrix multiplication between the transpose of `m.b` and `m.b`.
- Variables `m.g` through `m.o` demonstrate various forms of expression evaluation, indexing, and string interpolation.
  - Note that `"@{j}+1"` and `"${j}+1"` do not have the same meaning.
- `m.p` uses a raw string (with the `r` prefix) to correctly escape `${a[0]}`.


```python
# Example with simple matrix operations
m=param()
m.a = [1.0, .2, .03, .004]
m.b = np.array([m.a])
m.c = m.a*2
m.d = m.b*2
m.e = m.b.T
m.f = m.b.T@m.b # Matrix multiplication for (3x1) @ (1x3)
m.g = "${a[1]}"
m.h = "${b[0,1]} + ${a[0]}"
m.i = "${f[0,1]}"
m.j = "${f[:,1]}"
m.k = "@{j}+1"  # note that "@{j}+1" and "${j}+1" do not have the same meaning
m.l = "${b.T}"  # note that b is already a NumPy array (no need to call @(b).T, which works also)
m.m = "${b.T @ b}"    # evaluate fully the matrix operation
m.n = "${b.T} @ ${b}" # concatenate two string-results separated by @
m.o ="the result is: ${b[0,1]} + ${a[0]}"
m.p = r"the value of \${a[0]} is ${a[0]}" # literal (r"  ") is used because "\$" is not a valid escape sequence, use "\\$" alternatively
m
```

      -------------:----------------------------------------
                  a: [1.0, 0.2, 0.03, 0.004]
                   = [1.0, 0.2, 0.03, 0.004]
                  b: [1 0.2 0.03 0.004] (double)
                  c: [1.0, 0.2, 0.03, 0.0 [...] 0, 0.2, 0.03, 0.004]
                   = [1.0, 0.2, 0.03, 0.0 [...] 0, 0.2, 0.03, 0.004]
                  d: [2 0.4 0.06 0.008] (double)
                  e: [1 0.2 0.03 0.004]T (double)
                  f: [4×4 double]
                  g: ${a[1]}
                   = 0.2
                  h: ${b[0,1]} + ${a[0]}
                   = 1.2
                  i: ${f[0,1]}
                   = 0.2
                  j: ${f[:,1]}
                   = [0.2, 0.040000000000 [...] 0001, 0.006, 0.0008]
                  k: @{j}+1
                   = [1.2 1.04 1.006 1.001] (double)
                  l: ${b.T}
                   = [[1.   ]
     [0.2  ]
     [0.03 ]
     [0.004]]
                  m: ${b.T @ b}
                   = [[1.0, 0.2, 0.03, 0. [...] , 0.00012, 1.6e-05]]
                  n: ${b.T} @ ${b}
                   = [[1.   ]
     [0.2  ]
     [ [...]  0.2   0.03  0.004]]
                  o: the result is: ${b[0,1]} + ${a[0]}
                   = the result is: 0.2 + 1.0
                  p: the value of \${a[0]} is ${a[0]}
                   = the value of ${a[0]} is 1.0
      -------------:----------------------------------------
    




    parameter list (param object) with 16 definitions



**Slicing Example**

This example demonstrates slicing operations:
- `s.a` and `s.b` are scalar values.
- `s.c` creates a NumPy vector from an operation.
- `s.n` defines a vector using the `$` syntax.
- `s.o1` creates a copy of `n` using the `@{}` notation.
- `s.o2` creates a NumPy vector directly.
- `s.o3` performs multiplication between two vectors.
- `s.d` shows another multiplication example using a transpose.
- `s.f` uses an explicit NumPy operation.
- `s.nT` is the transpose of vector `n`.
- `s.m` attempts an illegal operation (it will be kept as a string).
- `s.o` shows the correct syntax for the operation.
- `s.p` defines a 2D NumPy array.
- `s.q` indexes the 2D array to retrieve an element.
- `s.r` slices the 2D array, returning a list.
- `s.s` applies an operation to the slice, preserving it as a NumPy array.


```python
s = param(debug=True);
s.a = 1.0
s.b = "10.0"
s.c = "$[${a},2,3]*${b}" # Create a Numpy vector from an operation
s.n = "$[0,0,1]"         # another one
s.o1 = "@{n}"          # create a copy
s.o2 = "$[${a},2,3]" # create a Numpy vector
s.o3 = "@{o1} @ @{o2}.T" # multiplication between two vectots
s.d = "@{n}.T @ $[[${a},2,3]]" # another one
s.f = "($[${a},2,3]*${b}) @ ns.array([[0,0,1]]).T" # another one using explicitly NumPy
s.nT = "@{n}.T" # transpose of a vector/matrix
s.m = "${n.T}*2" # this operation is illegal and will be kept as a string
s.o = "@{n}.T*2" # this one is the correct one
s.p = "$[[1,2],[3,4]]" # Create a 2D Numpy array
s.q = "${p[1,1]}"   # index a 2D NumPy array
s.r = "${p[:,1]}"   # this is a valid syntax to get the slice as a list
s.s = "@{p}[:,1]+1" # use this syntax if you need apply an operation to the slice
s
```

      -------------:----------------------------------------
                  a: 1.0
                  b: 10.0
                   = 10.0
                  c: $[${a},2,3]*${b}
                   = [10 20 30] (double)
                  n: $[0,0,1]
                   = [0 0 1] (int32)
                 o1: @{n}
                   = [0 0 1] (int32)
                 o2: $[${a},2,3]
                   = [1 2 3] (double)
                 o3: @{o1} @ @{o2}.T
                   = 3.0 (double)
                  d: @{n}.T @ $[[${a},2,3]]
                   = [3×3 double]
                  f: ($[${a},2,3]*${b}) @ [...] s.array([[0,0,1]]).T
                   = (np.atleast_2d(np.ar [...] s.array([[0,0,1]]).T
                 nT: @{n}.T
                   = [0 0 1]T (int32)
                  m: ${n.T}*2
                   = [[0]
     [0]
     [1]]*2
                  o: @{n}.T*2
                   = [0 0 2]T (int32)
                  p: $[[1,2],[3,4]]
                   = [2×2 int32]
                  q: ${p[1,1]}
                   = 4
                  r: ${p[:,1]}
                   = [2, 4]
                  s: @{p}[:,1]+1
                   = [3 5] (int32)
      -------------:----------------------------------------
    




    parameter list (param object) with 16 definitions



**Advanced Example**

This advanced example demonstrates operations such as:
- Defining a vector `V1`.
- Computing `V2` as `V1 + 1`.
- Performing matrix multiplication between the transpose of `V1` and `V2`.
- Creating a diagonal matrix from the resulting product.
- Calculating the eigenvalues and eigenvectors of the resulting matrix.
- Displaying the first eigenvalue in a formatted string.


```python
a = param(debug=True)
a.V1 = "$[1.0,0.2,0.03]"
a.V2 = "@{V1}+1"
a.V3 = "@{V1}.T @ @{V2}"
a.V4 = "np.diag(@{V3})"
a.V5 = "np.linalg.eig(@{V3})"
a.out = "the first eigenvalue is: ${V5.eigenvalues[0]}"
a
```

      -------------:----------------------------------------
                 V1: $[1.0,0.2,0.03]
                   = [1 0.2 0.03] (double)
                 V2: @{V1}+1
                   = [2 1.2 1.03] (double)
                 V3: @{V1}.T @ @{V2}
                   = [3×3 double]
                 V4: np.diag(@{V3})
                   = [2 0.24 0.0309] (double)
                 V5: np.linalg.eig(@{V3})
                   = EigResult(eigenvalue [...] 332, -0.06057363]]))
                out: the first eigenvalue [...] ${V5.eigenvalues[0]}
                   = the first eigenvalue [...] s: 2.270900000000001
      -------------:----------------------------------------
    




    parameter list (param object) with 6 definitions



### 5. **Global evaluation**

A global evaluation is attempted for all expressions after interpolation and local evaluations have been performed.
If the global evaluation does not raise any error, the evaluated result is kept; otherwise, the original interpolated
expression is preserved. Since several expressions involving matrix operations require global evaluation (i.e., outside
of `${...}` or `@{...}`), it is recommended to define mathematically valid expressions and, if needed, use separate
variables to store results as text.


**Global Evaluation Example with NumPy**

This example demonstrates global evaluation:
- `u.p` creates a 2D NumPy array.
- `u.q` indexes the array to retrieve an element.
- `u.r` adds 1 to the second column of `p`.
- `u.s` reshapes a slice and performs matrix multiplication in a Matlab-like manner.
- `u.t` computes the eigenvalues and eigenvectors of the resulting matrix.
- `u.w` calculates the sum of the first two eigenvalues.
- `u.x` horizontally concatenates a literal with the sum of the eigenvalues.


```python
u = param(debug=True)
u.p = "$[[1, 2], [3, 4]]"      # Create a 2D NumPy array
u.q = "${p[1, 1]}"             # Indexing: retrieves 4
u.r = "@{p}[:,1] + 1"          # Add 1 to the second column
u.s = "@{p}[:, 1].reshape(-1, 1) @ @{r}" # perform p(:,1)'*s in Matlab sense
u.t = "np.linalg.eig(@{s})"
u.w = "${t.eigenvalues[0]} + ${t.eigenvalues[1]}" # sum of eigen values
u.x = "$[[0,${t.eigenvalues[0]}+${t.eigenvalues[1]}]]" # horizontal concat à la Matlab
u
```

      -------------:----------------------------------------
                  p: $[[1, 2], [3, 4]]
                   = [2×2 int32]
                  q: ${p[1, 1]}
                   = 4
                  r: @{p}[:,1] + 1
                   = [3 5] (int32)
                  s: @{p}[:, 1].reshape(-1, 1) @ @{r}
                   = [2×2 int32]
                  t: np.linalg.eig(@{s})
                   = EigResult(eigenvalue [...] 576, -0.89442719]]))
                  w: ${t.eigenvalues[0]}  [...]  ${t.eigenvalues[1]}
                   = 26.0
                  x: $[[0,${t.eigenvalues [...] {t.eigenvalues[1]}]]
                   = [0 26] (double)
      -------------:----------------------------------------
    




    parameter list (param object) with 7 definitions



**Global Evaluation Example with Various Matrix and ND- Operations**

This example demonstrates various matrix operations:
- A list `l` is defined.
- Vectors and matrices (`a`, `b`, `c`) are created using Matlab-style notations.
- Element-wise and matrix operations are performed.
- More complex structures (`x0`, `y0`, `z0`) are defined using multiple operations.
- Finally, the results are flattened into vectors `X0`, `Y0`, and `Z0`.


```python
v = param()
v.l = [1e-3, 2e-3, 3e-3]    # l is defined as a list
v.a = "$[1 2 3]"            # a is defined with  Matlab notations
v.b = "$[1:3]"              # b is defined with  Matlab notations
v.c = "$[0.1:0.1:0.9]"      # c is defined with  Matlab notations
v.scale = "@{l}*2*@{a}"     # l is rescaled
v.x0 = "$[[[-0.5, -0.5],[-0.5, -0.5]],[[ 0.5,  0.5],[ 0.5,  0.5]]]*${scale[0,0]}*${a[0,0]}"
v.y0 = "$[[[-0.5, -0.5],[0.5, 0.5]],[[ -0.5,  -0.5],[ 0.5,  0.5]]]*${scale[0,1]}*${a[0,1]}"
v.z0 = "$[[-0.5 0.5 ;-0.5 0.5],[ -0.5,  0.5;  -0.5,  0.5]]*${l[2]}*${a[0,2]}"
v.X0 = "@{x0}.flatten()"
v.Y0 = "@{y0}.flatten()"
v.Z0 = "@{z0}.flatten()"
v
```

      -------------:----------------------------------------
                  l: [0.001, 0.002, 0.003]
                   = [0.001, 0.002, 0.003]
                  a: $[1 2 3]
                   = [1 2 3] (int32)
                  b: $[1:3]
                   = [1 2 3] (int32)
                  c: $[0.1:0.1:0.9]
                   = [0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9] (double)
              scale: @{l}*2*@{a}
                   = [0.002 0.008 0.018] (double)
                 x0: $[[[-0.5, -0.5],[-0. [...] cale[0,0]}*${a[0,0]}
                   = [[2×2 matrix] [2×2 matrix]] (2×2×2 double)
                 y0: $[[[-0.5, -0.5],[0.5 [...] cale[0,1]}*${a[0,1]}
                   = [[2×2 matrix] [2×2 matrix]] (2×2×2 double)
                 z0: $[[-0.5 0.5 ;-0.5 0. [...] ]]*${l[2]}*${a[0,2]}
                   = [[2×2 matrix] [2×2 matrix]] (2×2×2 double)
                 X0: @{x0}.flatten()
                   = [-0.001 -0.001 -0.001 -0.001 0.001 0.001 0.001 0.001] (double)
                 Y0: @{y0}.flatten()
                   = [-0.008 -0.008 0.008 0.008 -0.008 -0.008 0.008 0.008] (double)
                 Z0: @{z0}.flatten()
                   = [-0.0045 0.0045 -0.0045 0.0045 -0.0045 0.0045 -0.0045 0.0045] (double)
      -------------:----------------------------------------
    




    parameter list (param object) with 11 definitions


