# Variables & `global`

Every variable declaration in JPX uses the `global` keyword inside square brackets, and
**must end with a semicolon** `;`.

## Declaration

```jpx
global [name = "Alice"];
global [age = 30];
global [pi = 3.14];
```

Variables declared with `global [...]` can be used anywhere in the script.

## Declaring Several at Once

Separate `name = value` pairs with commas at the top level:

```jpx
global [a = 1, b = 2, c = 3];
global [list1 = [1, 2], list2 = [3, 4]];   # commas inside a list are safe
global [msg = "a,b", flag = true];         # commas inside a string are safe
```

Pairs are evaluated **in order**, so a later pair may read an earlier one:

```jpx
global [width = 10, area = width * 5];     # area = 50
```

## Plain Assignment (Local)

Inside a function, assignment without `global` is **local** — the variable disappears
when the function ends:

```jpx
function count() {
    total = 10;            # local — gone once the function ends
    total = total + 5;
    return total;
}
```

## `global` Inside a Function

To write to a global variable from inside a function, use `global [...]` inside it:

```jpx
global [counter = 0];

function increment() {
    global [counter = counter + 1];
}

increment();
increment();
print counter;              # 2
```

The `counter` on the right-hand side is read from the **current** global value, not a
snapshot taken when the function was created.

## Lookup Order Inside `global [...]`

When the interpreter evaluates values inside `global [...]`, the lookup order is:

1. **Parameters** of the currently running function — highest priority
   (a parameter named `arr` is not overwritten by `global [arr = ...]`).
2. **Current globals**.
3. Other **locals / closures**.

## The `;` Writing Rule

Every statement must end with `;`. If the `;` is missing after `global [...]`, the
interpreter gives a clear error — it does not silently swallow the next line of code:

```text
Unexpected text after global declaration: 'print "A"' (statements must end with ';')
```

## Things to Remember

- The `let` keyword **does not exist** in JPX — declaration is always `global [...]`.
- The `global` keyword is written in all lowercase; `Global` is rejected (case-sensitive).
- There are no "immutable" constants: global variable values can be rewritten through
  assignment or `global [...]` inside a function.

## Related Pages

- [data-types.md](data-types.md) — the types of values you can store
- [control-flow.md](control-flow.md) — using variables in conditions and loops
- [limitations.md](limitations.md) — list of features not yet supported
