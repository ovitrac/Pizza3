#!/usr/bin/env bash

cat <<'END_DOC' >/dev/null
==========================================================================
pdocme.sh - Automated Documentation Generation Script for Pizza3

Author:       Olivier Vitrac
Maintainer:   INRAE\olivier.vitrac@agroparistech.fr
Version:      0.99
Last Updated: 2024-12-26
License:      MIT License

==========================================================================
DESCRIPTION
----------
pdocme.sh is a Bash script designed to automate the generation of HTML 
documentation for Python modules within the Pizza3 project. It leverages 
tools like `pdoc` for documentation generation and incorporates custom 
features such as a collapsible sidebar and a notification banner to enhance 
the user experience of the generated documentation site.

FEATURES
--------
- **Automated Documentation Generation:** Scans Python files, excluding 
  specified directories and files, and generates HTML documentation using 
  `pdoc`. If the module cannot be converted, the raw code is converted into
  HTML.
  
- **Navigation Structure:** Creates a dynamic navigation sidebar (`folders.nav`) 
  that reflects the project's directory structure, allowing users to easily 
  navigate through different modules and packages.
  
- **Markdown Processing:** Processes Markdown files to include Mermaid 
  diagrams and ensures proper rendering by escaping necessary characters.
  
- **Responsive Design:** Integrates a collapsible sidebar that adapts to 
  various screen sizes, ensuring accessibility across devices.
  
- **Notification Banner:** Adds a customizable notification banner at the top 
  of the documentation site with a functional close button.

USAGE
-----
1. **Navigate to the Script Directory:**
   Ensure you're in the `Pizza3/utils/` directory where `pdocme.sh` resides.
   ```bash
   cd Pizza3/utils/
   ```

2. **Set Up Environment:**
   Remove any existing HTML documentation to avoid conflicts.
   ```bash
   rm -rf ../html/
   ```

3. **Execute the Script:**
   Run the script to generate the documentation.
   ```bash
   ./pdocme.sh
   ```

SCRIPT STRUCTURE
----------------
1. **Pre-execution Checks:**
   - Verifies that the script is executed from the correct directory.
   - Exits with an error message if not run from `Pizza3/utils/`.

2. **Configuration Variables:**
   - `mainfolder`: Absolute path to the main Pizza3 project directory.
   - `output_dir`: Destination directory for the generated HTML documentation.
   - `PYTHON_VERSION`: Python version used in `PYTHONPATH`.
   - `PIZZA3_VERSION`: Version identifier for the Pizza3 project.
   - `CONTACT`: Maintainer contact information.
   - Temporary file variables for processing.

3. **Environment Setup:**
   - Creates the output directory if it doesn't exist.
   - Dynamically sets the `PYTHONPATH` to include necessary project and Python directories.

4. **Exclusion Lists:**
   - Defines directories and files to exclude from documentation generation to streamline the output.

5. **File Discovery:**
   - Constructs and executes a `find` command to list all relevant Python files, excluding specified paths.
   - Saves the list of files to a temporary file for further processing.

6. **HTML File Management:**
   - Renames existing HTML files in the output directory to prevent overwriting, excluding protected files.

7. **Documentation Generation:**
   - Iterates over the list of Python modules and generates HTML documentation using `pdoc`.
   - Ensures that the directory structure in the output mirrors the project's structure.

8. **Navigation Structure Creation:**
   - Utilizes `awk` to parse the list of Python files and generate a hierarchical navigation sidebar (`folders.nav`).

9. **Markdown Processing:**
   - Processes Markdown files to replace Mermaid code blocks with `<div class="mermaid">` wrappers.
   - Escapes backticks and curly braces to ensure proper rendering in JavaScript template literals.

10. **Index Page Generation:**
    - Compiles the `index.html` file by embedding styles, scripts, navigation structure, and processed Markdown content.
    - Incorporates a responsive and collapsible sidebar along with a notification banner.

11. **Cleanup:**
    - Removes temporary files used during the documentation generation process to maintain a clean environment.

12. **Final Output:**
    - Opens the generated `index.html` in the default web browser for immediate viewing.

DEPENDENCIES
------------
- **pdoc:** Python documentation generator. Ensure it's installed and accessible in the system PATH.
  ```bash
  pip install pdoc
  ```
  
- **awk:** Text processing tool used for generating the navigation structure.
  
- **sed:** Stream editor for filtering and transforming text.

