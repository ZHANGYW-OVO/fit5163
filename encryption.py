import os
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

KEY_FILE = "key.bin"

def generate_key():
    return os.urandom(32)

def save_key(key):
    with open(KEY_FILE, 'wb') as f:
        f.write(key)

def load_key():
    with open(KEY_FILE, 'rb') as f:
        return f.read()

def initialize_key():
    if not os.path.exists(KEY_FILE):
        key = generate_key()
        save_key(key)
        print("✅ New encryption key generated and saved.")
    else:
        print("✅ Encryption key loaded.")

def encrypt_data(key, data):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    plaintext = json.dumps(data).encode('utf-8')
    pad_len = 16 - len(plaintext) % 16
    padded_plaintext = plaintext + bytes([pad_len] * pad_len)

    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    return {"iv": iv.hex(), "ciphertext": ciphertext.hex()}

def decrypt_data(key, encrypted_record):
    iv = bytes.fromhex(encrypted_record["iv"])
    ciphertext = bytes.fromhex(encrypted_record["ciphertext"])

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    pad_len = padded_plaintext[-1]
    plaintext = padded_plaintext[:-pad_len]
    return json.loads(plaintext.decode('utf-8'))