## **Mathematical Notations and Capabilities in `param()`**

> The `param()` class, located in `pizza.private.mstruct` is an essential low-level class for 🍕 Pizza³. It used as parent class for data containers used by `script`, `pipescript`, `dscript`, `scriptobject`, `forcefield`, `dforcefield`. Its methods offer scripting capabilities between Pythonic and LAMMPS syntaxes.

The `param` class extends the `struct` class (located in the same module) and allows **dynamic evaluation** of expressions, **implicit calculations**, and **NumPy-style operations**. Instances of this class are iterable and can be managed using a Matlab-like syntax(*).

The syntax evolved between versions towards more flexibility and robustness. The capacity to perform calculations matrix/nd-operations is vital for building LAMMPS codelets/blocks with complex displacements and boundary conditions.

(*)<kbd>note:</kbd> *<small>Matlab inputs are also enabled as shorthands.</small>*

### Manage dependencies
<kbd>note:</kbd> *It is mandatory to import NumPy as `np` (internal convention) if NumPy arrays are defined in `param` text expressions.*

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
from pizza.private.mstruct import param, paramauto # paramauto is used in one example

def prettyprint(var, value):
    """Display the variable's name, its value, and its type after evaluation."""
    print(f"{var} = {value} (type: {type(value).__name__})")
```

<kbd>note:</kbd> *<small>If your notebook is showing an empty figure above, it is normal at at the initialization of Pizza. The code is testing the graphical capabilities.</small>*



---



### **1 | Overview**

#### **1.1 | Variable Definition/Assignment**

The `param()` class uses fields/attributes to store values and expressions. Fields define variables, which can be accessed with the syntax `${var}`. For instance, if you create an instance as `p = param(var=value, ...)`, then:

- `p.var` returns the value of `${var}`.
- `p.var = value` assigns or changes the value.
- `p("var")` returns the evaluated value of `${var}` considering the current context.

🗑️ A variable can be deleted with the shorthand:
- `p.var = []` or by using `del(p,"var")`


#### **1.2 | `param` expressions**

🟰 `param` expressions are defined as strings. An expression can represent either a valid mathematical expression or an abstract string used for templating. Unlike Python's built-in `eval()` function, the context determines whether the result is numeric or remains a string. Vectorial calculus is enabled using the shorthand `@{matrix}` instead of `${matrix}`.

➗ Expressions must combine only operators (`+`, `*`, `**`, etc.), built-in functions (`sum`, `prod`, etc.), mathematical functions (`sin`, `pi`, etc.), and NumPy functions (prefixed with `np.`) and operators (`@`, `.T`). Some statistics functions are also available.


#### **1.3 | Interpolation and Evaluation**

🧮 Interpolation (substitution) and 🚀 evaluation are performed in the following order:
- **Direct interpolation/substitution:** e.g., `"the content of var is ${var}"`.
- **Local evaluation with a text result:** e.g., `"the sum of variables ${var1+var2}"`, `"the third value is ${var[2]}"`,
  or `"the sum is ${sum(var)}"`.
- **Full evaluation with a numeric result:** e.g., `"${var}"`, `"@{vector}.T"`, or `"@{matrix1} @ @{matrix2}"`.
- **Mixed evaluation in a list:** e.g., `["var=${myvar}"`, `"sum=${mylist}"`, `"@{matrix1} @ @{matrix2}"]`.

🤔 If a complete evaluation is not feasible, the final result is stored with 4 significant digits by default (the precision can be increased if needed).

❌ If an **error** occurs during evaluation, the evaluated value is replaced by an error message.

🔄 In most cases, simple variable substitutions are possible using the Pythonic syntax `{variable}` instead of `${variable}`, which enables more complex evaluation.


#### **1.4 | Native vs. `param` text expressions** 

🔢 Variables can be defined as strings (e.g., `"1.0"`) or as numbers (`1.0` for float or int), and they can be scalar or complex. When using text expressions, it is possible to define matrices and n-dimensional arrays using Matlab (`$[1 2 3; 4 5 6]`), NumPy (`$[[1,2,3];[4,5,6]]`), or hybrid notations (`$[[1 2 3; 4 5 6],[7 8 9; 10 11 12]]`).
Theoretically, variables can be any Matlab type (including class instances), though in practice lists or NumPy nd-arrays are recommended. Matlab and hybrid shorthands have been implemented for 1D vectors (row or column) up to 4D arrays, including expansions (e.g., `"$[1:10]"` or `"$[1:0.5:10]"`).

⚠️ **Warning:** Variables are evaluated in the order they are defined; use the `paramauto()` class instead if the order needs to be guessed or resolved. In contrast to Python f-strings, where expressions are dynamically re-evaluated, changing one field/variable in a `param` instance affects all others. Use the method `s = p.eval()` (or equivalently `s = p()`) to convert a dynamic `param` instance into a static structure `s`.


#### **1.5 | Iterable instances, indexing, and slicing**

🤝 Instances of `param` are iterable and can be managed as lists or collections:
- `p[5]` returns the 6^th^ element of `p`
- `p[[5]]` returns the sub-structure with only the 6^th^ element
- `p[1:10:2]'`and `p[[0,3,8]]`return substructure with the field indices between `[]` (Python notations)

