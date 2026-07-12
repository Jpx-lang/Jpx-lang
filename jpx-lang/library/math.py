"""
Modul Math untuk JPX
Menyediakan fungsi-fungsi matematika lanjutan
"""

import math as _math
import random as _random

class Math:
    def __init__(self):
        # Konstanta matematika
        self.pi = _math.pi
        self.e = _math.e
        self.tau = _math.tau
        self.inf = float('inf')
        self.nan = float('nan')

    # ========== FUNGSI DASAR ==========
    def abs(self, x):
        """Nilai absolut"""
        return abs(x)

    def ceil(self, x):
        """Pembulatan ke atas"""
        return _math.ceil(x)

    def floor(self, x):
        """Pembulatan ke bawah"""
        return _math.floor(x)

    def round(self, x, ndigits=0):
        """Pembulatan ke jumlah digit tertentu"""
        return round(x, ndigits)

    def trunc(self, x):
        """Memotong bagian desimal"""
        return _math.trunc(x)

    def mod(self, a, b):
        """Sisa pembagian (modulo)"""
        return a % b

    def divmod(self, a, b):
        """Pembagian dengan sisa, return [hasil_bagi, sisa]"""
        hasil = divmod(a, b)
        return [hasil[0], hasil[1]]

    # ========== FUNGSI PANGKAT DAN LOGARITMA ==========
    def pow(self, x, y):
        """x pangkat y"""
        return _math.pow(x, y)

    def sqrt(self, x):
        """Akar kuadrat"""
        return _math.sqrt(x)

    def cbrt(self, x):
        """Akar kubik"""
        return x ** (1/3) if x >= 0 else -(-x) ** (1/3)

    def exp(self, x):
        """e pangkat x"""
        return _math.exp(x)

    def log(self, x, base=_math.e):
        """Logaritma dengan basis tertentu (default e)"""
        return _math.log(x, base)

    def log10(self, x):
        """Logaritma basis 10"""
        return _math.log10(x)

    def log2(self, x):
        """Logaritma basis 2"""
        return _math.log2(x)

    # ========== FUNGSI TRIGONOMETRI ==========
    def sin(self, x):
        """Sinus (x dalam radian)"""
        return _math.sin(x)

    def cos(self, x):
        """Cosinus (x dalam radian)"""
        return _math.cos(x)

    def tan(self, x):
        """Tangen (x dalam radian)"""
        return _math.tan(x)

    def asin(self, x):
        """Arc sinus (hasil dalam radian)"""
        return _math.asin(x)

    def acos(self, x):
        """Arc cosinus (hasil dalam radian)"""
        return _math.acos(x)

    def atan(self, x):
        """Arc tangen (hasil dalam radian)"""
        return _math.atan(x)

    def atan2(self, y, x):
        """Arc tangen y/x (hasil dalam radian)"""
        return _math.atan2(y, x)

    def degrees(self, x):
        """Konversi radian ke derajat"""
        return _math.degrees(x)

    def radians(self, x):
        """Konversi derajat ke radian"""
        return _math.radians(x)

    def hypot(self, x, y):
        """Hipotenusa (sqrt(x*x + y*y))"""
        return _math.hypot(x, y)

    # ========== FUNGSI HIPERBOLIK ==========
    def sinh(self, x):
        """Sinus hiperbolik"""
        return _math.sinh(x)

    def cosh(self, x):
        """Cosinus hiperbolik"""
        return _math.cosh(x)

    def tanh(self, x):
        """Tangen hiperbolik"""
        return _math.tanh(x)

    def asinh(self, x):
        """Arc sinus hiperbolik"""
        return _math.asinh(x)

    def acosh(self, x):
        """Arc cosinus hiperbolik"""
        return _math.acosh(x)

    def atanh(self, x):
        """Arc tangen hiperbolik"""
        return _math.atanh(x)

    # ========== FUNGSI STATISTIK SEDERHANA ==========
    def min(self, a, b, *args):
        """Nilai minimum dari dua atau lebih angka"""
        if args:
            return min(a, b, *args)
        return min(a, b)

    def max(self, a, b, *args):
        """Nilai maksimum dari dua atau lebih angka"""
        if args:
            return max(a, b, *args)
        return max(a, b)

    def sum(self, arr):
        """Jumlah semua elemen dalam list"""
        total = 0
        for x in arr:
            total += x
        return total

    def avg(self, arr):
        """Rata-rata dari elemen list"""
        if not arr:
            return 0
        return self.sum(arr) / len(arr)

    def median(self, arr):
        """Median dari list"""
        if not arr:
            return 0
        sorted_arr = sorted(arr)
        n = len(sorted_arr)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_arr[mid-1] + sorted_arr[mid]) / 2
        return sorted_arr[mid]

    # ========== FUNGSI LAINNYA ==========
    def factorial(self, n):
        """Faktorial dari n (n!)"""
        if n < 0:
            return None
        return _math.factorial(n)

    def gcd(self, a, b):
        """Faktor persekutuan terbesar"""
        return _math.gcd(a, b)

    def lcm(self, a, b):
        """Kelipatan persekutuan terkecil"""
        return abs(a*b) // _math.gcd(a, b)

    def isclose(self, a, b, rel_tol=1e-9, abs_tol=0.0):
        """Cek apakah dua angka mendekati sama"""
        return _math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)

    def isfinite(self, x):
        """Cek apakah x finite (bukan inf atau nan)"""
        return _math.isfinite(x)

    def isinf(self, x):
        """Cek apakah x infinite"""
        return _math.isinf(x)

    def isnan(self, x):
        """Cek apakah x NaN (Not a Number)"""
        return _math.isnan(x)

    def copysign(self, x, y):
        """Mengembalikan x dengan tanda dari y"""
        return _math.copysign(x, y)

    def fmod(self, x, y):
        """Modulo float (sisa pembagian)"""
        return _math.fmod(x, y)

    def frexp(self, x):
        """Memecah float menjadi mantissa dan exponent"""
        mantissa, exponent = _math.frexp(x)
        return [mantissa, exponent]

    def ldexp(self, x, exp):
        """Mengembalikan x * (2**exp)"""
        return _math.ldexp(x, exp)

    def modf(self, x):
        """Memecah float menjadi bagian pecahan dan integer"""
        frac, intpart = _math.modf(x)
        return [frac, intpart]

    def erf(self, x):
        """Error function"""
        return _math.erf(x)

    def erfc(self, x):
        """Complementary error function"""
        return _math.erfc(x)

    def gamma(self, x):
        """Gamma function"""
        return _math.gamma(x)

    def lgamma(self, x):
        """Log gamma function"""
        return _math.lgamma(x)

    # ========== FUNGSI GENERATE ANGKA ACAK (tambahan) ==========
    def random(self):
        """Angka acak antara 0 dan 1"""
        return _random.random()

    def randint(self, a, b):
        """Angka acak integer antara a dan b (inklusif)"""
        return _random.randint(a, b)

    def uniform(self, a, b):
        """Angka acak float antara a dan b"""
        return _random.uniform(a, b)

    def choice(self, seq):
        """Pilih elemen acak dari list"""
        return _random.choice(seq)

    def shuffle(self, seq):
        """Acak urutan list (mengembalikan list baru)"""
        import copy
        new_seq = copy.copy(seq)
        _random.shuffle(new_seq)
        return new_seq

    def sample(self, population, k):
        """Ambil sampel acak sebanyak k dari populasi"""
        return _random.sample(population, k)

    # ========== FUNGSI STATISTIK LANJUTAN ==========
    def variance(self, data):
        """Variansi dari sampel"""
        n = len(data)
        if n < 2:
            return 0
        mean = self.avg(data)
        return sum((x - mean) ** 2 for x in data) / (n - 1)

    def stdev(self, data):
        """Standar deviasi dari sampel"""
        return _math.sqrt(self.variance(data))

# Ekspor instance math
exports = {
    'math': Math()
}