CONFIGURATION
-------------
- **Exclusion Lists:**
  - `excluded_dirs`: Directories within the project to exclude from documentation (e.g., `fork`, `history`, `help`).
  - `excluded_files`: Specific Python files to exclude (e.g., `__init__.py`, `debug.py`).

- **Protected HTML Files:**
  - A list of HTML files that should not be renamed during the documentation update process to preserve important pages.

ERROR HANDLING
--------------
- **Script Execution Location:**
  - The script checks if it's being run from the `Pizza3/utils/` directory. If not, it exits with an error message.
  
- **File Processing Warnings:**
  - Alerts the user if the processed Markdown file is empty or missing, indicating that Markdown content won't be displayed.

- **Toggle Button and Navigation Sidebar Presence:**
  - Logs an error in the browser console if the toggle button or navigation sidebar is not found, aiding in debugging front-end issues.

REVISION HISTORY
----------------
- **2022-12-06:** Initial version created.
- **2024-12-11:** Updated with sidebar functionality and notification banner adjustments.
- **2024-12-23:** Final revisions and bug fixes to ensure complete functionality.


EXAMPLE DIRECTORY STRUCTURE
---------------------------
```
mainfolder/
├── Pizza3_dir/
│   ├── pizza/
│   │   ├── __init__.py
│   │   ├── raster.py
│   │   ├── private/
│   │   │   ├── __init__.py
│   │   │   ├── struct.py
│   │   │   └── PIL/
│   │   │       └── Image.py
│   ├── examples/
│   └── scripts/
```

EXIT CODES
----------
- **0:** Successful execution.
- **1:** Error due to incorrect execution directory.

CONTACT
-------
For any issues, suggestions, or contributions, please contact:

**INRAE\Olivier Vitrac**  
Email: [olivier.vitrac@agroparistech.fr](mailto:olivier.vitrac@agroparistech.fr)

==========================================================================
END_DOC


# Ensure the script is run from Pizza3/utils/
if [[ ! -f "pdocme.sh" ]]; then
    echo "Error: This script must be run from the Pizza3/utils/ directory."
    exit 1
fi

mainfolder="$(realpath ../)"

# Configuration
output_dir="$mainfolder/html"
PYTHON_VERSION="3.10"
PIZZA3_VERSION="Pizza3 v.0.99"
CONTACT="INRAE\\olivier.vitrac@agroparistech.fr"
tmp_file="tmp.pdocme.txt"
nav_file="folders.nav"
output_markdown="$output_dir/pizza_classes_documentation.md"
processed_markdown="$output_dir/processed_pizza_classes_documentation.md"

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

# To fix MESA loader
# libstdc++.so.6 file is located in /usr/lib/x86_64-linux-gnu/libstdc++.so.6
export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6

# Files and folders to exclude
excluded_dirs=(
    "fork"
    "history"
    "help"
    "debug"
    "tmp"
    "PIL"
    "restore"
    "__all__"
    "windowsONLY"
)

excluded_files=(
    "__init__.py"
    "__main__.py"
    "manifest.py"
    "debug.py"
)

# Build find command
find_cmd="find \"$mainfolder\" -type f -name \"*.py\""
for dir in "${excluded_dirs[@]}"; do
    find_cmd+=" -not -path \"*/$dir/*\""
done
for file in "${excluded_files[@]}"; do
    find_cmd+=" -not -name \"$file\""
done

echo "Running find command to list Python files..."
eval "$find_cmd" > "$tmp_file"
echo "File list saved to $tmp_file"

# Rename existing HTML files to *.html~
#!/bin/bash

# List of HTML files to protect from renaming
protected_htmlfiles=(
    "class_examples.html"
    "index_matlab.html"
    "index_post.html"
    "POST_example1.html"
    "POST_example2.html"
    "POST_example3.html"
)

# Rename existing HTML files to *.html~
echo "Renaming existing HTML files to *.html~..."
find "$output_dir" -type f -name "*.html" | while read -r html_file; do
    # Get the base name of the HTML file
    base_name=$(basename "$html_file")    
    # Check if the file is in the protected list
    if [[ " ${protected_htmlfiles[@]} " =~ " ${base_name} " ]]; then
        echo "Skipping protected file: $html_file"
        continue
    fi
    # Rename the file
    mv "$html_file" "${html_file}~"
    echo "Renamed $html_file -> ${html_file}~"
done

