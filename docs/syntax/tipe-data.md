# Tipe Data

JPX punya tujuh tipe data. `print` menampilkannya dengan format berikut:

| Tipe | Contoh | Output `print` |
|---|---|---|
| Integer | `42` | `42` |
| Float | `3.14` | `3.14` |
| String | `"halo"` | `halo` |
| Boolean | `true` / `false` | `True` / `False` |
| Null | `null` | *(kosong)* |
| List | `[1, 2, 3]` | `[1, 2, 3]` |
| Dict | `{"k": "v"}` | `{'k': 'v'}` |

Perhatikan dua kebiasaan output yang berakar pada representasi internal:

- Boolean dicetak `True` / `False` (huruf besar, gaya Python).
- Dict dicetak dengan kutip tunggal, gaya repr Python: `{'k': 'v'}`.

## Contoh Deklarasi dan Inspeksi

```jpx
global [n = 42];
global [f = 3.14];
global [s = "halo"];
global [b = true];
global [z = null];
global [l = [1, 2, 3]];
global [d = {"k": "v"}];

print n;        # 42
print type(n);  # int
print type(s);  # str
print type(l);  # list
```

Fungsi `type()` mengembalikan nama tipe gaya Python: `int`, `float`, `str`, `bool`,
`NoneType`, `list`, `dict`.

## Catatan Penting tentang Integer dan Float

Hasil operasi numerik **tidak sepenuhnya konsisten** di A2:

```jpx
print 1 + 1;     # 2      (integer)
print 6 * 7;     # 42     (integer)
print 10 - 4;    # 6.0    (float!)
print 7 / 2;     # 3.5    (float, wajar)
print 7 // 2;    # 3      (pembagian bulat)
```

Operator `-` (termasuk negasi `-3`) selalu menghasilkan float, sehingga `fib(10)`
rekursif mencetak `55.0`. Sampai perilaku ini diseragamkan, jangan mengandalkan
format integer dari hasil pengurangan; gunakan `int()` bila perlu integer murni:

```jpx
print int(10 - 4);   # 6
```

## Escape Sequence

Di dalam string literal tersedia escape standar:

| Escape | Arti |
|---|---|
| `\n` | baris baru |
| `\t` | tab |
| `\r` | carriage return |
| `\\` | backslash |
| `\"` | kutip ganda |
| `\'` | kutip tunggal |
| `\0` | karakter null |
| `\b` | backspace |
| `\f` | form feed |
| `\$` | tanda dolar literal (mencegah interpolasi) |

Escape tak dikenal dibiarkan apa adanya (`\q` tetap `\q`).

```jpx
global [s = "baris satu\nbaris dua"];   # \n jadi baris baru
print s;
```

## String Multi-Baris

Selain `\n`, string boleh memuat baris baru literal:

```jpx
global [multi = "baris satu
baris dua"];
print multi;
```

## Halaman Terkait

- [string.md](string.md) — 17 method string dan interpolasi
- [list-dict.md](list-dict.md) — operasi list dan dict
- [fungsi-bawaan.md](fungsi-bawaan.md) — konversi tipe: `int()`, `float()`, `str()`, `bool()`
