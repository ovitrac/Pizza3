#!/usr/bin/env python3
"""
## **Script Documentation**

### **Pizza3.simple.manifest Generator**

#### **Description**

The `manifest_generator.py` script is designed to traverse the project directory structure and generate a manifest file named `Pizza3.simple.manifest`. This manifest lists all relevant files within the project, excluding specified directories and file types. It is particularly useful for tracking files included in the Pizza3 project, facilitating version control, deployment, or distribution processes.

#### **Features**

- **Exclusion of Specific Folders and File Types:**  
  The script ignores directories and file extensions that are unnecessary or irrelevant for the manifest, ensuring a clean and concise list of pertinent files.

- **Execution Directory Verification:**  
  Ensures that the script is executed from the `utils/` directory to maintain consistency and prevent path-related issues.

- **Configurable Output Folder:**  
  Allows specification of the output folder (`mainfolder`), which is the parent directory of `utils/`, ensuring that the manifest is generated in the correct location.

- **Custom Output Filename:**  
  Generates the manifest file with a standardized name, `Pizza3.simple.manifest`, for easy identification and access.

- **Timestamp Inclusion:**  
  Inserts the date and time of manifest generation within the file for reference and tracking purposes.

#### **Usage**

1. **Ensure Correct Execution Directory:**  
   The script must be run from the `utils/` directory of the Pizza3 project.

2. **Run the Script:**  
   Execute the script using Python 3:
   
   ```bash
   python3 manifest_generator.py
   ```

3. **Output:**  
   Upon successful execution, a file named `Pizza3.simple.manifest` will be created in the specified `mainfolder`. This file will contain a list of all relevant files in the project directory, excluding those defined in the `ignore` list.

#### **Configuration**

- **Excluded Directories and File Types:**  
  The `ignore` list contains patterns of directories and file extensions to exclude from the manifest. These are consistent with the exclusions used in your previous Python documentation script.

- **Output Folder (`mainfolder`):**  
  Defined as the parent directory of `utils/`, ensuring that the manifest is placed appropriately within the project structure.

#### **Dependencies**

- **Python 3.x**

#### **Author**

- **INRAE\Olivier Vitrac**
- **Email:** olivier.vitrac@agroparistech.fr
- **Last Revised:** 2024-12-11

"""

import os
import re
import sys
from datetime import datetime
import html

# Ensure the script is run from Pizza3/utils/
if not os.path.isfile("pdocme.sh"):
    print("Error: This script must be run from the Pizza3/utils/ directory.")
    sys.exit(1)

# Configuration
mainfolder = os.path.realpath(os.path.join(".."))
output_dir = os.path.join(mainfolder, "html")
output_file = "index_matlab.html"
PIZZA3_VERSION = "Pizza3 v.0.99"
CONTACT = "INRAE\\olivier.vitrac@agroparistech.fr"

# CSS Style as per user request with explicit header h1 color
CSS_STYLE = """
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
    color: #fff; /* Explicitly set to white */
}
#content {
    display: flex;
    height: calc(100vh - 50px); /* Adjusted for header height */
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
h1 {
    font-size: 1.8em;
    color: #333;
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
/* Collapsible Code Section */
.collapsible {
    background-color: #f1f1f1;
    color: #333;
    cursor: pointer;
    padding: 10px;
    width: 100%;
    border: none;
    text-align: left;
    outline: none;
    font-size: 1em;
}
.active, .collapsible:hover {
    background-color: #ddd;
}
.content {
    padding: 0 18px;
    display: none;
    overflow: hidden;
    background-color: #f9f9f9;
}
/* Minimal Syntax Highlighting */
.code {
    background-color: #f4f4f4;
    padding: 10px;
    border: 1px solid #ddd;
    overflow-x: auto;
    font-family: 'Courier New', Courier, monospace;
    color: #333;
}
.keyword {
    color: #007BFF;
    font-weight: bold;
}
.comment {
    color: #6a9955;
    font-style: italic;
}
.string {
    color: #a31515;
}
"""

