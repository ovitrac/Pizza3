#!/usr/bin/env bash

# Generate a global Markdown documentation with Mermaid diagrams
# for all modules found in $mainfolder/pizza
#
# Prerequisites:
#  - Python 3.x
#  - generate_mermaid.py (the Python script) must be in the same directory
#
# Usage:
#  ./generate_diagrams.sh

# Ensure script is run in a proper context (adjust if needed)
if [[ ! -d "../pizza" ]]; then
    echo "Error: '../pizza' directory not found. Adjust mainfolder path accordingly."
    exit 1
fi

########################
# Configuration Section
########################

# Main folder and paths
mainfolder="$(realpath ../)"
output_markdown="$mainfolder/html/pizza_classes_documentation.md"

# Python version (adjust if needed)
PYTHON_VERSION="3.10"

# Output directories and variables
output_dir="$(dirname "$output_markdown")"

# Ensure output directory exists
mkdir -p "$output_dir"

# Paths to include in PYTHONPATH
additional_paths=(
    "$mainfolder"
    "$mainfolder/pizza"
    "$HOME/anaconda3/lib/python$PYTHON_VERSION"
    "$HOME/anaconda3/lib/python$PYTHON_VERSION/lib-dynload"
    "$HOME/anaconda3/lib/python$PYTHON_VERSION/site-packages"
    "$HOME/.ipython"
)

# Set PYTHONPATH dynamically
export PYTHONPATH=$(IFS=:; echo "${additional_paths[*]}")
echo "PYTHONPATH set to: $PYTHONPATH"

# Directories to exclude (e.g., PIL)
excluded_dirs=(
    "PIL"
    "demo"
    "examples"
    "debug"
    "sandbox"
    "windowsONLY"
)

########################
# Generate Modules List
########################

# Build the find command with exclusions
find_cmd="find \"$mainfolder/pizza\" -type f -name \"*.py\""
for dir in "${excluded_dirs[@]}"; do
    find_cmd+=" ! -path \"*$dir/*\""
done

# Execute the find command and transform paths for Python import
modules_list=$(eval "$find_cmd" | sed "s|$mainfolder/||;s|\.py$||" | sed 's|/|.|g')


if [[ -z "$modules_list" ]]; then
    echo "Error: No Python files found in the specified directory."
    exit 1
fi

########################
# Generate Documentation
########################

# Pass the module list to the Python script
echo "$modules_list" | python3 generate_mermaid.py "$output_markdown"

# Final message
echo "Markdown file generated at $output_markdown"
