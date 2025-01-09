#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generates setup.py for SETUP

The following project structure is assumed.

Pizza3/
│
├── utils/
│   ├── generate_requirements.py  # SETUP script
│   ├── generate_manifest_in.py   # SETUP script
│   └── generate_setup.py         # SETUP script
│
├── pizza/
│   ├── __init__.py
│   ├── private/
│   │   ├── __init__.py
│   │   └── PIL/
│   │       ├── __init__.py
│   │       └── ... (other PIL modules)
│   └── ... (other modules)
│
├── example2.py
├── tmp/
├── README.md
├── LICENSE
├── Pizza3.simple.manifest
├── requirements.txt             # run ./generate_requirements.py   from utils/
├── MANIFEST.in                  # run ./generate_manifest_in.py  from utils/
└── setup.py                     # run ./generate_setup.py   from utils/


Update dependencies to needs and future evolutions:
    dependencies = [
        "numpy>=1.21.0"
    ]

Author:
    INRAE\\Olivier Vitrac
    Email: olivier.vitrac@agroparistech.fr
    Last Revised: 2025-01-09

    """

import os
import sys
import re
from pathlib import Path

def is_utils_directory(current_path):
    """
    Verify that the script is run from the 'utils/' directory.
    """
    return current_path.name == 'utils'

def get_version(parent_dir):
    """Extract the version number of Pizza3 from version_file."""
    mainfolder = Path(parent_dir).resolve()             # Resolve the main folder based on the provided current path
    version_file = mainfolder / "utils" / "VERSION.txt" # Construct the path to VERSION.txt
    if not os.path.isfile(version_file):
        sys.stderr.write(f"Error: {version_file} not found. Please create a file with content: version=\"XX.YY.ZZ\"\n")
        sys.exit(1)
    with open(version_file, "r") as f:
        for line in f:
            line = line.strip()
            match = re.match(r'^version\s*=\s*"(.*?)"$', line)
            if match:
                return match.group(1)
    sys.stderr.write(f"Error: No valid version string found in {version_file}. Ensure it contains: version=\"XX.YY.ZZ\"\n")
    sys.exit(1)

def check_project_structure(parent_dir):
    """
    Check if the parent directory contains essential project files.
    Modify the expected_files list based on your project's actual structure.
    """
    expected_files = ['README.md', 'setup.py']  # 'setup.py' will be created
    # Since 'setup.py' is to be created, we remove it from expected_files
    expected_files = [file for file in expected_files if not (parent_dir / file).exists()]
    for file in expected_files:
        if not (parent_dir / file).exists():
            return False
    return True

def prompt_overwrite(file_path):
    """
    Prompt the user to overwrite an existing setup.py file.
    """
    while True:
        choice = input(f"'{file_path}' already exists. Overwrite? [Y/n]: ").strip().lower()
        if choice in ['', 'y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        else:
            print("Please enter 'Y' or 'N'.")

def generate_setup_py(parent_dir, output_file, dependencies):
    """
    Generate setup.py with the specified dependencies.
    """
    setup_path = parent_dir / output_file

    if setup_path.exists():
        if not prompt_overwrite(setup_path):
            print("Operation cancelled. Existing 'setup.py' was not modified.")
            sys.exit(0)

    setup_content = f"""from setuptools import setup, find_packages

setup(
    name="Pizza3",
    version="{get_version(parent_dir)}",
    description="A LAMMPS toolkit",
    author="Olivier Vitrac",
    author_email="olivier.vitrac@agroparistech.fr",
    url="https://github.com/ovitrac/Pizza3",
    packages=find_packages(include=['pizza', 'pizza.*']),
    install_requires=[
        {', '.join([f'"{dep}"' for dep in dependencies])}
    ],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    include_package_data=True,
    zip_safe=True,
)
"""

    try:
        with open(setup_path, 'w') as f:
            f.write(setup_content)
        print(f"'{output_file}' has been created successfully in '{parent_dir}'.")
    except Exception as e:
        print(f"An error occurred while writing '{output_file}': {e}")
        sys.exit(1)

def main():
    # Get the current working directory
    current_dir = Path.cwd()

    # Ensure the script is run from the 'utils/' directory
    if not is_utils_directory(current_dir):
        print("Error: This script must be run from the 'utils/' directory of the Pizza3 project.")
        sys.exit(1)

    # Define the parent (root) directory
    parent_dir = current_dir.parent

    # Check if parent directory has essential files (excluding setup.py)
    # Adjust expected_files as needed
    # For initial setup, you might not have 'README.md', adjust accordingly
    # Here, we'll skip this check to allow setup.py creation even if other files are missing
    # Uncomment the following lines if you want to enforce the presence of certain files
    """
    if not check_project_structure(parent_dir):
        print(f"Error: The parent directory '{parent_dir}' does not contain the expected project files.")
        print("Please ensure you're running the script from the correct 'utils/' directory.")
        sys.exit(1)
    """

    # Define the output file
    output_file = 'setup.py'

    # Define external dependencies
    dependencies = [
        "numpy>=1.21.0"
    ]

    # Generate setup.py
    generate_setup_py(parent_dir, output_file, dependencies)

if __name__ == '__main__':
    main()
