from pydantic.schema import schema

from python_libs.pydantic.models import Vendor, Receipt, Customer, Account

if __name__ == '__main__':
    models_schema = schema([Vendor, Receipt, Customer, Account])

    # Export to a JSON file
    with open('models_schema.json', 'w') as f:
        f.write(models_schema.json())