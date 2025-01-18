#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__project__ = "Pizza3"
__author__ = "Olivier Vitrac"
__copyright__ = "Copyright 2022"
__credits__ = ["Olivier Vitrac"]
__license__ = "GPLv3"
__maintainer__ = "Olivier Vitrac"
__email__ = "olivier.vitrac@agroparistech.fr"
__version__ = "1.002"


"""
Module: struct.py
==================
Matlab-like structure class with extensions for parameter evaluation, file paths,
and automatic management of dependencies in parameter definitions. This module
provides the following key classes:

- `struct`: A flexible base class that mimics Matlab structures, offering dynamic
  field creation, indexing, concatenation, and field-level evaluation.
- `param`: Derived from `struct`, this class enables dynamic evaluation of fields
  based on interdependent definitions.
- `paramauto`: A further extension of `param` with automatic sorting and resolution
  of parameter dependencies during operations.
- `pstr`: A string subclass specialized for handling file paths and POSIX compatibility.

Purpose
-------
This module aims to streamline the creation and manipulation of structures for
scientific computation, data management, and dynamic scripting, particularly in
complex workflows.

Key Features
------------
- Flexible dynamic structure (`struct`) with field creation, deletion, and manipulation.
- Parameter evaluation and dependency resolution (`param`).
- Path and string management with POSIX compliance (`pstr`).
- Automatic dependency handling and evaluation (`paramauto`).

Examples
--------
### Basic Struct Usage
```python
s = struct(a=1, b=2, c='${a} + ${b}')
s.a = 10
s["b"] = 5
delattr(s, "c")  # Delete a field


### Parameter Evaluation with `param`
from struct import param

# Define parameters with dependencies
p = param(a=1, b='${a}*2', c='${b}+5')
evaluated = p.eval()  # Evaluate all fields dynamically
print(evaluated.c)  # Output: 7


### Path Management with `pstr`
from struct import pstr

# Create and manipulate POSIX-compliant paths
path = pstr("/this/is/a/path/")
combined = path / "file.txt"
print(combined)  # Output: "/this/is/a/path/file.txt"

### Automatic Dependency Handling with `paramauto`
from struct import paramauto

# Automatically resolve dependencies in parameters
pa = paramauto(a=1, b='${a}+1', c='${b}*2')
pa.disp()
# Output:
# -----------
#       a: 1
#       b: ${a}+1
#        = 2
#       c: ${b}*2
#        = 4
# -----------


Created on Sun Jan 23 14:19:03 2022

@author: olivier.vitrac@agroparistech.fr

"""

# revision history
# 2022-02-12 fix disp method for empty structures
# 2022-02-12 add type, format
# 2022-02-19 integration of the derived class param()
# 2022-02-20 code optimization, iterable class- major update
# 2022-02-26 clarify in the help the precedence s=s1+s2
# 2022-02-28 display nested structures
# 2022-03-01 implement value as list
# 2022-03-02 display correctly class names (not instances)
# 2022-03-04 add str()
# 2022-03-05 add __copy__ and __deepcopy__ methods
# 2022-03-05 AttributeError replaces KeyError in getattr() exceptions (required for for pdoc3)
# 2022-03-16 Prevent replacement/evaluation if the string is escaped \${parameter}
# 2022-03-19 add struct2dict(), dict2struct()
# 2022-03-20 add zip(), items()
# 2022-03-27 add __setitem__(), fromkeysvalues(), struct2param()
# 2022-03-28 add read() and write()
# 2022-03-29 fix protection for $var, $variable - add keysorted(), tostruct()
# 2022-03-30 specific display p"this/is/my/path" for pstr
# 2022-03-31 add dispmax()
# 2022-04-05 add check(), such that a.check(b) is similar to b+a
# 2022-04-09 manage None and [] values in check()
# 2022-05-14 s[:4], s[(3,5,2)] indexing a structure with a slice, list, turple generates a substructure
# 2022-05-14 isempty (property) is TRUE for an empty structure
# 2022-05-15 __getitem__ and __set__item are now vectorized, add clear()
# 2022-05-16 add sortdefinitions(), isexpression, isdefined(), isstrdefined()
# 2022-05-16 __add__ and __iadd__ when called explicitly (not with + and +=) accept sordefinitions=True
# 2022-05-16 improved help, add tostatic() - v 0.45 (major version)
# 2022-05-17 new class paramauto() to simplify the management of multiple definitions
# 2022-05-17 catches most common errors in expressions and display explicit error messages - v 0.46
# 2023-01-18 add indexing as a dictionary s["a"] is the same as s.a - 0.461
# 2023-01-19 add % as comment instead of # to enable replacement
# 2023-01-27 param.eval() add % to freeze an interpretation (needed when a list is spanned as a string)
# 2023-01-27 struct.format() will replace {var} by ${var} if var is not defined
# 2023-08-11 display "" as <empty string> if evaluated
# 2024-09-06 add _returnerror as paramm class attribute (default=true) - dscript.lambdaScriptdata overrides it
# 2024-09-12 file management for all OS
# 2024-09-12 repr() improvements
# 2024-10-09 enable @property as attribute if _propertyasattribute is True
# 2024-10-11 add _callable__ and update()
# 2024-10-22 raises an error in escape() if s is not a string
# 2024-10-25 add dellatr()
# 2024-10-26 force silentmode to + and += operators
# 2024-12-08 fix help
# 2025-01-17 enable evaluation with ! and first recursion for lists (v1.002)


# %% Dependencies
from math import * # import math to authorize all math expressions in parameters
import types       # to check types
import re          # regular expression
from pathlib import Path # for write
import numpy as np
from ast import literal_eval # used to evaluate strings starting with !
from copy import copy as duplicate # to duplicate objects
from copy import deepcopy as duplicatedeep # used by __deepcopy__()
from pathlib import PurePosixPath as PurePath

__all__ = ['param', 'paramauto', 'pstr', 'struct']


