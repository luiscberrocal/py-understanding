import json
from typing import Dict, Any
from datetime import datetime

def str_to_json_dict(data: str) -> Dict[str, Any]:
    data_dict = json.loads(data)
    return data_dict

def dict_to_str(data: Dict[str, Any]) -> str:
    data_str = json.dumps(data)
    return data_str


if __name__ == '__main__':
    # d = str_to_json_dict('Bla')
    d = dict_to_str({'d': 3, 't': datetime.now()})
    print(d)