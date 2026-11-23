# Referensi Sintaks JPX

Referensi sintaks JPX A2, dipecah menjadi berkas terpisah per topik. Semua contoh pada
folder ini sudah dijalankan dan diverifikasi terhadap interpreter A2.

> **Catatan penting**: JPX **case-sensitive**. Keyword ditulis huruf kecil —
> `print`, bukan `Print`; `global`, bukan `Global`.

---

## Konvensi Dasar yang Berlaku di Semua Halaman

1. **Setiap statement diakhiri titik koma `;`.** Blok yang ditutup `}` juga berfungsi
   sebagai pemisah. `;` yang hilang setelah `global [...]` memberi error yang jelas:
   `Unexpected text after global declaration: 'print "A"' (statements must end with ';')`.
2. **Komentar hanya `#`.** Komentar blok ditulis sebagai beberapa baris `#`.
   `//` **bukan** komentar — itu operator pembagian bulat (`7 // 2` → `3`).
3. **`print` adalah statement, bukan fungsi** — tanpa kurung, satu argumen.
   Detail di [print-dan-interpolasi.md](print-dan-interpolasi.md).
4. **Deklarasi variabel memakai `global [...]`.** Detail di [variabel.md](variabel.md).
5. **String mendukung interpolasi `$var` dan `${ekspresi}`.**
   Detail di [print-dan-interpolasi.md](print-dan-interpolasi.md).

---

## Indeks Berkas

| Berkas | Isi |
|---|---|
| [variabel.md](variabel.md) | Deklarasi `global [...]`, multi-deklarasi, scope lokal vs global, aturan `;` |
| [tipe-data.md](tipe-data.md) | Tujuh tipe data, `type()`, escape sequence, string multi-baris |
| [print-dan-interpolasi.md](print-dan-interpolasi.md) | Statement `print`, interpolasi `$var` dan `${ekspresi}`, perilaku error |
| [operator.md](operator.md) | Aritmetika, perbandingan, logika, `is`/`in`, ternary, pipe `\|>`, operator yang belum ada |
| [kontrol-alur.md](kontrol-alur.md) | `if`/`elif`/`else`, `while`, `for..in`, `break`/`continue`, `switch`, `try`/`catch` |
| [fungsi.md](fungsi.md) | Deklarasi `function`, `return`, rekursi, batasan argumen |
| [class.md](class.md) | Deklarasi `class`, constructor `__init__`, `self`, properti dan method |
| [string.md](string.md) | 17 method string, rantai method, indexing, `len()` |
| [list-dict.md](list-dict.md) | List (index, `push`, modul `array`) dan dict (akses, keanggotaan) |
| [modul.md](modul.md) | `import` dengan `[modul];`, modul bawaan, paket `jpx.*`, search path, `JPX_PATH` |
| [fungsi-bawaan.md](fungsi-bawaan.md) | `len`, `str`, `int`, `float`, `bool`, `type`, `ord`, `chr` |
| [batasan.md](batasan.md) | Daftar fitur yang belum didukung di A2 |

---

## Program Pertama

```jpx
# halo.jpx
global [nama = "JPX", tahun = 2026];

print "Selamat datang di $nama ${tahun}!";
print "2 + 3 = ${2 + 3}";

function kuadrat(x) {
    return x * x;
}
print kuadrat(7);            # 49
```

Jalankan dengan `jpx halo.jpx` (lihat [../cli/perintah-dasar.md](../cli/perintah-dasar.md)).