# %% core struct class
class struct():
    """
    Class: `struct`
    ================

    A lightweight class that mimics Matlab-like structures, with additional features
    such as dynamic field creation, indexing, concatenation, and compatibility with
    evaluated parameters (`param`).

    ---

    ### Features
    - Dynamic creation of fields.
    - Indexing and iteration support for fields.
    - Concatenation and subtraction of structures.
    - Conversion to and from dictionaries.
    - Compatible with `param` and `paramauto` for evaluation and dependency handling.

    ---

    ### Examples

    #### Basic Usage
    ```python
    s = struct(a=1, b=2, c='${a} + ${b} # evaluate me if you can')
    print(s.a)  # 1
    s.d = 11    # Append a new field
    delattr(s, 'd')  # Delete the field
    ```

    #### Using `param` for Evaluation
    ```python
    p = param(a=1, b=2, c='${a} + ${b} # evaluate me if you can')
    p.eval()
    # Output:
    # --------
    #      a: 1
    #      b: 2
    #      c: ${a} + ${b} # evaluate me if you can (= 3)
    # --------
    ```

    ---

    ### Concatenation and Subtraction
    Fields from the right-most structure overwrite existing values.
    ```python
    a = struct(a=1, b=2)
    b = struct(c=3, d="d", e="e")
    c = a + b
    e = c - a
    ```

    ---

    ### Practical Shorthands

    #### Constructing a Structure from Keys
    ```python
    s = struct.fromkeys(["a", "b", "c", "d"])
    # Output:
    # --------
    #      a: None
    #      b: None
    #      c: None
    #      d: None
    # --------
    ```

    #### Building a Structure from Variables in a String
    ```python
    s = struct.scan("${a} + ${b} * ${c} / ${d} --- ${ee}")
    s.a = 1
    s.b = "test"
    s.c = [1, "a", 2]
    s.generator()
    # Output:
    # X = struct(
    #      a=1,
    #      b="test",
    #      c=[1, 'a', 2],
    #      d=None,
    #      ee=None
    # )
    ```

    #### Indexing and Iteration
    Structures can be indexed or sliced like lists.
    ```python
    c = a + b
    c[0]      # Access the first field
    c[-1]     # Access the last field
    c[:2]     # Slice the structure
    for field in c:
        print(field)
    ```

    ---

    ### Dynamic Dependency Management
    `struct` provides control over dependencies, sorting, and evaluation.

    ```python
    s = struct(d=3, e="${c} + {d}", c='${a} + ${b}', a=1, b=2)
    s.sortdefinitions()
    # Output:
    # --------
    #      d: 3
    #      a: 1
    #      b: 2
    #      c: ${a} + ${b}
    #      e: ${c} + ${d}
    # --------
    ```

    For dynamic evaluation, use `param`:
    ```python
    p = param(sortdefinitions=True, d=3, e="${c} + ${d}", c='${a} + ${b}', a=1, b=2)
    # Output:
    # --------
    #      d: 3
    #      a: 1
    #      b: 2
    #      c: ${a} + ${b}  (= 3)
    #      e: ${c} + ${d}  (= 6)
    # --------
    ```

    ---

    ### Overloaded Methods and Operators
    #### Supported Operators
    - `+`: Concatenation of two structures (`__add__`).
    - `-`: Subtraction of fields (`__sub__`).
    - `len()`: Number of fields (`__len__`).
    - `in`: Check for field existence (`__contains__`).

    #### Method Overview
    | Method                | Description                                             |
    |-----------------------|---------------------------------------------------------|
    | `check(default)`      | Populate fields with defaults if missing.               |
    | `clear()`             | Remove all fields.                                      |
    | `dict2struct(dico)`   | Create a structure from a dictionary.                   |
    | `disp()`              | Display the structure.                                  |
    | `eval()`              | Evaluate expressions within fields.                     |
    | `fromkeys(keys)`      | Create a structure from a list of keys.                 |
    | `generator()`         | Generate Python code representing the structure.        |
    | `items()`             | Return key-value pairs.                                 |
    | `keys()`              | Return all keys in the structure.                       |
    | `read(file)`          | Load structure fields from a file.                      |
    | `scan(string)`        | Extract variables from a string and populate fields.    |
    | `sortdefinitions()`   | Sort fields to resolve dependencies.                    |
    | `struct2dict()`       | Convert the structure to a dictionary.                  |
    | `values()`            | Return all field values.                                |
    | `write(file)`         | Save the structure to a file.                           |

    ---

    ### Dynamic Properties
    | Property    | Description                            |
    |-------------|----------------------------------------|
    | `isempty`   | `True` if the structure is empty.      |
    | `isdefined` | `True` if all fields are defined.      |

    ---
    """

    # attributes to be overdefined
    _type = "struct"        # object type
    _fulltype = "structure" # full name
    _ftype = "field"        # field name
    _evalfeature = False    # true if eval() is available
    _maxdisplay = 40        # maximum number of characters to display (should be even)
    _propertyasattribute = False

    # attributes for the iterator method
    # Please keep it static, duplicate the object before changing _iter_
    _iter_ = 0

    # excluded attributes (keep the , in the Tupple if it is singleton)
    _excludedattr = {'_iter_','__class__','_protection','_evaluation','_returnerror'} # used by keys() and len()


    # Methods
    def __init__(self,**kwargs):
        """ constructor """
        # Optionally extend _excludedattr here
        self._excludedattr = self._excludedattr | {'_excludedattr', '_type', '_fulltype','_ftype'} # addition 2024-10-11
        self.set(**kwargs)

    def zip(self):
        """ zip keys and values """
        return zip(self.keys(),self.values())

    @staticmethod
    def dict2struct(dico,makeparam=False):
        """ create a structure from a dictionary """
        if isinstance(dico,dict):
            s = param() if makeparam else struct()
            s.set(**dico)
            return s
        raise TypeError("the argument must be a dictionary")

    def struct2dict(self):
        """ create a dictionary from the current structure """
        return dict(self.zip())

    def struct2param(self,protection=False,evaluation=True):
        """ convert an object struct() to param() """
        p = param(**self.struct2dict())
        for i in range(len(self)):
            if isinstance(self[i],pstr): p[i] = pstr(p[i])
        p._protection = protection
        p._evaluation = evaluation
        return p

    def set(self,**kwargs):
        """ initialization """
        self.__dict__.update(kwargs)

    def setattr(self,key,value):
        """ set field and value """
        if isinstance(value,list) and len(value)==0 and key in self:
            delattr(self, key)
        else:
            self.__dict__[key] = value

    def getattr(self,key):
        """Get attribute override to access both instance attributes and properties if allowed."""
        if key in self.__dict__:
            return self.__dict__[key]
        elif getattr(self, '_propertyasattribute', False) and \
             key not in self._excludedattr and \
             key in self.__class__.__dict__ and isinstance(self.__class__.__dict__[key], property):
            # If _propertyasattribute is True and it's a property, get its value
            return self.__class__.__dict__[key].fget(self)
        else:
            raise AttributeError(f'the {self._ftype} "{key}" does not exist')

    def hasattr(self, key):
        """Return true if the field exists, considering properties as regular attributes if allowed."""
        return key in self.__dict__ or (
            getattr(self, '_propertyasattribute', False) and
            key not in self._excludedattr and
            key in self.__class__.__dict__ and isinstance(self.__class__.__dict__[key], property)
        )

    def __getstate__(self):
        """ getstate for cooperative inheritance / duplication """
        return self.__dict__.copy()

    def __setstate__(self,state):
        """ setstate for cooperative inheritance / duplication """
        self.__dict__.update(state)

    def __getattr__(self,key):
        """ get attribute override """
        return pstr.eval(self.getattr(key))

    def __setattr__(self,key,value):
        """ set attribute override """
        self.setattr(key,value)

    def __contains__(self,item):
        """ in override """
        return self.hasattr(item)

    def keys(self):
        """ return the fields """
        # keys() is used by struct() and its iterator
        return [key for key in self.__dict__.keys() if key not in self._excludedattr]

    def keyssorted(self,reverse=True):
        """ sort keys by length() """
        klist = self.keys()
        l = [len(k) for k in klist]
        return [k for _,k in sorted(zip(l,klist),reverse=reverse)]

    def values(self):
        """ return the values """
        # values() is used by struct() and its iterator
        return [pstr.eval(value) for key,value in self.__dict__.items() if key not in self._excludedattr]

    @staticmethod
    def fromkeysvalues(keys,values,makeparam=False):
        """ struct.keysvalues(keys,values) creates a structure from keys and values
            use makeparam = True to create a param instead of struct
        """
        if keys is None: raise AttributeError("the keys must not empty")
        if not isinstance(keys,(list,tuple,np.ndarray,np.generic)): keys = [keys]
        if not isinstance(values,(list,tuple,np.ndarray,np.generic)): values = [values]
        nk,nv = len(keys), len(values)
        s = param() if makeparam else struct()
        if nk>0 and nv>0:
            iv = 0
            for ik in range(nk):
                s.setattr(keys[ik], values[iv])
                iv = min(nv-1,iv+1)
            for ik in range(nk,nv):
                s.setattr(f"key{ik}", values[ik])
        return s

    def items(self):
        """ return all elements as iterable key, value """
        return self.zip()

    def __getitem__(self,idx):
        """
            s[i] returns the ith element of the structure
            s[:4] returns a structure with the four first fields
            s[[1,3]] returns the second and fourth elements
        """
        if isinstance(idx,int):
            if idx<len(self):
                return self.getattr(self.keys()[idx])
            raise IndexError(f"the {self._ftype} index should be comprised between 0 and {len(self)-1}")
        elif isinstance(idx,slice):
            return struct.fromkeysvalues(self.keys()[idx], self.values()[idx])
        elif isinstance(idx,(list,tuple)):
            k,v= self.keys(), self.values()
            nk = len(k)
            s = param() if isinstance(self,param) else struct()
            for i in idx:
                if isinstance(i,int) and i>=0 and i<nk:
                    s.setattr(k[i],v[i])
                else:
                    raise IndexError("idx must contains only integers ranged between 0 and %d" % (nk-1))
            return s
        elif isinstance(idx,str):
            return self.getattr(idx)
        else:
            raise TypeError("The index must be an integer or a slice and not a %s" % type(idx).__name__)

    def __setitem__(self,idx,value):
        """ set the ith element of the structure  """
        if isinstance(idx,int):
            if idx<len(self):
                self.setattr(self.keys()[idx], value)
            else:
                raise IndexError(f"the {self._ftype} index should be comprised between 0 and {len(self)-1}")
        elif isinstance(idx,slice):
            k = self.keys()[idx]
            if len(value)<=1:
                for i in range(len(k)): self.setattr(k[i], value)
            elif len(k) == len(value):
                for i in range(len(k)): self.setattr(k[i], value[i])
            else:
                raise IndexError("the number of values (%d) does not match the number of elements in the slive (%d)" \
                       % (len(value),len(idx)))
        elif isinstance(idx,(list,tuple)):
            if len(value)<=1:
                for i in range(len(idx)): self[idx[i]]=value
            elif len(idx) == len(value):
                for i in range(len(idx)): self[idx[i]]=value[i]
            else:
                raise IndexError("the number of values (%d) does not match the number of indices (%d)" \
                                 % (len(value),len(idx)))

    def __len__(self):
        """ return the number of fields """
        # len() is used by struct() and its iterator
        return len(self.keys())

    def __iter__(self):
        """ struct iterator """
        # note that in the original object _iter_ is a static property not in dup
        dup = duplicate(self)
        dup._iter_ = 0
        return dup

    def __next__(self):
        """ increment iterator """
        self._iter_ += 1
        if self._iter_<=len(self):
            return self[self._iter_-1]
        self._iter_ = 0
        raise StopIteration(f"Maximum {self._ftype} iteration reached {len(self)}")

    def __add__(self,s,sortdefinitions=False,raiseerror=True, silentmode=True):
        """ add a structure
            set sortdefintions=True to sort definitions (to maintain executability)
        """
        if not isinstance(s,struct):
            raise TypeError(f"the second operand must be {self._type}")
        dup = duplicate(self)
        dup.__dict__.update(s.__dict__)
        if sortdefinitions: dup.sortdefinitions(raiseerror=raiseerror,silentmode=silentmode)
        return dup

    def __iadd__(self,s,sortdefinitions=False,raiseerror=False, silentmode=True):
        """ iadd a structure
            set sortdefintions=True to sort definitions (to maintain executability)
        """
        if not isinstance(s,struct):
            raise TypeError(f"the second operand must be {self._type}")
        self.__dict__.update(s.__dict__)
        if sortdefinitions: self.sortdefinitions(raiseerror=raiseerror,silentmode=silentmode)
        return self

    def __sub__(self,s):
        """ sub a structure """
        if not isinstance(s,struct):
            raise TypeError(f"the second operand must be {self._type}")
        dup = duplicate(self)
        listofkeys = dup.keys()
        for k in s.keys():
            if k in listofkeys:
                delattr(dup,k)
        return dup

    def __isub__(self,s):
        """ isub a structure """
        if not isinstance(s,struct):
            raise TypeError(f"the second operand must be {self._type}")
        listofkeys = self.keys()
        for k in s.keys():
            if k in listofkeys:
                delattr(self,k)
        return self

    def dispmax(self,content):
        """ optimize display """
        strcontent = str(content)
        if len(strcontent)>self._maxdisplay:
            nchar = round(self._maxdisplay/2)
            return strcontent[:nchar]+" [...] "+strcontent[-nchar:]
        else:
            return content

    def __repr__(self):
        """ display method """
        if self.__dict__=={}:
            print(f"empty {self._fulltype} ({self._type} object) with no {self._type}s")
            return f"empty {self._fulltype}"
        else:
            tmp = self.eval() if self._evalfeature else []
            keylengths = [len(key) for key in self.__dict__]
            width = max(10,max(keylengths)+2)
            fmt = "%%%ss:" % width
            fmteval = fmt[:-1]+"="
            fmtcls =  fmt[:-1]+":"
            line = ( fmt % ('-'*(width-2)) ) + ( '-'*(min(40,width*5)) )
            print(line)
            for key,value in self.__dict__.items():
                if key not in self._excludedattr:
                    if isinstance(value,(int,float,str,list,tuple,np.ndarray,np.generic)):
                        if isinstance(value,pstr):
                            print(fmt % key,'p"'+self.dispmax(value)+'"')
                        if isinstance(value,str) and value=="":
                            print(fmt % key,'""')
                        else:
                            print(fmt % key,self.dispmax(value))
                    elif isinstance(value,struct):
                        print(fmt % key,self.dispmax(value.__str__()))
                    elif isinstance(value,type):
                        print(fmt % key,self.dispmax(str(value)))
                    else:
                        print(fmt % key,type(value))
                        print(fmtcls % "",self.dispmax(str(value)))
                    if self._evalfeature:
                        if isinstance(self,paramauto):
                            try:
                                if isinstance(value,pstr):
                                    print(fmteval % "",'p"'+self.dispmax(tmp.getattr(key))+'"')
                                elif isinstance(value,str):
                                    if value == "":
                                        print(fmteval % "",self.dispmax("<empty string>"))
                                    else:
                                        print(fmteval % "",self.dispmax(tmp.getattr(key)))
                            except Exception as err:
                                print(fmteval % "",err.message, err.args)
                        else:
                            if isinstance(value,pstr):
                                print(fmteval % "",'p"'+self.dispmax(tmp.getattr(key))+'"')
                            elif isinstance(value,str):
                                if value == "":
                                    print(fmteval % "",self.dispmax("<empty string>"))
                                else:
                                    print(fmteval % "",self.dispmax(tmp.getattr(key)))
            print(line)
            return f"{self._fulltype} ({self._type} object) with {len(self)} {self._ftype}s"

    def disp(self):
        """ display method """
        self.__repr__()

    def __str__(self):
        return f"{self._fulltype} ({self._type} object) with {len(self)} {self._ftype}s"

    @property
    def isempty(self):
        """ isempty is set to True for an empty structure """
        return len(self)==0

    def clear(self):
        """ clear() delete all fields while preserving the original class """
        for k in self.keys(): delattr(self,k)

    def format(self,s,escape=False,raiseerror=True):
        """
            format a string with field (use {field} as placeholders)
                s.replace(string), s.replace(string,escape=True)
                where:
                    s is a struct object
                    string is a string with possibly ${variable1}
                    escape is a flag to prevent ${} replaced by {}
        """
        if raiseerror:
            try:
                if escape:
                    return s.format(**self.__dict__)
                else:
                    return s.replace("${","{").format(**self.__dict__)
            except KeyError as kerr:
                s_ = s.replace("{","${")
                print(f"WARNING: the {self._ftype} {kerr} is undefined in '{s_}'")
                return s_ # instead of s (we put back $) - OV 2023/01/27
            except Exception as othererr:
                s_ = s.replace("{","${")
                raise RuntimeError from othererr
        else:
            if escape:
                return s.format(**self.__dict__)
            else:
                return s.replace("${","{").format(**self.__dict__)

    def fromkeys(self,keys):
        """ returns a structure from keys """
        return self+struct(**dict.fromkeys(keys,None))

    @staticmethod
    def scan(s):
        """ scan(string) scan a string for variables """
        if not isinstance(s,str): raise TypeError("scan() requires a string")
        tmp = struct()
        #return tmp.fromkeys(set(re.findall(r"\$\{(.*?)\}",s)))
        found = re.findall(r"\$\{(.*?)\}",s);
        uniq = []
        for x in found:
            if x not in uniq: uniq.append(x)
        return tmp.fromkeys(uniq)

    @staticmethod
    def isstrexpression(s):
        """ isstrexpression(string) returns true if s contains an expression  """
        if not isinstance(s,str): raise TypeError("s must a string")
        return re.search(r"\$\{.*?\}",s) is not None

    @property
    def isexpression(self):
        """ same structure with True if it is an expression """
        s = param() if isinstance(self,param) else struct()
        for k,v in self.items():
            if isinstance(v,str):
                s.setattr(k,struct.isstrexpression(v))
            else:
                s.setattr(k,False)
        return s

    @staticmethod
    def isstrdefined(s,ref):
        """ isstrdefined(string,ref) returns true if it is defined in ref  """
        if not isinstance(s,str): raise TypeError("s must a string")
        if not isinstance(ref,struct): raise TypeError("ref must be a structure")
        if struct.isstrexpression(s):
            k = struct.scan(s).keys()
            allfound,i,nk = True,0,len(k)
            while (i<nk) and allfound:
                allfound = k[i] in ref
                i += 1
            return allfound
        else:
            return False


    def isdefined(self,ref=None):
        """ isdefined(ref) returns true if it is defined in ref """
        s = param() if isinstance(self,param) else struct()
        k,v,isexpr = self.keys(), self.values(), self.isexpression.values()
        nk = len(k)
        if ref is None:
            for i in range(nk):
                if isexpr[i]:
                    s.setattr(k[i],struct.isstrdefined(v[i],self[:i]))
                else:
                    s.setattr(k[i],True)
        else:
            if not isinstance(ref,struct): raise TypeError("ref must be a structure")
            for i in range(nk):
                if isexpr[i]:
                    s.setattr(k[i],struct.isstrdefined(v[i],ref))
                else:
                    s.setattr(k[i],True)
        return s

    def sortdefinitions(self,raiseerror=True,silentmode=False):
        """ sortdefintions sorts all definitions
            so that they can be executed as param().
            If any inconsistency is found, an error message is generated.

            Flags = default values
                raiseerror=True show erros of True
                silentmode=False no warning if True
        """
        find = lambda xlist: [i for i, x in enumerate(xlist) if x]
        findnot = lambda xlist: [i for i, x in enumerate(xlist) if not x]
        k,v,isexpr =  self.keys(), self.values(), self.isexpression.values()
        istatic = findnot(isexpr)
        idynamic = find(isexpr)
        static = struct.fromkeysvalues(
            [ k[i] for i in istatic ],
            [ v[i] for i in istatic ],
            makeparam = False)
        dynamic = struct.fromkeysvalues(
            [ k[i] for i in idynamic ],
            [ v[i] for i in idynamic ],
            makeparam=False)
        current = static # make static the current structure
        nmissing, anychange, errorfound = len(dynamic), False, False
        while nmissing:
            itst, found = 0, False
            while itst<nmissing and not found:
                teststruct = current + dynamic[[itst]] # add the test field
                found = all(list(teststruct.isdefined()))
                ifound = itst
                itst += 1
            if found:
                current = teststruct # we accept the new field
                dynamic[ifound] = []
                nmissing -= 1
                anychange = True
            else:
                if raiseerror:
                    raise KeyError('unable to interpret %d/%d expressions in "%ss"' % \
                                   (nmissing,len(self),self._ftype))
                else:
                    if (not errorfound) and (not silentmode):
                        print('WARNING: unable to interpret %d/%d expressions in "%ss"' % \
                              (nmissing,len(self),self._ftype))
                    current = teststruct # we accept the new field (even if it cannot be interpreted)
                    dynamic[ifound] = []
                    nmissing -= 1
                    errorfound = True
        if anychange:
            self.clear() # reset all fields and assign them in the proper order
            k,v = current.keys(), current.values()
            for i in range(len(k)):
                self.setattr(k[i],v[i])

    def generator(self):
        """ generate Python code of the equivalent structure """
        nk = len(self)
        if nk==0:
            print("X = struct()")
        else:
            ik = 0
            fmt = "%%%ss=" % max(10,max([len(k) for k in self.keys()])+2)
            print("\nX = struct(")
            for k in self.keys():
                ik += 1
                end = ",\n" if ik<nk else "\n"+(fmt[:-1] % ")")+"\n"
                v = getattr(self,k)
                if isinstance(v,(int,float)) or v == None:
                    print(fmt % k,v,end=end)
                elif isinstance(v,str):
                    print(fmt % k,f'"{v}"',end=end)
                elif isinstance(v,(list,tuple)):
                    print(fmt % k,v,end=end)
                else:
                    print(fmt % k,"/* unsupported type */",end=end)

    # copy and deep copy methpds for the class
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
            setattr(copie, k, duplicatedeep(v, memo))
        return copie


    # write a file
    def write(self, file, overwrite=True, mkdir=False):
        """
            write the equivalent structure (not recursive for nested struct)
                write(filename, overwrite=True, mkdir=False)

            Parameters:
            - file: The file path to write to.
            - overwrite: Whether to overwrite the file if it exists (default: True).
            - mkdir: Whether to create the directory if it doesn't exist (default: False).
        """
        # Create a Path object for the file to handle cross-platform paths
        file_path = Path(file).resolve()

        # Check if the directory exists or if mkdir is set to True, create it
        if mkdir:
            file_path.parent.mkdir(parents=True, exist_ok=True)
        elif not file_path.parent.exists():
            raise FileNotFoundError(f"The directory {file_path.parent} does not exist.")
        # If overwrite is False and the file already exists, raise an exception
        if not overwrite and file_path.exists():
            raise FileExistsError(f"The file {file_path} already exists, and overwrite is set to False.")
        # Open and write to the file using the resolved path
        with file_path.open(mode="w", encoding='utf-8') as f:
            print(f"# {self._fulltype} with {len(self)} {self._ftype}s\n", file=f)
            for k, v in self.items():
                if v is None:
                    print(k, "=None", file=f, sep="")
                elif isinstance(v, (int, float)):
                    print(k, "=", v, file=f, sep="")
                elif isinstance(v, str):
                    print(k, '="', v, '"', file=f, sep="")
                else:
                    print(k, "=", str(v), file=f, sep="")


    # read a file
    @staticmethod
    def read(file):
        """
            read the equivalent structure
                read(filename)

            Parameters:
            - file: The file path to read from.
        """
        # Create a Path object for the file to handle cross-platform paths
        file_path = Path(file).resolve()
        # Check if the parent directory exists, otherwise raise an error
        if not file_path.parent.exists():
            raise FileNotFoundError(f"The directory {file_path.parent} does not exist.")
        # If the file does not exist, raise an exception
        if not file_path.exists():
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        # Open and read the file
        with file_path.open(mode="r", encoding="utf-8") as f:
            s = struct()  # Assuming struct is defined elsewhere
            while True:
                line = f.readline()
                if not line:
                    break
                line = line.strip()
                expr = line.split(sep="=")
                if len(line) > 0 and line[0] != "#" and len(expr) > 0:
                    lhs = expr[0]
                    rhs = "".join(expr[1:]).strip()
                    if len(rhs) == 0 or rhs == "None":
                        v = None
                    else:
                        v = eval(rhs)
                    s.setattr(lhs, v)
        return s

    # argcheck
    def check(self,default):
        """
        populate fields from a default structure
            check(defaultstruct)
            missing field, None and [] values are replaced by default ones

            Note: a.check(b) is equivalent to b+a except for [] and None values
        """
        if not isinstance(default,struct):
            raise TypeError("the first argument must be a structure")
        for f in default.keys():
            ref = default.getattr(f)
            if f not in self:
                self.setattr(f, ref)
            else:
                current = self.getattr(f)
                if ((current is None)  or (current==[])) and \
                    ((ref is not None) and (ref!=[])):
                        self.setattr(f, ref)


    # update values based on key:value
    def update(self, **kwargs):
        """
        Update multiple fields at once, while protecting certain attributes.

        Parameters:
        -----------
        **kwargs : dict
            The fields to update and their new values.

        Protected attributes defined in _excludedattr are not updated.

        Usage:
        ------
        s.update(a=10, b=[1, 2, 3], new_field="new_value")
        """
        protected_attributes = getattr(self, '_excludedattr', ())

        for key, value in kwargs.items():
            if key in protected_attributes:
                print(f"Warning: Cannot update protected attribute '{key}'")
            else:
                self.setattr(key, value)


    # override () for subindexing structure with key names
    def __call__(self, *keys):
        """
        Extract a sub-structure based on the specified keys,
        keeping the same class type.

        Parameters:
        -----------
        *keys : str
            The keys for the fields to include in the sub-structure.

        Returns:
        --------
        struct
            A new instance of the same class as the original, containing
            only the specified keys.

        Usage:
        ------
        sub_struct = s('key1', 'key2', ...)
        """
        # Create a new instance of the same class
        sub_struct = self.__class__()

        # Get the full type and field type for error messages
        fulltype = getattr(self, '_fulltype', 'structure')
        ftype = getattr(self, '_ftype', 'field')

        # Add only the specified keys to the new sub-structure
        for key in keys:
            if key in self:
                sub_struct.setattr(key, self.getattr(key))
            else:
                raise KeyError(f"{fulltype} does not contain the {ftype} '{key}'.")

        return sub_struct


    def __delattr__(self, key):
        """ Delete an instance attribute if it exists and is not a class or excluded attribute. """
        if key in self._excludedattr:
            raise AttributeError(f"Cannot delete excluded attribute '{key}'")
        elif key in self.__class__.__dict__:  # Check if it's a class attribute
            raise AttributeError(f"Cannot delete class attribute '{key}'")
        elif key in self.__dict__:  # Delete only if in instance's __dict__
            del self.__dict__[key]
        else:
            raise AttributeError(f"{self._type} has no attribute '{key}'")