# JavaScript for toggle functionality and dynamic content display
JS_SCRIPT = """
// Toggle visibility of folder contents
function toggleFolder(el) {
    var content = el.nextElementSibling;
    if (content.style.display === "none" || content.style.display === "") {
        content.style.display = "block";
    } else {
        content.style.display = "none";
    }
};

// Load documentation into the main panel
function loadDoc(id) {
    // Hide all documentation sections
    var docs = document.getElementsByClassName('doc-content');
    for (var i = 0; i < docs.length; i++) {
        docs[i].style.display = 'none';
    }
    // Hide the welcome message
    var welcome = document.getElementById('welcome-message');
    if (welcome) {
        welcome.style.display = 'none';
    }
    // Show the selected documentation
    var selectedDoc = document.getElementById(id);
    if (selectedDoc) {
        selectedDoc.style.display = 'block';
    }
    
    // Reinitialize collapsible buttons within the displayed documentation
    var coll = selectedDoc.getElementsByClassName("collapsible");
    for (var i = 0; i < coll.length; i++) {
        // Remove existing event listeners to prevent multiple bindings
        coll[i].removeEventListener("click", toggleCollapsible);
        // Add event listener
        coll[i].addEventListener("click", toggleCollapsible);
    }
}

// Function to toggle collapsible sections
function toggleCollapsible() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
        content.style.display = "none";
    } else {
        content.style.display = "block";
    }
}

// Handle internal links to load in the same panel
document.addEventListener('click', function(e) {
    if (e.target.tagName === 'A' && e.target.getAttribute('href').startsWith('#')) {
        e.preventDefault();
        var targetId = e.target.getAttribute('href').substring(1);
        loadDoc(targetId);
    }
});
"""

# Build a list of MATLAB files, excluding certain directories or files
excluded_dirs = [
    "fork",
    "history",
    "help",
    "debug",
    "tmp",
    "PIL",
    "restore",
    "__all__",
    "windowsONLY"
]

excluded_files = [
    "__init__.m",
    "__main__.m",
    "manifest.m",
    "debug.m"
]

def is_excluded(path):
    # Check if path contains any excluded directory
    for d in excluded_dirs:
        if os.path.sep + d + os.path.sep in path:
            return True
    # Check if file is excluded
    basename = os.path.basename(path)
    if basename in excluded_files:
        return True
    return False

matlab_files = []
for root, dirs, files in os.walk(mainfolder):
    # filter out excluded dirs
    dirs[:] = [d for d in dirs if d not in excluded_dirs]
    for f in files:
        if f.endswith(".m"):
            full_path = os.path.join(root, f)
            if not is_excluded(full_path):
                matlab_files.append(full_path)

matlab_files.sort()