# Sort and generate documentation
sort "$tmp_file" -o "$tmp_file"
echo "Generating documentation for modules..."
while read -r module; do
    relative_path="${module#$mainfolder/}"
    relative_output_path="${relative_path%.py}.html"
    module_output_file="$output_dir/$relative_output_path"
    mkdir -p "$(dirname "$module_output_file")"
    echo "Processing $module -> $module_output_file"
    pdoc -f --html --output-dir "$(dirname "$module_output_file")" "$module"
    # Check if the HTML file exists
    if [[ ! -f "$module_output_file" ]]; then
        echo "pdoc failed for $module. Generating raw HTML with syntax highlighting..."
        ./convert_py_to_html.py "$module" "$module_output_file"
    else
        echo "HTML successfully created for $module"
    fi
done < "$tmp_file"

# Create a navigation structure using awk
awk -v mainfolder="$mainfolder" '
BEGIN {
    FS = "/";
}
{
    full=$0
    sub(mainfolder"/","",full)
    rel=full
    sub(/\.py$/, "", rel)
    dir=rel
    file=rel
    idx = length(rel)
    while (idx > 0 && substr(rel, idx, 1) != "/") idx--
    if (idx > 0) {
        dir = substr(rel,1,idx-1)
        file = substr(rel,idx+1)
    } else {
        dir = "."
    }
    files[dir, file] = 1
    dirs[dir] = 1
}
END {
    n=0
    for (d in dirs) {
        dirlist[n++]=d
    }
    asort(dirlist)

    print "<ul class=\"folder-list\">"
    for (i=1; i<=n; i++) {
        d = dirlist[i]
        if (d == ".") {
            dirname = "(root)"
        } else {
            dirname = d
        }

        print "<li class=\"folder\">"
        print "<div class=\"folder-title\" onclick=\"toggleFolder(this)\">" dirname "</div>"
        print "<ul class=\"folder-content\">"

        m=0
        for (ff in files) {
            split(ff,p,SUBSEP)
            if (p[1] == d) {
                filist[m++]=p[2]
            }
        }
        asort(filist)
        for (j=1; j<=m; j++) {
            f=filist[j]
            if (d == ".") {
                htmlpath = f ".html"
            } else {
                htmlpath = d "/" f ".html"
            }
            print "<li class=\"file\"><a href=\"" htmlpath "\" target=\"_blankpy\">" f "</a></li>"
        }
        delete filist
        print "</ul>"
        print "</li>"
    }
    print "</ul>"
}' "$tmp_file" > "$nav_file"

# Process the Markdown file:
# 1. Replace ```mermaid ... ``` with <div class="mermaid"> ... </div>
# 2. Escape backticks (`) and curly braces ({, })
sed -e '/```mermaid/,/```/ {
    /^```mermaid$/c\<div class="mermaid">
    /^```$/c\</div>
}' "$output_markdown" | sed -e 's/`/\\`/g' -e 's/{/\\{/g' -e 's/}/\\}/g' > "$processed_markdown"

# Create index.html
index_file="$output_dir/index.html"
echo "Creating index.html at $index_file..."

# Check if $processed_markdown exists and is not empty
if [[ ! -s "$processed_markdown" ]]; then
    echo "Warning: $processed_markdown is empty or does not exist. Markdown content will not be displayed."
fi

