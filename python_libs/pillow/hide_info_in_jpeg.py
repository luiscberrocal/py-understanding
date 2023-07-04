from pathlib import Path


def add_string_to_jpeg(image: Path, text: str):
    with open(image, 'ab') as f:
        f.write(text.encode('utf-8'))




