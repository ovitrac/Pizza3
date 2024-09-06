#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__project__ = "Pizza3"
__author__ = "Olivier Vitrac"
__copyright__ = "Copyright 2022"
__credits__ = ["Olivier Vitrac"]
__license__ = "GPLv3"
__maintainer__ = "Olivier Vitrac"
__email__ = "olivier.vitrac@agroparistech.fr"
__version__ = "0.97"

"""
Matlab-like Structure class
Matlab MS.alias like class (with MS = Molecular Studio, author INRAE\Olivier Vitrac)

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


# %% Dependencies
from math import * # import math to authorize all math expressions in parameters
import types       # to check types
import re          # regular expression
import numpy as np
from copy import copy as duplicate # to duplicate objects
from copy import deepcopy as duplicatedeep # used by __deepcopy__()
from pathlib import PurePosixPath as PurePath

# %% core struct class
class struct():
    """
    mini class behaving as a Matlab Stucture
    Use param() if you need evaluation as MS.alias()

    s=struct(a=1,b=2,c='${a}+${b} # evaluate me if you can')
    generates
      --------:----------------------------------------
             a: 1
             b: 2
             c: ${a}+${b} # evaluate me if you can
      --------:----------------------------------------
    Out: structure (struct object) with 3 fields


    s=param(a=1,b=2,c='${a}+${b} # evaluate me if you can')
    generates instead:
      --------:----------------------------------------
             a: 1
             b: 2
             c: ${a}+${b} # evaluate me if you can   (= 3 )
      --------:----------------------------------------
    Out: parameter list (param object) with 3 definitions


    Data can be appended or changed
        s.a = 10
        s.d = 11

    Data can be indexed
        for x in s: print(x)
        s[0]
        s[-1]

    To delete a field, use either
        delattr(s,'d') # Python's way
    or
        s.d = []       # à la Matlab

    To check whether a field exist, use either
        hasattr(s,'b') # Python' way
    or
        'b' in s       # other Python's way'


    Concatenate or remove structures
    Note: the definitions in the most right structure will overwrite existing values
        a=struct(a=1,b=2)
        b=struct(c=3,d="d",e="e")
        c=a+b
        d=a+struct(c=30)
        e=c-a
        f=b-struct(e="")
        b-=struct(e="")

    Practical shorthands

    > construct a structure from keys
        s = struct.fromkeys(["a","b","c","d"])
          --------:----------------------------------------
                 a: None
                 b: None
                 c: None
                 d: None
          --------:----------------------------------------
        Out: structure (struct object) with 4 fields

    > build a structure from variables in a string
        s = struct.scan("${a}+${b}*${c}/${d} --- ${ee}")
        s.a = 1
        s.b = "test"
        s.c = [1,"a",2]
        s.generator()
    leads to
        X = struct(
                 a= 1,
                 b= "test",
                 c= [1, 'a', 2],
                 d= None,
                ee= None
                 )

    > Structures can be concatenated and indexed as list
        a = struct(a=1,b=2)
        b = struct(c=3,d=4,e=5,f=6,g=7)
        c = a+b
        c[0]
        c[-1]
        for v in c: print(v,end=" ")
        d = struct(a=10,b=20,c=30,d=40,e=50,f=60,g=70)
        c[:2] = d[:2]
        c[[4,5,6]] = d[[4,5,6]]
        c.generator()
    leads to
        X = struct(
                 a= 10,
                 b= 20,
                 c= 3,
                 d= 4,
                 e= 50,
                 f= 60,
                 g= 70
                 )
    note: "f" in c returns True as it check the key, not the value

    > struct() offers low-level control to param() features
        s = struct(d=3,e="${c}+{d}",c = '${a}+${b}',a=1,b=2)
        s.sortdefinitions() will return
        --------:----------------------------------------
               d: 3
               a: 1
               b: 2
               c: ${a}+${b}
               e: ${c}+${d}
        --------:----------------------------------------
      Out[63]: structure (struct object) with 5 fields

      note: similar results can be obtained with param()
      p = param(sortdefinitions=True,d=3,e="${c}+${d}",c = '${a}+${b}',a=1,b=2)
      -----------:----------------------------------------
                d: 3
                a: 1
                b: 2
                c: ${a}+${b}
                 = 3
                e: ${c}+${d}
                 = 6
      -----------:----------------------------------------
    Out[80]: parameter list (param object) with 5 definitions

    note: variables shorthands $a, $b... can replace ${a}, ${b} in param()
    sortdefintions() do not recognize them (no protection)


    > Overview of implemented methods and arguments
      methods only available for param() objects are indicated with [*]

        check(default)
        clear()
        dict2struct(dico,makeparam=False)
        dispmax(content)
        disp()
        escape(s)   [*]
        eval(s="",protection=False)   [*]
        eval(value,ispstr=False)
        formateval(s,protection=False)   [*]
        format(s,escape=False)
        fromkeys(keys)
        fromkeysvalues(keys,values,makeparam=False)
        generator()
        getattr(key)
        hasattr(key)
        isdefined(ref=None)
        isempty()
        isexpression()
        isstrdefined(s,ref)
        isstrexpression(s)
        items()
        keys()
        keyssorted(reverse=True)
        protect(s="")   [*]
        read(file)
        scan(s)
        setattr(key,value)
        set(**kwargs)
        sortdefinitions()
        struct2dict()
        struct2param(protection=False,evaluation=True)
        topath()
        tostatic()  [*]
        tostruct(protection=False)  [*]
        values()
        write(file)
        zip()

    overloaded methods and operators: str(), list(), in, +, +=, /

        __add__(s,sortdefinitions=False)
        __add__(value)
        __contains__(item)
        __copy__()
        __deepcopy__( memo)
        __getattr__(key)
        __getitem__(idx)
        __getstate__()
        __iadd__(s,sortdefinitions=False)
        __iadd__(value)
        __init__(**kwargs)
        __init__(_protection=False,_evaluation=True,**kwargs)
        __isub__(s)
        __len__()
        __next__()
        __repr__()
        __setattr__(key,value)
        __setitem__(idx,value)
        __setstate__(state)
        __str__()
        __sub__(s)
        __truediv__(value)


    > dynamic properties
        isempty
        isdefinition



    """

    # attributes to be overdefined
    _type = "struct"        # object type
    _fulltype = "structure" # full name
    _ftype = "field"        # field name
    _evalfeature = False    # true if eval() is available
    _maxdisplay = 40        # maximum number of characters to display (should be even)

    # attributes for the iterator method
    # Please keep it static, duplicate the object before changing _iter_
    _iter_ = 0

    # excluded attributes (keep the , in the Tupple if it is singleton)
    _excludedattr = ('_iter_','__class__','_protection','_evaluation','_returnerror') # used by keys() and len()


    # Methods
    def __init__(self,**kwargs):
        """ constructor """
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
        """ get value """
        if key in self.keys():
            return self.__dict__[key]
        raise AttributeError(f'the {self._ftype} "{key}" does not exist')

    def hasattr(self,key):
        """ return true if the field exist """
        return key in self.keys()

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

    def __add__(self,s,sortdefinitions=False,raiseerror=True):
        """ add a structure
            set sortdefintions=True to sort definitions (to maintain executability)
        """
        if not isinstance(s,struct):
            raise TypeError(f"the second operand must be {self._type}")
        dup = duplicate(self)
        dup.__dict__.update(s.__dict__)
        if sortdefinitions: dup.sortdefinitions(raiseerror=raiseerror)
        return dup

    def __iadd__(self,s,sortdefinitions=False,raiseerror=False):
        """ iadd a structure
            set sortdefintions=True to sort definitions (to maintain executability)
        """
        if not isinstance(s,struct):
            raise TypeError(f"the second operand must be {self._type}")
        self.__dict__.update(s.__dict__)
        if sortdefinitions: self.sortdefinitions(raiseerror=raiseerror)
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

    def sortdefinitions(self,raiseerror=True):
        """ sortdefintions sorts all definitions
            so that they can be executed as param().
            If any inconsistency is found, an error message is generated.
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
                    if not errorfound:
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
    def write(self,file):
        """
            write the equivalent structure (not recursive for nested struct)
                write(filename)
        """
        f = open(file,mode="w",encoding='utf-8')
        print(f"# {self._fulltype} with {len(self)} {self._ftype}s\n",file=f)
        for k,v in self.items():
            if v is None:
                print(k,"=None",file=f,sep="")
            elif isinstance(v,(int,float)):
                print(k,"=",v,file=f,sep="")
            elif isinstance(v,str):
                print(k,'="',v,'"',file=f,sep="")
            else:
              print(k,"=",str(v),file=f,sep="")
        f.close()

    # write a file
    @staticmethod
    def read(file):
        """
            read the equivalent structure
                read(filename)
        """
        f = open(file,mode="r",encoding="utf-8")
        s = struct()
        while 1:
            line = f.readline()
            if not line: break
            line = line.strip()
            expr = line.split(sep="=")
            if len(line)>0 and line[0]!="#" and len(expr)>0:
                lhs = expr[0]
                rhs = "".join(expr[1:]).strip()
                if len(rhs)==0 or rhs=="None":
                    v = None
                else:
                    v = eval(rhs)
                s.setattr(lhs,v)
        f.close()
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


