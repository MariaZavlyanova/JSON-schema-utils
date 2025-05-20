import json
import sys

def infer_type(value):
    """
    Infers the JSON Schema type of a given value.
    """
    if isinstance(value, dict):
        return "object"
    elif isinstance(value, list):
        return "array"
    elif isinstance(value, str):
        return "string"
    elif isinstance(value, int):
        return "integer"
    elif isinstance(value, float):
        return "number"
    elif isinstance(value, bool):
        return "boolean"
    elif value is None:
        return "null"
    else:
        return "string"

def generate_schema_from_example(example, definitions=None, path="Root"):
    """
    Recursively generates a JSON schema from a given example JSON object.
    """
    if definitions is None:
        definitions = {}

    schema = {"type": infer_type(example)}

    if schema["type"] == "object":
        schema["properties"] = {}
        for key, value in example.items():
            nested_path = f"{path}.{key}"
            if isinstance(value, dict):
                # Handle nested objects with $ref
                ref_name = key.capitalize()
                definitions[ref_name] = generate_schema_from_example(value, definitions, nested_path)
                schema["properties"][key] = {"$ref": f"#/definitions/{ref_name}"}
            else:
                schema["properties"][key] = generate_schema_from_example(value, definitions, nested_path)
                schema["properties"][key]["description"] = f"Description for {key}"
                schema["properties"][key]["example"] = value

    elif schema["type"] == "array":
        if len(example) > 0:
            schema["items"] = generate_schema_from_example(example[0], definitions, f"{path}[]")
        else:
            schema["items"] = {"type": "string"}  # Default type for empty arrays

    else:
        # Add example and description for primitive types
        schema["description"] = f"Description for {path}"
        schema["example"] = example

    return schema

def generate_full_schema(example_path, output_path="schema_output.json"):
    """
    Generates a JSON schema from a given example JSON file and saves it to a file.
    """
    try:
        # Load the example JSON
        with open(example_path, 'r') as f:
            example = json.load(f)
    except Exception as e:
        print(f"Error loading JSON example: {e}")
        sys.exit(1)

    # Generate the schema
    definitions = {}
    schema = generate_schema_from_example(example, definitions)
    schema["$schema"] = "http://json-schema.org/draft-07/schema#"
    schema["title"] = "Generated Schema"
    schema["type"] = "object"
    schema["definitions"] = definitions

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
        print("Usage: python generate_schema_from_example.py <path_to_json_example>")
        sys.exit(1)

    example_path = sys.argv[1]
    output_path = "schema_output.json"  # Default output file name
    generate_full_schema(example_path, output_path)