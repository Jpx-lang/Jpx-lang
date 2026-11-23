# Output: `print` and String Interpolation

## `print` Is a Statement

`print` is **not a function** — so it must not use parentheses, and it doesn't accept
multiple arguments.

```jpx
print "hello";                # ✅  -> hello
print 42;                     # ✅  -> 42
print "a" + "b";              # ✅  -> ab
print("hello");               # ❌  Runtime Error: Undefined variable: print
print "a", "b";               # ❌  Runtime Error: Invalid expression
```

The `Undefined variable: print` message appears because JPX reads `print(...)` as a
lookup of a variable named `print`. Remember: call `print` without parentheses. To print
several values, combine them with `+` (and `str()` when needed):

```jpx
print "Age: " + str(30);
```

`print null` prints an empty line (null is printed as an empty string).

## String Interpolation

Two forms are supported and may be mixed within one string:

| Form | Result |
|---|---|
| `$name` | contents of a simple variable |
| `${expression}` | result of any expression: arithmetic, method call, function call |

```jpx
global [name = "JPX"];
global [age = 30];
global [nums = [3, 1, 4]];

print "Hello, $name!";                          # Hello, JPX!
print "Next year: ${age + 1}";                  # Next year: 31
print "Uppercase: ${name.upper()}";             # Uppercase: JPX
print "Count: ${len(nums)}";                    # Count: 3
print "n = $age, n+1 = ${age + 1}";             # both forms in 1 string
```

To display a literal dollar sign, escape it with `\$`:

```jpx
print "Price: \$5";        # Price: $5
```

`$name` interpolation reads the name after `$` up to the first character that is not part
of an identifier, so `$age` in the middle of a sentence is read whole, safely.

## Error Behavior Inside `${...}`

Mistakes in an interpolation expression **do not stop the program**. The error is
printed as `<error:...>` text exactly at the interpolation position:

```jpx
global [x = 1];
print "test: ${x + undefined_var}";
# -> test: <error:Variable 'undefined_var' not defined. Use 'global [undefined_var = value]' to declare it.>
print "done";             # still executed
```

This is useful to see the cause right in the output, but it also means the program
**does not fail hard** even when an expression in a string is wrong — inspect your
output, especially when the string is written to a file or sent somewhere else.

## Related Pages

- [data-types.md](data-types.md) — escape sequences and per-type output formats
- [strings.md](strings.md) — string methods usable inside `${...}`
- [functions.md](functions.md) — calling functions inside `${...}`
