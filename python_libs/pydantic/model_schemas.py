import json

from jsonschema.exceptions import ValidationError
from pydantic.schema import schema

from python_libs.pydantic.models import Vendor, Receipt, Customer, Account


def write_schemas(file: str, schemas: schema):
    with open(file, 'w') as f:
        json.dump(schemas, f, default=str)

def validate(file: str):
    # Load your JSON schema
    with open(file, 'r') as schema_file:
        schema = json.load(schema_file)

    # Your dictionary that you want to validate
    data_to_validate = {
        # ... Your dictionary data here
    }

    # Validate the data
    try:
        validate(instance=data_to_validate, schema=schema)
        print("Validation passed!")
    except ValidationError as e:
        print("Validation failed!")
        print(e)

if __name__ == '__main__':
    models_schema = schema([Vendor, Receipt, Customer, Account])

    # Export to a JSON file
    schema_json_file =  '../../tests/fixtures/models_schema.json'
    write_schemas(schema_json_file, models_schema)
