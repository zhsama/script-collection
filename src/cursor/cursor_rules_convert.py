#!/usr/bin/env python3
import os
import re
import sys


def extract_rule_parts(rule_text):
    """Extract name, description, globs and content from a rule text."""
    # Extract name using regex
    name_match = re.search(r'name:\s*(.*?)\.mdc', rule_text, re.DOTALL)
    if not name_match:
        return None

    name = name_match.group(1).strip()

    # Extract description
    desc_match = re.search(r'description:\s*(.*?)(?:\n|$)', rule_text, re.DOTALL)
    description = desc_match.group(1).strip() if desc_match else ""

    # Extract globs
    globs_match = re.search(r'globs:\s*(.*?)(?:\n|$)', rule_text, re.DOTALL)
    globs = globs_match.group(1).strip() if globs_match else ""

    # Extract content (everything after the header patterns)
    content_parts = rule_text.split("\n\n", 1)
    content = content_parts[1].strip() if len(content_parts) > 1 else ""
    
    # Clean content by removing name, description, and globs lines
    # but preserving them inside frontmatter
    cleaned_content = ""
    in_frontmatter = False
    
    for line in content.split('\n'):
        # Check if we're entering frontmatter
        if line.strip() == "---":
            in_frontmatter = not in_frontmatter
            cleaned_content += line + "\n"
            continue
            
        # If we're in frontmatter, keep all lines
        if in_frontmatter:
            cleaned_content += line + "\n"
        # If we're outside frontmatter, filter out metadata lines
        elif not re.match(r'^\s*(name|description|globs):', line, re.IGNORECASE):
            cleaned_content += line + "\n"
    
    return {
        "name": name,
        "description": description,
        "globs": globs,
        "content": cleaned_content.strip()
    }


def format_mdc_file(rule_parts):
    """Format the rule parts into a valid .mdc file content."""
    if not rule_parts:
        return None

    mdc_content = f"""---
description: {rule_parts['description']}
globs: {rule_parts['globs']}
---

{rule_parts['content']}
"""
    return mdc_content


def save_to_file(name, content, output_dir="."):
    """Save the content to a file in the specified directory."""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Create file path
    file_path = os.path.join(output_dir, f"{name}.mdc")

    # Write content to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return file_path


def process_rules_file(input_file, output_dir="."):
    """Process the input file and create individual .mdc files."""
    # Read input file
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Split by section divider
    rules = content.split("---")

    # Process each rule
    created_files = []
    for rule in rules:
        if not rule.strip():
            continue

        rule_parts = extract_rule_parts(rule)
        if not rule_parts:
            print(f"Warning: Could not extract rule parts from:\n{rule}")
            continue

        mdc_content = format_mdc_file(rule_parts)
        if not mdc_content:
            continue

        file_path = save_to_file(rule_parts["name"], mdc_content, output_dir)
        created_files.append(file_path)
        print(f"Created: {file_path}")

    return created_files


def main():
    """Main function to run the script."""
    input_file = input("Please enter the input file path: ").strip()
    output_dir = input("Please enter the output directory path (default: mdc_rules): ").strip()
    
    # Use default output directory if user input is empty
    if not output_dir:
        output_dir = "mdc_rules"

    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)

    print(f"Processing {input_file}...")
    created_files = process_rules_file(input_file, output_dir)
    print(f"Successfully created {len(created_files)} .mdc files in '{output_dir}'.")


if __name__ == "__main__":
    main()
