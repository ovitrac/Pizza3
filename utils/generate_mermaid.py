#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Automatic Python module class and method documentation generation with Mermaid diagrams
#
# Inputs:
#  - Takes a list of modules from STDIN (one per line, in dot notation)
#  - First argument: output Markdown file
#
# Outputs:
#  - A single Markdown file containing:
#    1) A tabulated list of methods for each module (method name, first paragraph of docstring, number of lines, __version__)
#    2) A Mermaid graph diagram for the class inheritance of that module
#    3) Date of generation

# INRAE\Olivier Vitrac
# Email: olivier.vitrac@agroparistech.fr
# Last Revised:** 2024-12-11


import sys
import os
import importlib
import inspect
from datetime import datetime

# Configuration Preambule
ConfigurationPreambule = """
## Configuration

To run Pizza3, ensure your Python environment is properly configured. This setup assumes that you are operating from the `Pizza3/` directory, which contains the `pizza/` and `doc/` folders. The main folder (`$mainfolder`) is set to the absolute path of the current directory.

### Setting Up PYTHONPATH

Add the following paths to your `PYTHONPATH` environment variable to allow Python to locate the Pizza3 library and its dependencies:

```bash
# Define mainfolder as the absolute path
mainfolder=$(realpath .)

# Dynamically retrieve Python paths
python_lib=$(python -c "import sysconfig; print(sysconfig.get_path('stdlib'))")
lib_dynload=$(python -c "import sysconfig; print(sysconfig.get_path('platlib'))")
site_packages=$(python -c "import site; print(site.getsitepackages()[0])")

# Paths to include in PYTHONPATH
additional_paths=(
    "$mainfolder"
    "$mainfolder/pizza"
    "$python_lib"
    "$lib_dynload"
    "$site_packages"
)

# Set PYTHONPATH dynamically
export PYTHONPATH=$(IFS=:; echo "${additional_paths[*]}")
echo "PYTHONPATH set to: $PYTHONPATH"

# Test Python Interpreter Configuration:
# You should read "Pizza library initialized successfully"
python -c "import pizza"
```

>**Note:**
>
>- The `.ipython/` directory has been excluded as it is not required for Pizza3.
>- If you're using a virtual environment, ensure it's activated before running the script to automatically include the virtual environment's `site-packages` in `PYTHONPATH`.
>- Replace `PYTHON_VERSION` with your actual Python version if different from `3.10`.
>- If you're not using `Conda`, adjust the environment creation and activation commands accordingly.

After setting up the `PYTHONPATH`, you can proceed to explore the Pizza3 modules below.

### Launch `example2.py`
You can now generate your first LAMMPS code from Python and run it with [LAMMPS-GUI](https://github.com/lammps/lammps/releases).
```bash 
    mkdir -p ./tmp     # create the output folder tmp/ if it does not exist
    python example2.py # run example2
```
"""

def class_name(cls):
    """Return a string representing the class"""
    return cls.__name__

def classes_tree(module, base_module=None):
    """Extract classes and their inheritances starting from a base module."""
    if base_module is None:
        base_module = module.__name__
    module_classes = set()
    inheritances = []
    def inspect_class(cls):
        if class_name(cls) not in module_classes:
            if cls.__module__.startswith(base_module):
                module_classes.add(class_name(cls))
                for base in cls.__bases__:
                    inheritances.append((class_name(base), class_name(cls)))
                    inspect_class(base)
    for cls in [e for e in module.__dict__.values() if inspect.isclass(e)]:
        inspect_class(cls)
    return module_classes, inheritances

def classes_tree_to_mermaid(module_classes, inheritances):
    lines = ["graph TD;"]
    for c in sorted(module_classes):
        lines.append(f"{c}")
    for (a, b) in sorted(inheritances):
        lines.append(f"{a} --> {b}")
    return "\n".join(lines)

def get_first_paragraph(docstring):
    if not docstring:
        return ""
    lines = docstring.strip().split('\n')
    # First paragraph is up to a blank line or the end of lines
    paragraph = []
    for line in lines:
        if line.strip() == "":
            break
        paragraph.append(line.strip())
    return " ".join(paragraph)

