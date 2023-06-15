from typing import Tuple, Optional


def version_str_to_tuple(version_str: str) -> tuple[int | str, ...]:
    version_tuple = tuple([
            int(num) if num.isdigit() else num
            for num in version_str.replace("-", ".", 1).split(".")
        ])
    return version_tuple




