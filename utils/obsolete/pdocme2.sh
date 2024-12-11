#!/usr/bin/env bash

# Bash launcher to generate documentation for Pizza3 modules using pdoc
# This version uses __init__.py files
# Maintained by INRAE\olivier.vitrac@agroparistech.fr
# Revision history: 2024-12-08

# Ensure the script is run from Pizza3/utils/
if [[ ! -f "pdocme.sh" ]]; then
    echo "Error: This script must be run from the Pizza3/utils/ directory."
    exit 1
fi

# Identify mainfolder dynamically
mainfolder="$(realpath ../)"

# Configuration
output_dir="$mainfolder/html"
mkdir -p "$output_dir"

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

# Paths to include in PYTHONPATH
additional_paths=(
    "$mainfolder"
    "$mainfolder/pizza"
)

# Set PYTHONPATH dynamically
export PYTHONPATH=$(IFS=:; echo "${additional_paths[*]}")

# Build the find command with exclusions for directories
find_cmd="find \"$mainfolder\" -type d"
for pattern in "${excluded_patterns[@]}"; do
    find_cmd+=" -not -path \"*/$pattern/*\""
done

# Filter out excluded directories and process valid packages
eval "$find_cmd" | while read -r dir; do
    # Check for __init__.py to identify Python packages
    if [[ -f "$dir/__init__.py" ]]; then
        # Derive module name from the directory structure
        relative_path="${dir#$mainfolder/}"
        module_name="${relative_path//\//.}"  # Convert path to module name
        module_output_dir="$output_dir/$relative_path"

        # Ensure the output directory exists
        mkdir -p "$module_output_dir"

        echo "Processing $module_name -> $module_output_dir"
        pdoc -f --html -o "$output_dir" "$module_name"
    fi
done
