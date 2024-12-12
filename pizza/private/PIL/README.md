# Custom Python Imaging Library (PIL) for Pizza3

This directory contains a lightweight, customized version of the Python Imaging Library (PIL). It is used for specialized image processing tasks required by Pizza3.

## Files and Subdirectories
- `__init__.py`: Initializes the `PIL` package.
- `Image.py`: Core image processing functions.

## Notes
- This version of PIL is self-contained and configured to avoid dependency issues with external PIL or Pillow libraries.
- Only used internally by Pizza3 for specific tasks (`pizza.raster()`).
