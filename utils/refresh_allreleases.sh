#!/bin/bash

# *********************************************************
# Script: refresh_allreleases.sh
# Purpose: Refresh all releases of Pizza3 by archiving old releases
#          and generating new full and minimalist releases.
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

# Step 1: Verify Execution Directory
print_header "Step 1/3: Verifying Execution Directory"

current_dir=$(basename "$PWD")
if [[ "$current_dir" != "utils" ]]; then
    echo "Error: This script must be run from the 'utils' directory."
    exit 1
else
    echo "Verified: Running from 'utils' directory."
fi

# Define absolute paths
mainfolder="$(realpath ../)"
releases_dir="${mainfolder}/release"
history_dir="${releases_dir}/history"

# Step 2: Archive Existing Releases
print_header "Step 2/3: Archiving Existing Releases"

# Create history directory if it doesn't exist
if [[ ! -d "$history_dir" ]]; then
    echo "Creating history directory at '$history_dir'."
    mkdir -p "$history_dir"
    echo "History directory created."
fi

# Find zip files in releases_dir (excluding subdirectories)
mapfile -t zip_files < <(find "$releases_dir" -maxdepth 1 -type f -name "*.zip")

if [[ ${#zip_files[@]} -eq 0 ]]; then
    echo "No release zip files found in '$releases_dir'. Skipping archiving."
else
    echo "Archiving the following release zip files:"
    printf "%-50s %10s\n" "Filename" "Size"
    printf "%-50s %10s\n" "--------" "----"
    
    for zip_file in "${zip_files[@]}"; do
        # Get filename without path
        filename=$(basename "$zip_file")
        
        # Get the modification date in YYYY-MM-DD_HH-MM format
        mod_date=$(date -r "$zip_file" '+%Y-%m-%d_%H-%M')
        
        # Define new filename with date
        new_filename="${filename%.zip}_$mod_date.zip"
        
        # Move and rename the zip file to history_dir
        mv "$zip_file" "${history_dir}/${new_filename}"
        
        # Get the size of the moved file in human-readable format
        filesize=$(du -h "${history_dir}/${new_filename}" | cut -f1)
        
        # Print the details
        printf "%-50s %10s\n" "$new_filename" "$filesize"
    done
fi

echo ""

# Step 3: Generating New Releases
print_header "Step 3/3: Generating New Releases"

# Define paths to generation scripts
generate_simple_manifest="${PWD}/generate_simple_manifest.py"
generate_release="${PWD}/generate_release.sh"
generate_mini_manifest="${PWD}/generate_mini_manifest.py"
generate_mini_release="${PWD}/generate_mini_release.sh"

# Check if the required scripts exist and are executable
check_script "$generate_simple_manifest"
check_script "$generate_release"
check_script "$generate_mini_manifest"
check_script "$generate_mini_release"

# Function to generate a release
generate_release_type() {
    local manifest_script="$1"
    local release_script="$2"
    local release_type="$3"
    
    print_header "Generating ${release_type} Release"
    
    echo "Running '${manifest_script##*/}'..."
    python3 "$manifest_script"
    echo "Manifest generated successfully."
    
    echo "Running '${release_script##*/}'..."
    bash "$release_script"
    echo "Completed '${release_script##*/}'."
}

# Generate Full Release
generate_release_type "$generate_simple_manifest" "$generate_release" "Full"

# Generate Minimalist Release
generate_release_type "$generate_mini_manifest" "$generate_mini_release" "Minimalist"

echo ""

# Step 4: Display Details of New Releases
print_header "Release Generation Summary"

# Find new zip files in releases_dir (excluding history/)
mapfile -t new_zip_files < <(find "$releases_dir" -maxdepth 1 -type f -name "*.zip")

if [[ ${#new_zip_files[@]} -eq 0 ]]; then
    echo "No new release zip files were generated."
else
    echo "Newly generated release zip files:"
    printf "%-50s %10s\n" "Filename" "Size"
    printf "%-50s %10s\n" "--------" "----"
    
    for new_zip in "${new_zip_files[@]}"; do
        filename=$(basename "$new_zip")
        filesize=$(du -h "$new_zip" | cut -f1)
        printf "%-50s %10s\n" "$filename" "$filesize"
    done
fi

echo ""
echo "All release generation steps have been executed successfully."
echo "Archived releases can be found in the '$history_dir' directory."
