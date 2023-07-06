from pathlib import Path

import rsa


def create_or_read_keys(folder: Path, length: int = 1024):
    public_key, private_key = rsa.newkeys(length)
    public_key_file = folder / 'public.pem'
    private_key_file = folder / 'private.pem'
    if public_key_file.exists():
        with open(public_key_file, 'rb') as f:
            public_key = rsa.PublicKey.load_pkcs1(f.read())
        with open(private_key_file, 'rb') as f:
            private_key = rsa.PrivateKey.load_pkcs1(f.read())
    else:
        with open(public_key_file, 'wb') as f:
            f.write(public_key.save_pkcs1('PEM'))
        with open(private_key_file, 'wb') as f:
            f.write(private_key.save_pkcs1('PEM'))
    return public_key, private_key


if __name__ == '__main__':
    pub_key, priv_key = create_or_read_keys(Path(__file__).parent)

    original_message = 'This is a secret message. 1256'
    encrypted_message = rsa.encrypt(original_message.encode('utf-8'), pub_key=pub_key)

    clear_message = rsa.decrypt(encrypted_message, priv_key=priv_key).decode('utf-8')

    print(f'{original_message=}')
    print(f'{clear_message=}')
