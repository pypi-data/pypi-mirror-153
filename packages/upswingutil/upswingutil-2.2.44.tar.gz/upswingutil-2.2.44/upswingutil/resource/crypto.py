from cryptography.fernet import Fernet
import os
import upswingutil as ul


def generate_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)


def _load_key():
    """
    Load the previously generated key
    """
    # return open("secret.key", "rb").read()
    return os.getenv('ENCRYPTION_SECRET', ul.ENCRYPTION_SECRET)


def encrypt(message):
    """
    Encrypts a message
    """
    key = _load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    return encrypted_message


def decrypt(message):
    key = _load_key()
    f = Fernet(key)
    return f.decrypt(message).decode()


if __name__ == "__main__":
    val = encrypt("encrypt this message")
    print(decrypt(val))
