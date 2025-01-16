# Converted Modules for Pizza3

This directory contains modules that have been directly converted from their Python 2.x equivalents to Python 3.x. These modules are utilized by the Pizza3 library to handle various data operations but have not yet been optimized specifically for Pizza3 (optimization is pending).

## Files

- **`bdump3.py`**: Python 3.x version of the `bdump` module for handling binary dump files.
- **`cdata3.py`**: Python 3.x version of the `cdata` module for managing ChemCell data.
- **`ldump3.py`**: Python 3.x version of the `ldump` module for handling lattice dump files.
- **`mdump3.py`**: Python 3.x version of the `mdump` module for handling molecular dump files.
- **`tdump3.py`**: Python 3.x version of the `tdump` module for handling text dump files.

## Notes

- **Integration**:
  - These modules are imported by `pizza.dump3` and `pizza.data3`.
  - They are directly converted from their Python 2.x equivalents sourced from the [Pizza GitHub Repository](https://github.com/lammps/pizza/tree/master/src) without optimization for Pizza3 (pending).

- **Usage**:
  - Ensure that you integrate these modules into the Pizza3 library under the `pizza/converted/` directory.
  - After integration, thoroughly test each functionality (loading data, creating geometry, triangulating, etc.) to confirm that the modules operate as expected within the Pizza3 environment.

- **Future Work**:
  - Optimization for Pizza3 is pending. Future updates may include performance enhancements and additional features tailored to Pizza3’s architecture.

## Directory Structure

```
pizza/
├── data3.py                   <---------- Pizza3 optimized files
├── dump3.py                   <---------- Pizza3 optimized files
├── data3_legacy.py            <---------- Pizza3 original files
├── dump3_legacy.py            <---------- Pizza3 original files
├── converted/
│   ├── bdump3.py
│   ├── cdata3.py
│   ├── ldump3.py
│   ├── mdump3.py
│   └── tdump3.py
└── private/
    ├── __init__.py
    ├── utils.py
    ├── mstruct.py
    └── PIL/
        ├── __init__.py
        └── ...
```

## Additional Information

- **Compatibility**:
  - These converted modules maintain the same interfaces as their Python 2.x counterparts, ensuring compatibility with existing Pizza3 functionalities that rely on them.
  
- **Modification**:
  - Avoid modifying these files unless you are extending or debugging Pizza3 internals. Any changes should be carefully tested to prevent disruptions in the library’s operations.

- **Support**:
  - For issues or contributions related to these converted modules, please refer to the Pizza3 repository’s contribution guidelines or contact the maintainers.

