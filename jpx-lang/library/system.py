import os
import subprocess
import platform
import sys

class System:
    # Eksekusi perintah (return code)
    def run(self, command):
        return os.system(command)

    # Eksekusi perintah dan ambil outputnya
    def get_output(self, command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout + result.stderr
        except Exception as e:
            return str(e)

    # Direktori saat ini
    def pwd(self):
        return os.getcwd()

    # Daftar isi direktori
    def ls(self, path="."):
        try:
            return os.listdir(path)
        except:
            return []

    # Pindah direktori
    def cd(self, path):
        try:
            os.chdir(path)
            return os.getcwd()
        except Exception as e:
            return str(e)

    # Buat direktori
    def mkdir(self, path):
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except:
            return False

    # Hapus file
    def rm(self, path):
        try:
            os.remove(path)
            return True
        except:
            return False

    # Cek apakah path ada
    def exists(self, path):
        return os.path.exists(path)

    # Informasi platform
    def platform(self):
        return sys.platform

    # Jumlah CPU
    def cpu_count(self):
        return os.cpu_count() or 1

# Ekspor instance system
exports = {
    'system': System()
}