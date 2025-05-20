# Schema & Example Automation Utilities

This repository provides four Python scripts to automate the conversion between JSON Schema, example JSON, and Excel documentation. These tools help you maintain, document, and test your data models efficiently.

---

## Scripts Overview

### 1. `generate_schema_from_example.py`
**Purpose:**  
Generate a JSON Schema from a sample/example JSON file.

**Usage:**  
```bash
python generate_schema_from_example.py path/to/example.json

### 2. `generate_schema_from_excel.py
**Purpose:**  
Generate a JSON Schema from an Excel file where each sheet describes an object and each row describes a field.

**Usage:**  
```bash
python generate_schema_from_excel.py path/to/schema.xlsx

Input: Excel file (one sheet per object, columns: Field Name, Type, Format, Description, Example, Enum, $ref:).
Output: JSON Schema (schema_output.json).

### 3. generate_example_from_schema.py
Purpose:
Generate an example JSON file from a JSON Schema.

Usage:

Input: JSON Schema file.
Output: Example JSON (example_output.json).

### 4. generate_excel_from_schema.py
Purpose:
Generate an Excel documentation file from a JSON Schema.

Usage:

Input: JSON Schema file.
Output: Excel file (schema_output.xlsx).

### Excel Format
When using Excel as input or output, the following columns are supported:

- Field Name
- Type
- Format
- Description
- Example
- Enum
- $ref: (for references to definitions or nested objects)

### Requirements
- Python 3.7+
- Install dependencies:

pip install pandas openpyxl

### Notes
- All scripts print errors and usage instructions if called incorrectly.
- $ref: columns in Excel are used for referencing definitions or nested objects in JSON Schema.
- Array fields with $ref: are handled as arrays of referenced objects.

### License

MIT License

### Author
Your Maria Zavlyanova