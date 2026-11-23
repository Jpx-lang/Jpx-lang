# Batasan yang Diketahui

Halaman ini daftar fitur yang **belum** didukung di JPX A2. Semua butir di bawah sudah
diverifikasi — jangan dipakai sampai diumumkan didukung. Daftar ini juga ada supaya Anda
tidak perlu menebak-nebak kenapa kode gagal.

## Sintaks dan Keyword

| Fitur | Status | Alternatif |
|---|---|---|
| `Print` / `Global` (huruf besar) | ❌ case-sensitive | tulis `print`, `global` |
| `let` | ❌ tidak ada | pakai `global [...]` |
| Komentar `//` atau `/* */` | ❌ | pakai `#` (`//` adalah pembagian bulat) |
| `print "a", "b"` (banyak argumen) | ❌ | gabung: `print "a" + "b"` |
| `print(...)` dengan kurung | ❌ | tulis `print ...;` |
| `catch e` tanpa kurung | ❌ | wajib `catch (e)` |
| Blok `finally` | ❌ | rapikan resource manual |

## Operator

| Fitur | Status | Alternatif |
|---|---|---|
| `**` (pangkat) | ❌ | `[mathx]` + `mathx.power(2, 8)` |
| `+=` `-=` `*=` `/=` `%=` | ❌ | tulis penuh: `n = n + 1` |
| `&&` `\|\|` `!` | ❌ | pakai `and`, `or`, `not` |
| `print 5 \|> f` tanpa kurung | ❌ | pakai `print (5 \|> f)` |

## Fungsi

| Fitur | Status | Alternatif |
|---|---|---|
| Default argument `f(a, b = 1)` | ❌ | terima null lalu isi manual, atau wajibkan argumen |
| Variadic `f(...args)` | ❌ | terima list: `f([1, 2, 3])` |
| Lambda / fungsi anonim | ❌ | deklarasikan `function` bernama |

## Fungsi dan Method

| Fitur | Status | Alternatif |
|---|---|---|
| `range(n)` | ❌ | siapkan list: `[0, 1, 2]` |
| Method `.length()` | ❌ | pakai `len()` |
| Method string menyusul `.split()` | ❌ hasilnya list | ambil elemen dulu: `.split(" ")[0].upper()` |
| `[io]` (tanpa prefix paket) | ❌ | tulis `[jpx.io]` |

## Modul dan Lingkungan

| Fitur | Status | Catatan |
|---|---|---|
| `[color]` tanpa `colorama` | ❌ | `pip install colorama` dulu |
| `[win32sys]` / `[win32ui]` di Linux/macOS | ❌ | khusus Windows + `pip install pywin32` |

## Perilaku yang Perlu Diwaspadai

Bukan error, tapi penting diketahui:

1. **Hasil `-` selalu float** — `10 - 4` → `6.0`, `fib(10)` → `55.0`, `str(-3)` →
   `-3.0`. Bungkus dengan `int()` bila butuh integer. Lihat
   [tipe-data.md](tipe-data.md).
2. **Error di `${ekspresi}` tidak menghentikan program** — muncul sebagai teks
   `<error:...>` di output. Periksa output string Anda. Lihat
   [print-dan-interpolasi.md](print-dan-interpolasi.md).
3. **`--jpx-interpreter` hanya subset** — jalur self-hosted tidak mendukung import,
   class lengkap, try-catch penuh, dan method string native; kegagalannya bisa diam-diam.
   Gunakan hanya untuk demo/debug. Lihat [../cli/perintah-dasar.md](../cli/perintah-dasar.md).

## Halaman Terkait

- [README.md](README.md) — konvensi dasar sintaks
- [modul.md](modul.md) — dependensi modul bawaan
