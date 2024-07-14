import json
from pathlib import Path
from typing import List, Dict, Any


def get_intents(file_path: Path) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        return json.load(file)
