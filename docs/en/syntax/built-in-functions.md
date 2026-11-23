# Built-in Functions

Built-in functions are available without any import.

## The List

| Function | Purpose | Example | Result |
|---|---|---|---|
| `len(x)` | length of a string/list/dict | `len("abc")` | `3` |
| `str(x)` | convert to string | `str(42)` | `"42"` |
| `int(x)` | convert to integer | `int("42")` | `42` |
| `float(x)` | convert to float | `float("1.5")` | `1.5` |
| `bool(x)` | convert to boolean | `bool(0)` | `False` |
| `type(x)` | name of the value's type | `type(1)` | `int` |
| `ord(s)` | code of the first character | `ord("A")` | `65` |
| `chr(n)` | character from a code | `chr(66)` | `"B"` |

## Example

```jpx
print len("abc");        # 3
print str(42);           # 42
print int("42");         # 42
print float("1.5");      # 1.5
print bool(0);           # False
print bool("");          # False
print ord("A");          # 65
print chr(66);           # B

global [n = 1];
print type(n);           # int
```

## Built-in Constants

`true`, `false`, and `null` are built-in values (not functions):

```jpx
global [b = true];
global [z = null];
print b;                 # True
print z is null;         # True
```

## Conversion Behavior

- `int()` on a non-numeric string returns `0` (no error):
  `int("abc")` → `0`. Validate yourself when needed, e.g. with
  `[jpx.string]` + `string.isDigit()`.
- `str(null)` produces an empty string — null is printed as empty.
- The combination `int("42") + float("1.5")` produces `43.5` (a float, because one
  operand is a float).

## What Is Not Available

- `range(n)` **does not exist**. For a fixed number of iterations, prepare a list:
  `for v in [0, 1, 2] { ... }` — see [control-flow.md](control-flow.md).
- There is no `print()` as a function, no `input()`, and no `eval()` — other
  interactions use modules (e.g. `[scanner]` to read input, `[fs]` for files).

## Related Pages

- [data-types.md](data-types.md) — type behavior and output formats
- [modules.md](modules.md) — `[scanner]`, `[fs]`, and other modules
- [limitations.md](limitations.md) — the complete list of what's not yet supported
