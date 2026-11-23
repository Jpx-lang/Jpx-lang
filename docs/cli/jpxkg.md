# `jpxkg` — Package Manager JPX

`jpxkg` adalah pengelola paket JPX (versi 1.0). Paket diambil dari katalog berbasis
`index.json`, diunduh, diverifikasi SHA256, lalu dipasang ke folder `lib/` yang ikut
menjadi search path modul JPX. Katalognya dapat diakses juga via web di
<https://jpxkg.netlify.app/>.

## Perintah

```bash
jpxkg install <paket>     # pasang paket dari katalog
jpxkg -v                  # tampilkan versi jpxkg
```

Tanpa argumen, `jpxkg` menampilkan ringkasan bantuan singkat.

### Contoh

```bash
jpxkg install contopaket
```

Output khas proses pemasangan:

```text
📦 Downloading contopaket...
  Progress: 100%
  Verifying SHA256...
✅ SHA256 OK
✅ Installed contopaket to lib/contopaket.py (12.3 KB)
```

## Bagaimana Pemasangan Bekerja

1. `jpxkg` membaca `index.json` di folder instalasi JPX.
2. Paket dicari berdasarkan `name`; jika tidak ada, daftar paket yang tersedia
   ditampilkan agar mudah mencari.
3. Berkas diunduh dari `download_url` milik paket.
4. Bila `sha256` tersedia di katalog, berkas diverifikasi; **checksum mismatch**
   memunculkan peringatan dan konfirmasi — sebaiknya jawab `n` bila Anda tidak yakin.
5. Berkas dipasang ke `install_path` (umumnya `lib/<nama>.py`). Bila berkas sudah ada,
   `jpxkg` meminta konfirmasi sebelum menimpa.
6. Bila paket punya `dependencies` (dependensi Python), `jpxkg` menampilkan daftarnya
   untuk dipasang manual lewat pip:

   ```text
   ⚠️ Dependencies:
     • colorama (pip install colorama)
   ```

## Format `index.json`

`jpxkg` membaca struktur berikut dari `index.json`:

```json
{
  "modules": [
    {
      "name": "contopaket",
      "download_url": "https://contoh.example/contopaket.py",
      "sha256": "algoritma-hash-hex-64-karakter",
      "install_path": "lib/contopaket.py",
      "dependencies": ["colorama"]
    }
  ]
}
```

Semua kunci opsional kecuali `name` dan `download_url`. Setelah `index.json` ada di
folder instalasi, `[contopaket];` bisa langsung diimpor dari skrip JPX karena folder
`lib/` berada di search path (urutan prioritas: folder skrip → `lib/` → `JPX_PATH` →
`library/` bawaan — lihat [../syntax/modul.md](../syntax/modul.md)).

## Catatan Keamanan

- Paket dari katalog adalah kode Python yang dieksekusi saat diimpor — pasang hanya dari
  sumber yang Anda percaya.
- Selalu biarkan verifikasi SHA256 berjalan; bila checksum tidak cocok, hentikan
  pemasangan dan laporkan ke pemilik katalog.
- `jpxkg` saat ini hanya menyediakan perintah `install` (belum ada `search`, `update`,
  atau `uninstall`). Menghapus paket dilakukan manual dengan menghapus berkasnya di
  folder `lib/`.

## Halaman Terkait

- [perintah-dasar.md](perintah-dasar.md) — opsi CLI `jpx` dan `--list-modules`
- [../syntax/modul.md](../syntax/modul.md) — search path dan modul kustom
- Katalog web: <https://jpxkg.netlify.app/>
