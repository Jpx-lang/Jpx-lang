# JPX Changelog

## A2 — 2026-11-22

### 🐛 Bug Fixes

#### `switch` tidak pernah match kecuali tanpa spasi
`handle_switch` melewati whitespace dengan membaca variabel `body`
(seluruh statement, termasuk `{` pembuka) padahal posisinya dipakai untuk
mengindeks `block`. Index tidak pernah sinkron, sehingga `case`/`default`
hanya terbaca kalau ditulis `{case 1 {...}` tanpa spasi sama sekali:

```jpx
switch x { case 1 { ... } }        # dulu: tidak jalan sama sekali
switch x {
    case 1 { print "one"; }        # dulu: tidak jalan
    default { print "other"; }     # sekarang: jalan
}
```

Sekarang skip-whitespace membaca `block`, ditambah pengecekan batas token
agar `defaults`/`mycase` tidak salah dikenali sebagai `default`/`case`.

#### `global` tanpa `;` menelan statement berikutnya
`handle_global` memakai regex greedy `global\s*\[(.*)\]` yang cocok sampai
`]` **terakhir** — sisa statement setelah `]` penutup diabaikan diam-diam,
jadi kode hilang tanpa error:

```jpx
global [a = 1]
print "A";          # dulu: hilang tanpa jejak, exit code 0
```

Diganti scan bracket seimbang (mendukung nested list) plus validasi sisa
teks, sehingga sekarang memberi error jelas:

```
Unexpected text after global declaration: 'print "A"' (statements must end with ';')
```

#### Stdlib: `global [...]` kurang `]` (pre-existing)
Lima deklarasi di stdlib tidak punya `]` penutup, sehingga statement
berikutnya ikut tertelan dan fungsi-fungsi ini rusak sejak awal:

- `library/jpx/string.jpx` — `isDigit()`, `isAlpha()` (2 tempat)
- `library/jpx/io.jpx` — `readLines()`, `copy()`
- `library/jpx/types.jpx` — `isCallable()`

```jpx
[jpx.string];
print string.isDigit("5");   # dulu: Invalid global statement
print string.isAlpha("B");   # sekarang: True
```

#### Multi declaration `global [a = 1, b = 2, c = 3]`
Sebelumnya `handle_global` memakai `inner.split('=', 1)`, sehingga
multi-deklarasi melempar `Invalid assignment target: '1'`. Sekarang
di-split per-pair memakai koma top-level (sadar string/list/dict), lalu
tiap pair dievaluasi **berurutan**:

```jpx
global [a = 1, b = 2, c = 3];                 # works
global [list1 = [1, 2], list2 = [3, 4]];      # koma di list aman
global [msg = "a,b", flag = true];            # koma di string aman
global [width = 10, area = width * 5];        # area = 50 (urut)
```

Bonus: `global [x == 1]` kini error jelas (bukan dianggap assignment),
dan env selalu di-restore lewat `finally` kalau ada error.

#### Parameter function ketimpa global (pre-existing)
`handle_global` mengevaluasi nilai dengan merged-env "global first",
sehingga **parameter ketimpa global** kalau namanya sama. Ini membuat
stdlib rusak begitu user mendeklarasikan global dengan nama parameter:

```jpx
global [arr = ["a", "b"]];
[array];
print array.sum([1, 2, 3]);   # Runtime Error: Cannot index list with 2
```

Sekarang parameter diberi prioritas lewat `param_scope_stack`
(di-push `JPXFunction.call`, di-pop di `finally`).

#### String method chaining
`eval_expression` hanya mengenali **satu** method call lewat regex
`obj.method(args)`, sehingga `s.upper().lower()` gagal dengan
`Invalid expression: ').lower('`. Diganti `_eval_string_method_chain`
yang mengevaluasi rantai postfix dari kiri ke kanan:

```jpx
word.upper().lower()
word.strip().upper()
word.replace("o", "0").upper()
csv.split(",")[0].upper()      # method -> index -> method
letters[0].upper()             # receiver index access
"abc".upper().trim()           # receiver literal
obj.name.lower()               # receiver property access
```

Rantai **hanya** diambil kalau semua method termasuk set method string —
nama lain (`array.sort`, `requests.get`, `choose.choose`) jatuh ke
function-call path seperti sebelumnya, jadi tidak ada regresi.

#### `trim()` alias
`trim` dipakai terus di stdlib (`jpx/string.jpx`, `library/string.py`)
tapi bukan method native, sehingga `s.trim()` diam-diam menghasilkan
`null`. Sekarang jadi alias `strip()`.