✅ Variables used in expressions as `${var}` and undefined in `param` instance `p` can be automatically assigned to their default value (`p.var="${var}"` with:
- `p.check()`


#### **1.6 | Update, inheritance and merging**

📦 Many variables in `param` instance `p` can be updated with:
- `p.update(var1=value1, var2="expression2"...)`
- `p.update(**d)` with `d` dictionary coding for `d["var"]=value or "expression"`


🔗 Multiple `param` instances can be merged together using the `+` operator:
    
    pmerged = poriginal + pupdate


#### **1.7 | Conversions**
➡️ Expressions stored in `param` instances (e.g., `p`) can be converted to various formats:
- `param` ➡️ `struct` (non-evaluated) via `s = p.tostatic()`
- `param` ➡️ `struct` (evaluated) via `se = p.tostruct()` or `se = p()`
- `param` ➡️ `dict` via `d = p.todict()`
- `param` ➡️ `paramauto` via `pa = p.paramauto()` or `pa = paramauto(**p)`
- `struct` ➡️ `param` via `p = s.struct2param()` with `s` the static structure
- `struct` ➡️ `dict` via `d = s.struct2dict()` with `s` the static structure
- `dict` ➡️ `struct` via `s = struct(**d)` with `d` a `dict` instance
- `dict` ➡️ `param` via `p = param(**d)` with `d` a `dict` instance
- `dict` ➡️ `paramauto` via `pa = paramauto(**d)` with `d` a `dict` instance

#### **1.8 | File Operations**
💾 Static results or expressions can be read/write to files
- 📥 saved to disk via `p.write(filename)`
- 📤 loaded from disk via `p = struct.read(filename).toparam()`



---



### **2 | Define variables**

#### **2.1 | Overview**

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

#### **2.2 | Literal expressions**

For legacy support, literal expressions can be defined either by:
- Adding the prefix `$` to the expression (e.g., `"$ab"`), or
- Placing the expression inside a list (e.g., `["ab"]`).

<kbd>note:</kbd> *The latest versions of `param()` can automatically detect literals that cannot be evaluated.*


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
l.line3 = 'The first letter in ${line2} is "${line2[0]}"'
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



#### **2.3 | Inheritance of Missing Variables/Parameters, `paramauto` altenative and variable reordering**

The missing parameter `x` can be supplied :
- by another `param` instance `param(x=np.pi/4)` and combined with the previous instance via the operator `+` (<kbd>solution 1</kbd>);
- by using a `paramauto` instance `l_auto` capable of reordering automatically fields at runtime (<kbd>solution 2</kbd>);
- by reordering directly the variables in `l`  (<kbd>solution 3</kbd>)

**<kbd>Solution 1:</kbd>** *operator `+`*


```python
lfixed = param(x=np.pi/4) + l # the missing parameter must precede the definition of l (prepend)
lfixed
```

      -------------:----------------------------------------
                  x: 0.7853981633974483
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
                   = 0.7071067811865475
      -------------:----------------------------------------





    parameter list (param object) with 9 definitions



**<kbd>Solution 2:</kbd>** *Altenatively, the missing parameter can be appended to `l` and `l` can be converted to a `paramauto` instance. The instance `paramauto` shows eventually order errors, but it tries to reorder the fields at runtime to remove errors*.


```python
l.x = np.pi/4 # l is added
l_auto = l.toparamauto() ## note that the syntax **l is required to zip all variables
l_auto
```

    WARNING: unable to interpret 3/9 expressions in "definitions"
      -------------:----------------------------------------
              line1: \${a}+1
                   = ${a}+1
              line2: ['a', 'b']
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
                   = <Error: Variable or  [...]  'x' is not defined>
                  x: 0.7853981633974483
      -------------:----------------------------------------





    parameter list (param object) with 9 definitions



**<kbd>Solution 3:</kbd>** *Reordering fields using slicing and `+`*.


```python
lreordered = l[-1:] + l[:-1] # x has been appended at the previous step
lreordered
```

      -------------:----------------------------------------
                  x: 0.7853981633974483
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
                   = 0.7071067811865475
      -------------:----------------------------------------





    parameter list (param object) with 9 definitions



<kbd>note:</kbd> `param` and `struct` instances can be indexed with lists `[idx1,idx2,key1,key2...]`:

- with integers (`0` being the first value, `-1` the last one, `-2` the one before the last...)


```python
l[[-1,7]]
```

      -------------:----------------------------------------
                  x: 0.7853981633974483
              line7: ${sin(x)}
                   = 0.7071067811865475
      -------------:----------------------------------------





    parameter list (param object) with 2 definitions



- with a list of keys/names


```python
l[["x","line7"]]
```

      -------------:----------------------------------------
                  x: 0.7853981633974483
              line7: ${sin(x)}
                   = 0.7071067811865475
      -------------:----------------------------------------





    parameter list (param object) with 2 definitions



- with a hybrid list mixing integers and key names


```python
l[["x",-2]]
```

      -------------:----------------------------------------
                  x: 0.7853981633974483
              line7: ${sin(x)}
                   = 0.7071067811865475
      -------------:----------------------------------------





    parameter list (param object) with 2 definitions



#### **2.4 | Numeric examples**
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
p.f  = np.array([p.d])         # Converts the list d into a row vector
```



---



### **3 | Interpolation and Local Evaluation**

#### **3.1 | General Rules**

This section demonstrates the interpolation and local evaluation capabilities:

- **Simple interpolation/substitution:** `${var}` is replaced by its content.
- **Mathematical expressions:** Expressions within `${}` are evaluated in place.
- **Local evaluation:** Supports scalars, lists, NumPy arrays, and expressions.
- **Indexing:** Use `${var[i]}` or `${var[i,j]}` to index into arrays or matrices.
- **Indexing:** Use `${var[key]}` to index dictionaries (do not quote `key`).
- **Escaping:** Use `\${...}` to prevent execution of the interpolation.

✅ **Supported Operations**
- Indexing of lists, dicts, and arrays.
- Mathematical operations using operators like `+`, `-`, `*`, `/`.`**`

✅ **Supported Mathematical Functions**
- Built-in functions: `abs`, `round`, `min`, `max`, `sum`, `divmod`.
- Functions from the `math` module such as `pi`, `e`, `nan`, `inf`.
- NumPy functions (with the `np.` prefix) and operators such as `@` and `.T`.
- Statistics functions: `gauss`, `uniform`, `randint`, `choice`.


#### **3.2 | Scalar evaluations Example**
The following examples show scalar evaluations:
- `p.g` evaluates an expression that retrieves `d[1]` and adds `b`.
- `p.h` evaluates an expression combining an element from the NumPy array `f` and an element from `d`.
- `p.i` demonstrates that the notation `${d}[1] + ${b}` is equivalent to a global evaluation.
- `p.j` uses a similar pattern for matrix operations but mixing outer indexing is not recommended.

<kbd>note:</kbd> ` *It is recommended not to mix global and local expressions (especially for indexing with NumPy arrays).*


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
                   = [[1.0,0.2,0.03,0.004 [...] 0.2, 0.03, 0.004][0]
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
                  j: [[1.0,0.2,0.03,0.004 [...] 0.2, 0.03, 0.004][0]
      -------------:----------------------------------------
    only the first value (h) is numeric
    h = 1.2 (type: float)
    j = [[1.0,0.2,0.03,0.004]][0,1] + [1.0, 0.2, 0.03, 0.004][0] (type: str)
    avoid using outer indexing and keep it within "{}"


#### **3.3 | Nested Interpolations**

Nested interpolation enables the use of a variable as an index or key:
- `${list[${idx}]}`  with `${idx}` a variable coding for a scalar index (for example 1 or "1") of a `list`.
- `${dict["${key}"]}` with `${key}` a string coding for a key value of a `dict

<kbd>note:</kbd> *Nested interpolation is not enabled for NumPy arrays defined in `param` text expressions. Tuples can be indexed*

The following examples show the principles:

- `i.a` is a list (not a vector).
- `i.b` is an index of `a` defined as `int` (integer)
- `i.c` returns the value for the next index `b+1`; the shift is done before interpolation.
- `i.d` returns the same value with the shift applied after interpolation.
  - <kbd>note:</kbd> <small> *`e` is not used as a key as it can be confused with `exp(1)`*</small>
- `i.f` defines a `dict` (dictionary) container
- `i.g` is a key of `i.f`
- `i.h` operates an operation `*100` on the entry of `f` matching `g`; *note that quotes (here `'${g}'`) are mandatory. 


```python
i = param()
i.a = [1,2,3]
i.b = 1
i.c = "${a[${b+1}]}"
i.d = "${a[${b}+1]}"   # as c with the increment performed outside the expression 
i.f = {"A":1, "B":2, "C":3}
i.g = "C"
i.h ="${f['${g}']*100}"
i
```

      -------------:----------------------------------------
                  a: [1, 2, 3]
                   = [1, 2, 3]
                  b: 1
                  c: ${a[${b+1}]}
                   = 3
                  d: ${a[${b}+1]}
                   = 3
                  f: {'A': 1, 'B': 2, 'C': 3}
                  g: C
                   = C
                  h: ${f['${g}']*100}
                   = 300
      -------------:----------------------------------------





    parameter list (param object) with 7 definitions



<kbd>note:</kbd> *Lists and dictionaries defined in `param` text expressions can be also indexed.*

These features are exemplified by replacing Python expressions with text ones.


```python
i.a = "[10,20,30]" # previous values are multiplied by  (without $, it is a list)
i.b = "2" # index +1
i.f = '{"A":100, "B":200, "C":300}'  # previous values are multiplied by 100
i
```

      -------------:----------------------------------------
                  a: [10,20,30]
                   = [10, 20, 30]
                  b: 2
                   = 2
                  c: ${a[${b+1}]}
                   = Type Error < list indices must be integers or slices, not str >
                  d: ${a[${b}+1]}
                   = Type Error < list indices must be integers or slices, not str >
                  f: {"A":100, "B":200, "C":300}
                   = {'A': 100, 'B': 200, 'C': 300}
                  g: C
                   = C
                  h: ${f['${g}']*100}
                   = 30000
      -------------:----------------------------------------





    parameter list (param object) with 7 definitions



#### **3.4 | List and Nested Evaluations**
This section demonstrates that variables can hold multiple values and that results are stored in lists:

<kbd>note:</kbd> *The special character `!` can be placed in front of expressions using lists as results (e.g., `"!["${myvar}",${sum(myvar)+offset}]"` to force recursive execution if it is not guessed internally.*

**`param` Text Example**

In the following example, `q.units` is a literal string (with the `$` prefix).

- `q.a` is a list containing a literal string and another literal.
- `q.b` uses interpolation to reference `units`.
- `q.c` shows a string with interpolation and an escaped placeholder.


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



#### **3.5 | Support of `dict` (dictionnaries)**

By design, instances of `struct` (and, by extension, `param()`) are intended to serve as flexible containers that can
hold any type of data—including class instances. However, evaluating advanced types, such as nested lists or dictionaries,
is more challenging. At this stage, only minimal support is provided for these advanced types in `param()`.

<kbd>note:</kbd> *Dictionary fields can be defined either as native Python dictionaries or as strings representing dictionaries. One
limitation is that nesting strings for key names (i.e., defining keys as strings within string representations) remains an
open issue. This is because, according to PEP 3101 (the guidelines for Python's advanced string formatting),
quoted keys are not accepted in formatted strings. Consequently, a compromise approach is currently implemented.*

- Local evaluation/interpolation within `${}` follows PEP 3101: no quotes.
- Global evaluation outside `${}` uses conventional Pythonic syntax with quotes `'` or `"`
- A representation (global) of a `dict` `d` can be achieved outside local evaluation/interpolation with `${d}` and `{d}`

**Example Demonstrating Dictionary Support in `param()`**

- `d.a` is directly assigned a dictionary.
- `d.b` is assigned a string that represents a dictionary.
- `d.c` is assigned an expression referencing `b`.
- `d.d` is assigned an expression that uses dictionary indexing.
- `d.f` is assigned an expression that indexes a dictionary and performs an arithmetic operation.
  - <kbd>note:</kbd> <small> *`e` is not used as a key as it can be confused with `exp(1)`*</small>
- `d.g` sets a `dict` using local interpolation/evaluation (PEP 3101 syntax).
- `d.h` same definition using a global evaluation (conventional Pythonic syntax).
- `d.i` global representation of `h` using `${h}`, no possibility of interpolation
- `d.j` idem using the Pythonic shorthand `{h}`, no possibility of interpolation

<kbd>note:</kbd> *The definition of a `dict` within a `param` expression `${}' imposes fields to be used without quotes (adherence to PEP 3101)*


```python
d = param()
d.a = {'a': 'a', 'b': 2}
d.b = "{'a': 'a', 'b': 2}"
d.c = "${b}"
d.d = "${a[a]}"
d.f = "${c[b]}+1"
d.g = "${{bcopy: ${c[b]}, fcopy: ${f}}}"     # syntax within ${}, PEP 3101 holds (no quote) - local evaluation
d.h = "{'bcopy': ${c['b']}, 'fcopy': ${f}}"  # syntax outside ${} using global evaluation
d.i = "the value of h is: ${h}" # ${h} is used outside any evaluation/interpolation region
d.j = "the value of h is: {h}"  # 
d
```

      -------------:----------------------------------------
                  a: {'a': 'a', 'b': 2}
                  b: {'a': 'a', 'b': 2}
                   = {'a': 'a', 'b': 2}
                  c: ${b}
                   = {'a': 'a', 'b': 2}
                  d: ${a[a]}
                   = a
                  f: ${c[b]}+1
                   = 3
                  g: ${{bcopy: ${c[b]}, fcopy: ${f}}}
                   = {bcopy: 2, fcopy: 3}
                  h: {'bcopy': ${c['b']}, 'fcopy': ${f}}
                   = {'bcopy': 2, 'fcopy': 3}
                  i: the value of h is: ${h}
                   = the value of h is: { [...] opy': 2, 'fcopy': 3}
                  j: the value of h is: {h}
                   = the value of h is: { [...] opy': 2, 'fcopy': 3}
      -------------:----------------------------------------





    parameter list (param object) with 9 definitions





---



### **4 | Mathematical shorthands for vectors, matrices, 3D and 4D arrays**

Lists cannot be directly used as vectors and must be converted into NumPy arrays before performing vectorized operations.

<kbd>Note:</kbd>This section separate ***non-mathematical* syntaxes** leading to `list` instances from ***mathematical* ones** generating NumPy instances.

#### **4.1 | Non-Mathematical Syntaxes for Lists**

Numeric lists and lists of strings are non-mathematical containers. They accept *à la Matlab* and Pythonic shorthands for rapid prototyping and definitions. They cannot be used directly in NumPy operations, and only their scalar values can be used.

These syntaxes are used without `$[]` and operates only with a minimum of interpolation. Their use is limited to simple expressions and constants (`float`, `int`, `str`):
- `start:stop` and `start:step:stop` expands a list between `start` and `stop` values with a step `step` (default value = 1).
- `[a b; c d; e f]` embeds lists row-wise `[[a,b],[c,d],[e,f]]`, the result is not a NumPy object.
- the operator `*` repeats a string or lists element-wise 
- the lists can be indexed with `int`, including with negative integers (e.g., `-1` represents the last value, etc.)
- the list content can be included in a string with `{list}` without using `$`

The following example illustrates rapid syntaxes applicable to lists 
- `u.a` defines the list `[1,2,3,4,5]` using a matlab shorthand `1:5`
- `u.b` expands a list similarly using variables `start`, `step` and `stop`
- `u.c` defines explicitly a list combining values and `a[2]`
- `u.d` generates a nested list including numbers `exp(1)` and `pi`
- `u.f` repeats "~" `f_repetitions` times
- `u.g` repeats `["p"]` `g_repetitions` times
- `u.h` extracts the last sublist of `d`
- `u.i` embeds the value of `h` in a string


```python
u = param()
u.a = "1:5"
u.start = "0"
u.step = "10"
u.stop = "50"
u.b = "${start}:${step}:${stop}"
u.c = "[1,30,500,${a[2]}]"
u.d = "[1 e; 3 pi; 4 5.0]"
u.f_repetitions = "20"
u.f = "'~'*${f_repetitions}"
u.g_repetitions = "3"
u.g = "['p']*${g_repetitions}"
u.h = "${d[-1]}"
u.i = "the values of h are {h}"
u
```

      -------------:----------------------------------------
                  a: 1:5
                   = [1, 2, 3, 4, 5]
              start: 0
                   = 0
               step: 10
                   = 10
               stop: 50
                   = 50
                  b: ${start}:${step}:${stop}
                   = [0, 10, 20, 30, 40, 50]
                  c: [1,30,500,${a[2]}]
                   = [1, 30, 500, 3]
                  d: [1 e; 3 pi; 4 5.0]
                   = [[1, 2.7182818284590 [...] 53589793], [4, 5.0]]
      f_repetitions: 20
                   = 20
                  f: '~'*${f_repetitions}
                   = ~~~~~~~~~~~~~~~~~~~~
      g_repetitions: 3
                   = 3
                  g: ['p']*${g_repetitions}
                   = ['p', 'p', 'p']
                  h: ${d[-1]}
                   = [4, 5.0]
                  i: the values of h are {h}
                   = the values of h are [4, 5.0]
      -------------:----------------------------------------





    parameter list (param object) with 13 definitions



#### **4.2 | Mathematical/NumPy Syntax**

The `param()` class offers several shorthands to seamlessly manipulate NumPy arrays using `param` text expressions:

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

#### **4.3 | Simple Definitions Example**

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
                   = [1 2 3] (int64)
                  b: $[1;2;3]
                   = [1 2 3]T (int64)
                  c: $[0.1:0.1:0.9]
                   = [0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9] (double)
                  d: $[1 2 3; 4 5 6]
                   = [2×3 int64]
      -------------:----------------------------------------





    parameter list (param object) with 4 definitions



#### **4.4 | Matrix Operations Example**

This example illustrates simple matrix operations:
- `m.a` is a list of numeric values.
- `m.b` is a NumPy array created from `m.a` (as a row vector).
- `m.c` computes `m.a * 2` (element-wise multiplication for a list).
- `m.d` computes `m.b * 2` (element-wise multiplication for a NumPy array).
- `m.e` is the transpose of `m.b`.
- `m.f` performs matrix multiplication between the transpose of `m.b` and `m.b`.
- Variables `m.g` through `m.o` demonstrate various forms of expression evaluation, indexing, and string interpolation.
  - <kbd>note:</kbd> `"@{j}+1"` and `"${j}+1"` do not have the same meaning.
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



#### **4.5 | Slicing Example**

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
                   = [0 0 1] (int64)
                 o1: @{n}
                   = [0 0 1] (int64)
                 o2: $[${a},2,3]
                   = [1 2 3] (double)
                 o3: @{o1} @ @{o2}.T
                   = 3.0 (double)
                  d: @{n}.T @ $[[${a},2,3]]
                   = [3×3 double]
                  f: ($[${a},2,3]*${b}) @ [...] s.array([[0,0,1]]).T
                   = (np.atleast_2d(np.ar [...] s.array([[0,0,1]]).T
                 nT: @{n}.T
                   = [0 0 1]T (int64)
                  m: ${n.T}*2
                   = [[0]
     [0]
     [1]]*2
                  o: @{n}.T*2
                   = [0 0 2]T (int64)
                  p: $[[1,2],[3,4]]
                   = [2×2 int64]
                  q: ${p[1,1]}
                   = 4
                  r: ${p[:,1]}
                   = [2, 4]
                  s: @{p}[:,1]+1
                   = [3 5] (int64)
      -------------:----------------------------------------





    parameter list (param object) with 16 definitions



#### **4.6 | Advanced Example**

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





---



### **5 | Global evaluation**

A global evaluation is attempted for all expressions after interpolation and local evaluations have been performed.
If the global evaluation does not raise any error, the evaluated result is kept; otherwise, the original interpolated
expression is preserved. Since several expressions involving matrix operations require global evaluation (i.e., outside
of `${...}` or `@{...}`), it is recommended to define mathematically valid expressions and, if needed, use separate
variables to store results as text.


#### **5.1 | Global Evaluation Example with NumPy**

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
                   = [2×2 int64]
                  q: ${p[1, 1]}
                   = 4
                  r: @{p}[:,1] + 1
                   = [3 5] (int64)
                  s: @{p}[:, 1].reshape(-1, 1) @ @{r}
                   = [2×2 int64]
                  t: np.linalg.eig(@{s})
                   = EigResult(eigenvalue [...] 576, -0.89442719]]))
                  w: ${t.eigenvalues[0]}  [...]  ${t.eigenvalues[1]}
                   = 26.0
                  x: $[[0,${t.eigenvalues [...] {t.eigenvalues[1]}]]
                   = [0 26] (double)
      -------------:----------------------------------------





    parameter list (param object) with 7 definitions



#### **5.2 | Global Evaluation Example with Various Matrix and ND- Operations**

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
                   = [1 2 3] (int64)
                  b: $[1:3]
                   = [1 2 3] (int64)
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




---

<small>For any question, contact INRAE\olivier.vitrac@agroparistech.fr | last revision $2025-02-07$</small>

