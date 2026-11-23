# Data Types

JPX has seven data types. `print` displays them with the following formats:

| Type | Example | `print` output |
|---|---|---|
| Integer | `42` | `42` |
| Float | `3.14` | `3.14` |
| String | `"hello"` | `hello` |
| Boolean | `true` / `false` | `True` / `False` |
| Null | `null` | *(empty)* |
| List | `[1, 2, 3]` | `[1, 2, 3]` |
| Dict | `{"k": "v"}` | `{'k': 'v'}` |

Note two output habits rooted in the internal representation:

- Booleans print as `True` / `False` (capitalized, Python style).
- Dicts print with single quotes, Python repr style: `{'k': 'v'}`.

## Declaration and Inspection Example

```jpx
global [n = 42];
global [f = 3.14];
global [s = "hello"];
global [b = true];
global [z = null];
global [l = [1, 2, 3]];
global [d = {"k": "v"}];

print n;        # 42
print type(n);  # int
print type(s);  # str
print type(l);  # list
```

The `type()` function returns Python-style type names: `int`, `float`, `str`, `bool`,
`NoneType`, `list`, `dict`.

## Important Notes on Integer and Float

Numeric operation results are **not fully consistent** in A2:

```jpx
print 1 + 1;     # 2      (integer)
print 6 * 7;     # 42     (integer)
print 10 - 4;    # 6.0    (float!)
print 7 / 2;     # 3.5    (float, expected)
print 7 // 2;    # 3      (integer division)
```

The `-` operator (including negation `-3`) always produces a float, so recursive
`fib(10)` prints `55.0`. Until this behavior is unified, don't rely on the integer format
of subtraction results; use `int()` when you need a pure integer:

```jpx
print int(10 - 4);   # 6
```

## Escape Sequences

Inside string literals these standard escapes are available:

| Escape | Meaning |
|---|---|
| `\n` | newline |
| `\t` | tab |
| `\r` | carriage return |
| `\\` | backslash |
| `\"` | double quote |
| `\'` | single quote |
| `\0` | null character |
| `\b` | backspace |
| `\f` | form feed |
| `\$` | literal dollar sign (prevents interpolation) |

Unknown escapes are left as-is (`\q` stays `\q`).

```jpx
global [s = "line one\nline two"];   # \n becomes a newline
print s;
```

## Multi-Line Strings

Besides `\n`, strings may contain literal newlines:

```jpx
global [multi = "line one
line two"];
print multi;
```

## Related Pages

- [strings.md](strings.md) — the 17 string methods and interpolation
- [lists-dicts.md](lists-dicts.md) — list and dict operations
- [built-in-functions.md](built-in-functions.md) — type conversions: `int()`, `float()`, `str()`, `bool()`
