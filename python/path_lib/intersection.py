from pathlib import Path


def relative():
    module_file = Path(__file__)
    folder = module_file.parent
    parent = folder.parent.parent

    print(folder)
    print(parent)
    print(folder.relative_to(parent))
    print(module_file.relative_to(parent))


if __name__ == '__main__':
    relative()