# %% param class with scripting and evaluation capabilities
class param(struct):
    """
    Class: `param`
    ==============

    A class derived from `struct` that introduces dynamic evaluation of field values.
    The `param` class acts as a container for evaluated parameters, allowing expressions
    to depend on other fields. It supports advanced evaluation, sorting of dependencies,
    and text formatting.

    ---

    ### Features
    - Inherits all functionalities of `struct`.
    - Supports dynamic evaluation of field expressions.
    - Automatically resolves dependencies between fields.
    - Includes utility methods for text formatting and evaluation.

    ---

    ### Examples

    #### Basic Usage with Evaluation
    ```python
    s = param(a=1, b=2, c='${a} + ${b} # evaluate me if you can', d="$this is a string", e="1000 # this is my number")
    s.eval()
    # Output:
    # --------
    #      a: 1
    #      b: 2
    #      c: ${a} + ${b} # evaluate me if you can (= 3)
    #      d: $this is a string (= this is a string)
    #      e: 1000 # this is my number (= 1000)
    # --------

    s.a = 10
    s.eval()
    # Output:
    # --------
    #      a: 10
    #      b: 2
    #      c: ${a} + ${b} # evaluate me if you can (= 12)
    #      d: $this is a string (= this is a string)
    #      e: 1000 # this is my number (= 1000)
    # --------
    ```

    #### Handling Text Parameters
    ```python
    s = param()
    s.mypath = "$/this/folder"
    s.myfile = "$file"
    s.myext = "$ext"
    s.fullfile = "$${mypath}/${myfile}.${myext}"
    s.eval()
    # Output:
    # --------
    #    mypath: $/this/folder (= /this/folder)
    #    myfile: $file (= file)
    #     myext: $ext (= ext)
    #  fullfile: $${mypath}/${myfile}.${myext} (= /this/folder/file.ext)
    # --------
    ```

    ---

    ### Text Evaluation and Formatting

    #### Evaluate Strings
    ```python
    s = param(a=1, b=2)
    result = s.eval("this is a string with ${a} and ${b}")
    print(result)  # "this is a string with 1 and 2"
    ```

    #### Prevent Evaluation
    ```python
    definitions = param(a=1, b="${a}*10+${a}", c="\${a}+10", d='\${myparam}')
    text = definitions.formateval("this is my text ${a}, ${b}, \${myvar}=${c}+${d}")
    print(text)  # "this is my text 1, 11, \${myvar}=\${a}+10+${myparam}"
    ```

    ---

    ### Advanced Usage

    #### Rearranging and Sorting Definitions
    ```python
    s = param(
        a=1,
        f="${e}/3",
        e="${a}*${c}",
        c="${a}+${b}",
        b=2,
        d="${c}*2"
    )
    s.sortdefinitions()
    s.eval()
    # Output:
    # --------
    #      a: 1
    #      b: 2
    #      c: ${a} + ${b} (= 3)
    #      d: ${c} * 2 (= 6)
    #      e: ${a} * ${c} (= 3)
    #      f: ${e} / 3 (= 1.0)
    # --------
    ```

    #### Internal Evaluation and Recursion with !
    ```python
    p=param()
    p.a = [0,1,2]
    p.b = '![1,2,"test","${a[1]}"]'
    p
    # Output:
    #  -------------:----------------------------------------
    #          a: [0, 1, 2]
    #          b: ![1,2,"test","${a[1]}"]
    #           = [1, 2, 'test', '1']
    #  -------------:----------------------------------------
    # Out: parameter list (param object) with 2 definitions
    ```

    #### Error Handling
    ```python
    p = param(b="${a}+1", c="${a}+${d}", a=1)
    p.disp()
    # Output:
    # --------
    #      b: ${a} + 1 (= 2)
    #      c: ${a} + ${d} (= < undef definition "${d}" >)
    #      a: 1
    # --------
    ```

    Sorting unresolved definitions raises errors unless explicitly suppressed:
    ```python
    p.sortdefinitions(raiseerror=False)
    # WARNING: unable to interpret 1/3 expressions in "definitions"
    ```

    ---

    ### Utility Methods
    | Method                | Description                                             |
    |-----------------------|---------------------------------------------------------|
    | `eval()`              | Evaluate all field expressions.                         |
    | `formateval(string)`  | Format and evaluate a string with field placeholders.   |
    | `protect(string)`     | Escape variable placeholders in a string.               |
    | `sortdefinitions()`   | Sort definitions to resolve dependencies.               |
    | `escape(string)`      | Protect escaped variables in a string.                  |

    ---

    ### Overloaded Methods and Operators
    #### Supported Operators
    - `+`: Concatenation of two parameter lists, sorting definitions.
    - `-`: Subtraction of fields.
    - `len()`: Number of fields.
    - `in`: Check for field existence.

    ---

    ### Notes
    - The `paramauto` class simplifies handling of partial definitions and inherits from `param`.
    - Use `paramauto` when definitions need to be stacked irrespective of execution order.
    """

    # override
    _type = "param"
    _fulltype = "parameter list"
    _ftype = "definition"
    _evalfeature = True    # This class can be evaluated with .eval()
    _returnerror = True    # This class returns an error in the evaluation string (added on 2024-09-06)

    # magic constructor
    def __init__(self,_protection=False,_evaluation=True,
                 sortdefinitions=False,**kwargs):
        """ constructor """
        super().__init__(**kwargs)
        self._protection = _protection
        self._evaluation = _evaluation
        if sortdefinitions: self.sortdefinitions()

    # escape definitions if needed
    @staticmethod
    def escape(s):
        """
            escape \${} as ${{}} --> keep variable names
            convert ${} as {} --> prepare Python replacement

            Examples:
                escape("\${a}")
                returns ('${{a}}', True)

                escape("  \${abc} ${a} \${bc}")
                returns ('  ${{abc}} {a} ${{bc}}', True)

                escape("${a}")
                Out[94]: ('{a}', False)

                escape("${tata}")
                returns ('{tata}', False)

        """
        if not isinstance(s,str):
            raise TypeError(f'the argument must be string not {type(s)}')
        se, start, found = "", 0, True
        while found:
            pos0 = s.find("\${",start)
            found = pos0>=0
            if found:
                pos1 = s.find("}",pos0)
                found = pos1>=0
                if found:
                    se += s[start:pos0].replace("${","{")+"${{"+s[pos0+3:pos1]+"}}"
                    start=pos1+1
        result = se+s[start:].replace("${","{")
        if isinstance(s,pstr): result = pstr(result)
        return result,start>0

    # protect variables in a string
    def protect(self,s=""):
        """ protect $variable as ${variable} """
        if isinstance(s,str):
            t = s.replace("\$","££") # && is a placeholder
            escape = t!=s
            for k in self.keyssorted():
                t = t.replace("$"+k,"${"+k+"}")
            if escape: t = t.replace("££","\$")
            if isinstance(s,pstr): t = pstr(t)
            return t, escape
        raise TypeError(f'the argument must be string not {type(s)}')


    # lines starting with # (hash) are interpreted as comments
    # ${variable} or {variable} are substituted by variable.value
    # any line starting with $ is assumed to be a string (no interpretation)
    # ^ is accepted in formula(replaced by **))
    def eval(self,s="",protection=False):
        """
            Eval method for structure such as MS.alias

                s = p.eval() or s = p.eval(string)

                where :
                    p is a param object
                    s is a structure with evaluated fields
                    string is only used to determine whether definitions have been forgotten

        """
        # Evaluate all DEFINITIONS
        # the argument s is only used by formateval() for error management
        tmp = struct()
        for key,value in self.items():
            # strings are assumed to be expressions on one single line
            if isinstance(value,str):
                # replace ${variable} (Bash, Lammps syntax) by {variable} (Python syntax)
                # use \${variable} to prevent replacement (espace with \)
                # Protect variables if required
                ispstr = isinstance(value,pstr)
                valuesafe = pstr.eval(value,ispstr=ispstr) # value.strip()
                if protection or self._protection:
                    valuesafe, escape0 = self.protect(valuesafe)
                else:
                    escape0 = False
                valuesafe, escape = param.escape(valuesafe)
                escape = escape or escape0
                # replace "^" (Matlab, Lammps exponent) by "**" (Python syntax)
                valuesafe = pstr.eval(valuesafe.replace("^","**"),ispstr=ispstr)
                # Remove all content after #
                # if the first character is '#', it is not comment (e.g. MarkDown titles)
                poscomment = valuesafe.find("#")
                if poscomment>0: valuesafe = valuesafe[0:poscomment].strip()
                # Literal string starts with $ (no interpretation), ! (evaluation)
                if not self._evaluation:
                    tmp.setattr(key, pstr.eval(tmp.format(valuesafe,escape),ispstr=ispstr))
                elif valuesafe.startswith("!"):
                    try:
                        vtmp = literal_eval(valuesafe[1:])
                        if isinstance(vtmp,list):
                            for i,item in enumerate(vtmp):
                                if isinstance(item,str) and not item.strip().startswith("$"):
                                    try:
                                        vtmp[i] = tmp.format(item, raiseerror=False)
                                    except Exception as ve:
                                        vtmp[i] = f"Error in <{item}>: {ve.__class__.__name__} - {str(ve)}"
                        tmp.setattr(key,vtmp)
                    except (SyntaxError, ValueError):
                        tmp.setattr(key, f"Error: {e.__class__.__name__} - {str(e)}")
                elif valuesafe.startswith("$") and not escape:
                    tmp.setattr(key,tmp.format(valuesafe[1:].lstrip())) # discard $
                elif valuesafe.startswith("%"):
                    tmp.setattr(key,tmp.format(valuesafe[1:].lstrip())) # discard %
                else: # string empty or which can be evaluated
                    if valuesafe=="":
                        tmp.setattr(key,valuesafe) # empty content
                    else:
                        if isinstance(value,pstr): # keep path
                            tmp.setattr(key, pstr.topath(tmp.format(valuesafe,escape=escape)))
                        elif escape:  # partial evaluation
                            tmp.setattr(key, tmp.format(valuesafe,escape=True))
                        else: # full evaluation
                            try:
                                resstr = tmp.format(valuesafe,raiseerror=False)
                            except (KeyError,NameError) as nameerr:
                                if self._returnerror: # added on 2024-09-06
                                    strnameerr = str(nameerr).replace("'","")
                                    tmp.setattr(key,'< undef %s "${%s}" >' % \
                                            (self._ftype,strnameerr))
                                else:
                                    tmp.setattr(key,value) #we keep the original value
                            except (SyntaxError,TypeError,ValueError) as commonerr:
                                tmp.setattr(key,"ERROR < %s >" % commonerr)
                            except Exception as othererr:
                                tmp.setattr(key,"Unknown Error < %s >" % othererr)
                            else:
                                try:
                                    reseval = eval(resstr)
                                except Exception as othererr:
                                    tmp.setattr(key,"Eval Error < %s >" % othererr)
                                else:
                                    tmp.setattr(key,reseval)
            elif isinstance(value,(int,float,list,tuple)): # already a number
                tmp.setattr(key, value) # store the value with the key
            else: # unsupported types
                if s.find("{"+key+"}")>=0:
                    print(f'*** WARNING ***\n\tIn the {self._ftype}:"\n{s}\n"')
                else:
                    print(f'unable to interpret the "{key}" of type {type(value)}')
        return tmp

    # formateval obeys to following rules
    # lines starting with # (hash) are interpreted as comments
    def formateval(self,s,protection=False):
        """
            format method with evaluation feature

                txt = p.formateval("this my text with ${variable1}, ${variable2} ")

                where:
                    p is a param object

                Example:
                    definitions = param(a=1,b="${a}",c="\${a}")
                    text = definitions.formateval("this my text ${a}, ${b}, ${c}")
                    print(text)

        """
        tmp = self.eval(s,protection=protection)
        # Do all replacements in s (keep comments)
        if len(tmp)==0:
            return s
        else:
            ispstr = isinstance(s,pstr)
            ssafe, escape = param.escape(s)
            slines = ssafe.split("\n")
            for i in range(len(slines)):
                poscomment = slines[i].find("#")
                if poscomment>=0:
                    while (poscomment>0) and (slines[i][poscomment-1]==" "):
                        poscomment -= 1
                    comment = slines[i][poscomment:len(slines[i])]
                    slines[i]  = slines[i][0:poscomment]
                else:
                    comment = ""
                # Protect variables if required
                if protection or self._protection:
                    slines[i], escape2 = self.protect(slines[i])
                # conversion
                if ispstr:
                    slines[i] = pstr.eval(tmp.format(slines[i],escape=escape),ispstr=ispstr)
                else:
                    slines[i] = tmp.format(slines[i],escape=escape)+comment
                # convert starting % into # to authorize replacement in comments
                if len(slines[i])>0:
                    if slines[i][0] == "%": slines[i]="#"+slines[i][1:]
            return "\n".join(slines)

    # returns the equivalent structure evaluated
    def tostruct(self,protection=False):
        """
            generate the evaluated structure
                tostruct(protection=False)
        """
        return self.eval(protection=protection)

    # returns the equivalent structure evaluated
    def tostatic(self):
        """ convert dynamic a param() object to a static struct() object.
            note: no interpretation
            note: use tostruct() to interpret them and convert it to struct
            note: tostatic().struct2param() makes it reversible
        """
        return struct.fromkeysvalues(self.keys(),self.values(),makeparam=False)

