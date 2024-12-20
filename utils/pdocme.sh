#!/usr/bin/env bash

# Generate documentation for Python files in Pizza3
# Maintained by INRAE\olivier.vitrac@agroparistech.fr
# Revision history: 2022-12-06, updated 2024-12-11

# Short view of the file tree
# mainfolder/
# ├── Pizza3_dir/
# │   ├── pizza/
# │   │   ├── __init__.py
# │   │   ├── raster.py
# │   │   ├── private/
# │   │   │   ├── __init__.py
# │   │   │   ├── struct.py
# │   │   │   └── PIL/
# │   │   │       └── Image.py
# │   ├── examples/
# │   └── scripts/

# Typycal usage
# cd utils
# rm -rf ../html/
# ./generate_matlab_docs.py 
# ./generate_diagrams.sh 
# ./pdocme.sh

# INRAE\Olivier Vitrac
# Email: olivier.vitrac@agroparistech.fr
# Last Revised:** 2024-12-19



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
            print "<li class=\"file\"><a href=\"" htmlpath "\">" f "</a></li>"
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

# Create the initial part of index.html with head and scripts
cat > "$index_file" <<EOF
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Pizza3 Documentation Index</title>
    <style>
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
    }
    header h1 {
        margin: 0; 
        font-size: 1.5em;
    }
    #content {
        display: flex;
        height: 100vh;
    }
    #nav {
        min-width: 250px; 
        background: #fff; 
        border-right: 1px solid #ddd; 
        padding: 20px;
        overflow-y: auto; 
        box-sizing: border-box;
    }
    #main {
        flex: 1; 
        padding: 20px;
        overflow-y: auto;
        box-sizing: border-box;
    }
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
        background-color: #ff4d4d; /* fffae6 Light yellow background */
        color: #333; /* Dark text color */
        padding: 15px 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000; /* Ensures the banner stays on top */
        font-family: Arial, sans-serif;
        z-index: 1000;
    }
    .notification-banner a {
        color: #1a73e8; /* Blue color for the link */
        text-decoration: none;
        font-weight: bold;
    }
    .notification-banner a:hover {
    text-decoration: underline;
    }
    .close-button {
        position: absolute;
        right: 60px;
        top: 15px;
        background: none;
        border: none;
        font-size: 32px;
        font-weight: bold;
        color: #ffffff;
        cursor: pointer;
        z-index: 1001;
    }
    .close-button:hover {
        color: #dddddd;
    }
    .notification-banner {
        transition: all 0.3s ease;
    }

    .notification-banner a {
        transition: color 0.3s ease;
    }

    .notification-banner a:hover {
        color: #0056b3; /* Darker blue on hover */
    }
    /* Media Queries for Responsiveness */
    @media (max-width: 600px) {
      .notification-banner {
        flex-direction: column;
        text-align: center;
        padding: 10px;
      }

      .close-button {
        position: static;
        margin-top: 10px;
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
    </script>
</head>
<body>
    <header>
      <h1>Pizza3 Documentation Index</h1>
    </header>
    <div id="content">
      <div id="nav">
        <p><strong>Version:</strong> $PIZZA3_VERSION</p>
        <p><strong>Maintained by:</strong> $CONTACT</p>
        <hr>
EOF

# Append the navigation HTML
cat "$nav_file" >> "$index_file"

# Append the main content with markdownContent embedded within a <script> block
cat >> "$index_file" <<'EOF'
      </div>
        <!-- Notification Banner -->
        <div id="notification-banner" class="notification-banner">
        <span>
            If you were looking for the documentation of post- and pre-processing tools in Matlab, use this 
            <a href="./index_matlab.html" target="_blank">link</a> instead.
        </span>
        <button class="close-button" onclick="closeBanner()">&times;</button>
        </div>
      <div id="main">
        <h2>Welcome to Pizza3 Documentation</h2>
        <p>Select a Python module from the left panel to view its documentation. Click on a folder to expand/collapse its contents. <br/><i>Matlab/Octave codes for pre_ and post-preocessing are not listed here.</i></p>
        <hr>
        <!-- Embed the raw Markdown in a script block -->
        <div id="markdown-content"></div>
        <script>
          // Sample Markdown content with Mermaid diagram and table
          const markdownContent = `
EOF

# Append the processed markdown content
cat "$processed_markdown" >> "$index_file"

# Close the string and the script tag, and include the rest of the HTML
cat >> "$index_file" <<'EOF'
          `;
        
          // Render the Markdown content
          const markdownDiv = document.getElementById('markdown-content');
          markdownDiv.innerHTML = marked.parse(markdownContent);
          // Initialize Mermaid after Markdown is rendered
          mermaid.initialize({ startOnLoad: true });
        </script>
        <div id="markdown-content"></div>
        <footer>
            <p>Current date:<strong> <script>document.write(new Date().toLocaleDateString())</script></strong></p>
        </footer>
      </div>
    </div>
    <script>
        // Function to close the notification banner
        function closeBanner() {
        var banner = document.getElementById('notification-banner');
        if (banner) {
            banner.style.display = 'none';
        }
        }
    </script>
</body>
</html>
EOF

# Cleanup temporary files
rm "$tmp_file" "$nav_file" "$processed_markdown"

echo "Documentation generation completed. Output in $output_dir"
echo "Index created at $index_file"