# Create the initial part of index.html with head and styles
cat > "$index_file" <<EOF
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Pizza3 Documentation Index</title>
    <style>
    /* General Styles */
    body {
        font-family: 'Segoe UI', Arial, sans-serif; 
        margin: 0; 
        padding: 0; 
        line-height: 1.6; 
        background-color: #f9f9f9; 
        color: #333;
    }
    header {
        background: #4CAF50; 
        color: #fff; 
        padding: 10px;
        position: relative; /* For positioning the toggle button */
    }
    header h1 {
        margin: 0; 
        font-size: 1.5em;
        color: #fff; /* Explicitly set to white */
        padding-left: 50px; /* Space for the toggle button */
    }
    /* Sidebar Styles */
    #content {
        display: flex;
        height: calc(100vh - 50px); /* Adjusted for header height */
        transition: all 0.3s ease; /* Enable transitions for smooth animations */
    }
    #nav {
        width: 300px; /* Set a fixed width */
        background: #fff;
        border-right: 1px solid #ddd;
        padding: 20px;
        overflow-y: auto;
        box-sizing: border-box;
        transition: width 0.3s ease, padding 0.3s ease; /* Transition for smooth width and padding changes */
        position: relative; /* Ensure it stays in place when collapsing */
        z-index: 1000; /* To overlay on small screens */
    }
    #nav.collapsed {
        width: 0; /* Hide the sidebar by setting width to 0 */
        padding: 0; /* Remove padding to allow full collapse */
        overflow: hidden; /* Hide overflowing content */
    }
    #main {
        flex: 1;
        padding: 20px;
        overflow-y: auto;
        box-sizing: border-box;
        transition: margin-left 0.3s ease; /* Smooth transition when sidebar collapses */
    }
    /* Folder Styles */
    h2 {
        color: #333; 
        border-bottom: 2px solid #4CAF50; 
        padding-bottom: 5px;
    }
    a {
        text-decoration: none; 
        color: #007BFF;
    }
    a:hover {
        text-decoration: underline;
    }
    ul {
        list-style-type: none; 
        padding-left: 0;
        margin: 0;
    }
    li {
        margin: 5px 0;
    }
    .folder-title {
        font-weight: bold; 
        color: #333; 
        padding: 5px 0;
        cursor: pointer;
    }
    .folder-content {
        margin-left: 20px;
        display: none; /* start collapsed */
    }
    .file {
        margin-left: 20px;
    }
    hr {
        margin: 20px 0; 
        border: 1px solid #ddd;
    }
    footer {
        font-size: 0.9em; 
        color: #666; 
        margin-top: 20px; 
        text-align: center;
    }
    /* Enhanced Table Styling with Banded Colors */
    table {
        border-collapse: collapse;
        width: 100%;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 8px;
    }
    th {
        background-color: #4CAF50;
        color: white;
    }
    tr:nth-child(even) {
        background-color: #f2f2f2; /* Light gray for even rows */
    }
    tr:nth-child(odd) {
        background-color: rgba(76, 175, 80, 0.1); /* Light green for odd rows */
    }
    /* Notification Banner Styling */
    .notification-banner {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: #ff4d4d; /* Red background */
        color: #fff; /* White text */
        padding: 15px 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000; /* Ensures the banner stays on top */
        font-family: Arial, sans-serif;
        box-sizing: border-box; /* Ensure padding is included in width */
    }
    .notification-banner a {
        color: #ffffff; /* White color for the link */
        text-decoration: underline;
        font-weight: bold;
    }
    .notification-banner a:hover {
        color: #dddddd; /* Light gray on hover */
    }
    .close-button {
        position: absolute;
        right: 40px; /* Adjusted from 20px to 50px for visibility */
        top: 15px;
        background: none;
        border: none;
        font-size: 24px;
        font-weight: bold;
        color: #ffffff;
        cursor: pointer;
        z-index: 1001;
    }
    .close-button:hover {
        color: #dddddd;
    }
    /* Toggle Sidebar Button */
    .toggle-btn {
        position: absolute;
        top: 50%;
        transform: translateY(-50%); /* Center the button vertically */
        left: 10px; /* Place the button on the left */
        background-color: #4CAF50; /* Green background */
        border: none;
        color: white; /* Ensure the hamburger icon is white */
        padding: 10px 12px; /* Adjust padding for larger button */
        cursor: pointer;
        font-size: 1.2em; /* Increase font size for better visibility */
        border-radius: 4px;
        z-index: 1001; /* Ensure the button is above other elements */
    }
    .toggle-btn:hover {
        background-color: #45a049;
    }
    .toggle-btn kbd {
        font-family: 'Arial', sans-serif; /* Match the header font */
        color: white; /* Ensure the hamburger icon is white */
        font-size: 1.2em; /* Same size as the button text */
        background: none; /* Remove any background styling from <kbd> */
        border: none; /* Remove any borders from <kbd> */
    }
    /* Responsive Design for Sidebar */
    @media screen and (max-width: 768px) {
        #nav {
            position: fixed;
            top: 0;
            left: 0;
            height: 100%;
            width: 250px; /* Ensure the width remains consistent */
            transform: translateX(-100%);
            transition: transform 0.3s ease;
            background: #fff;
            border-right: 1px solid #ddd;
            padding: 20px; /* Default padding */
        }
        #nav.collapsed {
            transform: translateX(-100%);
            width: 250px; /* Maintain width for small screens */
            padding: 20px; /* Maintain padding */
        }
        #nav.expanded {
            transform: translateX(0);
            width: 250px;
            padding: 20px;
        }
        /* Overlay when sidebar is open */
        body.nav-open::before {
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: 999;
        }
    }
    </style>
    <!-- Include Marked.js from CDN -->
    <script src="https://cdn.jsdelivr.net/npm/marked/lib/marked.umd.js"></script>
    <!-- Include Mermaid.js from CDN -->
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>
    // Toggle visibility of folder contents
    function toggleFolder(el) {
        var content = el.nextElementSibling;
        if (content.style.display === "none" || content.style.display === "") {
            content.style.display = "block";
        } else {
            content.style.display = "none";
        }
    };
    
    // Function to close the notification banner
    function closeBanner() {
        var banner = document.getElementById('notification-banner');
        if (banner) {
            banner.style.display = 'none';
        }
    }
    </script>
