import json
from _decimal import Decimal
from datetime import datetime
from typing import Dict, Any


def str_to_json_dict(data: str) -> Dict[str, Any]:
    data_dict = json.loads(data)
    return data_dict


def dict_to_str(data: Dict[str, Any]) -> str:
    data_str = json.dumps(data)
    return data_str


def dict_to_str_unserializable(data: Dict[str, Any]) -> str:
    """This function will coerce any non-serializable value to string."""
    data_str = json.dumps(data, default=str)
    return data_str


if __name__ == '__main__':
    # d = str_to_json_dict('Bla')
    # d = dict_to_str({'d': 3, 't': datetime.now()})
    d = dict_to_str_unserializable({'d': 5, 't': datetime.now(), 'value': Decimal('152.52')})
    print(d)
