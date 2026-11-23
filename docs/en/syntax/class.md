# Class

JPX supports object-oriented programming the Python way: an `__init__` constructor and an
explicit `self` parameter written on every method.

## Declaration and Instantiation

```jpx
class Point {
    function __init__(self, x, y) {
        self.x = x;
        self.y = y;
    }

    function dist(self) {
        return self.x * self.x + self.y * self.y;
    }
}

global [p = Point(3, 4)];
print p.x;                  # 3
print p.dist();             # 25
```

Important rules:

- `self` is written **explicitly** as the first parameter of every method, and methods
  are called without passing `self` (`p.dist()`, not `p.dist(p)`).
- `__init__` is the constructor — called automatically on instantiation.
- Instances are created by calling the class name like a function: `Point(3, 4)`.
- Instance properties are stored via `self.name = value` inside methods.
- Property access uses a dot: `p.x`; calling a method uses a dot and parentheses:
  `p.dist()`.

## Another Example: Counter

```jpx
class Counter {
    function __init__(self) {
        self.n = 0;
    }
    function up(self) {
        self.n = self.n + 1;
        return self.n;
    }
}

global [c = Counter()];
c.up();
c.up();
print c.n;                  # 2
```

## Calling Outer Functions From Inside a Method

Methods can read global functions that were declared before the class is used:

```jpx
function asInt(n) {
    return int(n);
}

class Number {
    function __init__(self, v) {
        self.v = asInt(v);
    }
}

global [a = Number("7")];
print a.v;                  # 7
```

## Notes

- Inheritance (`extends` / `super`) is not supported yet in A2.
- On the experimental `--jpx-interpreter` path (self-hosted), class instantiation only
  supports a subset — see [../cli/basic-commands.md](../cli/basic-commands.md).

## Related Pages

- [functions.md](functions.md) — the `function` declaration, also used for methods
- [variables.md](variables.md) — `self`, local, and global scope
