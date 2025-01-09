#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
### Follow-up Example: Introducing Physics via Forcefields (Example2bis)

This script builds upon Example2 by introducing **physics** into the simulation through the use of forcefields. It demonstrates the integration of forcefields into the simulation workflow, their customization for different regions, and their incorporation into the overall LAMMPS script.

---

### **Objective**

The goal of this example is to extend the functionality of Example2 by adding:
1. **Forcefield Definitions:** Introduce physical properties for simulation particles.
2. **Customization:** Derive region-specific forcefields with modified physical parameters.
3. **Integration:** Incorporate forcefields into the LAMMPS script dynamically.
4. **Analysis and Debugging:** Explore variables and generate detailed reports.

---

### **Key Features**

- **Forcefield Initialization:** Create and customize forcefields programmatically or using DSCRIPT syntax.
- **Dynamic Region-Specific Adjustments:** Modify forcefield parameters for different subregions.
- **Script Integration:** Combine forcefields with previous simulation steps.
- **Debugging:** Analyze variable occurrences and validate workflow consistency.

Last revision 2025-01-07
Author: INRAE\olivier.vitrac@agroparistech.fr
"""

# Import necessary modules
from pizza.forcefield import parameterforcefield, tlsph
from pizza.generic import generic
from pizza.dforcefield import dforcefield
from pizza.dscript import dscript

# %% LOAD PREVIOUS SCRIPT
"""
Load the DSCRIPT file from example2.py to reuse its definitions, such as regions and bead types.
"""
dscriptfilename = "tmp/example2.d.txt"
previoussteps = dscript.load(dscriptfilename)

# Extract bead type mappings and region arguments from the previous script
beadtype = previoussteps.search("ID", previoussteps.list_values("ID"), "beadtype")

# Additional control (for debugging purposes)
region_args = previoussteps.list_values('args', details=True).get_raw_data()

# %% DEFINE BASE FORCEFIELD
"""
Create a default forcefield using `parameterforcefield` and `dforcefield`.
This serves as the base forcefield for all regions.
"""
FFbase_parameters = parameterforcefield(
    base_class=tlsph,         # Forcefield class: Total Lagrangian Smoothed Particle Hydrodynamics
    rho=1050,                 # Density
    c0=10.0,                  # Speed of sound
    E="50*${c0}^2*${rho}",    # Elastic modulus
    nu=0.3,                   # Poisson's ratio
    q1=1.0, q2=0.0,           # Artificial viscosity parameters
    Hg=10.0, Cp=1.0,          # Heat capacity and specific energy
    sigma_yield="0.1*${E}",   # Yield stress
    hardening=0,              # Hardening coefficient
    contact_scale=1.5,        # Contact scale
    contact_stiffness="2.5*${c0}^2*${rho}"  # Contact stiffness
)
FFbase = dforcefield(userid="FFbase", **FFbase_parameters)

# Save the base forcefield for future reuse
FFbase.save("FFbase.default.txt", foldername="./tmp", overwrite=True, verbose=False)

# Reload the base forcefield to demonstrate file management
FFbase = dforcefield.load("FFbase.default.txt", foldername="./tmp")

# %% DEFINE REGION-SPECIFIC FORCEFIELDS
"""
Create specialized forcefields for each region by copying the base forcefield
and modifying region-specific properties.
"""
FFlower = FFbase.copy(
    beadtype=beadtype["LowerCylinder"],  # Assign bead type
    userid="LowerCylinder",             # Unique identifier
    E="2*"+FFbase.parameters.E,         # Increase elastic modulus
    rho=1050                            # Same density as base
)

FFcentral = FFbase.copy(
    beadtype=beadtype["CentralCylinder"],
    userid="CentralCylinder",
    E="0.5*"+FFbase.parameters.E,
    rho=1000                            # Reduced density
)

FFupper = FFbase.copy(
    beadtype=beadtype["UpperCylinder"],
    userid="UpperCylinder",
    E="10*"+FFbase.parameters.E,        # Much stiffer material
    rho=1300, nu=0.1                    # Higher density, lower Poisson's ratio
)

# %% ASSIGN FORCEFIELDS TO GROUPS
"""
Assign the specialized forcefields to atom groups and prepare them for the LAMMPS script.
"""
blower = FFlower.scriptobject(name="lowerAtoms", group="lowerAtoms")
bcentral = FFcentral.scriptobject(name="centralAtoms", group="centralAtoms")
bupper = FFupper.scriptobject(name="upperAtoms", group="upperAtoms")

# Combine all forcefield group scripts into a single collection
bcollection = blower + bcentral + bupper

# %% UPDATE SCRIPT WITH FORCEFIELDS
"""
Integrate the new forcefields into the previous script using `pipescript`.
The forcefields are added before the final steps of the previous script.
"""
updatedScript = previoussteps[:-1] | bcollection | previoussteps[-1:]

# Write the updated LAMMPS script to a file
updatedScriptfile = updatedScript.write("tmp/example2bis.txt", verbosity=1, overwrite=True)
print(f"The updated LAMMPS script (example2bis) is available here:\n{updatedScriptfile}")

# %% ANALYZE VARIABLES IN THE UPDATED SCRIPT
"""
Extract and analyze occurrences of variables like 'args' and 'move' from the updated script.
"""
args_values = updatedScript.list_values("args").get_raw_data()
move_count = updatedScript.list_values("move").get_usage_count("")

# %% CONVERT TO DSCRIPT AND SAVE
"""
Convert the updated script to DSCRIPT format for future reuse and reverse engineering.
"""
DupdatedScript = updatedScript.dscript(verbose=True)
DupdatedScriptFile = DupdatedScript.save("tmp/example2bis.d.txt", overwrite=True)
print(f"The updated DSCRIPT (example2bis) is available here:\n{DupdatedScriptFile}")

# %% VERIFY REVERSIBILITY
"""
Reload the updated DSCRIPT file and regenerate the LAMMPS script to ensure consistency.
"""
Drev2bis = dscript.load(DupdatedScriptFile)
Srev2bis = Drev2bis.pipescript(verbose=False)

# Variable control (for eventual debugging)
allvars = Srev2bis.list_values()
allvars["args"].export("tmp/example2bis.rev.args.html")
repr(allvars["args"])
Srev2bis.generate_report("tmp/example2bis.rev.var.html")

# Save the reversed script for control
revUpdatedScriptfile = Srev2bis.write("tmp/example2bis.rev.txt", verbosity=0, overwrite=True)
print(f"The updated and reversed LAMMPS script is available here:\n{revUpdatedScriptfile}")
