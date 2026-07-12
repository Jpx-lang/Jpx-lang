# JPX Programming Language v1.5.0

Versi 1.5 — scoping fix, `${expr}` interpolation, switch/pipe syntax, dan `jpx/` standard library package.

## 🎯 Apa yang Baru di v1.5

### Language Features
- ✅ **Scoping fix**: `global [x = 5]` = locked global, `x = 5` = local scope
- ✅ **`${expr}` interpolation**: `"${age + 1}"`, `"${name.upper()}"`, `"${len(arr)}"`
- ✅ **Switch statement**: `switch expr { case val { ... } default { ... } }`
- ✅ **Pipe operator `|>`**: `5 |> double |> inc` = `inc(double(5))`
- ✅ **`in` operator**: `3 in [1,2,3]` = `true`, `"key" in dict`
- ✅ **`is` operator**: `x is null` = identity check

### Standard Library (`jpx/` package)
- ✅ `jpx/string.jpx` — 18 string functions
- ✅ `jpx/math.jpx` — 14 math functions
- ✅ `jpx/functional.jpx` — map, filter, reduce, pipe, compose
- ✅ `jpx/array.jpx` — 20+ array functions (sort, reverse, unique, chunk, flatten, map, filter, reduce)
- ✅ `jpx/io.jpx` — file read/write/append/copy/listDir
- ✅ `jpx/types.jpx` — type checking (isNull, isString, isInt, isNumber, isBool, isList, isDict, coerce, default)
- ✅ `jpx/choose.jpx` — multi-candidate execution with strategy selection

### Importer Upgrade
- ✅ **Folder packages**: direktori dengan `_jpx_.jpx` = importable package
- ✅ **Sub-module imports**: `[jpx.string]` loads `jpx/string.jpx`
- ✅ **`--list-modules`** detects folder packages

### Bug Fixes
- ✅ `return;` (bare return) now works
- ✅ `}` in string literals no longer breaks block extraction
- ✅ `global [x = 5]` inside function properly sets global env
- ✅ `global [counter = counter + 1]` reads from current global value
- ✅ Late binding for sibling functions and class methods
- ✅ Recursive function support (self-reference in closure)
- ✅ Escape sequences in string literals (`\n`, `\t`, `\"`, etc.)

## 📦 Cara Pakai

### Run dengan main interpreter (default)
```bash
python3 jpx.py examples/demo_lib.jpx
```

### Run dengan self-hosted interpreter (experimental)
```bash
python3 jpx.py --jpx-interpreter examples/mini_interp.jpx
```

### List available modules
```bash
python3 jpx.py --list-modules
```

### Run all tests
```bash
python3 tests/run_tests.py
python3 tests/run_bootstrap_tests.py
```

## 📁 Struktur Direktori

```
jpx-lang-1.5/
├── jpx.py                        # CLI entry point
├── JpXkg.py                      # Package manager
├── core/                         # Modular core (exceptions package)
├── interpreter/                  # Main interpreter (Python)
├── bootstrap/                    # Self-hosted interpreter (JPX)
│   ├── tokens.jpx                # Token types (46 tests)
│   ├── lexer.jpx                 # Tokenizer (46 tests)
│   ├── ast.jpx                   # AST helpers (54 tests)
│   ├── parser.jpx                # Parser (70 tests)
│   ├── evaluator.jpx             # Minimal evaluator (55 tests)
│   └── test_*.jpx
├── library/                      # Standard library
│   ├── jpx/                      # ⭐ JPX standard library package
│   │   ├── _jpx_.jpx             # Package init
│   │   ├── string.jpx            # String utilities
│   │   ├── math.jpx              # Math utilities
│   │   ├── array.jpx             # Array utilities
│   │   ├── functional.jpx        # Functional programming
│   │   ├── io.jpx                # File I/O
│   │   ├── types.jpx             # Type checking
│   │   └── choose.jpx            # Multi-candidate selection
│   ├── array.jpx                 # Legacy array lib
│   ├── mathx.jpx                 # Legacy math lib
│   └── *.py                      # Native Python modules
├── tests/
│   ├── unit/                     # Main interpreter tests (8 files)
│   ├── e2e/                      # End-to-end tests
│   ├── bootstrap/                # Bootstrap tests (4 files)
│   ├── run_tests.py
│   └── run_bootstrap_tests.py
├── examples/
│   ├── demo_lib.jpx
│   ├── demo_string.jpx
│   ├── demo_game.jpx
│   ├── mini_interp.jpx           # Mini interpreter in JPX
│   ├── JpxOsint/                  # OSINT URL checker
│   └── multi_module/             # Multi-module demo
├── docs/
│   ├── structure.md
│   └── syntax.md
├── CHANGELOG.md
├── README.md
└── LICENSE.txt
```

## 🚀 Quick Start

```jpx
[jpx.string];
[jpx.math];
[jpx.array];
[jpx.choose];

global [name = "Alice"];
global [age = 30];
global [nums = [3, 1, 4, 1, 5, 9, 2, 6]];

# String interpolation
print "Hello, $name! Next year: ${age + 1}";

# Array operations
print "Sorted: ${array.join(array.sort(nums), \", \")}";
print "Sum: ${array.sum(nums)}";
print "Max: ${array.max(nums)}";

# Math
print "Fib(10): ${math.fib(10)}";
print "IsPrime(17): ${math.isPrime(17)}";

# Choose — multi-candidate selection
function fastFn() { return "fast"; }
function slowFn() { return "slow"; }
global [result = choose.choose([fastFn, slowFn], "RapidThroughput")];
print "Winner: ${result.value}";

# Switch
switch age {
    case 30 { print "Thirty"; }
    case 40 { print "Forty"; }
    default { print "Other"; }
}

# Pipe
function double(x) { return x * 2; }
function inc(x) { return x + 1; }
print 5 |> double |> inc;  # 11
```

## 📊 Test Results

| Test Suite | Tests | Status |
|---|---|---|
| Main test suite | 8 files | ✅ All pass |
| Bootstrap lexer | 46 | ✅ All pass |
| Bootstrap AST | 54 | ✅ All pass |
| Bootstrap parser | 70 | ✅ All pass |
| Bootstrap evaluator | 55 | ✅ All pass |
| **Total** | **225+** | **All pass** |

## 📜 License

MIT License — lihat `LICENSE.txt`.
