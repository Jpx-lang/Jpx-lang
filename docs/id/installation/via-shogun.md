# Instalasi Via Shogun

Jika Anda sudah memakai **shogun** sebagai pengelola paket/alat CLI, JPX dapat dipasang
langsung dari katalog shogun tanpa perlu mengunduh rilis manual.

## Langkah

1. Pastikan shogun sudah terpasang dan bisa dipanggil:

   ```bash
   shogun --version
   ```

2. Pasang JPX:

   ```bash
   shogun install jpx-cli
   ```

3. Verifikasi instalasi:

   ```bash
   jpx --version
   ```

   Output yang diharapkan diawali dengan:

   ```text
   JPX A2 - A exclusive version
   ```

## Memperbarui dan Menghapus

Gunakan perintah bawaan shogun untuk mengelola paket, sesuai versi shogun Anda:

```bash
shogun update jpx-cli     # perbarui ke versi terbaru (jika didukung)
shogun uninstall jpx-cli  # hapus instalasi (jika didukung)
```

## Catatan Penting

- **Nama paket**: perintah di halaman ini memakai nama paket `jpx-cli`. Nama persisnya
  mengikuti katalog shogun yang Anda gunakan — jika `shogun install jpx-cli` tidak
  ditemukan, cari daftar paketnya dengan perintah pencarian milik shogun (mis.
  `shogun search jpx`) lalu sesuaikan nama paketnya.
- **Struktur berkas**: apapun metode instalasi, folder `library/` tetap harus berada di
  samping binary `jpx` (lihat [via-repository.md](via-repository.md)). Jika shogun
  menaruh berkas di lokasi kustom, pastikan struktur itu utuh.
- **Alternatif**: jika metode ini bermasalah, gunakan metode
  [via repository](via-repository.md) yang selalu memakai rilis resmi terbaru.

## Berikutnya

- Jalankan skrip pertama: [cli/perintah-dasar.md](../cli/perintah-dasar.md)