# Function to extract documentation from a MATLAB file
def extract_matlab_doc(filepath):
    """
    Extracts MATLAB help from a .m file according to the standard MATLAB format.
    Enhancements:
    - Correctly captures the function name from the function definition.
    - If no function line is found, uses the filename as the function name.
    - Ensures that the entire help block is captured, not just until the first empty line.
    - Recognizes "NOTE:", "Note:", "note:", "EXAMPLES:", etc., and handles multi-line content.
    - Includes the MATLAB code in a collapsible section with minimal syntax highlighting.
    """
    doc_lines = []
    function_name = None
    inside_help = False
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()

    # First pass: Try to find the function line with improved regex
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("function"):
            # Improved regex to capture the function name correctly
            match = re.match(r'^function\s+(?:\[[^\]]*\]\s*=\s*)?(?:[A-Za-z0-9_]+\s*=\s*)?([A-Za-z0-9_]+)', stripped)
            if match:
                function_name = match.group(1)
            # Start looking for help after this line
            help_start_idx = idx + 1
            break
    else:
        # No function line found; use filename as function name
        function_name = os.path.splitext(os.path.basename(filepath))[0]
        help_start_idx = 0  # Start from the beginning of the file

    # Extract help lines
    for line in lines[help_start_idx:]:
        stripped = line.strip()
        if stripped.startswith("%"):
            # Remove the leading '%' and one space if present
            helpline = stripped.lstrip('%').lstrip()
            doc_lines.append(helpline)
            inside_help = True
        else:
            # If we were inside help and hit a non-% line, stop
            if inside_help:
                break

    # If no help was found after function line, and no function line exists, check for leading comments
    if not doc_lines and function_name == os.path.splitext(os.path.basename(filepath))[0]:
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("%"):
                helpline = stripped.lstrip('%').lstrip()
                doc_lines.append(helpline)
            else:
                break  # Stop at first non-comment line

    # Now doc_lines contains the help block
    if not doc_lines:
        # No help available
        html_content = "<p>No help available.</p>"
    else:
        # Process help lines
        # The first line is considered the synopsis
        title_line = doc_lines[0]
        html_lines = []
        html_lines.append(f"<h1>{html.escape(title_line)}</h1>")

        # Define keywords and their corresponding HTML tags
        keywords = {
            "EXAMPLES:": "Examples",
            "EXAMPLE:": "Example",
            "SEE ALSO:": "See also",
            "CREDITS:": "Credits",
            "NOTE:": "Note",
            "NOTES:": "Notes",
            "AUTHOR:": "Author",
            "AUTHORS:": "Authors"
        }

        # Regular expression to detect keywords
        keyword_regex = re.compile(r'^(EXAMPLES?:|SEE ALSO:|CREDITS?:|NOTES?:|AUTHORS?:)', re.IGNORECASE)

        current_section = None
        section_content = []

        def flush_section():
            nonlocal current_section, section_content
            if current_section:
                if current_section.lower() == "see also":
                    # Process SEE ALSO links
                    links = []
                    for item in re.split(r'[,\s]+', ' '.join(section_content)):
                        if item in all_functions:
                            # Construct internal link
                            links.append(f'<a href="#{item}">{html.escape(item)}</a>')
                        else:
                            links.append(html.escape(item))
                    html_lines.append(f"<h2>{html.escape(current_section)}</h2>")
                    html_lines.append("<p>" + ", ".join(links) + "</p>")
                elif current_section.lower() in ["examples", "example"]:
                    html_lines.append(f"<h2>{html.escape(current_section)}</h2>")
                    # Preserve indentation and line breaks
                    html_lines.append("<pre class='code'><code class='language-matlab'>" + html.escape('\n'.join(section_content)) + "</code></pre>")
                elif current_section.lower() in ["note", "notes"]:
                    html_lines.append(f"<h2>{html.escape(current_section)}</h2>")
                    html_lines.append("<p>" + "<br/>".join(html.escape(line) for line in section_content) + "</p>")
                else:
                    html_lines.append(f"<h2>{html.escape(current_section)}</h2>")
                    html_lines.append("<p>" + "<br/>".join(html.escape(line) for line in section_content) + "</p>")
                section_content = []
            elif section_content:
                # Regular paragraph
                html_lines.append("<p>" + "<br/>".join(html.escape(line) for line in section_content) + "</p>")
                section_content = []

        # Collect all function names for linking in SEE ALSO
        all_functions = [os.path.splitext(os.path.basename(x))[0] for x in matlab_files]

        # Iterate over the help lines starting from the second line
        for line in doc_lines[1:]:
            if not line.strip():
                flush_section()
                continue
            keyword_match = keyword_regex.match(line)
            if keyword_match:
                flush_section()
                key = keyword_match.group(1).rstrip(':').capitalize()
                current_section = keywords.get(keyword_match.group(1).upper(), key)
                remainder = line[keyword_match.end():].strip()
                if remainder:
                    section_content.append(remainder)
            else:
                section_content.append(line)

        # Flush any remaining content
        flush_section()

        # Insert collapsible MATLAB code
        # Extract the MATLAB code from the file
        matlab_code = ''.join(lines)
        # Minimal Syntax Highlighting using CSS classes
        # Simple regex-based highlighting for keywords, comments, and strings
        def syntax_highlight(code):
            # Highlight comments
            code = re.sub(r'(%[^\n]*)', r'<span class="comment">\1</span>', code)
            # Highlight strings
            code = re.sub(r'(\'[^\']*\')', r'<span class="string">\1</span>', code)
            # Highlight keywords (a minimal set)
            keywords = ['function', 'end', 'if', 'else', 'elseif', 'for', 'while', 'switch', 'case', 'otherwise', 'return']
            pattern = r'\b(' + '|'.join(keywords) + r')\b'
            code = re.sub(pattern, r'<span class="keyword">\1</span>', code)
            return code

        highlighted_code = syntax_highlight(matlab_code)

        # Add collapsible section
        html_lines.append('<button class="collapsible">Show MATLAB Code</button>')
        html_lines.append('<div class="content"><pre class="code"><code class="language-matlab">' + highlighted_code + '</code></pre></div>')

        # Join all HTML lines
        html_content = "\n".join(html_lines)

    return function_name, html_content

