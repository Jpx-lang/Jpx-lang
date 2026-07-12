# JPX Programming Language v1.3.0

Versi 1.3 — major update dengan class support, modular structure, dan banyak fitur baru.

## 🎯 Apa yang Baru di v1.3

### Phase A — Core Language Features
- ✅ **Mutable list assignment**: `arr[i] = value` (sebelumnya musti rebuild list)
- ✅ **Integer division**: `17 // 5` → `3`
- ✅ **Multiple assignment**: `a, b = b, a` (swap)
- ✅ **`elif` syntax**: `if {} elif {} else {}` (sebelumnya nested if)
- ✅ **Native string methods**: `s.split()`, `s.strip()`, `s.replace()`, `s.upper()`, `s.contains()`, dll (14 method)

### Phase B — Architecture
- ✅ **Class/OOP support**: `class Name { __init__(self) {...} method(self){...} }`
- ✅ **Modular structure**: `core/exceptions/` sebagai package (satu class per file)
- ✅ **Syntax reference**: `docs/syntax.md` (identitas JPX)
- ✅ **Structure docs**: `docs/structure.md`

### Bug Fixes Critical
- ✅ Auto-conversion string→int dihapus (pakai `int()` eksplisit)
- ✅ `//` bukan komentar lagi (jadinya operator integer division)
- ✅ `tok[0] == "NUM"` sekarang return `True` (sebelumnya return 'NUM'!)
- ✅ Chained access `obj.field.method()` properly fall through
- ✅ String method path tidak tertimpa function call path
- ✅ Class method bisa akses `self.field` dari dalam method lain

## 📦 Cara Pakai

### Run JPX file
```bash
python3 jpx.py examples/demo_lib.jpx
```

### List available modules
```bash
python3 jpx.py --list-modules
```

### Run all tests
```bash
python3 tests/run_tests.py
```

### Install package
```bash
python3 JpXkg.py install <package_name>
```

## 📁 Struktur Direktori

```
jpx-lang-1.3/
├── jpx.py                    # CLI entry point
├── JpXkg.py                  # Package manager
├── core/                     # Interpreter core (modular)
│   └── exceptions/           # Exception package (satu class per file)
├── interpreter/              # Interpreter engine (Python)
│   ├── interpreter.py
│   ├── eval.py
│   ├── function.py
│   ├── importer.py           # v4.0 — relative import, JPX_PATH, circular detection
│   ├── lexer.py              # NEW — tokenizer
│   ├── parser.py             # NEW — recursive descent parser
│   └── astnodes.py           # NEW — AST node definitions
├── library/                  # Standard library (.py + .jpx)
│   ├── array.jpx             # Self-hosted array library
│   ├── mathx.jpx             # Self-hosted math library
│   └── *.py                  # Native Python modules
├── lib/                      # User-installed packages
├── tests/
│   ├── unit/                 # Unit tests
│   ├── e2e/                  # End-to-end tests
│   └── run_tests.py
├── examples/                 # Example JPX programs
│   ├── demo_lib.jpx
│   ├── demo_string.jpx
│   ├── demo_game.jpx
│   ├── mini_interp.jpx       # Mini interpreter written in JPX!
│   └── multi_module/         # Multi-module demo
├── docs/
│   ├── structure.md
│   └── syntax.md             # Language reference
└── LICENSE.txt
```

## 🎯 Test Results

- **8/8 test files pass** (134+ individual assertions)
- **All 5 example programs** run without error
- **Self-hosting milestone**: Library `array.jpx` dan `mathx.jpx` (ditulis dalam JPX) bekerja penuh

## 🚀 Quick Start

Buat file `hello.jpx`:

```jpx
print "Hello, JPX!";
global [name = "World";
print "Hello, $name!";

# Class
class Greeter {
    __init__(self, name) {
        self.name = name;
    }
    greet(self) {
        return "Hello, " + self.name + "!";
    }
}

global [g = Greeter("JPX");
print g.greet();

# Library
[array];
[mathx];
global [nums = [3, 1, 4, 1, 5, 9, 2, 6];
print "Sorted: " + array.join(array.sort(nums), ", ");
print "Fib(10): " + mathx.fib(10);
```

Run:
```bash
python3 jpx.py hello.jpx
```

## 📜 License

MIT License — lihat `LICENSE.txt`.
