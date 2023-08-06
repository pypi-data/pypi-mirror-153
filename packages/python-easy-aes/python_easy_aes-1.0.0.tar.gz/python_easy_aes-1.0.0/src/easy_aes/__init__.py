__author__ = """Aria Bagheri"""
__email__ = 'ariab9342@gmail.com'
__version__ = '1.0.0'

import base64
import hashlib
import secrets

from Crypto.Cipher import AES

BLOCK_SIZE = 16


def pad(data: bytes) -> bytes:
    return data + ((BLOCK_SIZE - len(data) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(data) % BLOCK_SIZE)).encode()


def unpad(data: bytes) -> bytes:
    return data[:-ord(data[-1:])]


def encrypt(plain_text: bytes, password: str, nist_nsa_compliant: bool = False):
    salt = secrets.token_bytes(AES.block_size)
    iv = secrets.token_bytes(AES.block_size)
    padded_text = pad(plain_text)

    pbkdf = level_8_pbkdf if nist_nsa_compliant else level_9_pbkdf
    private_key = pbkdf(password, salt)

    cipher_config = AES.new(private_key, AES.MODE_CBC, iv)
    cipher = cipher_config.encrypt(padded_text)
    return base64.b64encode(salt + cipher + iv)


def level_8_pbkdf(password: str, salt: bytes):
    return hashlib.pbkdf2_hmac("sha256", password, salt, 20000)


def level_9_pbkdf(password: str, salt: bytes):
    return hashlib.scrypt(password.encode(), salt=salt, n=16384, r=8, p=1, dklen=32)


def decrypt(cipher_text: bytes, password: str, nist_nsa_compliant: bool = False):
    cipher_text = base64.b64decode(cipher_text)
    salt = cipher_text[:AES.block_size]
    iv = cipher_text[-AES.block_size:]
    cipher_text = cipher_text[AES.block_size:-AES.block_size]

    pbkdf = level_8_pbkdf if nist_nsa_compliant else level_9_pbkdf
    private_key = pbkdf(password, salt)

    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    decrypted_text = cipher.decrypt(cipher_text)
    return unpad(decrypted_text)


def encrypt_file(input_filename: str, output_filename: str, password: str):
    with open(input_filename, "rb") as f:
        encrypted = encrypt(f.read(), password)
        with open(output_filename, "wb") as fw:
            fw.write(encrypted)


def decrypt_file(input_filename: str, output_filename: str, password: str):
    with open(input_filename, "rb") as f:
        decrypted_file = decrypt(f.read(), password)
        with open(output_filename, "wb") as fw:
            fw.write(decrypted_file)
