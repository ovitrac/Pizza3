## Overview

This directory (`utils/__all__`) contains backup files for dynamically generated `__all__` variables from Python modules in the **Pizza** package. The files are generated using a script that ensures each module has an accurate and consistent `__all__` variable reflecting only public symbols defined within the module itself. This improves module encapsulation, export control, and code maintainability.

---

## Script Description

The script **`generate_all.py`** performs the following key tasks:

1. **Extract Public Symbols**:
   - Scans a module to extract all public symbols (classes, functions, variables) defined within the module itself.
   - Symbols are excluded if they:
     - Begin with an underscore (`_`).
     - Are not defined in the current module (i.e., imported symbols are ignored).

2. **Backup Generated `__all__` Variables**:
   - Saves the generated `__all__` definitions in this directory (`utils/__all__`) for review and potential manual adjustments.

3. **Update Module Files**:
   - Automatically adds or updates the `__all__` variable in the target module's source file.

4. **Modularity**:
   - Processes all specified modules in the **Pizza** package while skipping sub-packages.

---

## Usage Instructions

1. **Ensure Correct Directory**:
   - Run the script from the `utils/` directory using the command:
     ```
     ./generate_all.py
     ```
   - The script validates that it is being executed from the correct directory.

2. **Paths**:
   - The base path for the **Pizza** package is inferred automatically relative to the `utils/` directory.
   - The `__all__` backup files are saved in this directory (`utils/__all__`).

3. **Modules Processed**:
   - By default, the script processes the following packages:
     - `pizza`
     - `pizza.private`

4. **Outputs**:
   - **Backup Files**: Saved as `<module_name>_all.py` in this directory.
   - **Updated Modules**: The `__all__` variable in each module is added or updated directly in the source file.

---

## File Format for Backups

Each backup file in this directory follows this format:

```python
# __all__ for <module_name>
__all__ = [
    "public_function_1",
    "PublicClass",
    "CONSTANT_VALUE",
]
```

---

## Troubleshooting

- **Module Import Errors**:
  - Ensure the **Pizza** package is structured correctly and all dependencies are installed.

- **File Permission Issues**:
  - Ensure you have write permissions for the module files and the `utils/__all__` directory.

- **Symbol Missing in `__all__`**:
  - Verify the symbol is defined in the target module and does not begin with `_`.

---

## Maintainer

- **Author**: INRAE\\Olivier Vitrac
- **Email**: olivier.vitrac@agroparistech.fr

---

## Revision History

- **2024-12-08**: Initial release.
- **2025-01-07**: Fixed `extract_symbols` by adding `package_root` parameter.

---


