import zipfile
from pathlib import Path


def unzip_all(zip_file: Path, target_folder: Path, password: str):
    # How to Extract Files from a Password Protected Zip File

    with zipfile.ZipFile(zip_file, 'r') as zip:
        zip.extractall(target_folder, pwd=password.encode('utf-8'))


def unzip_file(zip_file: Path, target_folder: Path, password: str):
    with zipfile.ZipFile(zip_file, 'r') as zip:
        files = zip.namelist()
        for file in files:
            zip.extract(file, target_folder, pwd=password.encode('utf-8'))
    return files


if __name__ == '__main__':
    output_folder = Path(__file__).parent.parent.parent / 'output'
    # zip -P pass123 ccat-command.zip ./davinci_resolve/*.*
    z_file = Path('compressed_folder_pwd.zip')
    pwd = 'pass123'
    # unzip_file(zip_file=z_file, target_folder=output_folder, password=pwd)
    unzipped_files = unzip_file(zip_file=z_file, target_folder=output_folder, password=pwd)
    print(unzipped_files)