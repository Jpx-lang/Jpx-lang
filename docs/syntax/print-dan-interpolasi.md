# Output: `print` dan Interpolasi String

## `print` adalah Statement

`print` **bukan fungsi** — jadi tidak boleh memakai kurung, dan tidak menerima banyak
argumen.

```jpx
print "halo";                 # ✅  -> halo
print 42;                     # ✅  -> 42
print "a" + "b";              # ✅  -> ab
print("halo");                # ❌  Runtime Error: Undefined variable: print
print "a", "b";               # ❌  Runtime Error: Invalid expression
```

Pesan `Undefined variable: print` muncul karena JPX membaca `print(...)` sebagai
pencarian variabel bernama `print`. Ingat: panggil `print` tanpa kurung. Untuk mencetak
beberapa nilai, gabungkan dengan `+` (dan `str()` bila perlu):

```jpx
print "Umur: " + str(30);
```

`print null` mencetak baris kosong (null dicetak sebagai string kosong).

## Interpolasi String

Dua bentuk didukung dan boleh dicampur dalam satu string:

| Bentuk | Hasil |
|---|---|
| `$nama` | isi variabel sederhana |
| `${ekspresi}` | hasil ekspresi apa pun: aritmetika, method call, pemanggilan fungsi |

```jpx
global [name = "JPX"];
global [age = 30];
global [nums = [3, 1, 4]];

print "Halo, $name!";                          # Halo, JPX!
print "Tahun depan: ${age + 1}";               # Tahun depan: 31
print "Huruf besar: ${name.upper()}";          # Huruf besar: JPX
print "Jumlah: ${len(nums)}";                  # Jumlah: 3
print "n = $age, n+1 = ${age + 1}";            # keduanya dalam 1 string
```

Untuk menampilkan tanda dolar literal, escape dengan `\$`:

```jpx
print "Harga: \$5";        # Harga: $5
```

Interpolasi `$nama` mengikuti nama setelah `$` sampai karakter yang bukan bagian dari
identifier, sehingga `$age` di tengah kalimat aman dibaca utuh.

## Perilaku Error di Dalam `${...}`

Kesalahan pada ekspresi interpolasi **tidak menghentikan program**. Error ditampilkan
sebagai teks `<error:...>` tepat di posisi interpolasi:

```jpx
global [x = 1];
print "tes: ${x + tidakada}";
# -> tes: <error:Variable 'tidakada' not defined. Use 'global [tidakada = value]' to declare it.>
print "selesai";          # tetap dieksekusi
```

Ini berguna untuk melihat penyebabnya langsung di output, tetapi juga berarti program
**tidak gagal keras** walau ada ekspresi yang salah di string — periksa output Anda,
terutama bila string itu ditulis ke berkas atau dikirim ke tempat lain.

## Halaman Terkait

- [tipe-data.md](tipe-data.md) — escape sequence dan format output per tipe
- [string.md](string.md) — method string yang bisa dipakai di dalam `${...}`
- [fungsi.md](fungsi.md) — memanggil fungsi di dalam `${...}`
