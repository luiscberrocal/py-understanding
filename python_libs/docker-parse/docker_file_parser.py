from pprint import pprint
from typing import List, Dict, Any

from dockerfile_parse import DockerfileParser


def parse_docker_file(file_path) -> DockerfileParser:
    """
    Parse a Dockerfile and return a list of instructions.

    :param file_path: Path to the Dockerfile.
    :return: List of instructions.
    """
    content = None
    with open(file_path, 'r') as f:
        content = f.read()
    dfp = DockerfileParser()
    dfp.content = content
    return dfp


def main():
    file_path = 'Dockerfile'
    dfp: DockerfileParser = parse_docker_file(file_path)
    print('*' * 120)
    structure: List[Dict[str, Any]] = dfp.structure
    pprint(structure)
    print('*' * 60, 'JSON', '*' * 60)
    json_str: str = dfp.json
    pprint(json_str)
    print('*' * 120)
    pprint(dfp.labels)


if __name__ == '__main__':
    main()
