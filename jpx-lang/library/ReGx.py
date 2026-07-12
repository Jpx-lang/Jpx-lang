"""
Modul Regex untuk JPX
Membungkus fungsi-fungsi regular expression Python
"""

import re

class Regex:
    def match(self, pattern, string):
        """
        Mencocokkan pattern dari awal string.
        Mengembalikan string yang cocok atau null jika tidak cocok.
        """
        try:
            m = re.match(pattern, string)
            if m:
                return m.group(0)
            return None
        except Exception as e:
            return f"<error: {e}>"

    def search(self, pattern, string):
        """
        Mencari pattern di mana saja dalam string.
        Mengembalikan string yang cocok pertama atau null.
        """
        try:
            m = re.search(pattern, string)
            if m:
                return m.group(0)
            return None
        except Exception as e:
            return f"<error: {e}>"

    def findall(self, pattern, string):
        """
        Mencari semua kecocokan pattern dalam string.
        Mengembalikan list string.
        """
        try:
            return re.findall(pattern, string)
        except Exception as e:
            return [f"<error: {e}>"]

    def sub(self, pattern, repl, string, count=0):
        """
        Mengganti pattern dengan repl dalam string (sebanyak count kali).
        count=0 berarti semua.
        """
        try:
            return re.sub(pattern, repl, string, count)
        except Exception as e:
            return f"<error: {e}>"

    def split(self, pattern, string, maxsplit=0):
        """
        Memisahkan string berdasarkan pattern.
        Mengembalikan list.
        """
        try:
            return re.split(pattern, string, maxsplit)
        except Exception as e:
            return [f"<error: {e}>"]

    def escape(self, string):
        """
        Meng-escape karakter khusus regex dalam string.
        """
        try:
            return re.escape(string)
        except Exception as e:
            return f"<error: {e}>"

    # Method tambahan untuk mendapatkan informasi lebih detail (opsional)
    def match_obj(self, pattern, string):
        """
        Mengembalikan objek match dengan method group().
        Karena JPX tidak punya objek, kita kembalikan dictionary sederhana.
        """
        try:
            m = re.match(pattern, string)
            if m:
                return {
                    'group': m.group(0),
                    'groups': m.groups(),
                    'start': m.start(),
                    'end': m.end(),
                    'span': m.span()
                }
            return None
        except Exception as e:
            return f"<error: {e}>"

# Ekspor instance regex
exports = {
    'regex': Regex()
}