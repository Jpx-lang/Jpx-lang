"""
env.py - Modul untuk mengelola environment variables dan konfigurasi rahasia
Membaca file .env untuk menyimpan API key, token, password, dll.
"""

import os
import re

class Env:
    def __init__(self):
        self.variables = {}
        self.files_loaded = []
        # Auto-load .env jika ada
        self._load_default()
    
    def _load_default(self):
        """Load .env file jika ada di current directory"""
        if os.path.exists(".env"):
            self.load(".env")
    
    def _parse_line(self, line):
        """Parse satu baris dari file .env"""
        line = line.strip()
        
        # Skip komentar dan baris kosong
        if not line or line.startswith('#') or line.startswith('//'):
            return None, None
        
        # Cari tanda = pertama
        if '=' not in line:
            return None, None
        
        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip()
        
        # Handle quotes
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]
        
        # Handle escape sequences
        value = value.replace('\\n', '\n').replace('\\t', '\t')
        
        return key, value
    
    def load(self, filename):
        """
        Load file .env
        Args:
            filename: Nama file .env (bisa dengan path)
        Returns:
            True jika berhasil, False jika gagal
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    key, value = self._parse_line(line)
                    if key:
                        self.variables[key] = value
            
            if filename not in self.files_loaded:
                self.files_loaded.append(filename)
            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return False
    
    def get(self, key, default=None):
        """
        Ambil nilai environment variable
        Args:
            key: Nama variable
            default: Nilai default jika tidak ditemukan
        Returns:
            Nilai variable atau default
        """
        # Cek di internal variables dulu
        if key in self.variables:
            return self.variables[key]
        
        # Cek di system environment
        if key in os.environ:
            return os.environ[key]
        
        return default
    
    def __call__(self, key, default=None):
        """
        Shorthand untuk env.get()
        Contoh: api_key = env("API_KEY")
        """
        return self.get(key, default)
    
    def set(self, key, value):
        """
        Set environment variable (hanya di memory)
        """
        self.variables[key] = str(value)
        return True
    
    def delete(self, key):
        """
        Hapus environment variable
        """
        if key in self.variables:
            del self.variables[key]
            return True
        return False
    
    def list(self):
        """
        Daftar semua keys yang tersedia
        Returns:
            List of keys
        """
        keys = list(self.variables.keys())
        # Tambahkan system env vars? (opsional)
        # keys.extend([k for k in os.environ.keys() if k not in keys])
        return keys
    
    def has(self, key):
        """
        Cek apakah key ada
        """
        return key in self.variables or key in os.environ
    
    def save(self, filename=".env"):
        """
        Simpan variables ke file .env
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for key, value in self.variables.items():
                    # Escape special characters
                    if '\n' in value or '\t' in value:
                        value = value.replace('\n', '\\n').replace('\t', '\\t')
                        f.write(f'{key}="{value}"\n')
                    elif ' ' in value or '#' in value:
                        f.write(f'{key}="{value}"\n')
                    else:
                        f.write(f'{key}={value}\n')
            return True
        except Exception as e:
            print(f"Error saving to {filename}: {e}")
            return False
    
    def reload(self):
        """
        Reload semua file .env yang sudah diload
        """
        self.variables = {}
        for f in self.files_loaded:
            self.load(f)
        return True
    
    def clear(self):
        """
        Hapus semua variables
        """
        self.variables = {}
        self.files_loaded = []
        return True
    
    def export(self):
        """
        Export semua variables sebagai dictionary
        """
        return self.variables.copy()
    
    # ========== PROPERY ACCESS ==========
    @property
    def env(self):
        """
        Akses ke semua variables sebagai properti
        Contoh: env.env.API_KEY
        """
        return self
    
    def __getattr__(self, name):
        """
        Memungkinkan akses seperti env.API_KEY
        """
        return self.get(name, "")
    
    def __repr__(self):
        return f"<Env variables: {len(self.variables)} loaded>"

# Ekspor instance env
exports = {
    'env': Env()
}