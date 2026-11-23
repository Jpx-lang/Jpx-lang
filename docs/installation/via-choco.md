# Instalasi Via Chocolatey — Coming Soon

> ⏳ **Status: BELUM TERSEDIA.**
> Paket `Jpx-cli` sedang disiapkan untuk Chocolatey dan **belum** bisa dipasang saat
> dokumen ini ditulis. Halaman ini dipublikasikan lebih awal agar struktur dokumentasi
> sudah lengkap; perintah di bawah akan aktif begitu paket rilis.

## Rencana Perintah

Setelah paket terbit, pengguna Windows dengan Chocolatey akan memasang JPX dengan:

```powershell
choco install Jpx-cli
```

Verifikasi:

```powershell
jpx --version
```

Pembaruan dan penghapusan:

```powershell
choco upgrade Jpx-cli
choco uninstall Jpx-cli
```

## Persiapan (Ketika Paket Sudah Rilis)

1. Pasang [Chocolatey](https://chocolatey.org/install) jika belum ada.
2. Jalankan `choco install Jpx-cli` dari terminal yang memiliki izin administrator.
3. Chocolatey menaruh `jpx.exe` beserta folder `library/` pada lokasi paket dan
   menambahkannya ke `PATH`, sehingga `jpx` langsung bisa dipanggil.

## Alternatif Sementara

Sementara menunggu paket Chocolatey, gunakan salah satu metode yang sudah aktif:

- [Via repository](via-repository.md) — unduh `jpx.exe` / `jpx-win64.zip` dari halaman
  rilis GitHub (tanpa Python), atau clone source dan jalankan dengan Python.
- [Via shogun](via-shogun.md) — jika Anda memakai shogun.
