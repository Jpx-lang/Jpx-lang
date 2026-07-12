"""
Modul Random untuk JPX
Menyediakan fungsi-fungsi untuk menghasilkan angka acak
"""

import random as _random
import time
import math

class Random:
    def __init__(self):
        # Inisialisasi seed dengan waktu saat ini
        _random.seed(time.time())
    
    # ========== FUNGSI DASAR ==========
    def random(self):
        """
        Mengembalikan angka float acak antara 0.0 dan 1.0
        Contoh: random.random() -> 0.3745
        """
        return _random.random()
    
    def uniform(self, a, b):
        """
        Mengembalikan angka float acak antara a dan b
        Contoh: random.uniform(5, 10) -> 7.234
        """
        return _random.uniform(a, b)
    
    def randint(self, a, b):
        """
        Mengembalikan integer acak antara a dan b (inklusif)
        Contoh: random.randint(1, 100) -> 42
        """
        return _random.randint(a, b)
    
    def randrange(self, start, stop=None, step=1):
        """
        Mengembalikan integer acak dari range(start, stop, step)
        Contoh: random.randrange(10) -> 0-9
        Contoh: random.randrange(5, 10) -> 5-9
        Contoh: random.randrange(0, 10, 2) -> genap 0-8
        """
        if stop is None:
            return _random.randrange(start)
        return _random.randrange(start, stop, step)
    
    # ========== FUNGSI PILIHAN ACAK ==========
    def choice(self, seq):
        """
        Memilih satu elemen acak dari list
        Contoh: random.choice(["apel", "mangga", "jeruk"]) -> "mangga"
        """
        if not seq or len(seq) == 0:
            return None
        return _random.choice(seq)
    
    def choices(self, population, weights=None, k=1):
        """
        Memilih k elemen acak dengan kemungkinan bobot (boleh sama)
        Contoh: random.choices(["A","B","C"], [0.5,0.3,0.2], 3) -> ["A","B","A"]
        """
        if not population or len(population) == 0:
            return []
        return _random.choices(population, weights=weights, k=k)
    
    def sample(self, population, k):
        """
        Mengambil sampel acak sebanyak k tanpa pengembalian (unik)
        Contoh: random.sample([1,2,3,4,5], 3) -> [2,5,1]
        """
        if not population or len(population) < k:
            return []
        return _random.sample(population, k)
    
    def shuffle(self, seq):
        """
        Mengacak urutan list (mengembalikan list baru)
        Contoh: random.shuffle([1,2,3,4,5]) -> [3,1,5,2,4]
        """
        if not seq:
            return []
        new_seq = seq.copy()
        _random.shuffle(new_seq)
        return new_seq
    
    # ========== FUNGSI DISTRIBUSI ==========
    def gauss(self, mu, sigma):
        """
        Distribusi Gaussian (normal) dengan mean mu dan standard deviation sigma
        Contoh: random.gauss(0, 1) -> -0.234
        """
        return _random.gauss(mu, sigma)
    
    def normalvariate(self, mu, sigma):
        """
        Distribusi normal (sama dengan gauss)
        """
        return _random.normalvariate(mu, sigma)
    
    def expovariate(self, lambd):
        """
        Distribusi eksponensial dengan parameter lambda (1/mean)
        Contoh: random.expovariate(2) -> 0.123
        """
        return _random.expovariate(lambd)
    
    def betavariate(self, alpha, beta):
        """
        Distribusi Beta dengan parameter alpha dan beta
        """
        return _random.betavariate(alpha, beta)
    
    def gammavariate(self, alpha, beta):
        """
        Distribusi Gamma dengan parameter alpha dan beta
        """
        return _random.gammavariate(alpha, beta)
    
    def lognormvariate(self, mu, sigma):
        """
        Distribusi log-normal
        """
        return _random.lognormvariate(mu, sigma)
    
    def paretovariate(self, alpha):
        """
        Distribusi Pareto dengan parameter alpha
        """
        return _random.paretovariate(alpha)
    
    def weibullvariate(self, alpha, beta):
        """
        Distribusi Weibull dengan parameter alpha dan beta
        """
        return _random.weibullvariate(alpha, beta)
    
    # ========== FUNGSI SEED ==========
    def seed(self, a=None):
        """
        Mengatur seed untuk generator angka acak
        Contoh: random.seed(123) -> hasil acak akan sama setiap run
        """
        _random.seed(a)
        return True
    
    def get_seed(self):
        """
        Mendapatkan state seed saat ini (untuk debugging)
        """
        return _random.getstate()
    
    # ========== FUNGSI BOOLEAN ACAK ==========
    def coin(self):
        """
        Melempar koin: true untuk kepala, false untuk ekor
        Contoh: random.coin() -> true
        """
        return _random.choice([True, False])
    
    def boolean(self, probability=0.5):
        """
        Mengembalikan true dengan probabilitas tertentu (0.0-1.0)
        Contoh: random.boolean(0.7) -> 70% kemungkinan true
        """
        return _random.random() < probability
    
    # ========== FUNGSI UTILITY ==========
    def color(self):
        """
        Menghasilkan warna acak dalam format hex
        Contoh: random.color() -> "#A3F12B"
        """
        r = _random.randint(0, 255)
        g = _random.randint(0, 255)
        b = _random.randint(0, 255)
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def rgb(self):
        """
        Menghasilkan warna acak dalam format RGB
        Contoh: random.rgb() -> [120, 45, 200]
        """
        return [
            _random.randint(0, 255),
            _random.randint(0, 255),
            _random.randint(0, 255)
        ]
    
    def string(self, length=10, chars=None):
        """
        Menghasilkan string acak dengan panjang tertentu
        Contoh: random.string(8) -> "aB3kL9xP"
        """
        import string
        if chars is None:
            chars = string.ascii_letters + string.digits
        return ''.join(_random.choice(chars) for _ in range(length))
    
    def password(self, length=12):
        """
        Menghasilkan password acak yang kuat (huruf besar, kecil, angka, simbol)
        Contoh: random.password(10) -> "aB3$kL9#xP"
        """
        import string
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(_random.choice(chars) for _ in range(length))
    
    def uuid(self):
        """
        Menghasilkan UUID versi 4 acak
        Contoh: random.uuid() -> "550e8400-e29b-41d4-a716-446655440000"
        """
        import uuid
        return str(uuid.uuid4())
    
    # ========== FUNGSI STATISTIK DENGAN DATA ACAK ==========
    def shuffle_string(self, s):
        """
        Mengacak karakter dalam string
        Contoh: random.shuffle_string("hello") -> "olleh"
        """
        if not s:
            return s
        chars = list(s)
        _random.shuffle(chars)
        return ''.join(chars)
    
    def weighted_choice(self, items, weights):
        """
        Memilih item berdasarkan bobot
        items: list item
        weights: list bobot (jumlah harus sama)
        Contoh: random.weighted_choice(["A","B","C"], [0.1,0.3,0.6])
        """
        if not items or not weights or len(items) != len(weights):
            return None
        return _random.choices(items, weights=weights, k=1)[0]
    
    def lottery(self, tickets, winners=1):
        """
        Memilih pemenang undian (tanpa pengembalian)
        tickets: list peserta
        winners: jumlah pemenang
        Contoh: random.lottery(["Budi","Ana","Citra"], 2) -> ["Ana","Budi"]
        """
        if not tickets or winners > len(tickets):
            return []
        return _random.sample(tickets, winners)
    
    def dice(self, sides=6):
        """
        Melempar dadu dengan jumlah sisi tertentu
        Contoh: random.dice(6) -> 4
        """
        return _random.randint(1, sides)
    
    def dice_roll(self, count=2, sides=6):
        """
        Melempar beberapa dadu sekaligus
        Contoh: random.dice_roll(3, 6) -> [4, 2, 6]
        """
        return [_random.randint(1, sides) for _ in range(count)]
    
    def probability(self, percentage):
        """
        Mengembalikan true dengan persentase tertentu (0-100)
        Contoh: random.probability(75) -> 75% kemungkinan true
        """
        return _random.random() * 100 < percentage

# Ekspor instance random
exports = {
    'random': Random()
}