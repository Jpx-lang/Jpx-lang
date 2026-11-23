# JPX Syntax Reference

The JPX A2 syntax reference, split into separate files per topic. Every example in this
folder has been executed and verified against the A2 interpreter.

> **Important note**: JPX is **case-sensitive**. Keywords are lowercase —
> `print`, not `Print`; `global`, not `Global`.

---

## Basic Conventions That Apply on Every Page

1. **Every statement ends with a semicolon `;`.** A block closed with `}` also acts as a
   separator. A missing `;` after `global [...]` gives a clear error:
   `Unexpected text after global declaration: 'print "A"' (statements must end with ';')`.
2. **Comments are `#` only.** Block comments are written as several `#` lines.
   `//` is **not** a comment — it's the integer-division operator (`7 // 2` → `3`).
3. **`print` is a statement, not a function** — no parentheses, one argument.
   Details in [print-and-interpolation.md](print-and-interpolation.md).
4. **Variable declarations use `global [...]`.** Details in [variables.md](variables.md).
5. **Strings support `$var` and `${expression}` interpolation.**
   Details in [print-and-interpolation.md](print-and-interpolation.md).

---

## File Index

| File | Contents |
|---|---|
| [variables.md](variables.md) | `global [...]` declarations, multi-declarations, local vs global scope, `;` rules |
| [data-types.md](data-types.md) | The seven data types, `type()`, escape sequences, multi-line strings |
| [print-and-interpolation.md](print-and-interpolation.md) | The `print` statement, `$var` and `${expression}` interpolation, error behavior |
| [operators.md](operators.md) | Arithmetic, comparison, logic, `is`/`in`, ternary, the pipe `\|>`, operators that don't exist yet |
| [control-flow.md](control-flow.md) | `if`/`elif`/`else`, `while`, `for..in`, `break`/`continue`, `switch`, `try`/`catch` |
| [functions.md](functions.md) | `function` declaration, `return`, recursion, argument limitations |
| [class.md](class.md) | `class` declaration, the `__init__` constructor, `self`, properties and methods |
| [strings.md](strings.md) | 17 string methods, method chaining, indexing, `len()` |
| [lists-dicts.md](lists-dicts.md) | Lists (indexing, `push`, the `array` module) and dicts (access, membership) |
| [modules.md](modules.md) | `import` with `[module];`, built-in modules, `jpx.*` packages, search paths, `JPX_PATH` |
| [built-in-functions.md](built-in-functions.md) | `len`, `str`, `int`, `float`, `bool`, `type`, `ord`, `chr` |
| [limitations.md](limitations.md) | List of features not yet supported in A2 |

---

## First Program

```jpx
# hello.jpx
global [name = "JPX", year = 2026];

print "Welcome to $name ${year}!";
print "2 + 3 = ${2 + 3}";

function square(x) {
    return x * x;
}
print square(7);            # 49
```

Run it with `jpx hello.jpx` (see [../cli/basic-commands.md](../cli/basic-commands.md)).
