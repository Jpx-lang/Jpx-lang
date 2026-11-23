# Fungsi

Fungsi dideklarasikan dengan keyword `function`, blok `{ }`, dan parameter tanpa tipe:

```jpx
function jumlah(a, b) {
    return a + b;
}

print jumlah(1, 2);         # 3
```

## Fungsi Tanpa `return`

Function tanpa `return` tetap sah — ia mengembalikan null secara internal:

```jpx
function sapa() {
    print "halo dari function";
}
sapa();                     # halo dari function
```

## Rekursi

Rekursi didukung penuh:

```jpx
function fib(n) {
    if n < 2 { return n; }
    return fib(n - 1) + fib(n - 2);
}

print fib(10);              # 55.0
```

Catatan: hasilnya `55.0` (float) karena operator `-` menghasilkan float — lihat
[tipe-data.md](tipe-data.md). Bungkus dengan `int(fib(10))` bila butuh integer.

## `return` Kosong

`return` tanpa nilai keluar lebih awal dari fungsi:

```jpx
function cek(x) {
    if x < 0 { return; }
    print "positif";
}
```

## Variabel di Dalam Fungsi

- Assignment biasa bersifat **lokal** (hilang saat fungsi selesai).
- `global [nama = nilai];` di dalam fungsi menulis ke variabel global.
- Rinciannya di [variabel.md](variabel.md).

```jpx
global [counter = 0];

function tambah() {
    global [counter = counter + 1];
}

tambah();
tambah();
print counter;              # 2
```

## Batasan yang Perlu Diketahui

- **Default argument belum didukung.** `function f(a, b = 9)` gagal dengan
  `Variable 'b' not defined`. Sediakan argumen secara eksplisit dari pemanggil, atau
  terima null dan isi manual:

  ```jpx
  function sapa(nama) {
      if nama is null { nama = "Dunia"; }
      print "Halo, $nama!";
  }
  sapa(null);      # Halo, Dunia!
  sapa("JPX");     # Halo, JPX!
  ```

- Tidak ada variadic (`...args`) dan tidak ada lambda di interpreter utama.
- Fungsi dipanggil dengan kurung `nama(arg)`; tanpa kurung tidak ada mekanisme
  reference-function yang stabil — untuk komposisi, gunakan pipe `|>` (lihat
  [operator.md](operator.md)).

## Halaman Terkait

- [kontrol-alur.md](kontrol-alur.md) — `if` dan loop di dalam fungsi
- [class.md](class.md) — method di dalam class
- [print-dan-interpolasi.md](print-dan-interpolasi.md) — memanggil fungsi di `${...}`
