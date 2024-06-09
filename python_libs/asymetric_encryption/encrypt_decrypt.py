from io import StringIO
from pathlib import Path
from typing import Tuple

import rsa
from dotenv import load_dotenv

from .exceptions import EncryptionError


def create_or_read_keys(
        *, private_folder: Path, public_folder: Path, length: int = 1024, key_file_prefix: str = ""
) -> Tuple[rsa.PublicKey, rsa.PrivateKey, bool]:
    """Create or read the public and private keys for encryption and decryption.

    Args:
        private_folder: Folder to store or read private key.
        public_folder: Folder to store or read public key.
        length: Length of the keys. The longer the key, the more secure the encryption but slower to generate.
        key_file_prefix: Prefix for the key files.
    """
    file_prefix = "" if not key_file_prefix else f"{key_file_prefix}_"
    public_key, private_key = rsa.newkeys(length)
    public_key_file = public_folder / f"{file_prefix}public.pem"
    private_key_file = private_folder / f"{file_prefix}private.pem"
    created = False
    if public_key_file.exists() and private_key_file.exists():
        with open(public_key_file, "rb") as f:
            public_key = rsa.PublicKey.load_pkcs1(f.read())
        with open(private_key_file, "rb") as f:
            private_key = rsa.PrivateKey.load_pkcs1(f.read())
    elif not public_key_file.exists() and not private_key_file.exists():
        created = True
        with open(public_key_file, "wb") as f:
            f.write(public_key.save_pkcs1("PEM"))
        with open(private_key_file, "wb") as f:
            f.write(private_key.save_pkcs1("PEM"))
    else:
        raise EncryptionError(f"Public and private keys must be created or read together. "
                              f"{public_key_file=} {private_key_file=}")
    return public_key, private_key, created


def encrypt_environment_file(*, source_file: Path, public_key: rsa.PublicKey) -> Path:
    """Encrypt the environment file.

    Args:
        source_file: File to encrypt.
        public_key: Public key to encrypt the file.

    Returns: Encrypted file.
    """
    encrypted_file = source_file.with_suffix(".enc")
    if encrypted_file.exists():
        raise EncryptionError(f"The file {encrypted_file} already exists.")
    with open(source_file) as f:
        data = f.read()
    data_bytes = data.encode("utf-8")
    encrypted_data = rsa.encrypt(data_bytes, pub_key=public_key)
    encrypted_file = source_file.with_suffix(".enc")
    with open(encrypted_file, "wb") as f:
        f.write(encrypted_data)
    return encrypted_file


def decrypt_environment_file(*, source_file: Path, private_key: rsa.PrivateKey) -> str:
    """Decrypt the environment file.

    Args:
        source_file: File to decrypt.
        private_key: Private key to decrypt the file.

    Returns: File content.
    """
    with open(source_file, "rb") as f:
        data = f.read()
    return rsa.decrypt(data, priv_key=private_key).decode("utf-8")


def load_encrypted_environment_file(*, source_file: Path, private_key: rsa.PrivateKey) -> None:
    """
    Load the encrypted environment file to environment variables.
    Args:
        source_file: Encrypted file.
        private_key: Private key to decrypt the file.
    """
    # https://pypi.org/project/python-dotenv/#load-configuration-without-altering-the-environment
    content = decrypt_environment_file(source_file=source_file, private_key=private_key)
    config = StringIO(content)
    load_dotenv(stream=config)
