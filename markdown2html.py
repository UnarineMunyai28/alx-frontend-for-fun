#!/usr/bin/env python3
import sys
import os
import re
import hashlib

# Check if the number of arguments is correct
if len(sys.argv) < 3:
    sys.stderr.write("Usage: ./markdown2html.py <input_file.md> <output_file.html>\n")
    sys.exit(1)

# Assign arguments to variables
input_file = sys.argv[1]
output_file = sys.argv[2]

# Check if the input file exists
if not os.path.exists(input_file):
    sys.stderr.write(f"Missing {input_file}\n")
    sys.exit(1)

# Function to convert content within [[ ]] to its MD5 hash
def convert_to_md5(text):
    return hashlib.md5(text.encode()).hexdigest()

# Function to remove 'c' or 'C' from text
def remove_c(text):
    return re.sub(r'[cC]', '', text)

# Function to replace inline styles (bold, emphasis, MD5, and removal of 'c')
def parse_inline_styles(line):
    # Bold syntax
    line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)  # **text** -> <b>text</b>
    line = re.sub(r'__(.*?)__', r'<em>\1</em>', line)    # __text__ -> <em>text</em>
    
    # MD5 hash conversion
    line = re.sub(r'\[\[(.*?)\]\]', lambda m: convert_to_md5(m.group(1)), line)  # [[text]] -> MD5 hash
    
    # Remove 'c' (case insensitive)
    line = re.sub(r'\(\((.*?)\)\)', lambda m: remove_c(m.group(1)), line)  # ((text)) -> remove 'c'
    
    return line

# Function to convert markdown to HTML
def markdown_to_html_line(line):
    # Apply inline styles first (bold, emphasis, MD5, remove 'c')
    line = parse_inline_styles(line)

    # Handle heading conversion
    heading_match = re.match(r'^(#{1,6})\s+(.*)', line)
    if heading_match:
        heading_level = len(heading_match.group(1))  # Number of # symbols
        heading_text = heading_match.group(2)        # The text after the # symbols
        return f"<h{heading_level}>{heading_text}</h{heading_level}>"

    # Handle unordered list items (- item)
    unordered_list_match = re.match(r'^-\s+(.*)', line)
    if unordered_list_match:
        list_item_text = unordered_list_match.group(1)
        return f"<li>{list_item_text}</li>"

    # Handle paragraphs (for non-empty lines not in lists)
    if line:
        return f"<p>{line}</p>"

    return line

# Process the Markdown file and write the HTML output
try:
    with open(input_file, 'r') as infile:
        with open(output_file, 'w') as outfile:
            for line in infile:
                line = line.strip()  # Remove leading/trailing whitespace
                html_line = markdown_to_html_line(line)
                outfile.write(html_line + "\n")

    sys.exit(0)  # Success
except Exception as e:
    sys.stderr.write(f"An error occurred: {str(e)}\n")
    sys.exit(1)