# %% str class for file and paths
# this class guarantees that paths are POSIX at any time


class pstr(str):
    """
    Class: `pstr`
    =============

    A specialized string class for handling paths and filenames, derived from `struct`.
    The `pstr` class ensures compatibility with POSIX-style paths and provides enhanced
    operations for path manipulation.

    ---

    ### Features
    - Maintains POSIX-style paths.
    - Automatically handles trailing slashes.
    - Supports path concatenation using `/`.
    - Converts seamlessly back to `str` for compatibility with string methods.
    - Includes additional utility methods for path evaluation and formatting.

    ---

    ### Examples

    #### Basic Usage
    ```python
    a = pstr("this/is/mypath//")
    b = pstr("mylocalfolder/myfile.ext")
    c = a / b
    print(c)  # this/is/mypath/mylocalfolder/myfile.ext
    ```

    #### Keeping Trailing Slashes
    ```python
    a = pstr("this/is/mypath//")
    print(a)  # this/is/mypath/
    ```

    ---

    ### Path Operations

    #### Path Concatenation
    Use the `/` operator to concatenate paths:
    ```python
    a = pstr("folder/subfolder")
    b = pstr("file.txt")
    c = a / b
    print(c)  # folder/subfolder/file.txt
    ```

    #### Path Evaluation
    Evaluate or convert paths while preserving the `pstr` type:
    ```python
    result = pstr.eval("some/path/afterreplacement", ispstr=True)
    print(result)  # some/path/afterreplacement
    ```

    ---

    ### Advanced Usage

    #### Using String Methods
    Methods like `replace()` convert `pstr` back to `str`. To retain the `pstr` type:
    ```python
    new_path = pstr.eval(a.replace("mypath", "newpath"), ispstr=True)
    print(new_path)  # this/is/newpath/
    ```

    #### Handling POSIX Paths
    The `pstr.topath()` method ensures the path remains POSIX-compliant:
    ```python
    path = pstr("C:\\Windows\\Path")
    posix_path = path.topath()
    print(posix_path)  # C:/Windows/Path
    ```

    ---

    ### Overloaded Operators

    #### Supported Operators
    - `/`: Concatenates two paths (`__truediv__`).
    - `+`: Concatenates strings as paths, resulting in a `pstr` object (`__add__`).
    - `+=`: Adds to an existing `pstr` object (`__iadd__`).

    ---

    ### Utility Methods

    | Method          | Description                                  |
    |------------------|----------------------------------------------|
    | `eval(value)`    | Evaluates the path or string for compatibility with `pstr`. |
    | `topath()`       | Returns the POSIX-compliant path.           |

    ---

    ### Notes
    - Use `pstr` for consistent and safe handling of file paths across different platforms.
    - Converts back to `str` when using non-`pstr` specific methods to ensure compatibility.
    """

    def __repr__(self):
        result = self.topath()
        if result[-1] != "/" and self[-1] == "/":
            result += "/"
        return result

    def topath(self):
        """ return a validated path """
        value = pstr(PurePath(self))
        if value[-1] != "/" and self [-1]=="/":
            value += "/"
        return value


    @staticmethod
    def eval(value,ispstr=False):
        """ evaluate the path of it os a path """
        if isinstance(value,pstr):
            return value.topath()
        elif isinstance(value,PurePath) or ispstr:
            return pstr(value).topath()
        else:
            return value

    def __truediv__(self,value):
        """ overload / """
        operand = pstr.eval(value)
        result = pstr(PurePath(self) / operand)
        if result[-1] != "/" and operand[-1] == "/":
            result += "/"
        return result

    def __add__(self,value):
        return pstr(str(self)+value)

    def __iadd__(self,value):
        return pstr(str(self)+value)