def get_method_info(obj):
    """Return a dict with method name, docstring first paragraph, number of lines, and __version__."""
    info = {}
    if not (inspect.isfunction(obj) or inspect.ismethod(obj)):
        return info

    name = obj.__name__
    doc = inspect.getdoc(obj)
    first_par = get_first_paragraph(doc)
    try:
        lines, _ = inspect.getsourcelines(obj)
        nlines = len(lines)
    except (OSError, TypeError):
        nlines = 0

    # Attempt to find __version__ attribute:
    # Methods typically won't have their own __version__, but we can check their __globals__ if function
    __version__ = None
    if inspect.isfunction(obj):
        __version__ = obj.__globals__.get('__version__', None)
    # If not found there, we can try attributes
    if hasattr(obj, '__version__'):
        __version__ = getattr(obj, '__version__', __version__)

    info['name'] = name
    info['doc'] = first_par
    info['nlines'] = nlines
    info['__version__'] = __version__ if __version__ is not None else ""
    return info

def get_module_methods(module):
    """Get methods and functions defined at the top-level and within classes of the module."""
    # Top-level functions
    top_methods = []
    for name, obj in inspect.getmembers(module, inspect.isfunction):
        if obj.__module__ == module.__name__:
            top_methods.append(get_method_info(obj))

    # Class methods
    class_methods = []
    for name, cls in inspect.getmembers(module, inspect.isclass):
        if cls.__module__ == module.__name__:
            for mname, mobj in inspect.getmembers(cls, inspect.isfunction):
                # To filter out inherited methods from outside modules if desired:
                if mobj.__module__ == module.__name__:
                    method_info = get_method_info(mobj)
                    method_info['class'] = cls.__name__
                    class_methods.append(method_info)

    return top_methods, class_methods

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: generate_mermaid.py output_markdown.md < modules_list.txt")
        sys.exit(1)

    output_markdown = sys.argv[1]
    modules = [line.strip() for line in sys.stdin if line.strip()]

    with open(output_markdown, "w", encoding="utf-8") as f:
        f.write(f"# Pizza Modules Documentation\n\n")
        f.write(f"Generated on: **{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**\n\n")
        f.write('<hr style="border: none; height: 1px; background-color: #e0e0e0;" />\n\n')
        f.write(ConfigurationPreambule + "\n\n")
        f.write('<hr style="border: none; height: 1px; background-color: #e0e0e0;" />\n\n')
        for mod_name in sorted(modules):
            # Attempt to import module
            try:
                mod = importlib.import_module(mod_name)
            except Exception as e:
                f.write(f"## Module `{mod_name}`\n\n")
                f.write(f"**Error importing module**: {e}\n\n")
                continue

            f.write(f"## Module `{mod_name}`\n\n")

            # Get class tree
            module_classes, inheritances = classes_tree(mod, base_module='pizza')
            # Mermaid diagram
            if module_classes:
                f.write("### Class Inheritance Diagram\n")
                f.write("```mermaid\n")
                f.write(classes_tree_to_mermaid(module_classes, inheritances))
                f.write("\n```\n\n")
            else:
                f.write("*No classes found in this module.*\n\n")

            # Get methods
            top_methods, class_methods = get_module_methods(mod)

            if top_methods or class_methods:
                f.write("### Methods Table\n\n")
                f.write("| Class | Method | Docstring First Paragraph | # Lines | __version__ |\n")
                f.write("|-------|---------|---------------------------|---------|-------------|\n")
                # Top-level methods
                for m in top_methods:
                    f.write(f"| (module-level) | {m['name']} | {m['doc']} | {m['nlines']} | {m['__version__']} |\n")
                # Class methods
                for m in class_methods:
                    f.write(f"| {m.get('class','')} | {m['name']} | {m['doc']} | {m['nlines']} | {m['__version__']} |\n")
                f.write("\n")
            else:
                f.write("*No methods found in this module.*\n\n")
