

# Why you should not use RSA to encrypt files

RSA PKCS#1 encryption is limited to ((KeySize/8) - 11) bytes of payload. Based on your numbers you are using 
RSA-512 (which is “too easy” to break, you should really be using 1024 or 2048-bit RSA).

The most common use for RSA encryption is to encrypt an AES key, and then send the encrypted AES key plus 
the AES-encrypted message: a scheme known as hybrid encryption. Since AES keys are small (16, 24, or 32 bytes) even 
small RSA can transport them.

https://stackoverflow.com/questions/57844204/how-to-encrypt-message-longer-than-53-bytes-using-rsa-encryption

This tests proves it a file with just 4 environment variables is too big to be encrypted with RSA-512.

```python
def test_encrypt_env_file_too_big(tmp_path, dummy_env_file, dummy_env_variables):
    public_key, private_key, _ = create_or_read_keys(private_folder=tmp_path, public_folder=tmp_path, length=515)
    with pytest.raises(OverflowError):
        encrypt_environment_file(source_file=dummy_env_file, public_key=public_key)

```