# %% class paramauto() which enforces sortdefinitions = True, raiseerror=False
class paramauto(param):
    """
    Class: `paramauto`
    ==================

    A subclass of `param` with enhanced handling for automatic sorting and evaluation
    of definitions. The `paramauto` class ensures that all fields are sorted to resolve
    dependencies, allowing seamless stacking of partially defined objects.

    ---

    ### Features
    - Inherits all functionalities of `param`.
    - Automatically sorts definitions for dependency resolution.
    - Simplifies handling of partial definitions in dynamic structures.
    - Supports safe concatenation of definitions.

    ---

    ### Examples

    #### Automatic Dependency Sorting
    Definitions are automatically sorted to resolve dependencies:
    ```python
    p = paramauto(a=1, b="${a}+1", c="${a}+${b}")
    p.disp()
    # Output:
    # --------
    #      a: 1
    #      b: ${a} + 1 (= 2)
    #      c: ${a} + ${b} (= 3)
    # --------
    ```

    #### Handling Missing Definitions
    Unresolved dependencies raise warnings but do not block execution:
    ```python
    p = paramauto(a=1, b="${a}+1", c="${a}+${d}")
    p.disp()
    # Output:
    # --------
    #      a: 1
    #      b: ${a} + 1 (= 2)
    #      c: ${a} + ${d} (= < undef definition "${d}" >)
    # --------
    ```

    ---

    ### Concatenation and Inheritance
    Concatenating `paramauto` objects resolves definitions:
    ```python
    p1 = paramauto(a=1, b="${a}+2")
    p2 = paramauto(c="${b}*3")
    p3 = p1 + p2
    p3.disp()
    # Output:
    # --------
    #      a: 1
    #      b: ${a} + 2 (= 3)
    #      c: ${b} * 3 (= 9)
    # --------
    ```

    ---

    ### Utility Methods

    | Method                | Description                                            |
    |-----------------------|--------------------------------------------------------|
    | `sortdefinitions()`   | Automatically sorts fields to resolve dependencies.    |
    | `eval()`              | Evaluate all fields, resolving dependencies.           |
    | `disp()`              | Display all fields with their resolved values.         |

    ---

    ### Overloaded Operators

    #### Supported Operators
    - `+`: Concatenates two `paramauto` objects, resolving dependencies.
    - `+=`: Updates the current object with another, resolving dependencies.
    - `len()`: Number of fields.
    - `in`: Check for field existence.

    ---

    ### Advanced Usage

    #### Partial Definitions
    The `paramauto` class simplifies handling of partially defined fields:
    ```python
    p = paramauto(a="${d}", b="${a}+1")
    p.disp()
    # Warning: Unable to resolve dependencies.
    # --------
    #      a: ${d} (= < undef definition "${d}" >)
    #      b: ${a} + 1 (= < undef definition "${d}" >)
    # --------

    p.d = 10
    p.disp()
    # Dependencies are resolved:
    # --------
    #      d: 10
    #      a: ${d} (= 10)
    #      b: ${a} + 1 (= 11)
    # --------
    ```

    ---

    ### Notes
    - The `paramauto` class is computationally more intensive than `param` due to automatic sorting.
    - It is ideal for managing dynamic systems with complex interdependencies.

    ### Examples
                    p = paramauto()
                    p.b = "${aa}"
                    p.disp()
                yields
                    WARNING: unable to interpret 1/1 expressions in "definitions"
                      -----------:----------------------------------------
                                b: ${aa}
                                 = < undef definition "${aa}" >
                      -----------:----------------------------------------
                      p.aa = 2
                      p.disp()
                yields
                    -----------:----------------------------------------
                             aa: 2
                              b: ${aa}
                               = 2
                    -----------:----------------------------------------
                    q = paramauto(c="${aa}+${b}")+p
                    q.disp()
                yields
                    -----------:----------------------------------------
                             aa: 2
                              b: ${aa}
                               = 2
                              c: ${aa}+${b}
                               = 4
                    -----------:----------------------------------------
                    q.aa = 30
                    q.disp()
                yields
                    -----------:----------------------------------------
                             aa: 30
                              b: ${aa}
                               = 30
                              c: ${aa}+${b}
                               = 60
                    -----------:----------------------------------------
                    q.aa = "${d}"
                    q.disp()
                yields multiple errors (recursion)
                WARNING: unable to interpret 3/3 expressions in "definitions"
                  -----------:----------------------------------------
                           aa: ${d}
                             = < undef definition "${d}" >
                            b: ${aa}
                             = Eval Error < invalid [...] (<string>, line 1) >
                            c: ${aa}+${b}
                             = Eval Error < invalid [...] (<string>, line 1) >
                  -----------:----------------------------------------
                    q.d = 100
                    q.disp()
                yields
                  -----------:----------------------------------------
                            d: 100
                           aa: ${d}
                             = 100
                            b: ${aa}
                             = 100
                            c: ${aa}+${b}
                             = 200
                  -----------:----------------------------------------


            Example:

                p = paramauto(b="${a}+1",c="${a}+${d}",a=1)
                p.disp()
            generates:
                WARNING: unable to interpret 1/3 expressions in "definitions"
                  -----------:----------------------------------------
                            a: 1
                            b: ${a}+1
                             = 2
                            c: ${a}+${d}
                             = < undef definition "${d}" >
                  -----------:----------------------------------------
            setting p.d
                p.d = 2
                p.disp()
            produces
                  -----------:----------------------------------------
                            a: 1
                            d: 2
                            b: ${a}+1
                             = 2
                            c: ${a}+${d}
                             = 3
                  -----------:----------------------------------------

    """

    def __add__(self,p):
        return super(param,self).__add__(p,sortdefinitions=True,raiseerror=False)

    def __iadd__(self,p):
        return super(param,self).__iadd__(p,sortdefinitions=True,raiseerror=False)

    def __repr__(self):
        self.sortdefinitions(raiseerror=False)
        #super(param,self).__repr__()
        super().__repr__()
        return str(self)

