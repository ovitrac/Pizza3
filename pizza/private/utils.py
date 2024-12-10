# -*- coding: utf-8 -*-
"""

    Utilities to update modules
        updatepptx()


Created on Wed Mar 30 20:59:25 2022

@author: olivi
"""

# %% Dependencies
import os, fnmatch
from pathlib import Path

__all__ = ['list', 'replaceall', 'updatepptx']

# %% replacement in several files
def replaceall(directory=".",
                find="string to find",
                replace="newstring",
                filePattern="*.py"):
    """
        replaceall("some_dir", "find this", "replace with this", "*.txt")
    """
    nprocessedfiles = nrevisedfiles = 0
    for path, dirs, files in os.walk(os.path.abspath(directory),topdown=True,onerror=None):
        for filename in fnmatch.filter(files, filePattern):
            nprocessedfiles += 1
            print(f'[{nprocessedfiles}]: "{filename}" in "{path}"')
            try:
                filepath = os.path.join(path, filename)
                with open(filepath) as f:
                    s0 = f.read()
            except IOError:
                raise IOError('the file cannot be open for reading')
            s = s0.replace(find, replace)
            if s==s0:
                print("\t no modification done")
            else:
                try:
                    with open(filepath, "w") as f:
                        f.write(s)
                except IOError:
                    raise IOError('the file cannot be open for writting')
                print("\t the file has ben revised")
                nrevisedfiles += 1
    if nprocessedfiles==0:
        print(f'\nno file matched "{filePattern}" in "{directory}"')
    else:
        print(f'\n{nprocessedfiles} files matched "{filePattern}" in "{directory}"')
        print(f'\t==> {nrevisedfiles} files have been modified')

def list(directory="."):
    """ list folders and files  """
    for root, dirs, files in os.walk(directory, topdown=False):
       for name in files:
          print(os.path.join(root, name))
       for name in dirs:
          print(os.path.join(root, name))


# update PPTX library
def updatepptx():
    """ update PPTX """

    rootmodule = "fitness"
    prefix = f"{rootmodule}.private"
    module = "pptx"
    fullmodule = f"{prefix}.{module}"

    directory = Path(os.path.join(os.path.abspath(rootmodule), "pptx")).as_posix()
    directory = "./pptx"
    find = f"from {module}"
    replace = f"from {fullmodule}"
    filepattern = "*.py"
    replaceall(directory,find,replace,filepattern)

    find = f"import {module}"
    replace = f"import {fullmodule}"
    replaceall(directory,find,replace,filepattern)

    find = f'["{module}.exceptions"]'
    replace = f'["{fullmodule}.exceptions"]'
    replaceall(directory,find,replace,filepattern)


# %% DEBUG
# ===================================================
# main()
# ===================================================
# for debugging purposes (code called as a script)
# the code is called from here
# ===================================================
if __name__ == '__main__':
    updatepptx()
