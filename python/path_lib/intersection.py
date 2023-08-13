from pathlib import Path


def relative():
    module_file = Path(__file__)
    folder = module_file.parent
    parent = folder.parent.parent

    print(folder)
    print(parent)
    print(folder.relative_to(parent))
    print(module_file.relative_to(parent))


def list_downloads():
    download_folder = Path().home() / 'Downloads'
    download_folder = Path().home() / 'Documents'
    files = download_folder.glob('**/*.*')
    for f in files:
        print(f.relative_to(download_folder))


if __name__ == '__main__':
    # relative()
    list_downloads()