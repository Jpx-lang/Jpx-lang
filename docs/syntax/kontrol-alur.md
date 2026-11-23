# Kontrol Alur

## `if` / `else if` / `elif` / `else`

```jpx
global [x = 2];

if x == 1 {
    print "satu";
} elif x == 2 {
    print "dua";
} else {
    print "lainnya";
}
# -> dua
```

- `elif` dan `else if` keduanya diterima.
- Kurung pada kondisi bersifat **opsional**: `if (x == 1) {` sama dengan `if x == 1 {`.
- Blok selalu ditulis dengan `{ }`.

## `while`

```jpx
global [i = 0];
while i < 3 {
    i = i + 1;
}
print i;            # 3
```

`while true { ... }` berjalan terus sampai `break`.

## `for ... in`

Iterasi atas list. Fungsi `range()` **tidak ada**, jadi siapkan list-nya sendiri:

```jpx
global [total = 0];
for v in [1, 2, 3] {
    total = total + v;
}
print total;        # 6
```

Untuk iterasi berjumlah tertentu, tulis list literal atau bangun dengan `while`:

```jpx
for v in [0, 1, 2, 3, 4] {
    print v;
}
```

## `break` dan `continue`

```jpx
global [i = 0];
while true {
    i = i + 1;
    if i > 2 { break; }
}
print i;            # 3

global [total = 0];
for v in [1, 2, 3] {
    if v == 2 { continue; }
    total = total + v;
}
print total;        # 4
```

`break` / `continue` di luar loop memberi `SyntaxError`. Keduanya hanya berlaku pada
loop terdalam tempat mereka ditulis.

## `switch` / `case` / `default`

Gaya Go, **tanpa fall-through** — hanya blok case yang cocok yang dijalankan, lalu
eksekusi keluar dari switch. Spasi dan indentasi bebas.

```jpx
global [x = 2];

switch x {
    case 1 { print "satu"; }
    case 2 { print "dua"; }
    case 3 { print "tiga"; }
    default { print "lainnya"; }
}
# -> dua
```

Nilai `case` boleh berupa ekspresi:

```jpx
global [a = 2];
global [b = 3];

switch a + b {
    case 4 { print "empat"; }
    case 5 { print "lima"; }
    default { print "?"; }
}
# -> lima
```

## `try` / `catch`

```jpx
try {
    print "di dalam try";
} catch (e) {
    print "error: " + e;
}
print "selesai";
```

- `catch` **wajib** memakai kurung: `catch (e)`, bukan `catch e`.
- Variabel `e` berisi pesan error, misalnya:
  `error: Variable 'undefined_var' not defined. Use 'global [undefined_var = value]' to declare it.`
- Bisa ditaruh di dalam function, di dalam loop, maupun di tingkat atas skrip.
- Blok `finally` **belum** didukung di A2.

## Halaman Terkait

- [operator.md](operator.md) — operator perbandingan dan logika untuk kondisi
- [fungsi.md](fungsi.md) — `return` di dalam kontrol alur
- [batasan.md](batasan.md) — `range()`, `finally`, dan lainnya
