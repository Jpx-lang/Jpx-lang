# string.py - Simple String Library untuk JPX
# Mengikuti pola dari color.py

import re
import hashlib
import base64
import random as _random
import string as py_string

# ============================================================
# FUNGSI-FUNGSI STRING
# ============================================================

def length(s):
    if s is None: return 0
    return len(str(s))

def upper(s):
    if s is None: return ""
    return str(s).upper()

def lower(s):
    if s is None: return ""
    return str(s).lower()

def trim(s):
    if s is None: return ""
    return str(s).strip()

def reverse(s):
    if s is None: return ""
    return str(s)[::-1]

def contains(s, sub):
    if s is None or sub is None: return False
    return sub in str(s)

def replace(s, old, new):
    if s is None: return ""
    return str(s).replace(str(old), str(new))

def split(s, delim=" "):
    if s is None: return []
    return str(s).split(str(delim))

def join(lst, glue=""):
    if lst is None: return ""
    if not isinstance(lst, list):
        try: lst = list(lst)
        except: return str(lst)
    return glue.join(str(x) for x in lst)

def md5(s):
    if s is None: return ""
    return hashlib.md5(str(s).encode()).hexdigest()

def random(length=8):
    try:
        chars = py_string.ascii_letters + py_string.digits
        return ''.join(_random.choice(chars) for _ in range(int(length)))
    except:
        return ""

def base64_encode(s):
    if s is None: return ""
    return base64.b64encode(str(s).encode()).decode()

def base64_decode(s):
    if s is None: return ""
    try:
        return base64.b64decode(str(s).encode()).decode()
    except:
        return ""

def starts_with(s, prefix):
    if s is None: return False
    return str(s).startswith(str(prefix))

def ends_with(s, suffix):
    if s is None: return False
    return str(s).endswith(str(suffix))

def is_email(s):
    if s is None: return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, str(s)) is not None

def constants():
    return {
        "digits": "0123456789",
        "letters": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "lowercase": "abcdefghijklmnopqrstuvwxyz",
        "uppercase": "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    }

# ============================================================
# CLASS STRING - SEPERTI COLOR.PY
# ============================================================

class String:
    def __init__(self):
        # Dasar
        self.length = length
        self.upper = upper
        self.lower = lower
        self.trim = trim
        self.reverse = reverse
        self.contains = contains
        self.replace = replace
        self.split = split
        self.join = join
        
        # Hashing & Encoding
        self.md5 = md5
        self.base64_encode = base64_encode
        self.base64_decode = base64_decode
        self.random = random
        
        # Validasi
        self.starts_with = starts_with
        self.ends_with = ends_with
        self.is_email = is_email
        
        # Constants
        self.constants = constants

# ============================================================
# EXPORT - INI YANG DICARI JPX (SAMA PERSIS DENGAN COLOR.PY)
# ============================================================
exports = {'string': String()}

# Debug
if __name__ == "__main__":
    print("[string.py] Library string siap digunakan!")