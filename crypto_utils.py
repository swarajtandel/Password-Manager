import hashlib
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import base64

class CryptoManager:
    def __init__(self, master_password: str):
        # Derive a 32-byte key from master password via PBKDF2
        self.salt = b"fixed_salt_16_b"  # In production, use a random salt and store it
        self.key = PBKDF2(master_password, self.salt, dkLen=32, count=100000)

    def encrypt(self, plaintext: str) -> str:
        data = plaintext.encode()
        iv = get_random_bytes(16)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        pad_len = 16 - len(data) % 16
        padded = data + bytes([pad_len]) * pad_len
        ct = cipher.encrypt(padded)
        return base64.b64encode(iv + ct).decode()

    def decrypt(self, b64_ciphertext: str) -> str:
        raw = base64.b64decode(b64_ciphertext)
        iv, ct = raw[:16], raw[16:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        padded = cipher.decrypt(ct)
        pad_len = padded[-1]
        return padded[:-pad_len].decode()

    def hash_master(self) -> str:
        # Hash the derived key for master password verification
        return hashlib.sha256(self.key).hexdigest()

    def verify_master(self, master_password: str, stored_hash: str) -> bool:
        key = PBKDF2(master_password, self.salt, dkLen=32, count=100000)
        return hashlib.sha256(key).hexdigest() == stored_hash