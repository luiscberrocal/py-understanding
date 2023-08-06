from datetime import datetime
from pathlib import Path


def clean(folder: Path, glob_pattern: str):
    files = folder.glob(glob_pattern)
    files_to_delete = []
    for i, file in enumerate(files, 1):
        creation_time = file.stat().st_ctime
        creation_date = datetime.fromtimestamp(creation_time)
        size = file.stat().st_size
        content = f'{i} {file} size: {size:.2f} creation: {creation_date}'
        print(content)
        delete_file = input('Delete?')
        if delete_file.upper() == 'Y':
            file.unlink()


if __name__ == '__main__':
    downloads = Path.home() / 'Downloads'
    g_pattern = '**/*.csv'
    clean(folder=downloads, glob_pattern=g_pattern)

