# Class

JPX mendukung pemrograman berorientasi objek dengan gaya Python: constructor
`__init__` dan parameter `self` yang ditulis eksplisit di setiap method.

## Deklarasi dan Instansiasi

```jpx
class Point {
    function __init__(self, x, y) {
        self.x = x;
        self.y = y;
    }

    function jarak(self) {
        return self.x * self.x + self.y * self.y;
    }
}

global [p = Point(3, 4)];
print p.x;                  # 3
print p.jarak();            # 25
```

Aturan penting:

- `self` ditulis **eksplisit** sebagai parameter pertama setiap method, dan method
  dipanggil tanpa mengisi `self` (`p.jarak()`, bukan `p.jarak(p)`).
- `__init__` adalah constructor — dipanggil otomatis saat instansiasi.
- Instance dibuat dengan memanggil nama class seperti fungsi: `Point(3, 4)`.
- Properti instance disimpan lewat `self.nama = nilai` di dalam method.
- Akses properti memakai titik: `p.x`; memanggil method memakai titik dan kurung:
  `p.jarak()`.

## Contoh Lain: Counter

```jpx
class Counter {
    function __init__(self) {
        self.n = 0;
    }
    function naik(self) {
        self.n = self.n + 1;
        return self.n;
    }
}

global [c = Counter()];
c.naik();
c.naik();
print c.n;                  # 2
```

## Memanggil Fungsi Luar dari Dalam Method

Method bisa membaca fungsi global yang sudah dideklarasikan sebelum class dipakai:

```jpx
function desimal(n) {
    return int(n);
}

class Angka {
    function __init__(self, v) {
        self.v = desimal(v);
    }
}

global [a = Angka("7")];
print a.v;                  # 7
```

## Catatan

- Pewarisan (`extends` / `super`) belum didukung di A2.
- Di jalur eksperimental `--jpx-interpreter` (self-hosted), instansiasi class hanya
  mendukung subset — lihat [../cli/perintah-dasar.md](../cli/perintah-dasar.md).

## Halaman Terkait

- [fungsi.md](fungsi.md) — deklarasi function yang juga dipakai sebagai method
- [variabel.md](variabel.md) — scope `self`, lokal, dan global
