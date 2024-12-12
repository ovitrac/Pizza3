# Pizza3 Core Library

This directory contains the core Python modules for the Pizza3 LAMMPS toolkit. These modules provide foundational functionalities for building, running, and analyzing simulations with LAMMPS.

## Files and Subdirectories (overview, not exhausitve)
- `__init__.py`: Initializes the Pizza3 Python package.
- `script.py`: Handles LAMMPS script creation and management.
- `forcefield.py`: Provides tools to manage forcefields in simulations.
- `dforcefield.py`: Extends `forcefield.py` with dynamic features.
- `region.py`: Defines regions for LAMMPS simulations.
- `raster.py`: Tools for grid-based operations.
- `generic.py`: General utility functions.
- `private/`: Contains internal modules not intended for direct usage by end-users.

## Notes
- Ensure that the `PYTHONPATH` includes this directory when running Pizza3 scripts.
