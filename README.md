# JPX
<img width="1024" height="1024" alt="1000227244" src="https://github.com/user-attachments/assets/3e61732d-77e6-4a47-8195-5b7350946df3" />


JPX adalah bahasa scripting sederhana yang dirancang untuk eksperimen, automasi ringan, dan eksplorasi konsep runtime yang minimalis. Fokus utamanya adalah sintaks yang mudah dibaca serta eksekusi yang cepat tanpa kompleksitas berlebihan.

---

# ✨ Features

- Sintaks sederhana dan mudah dipahami
- Deklarasi variabel global yang jelas
- Interpolasi variabel langsung dalam string
- Ringan dan minimal dependency
- Cocok untuk eksperimen scripting

---

# 📦 Installation

Unduh binary JPX dari halaman release.

```
jpx <file.jpx>
```

Pastikan binary berada di PATH atau jalankan langsung dari direktori file.

---

# 📜 Syntax Overview

JPX memiliki sintaks yang sederhana dan langsung.

## Global Variable

Deklarasi variabel global menggunakan keyword `Global`.

```
Global [name = "john"];
```

Variabel tersebut dapat dipanggil di bagian mana pun dalam script.

---

## Print Statement

Untuk menampilkan output gunakan `Print`.

```
Print "Hello World";
```

---

## Variable Interpolation

JPX mendukung penggunaan variabel langsung di dalam string menggunakan `$`.

```
Global [name = "john"];

Print "Name : $john";
```

Output:

```
Name : john
```

---

# 📄 Example Script

Contoh file `example.jpx`:

```
Global [name = "john"];

Print "Name : $john";
Print "Welcome to JPX";
```

Jalankan:

```
jpx example.jpx
```

Output:

```
Name : john
Welcome to JPX
```

---

# 📂 Project Structure

struktur repo:

```
JPX/
│
├── README.md
├── LICENSE
├── bin/
│   └── jpx
│
└── examples/
    └── hello.jpx
```

---

# 📚 Documentation

Dokumentasi tambahan akan tersedia melalui:

- Wiki repository
- Artikel tutorial
- Contoh script

---

# 🧪 Use Cases

Beberapa penggunaan JPX:

- Eksperimen bahasa scripting
- Automasi sederhana
- Pembelajaran konsep interpreter
- Prototyping logic

---

# 🤝 Contributing

Kontribusi sangat terbuka.

Beberapa cara berkontribusi:

- Menambahkan contoh script
- Membuat dokumentasi
- Melaporkan bug
- Memberikan ide fitur baru

---

# 🪪 License

Proyek ini dirilis di bawah lisensi **MIT License**.

Anda bebas menggunakan, memodifikasi, dan mendistribusikan sesuai dengan ketentuan lisensi MIT.

---

# 🚀 Roadmap

Beberapa rencana pengembangan JPX:

- Penambahan kontrol alur
- Fungsi dasar
- Modul system
- Dokumentasi lebih lengkap
- CLI tooling tambahan

---

# 📢 Community

Ikuti perkembangan JPX melalui:

- Repository
- Wiki
- Channel komunitas

---

JPX dibuat sebagai eksplorasi bahasa scripting yang sederhana dan fleksibel.
