# JPX v1.3.0 Changelog

Released: 2026-07-12

## ✨ New Features

### Phase A — Core Language

#### Mutable List Assignment
```jpx
global [arr = [1, 2, 3];
arr[0] = 99;          # Was: must rebuild list
arr[2] = 77;
# Nested juga work:
matrix[0][1] = 42;
```

#### Integer Division (`//`)
```jpx
print 17 // 5;        # 3 (was: workaround int(17/5))
print 10 // 4;        # 2
```

**Breaking**: `//` bukan komentar lagi. Pakai `#` untuk komentar.

#### Multiple Assignment
```jpx
global [a = 1;
global [b = 2;
a, b = b, a;          # Swap!
# Triple:
x, y, z = 100, 200, 300;
```

#### `elif` Syntax
```jpx
if score >= 90 {
    print "A";
} elif score >= 80 {
    print "B";
} elif score >= 70 {
    print "C";
} else {
    print "F";
}
```

`else if` juga didukung sebagai alternatif.

#### Native String Methods (14 method)
```jpx
s.split(",")          # → list
s.strip()             # trim whitespace
s.lstrip() / s.rstrip()
s.replace("a", "b")
s.upper() / s.lower()
s.contains("sub")     # → bool
s.startsWith("pre")   # → bool
s.endsWith("suf")     # → bool
s.find("sub")         # → index or -1
s.count("sub")        # → int
s.repeat(n)           # → string repeated
s.substring(start, end)
s.toCharArray()       # → list of chars
```

### Phase B — Architecture

#### Class/OOP Support
```jpx
class Counter {
    __init__(self, start) {
        self.count = start;
    }
    inc(self) {
        self.count = self.count + 1;
        return self.count;
    }
    val(self) {
        return self.count;
    }
}

global [c = Counter(10);
print c.inc();        # 11
print c.val();        # 11
```

Features:
- Constructor `__init__`
- Instance fields via `self.field`
- Method calls dengan auto-inject `self`
- Multiple instances independent
- Mutable state
- Method chaining (return `self`)

#### Modular Exception Package
Struktur baru di `core/exceptions/`:
```
core/exceptions/
├── __init__.py     # Re-exports
├── base.py         # JPXError, JPXExceptionWrapper
├── syntax.py       # JPXSyntaxError
├── name.py         # JPXNameError
├── type.py         # JPXTypeError
├── attribute.py    # JPXAttributeError (NEW)
├── runtime.py      # JPXRuntimeError, JPXImportError
└── control.py      # break/continue/return
```

Backward compatible — `interpreter/exceptions.py` re-exports dari `core/exceptions/`.

#### Importer v4.0
- **Relative import**: module `.jpx`/`.py` di direktori script otomatis ketemu
- **`JPX_PATH` env var**: tambah search path custom
- **Circular import detection**: error message jelas dengan chain
- **Multi-import**: `[a, b, c]` import beberapa module sekaligus
- **Multi-attribute**: `[m.a, m.b, n.c]`
- **`--list-modules` command**: lihat semua module tersedia

#### Lexer + Parser + AST (Foundation)
File baru:
- `interpreter/lexer.py` — tokenizer penuh
- `interpreter/parser.py` — recursive descent parser
- `interpreter/astnodes.py` — 20+ AST node class

Belum di-wire ke main interpreter (masih regex-based), tapi siap untuk Phase C.

## 🐛 Bug Fixes (Critical)

| Bug | Impact | Fix |
|-----|--------|-----|
| `global [s = "123"]` auto-convert ke int | String digit rusak | Hapus auto-conversion |
| `//` dianggap komentar | `print 17 // 5` kehilangan `// 5` | Hapus `//` dari comment handler |
| `tok[0] == "NUM"` return `'NUM'` | Comparison rusak di chained access | Fall through kalau expr gak habis dikonsumsi |
| `"x: " + (5 == 5)` invalid | String + comparison error | Comparison track depth |
| `(4 * 6) / (2 * 3)` invalid | Parenthesized division error | Multiplicative op track depth |
| `arr[i] > arr[i]` invalid | Comparison dengan index access rusak | Perketat index regex |
| `print "x" + (5 == 5)` return '5' | String + bool broken | Comparison cek depth |
| Function call greedy | `len(kata[i]) > len(longest)` dianggap call | Manual paren matching |
| Class method gak nemu `self.field` | OOP rusak | Function call traverse parts properly |

## 📊 Test Coverage

- **8 test files**, all pass
- **134+ individual assertions**
- Unit tests: lexer, parser, fitur baru, library
- E2E tests: showcase program lengkap

## 📦 Files Changed

### New Files
- `core/__init__.py`
- `core/exceptions/__init__.py` + 7 sub-modules
- `interpreter/lexer.py`
- `interpreter/parser.py`
- `interpreter/astnodes.py`
- `library/array.jpx` (self-hosted)
- `library/mathx.jpx` (self-hosted)
- `tests/unit/test_phase_a.jpx`
- `tests/unit/test_phase_b.jpx`
- `tests/unit/test_array_lib.jpx`
- `tests/unit/test_mathx_lib.jpx`
- `tests/unit/test_lexer_parser.py`
- `tests/unit/test_new_features.py`
- `tests/unit/self_test.jpx`
- `tests/e2e/test_showcase.jpx`
- `tests/run_tests.py`
- `examples/multi_module/` (3 files)
- `examples/mini_interp.jpx`
- `docs/structure.md`
- `docs/syntax.md`
- `README.md`
- `CHANGELOG.md`

### Modified Files
- `jpx.py` — tambah `--list-modules`, set script_dir
- `JpXkg.py` — minor cleanup
- `interpreter/interpreter.py` — class support, elif, fix `//` comment
- `interpreter/eval.py` — major rewrite (string methods, class, mutable assign, dll)
- `interpreter/function.py` — closure proper, single source of JPXReturnException
- `interpreter/importer.py` — v4.0 dengan semua fitur baru
- `interpreter/exceptions.py` — re-export dari `core/exceptions/`
- `library/string.py` — fix `random()` name shadowing, `__name__` guard
- `library/json.py` — fix `__name__` guard
- `library/scanner.py` — fix `if default:` → `if default is not None:`
- `library/print.py` — fix `Print.string()` yang gak nge-print

## 🚀 Migration dari v1.0 → v1.3

### Breaking Changes
1. `//` bukan komentar lagi → ganti ke `#`
2. String digit gak auto-convert ke int → pakai `int("123")` eksplisit
3. `else if` sekarang lebih disarankan pakai `elif`

### Compatible
Semua code v1.0 yang pakai fitur dasar (function, if-else, while, for, list, dict, library) tetap jalan tanpa perubahan.

## 🎯 Next Steps (v1.4+)

- Wire lexer + parser ke main interpreter (AST-based eval)
- Migrate `interpreter/` → `core/` penuh
- Migrate `library/` → `stdlib/{text,math,io,...}/`
- Bitwise operators `& | ^ ~ << >>`
- Typed try-catch `catch (JPXNameError e)`
- Power operator `**`
- Default arguments `function f(a, b=10)`
- Switch/match statement
