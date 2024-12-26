## DSCRIPT-based LAMMPS Simulations for Pizza3

This directory contains simulations written in DSCRIPT, a Pythonic language for parameterized and modular input scripting in LAMMPS, as utilized in the Pizza3 framework.

### About DSCRIPT
DSCRIPT leverages Python objects to generate LAMMPS input files dynamically, enabling:
- Modularity: Reusable templates for similar simulations.
- Parameterization: Variables and expressions for flexible configurations.
- Advanced Logic: Dynamic definitions and templates evaluated at runtime.

### File Structure
- **Global Parameters:** Defines simulation-wide settings such as dimensions, material properties, and initial conditions.
- **Definitions:** Includes variables with optional dependency on other variables using `${}` syntax.
- **Templates:** Specifies the actual LAMMPS commands, organized into blocks for initialization, boundary conditions, physics, and output.
- **Attributes (Optional):** Metadata and evaluation rules for individual templates or commands.

### Usage
1. Each simulation is defined in a DSCRIPT template (Python `.py` file).
2. To generate a LAMMPS input script:
   - Run the Python script that defines the DSCRIPT object.
   - Call the `script().do()` method on the DSCRIPT object to print or save the LAMMPS input file.
3. Example workflow:
   ```bash
   python aluminum_strip_pull.py > in.aluminum_strip_pull
   lmp_mpi -in in.aluminum_strip_pull
   ```

### Conversion Rules
Simulations in this directory follow a strict format and conversion methodology:
1. **DSCRIPT SAVE FILE Format:** Each file starts with `# DSCRIPT SAVE FILE`, including:
   - Global Parameters: Key-value pairs for simulation-wide constants.
   - Definitions: Variables used across the simulation.
   - Template: LAMMPS commands in parameterized blocks.
2. Variables use `${}` for dynamic substitution.
3. Templates may include both single-line and multi-line blocks.

Example DSCRIPT Syntax:
```python
from pizza.dscript import dscript

template = """# DSCRIPT SAVE FILE
{
    SECTIONS = ['INITIALIZE', 'CREATE_GEOMETRY', 'DISCRETIZATION'],
    section = 0,
    description = "Example Simulation"
}

# GLOBAL PARAMETERS
E=69.0 # Young's modulus
rho=2.7 # Density

initialize: [
    units si
    dimension 3
]

create_geometry: [
    lattice sq 1.0
    region box block 0 10 0 10 0 10 units box
    create_box 1 box
    create_atoms 1 box
]

run: run 10000
"""
example_simulation = dscript.parsesyntax(template)
print(example_simulation.script().do())
```

### Notes
- Generated LAMMPS input scripts are stored in the `output/` subdirectory.
- Simulation results can be analyzed using post-processing tools available in Pizza3.
- For further guidance, refer to the [Pizza3 Documentation](../docs/README.md).






---


# 📝 **DSCRIPT SAVE FILE Format Instructions**

📋 Use the following instructions to teach ChatGPT how to convert scripts into LAMMPS code using `pizza.dscript()`.

---

### 🚀 **Step-by-Step Guide**

Each DSCRIPT file begins with the line:

```plaintext
# DSCRIPT SAVE FILE
```

The file is divided into the following **sections**:

---

### 1️⃣ **Global Parameters Section**
📂 Enclosed in `{}` and contains key-value pairs where values can be:
- Integers
- Floats
- Strings
- Booleans
- Lists

📖 **Example**:
```python
# GLOBAL PARAMETERS
{
    SECTIONS = ['SECTION1', 'SECTION2'],
    section = 0,
    position = 0,
    role = "dscript instance",
    description = "A description",
    userid = "dscript",
    version = 0.1,
    verbose = False
}
```

---

### 2️⃣ **Definitions Section**
🔧 Defines variables as key-value pairs. Variables can reference other variables using `${}`.

📖 **Example**:
```plaintext
# DEFINITIONS (number of definitions=X)
var1 = value1
var2 = "${var1}"
```

---

### 3️⃣ **Template Section**
🖋️ Contains key-value pairs for blocks of script content:
- **Single-line content**: `key: value`
- **Multi-line content**: Enclosed in square brackets `[]`.

📖 **Example**:
```plaintext
# TEMPLATE (number of lines=X)
block1: command using ${var1}
block2: [
    multi-line command 1
    multi-line command 2
]
```

---

### 4️⃣ **Attributes Section**
✨ Optional attributes are attached to each block as key-value pairs inside `{}`.

📖 **Example**:
```plaintext
# ATTRIBUTES (number of lines with explicit attributes=X)
block1: {facultative=True, eval=True}
```

---

### 🔗 **Dynamic Substitution**
- Variables can be dynamically substituted into templates using `${}`.
- Both **single-line** and **multi-line** templates are supported.

---

⚡ **Copy and paste these instructions into ChatGPT to teach it how to process DSCRIPT files!**
```