# %% param class with scripting and evaluation capabilities
class param(struct):
    """
    class parameters derived from struct() with dynamic evaluation
    container obj.param = value

    Example:
        s=param(a=1,b=2,c='${a}+${b} # evaluate me if you can',
                d="$this is a string",e="1000 # this is my number")

    returns
          --------:----------------------------------------
                 a: 1
                 b: 2
                 c: ${a}+${b} # evaluate me if you can
                  = 3
                 d: $this is a string
                  = this is a string
                 e: 1000 # this is my number
                  = 1000
          --------:----------------------------------------
        Out: parameter list (param object) with 5 definitions

        s.a=10

    produces
          --------:----------------------------------------
                 a: 10
                 b: 2
                 c: ${a}+${b} # evaluate me if you can
                  = 12
                 d: $this is a string
                  = this is a string
                 e: 1000 # this is my number
                  = 1000
          --------:----------------------------------------
      Out: parameter list (param object) with 5 definitions


     Other example with text parameters
      s = param()
      s.mypath = "$/this/folder"
      s.myfile = "$file"
      s.myext = "$ext"
      s.fullfile = "$${mypath}/${myfile}.${myext}"

    generates
          --------:----------------------------------------
            mypath: $/this/folder
                  = /this/folder
            myfile: $file
                  = file
             myext: $ext
                  = ext
          fullfile: $${mypath}/${myfile}.${myext}
                  = /this/folder/file.ext
          --------:----------------------------------------
    Out: parameter list (param object) with 4 definitions


    Evaluate a string with variables define in s
        s.eval("this a string with ${variable1}, ${variable2}")

    note: \${variable} prevents the evaluation
    note: use s.eval("...$variable",protection=True) to add automatically {}

    Examples:

        definitions = param(a=1,b="${a}*10+${a}",c="\${a}+10",d='\${myparam}')
        text = definitions.formateval("this my text ${a}, ${b}, \${myvar}=${c}+${d}")
        print(text)

        definitions = param(a=1,b="$a*10+$a",c="\$a+10",d='\$myparam')
        text = definitions.formateval("this my text $a, $b, \$myvar=$c+$d",protection=True)
        print(text)

        s = struct(a=1,b=2)
        s[1] = 3
        s.disp()

        s = {"a":1, "b":2}
        t=struct.dict2struct(s)
        t.disp()
        sback = t.struct2dict()
        sback.__repr__()

        p=struct.fromkeysvalues(["a","b","c","d"],[1,2,3]).struct2param()
        ptxt = p.protect("$c=$a+$b")

        # Example with interpretation and rearranging
        s = param(
            a = 1,
            f = "${e}/3",
            e = "${a}*${c}",
            c = "${a}+${b}",
            b = 2,
            d = "${c}*2"
            )
        s.isexpression
        struct.isstrdefined("${a}+${b}",s)
        s.isdefined()
        s.sortdefinitions()
        s.disp()


    Error handling (most common errors are captured)

        p = param(b="${a}+1",c="${a}+${d}",a=1)
        p.disp()

    returns the first error on each line
        -----------:----------------------------------------
                  b: ${a}+1
                   = < undef definition "${a}" >
                  c: ${a}+${d}
                   = < undef definition "${a}" >
                  a: 1
        -----------:----------------------------------------

    calling p.sortdefinitions() generates an error
        KeyError: 'unable to interpret 1/3 expressions in "definitions"'

    calling p.sortdefinitions(raiseerror=False) generates only a warning
        WARNING: unable to interpret 1/3 expressions in "definitions"
    and p.disp()
        -----------:----------------------------------------
                  a: 1
                  b: ${a}+1
                   = 2
                  c: ${a}+${d}
                   = < undef definition "${d}" >
        -----------:----------------------------------------

    note: paramauto() simplifies operations and inheritances
    on objects with patial definitions (some definitions are missing)

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
        raise TypeError('the argument must be string')


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
                # Literal string starts with $
                if not self._evaluation:
                    tmp.setattr(key, pstr.eval(tmp.format(valuesafe,escape),ispstr=ispstr))
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
        str class for paths and filenames
            a = pstr("this/is/mypath//")
            b = pstr("mylocalfolder/myfile.ext")
            c = a / b # this/is/mypath/mylocalfolder/myfile.ext

            note: keep trailing "/" if present

            Methods such as replace()... convert pstr back to str
            use pstr.eval("some/path/afterreplcament",ispstr=True) to keep the class pstr

            Operators + and += generate a pstr

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
        paramauto() inherits all param() features with sorteddefinitions = True
        for concatenation (+ or +=) and display

        These features are used when a param() object is augmented irrespectively
        is capacity of executing expressions.
        Note that it is mandatory to use ${variable} and not $variable
        (which is tolerated in param() with an internal protection)

        paramauto() is more computationally-intensive

        Usage:
            Contrarily to param(), defintions can be stacked irrespectively
            their execution order.

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
