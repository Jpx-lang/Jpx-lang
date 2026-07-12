import colorama
from colorama import Fore, Style

# Inisialisasi colorama (tanpa autoreset agar kita bisa reset manual)
colorama.init()

class Color:
    def __init__(self):
        # Warna teks
        self.red = Fore.RED
        self.green = Fore.GREEN
        self.yellow = Fore.YELLOW
        self.blue = Fore.BLUE
        self.magenta = Fore.MAGENTA
        self.cyan = Fore.CYAN
        self.white = Fore.WHITE
        # Reset ke warna default
        self.reset = Style.RESET_ALL

# Ekspor instance color agar bisa diimpor di JPX
exports = {'color': Color()}