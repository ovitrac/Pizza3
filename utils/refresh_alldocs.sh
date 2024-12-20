#!/bin/bash

# *********************************************************
# Script: refresh_alldocs.sh
# Purpose: Refresh the entire documentation of Pizza3.
# Author: INRAE\Olivier Vitrac
# Email: olivier.vitrac@agroparistech.fr
# Last Revised: 2024-12-20
# *********************************************************

# Exit immediately if a command exits with a non-zero status
set -e

# Function to print headers
print_header() {
    echo ""
    echo "=============================================="
    echo "$1"
    echo "=============================================="
    echo ""
}

# Function to check if a script exists and is executable
check_script() {
    if [[ ! -x "$1" ]]; then
        echo "Error: '$1' does not exist or is not executable."
        exit 1
    fi
}

# Step 1: Ensure the script is run from the 'utils' directory
current_dir=$(basename "$PWD")
if [[ "$current_dir" != "utils" ]]; then
    echo "Error: This script must be run from the 'utils' directory."
    exit 1
fi

# Define paths
HTML_DIR="../html"
HISTORY_DIR="../history"

# Step 2: Archive the existing 'html' directory
print_header "Step 1/3: Archiving the existing 'html' directory"

# Create history directory if it doesn't exist
if [[ ! -d "$HISTORY_DIR" ]]; then
    echo "Creating history directory at '$HISTORY_DIR'."
    mkdir -p "$HISTORY_DIR"
    echo "History directory created."
fi

# Check if 'html' directory exists
if [[ -d "$HTML_DIR" ]]; then
    # Get username and hostname
    USERNAME=$(whoami)
    HOSTNAME=$(hostname)
    
    # Get current timestamp in 'yyyy-mm-dd_HH-MM' format
    TIMESTAMP=$(date '+%Y-%m-%d_%H-%M')
    
    # Define zip filename
    ZIP_FILENAME="${USERNAME}@${HOSTNAME}_${TIMESTAMP}.zip"
    
    # Define full path for the zip file
    ZIP_PATH="${HISTORY_DIR}/${ZIP_FILENAME}"
    
    # Archive the 'html' directory with maximum compression
    echo "Archiving '$HTML_DIR' to '$ZIP_PATH' with maximum compression (-9)..."
    zip -r -9 "$ZIP_PATH" "$HTML_DIR" > /dev/null
    echo "Archiving completed successfully."
else
    echo "Warning: '$HTML_DIR' does not exist. Skipping archiving."
fi

# Step 3: Remove the existing 'html' directory and regenerate documentation
print_header "Step 2/3: Removing the existing 'html' directory and regenerating documentation"

# Remove the existing 'html' directory
if [[ -d "$HTML_DIR" ]]; then
    echo "Removing the existing '$HTML_DIR' directory..."
    rm -rf "$HTML_DIR"
    echo "Removal completed successfully."
else
    echo "No existing '$HTML_DIR' directory found. Proceeding to generate new documentation."
fi

# Check if the required scripts exist and are executable
check_script "./generate_matlab_docs.py"
check_script "./generate_diagrams.sh"
check_script "./pdocme.sh"

# Run the documentation generation scripts with status messages
echo "Running 'generate_matlab_docs.py'..."
./generate_matlab_docs.py
echo "Completed 'generate_matlab_docs.py'."

echo "Running 'generate_diagrams.sh'..."
./generate_diagrams.sh
echo "Completed 'generate_diagrams.sh'."

echo "Running 'pdocme.sh'..."
./pdocme.sh
echo "Completed 'pdocme.sh'."

# Step 4: Final Completion Message
print_header "Step 3/3: Documentation refresh completed successfully"

echo "All documentation steps have been executed successfully."
echo "The new 'html' documentation has been generated."
echo "Previous documentation archives can be found in the '$HISTORY_DIR' directory."