# Extract docs from all .m files and generate HTML snippets
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Collect all function names for linking purposes
all_function_names = [os.path.splitext(os.path.basename(x))[0] for x in matlab_files]

# Create a structure (directory nav) similar to the Python version
file_structure = {}
for fpath in matlab_files:
    rel = os.path.relpath(fpath, mainfolder)
    d = os.path.dirname(rel)
    b = os.path.splitext(os.path.basename(rel))[0]
    if d not in file_structure:
        file_structure[d] = []
    file_structure[d].append(b)

# Sort directories and files
sorted_dirs = sorted(file_structure.keys())
for d in sorted_dirs:
    file_structure[d].sort()

# Generate individual HTML content for each function (hidden by default)
docs_html = ""
for fpath in matlab_files:
    function_name, html_doc = extract_matlab_doc(fpath)
    # Ensure that function_name is a valid HTML id (no spaces, special chars)
    valid_id = re.sub(r'\s+', '_', function_name)
    valid_id = re.sub(r'[^\w\-]', '', valid_id)
    # Create a div with id equal to valid_id
    docs_html += f"<div id='{html.escape(valid_id)}' class='doc-content' style='display: none;'>\n"
    docs_html += html_doc + "\n"
    docs_html += "</div>\n"

# Generate index.html
index_file = os.path.join(output_dir, output_file)
with open(index_file, "w", encoding="utf-8") as fout:
    fout.write("<!DOCTYPE html>\n<html lang='en'>\n<head>\n")
    fout.write("<meta charset='UTF-8'>\n")
    fout.write("<meta name='viewport' content='width=device-width, initial-scale=1.0'>\n")
    fout.write("<title>Pizza3 Matlab Documentation</title>\n")
    fout.write(f"<style>{CSS_STYLE}</style>\n")
    fout.write("</head>\n<body>\n")
    fout.write("<header><h1>Pizza3 Documentation</h1></header>\n")
    fout.write("<div id='content'>\n")
    fout.write("<div id='nav'>\n")
    fout.write(f"<p><strong>Version:</strong> {html.escape(PIZZA3_VERSION)}</p>\n")
    fout.write(f"<p><strong>Maintained by:</strong> {html.escape(CONTACT)}</p>\n")
    fout.write("<hr>\n")
    # Build the nav menu
    fout.write("<ul class='folder-list'>\n")
    for d in sorted_dirs:
        dirname = d if d != "." else "(root)"
        fout.write(f"<li class='folder'>\n")
        fout.write(f"<div class='folder-title' onclick='toggleFolder(this)'>{html.escape(dirname)}</div>\n")
        fout.write("<ul class='folder-content'>\n")
        for fname in file_structure[d]:
            # Ensure that fname corresponds to a valid_id
            valid_id = re.sub(r'\s+', '_', fname)
            valid_id = re.sub(r'[^\w\-]', '', valid_id)
            fout.write(f"<li class='file'><a href='#{html.escape(valid_id)}' onclick=\"loadDoc('{html.escape(valid_id)}')\">{html.escape(fname)}</a></li>\n")
        fout.write("</ul>\n</li>\n")
    fout.write("</ul>\n</div>\n")  # end nav
    fout.write("<div id='main'>\n")
    fout.write("<div id='welcome-message'>\n")
    fout.write("<h2>Welcome to Pizza3 Matlab Documentation</h2>\n")
    fout.write("<p>Select a function in the left menu to view its documentation.</p>\n")
    fout.write("<hr>\n")
    fout.write("<p><i>When no function is selected, you see this welcome page.</i></p>\n")
    # print the date
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    fout.write(f"Generated on: {formatted_datetime}")
    fout.write("</div>\n")
    # Insert all documentation content inside #main
    fout.write(docs_html)
    fout.write("</div>\n")  # end main
    fout.write("</div>\n")  # end content
    # Insert JavaScript at the end of the body
    fout.write("<script>")
    fout.write(JS_SCRIPT)
    fout.write("</script>\n")
    fout.write("</body>\n</html>")

print(f"Documentation generation completed. Output in {output_dir}")
print(f"Index created at {index_file}")
