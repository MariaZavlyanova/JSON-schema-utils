import json
import sys

def generate_example_from_schema(schema, definitions=None):
    """
    Recursively generates an example JSON object based on the provided JSON schema.
    """
    if definitions is None:
        definitions = schema.get("definitions", {})

    # Handle $ref references
    if "$ref" in schema:
        ref_path = schema["$ref"].split("/")[-1]
        schema = definitions.get(ref_path, {})

    if schema.get("type") == "object":
        # Handle object type
        example = {}
        properties = schema.get("properties", {})
        for field_name, field_props in properties.items():
            example[field_name] = generate_example_from_schema(field_props, definitions)
        return example

    elif schema.get("type") == "array":
        # Handle array type
        items = schema.get("items", {})
        return [generate_example_from_schema(items, definitions)]

    else:
        # Handle primitive types
        if "example" in schema:
            return schema["example"]
        elif schema.get("type") == "string":
            return "string_example"
        elif schema.get("type") == "integer":
            return 123
        elif schema.get("type") == "number":
            return 123.45
        elif schema.get("type") == "boolean":
            return True
        else:
            return None

def generate_examples(schema_path, output_path="example_output.json"):
    """
    Generates example JSON objects based on the provided JSON schema and saves them to a file.
    """
    try:
        # Load the JSON schema
        with open(schema_path, 'r') as f:
            schema = json.load(f)
    except Exception as e:
        print(f"Error loading JSON schema: {e}")
        sys.exit(1)

    # Generate the main example
    example = generate_example_from_schema(schema)

    # Save the example to a file
    try:
        with open(output_path, 'w') as f:
            json.dump(example, f, indent=4)
        print(f"Example JSON generated: {output_path}")
    except Exception as e:
        print(f"Error saving example JSON: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_examples_from_schema.py <path_to_json_schema>")
        sys.exit(1)

    schema_path = sys.argv[1]
    output_path = "example_output.json"  # Default output file name
    generate_examples(schema_path, output_path)