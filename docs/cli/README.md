# CLI `jpx`

Semua interaksi dengan JPX dilakukan lewat perintah `jpx`. Folder ini menjelaskan
setiap perintah, opsi, variabel lingkungan, exit code, dan package manager `jpxkg`.

## Daftar Perintah

| Perintah | Fungsi |
|---|---|
| `jpx <file.jpx>` | Jalankan skrip JPX |
| `jpx --version`, `-v` | Tampilkan versi dan lokasi pustaka |
| `jpx --help`, `-h` | Tampilkan bantuan |
| `jpx --info` | Informasi sistem dan status folder instalasi |
| `jpx --list-modules` | Daftar semua modul yang terdeteksi + search path |
| `jpx --jpx-interpreter <file.jpx>` | Jalankan dengan interpreter self-hosted (eksperimental) |

Rincian tiap opsi dengan contoh output nyata:
[perintah-dasar.md](perintah-dasar.md).

## Variabel Lingkungan

| Variabel | Fungsi |
|---|---|
| `JPX_PATH` | Menambah direktori pencarian modul (dipisah `;` di Windows, `:` di Linux) |

## Exit Code

| Kode | Arti |
|---|---|
| `0` | Skrip selesai normal |
| `1` | Runtime error / berkas tidak ditemukan |
| `130` | Eksekusi diinterupsi (Ctrl+C) |

Exit code ini berguna untuk scripting: `jpx job.jpx && echo "sukses"`.

## Package Manager

Paket JPX dipasang dengan `jpxkg install <paket>` — pemasangan berbasis `index.json`,
dengan verifikasi SHA256. Lihat [jpxkg.md](jpxkg.md).

## Halaman Instalasi

Belum memasang JPX? Mulai dari [../installation/README.md](../installation/README.md).
