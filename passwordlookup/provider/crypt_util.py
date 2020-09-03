from cryptography.fernet import Fernet


class CryptUtil:
    def __init__(self):
        pass

    def generate_key(self):
        return Fernet.generate_key()

    def write_key_to_file(self, file, key):
        with open(file, 'wb') as f:
            f.write(key)

    def read_key_from_file(self, file):
        with open(file, 'rb') as f:
            return f.read()

    def encrypt_str(self, message, key):
        f = Fernet(key)
        encrypted = f.encrypt(message.encode())
        return encrypted

    def decrypt_bytes(self, bytes, key):
        f = Fernet(key)
        decrypted = f.decrypt(bytes)
        return decrypted.decode()
