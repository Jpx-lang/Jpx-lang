# Modul & Import

## Cara Import

Taruh import di bagian atas skrip. Sintaksnya `nama_modul` di dalam kurung siku,
diakhiri `;`:

```jpx
[string];
[array];
[math];
```

Hasilnya tersedia sebagai objek dengan nama modul: `string.upper("hi")`,
`array.sum([1, 2])`, dan seterusnya.

## Modul Bawaan Native (`.py`)

Modul berikut dikirim bersama JPX (implementasi Python, pustaka standar kecuali yang
dicatat):

`array` `beuty` `color` `env` `fs` `hash` `JpXhash` `JpXUi` `json` `math` `mem`
`notification` `print` `random` `ReGx` `requests` `scanner` `speedreq` `string`
`subnotif` `system` `time` `win32sys` `win32ui`

Dependensi khusus:

| Modul | Kebutuhan |
|---|---|
| `[color]` | paket pip `colorama` — `pip install colorama`; tanpa itu import gagal |
| `[win32sys]`, `[win32ui]` | paket pip `pywin32`, **hanya Windows** |
| lainnya | pustaka standar Python — tanpa instalasi tambahan |

Bila muncul `No module named '...'`, itu berarti modulnya memakai pustaka pihak ketiga
yang belum terpasang — pasang lewat pip.

## Paket Self-Hosted (`library/jpx/*.jpx`)

Sebagian pustaka ditulis dengan sintaks JPX sendiri dan diimpor memakai titik:

```jpx
[jpx.string];
[jpx.io];
[jpx.types];
[jpx.functional];
[jpx.choose];
```

Modul di dalam paket diekspor dengan **nama terakhirnya**:

```jpx
[jpx.string];
print string.isDigit("5");      # True
print string.isAlpha("B");      # True
```

> `[io]` **tidak** bisa — modul `io` berada di dalam paket `jpx`, jadi tulis
> `[jpx.io]`.

## Contoh Pemakaian Modul

```jpx
[string];
[array];
[mathx];
[json];
[time];

print string.upper("hi");               # HI
print string.starts_with("abc", "a");   # True

print array.sum([1, 2, 3]);             # 6
print array.sort([3, 1, 2]);            # [1, 2, 3]

print mathx.fib(10);                    # 55
print mathx.isPrime(17);                # True
print mathx.gcd(12, 8);                 # 4
print mathx.lcm(4, 6);                  # 12
print mathx.power(2, 8);                # 256
print mathx.mean([1, 2, 3]);            # 2.0

print json.encode({"a": 1});            # {"a": 1}
print time.now();                       # 2026-11-22 10:39:39
```

Fungsi `mathx` yang tersedia:
`fib` `factorial` `isPrime` `gcd` `lcm` `power` `isqrt` `mean` `median`

Lihat daftar lengkap modul yang terdeteksi di sistem Anda:

```bash
jpx --list-modules
```

## Urutan Pencarian Modul

Saat skrip memanggil `[modul];`, interpreter mencari berkas `modul.jpx` atau
`modul.py` (atau folder paket berisi `_jpx_.jpx`) dengan urutan prioritas:

1. **Folder skrip** — direktori tempat file `.jpx` yang dijalankan berada
   (mendukung import relatif).
2. **`lib/` di direktori kerja** — tempat `jpxkg` memasang paket.
3. **`JPX_PATH`** — direktori tambahan dari variabel lingkungan (dipisah `;` di Windows
   atau `:` di Linux).
4. **`library/` bawaan** — fallback terakhir.

Set `JPX_PATH` untuk menambah lokasi modul kustom:

```bash
# Linux / macOS
export JPX_PATH="/home/aku/modul-jpx:/opt/jpx-modul"

# Windows PowerShell
$env:JPX_PATH = "C:\modul-jpx;C:\opt\jpx-modul"
```

## Membuat Modul Sendiri

1. Taruh berkas `modulku.jpx` (atau `modulku.py` untuk implementasi Python) di folder
   skrip Anda, atau di folder yang terdaftar di search path di atas.
2. Import dengan `[modulku];`.
3. Verifikasi terdeteksi dengan `jpx --list-modules`.

Paket pihak ketiga dapat dipasang dengan `jpxkg` — lihat
[../cli/jpxkg.md](../cli/jpxkg.md).

## Catatan Keamanan

Mengimpor modul `.py` berarti mengeksekusi kode Python dari berkas tersebut. Hanya
impor modul dari sumber yang Anda percaya (bawaan, `lib/` hasil `jpxkg`, atau berkas
Anda sendiri).

## Halaman Terkait

- [../cli/jpxkg.md](../cli/jpxkg.md) — memasang paket dengan package manager
- [../cli/perintah-dasar.md](../cli/perintah-dasar.md) — `--list-modules` dan `JPX_PATH`
- [list-dict.md](list-dict.md) — modul `array` untuk list
