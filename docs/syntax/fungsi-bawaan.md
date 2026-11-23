# Fungsi Bawaan

Fungsi bawaan (builtin) tersedia tanpa import.

## Daftar

| Fungsi | Kegunaan | Contoh | Hasil |
|---|---|---|---|
| `len(x)` | panjang string/list/dict | `len("abc")` | `3` |
| `str(x)` | konversi ke string | `str(42)` | `"42"` |
| `int(x)` | konversi ke integer | `int("42")` | `42` |
| `float(x)` | konversi ke float | `float("1.5")` | `1.5` |
| `bool(x)` | konversi ke boolean | `bool(0)` | `False` |
| `type(x)` | nama tipe nilai | `type(1)` | `int` |
| `ord(s)` | kode karakter pertama | `ord("A")` | `65` |
| `chr(n)` | karakter dari kode | `chr(66)` | `"B"` |

## Contoh

```jpx
print len("abc");        # 3
print str(42);           # 42
print int("42");         # 42
print float("1.5");      # 1.5
print bool(0);           # False
print bool("");          # False
print ord("A");          # 65
print chr(66);           # B

global [n = 1];
print type(n);           # int
```

## Konstanta Bawaan

`true`, `false`, dan `null` adalah nilai bawaan (bukan fungsi):

```jpx
global [b = true];
global [z = null];
print b;                 # True
print z is null;         # True
```

## Perilaku Konversi

- `int()` pada string non-angka mengembalikan `0` (tidak error):
  `int("abc")` → `0`. Validasi sendiri bila perlu, misalnya dengan
  `[jpx.string]` + `string.isDigit()`.
- `str(null)` menghasilkan string kosong — `null` dicetak sebagai kosong.
- Kombinasi `int("42") + float("1.5")` menghasilkan `43.5` (float, karena ada operand
  float).

## Yang Tidak Tersedia

- `range(n)` **tidak ada**. Untuk iterasi berjumlah tertentu, siapkan list:
  `for v in [0, 1, 2] { ... }` — lihat [kontrol-alur.md](kontrol-alur.md).
- Tidak ada `print()` sebagai fungsi, `input()`, maupun `eval()` — interaksi lain
  memakai modul (mis. `[scanner]` untuk baca input, `[fs]` untuk berkas).

## Halaman Terkait

- [tipe-data.md](tipe-data.md) — perilaku tipe dan format output
- [modul.md](modul.md) — `[scanner]`, `[fs]`, dan modul lainnya
- [batasan.md](batasan.md) — daftar lengkap yang belum didukung
