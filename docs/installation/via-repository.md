# Instalasi Via Repository

Ini adalah metode paling pasti: mengambil JPX langsung dari repository GitHub resmi
[Jpx-lang/Jpx-lang](https://github.com/Jpx-lang/Jpx-lang). Ada dua jalur:

1. **Jalur A — unduh binary rilis** (tanpa Python). Direkomendasikan untuk pengguna umum.
2. **Jalur B — clone source dan jalankan dengan Python**. Cocok jika Anda ingin membaca,
   mengubah, atau ikut mengembangkan JPX.

---

## Jalur A — Unduh Binary Rilis (Tanpa Python)

Binary dibangun dengan PyInstaller 6.22.3 dan membawa runtime Python di dalamnya, jadi
mesin target tidak perlu memasang Python.

### Langkah

1. Buka halaman rilis: <https://github.com/Jpx-lang/Jpx-lang/releases>
2. Pilih rilis **A2**.
3. Unduh aset sesuai sistem Anda:

   | Aset | Untuk |
   |---|---|
   | `jpx.exe` | Windows x64 (executable saja) |
   | `jpx-win64.zip` | Windows x64 (executable + `library/` + `bootstrap/` + docs) |
   | `jpx-x86-linux.zip` | Linux x86-64 (executable + `library/` + `bootstrap/` + docs) |

4. Ekstrak arsip ke folder permanen, misalnya:
   - Windows: `C:\Tools\jpx\`
   - Linux: `~/.local/share/jpx/` atau `/opt/jpx/`
5. Tambahkan folder tersebut ke `PATH` agar perintah `jpx` bisa dipanggil dari mana saja,
   atau panggil dengan path lengkap.

### Penting: Jangan Pisahkan Folder `library/`

Interpreter mencari modul bawaan relatif terhadap lokasi executable. Folder `library/`
(berisi modul seperti `fs`, `json`, `time`, `requests`) dan `bootstrap/` harus tetap di
samping `jpx`. Jika dipindah, skrip yang mengimpor modul akan gagal dengan
`Module not found` walau binary-nya berjalan normal.

### Verifikasi

```bash
jpx --version
```

Lihat [README instalasi](README.md) untuk contoh output lengkap.

---

## Jalur B — Clone dan Jalankan Dari Source

### Langkah

1. Clone repository:

   ```bash
   git clone https://github.com/Jpx-lang/Jpx-lang.git
   cd Jpx-lang
   ```

2. Masuk ke folder `jpx-lang/` — di sinilah interpreter dan pustaka berada:

   ```bash
   cd jpx-lang
   ```

3. Jalankan skrip JPX langsung dengan Python (tanpa build):

   ```bash
   python3 jpx.py nama_file.jpx
   ```

4. (Opsional) Jadikan perintah `jpx` bisa dipanggil langsung dengan membuat alias atau
   wrapper, misalnya di Linux:

   ```bash
   sudo ln -s "$(pwd)/jpx.py" /usr/local/bin/jpx
   ```

   Catatan: wrapper berbasis symlink membutuhkan shebang yang benar dan izin eksekusi
   (`chmod +x jpx.py`). Jika tidak mau repot, selalu jalankan dengan
   `python3 jpx.py <file.jpx>`.

### Verifikasi dan Uji

```bash
python3 jpx.py --version          # versi dan lokasi pustaka
python3 jpx.py --list-modules     # daftar modul + search path
python3 tests/run_tests.py        # test suite resmi (harus lulus hampir semua)
```

Terakhir terverifikasi: `run_tests.py` lulus 25 dari 26 pengujian, `run_e2e.py` lulus
seluruhnya.

### Struktur yang Perlu Anda Tahu

```text
jpx-lang/
├── jpx.py            # entry point CLI
├── interpreter/      # mesin eksekusi (interpreter, eval, parser, lexer, importer)
├── library/          # modul bawaan native (.py) dan self-hosted (.jpx)
├── bootstrap/        # interpreter self-hosted eksperimental (ditulis dalam JPX)
├── tests/            # test suite (unit, e2e, bootstrap)
└── examples/         # contoh program
```

---

## Pemecahan Masalah Umum

| Gejala | Penyebab | Solusi |
|---|---|---|
| `Error: File 'x.jpx' not found` | Path salah / bukan di folder kerja | Jalankan dari folder berkas, atau pakai path lengkap |
| `Module not found` saat import | Folder `library/` terpisah dari executable | Kembalikan `library/` di samping `jpx` |
| Modul tertentu tidak muncul di `--list-modules` | Folder modul kustom belum ada di search path | Cek `--list-modules` bagian bawah; tambahkan folder lewat `JPX_PATH` |
| `No module named 'colorama'` | Modul `[color]` butuh pip | `pip install colorama` |
| `No module named 'win32api'` | Modul `win32*` butuh pywin32 (khusus Windows) | `pip install pywin32` |

## Berikutnya

- Pasang paket tambahan dengan `jpxkg`: [cli/jpxkg.md](../cli/jpxkg.md)
- Semua opsi CLI: [cli/perintah-dasar.md](../cli/perintah-dasar.md)
