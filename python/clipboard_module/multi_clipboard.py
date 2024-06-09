import json
import sys

CLIPBOARD_FILE = 'clipboard.json'


def load_clipboard():
    try:
        with open(CLIPBOARD_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_clipboard(clipboard_data):
    with open(CLIPBOARD_FILE, 'w') as f:
        json.dump(clipboard_data, f)


def main(command: str):
    clipboard_data = load_clipboard()
    if command == 'list':
        for key, value in clipboard_data.items():
            print(f'Key {key}: {value}')
    elif command == 'save':
        key = input('Key: ')
        clipboard_data[key] = clipboard.paste()
        save_clipboard(clipboard_data)
    elif command == 'load':
        key = input('Key: ')
        if key in clipboard_data:
            clipboard.copy(clipboard_data[key])
        else:
            print(f'No value for {key}')
    else:
        print(f'Invalid command: {command}')


if __name__ == '__main__':
    cmd = sys.argv[1]
    main(cmd)
