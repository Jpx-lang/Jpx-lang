# json.py - JSON Library untuk JPX
# Versi: Mendukung multiple args (untuk list) dan variabel perantara

import json as py_json

class JSON:
    def encode(self, *args):
        """
        Encode ke JSON string.
        Jika banyak argumen, gabung jadi list.
        Untuk object, gunakan variabel perantara.
        """
        if len(args) == 0:
            return "null"
        if len(args) == 1:
            obj = args[0]
        else:
            # Banyak argumen -> jadikan list
            obj = list(args)
        try:
            return py_json.dumps(obj)
        except:
            return "{}"
    
    def decode(self, *args):
        """
        Decode JSON string ke object.
        Jika banyak argumen, gabung dengan spasi.
        """
        if len(args) == 0:
            return {}
        json_str = ' '.join(str(a) for a in args)
        try:
            return py_json.loads(json_str)
        except:
            return {}
    
    def pretty(self, *args, indent=2):
        """Pretty print JSON"""
        if len(args) == 0:
            return "{}"
        if len(args) == 1:
            obj = args[0]
        else:
            obj = list(args)
        try:
            return py_json.dumps(obj, indent=int(indent))
        except:
            return "{}"
    
    def read(self, filepath):
        """Baca JSON dari file"""
        try:
            with open(str(filepath), 'r', encoding='utf-8') as f:
                return py_json.load(f)
        except:
            return {}
    
    def write(self, filepath, obj):
        """Tulis JSON ke file"""
        try:
            with open(str(filepath), 'w', encoding='utf-8') as f:
                py_json.dump(obj, f, indent=2)
            return True
        except:
            return False
    
    def keys(self, obj):
        """Ambil keys dari object"""
        if isinstance(obj, dict):
            return list(obj.keys())
        return []
    
    def values(self, obj):
        """Ambil values dari object"""
        if isinstance(obj, dict):
            return list(obj.values())
        return []
    
    def get(self, obj, key, default=None):
        """Ambil value dengan key"""
        if isinstance(obj, dict):
            return obj.get(key, default)
        return default
    
    def merge(self, obj1, obj2):
        """Gabungkan dua object"""
        if not isinstance(obj1, dict) or not isinstance(obj2, dict):
            return obj1
        result = obj1.copy()
        result.update(obj2)
        return result

exports = {'json': JSON()}

if __name__ == "__main__":
    print("[json.py] Library JSON siap!")