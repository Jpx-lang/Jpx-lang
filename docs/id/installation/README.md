# Instalasi JPX

Halaman ini merangkum semua cara resmi untuk memasang JPX A2. Pilih satu metode sesuai
kebutuhan Anda — ketiganya menghasilkan CLI `jpx` yang sama.

## Ringkasan Metode

| Metode | Perintah / Langkah | Cocok untuk | Status |
|---|---|---|---|
| [Via repository](via-repository.md) | Unduh rilis biner, atau `git clone` + Python | Semua pengguna; cara paling pasti | ✅ Tersedia |
| [Via shogun](via-shogun.md) | `shogun install` dari katalog shogun | Pengguna yang sudah memakai shogun | ✅ Tersedia |
| [Via Chocolatey](via-choco.md) | `choco install Jpx-cli` | Pengguna Windows yang memakai Chocolatey | ⏳ **Coming soon** |

## Persyaratan

**Menggunakan binary rilis** (direkomendasikan):

- Windows x64 atau Linux x86-64.
- Tidak perlu Python — binary dibangun dengan PyInstaller dan membawa runtime Python
  di dalamnya.
- Ikuti aturan penting: folder `library/` harus tetap berada **di samping** executable,
  karena interpreter mencari modul bawaan relatif terhadap lokasinya sendiri.

**Menjalankan dari source:**

- Python 3.x (dipakai dan diuji pada Python 3.12).
- Git (untuk meng-clone repository).
- Modul bawaan JPX sebagian besar hanya memakai pustaka standar Python. Dua pengecualian:
  `[color]` membutuhkan paket pip `colorama`, dan modul Windows (`win32sys`, `win32ui`)
  membutuhkan `pywin32` serta hanya berjalan di Windows.

## Verifikasi Setelah Instalasi

Apapun metodenya, verifikasi dengan:

```bash
jpx --version
```

Output yang diharapkan (versi Python pada baris kedua menyesuaikan sistem Anda):

```text
JPX A2 - A exclusive version
Python: 3.12.16
Root: <lokasi instalasi JPX>
Library: <lokasi instalasi JPX>/library
User lib: <lokasi instalasi JPX>/lib
```

Jika perintah `jpx` belum dikenali, tambahkan folder instalasi ke `PATH` sistem Anda,
atau jalankan dengan path lengkap (mis. `./jpx` di Linux, `jpx.exe` di Windows).

## Berikutnya

- Jalankan skrip pertama Anda: [cli/perintah-dasar.md](../cli/perintah-dasar.md)
- Pelajari sintaks: [syntax/README.md](../syntax/README.md)
