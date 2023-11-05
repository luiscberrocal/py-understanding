import json

from python_libs.settings import OUTPUT_FOLDER
from tests.python_libs.pydantic.factories import VendorFactory


def test_vendor_factory():
    vendor = VendorFactory.create()
    vendor_dict = vendor.dict()
    file = OUTPUT_FOLDER / 'vendor.json'
    with open(file, 'w') as f:
        json.dump(vendor_dict, f, indent=4)

    assert file.exists()
