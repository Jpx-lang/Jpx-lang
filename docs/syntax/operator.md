# Operator

## Aritmetika

| Operator | Arti | Contoh | Hasil |
|---|---|---|---|
| `+` | tambah / gabung string | `1 + 1` | `2` |
| `-` | kurang | `10 - 4` | `6.0` |
| `*` | kali | `6 * 7` | `42` |
| `/` | bagi (float) | `7 / 2` | `3.5` |
| `//` | bagi bulat | `7 // 2` | `3` |
| `%` | sisa bagi | `7 % 2` | `1` |

Dua catatan perilaku:

- `-` menghasilkan **float** (`10 - 4` → `6.0`), sedangkan `+` dan `*` menghasilkan
  integer. Lihat juga [tipe-data.md](tipe-data.md).
- `+` bertindak sebagai penggabung string bila operandnya string: `"a" + "b"` → `ab`.

> Operator pangkat `**` **tidak** ada — pakai `mathx.power(2, 8)` dari modul
> `[mathx]` (hasil: `256`).

## Perbandingan

`==` `!=` `<` `>` `<=` `>=`

```jpx
print 1 == 1;      # True
print 1 != 2;      # True
print 1 < 2;       # True
print 2 >= 2;      # True
```

## Logika

```jpx
print true and false;   # False
print true or false;    # True
print not false;        # True
```

Gunakan kata kunci `and`, `or`, `not`. Operator simbol `&&`, `||`, `!` **tidak**
didukung.

## Operator `is` dan `in`

```jpx
global [x = null];
print x is null;                    # True

print 3 in [1, 2, 3];               # True
global [d = {"a": 1}];
print "a" in d;                     # True
```

- `is` dipakai untuk menguji `null`.
- `in` menguji keanggotaan list atau key dict.

## Ternary

```jpx
global [x = 5];
print x > 3 ? "besar" : "kecil";    # besar
```

## Pipe `|>`

Meneruskan hasil sisi kiri sebagai argumen pertama fungsi di sisi kanan — memudahkan
rantai transformasi:

```jpx
function double(x) { return x * 2; }
function inc(x)    { return x + 1; }

global [r = 5 |> double |> inc];
print r;                            # 11
```

> **Catatan**: pipe butuh kurung bila langsung dipakai di `print`:
> `print (5 |> double |> inc);` → `11`. Tanpa kurung, `print` hanya membaca angka
> pertama (`5`).

## Operator yang Belum Ada

`+=` `-=` `*=` `/=` `%=` dan `**` belum didukung. Tulis ulang secara eksplisit:

```jpx
global [n = 0];
n = n + 1;        # ✅
# n += 1;         # ❌ Invalid assignment target
```

Ini juga berlaku untuk penambahan di loop — pola umum di JPX:

```jpx
global [i = 0];
while i < 5 {
    i = i + 1;
}
print i;            # 5
```

## Halaman Terkait

- [tipe-data.md](tipe-data.md) — perilaku integer vs float
- [fungsi.md](fungsi.md) — fungsi sebagai target pipe `\|>`
- [batasan.md](batasan.md) — daftar lengkap yang belum didukung
