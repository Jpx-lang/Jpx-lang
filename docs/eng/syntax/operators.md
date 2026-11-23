# Operators

## Arithmetic

| Operator | Meaning | Example | Result |
|---|---|---|---|
| `+` | add / concatenate strings | `1 + 1` | `2` |
| `-` | subtract | `10 - 4` | `6.0` |
| `*` | multiply | `6 * 7` | `42` |
| `/` | divide (float) | `7 / 2` | `3.5` |
| `//` | integer divide | `7 // 2` | `3` |
| `%` | remainder | `7 % 2` | `1` |

Two behavior notes:

- `-` produces a **float** (`10 - 4` → `6.0`), while `+` and `*` produce integers.
  See also [data-types.md](data-types.md).
- `+` acts as string concatenation when its operands are strings: `"a" + "b"` → `ab`.

> The power operator `**` does **not** exist — use `mathx.power(2, 8)` from the
> `[mathx]` module (result: `256`).

## Comparison

`==` `!=` `<` `>` `<=` `>=`

```jpx
print 1 == 1;      # True
print 1 != 2;      # True
print 1 < 2;       # True
print 2 >= 2;      # True
```

## Logic

```jpx
print true and false;   # False
print true or false;    # True
print not false;        # True
```

Use the keywords `and`, `or`, `not`. The symbolic operators `&&`, `||`, `!` are **not**
supported.

## The `is` and `in` Operators

```jpx
global [x = null];
print x is null;                    # True

print 3 in [1, 2, 3];               # True
global [d = {"a": 1}];
print "a" in d;                     # True
```

- `is` is used to test for `null`.
- `in` tests membership in a list or keys in a dict.

## Ternary

```jpx
global [x = 5];
print x > 3 ? "big" : "small";    # big
```

## The Pipe `|>`

Forwards the left-hand result as the first argument of the function on the right — handy
for transformation chains:

```jpx
function double(x) { return x * 2; }
function inc(x)    { return x + 1; }

global [r = 5 |> double |> inc];
print r;                            # 11
```

> **Note**: the pipe needs parentheses when used directly in `print`:
> `print (5 |> double |> inc);` → `11`. Without parentheses, `print` only reads the first
> number (`5`).

## Operators That Don't Exist Yet

`+=` `-=` `*=` `/=` `%=` and `**` are not supported yet. Rewrite them explicitly:

```jpx
global [n = 0];
n = n + 1;        # ✅
# n += 1;         # ❌ Invalid assignment target
```

This also applies to incrementing in loops — a common pattern in JPX:

```jpx
global [i = 0];
while i < 5 {
    i = i + 1;
}
print i;            # 5
```

## Related Pages

- [data-types.md](data-types.md) — integer vs float behavior
- [functions.md](functions.md) — functions as pipe `\|>` targets
- [limitations.md](limitations.md) — the complete list of what's not yet supported
