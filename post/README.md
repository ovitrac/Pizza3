# Post-Processing Tools for Pizza3

The `post/` directory contains tools, examples, and resources for post-processing results from LAMMPS simulations. This includes a dedicated MATLAB toolbox for handling SPH (Smoothed Particle Hydrodynamics) simulations, visualization utilities, pre-configured templates, and detailed documentation.

## **Directory Structure**

### **Root Files**
- **MATLAB Scripts**: Various `.m` files for SPH simulation analysis and related tasks.
  - Example scripts include `interp2SPH.m`, `forceHertz.m`, and `buildVerletList.m`.
- **Templates**: Pre-configured MATLAB scripts for specific tasks, such as:
  - `Billy_results_template.m` for specific simulation analysis.
- **Examples**: Ready-to-run examples such as `example1.m` and `example2.m` to help users get started with post-processing.

### **Key Subdirectories**
- **`docs/`**
  - Documentation files in Markdown, HTML, and PDF formats.
  - Includes descriptions of functions, SPH theory, and examples.
  - Contains assets (images, diagrams) used in documentation.
- **`dumps/`**
  - Stores simulation output data, organized by use case.
  - Includes sample datasets such as `TIMESTEP_*.mat` for test runs.
- **`figs/`**
  - Stores MATLAB `.fig` files and PNG exports for visualizations.
  - Organized by example and test cases.
- **`html/`**
  - Pre-rendered HTML documentation for MATLAB scripts and examples.
  - Includes workshop guides and visual explanations.
- **`notebook/`**
  - MATLAB Live Script (`.mlx`) files for interactive tutorials and post-processing examples.
  - Contains historical versions of key notebooks.
- **`draft/`**
  - Drafts for workshops and further development, e.g., `"Workshop on Suspended Particles in a Fluid"`.

## **Key Features**
### **MATLAB Toolbox**
- Dedicated tools for SPH simulation:
  - Verlet list construction (`buildVerletList.m`).
  - Force analysis (`forceHertz.m`, `forceLandshoff.m`).
  - Particle packing (`packSPH.m`).
  - Boundary condition handling (`unwrapPBC.m`, `trajunwrap.m`).

### **Documentation**
- Comprehensive function documentation available in `docs/`:
  - Markdown (`.md`), HTML (`.html`), and PDF (`.pdf`) formats.
  - Example: `forceLandshoff Function Documentation.html`.

### **Workshops**
- Detailed tutorials and workshops on SPH post-processing available in `html/` and `docs/`.

### **Examples**
- Ready-to-run MATLAB examples such as `example1.m`, `example2.m`, and their corresponding live scripts in `notebook/`.

## **Getting Started**
1. **Run MATLAB Examples**:
   - Open any example script in MATLAB, e.g., `example1.m`.
   - Follow the comments in the script to understand the workflow.

2. **Explore Documentation**:
   - Open HTML files in `docs/` or `html/` for guidance on specific functions or workflows.

3. **Use the Toolbox**:
   - Add the `post/` directory to your MATLAB path.
   - Call functions such as `interp2SPH` or `forceHertz` in your scripts.

4. **Analyze Simulation Data**:
   - Use the scripts in `dumps/` as references for processing LAMMPS output files.

## **Dependencies**
- MATLAB (R2021b or later recommended).
- Required MATLAB toolboxes:
  - Curve Fitting Toolbox (for interpolation scripts).
  - Optimization Toolbox (optional for advanced post-processing).

## **Contributing**
- Contributions are welcome! If you add new scripts or documentation:
  - Place new MATLAB scripts in the root directory.
  - Add documentation in `docs/`.
  - Update examples in `examples/`.

## **Notes**
- Ensure adequate disk space when working with large datasets in `dumps/`.
- Documentation files in `docs/` can be converted into HTML/PDF using tools like `pandoc`.

## **Contact**
For support or questions, contact **Olivier Vitrac** at INRAE:
- Email: [olivier.vitrac@agroparistech.fr](mailto:olivier.vitrac@agroparistech.fr)