### 📦 Build & Release

#### Support PyInstaller (frozen mode)
`get_jpx_paths()` selalu memakai `dirname(__file__)` yang menunjuk folder
ekstraksi temp saat di-build, sedangkan `ImportHandler` memakai
`dirname(sys.executable)` — dua path berbeda sehingga build frozen tidak
menemukan `library/`. Sekarang keduanya konsisten menunjuk folder yang
sama dengan executable.

#### Versi
`VERSION`/`VERSION_NAME` diperbarui menjadi **A2**.

### ✅ Tests
- `tests/unit/test_global_and_chains.jpx` — 36 assertion baru
  (multi-global, chaining, param-vs-global collision)
- `tests/unit/test_switch.jpx` — 10 assertion baru (spasi, multiline,
  default, string case, nested brace, expression case value, no fall-through)
- Suite utama: **10/10** file test lulus

---

# JPX v1.5.0 Changelog

Released: 2026-07-12

## ✨ New Features

### Language Features

#### Scoping Fix
```jpx
# global = locked di global scope, accessible dari mana saja
global [counter = 0];
function inc() {
    global [counter = counter + 1];  # baca dari global, set ke global
    return counter;
}
inc();  # 1
inc();  # 2
inc();  # 3

# local = hanya di scope saat ini
function f() {
    x = 10;        # local, hilang setelah function selesai
    return x;
}
```
- `global [x = 5]` sekarang properly set di global env (persistent)
- `x = 5` di function body = local variable
- `global [counter = counter + 1]` baca dari current global value, bukan stale closure copy
- Merged env saat evaluasi `global` expression: global values diutamakan, local vars (parameters) tetap terlihat

#### `${expr}` Interpolation
```jpx
global [name = "Alice"];
global [age = 30];
global [arr = [1, 2, 3]];

print "Hello, $name!";                    # backward compat
print "Next year: ${age + 1}";            # arithmetic
print "Length: ${len(arr)}";              # function call
print "Upper: ${name.upper()}";           # method call
print "Sum: ${arr[0] + arr[1] + arr[2]}"; # index + arithmetic
```
- `${expr}` evaluasi expression apa pun
- `$var` tetap backward compat (simple variable interpolation)
- Optimized: hanya scan untuk `${` jika ada di string

#### Switch Statement
```jpx
switch day {
    case 1 { print "Monday"; }
    case 2 { print "Tuesday"; }
    case 3 { print "Wednesday"; }
    default { print "Other"; }
}
```
- Go-style (no fall-through, block per case)
- Track string literals saat parse case values
- Default block opsional

#### Pipe Operator `|>`
```jpx
function double(x) { return x * 2; }
function inc(x) { return x + 1; }

print 5 |> double |> inc;  # = inc(double(5)) = 11
print 10 |> double |> inc |> double;  # = 42
```
- Left-to-right evaluation
- Track string/depth agar `|>` di dalam string/paren diabaikan

#### `in` Operator (Membership)
```jpx
print 3 in [1, 2, 3];           # true
print "name" in {"name": "Alice"};  # true
print "hel" in "hello";         # true
```

#### `is` Operator (Identity)
```jpx
global [x = null];
print x is null;  # true
```

### Standard Library (`jpx/` package)

#### `jpx/string.jpx` — String Utilities (18 functions)
upper, lower, trim, reverse, contains, replace, split, join, startsWith, endsWith, find, count, repeat, substring, isDigit, isAlpha, toCharArray, fromCharArray

#### `jpx/math.jpx` — Math Utilities (14 functions)
fib, factorial, isPrime, gcd, lcm, power, isqrt, mean, max, min, sum, abs, clamp, range

#### `jpx/array.jpx` — Array Utilities (20+ functions)
push, pop, first, last, contains, indexOf, count, reverse, sort, sum, max, min, join, slice, map, filter, reduce, each, range, concat, flatten, unique, chunk

#### `jpx/functional.jpx` — Functional Programming (8 functions)
map, filter, reduce, each, pipe, compose, identity, constant

#### `jpx/io.jpx` — File I/O (10 functions)
read, write, append, exists, readLines, writeLines, copy, size, isDir, isFile, listDir

#### `jpx/types.jpx` — Type Checking (13 functions)
isNull, isNotNull, isString, isInt, isFloat, isNumber, isBool, isList, isDict, isFunction, isCallable, isTruthy, coerce, default, toString, name

