import sys
from datetime import datetime

from pathlib import Path


def format_size(size: float) -> str:
    mb = size / 1024.00 ** 2
    return f'{mb:.2f} MB'


def clean(folder: Path, glob_pattern: str, max_age: int = None):
    files = folder.glob(glob_pattern)
    files_to_delete = []
    for i, file in enumerate(files, 1):
        creation_time = file.stat().st_ctime
        age_days = (datetime.now() - datetime.fromtimestamp(creation_time)).total_seconds() / 3600.0 / 24.0
        if max_age is None:
            max_age = 1_000_000
        if age_days <= max_age:
            size = format_size(file.stat().st_size)
            content = f'{i} {file} size: {size} age: {age_days:.1f} days old'
            print(content)
            action = input('Action [D]elete, [S]top [N]one')
            if action.upper() == 'D':
                file.unlink()
            elif action.upper() == 'S':
                sys.exit()


if __name__ == '__main__':
    downloads = Path.home() / 'Downloads'
    g_pattern = '**/*.pdf'
    clean(folder=downloads, glob_pattern=g_pattern)  # , max_age=60)
