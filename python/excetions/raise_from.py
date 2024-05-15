def do_with_raise_from():
    try:
        filename = 'xx'
        # some operation that may raise an IOError
        with open(filename, 'r') as f:
            content = f.read()
        print(content)
    except IOError as e:
        raise RuntimeError('Failed to open file') from e


def do_without_raise_from():
    try:
        filename = 'xx'
        # some operation that may raise an IOError
        with open(filename, 'r') as f:
            content = f.read()
        print(content)
    except IOError:
        raise RuntimeError('Failed to open file')


if __name__ == '__main__':
    try:
        do_with_raise_from()
    except Exception as e:
        print(f'Caught exception: {e}')
        print(f'Original cause: {e.__cause__}')
        print(f'Original cause type: {type(e.__cause__)}')
        print(f'Original cause message: {e.__cause__.args[0]}')
    try:
        do_without_raise_from()
    except Exception as e:
        print(f'Caught exception: {e}')
        print(f'Original cause: {e.__cause__}')
        print(f'Original cause type: {type(e.__cause__)}')
