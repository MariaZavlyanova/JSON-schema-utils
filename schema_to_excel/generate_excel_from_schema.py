import json
import sys
import pandas as pd
from openpyxl import Workbook

def generate_excel_from_schema(schema_path, output_path="schema_output.xlsx"):
    try:
        # Load the JSON schema
        with open(schema_path, 'r') as f:
            schema = json.load(f)
    except Exception as e:
        print(f"Error loading JSON schema: {e}")
        sys.exit(1)

    # Create a new Excel workbook
    writer = pd.ExcelWriter(output_path, engine='openpyxl')

    # Function to process an object and create a DataFrame
    def process_object(object_name, object_data):
        rows = []
        properties = object_data.get("properties", {})
        if not properties:
            print(f"No properties found for object: {object_name}")
        for field_name, field_props in properties.items():
            row = {
                "Field Name": field_name,
                "Type": field_props.get("type", ""),
                "Format": field_props.get("format", ""),
                "Description": field_props.get("description", ""),
                "Example": field_props.get("example", ""),
                "Enum": ", ".join(field_props.get("enum", [])) if "enum" in field_props else "",
                "$ref:": ""  # New column for $ref
            }

            # Handle $ref for fields with no "type"
            if "type" not in field_props and "$ref" in field_props:
                row["$ref:"] = field_props["$ref"]

            # Handle arrays with $ref
            if row["Type"] == "array" and "items" in field_props:
                items = field_props["items"]
                if "$ref" in items:
                    row["$ref:"] = items["$ref"]

            rows.append(row)
        return pd.DataFrame(rows)

    try:
        # Process the main schema object
        main_sheet = process_object(schema.get("title", "Main"), schema)
        main_sheet.to_excel(writer, sheet_name=schema.get("title", "Main"), index=False)

        # Process definitions
        definitions = schema.get("definitions", {})
        for definition_name, definition_data in definitions.items():
            sheet = process_object(definition_name, definition_data)
            sheet.to_excel(writer, sheet_name=definition_name, index=False)

        # Save the Excel file
        writer.close()
        print(f"Excel file generated: {output_path}")
    except Exception as e:
        print(f"Error generating Excel file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_excel_from_schema.py <path_to_json_schema>")
        sys.exit(1)

    schema_path = sys.argv[1]
    output_path = "schema_output.xlsx"  # Default output file name
    generate_excel_from_schema(schema_path, output_path)