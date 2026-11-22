# JPX A2 — What's New & Fixed

**Released:** 2026-11-22
**Compared against:** [source-code-A1.0-mit-dev.zip](https://github.com/Jpx-lang/Jpx-lang/releases/download/Source-code%2FA%2Fv1.0/source-code-A1.0-mit-dev.zip)

---

## Downloads

| File | Description |
|---|---|
| `Jpx-lang-A2-source-code.zip` | Full A2 source tree |
| `jpx.exe` | Windows x64 standalone executable |
| `jpx-win64.zip` | `jpx.exe` + `library/` + `bootstrap/` + docs |
| `jpx-x86-linux.zip` | Linux x86-64 standalone executable + `library/` + `bootstrap/` + docs |

Both binaries are built with **PyInstaller 6.22.3** and bundle the Python
runtime — no Python installation is required on the target machine.

> Keep the `library/` folder next to the executable. The interpreter
> resolves built-in modules relative to its own location.

---

## 🐛 Bugs fixed

Every row below was verified by running the same snippet against the
A1.0 source tree and against A2.

### 1. Arithmetic was fundamentally broken

A1 implemented `+` **exclusively as string concatenation** — the code
built `result = ""` and appended `str(val)` for every operand. There was
no numeric addition path at all.

```python
# A1.0 interpreter/eval.py
result = ""
for part in parts:
    ...
    result += str(val)     # <- always string concatenation
return result
```

| Expression | A1.0 | A2 |
|---|---|---|
| `print 1 + 1;` | `11` | `2` |
| `print 2 + 3 * 4;` | `212.0` | `14` |
| `print 10 - 4;` | ❌ `Invalid expression: '10 - 4'` | `6.0` |
| `print 7 % 2;` | ❌ `Invalid expression: '7 % 2'` | `1` |
| `print 7 // 2;` | `7` | `3` |
| `global [i = 0]; i = i + 1;` | `"01"` | `1` |

This also made `while` loops, `for` accumulation and `break`/`continue`
unusable in A1, since loop counters were string-concatenated.

### 2. `if` / `else` / `elif`

A1 could not evaluate `==` inside an `if` condition, and `else` blocks
were not handled:

```jpx
if (x == 1) { print "one"; } else { print "other"; }
```
- **A1.0:** ❌ `Invalid expression: '= 1'`
- **A2:** ✅ works (parentheses optional, `elif` supported)

### 3. Operators and builtins missing in A1

| Feature | A1.0 | A2 |
|---|---|---|
| `x is null` | ❌ `Invalid expression: 'x is null'` | ✅ |
| `7 % 2` | ❌ `Invalid expression` | ✅ `1` |
| `len([1,2])` | ❌ `Undefined variable: len` | ✅ `2` |
| `arr.push(2)` | ❌ `'list' object has no attribute 'push'` | ✅ |
| `a.push` list methods | ❌ | ✅ |

### 4. String methods & method chaining

A1's evaluator had **no method-call support whatsoever** (no
`STRING_METHODS`, no method dispatch), so any `obj.method()` syntax failed:

```jpx
"  x  ".trim()          # A1: 'str' object has no attribute 'trim'
"a,b".split(",")[0]     # A1: Undefined variable: ","
```

A2 adds a postfix chain evaluator (`_eval_string_method_chain`) that walks
`base -> method -> method -> index` left to right:

```jpx
word.upper().lower()
word.replace("o", "0").upper()
csv.split(",")[0].upper()
"abc".upper().trim()
```

Chaining is restricted to methods in `STRING_METHODS`; anything else falls
through to the normal function-call path, so `array.sort(...)` and
`requests.get(...)` behave exactly as before.

`trim` is also registered as an alias of the native `strip()` — the
stdlib calls `trim` everywhere but the native method did not exist, so
`s.trim()` silently returned `null`.

### 5. Multi-variable `global`

```jpx
global [a = 1, b = 2, c = 3];
```
- **A1.0:** ❌ `Invalid expression: '1, b = 2, c = 3'`
- **A2:** ✅ each pair is split at top level (string/list/dict aware) and
  evaluated **in order**, so `global [a = 1, b = a + 1]` gives `b == 2`

Also fixed: a parameter shadowing a same-named global no longer breaks
stdlib calls (e.g. `array.sum(arr)` while a global `arr` exists).

### 6. `switch` whitespace bug

`switch` is new in A2, but its whitespace-skip loop indexed the wrong
variable, so `case`/`default` were only recognised when written with **no
space at all** after `{`:

```jpx
switch x { case 1 { ... } }     # worked
switch x {
    case 1 { print "one"; }     # did NOT work before this release
    default { print "other"; }
}
```

Fixed by skipping whitespace inside `block` instead of `body`, plus a
token-boundary check so `defaults` / `mycase` are not misread.

### 7. `global` without `;` silently deleted the next statement

A1/A2 used a greedy regex `global\s*\[(.*)\]` that matched up to the
**last** `]` in the statement and discarded everything after it. Because
the language requires `;` as a statement terminator, this code vanished
without any error:

```jpx
global [a = 1]
print "A";          # was silently dropped, exit code 0
```

Now replaced with a balanced bracket scan plus validation:

```
Unexpected text after global declaration: 'print "A"' (statements must end with ';')
```

### 8. Standard library functions that never worked

Five declarations in the stdlib were missing their closing `]`, so the
following statement was swallowed and the function broke:

| Module | Functions |
|---|---|
| `library/jpx/string.jpx` | `isDigit()`, `isAlpha()` (2 sites) |
| `library/jpx/io.jpx` | `readLines()`, `copy()` |
| `library/jpx/types.jpx` | `isCallable()` |

```jpx
[jpx.string];
print string.isDigit("5");   # A1: Invalid global statement → now True
print string.isAlpha("B");   # A1: Invalid global statement → now True
```

---

## ✨ New features

| Feature | Notes |
|---|---|
| `switch` / `case` / `default` | Go-style, no fall-through, expression case values, nested `{}` bodies |
| `class` / `self` / `__init__` | Class declarations with methods |
| String method chaining | `.upper().lower()`, method → index → method |
| `library/array.jpx` | `array.sum`, `array.first`, `array.sort`, … |
| `library/mathx.jpx` | Extended math helpers |
| Self-hosted stdlib | 8 modules under `library/jpx/` (`array`, `choose`, `functional`, `io`, `math`, `string`, `types`, `_jpx_`) imported as `[jpx.string]` |
| Script-relative imports | `import` resolves modules next to the running script |
| Structured exceptions | New `core/exceptions/` hierarchy (`syntax`, `type`, `name`, `runtime`, `control`, `attribute`, `base`) |

---

## 🛠 Project & tooling additions

A1.0 shipped only `interpreter/`, `library/`, `jpx.py`, `JpXkg.py` and
`LICENSE.txt` (34 files). A2 is a full project (116 files):

- **`tests/`** — 8 `.jpx` + 2 `.py` test files (plus 2 runners),
  **~194 assertions**
- **`run_tests.py`** — main runner (currently **10/10** passing)
- **`run_e2e.py`**, **`tests/run_bootstrap_tests.py`**
- **`docs/syntax.md`**, **`docs/structure.md`** — language reference
- **`examples/`** — 11 sample programs
- **`bootstrap/`** — experimental self-hosted implementation, run with
  `jpx --jpx-interpreter` (9 files)
- **`interpreter/lexer.py`**, **`parser.py`**, **`astnodes.py`** —
  replaces A1's mistyped `interprter.py`
- **`README.md`**, **`CHANGELOG.md`**
- **`jpx.spec`** — PyInstaller build spec
- **`.gitignore`** — keeps `__pycache__/`, `build/`, `dist/`, `release/`
  out of the repository

---

## ✅ Verification

| Suite | Result |
|---|---|
| `tests/run_tests.py` | **10/10** test files passed |
| `run_tests.py` (root) | **26/26** |
| `run_e2e.py` | PASS |
| `tests/run_bootstrap_tests.py` | 2/4 (pre-existing, experimental `--jpx-interpreter`) |

Obsolete test files were removed in this release: `tests/bootstrap/` was a
byte-identical copy of `bootstrap/` (the directory the runner actually
uses), and `test_comprehensive.jpx` / `test_trycatch.jpx` are regenerated
by `run_e2e.py` on every run, so they are now gitignored instead of
tracked.

Both binaries were smoke-tested after building: `--version`, `switch`,
arithmetic, and `[jpx.string]` stdlib imports all behave identically on
Windows and Linux.

---

## ⚠️ Known limitations

- Statements must end with `;` (a closing `}` also terminates a
  statement). Missing `;` now produces a clear error instead of silently
  dropping code.
- Default function arguments and `lambda` are **not** implemented.
- `bootstrap/` is experimental; 2 of its 4 tests pass.
- `interpreter/lexer.py` and `parser.py` are present but not yet wired
  into the runtime.
