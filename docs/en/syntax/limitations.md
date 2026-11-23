# Known Limitations

This page lists features that are **not yet** supported in JPX A2. Every item below has
been verified — don't rely on them until support is announced. This list also exists so
you don't have to guess why your code fails.

## Syntax and Keywords

| Feature | Status | Alternative |
|---|---|---|
| `Print` / `Global` (capitalized) | ❌ case-sensitive | write `print`, `global` |
| `let` | ❌ doesn't exist | use `global [...]` |
| `//` or `/* */` comments | ❌ | use `#` (`//` is integer division) |
| `print "a", "b"` (multiple arguments) | ❌ | combine: `print "a" + "b"` |
| `print(...)` with parentheses | ❌ | write `print ...;` |
| `catch e` without parentheses | ❌ | `catch (e)` is required |
| `finally` block | ❌ | clean up resources manually |

## Operators

| Feature | Status | Alternative |
|---|---|---|
| `**` (power) | ❌ | `[mathx]` + `mathx.power(2, 8)` |
| `+=` `-=` `*=` `/=` `%=` | ❌ | write it fully: `n = n + 1` |
| `&&` `\|\|` `!` | ❌ | use `and`, `or`, `not` |
| `print 5 \|> f` without parentheses | ❌ | use `print (5 \|> f)` |

## Functions

| Feature | Status | Alternative |
|---|---|---|
| Default arguments `f(a, b = 1)` | ❌ | accept null then fill it in, or require the argument |
| Variadics `f(...args)` | ❌ | accept a list: `f([1, 2, 3])` |
| Lambdas / anonymous functions | ❌ | declare a named `function` |

## Functions and Methods

| Feature | Status | Alternative |
|---|---|---|
| `range(n)` | ❌ | prepare a list: `[0, 1, 2]` |
| The `.length()` method | ❌ | use `len()` |
| A string method right after `.split()` | ❌ result is a list | take the element first: `.split(" ")[0].upper()` |
| `[io]` (without the package prefix) | ❌ | write `[jpx.io]` |

## Modules and Environment

| Feature | Status | Notes |
|---|---|---|
| `[color]` without `colorama` | ❌ | `pip install colorama` first |
| `[win32sys]` / `[win32ui]` on Linux/macOS | ❌ | Windows only + `pip install pywin32` |

## Behaviors to Watch Out For

Not errors, but important to know:

1. **The result of `-` is always a float** — `10 - 4` → `6.0`, `fib(10)` → `55.0`,
   `str(-3)` → `-3.0`. Wrap it in `int()` when you need an integer. See
   [data-types.md](data-types.md).
2. **Errors inside `${expression}` don't stop the program** — they appear as
   `<error:...>` text in the output. Inspect your string output. See
   [print-and-interpolation.md](print-and-interpolation.md).
3. **`--jpx-interpreter` is a subset only** — the self-hosted path doesn't support
   imports, full classes, complete try-catch, or native string methods; its failures
   can be silent. Use it only for demos/debugging. See
   [../cli/basic-commands.md](../cli/basic-commands.md).

## Related Pages

- [README.md](README.md) — basic syntax conventions
- [modules.md](modules.md) — built-in module dependencies
