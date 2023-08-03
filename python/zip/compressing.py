import zipfile
from pathlib import Path


def unzip_all(zip_file: Path, target_folder: Path, password: str):
    # How to Extract Files from a Password Protected Zip File

    with zipfile.ZipFile(zip_file, 'r') as zip:
        zip.extractall(target_folder, pwd=password.encode('utf-8'))


def unzip_file(zip_file: Path, target_folder: Path, password: str):
    with zipfile.ZipFile(zip_file, 'r') as zf:
        files = zf.namelist()
        for file in files:
            zf.extract(file, target_folder, pwd=password.encode('utf-8'))
    return files


def zip_folder(zip_file: Path, folder: Path, password: str):
    files = folder.glob('**/*.*')
    zipped_files = []
    with zipfile.ZipFile(zip_file, 'w') as zf:
        if password is not None:
            zf.setpassword(password.encode('utf-8'))
        for file in files:
            file_path = folder / file
            zipped_files.append(file_path)
            zf.write(file_path)
    return zipped_files


if __name__ == '__main__':
    # https://datagy.io/python-zip-unzip-files/#:~:text=In%20order%20to%20extract%20all,members%20of%20the%20zip%20file.&text=In%20the%20example%20above%2C%20we%20can%20see%20how%20simple%20it,files%20from%20a%20zip%20file.
    # obsidian://open?vault=django-blog&file=Zipping%20a%20file%20with%20password

    output_folder = Path(__file__).parent.parent.parent / 'outpout'
    # zip -P pass123 ccat-command.zip ./davinci_resolve/*.*
    z_file = Path('compressed_folder_pwd.zip')
    pwd = 'pass123'
    # unzip_file(zip_file=z_file, target_folder=output_folder, password=pwd)
    # unzipped_files = unzip_file(zip_file=z_file, target_folder=output_folder, password=pwd)
    # print(unzipped_files)

    new_zip = output_folder / 'test.zip'
    folder_to_zip = Path(__file__).parent.parent / 'json'
    files_zipped = zip_folder(zip_file=new_zip, folder=folder_to_zip, password=pwd)
    print(files_zipped)
