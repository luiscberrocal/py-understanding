from typing import Tuple


def version_str_to_tuple(version_str: str) -> Tuple[int | str, ...]:
    version_tuple = tuple([
        int(num) if num.isdigit() else num
        for num in version_str.replace("-", ".", 1).split(".")
    ])
    return version_tuple


if __name__ == '__main__':
    versions = ['5.2.6', '5.2.7', '5.3.0a1', '5.3.0b1', '5.3.0b2', '5.3.0rc1', '5.3.0']
    for version in versions:
        print(f'{version_str_to_tuple(version)=}')
