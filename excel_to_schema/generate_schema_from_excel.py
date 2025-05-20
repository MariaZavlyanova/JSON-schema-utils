import json
import sys
import pandas as pd

def generate_schema_from_excel(excel_path, output_path="schema_output.json"):
    """
    Generates a JSON schema from an Excel file where each sheet represents an object.
    """
    try:
        # Load the Excel file
        excel_data = pd.ExcelFile(excel_path)
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        sys.exit(1)

    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Generated Schema",
        "type": "object",
        "properties": {},
        "definitions": {}
    }

    # Process each sheet in the Excel file
    for sheet_name in excel_data.sheet_names:
        df = excel_data.parse(sheet_name)
        if "Field Name" not in df.columns:
            print(f"Skipping sheet '{sheet_name}' as it does not contain a 'Field Name' column.")
            continue

        # Generate schema for the current sheet
        object_schema = {"type": "object", "properties": {}}
        for _, row in df.iterrows():
            field_name = row["Field Name"]
            field_type = row.get("Type", "string")
            field_format = row.get("Format", None)
            field_description = row.get("Description", "")
            field_example = row.get("Example", None)
            field_ref = row.get("$ref:", None)

            # If $ref: column is present and not empty
            if pd.notna(field_ref) and str(field_ref).strip():
                if field_type == "array":
                    field_schema = {
                        "type": "array",
                        "items": {"$ref": str(field_ref).strip()}
                    }
                else:
                    field_schema = {"$ref": str(field_ref).strip()}
            else:
                field_schema = {"type": field_type}
                if pd.notna(field_format):
                    field_schema["format"] = field_format
                if pd.notna(field_description):
                    field_schema["description"] = field_description
                if pd.notna(field_example):
                    field_schema["example"] = field_example

            object_schema["properties"][field_name] = field_schema

        # Add the object schema to definitions or main properties
        if sheet_name == schema["title"]:
            schema["properties"] = object_schema["properties"]
        else:
            schema["definitions"][sheet_name] = object_schema
            schema["properties"][sheet_name] = {"$ref": f"#/definitions/{sheet_name}"}

    # Save the schema to a file
    try:
        with open(output_path, 'w') as f:
            json.dump(schema, f, indent=4)
        print(f"JSON schema generated: {output_path}")
    except Exception as e:
        print(f"Error saving JSON schema: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_schema_from_excel.py <path_to_excel_file>")
        sys.exit(1)

    excel_path = sys.argv[1]
    output_path = "schema_output.json"  # Default output file name
    generate_schema_from_excel(excel_path, output_path)