# %% DEBUG
# ===================================================
# main()
# ===================================================
# for debugging purposes (code called as a script)
# the code is called from here
# ===================================================
if __name__ == '__main__':
# =============================================================================
#     # very advanced
#     import os
#     from fitness.private.loadods import alias
#     local = "C:/Users/olivi/OneDrive/Data/Olivier/INRA/Etudiants & visiteurs/Steward Ouadi/python/test/output/"
#     odsfile = "fileid_conferences_FoodRisk.ods"
#     fullfodsfile = os.path.join(local,odsfile)
#     p = alias(fullfodsfile)
#     p.disp()
# =============================================================================
# new feature
    a = struct(a=1,b=2)
    a["b"]
# path example
    s0 = struct(a=pstr("/tmp/"),b=pstr("test////"),c=pstr("${a}/${b}"),d=pstr("${a}/${c}"),e=pstr("$c/$a"))
    s = struct.struct2param(s0,protection=True)
    s.disp()
    s.a/s.b
    str(pstr.topath(f"{s.a}/{s.b}"))
    s.eval()
    # escape example
    definitions = param(a=1,b="${a}*10+${a}",c="\${a}+10",d='\${myparam}')
    text = definitions.formateval("this my text ${a}, ${b}, \${myvar}=${c}+${d}")
    print(text)

    definitions = param(a=1,b="$a*10+$a",c="\$a+10",d='\$myparam')
    text = definitions.formateval("this my text $a, $b, \$myvar=$c+$d",protection=True)
    print(text)
    # assignment
    s = struct(a=1,b=2)
    s[1] = 3
    s.disp()
    # conversion
    s = {"a":1, "b":2}
    t=struct.dict2struct(s)
    t.disp()
    sback = t.struct2dict()
    sback.__repr__()
    # file definition
    p=struct.fromkeysvalues(["a","b","c","d"],[1,2,3]).struct2param()
    ptxt = p.protect("$c=$a+$b")
    definitions.write("../../tmp/test.txt")
    # populate/inherit fields
    default = struct(a=1,b="2",c=[1,2,3])
    tst = struct(a=10)
    tst.check(default)
    tst.disp()
    # multiple assigment
    a = struct(a=1,b=2,c=3,d=4)
    b = struct(a=10,b=20,c=30,d=40)
    a[:2] = b[1:3]
    a[:2] = b[(1,3)]
    # reorganize definitions to enable param.eval()
    s = param(
        a = 1,
        f = "${e}/3",
        e = "${a}*${c}",
        c = "${a}+${b}",
        b = 2,
        d = "${c}*2"
        )
    #s[0:2] = [1,2]
    s.isexpression
    struct.isstrdefined("${a}+${b}",s)
    s.isdefined()
    s.sortdefinitions()
    s.disp()
    p = param(b="${a}+1",c="${a}+${d}",a=1)
    p.disp()

# features 2025
    p=param()
    p.a = [0,1,2]
    p.b = '![1,2,"test","${a[1]}"]'
    p
