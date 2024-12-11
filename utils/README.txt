# Directory for small utilities
# backup, maintenance, synchronization
# INRAE\Olivier Vitrac - 2024

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