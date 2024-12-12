# Private Modules for Pizza3

This directory contains internal modules that are used internally by the Pizza3 library. These modules provide additional utilities and extended functionalities but are not intended for direct interaction by the user.

## Files and Subdirectories
- `__init__.py`: Initializes the `private` package.
- `utils.py`: General utilities for internal operations.
- `mstruct.py`: Tools for handling structured data.
- `PIL/`: A lightweight version of the Python Imaging Library (PIL) customized for Pizza3.

## Notes
- Modules in this folder are accessed indirectly through public-facing modules in `pizza/`.
- Avoid modifying files here unless you're extending or debugging Pizza3 internals.
