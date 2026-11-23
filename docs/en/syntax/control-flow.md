# Control Flow

## `if` / `else if` / `elif` / `else`

```jpx
global [x = 2];

if x == 1 {
    print "one";
} elif x == 2 {
    print "two";
} else {
    print "other";
}
# -> two
```

- Both `elif` and `else if` are accepted.
- Parentheses on conditions are **optional**: `if (x == 1) {` is the same as
  `if x == 1 {`.
- Blocks are always written with `{ }`.

## `while`

```jpx
global [i = 0];
while i < 3 {
    i = i + 1;
}
print i;            # 3
```

`while true { ... }` runs forever until `break`.

## `for ... in`

Iterates over a list. The `range()` function **does not exist**, so prepare the list
yourself:

```jpx
global [total = 0];
for v in [1, 2, 3] {
    total = total + v;
}
print total;        # 6
```

For a fixed number of iterations, write a list literal or build one with `while`:

```jpx
for v in [0, 1, 2, 3, 4] {
    print v;
}
```

## `break` and `continue`

```jpx
global [i = 0];
while true {
    i = i + 1;
    if i > 2 { break; }
}
print i;            # 3

global [total = 0];
for v in [1, 2, 3] {
    if v == 2 { continue; }
    total = total + v;
}
print total;        # 4
```

`break` / `continue` outside a loop raise a `SyntaxError`. Both only apply to the
innermost loop where they are written.

## `switch` / `case` / `default`

Go style, **no fall-through** — only the matching case block runs, then execution leaves
the switch. Whitespace and indentation are free.

```jpx
global [x = 2];

switch x {
    case 1 { print "one"; }
    case 2 { print "two"; }
    case 3 { print "three"; }
    default { print "other"; }
}
# -> two
```

`case` values may be expressions:

```jpx
global [a = 2];
global [b = 3];

switch a + b {
    case 4 { print "four"; }
    case 5 { print "five"; }
    default { print "?"; }
}
# -> five
```

## `try` / `catch`

```jpx
try {
    print "inside try";
} catch (e) {
    print "error: " + e;
}
print "done";
```

- `catch` **must** use parentheses: `catch (e)`, not `catch e`.
- The `e` variable holds the error message, for example:
  `error: Variable 'undefined_var' not defined. Use 'global [undefined_var = value]' to declare it.`
- It can be placed inside a function, inside a loop, or at the top level of a script.
- A `finally` block is **not yet** supported in A2.

## Related Pages

- [operators.md](operators.md) — comparison and logic operators for conditions
- [functions.md](functions.md) — `return` inside control flow
- [limitations.md](limitations.md) — `range()`, `finally`, and more
