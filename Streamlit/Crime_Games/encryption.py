import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

def hash_key(input_key: bytes, hash_algo='sha256') -> bytes:
    """Hash the input key using the specified hash algorithm."""
    hash_func = getattr(hashlib, hash_algo)()
    hash_func.update(input_key)
    return hash_func.digest()

def encrypt_ecb(plaintext: str, key: bytes) -> str:
    cipher = AES.new(key, AES.MODE_ECB)
    padded_plaintext = pad(plaintext.encode(), AES.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)
    return base64.b64encode(ciphertext).decode()

def decrypt_ecb(ciphertext: str, key: bytes) -> str:
    cipher = AES.new(key, AES.MODE_ECB)
    decoded_ciphertext = base64.b64decode(ciphertext)
    padded_plaintext = cipher.decrypt(decoded_ciphertext)
    plaintext = unpad(padded_plaintext, AES.block_size)
    return plaintext.decode()