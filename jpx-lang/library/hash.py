"""
Modul Hash untuk JPX
Menyediakan fungsi encoding, decoding, dan hashing
"""

import base64
import hashlib
import binascii
import json

class Hash:
    def __init__(self):
        pass
    
    # ========== BASE64 ==========
    def base64_encode(self, data):
        """
        Encode data ke Base64
        Contoh: hash.base64_encode("Hello World") -> "SGVsbG8gV29ybGQ="
        """
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = str(data).encode('utf-8')
            return base64.b64encode(data_bytes).decode('utf-8')
        except Exception as e:
            return f"<error: {e}>"
    
    def base64_decode(self, data):
        """
        Decode data dari Base64
        Contoh: hash.base64_decode("SGVsbG8gV29ybGQ=") -> "Hello World"
        """
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = str(data).encode('utf-8')
            return base64.b64decode(data_bytes).decode('utf-8')
        except Exception as e:
            return f"<error: {e}>"
    
    def base64url_encode(self, data):
        """
        Encode data ke Base64URL (aman untuk URL)
        Contoh: hash.base64url_encode("Hello World") -> "SGVsbG8gV29ybGQ="
        """
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = str(data).encode('utf-8')
            return base64.urlsafe_b64encode(data_bytes).decode('utf-8')
        except Exception as e:
            return f"<error: {e}>"
    
    def base64url_decode(self, data):
        """
        Decode data dari Base64URL
        Contoh: hash.base64url_decode("SGVsbG8gV29ybGQ=") -> "Hello World"
        """
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = str(data).encode('utf-8')
            return base64.urlsafe_b64decode(data_bytes).decode('utf-8')
        except Exception as e:
            return f"<error: {e}>"
    
    # ========== BASE32 ==========
    def base32_encode(self, data):
        """
        Encode data ke Base32
        Contoh: hash.base32_encode("Hello World") -> "JBSWY3DPEBLW64TMMQQQ===="
        """
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = str(data).encode('utf-8')
            return base64.b32encode(data_bytes).decode('utf-8')
        except Exception as e:
            return f"<error: {e}>"
    
    def base32_decode(self, data):
        """
        Decode data dari Base32
        Contoh: hash.base32_decode("JBSWY3DPEBLW64TMMQQQ====") -> "Hello World"
        """
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = str(data).encode('utf-8')
            return base64.b32decode(data_bytes).decode('utf-8')
        except Exception as e:
            return f"<error: {e}>"
    
    # ========== BASE16 (HEX) ==========
    def base16_encode(self, data):
        """
        Encode data ke Base16 (Hex)
        Contoh: hash.base16_encode("Hello World") -> "48656C6C6F20576F726C64"
        """
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = str(data).encode('utf-8')
            return binascii.hexlify(data_bytes).decode('utf-8')
        except Exception as e:
            return f"<error: {e}>"
    
    def base16_decode(self, data):
        """
        Decode data dari Base16 (Hex)
        Contoh: hash.base16_decode("48656C6C6F20576F726C64") -> "Hello World"
        """
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = str(data).encode('utf-8')
            return binascii.unhexlify(data_bytes).decode('utf-8')
        except Exception as e:
            return f"<error: {e}>"
    
    # ========== BASE85 (ASCII85) ==========
    def base85_encode(self, data):
        """
        Encode data ke Base85
        Contoh: hash.base85_encode("Hello World") -> "87cURD]j7D0c"
        """
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = str(data).encode('utf-8')
            return base64.b85encode(data_bytes).decode('utf-8')
        except Exception as e:
            return f"<error: {e}>"
    
    def base85_decode(self, data):
        """
        Decode data dari Base85
        Contoh: hash.base85_decode("87cURD]j7D0c") -> "Hello World"
        """
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = str(data).encode('utf-8')
            return base64.b85decode(data_bytes).decode('utf-8')
        except Exception as e:
            return f"<error: {e}>"
    
    # ========== MD5 HASH ==========
    def md5(self, data):
        """
        Hash MD5 (32 karakter hex)
        Contoh: hash.md5("Hello World") -> "b10a8db164e0754105b7a99be72e3fe5"
        """
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = str(data).encode('utf-8')
            return hashlib.md5(data_bytes).hexdigest()
        except Exception as e:
            return f"<error: {e}>"
    
    def md5_bytes(self, data):
        """
        Hash MD5 dalam format bytes
        """
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = str(data).encode('utf-8')
            return hashlib.md5(data_bytes).digest()
        except Exception as e:
            return f"<error: {e}>"
    
    # ========== SHA FAMILY ==========
    def sha1(self, data):
        """
        Hash SHA-1 (40 karakter hex)
        Contoh: hash.sha1("Hello World") -> "0a4d55a8d778e5022fab701977c5d840bbc486d0"
        """
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = str(data).encode('utf-8')
            return hashlib.sha1(data_bytes).hexdigest()
        except Exception as e:
            return f"<error: {e}>"
    
    def sha224(self, data):
        """
        Hash SHA-224 (56 karakter hex)
        """
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = str(data).encode('utf-8')
            return hashlib.sha224(data_bytes).hexdigest()
        except Exception as e:
            return f"<error: {e}>"
    
    def sha256(self, data):
        """
        Hash SHA-256 (64 karakter hex)
        Contoh: hash.sha256("Hello World") -> "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e"
        """
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = str(data).encode('utf-8')
            return hashlib.sha256(data_bytes).hexdigest()
        except Exception as e:
            return f"<error: {e}>"
    
    def sha384(self, data):
        """
        Hash SHA-384 (96 karakter hex)
        """
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = str(data).encode('utf-8')
            return hashlib.sha384(data_bytes).hexdigest()
        except Exception as e:
            return f"<error: {e}>"
    
    def sha512(self, data):
        """
        Hash SHA-512 (128 karakter hex)
        """
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = str(data).encode('utf-8')
            return hashlib.sha512(data_bytes).hexdigest()
        except Exception as e:
            return f"<error: {e}>"
    
    def sha3_224(self, data):
        """
        Hash SHA3-224
        """
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = str(data).encode('utf-8')
            return hashlib.sha3_224(data_bytes).hexdigest()
        except Exception as e:
            return f"<error: {e}>"
    
    def sha3_256(self, data):
        """
        Hash SHA3-256
        """
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = str(data).encode('utf-8')
            return hashlib.sha3_256(data_bytes).hexdigest()
        except Exception as e:
            return f"<error: {e}>"
    
    def sha3_384(self, data):
        """
        Hash SHA3-384
        """
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = str(data).encode('utf-8')
            return hashlib.sha3_384(data_bytes).hexdigest()
        except Exception as e:
            return f"<error: {e}>"
    
    def sha3_512(self, data):
        """
        Hash SHA3-512
        """
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = str(data).encode('utf-8')
            return hashlib.sha3_512(data_bytes).hexdigest()
        except Exception as e:
            return f"<error: {e}>"
    
    # ========== BLAKE2 ==========
    def blake2b(self, data, digest_size=64):
        """
        Hash BLAKE2b (max 64 bytes)
        """
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = str(data).encode('utf-8')
            return hashlib.blake2b(data_bytes, digest_size=digest_size).hexdigest()
        except Exception as e:
            return f"<error: {e}>"
    
    def blake2s(self, data, digest_size=32):
        """
        Hash BLAKE2s (max 32 bytes)
        """
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = str(data).encode('utf-8')
            return hashlib.blake2s(data_bytes, digest_size=digest_size).hexdigest()
        except Exception as e:
            return f"<error: {e}>"
    
    # ========== CRC / HASH LAINNYA ==========
    def crc32(self, data):
        """
        CRC32 checksum (integer)
        """
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = str(data).encode('utf-8')
            return binascii.crc32(data_bytes)
        except Exception as e:
            return f"<error: {e}>"
    
    def adler32(self, data):
        """
        Adler32 checksum (integer)
        """
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = str(data).encode('utf-8')
            return binascii.adler32(data_bytes)
        except Exception as e:
            return f"<error: {e}>"
    
    # ========== HMAC (Hash-based Message Authentication Code) ==========
    def hmac_md5(self, key, message):
        """
        HMAC dengan MD5
        """
        try:
            import hmac
            if isinstance(key, str):
                key_bytes = key.encode('utf-8')
            else:
                key_bytes = str(key).encode('utf-8')
            if isinstance(message, str):
                msg_bytes = message.encode('utf-8')
            else:
                msg_bytes = str(message).encode('utf-8')
            return hmac.new(key_bytes, msg_bytes, hashlib.md5).hexdigest()
        except Exception as e:
            return f"<error: {e}>"
    
    def hmac_sha256(self, key, message):
        """
        HMAC dengan SHA256
        """
        try:
            import hmac
            if isinstance(key, str):
                key_bytes = key.encode('utf-8')
            else:
                key_bytes = str(key).encode('utf-8')
            if isinstance(message, str):
                msg_bytes = message.encode('utf-8')
            else:
                msg_bytes = str(message).encode('utf-8')
            return hmac.new(key_bytes, msg_bytes, hashlib.sha256).hexdigest()
        except Exception as e:
            return f"<error: {e}>"
    
    # ========== UTILITY FUNCTIONS ==========
    def hash_file(self, filename, algorithm="sha256"):
        """
        Hash file dengan algoritma tertentu
        """
        try:
            hash_func = getattr(hashlib, algorithm, None)
            if not hash_func:
                return f"<error: Unknown algorithm {algorithm}>"
            
            h = hash_func()
            with open(filename, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    h.update(chunk)
            return h.hexdigest()
        except Exception as e:
            return f"<error: {e}>"
    
    def verify_hash(self, data, hash_value, algorithm="sha256"):
        """
        Verifikasi apakah hash dari data cocok dengan hash_value
        """
        try:
            hash_func = getattr(self, algorithm, None)
            if not hash_func:
                return False
            computed = hash_func(data)
            return computed == hash_value
        except:
            return False

# Ekspor instance hash
exports = {
    'hash': Hash()
}