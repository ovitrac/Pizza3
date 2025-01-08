#!/usr/bin/env bash

# ----------------------------------------------------------
#                      W A R N I N G
# ----------------------------------------------------------
# Legacy/obsolete code for refreshing all pdoc files (html).
# Use pdocme.sh or refresh_alldocs.sh instead
# Use generate_all.py to  __all__ variables in modules
# ----------------------------------------------------------

# Maintained by INRAE\olivier.vitrac@agroparistech.fr
# Revision history: 2024-12-06, 2025-01-08

# Typical file structure

# mainfolder/
# ├── pizza/
# │   ├── data3.py
# │   ├── __init__.py
# │   ├── raster.py
# ├── scripts/
# │   ├── setup.py
# │   ├── __main__.py
# ├── history/
# │   ├── old_script.py
# ├── tmp/
# │   ├── debug.py


# Ensure the script is run from Pizza3/utils/
if [[ ! -f "pdocme.sh" ]]; then
    echo "Error: This script must be run from the Pizza3/utils/ directory."
    exit 1
fi

# Identify mainfolder dynamically
mainfolder="$(realpath ../)"

# Configuration
output_dir="$mainfolder/html"
mkdir -p $output_dir

# Names to exclude (directories)
excluded_patterns=(
    "history"
    "fork"
    "tmp"
    "sandbox"
    "PIL"
    "draft"
    "restore"
    "windowsONLY"
    "__all__"
    "debug"
)

# Files to exclude
excluded_files=(
    "__init__.py"
    "__main__.py"
)


# Paths to include in PYTHONPATH
additional_paths=(
    "$mainfolder"
    "$mainfolder/pizza"
)

# Set PYTHONPATH dynamically
export PYTHONPATH=$(IFS=:; echo "${additional_paths[*]}")

# To fix MESA loader
# libstdc++.so.6 file is located in /usr/lib/x86_64-linux-gnu/libstdc++.so.6
export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6

# Build find command with exclusions
find_cmd="find \"$mainfolder\" -type f -name \"*.py\""
for pattern in "${excluded_patterns[@]}"; do
    find_cmd+=" -not -path \"*/$pattern/*\""
done
for file in "${excluded_files[@]}"; do
    find_cmd+=" -not -name \"$file\""
done

# Generate the list of files
eval "$find_cmd" > pyfilelist.txt

# Run pdoc for each file
while read -r file; do
    # Derive the relative path for output
    relative_path="${file#$mainfolder/}"
    module_output_dir="$output_dir/$(dirname "$relative_path")"

    # Ensure the output directory exists
    mkdir -p "$module_output_dir"

    echo "Processing $file -> $module_output_dir"
    pdoc -f --html -o "$module_output_dir" "$file"
done < pyfilelist.txt

# Cleanup
rm pyfilelist.txt