</head>
<body>
    <!-- Notification Banner -->
    <div id="notification-banner" class="notification-banner">
        <span>
            If you were looking for the documentation of post- and pre-processing tools in Matlab, use this 
            <a href="./index_matlab.html" target="_blank">link</a> instead.
        </span>
        <button class="close-button" onclick="closeBanner()">&times;</button>
    </div>

    <header>
        <!-- Toggle Sidebar Button -->
        <button class='toggle-btn' id='toggleSidebar' aria-label='Toggle Sidebar' aria-expanded='false'>
            <kbd>&#9776;</kbd>
        </button>
        <h1>Pizza3 Documentation Index</h1>
    </header>
    <div id='content'>
        <div id='nav'>
            <p><strong>Version:</strong> $PIZZA3_VERSION</p>
            <p><strong>Maintained by:</strong> $CONTACT</p>
            <hr>
EOF

# Append the navigation HTML
cat "$nav_file" >> "$index_file"

# Continue writing the HTML body
cat >> "$index_file" <<'EOF'
        </div>
        <div id='main'>
            <h2>Welcome to Pizza3 Documentation</h2>
            <p>Select a Python module from the left panel to view its documentation. Click on a folder to expand/collapse its contents. <br/><i>Matlab/Octave codes for pre_ and post-preocessing are not listed here.</i></p>
            <hr>
            <!-- Embed the raw Markdown in a script block -->
            <div id="markdown-content"></div>
            <script>
                // Define the markdownContent variable with the processed Markdown
                const markdownContent = `
EOF

# Append the processed markdown content
cat "$processed_markdown" >> "$index_file"

# Continue writing the HTML with closing script tags and additional JavaScript
cat >> "$index_file" <<'EOF'
                `;
            
                // Render the Markdown content
                const markdownDiv = document.getElementById('markdown-content');
                if (markdownDiv) {
                    markdownDiv.innerHTML = marked.parse(markdownContent);
                    // Initialize Mermaid after Markdown is rendered
                    mermaid.initialize({ startOnLoad: true });
                }
            </script>
            <footer>
                <p>Current date:<strong> <script>document.write(new Date().toLocaleDateString())</script></strong></p>
            </footer>
        </div>
    </div>
    <script>
        // Toggle Sidebar Functionality
        document.addEventListener("DOMContentLoaded", function() {
            const toggleButton = document.getElementById('toggleSidebar');
            const nav = document.getElementById('nav');
            const body = document.body;

            if (toggleButton && nav) {
                toggleButton.addEventListener('click', () => {
                    if (window.innerWidth > 768) {
                        // For large screens, toggle 'collapsed' class to adjust width
                        nav.classList.toggle('collapsed');
                        // Change icon based on sidebar state
                        if(nav.classList.contains('collapsed')) {
                            toggleButton.innerHTML = '<kbd>&#9776;</kbd>'; // Hamburger icon
                            toggleButton.setAttribute('aria-expanded', 'false');
                        } else {
                            toggleButton.innerHTML = '<kbd>&#10005;</kbd>'; // Close icon (X)
                            toggleButton.setAttribute('aria-expanded', 'true');
                        }
                    } else {
                        // For small screens, toggle 'expanded' class to overlay sidebar
                        nav.classList.toggle('expanded');
                        body.classList.toggle('nav-open'); // Toggle overlay
                        // Change icon based on sidebar state
                        if(nav.classList.contains('expanded')) {
                            toggleButton.innerHTML = '<kbd>&#10005;</kbd>'; // Close icon (X)
                            toggleButton.setAttribute('aria-expanded', 'true');
                        } else {
                            toggleButton.innerHTML = '<kbd>&#9776;</kbd>'; // Hamburger icon
                            toggleButton.setAttribute('aria-expanded', 'false');
                        }
                    }
                });
            } else {
                console.error("Toggle button or navigation sidebar not found.");
            }

            // No need to attach additional event listeners for folder toggling
            // since the folders have inline onclick="toggleFolder(this)"
        });
    </script>
</body>
</html>
EOF

# Cleanup temporary files
rm "$tmp_file" "$nav_file" "$processed_markdown"

echo "Documentation generation completed. Output in $output_dir"
echo "Index created at $index_file"