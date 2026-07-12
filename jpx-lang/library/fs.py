"""
fs.py - File System Module untuk JPX
Membaca, menulis, dan memanipulasi file dan folder
"""

import os
import shutil
import glob

class FileSystem:
    def __init__(self):
        self.current_dir = os.getcwd()
    
    # ========== FILE OPERATIONS ==========
    
    def write(self, filename, content):
        """
        Menulis konten ke file
        Contoh: fs.write("data.txt", "Hello World")
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error writing file: {e}")
            return False
    
    def append(self, filename, content):
        """
        Menambahkan konten ke file
        Contoh: fs.append("log.txt", "New log entry")
        """
        try:
            with open(filename, 'a', encoding='utf-8') as f:
                f.write(content + "\n")
            return True
        except Exception as e:
            print(f"Error appending to file: {e}")
            return False
    
    def read(self, filename):
        """
        Membaca isi file
        Contoh: isi = fs.read("data.txt")
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return None
    
    def read_lines(self, filename):
        """
        Membaca file per baris (return list)
        Contoh: lines = fs.read_lines("data.txt")
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return f.readlines()
        except Exception as e:
            print(f"Error reading file: {e}")
            return []
    
    def copy(self, src, dst):
        """
        Copy file
        Contoh: fs.copy("source.txt", "backup.txt")
        """
        try:
            shutil.copy2(src, dst)
            return True
        except Exception as e:
            print(f"Error copying file: {e}")
            return False
    
    def move(self, src, dst):
        """
        Move/rename file
        Contoh: fs.move("lama.txt", "baru.txt")
        """
        try:
            shutil.move(src, dst)
            return True
        except Exception as e:
            print(f"Error moving file: {e}")
            return False
    
    def delete(self, filename):
        """
        Hapus file
        Contoh: fs.delete("sampah.txt")
        """
        try:
            os.remove(filename)
            return True
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
    
    def rename(self, old, new):
        """
        Rename file
        Contoh: fs.rename("lama.txt", "baru.txt")
        """
        try:
            os.rename(old, new)
            return True
        except Exception as e:
            print(f"Error renaming file: {e}")
            return False
    
    def exists(self, path):
        """
        Cek apakah file/folder ada
        Contoh: if fs.exists("file.txt") { ... }
        """
        return os.path.exists(path)
    
    def is_file(self, path):
        """
        Cek apakah path adalah file
        Contoh: fs.is_file("data.txt")
        """
        return os.path.isfile(path)
    
    def is_dir(self, path):
        """
        Cek apakah path adalah folder
        Contoh: fs.is_dir("folder")
        """
        return os.path.isdir(path)
    
    def size(self, filename):
        """
        Ukuran file dalam bytes
        Contoh: fs.size("bigfile.zip")
        """
        try:
            return os.path.getsize(filename)
        except:
            return 0
    
    def info(self, filename):
        """
        Informasi lengkap file
        Contoh: info = fs.info("data.txt")
        """
        try:
            stat = os.stat(filename)
            return {
                'size': stat.st_size,
                'created': stat.st_ctime,
                'modified': stat.st_mtime,
                'accessed': stat.st_atime,
                'is_file': os.path.isfile(filename),
                'is_dir': os.path.isdir(filename)
            }
        except:
            return {}
    
    # ========== FOLDER OPERATIONS ==========
    
    def mkdir(self, path):
        """
        Buat folder baru
        Contoh: fs.mkdir("folder_baru")
        """
        try:
            os.mkdir(path)
            return True
        except Exception as e:
            print(f"Error creating directory: {e}")
            return False
    
    def mkdirs(self, path):
        """
        Buat folder beserta parent folder (seperti mkdir -p)
        Contoh: fs.mkdirs("parent/child/grandchild")
        """
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except Exception as e:
            print(f"Error creating directories: {e}")
            return False
    
    def rmdir(self, path):
        """
        Hapus folder kosong
        Contoh: fs.rmdir("folder_kosong")
        """
        try:
            os.rmdir(path)
            return True
        except Exception as e:
            print(f"Error removing directory: {e}")
            return False
    
    def rmtree(self, path):
        """
        Hapus folder beserta isinya (WARNING: tidak bisa dikembalikan!)
        Contoh: fs.rmtree("folder_berisi")
        """
        try:
            shutil.rmtree(path)
            return True
        except Exception as e:
            print(f"Error removing tree: {e}")
            return False
    
    def listdir(self, path="."):
        """
        Daftar isi folder
        Contoh: files = fs.listdir(".")
        """
        try:
            return os.listdir(path)
        except:
            return []
    
    def list_files(self, path=".", pattern="*"):
        """
        Daftar file dengan pattern tertentu
        Contoh: fs.list_files(".", "*.txt")
        """
        try:
            return glob.glob(os.path.join(path, pattern))
        except:
            return []
    
    def walk(self, path="."):
        """
        Berjalan melalui semua folder dan file (recursive)
        Contoh: for root, dirs, files in fs.walk(".") { ... }
        """
        try:
            result = []
            for root, dirs, files in os.walk(path):
                result.append({
                    'root': root,
                    'dirs': dirs,
                    'files': files
                })
            return result
        except:
            return []
    
    def tree(self, path=".", indent=0):
        """
        Tampilkan struktur folder seperti pohon
        Contoh: print fs.tree("project")
        """
        try:
            result = []
            items = os.listdir(path)
            for i, item in enumerate(items):
                full_path = os.path.join(path, item)
                is_last = (i == len(items) - 1)
                
                if is_last:
                    prefix = "└── "
                    next_indent = "    "
                else:
                    prefix = "├── "
                    next_indent = "│   "
                
                result.append(" " * indent + prefix + item)
                
                if os.path.isdir(full_path):
                    result.append(self.tree(full_path, indent + len(next_indent)))
            
            return "\n".join(result)
        except:
            return ""
    
    def chdir(self, path):
        """
        Pindah directory
        Contoh: fs.chdir("folder")
        """
        try:
            os.chdir(path)
            self.current_dir = os.getcwd()
            return True
        except:
            return False
    
    def getcwd(self):
        """
        Lihat directory sekarang
        Contoh: fs.getcwd()
        """
        return self.current_dir
    
    # ========== PATH OPERATIONS ==========
    
    def join(self, *paths):
        """
        Gabungkan path
        Contoh: path = fs.join("folder", "sub", "file.txt")
        """
        return os.path.join(*paths)
    
    def basename(self, path):
        """
        Ambil nama file dari path
        Contoh: fs.basename("folder/file.txt") -> "file.txt"
        """
        return os.path.basename(path)
    
    def dirname(self, path):
        """
        Ambil folder dari path
        Contoh: fs.dirname("folder/file.txt") -> "folder"
        """
        return os.path.dirname(path)
    
    def split(self, path):
        """
        Pisah folder dan file
        Contoh: folder, file = fs.split("folder/file.txt")
        """
        return os.path.split(path)
    
    def splitext(self, path):
        """
        Pisah nama file dan extension
        Contoh: name, ext = fs.splitext("data.txt")
        """
        return os.path.splitext(path)
    
    def abspath(self, path):
        """
        Dapatkan absolute path
        Contoh: fs.abspath("file.txt")
        """
        return os.path.abspath(path)
    
    # ========== FILE ATTRIBUTES ==========
    
    def touch(self, filename):
        """
        Buat file kosong atau update timestamp
        Contoh: fs.touch("newfile.txt")
        """
        try:
            with open(filename, 'a'):
                os.utime(filename, None)
            return True
        except:
            return False
    
    def chmod(self, path, mode):
        """
        Ubah permission file (Unix/Windows terbatas)
        Contoh: fs.chmod("script.sh", 0o755)
        """
        try:
            os.chmod(path, mode)
            return True
        except:
            return False
    
    # ========== UTILITY ==========
    
    def which(self, command):
        """
        Cari lokasi executable
        Contoh: fs.which("python")
        """
        return shutil.which(command)
    
    def disk_usage(self, path="."):
        """
        Info penggunaan disk
        Contoh: usage = fs.disk_usage("C:")
        """
        try:
            total, used, free = shutil.disk_usage(path)
            return {
                'total': total,
                'used': used,
                'free': free,
                'percent_used': (used / total) * 100
            }
        except:
            return {}

# Ekspor instance fs
exports = {
    'fs': FileSystem()
}