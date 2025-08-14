import hashlib
import hmac
import time
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class DriveEncryption:
    @classmethod
    def get_current_key(cls):
        # Use current minute as entropy source
        now = int(time.time() // 60)  
        salt = b'drivenotepadprotection'
        key_material = hmac.new(salt, str(now).encode(), hashlib.sha256).digest()
        return key_material[:32]