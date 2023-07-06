from pathlib import Path


def add_string_to_jpeg(image: Path, text: str):
    with open(image, 'ab') as f:
        f.write(text.encode('utf-8'))


if __name__ == '__main__':
    photo = Path(__file__).parent / 'download.jpeg'
    message = 'This is hidden'
    add_string_to_jpeg(photo, message)
