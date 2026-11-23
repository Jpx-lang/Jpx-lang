# Variabel & `global`

Semua deklarasi variabel di JPX memakai keyword `global` di dalam kurung siku, dan
**wajib diakhiri titik koma** `;`.

## Deklarasi

```jpx
global [name = "Alice"];
global [age = 30];
global [pi = 3.14];
```

Variabel yang dideklarasikan dengan `global [...]` bisa dipanggil di bagian mana pun
dalam skrip.

## Deklarasi Banyak Sekaligus

Pisahkan pasangan `nama = nilai` dengan koma di level atas:

```jpx
global [a = 1, b = 2, c = 3];
global [list1 = [1, 2], list2 = [3, 4]];   # koma di dalam list aman
global [msg = "a,b", flag = true];         # koma di dalam string aman
```

Pasangan dievaluasi **berurutan**, jadi pasangan berikutnya boleh membaca pasangan
sebelumnya:

```jpx
global [width = 10, area = width * 5];     # area = 50
```

## Assignment Biasa (Lokal)

Di dalam function, assignment tanpa `global` bersifat **lokal** — variabelnya hilang
setelah function selesai:

```jpx
function hitung() {
    total = 10;            # lokal — hilang setelah function selesai
    total = total + 5;
    return total;
}
```

## `global` di Dalam Function

Untuk menulis ke variabel global dari dalam function, pakai `global [...]` di dalamnya:

```jpx
global [counter = 0];

function tambah() {
    global [counter = counter + 1];
}

tambah();
tambah();
print counter;              # 2
```

`counter` di sisi kanan dibaca dari nilai global **terkini**, bukan snapshot saat
function dibuat.

## Urutan Pembacaan Saat `global [...]`

Saat interpreter mengevaluasi nilai di dalam `global [...]`, urutan pencariannya:

1. **Parameter** function yang sedang berjalan — prioritas tertinggi
   (parameter bernama `arr` tidak ketimpa oleh `global [arr = ...]`).
2. **Global terkini**.
3. **Local / closure** lainnya.

## Aturan Penulisan `;`

Setiap statement harus diakhiri `;`. Jika `;` hilang setelah `global [...]`, interpreter
memberi error yang jelas — bukan diam-diam menelan kode berikutnya:

```text
Unexpected text after global declaration: 'print "A"' (statements must end with ';')
```

## Yang Perlu Diingat

- Keyword `let` **tidak ada** di JPX — deklarasi selalu `global [...]`.
- Keyword `global` ditulis huruf kecil semua; `Global` akan ditolak (case-sensitive).
- Tidak ada konstanta "immutable": nilai variabel global bisa ditulis ulang lewat
  assignment atau `global [...]` di dalam function.

## Halaman Terkait

- [tipe-data.md](tipe-data.md) — tipe nilai yang bisa disimpan
- [kontrol-alur.md](kontrol-alur.md) — memakai variabel di kondisi dan loop
- [batasan.md](batasan.md) — daftar fitur yang belum didukung
