# String

String ditulis dengan kutip ganda (atau kutip tunggal). Method string bisa dipanggil
langsung dari literal maupun variabel.

## 17 Method String

```jpx
print "abc".upper();                 # ABC
print "ABC".lower();                 # abc
print "  x  ".trim();                # x
print "  x  ".strip();               # x
print "a,b".split(",");              # ['a', 'b']
print "aaa".replace("a", "b");       # bbb
print "abc".contains("b");           # True
print "abc".startsWith("a");         # True
print "abc".endsWith("c");           # True
print "hello".find("ll");            # 2
print "hello".substring(1, 3);       # el
print "ab".repeat(3);                # ababab
print "abcabc".count("a");           # 2
print "abc".toCharArray();           # ['a', 'b', 'c']
```

Daftar lengkap (17 method):

`contains` `count` `endsWith` `find` `lower` `lstrip` `repeat` `replace` `rstrip`
`split` `startsWith` `strip` `substring` `toCharArray` `trim` `upper`

Perhatikan campuran gaya penamaan: sebagian camelCase (`startsWith`, `toCharArray`),
sebagian bergaya Python (`strip`, `lstrip`, `rstrip`, `find`). Hafalkan dari tabel ini,
bukan dari tebakan.

## Rantai Method

Method bisa dirantai selama hasil sebelumnya masih bertipe sesuai:

```jpx
global [kata = "hello world"];

print kata.upper();                          # HELLO WORLD
print kata.replace("o", "0").upper();        # hell0 w0rld
print "  a,b  ".trim().split(",");           # ['a', 'b']
```

**Hati-hati**: `.split()` menghasilkan **list**, jadi method string tidak boleh langsung
menyusulnya:

```jpx
print kata.split(" ").upper();               # ❌ error: 'upper' pada list
print kata.split(" ")[0].upper();            # ✅ HELLO — ambil elemen dulu
```

## Panjang dan Indexing

Panjang string memakai `len()` — method `.length()` **tidak ada**:

```jpx
global [s = "abc"];
print len(s);            # 3
print s[1];              # b   (index karakter, mulai 0)
```

## Interpolasi di Dalam String

Selain method, string mendukung interpolasi `$var` dan `${ekspresi}` — bahkan berantai
dengan method:

```jpx
global [nama = "jpx"];
print "Halo, ${nama.upper()}!";      # Halo, JPX!
```

Rinciannya di [print-dan-interpolasi.md](print-dan-interpolasi.md).

## Escape

Escape sequence lengkap (`\n`, `\t`, `\$`, dll.) dijelaskan di
[tipe-data.md](tipe-data.md).

## Modul Pendamping

Untuk operasi string yang lebih luas (mis. `isDigit`, `isAlpha`, `starts_with`),
impor paket self-hosted `[jpx.string]` — lihat [modul.md](modul.md).

## Halaman Terkait

- [list-dict.md](list-dict.md) — hasil `.split()` dan `.toCharArray()` adalah list
- [fungsi-bawaan.md](fungsi-bawaan.md) — `len()`, `str()`, `ord()`, `chr()`