#### `jpx/choose.jpx` — Multi-Candidate Selection
```jpx
[jpx.choose];
function fastFn() { return "quick"; }
function slowFn() { return "slow"; }
function failFn() { return undefined_var; }

global [result = choose.choose([fastFn, slowFn, failFn], "RapidThroughput")];
print result.ok;       # true
print result.value;    # "quick"
print result.winner;   # 0
print result.time;     # execution time

# Strategies: RapidThroughput, AtTheLatest, FirstOk, MostAccurate
# Convenience: choose.firstOk(), choose.fastest(), choose.all()
```

### Importer Upgrade
- **Folder packages**: direktori dengan `_jpx_.jpx` (atau `_jpx_.py`) = importable package
- **Sub-module imports**: `[jpx.string]` loads `jpx/string.jpx` dari folder package
- **`--list-modules`** mendeteksi folder packages

### `--jpx-interpreter` Flag
```bash
python3 jpx.py --jpx-interpreter program.jpx
```
Run program dengan self-hosted lexer+parser+evaluator (experimental).

## 🐛 Bug Fixes

| Bug | Impact | Fix |
|-----|--------|-----|
| `return;` (bare return) not handled | Function can't return without value | Add `stmt == 'return'` check |
| `}` in string breaks block extraction | Class/method/if/while body salah parse | Track string in extract_block, handle_class_def, _find_brace_pos |
| `global [x = 5]` inside function sets local | Global var hilang setelah function | Set ke global_env, bukan self.env |
| `global [counter = counter + 1]` reads stale | Counter tidak increment | Eval dengan merged env (global first) |
| Sibling functions can't call each other | Function A can't call Function B | Late binding: inject all exports to closure_env |
| Recursive function fails | `dump()` can't call itself | Self-reference in closure_env |
| `module.ClassName()` instantiation fails | Class in module can't be instantiated | Check `__jpx_class__` in function call path |
| Escape sequences not unescaped | `\n` stays as backslash-n | Add escape handler in process_string |
| `//` treated as comment | `17 // 5` loses `// 5` | Remove `//` from comment handler |
| String slice with float index | `s[:len(s)-1]` errors | Convert float to int in slice handler |
| `arr[i].method()` chained access | String method on index result fails | Eval obj_str first, check if string |
| `[1,2,3]` at top-level treated as import | List literal fails | Check if `[` followed by IDENT before treating as import |
| `try { return X; } catch` swallows return | Function returns null | Use `in` operator instead of try/catch for dict lookup |

## 📦 Files Changed

### New Files
- `library/jpx/_jpx_.jpx` — Package init
- `library/jpx/string.jpx` — String utilities
- `library/jpx/math.jpx` — Math utilities
- `library/jpx/array.jpx` — Array utilities
- `library/jpx/functional.jpx` — Functional programming
- `library/jpx/io.jpx` — File I/O
- `library/jpx/types.jpx` — Type checking
- `library/jpx/choose.jpx` — Multi-candidate selection
- `bootstrap/evaluator.jpx` — Minimal AST evaluator
- `bootstrap/test_evaluator.jpx` — 55 tests
- `tests/run_bootstrap_tests.py` — Bootstrap test runner

### Modified Files
- `jpx.py` — Add `--jpx-interpreter` flag, `run_with_jpx_interpreter()`
- `interpreter/interpreter.py` — Switch statement, scoping fix (global_env), `_find_brace_pos`, string tracking, late binding
- `interpreter/eval.py` — `${expr}` interpolation, `in`/`is` operators, pipe `|>`, string method improvements
- `interpreter/function.py` — Self-reference for recursive functions
- `interpreter/importer.py` — Folder packages, sub-module imports, `_jpx_.jpx` marker
- `library/mathx.jpx` — Fix all `global [x = ...]` to plain `x = ...` for local vars

## 🚀 Migration dari v1.4 → v1.5

### Breaking Changes
- `global [x = 5]` inside function now properly sets global (was setting local)
- Library code that used `global [x = ...]` for local variables must change to `x = ...`

### Compatible
- All v1.4 user code that uses `global [x = 5]` at top-level still works
- All v1.4 library imports still work
- `$var` interpolation still works (backward compat)

## 🎯 Next Steps (v1.6+)

- Power operator `**`
- Bitwise operators `& | ^ ~ << >>`
- Compound assignment `+= -= *= /=`
- Default arguments `function f(a, b=10)`
- Anonymous functions `function(x) { ... }`
- Complete bootstrap evaluator (imports, class, string methods)
- Wire bootstrap as optional default interpreter
