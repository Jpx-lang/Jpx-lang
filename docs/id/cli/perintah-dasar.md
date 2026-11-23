# Perintah Dasar CLI `jpx`

Semua output di halaman ini adalah output nyata dari CLI A2 (versi Python pada contoh
menyesuaikan sistem Anda).

## Menjalankan Skrip

```bash
jpx nama_file.jpx
```

Contoh — berkas `halo.jpx`:

```jpx
global [nama = "Dunia"];
print "Halo, $nama!";
```

Diambil sebagai:

```text
Halo, Dunia!
```

Detail penting saat menjalankan:

- Folder tempat berkas `.jpx` berada otomatis ditambahkan ke **search path modul**, jadi
  `[modul];` bisa mengimpor berkas `.jpx`/`.py` yang ada di folder yang sama
  (import relatif).
- Runtime error ditampilkan sebagai `Runtime Error: <pesan>` dan program keluar dengan
  exit code `1`. Gunakan `try/catch` untuk menangkapnya di dalam skrip.
- Tekan Ctrl+C untuk menginterupsi; keluar dengan exit code `130`.

## `jpx --version` / `-v`

```bash
jpx --version
```

```text
JPX A2 - A exclusive version
Python: 3.12.16
Root: /lokasi/instalasi/jpx
Library: /lokasi/instalasi/jpx/library
User lib: /lokasi/instalasi/jpx/lib
```

Berguna untuk memastikan CLI yang terpanggil benar-benar versi A2 dan melihat di mana
`library/` dan `lib/` dicari.

## `jpx --help` / `-h`

```text
JPX Programming Language
Version: JPX A2 - A exclusive version

Usage:
  jpx <file.jpx>              Run a JPX script
  jpx --version, -v            Show version information
  jpx --help, -h               Show this help message
  jpx --info                    Show system information

Examples:
  jpx script.jpx
  jpx examples/hello.jpx

Environment:
  JPX_PATH                      Additional library paths

More info: https://github.com/alzzmetth/Jpx-lang
```

> **Catatan**: `--list-modules` dan `--jpx-interpreter` **berfungsi** tetapi belum
> dicantumkan di teks `--help`. Dokumen ini adalah referensi lengkapnya.

## `jpx --info`

Informasi sistem yang lebih lengkap dari `--version`: path root/pustaka, status keberadaan
tiap folder (`✓`/`✗`), platform, versi Python, dan isi `JPX_PATH` bila diset.

```bash
jpx --info
```

Gunakan perintah ini pertama kali setelah instalasi untuk memastikan struktur folder
benar (ingat: `library/` harus di samping executable).

## `jpx --list-modules`

Menampilkan semua modul yang terdeteksi di semua search path, ditag `[PY]` (implementasi
Python) atau `[JPX]` (ditulis dalam JPX sendiri), diikuti total dan urutan search path:

```text
Available JPX modules:
=================================================
  [PY] json            (library/json.py)
  [PY] math            (library/math.py)
  [JPX] array          (library/array.jpx)
  [JPX] mathx          (library/mathx.jpx)
  ...

Total: 27 modules

Search paths (priority order):
  1. ✗ /folder/kerja/lib
  2. ✓ /lokasi/instalasi/jpx/library
```

Jika modul yang Anda buat tidak muncul di sini, skrip Anda juga tidak akan bisa
mengimpornya — perbaiki letak berkasnya atau tambahkan foldernya ke `JPX_PATH`.
Urutan prioritas lengkap dijelaskan di [../syntax/modul.md](../syntax/modul.md).

## `jpx --jpx-interpreter <file.jpx>`

Menjalankan skrip lewat **interpreter self-hosted** (lexer, parser, AST, dan evaluator
yang ditulis dalam JPX sendiri, di folder `bootstrap/`). Ini fitur **eksperimental**
untuk mendemonstrasikan progres self-hosting — outputnya diawali banner:

```text
[JPX-Interpreter] Running halo.jpx with self-hosted interpreter
[JPX-Interpreter] (experimental — subset features only)
```

Batasan yang sudah dinyatakan resmi:

- Import modul tidak didukung (evaluator belum punya module loader).
- Instansiasi class hanya minimal.
- Try-catch tidak didukung penuh.
- Method string native tidak didukung.

**Peringatan**: pada jalur ini kegagalan bisa terjadi **tanpa pesan** — statement yang
gagal dieksekusi bisa hilang dari output tanpa error. Gunakan interpreter utama
(`jpx file.jpx`) untuk pekerjaan nyata; pakai `--jpx-interpreter` hanya untuk demo dan
pengujian komponen bootstrap.

## Variabel Lingkungan `JPX_PATH`

Menambah direktori pencarian modul. Contoh:

```bash
# Linux / macOS
export JPX_PATH="/home/aku/modul-jpx:/opt/jpx-modul"
jpx app.jpx

# Windows (PowerShell)
$env:JPX_PATH = "C:\modul-jpx;C:\opt\jpx-modul"
jpx app.jpx
```

Cek efeknya lewat bagian `Search paths` pada `jpx --list-modules`.

## Menjalankan Tanpa Instalasi (Dari Source)

Jika Anda clone repository, semua perintah di atas bisa dipanggil lewat Python langsung:

```bash
python3 jpx.py script.jpx
python3 tests/run_tests.py     # test suite resmi
```

## Halaman Terkait

- [jpxkg.md](jpxkg.md) — memasang paket dengan package manager
- [../syntax/modul.md](../syntax/modul.md) — urutan search path dan pembuatan modul
- [../installation/via-repository.md](../installation/via-repository.md) — instalasi
