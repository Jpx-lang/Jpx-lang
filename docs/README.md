# Dokumentasi JPX

Selamat datang di dokumentasi resmi bahasa pemrograman **JPX** versi **A2**.

JPX adalah bahasa skrip dinamis yang menggabungkan wajah beberapa bahasa populer:
blok kurung kurawal dan titik koma (gaya C/JavaScript), kata kunci ringkas (gaya Python),
interpolasi string `$var` (gaya PHP/bash), operator pipeline `|>` (gaya Elixir), dan
`switch` tanpa fall-through (gaya Go). JPX dirancang untuk eksperimen, automasi ringan,
dan eksplorasi konsep runtime yang minimalis.

> **Catatan penting**: JPX **case-sensitive**. Semua keyword ditulis huruf kecil —
> `print`, bukan `Print`; `global`, bukan `Global`.

---

## Peta Dokumentasi

| Folder / Berkas | Isi |
|---|---|
| [`installation/`](installation/README.md) | Cara memasang JPX: via repository (release biner atau source), via `shogun install`, dan `choco install Jpx-cli` (coming soon) |
| [`syntax/`](syntax/README.md) | Referensi sintaks lengkap, dipecah per topik: variabel, tipe data, print & interpolasi, operator, kontrol alur, fungsi, class, string, list & dict, modul, fungsi bawaan, dan batasan |
| [`cli/`](cli/README.md) | Cara memakai CLI `jpx`: menjalankan skrip, opsi-opsi command line, variabel lingkungan, exit code, dan package manager `jpxkg` |

---

## Mulai Cepat

Setelah JPX terpasang (lihat [installation/README.md](installation/README.md)), buat
berkas `halo.jpx`:

```jpx
global [nama = "Dunia"];
print "Halo, $nama!";
print "Sekarang: ${2025 + 1}";
```

Jalankan:

```bash
jpx halo.jpx
```

Output:

```text
Halo, Dunia!
Sekarang: 2026
```

---

## Status Versi

Dokumentasi ini ditulis untuk **JPX A2** ("A exclusive version"). Seluruh contoh sintaks
pada folder `syntax/` sudah dijalankan dan diverifikasi terhadap interpreter A2. Fitur
yang **belum** didukung dikumpulkan jujur di [syntax/batasan.md](syntax/batasan.md) —
baca dulu halaman itu supaya tidak menabrak batasan yang sudah diketahui.

Dokumentasi lama (`docs.md` dan `installation.md` versi v1.0) sudah tidak mencerminkan
sintaks A2 (masih memakai `Global`/`Print` berhuruf kapital) dan digantikan oleh dokumen
di folder ini.

---

## Tautan Resmi

- Repository: <https://github.com/Jpx-lang/Jpx-lang>
- Halaman rilis: <https://github.com/Jpx-lang/Jpx-lang/releases>
- Situs proyek: <https://jpx-lang.netlify.app>
- Halaman unduhan paket (jpxkg): <https://jpxkg.netlify.app/>
