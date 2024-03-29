import json

from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate
from pydantic.schema import schema

from python_libs.pydantic.models import Vendor, Receipt, Customer, Account


def write_schemas(file: str, schemas: schema):
    with open(file, 'w') as f:
        json.dump(schemas, f, default=str)

def validate_file(file: str):
    # Load your JSON schema
    with open(file, 'r') as schema_file:
        schema = json.load(schema_file)

    # Your dictionary that you want to validate
    data_to_validate = {
        "name": "Martinez-Davis",
        "national_id": "041-96-9376",
        "verification_digit": "68",
        "vendor_type": "COMPANY"
    }
    # Validate the data
    try:
        validate(instance=data_to_validate, schema=schema)
        print("Validation passed!")
    except ValidationError as e:
        print("Validation failed!")
        print(e)
        raise e

if __name__ == '__main__':
    models_schema = schema([Vendor, Receipt, Customer, Account])

    # Export to a JSON file
    schema_json_file =  '../../tests/fixtures/models_schema.json'
    # write_schemas(schema_json_file, models_schema)
    validate_file(schema_json_file)
