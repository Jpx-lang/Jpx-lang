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
