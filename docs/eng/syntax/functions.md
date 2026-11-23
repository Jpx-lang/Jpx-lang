# Functions

Functions are declared with the `function` keyword, a `{ }` block, and untyped parameters:

```jpx
function sum(a, b) {
    return a + b;
}

print sum(1, 2);         # 3
```

## Functions Without `return`

A function without `return` is still valid — it internally returns null:

```jpx
function greet() {
    print "hello from function";
}
greet();                     # hello from function
```

## Recursion

Recursion is fully supported:

```jpx
function fib(n) {
    if n < 2 { return n; }
    return fib(n - 1) + fib(n - 2);
}

print fib(10);              # 55.0
```

Note: the result is `55.0` (a float) because the `-` operator produces floats — see
[data-types.md](data-types.md). Wrap it in `int(fib(10))` when you need an integer.

## Bare `return`

`return` without a value exits the function early:

```jpx
function check(x) {
    if x < 0 { return; }
    print "positive";
}
```

## Variables Inside Functions

- Plain assignment is **local** (gone once the function ends).
- `global [name = value];` inside a function writes to a global variable.
- Details in [variables.md](variables.md).

```jpx
global [counter = 0];

function increment() {
    global [counter = counter + 1];
}

increment();
increment();
print counter;              # 2
```

## Limitations You Should Know

- **Default arguments are not supported yet.** `function f(a, b = 9)` fails with
  `Variable 'b' not defined`. Pass arguments explicitly from the caller, or accept null
  and fill it in manually:

  ```jpx
  function greet(name) {
      if name is null { name = "World"; }
      print "Hello, $name!";
  }
  greet(null);      # Hello, World!
  greet("JPX");     # Hello, JPX!
  ```

- There are no variadics (`...args`) and no lambdas in the main interpreter.
- Functions are called with parentheses `name(arg)`; without parentheses there is no
  stable function-reference mechanism — for composition, use the pipe `|>` (see
  [operators.md](operators.md)).

## Related Pages

- [control-flow.md](control-flow.md) — `if` and loops inside functions
- [class.md](class.md) — methods inside a class
- [print-and-interpolation.md](print-and-interpolation.md) — calling functions in `${...}`
