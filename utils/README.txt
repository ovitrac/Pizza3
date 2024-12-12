# Directory for small utilities
# backup, maintenance, synchronization
# INRAE\Olivier Vitrac - 2024-12-12

# *********************************************************
# All files are intented to be run from Pizza3/utils
# ********************************************************


Use ./generate_diagrams.sh
    to generate the inheritance tree for all classes in pizza/.
Use ./generate_all.sh
    to refresh all metadata __all__
    --> __all__ global variables defined or updated in all Python codes
Use ./generate_matlab_docs.py
    to refresh Matlab/Octave documentation
    --> html/index_matlab.html (no additional files)
Use ./pdocme.sh
    to regenerate the entire documentation in HTML
    --> html/index_matlab.html (with additional files)


Use ./create_default_manifest.sh to generate the manifest (with hashes)
    --> ../Pizza3.manifest

Use ./generate_simple_manifest.py to generate the simple manifest
    --> ../Pizza3.simple.manifest

Use ./backupme.sh to backup all files
    --> ../history/*.zip

Use ./generate_release.sh to generate a release from Pizza3.simple.manifest
    --> ../release/*.zip


# *********************************************************
# Procedure to refresh the entire help/documentation
# ********************************************************
cd utils
rm -rf ../html/
./generate_matlab_docs.py
./generate_diagrams.sh
./pdocme.sh

# *********************************************************
# Procedure to create a release
# ********************************************************
cd utils
./generate_simple_manifest.py
# edit and run
./generate_release.sh


# *********************************************************
# Procedure to resfresh 
#    setup.py
#    requirements.txt
#    MANIFEST.in <-- run first ./generate_simple_manifest.py
# ********************************************************
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