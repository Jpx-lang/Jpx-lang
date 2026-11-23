# Strings

Strings are written with double quotes (or single quotes). String methods can be called
directly on literals as well as variables.

## The 17 String Methods

```jpx
print "abc".upper();                 # ABC
print "ABC".lower();                 # abc
print "  x  ".trim();                # x
print "  x  ".strip();               # x
print "a,b".split(",");              # ['a', 'b']
print "aaa".replace("a", "b");       # bbb
print "abc".contains("b");           # True
print "abc".startsWith("a");         # True
print "abc".endsWith("c");           # True
print "hello".find("ll");            # 2
print "hello".substring(1, 3);       # el
print "ab".repeat(3);                # ababab
print "abcabc".count("a");           # 2
print "abc".toCharArray();           # ['a', 'b', 'c']
```

Full list (17 methods):

`contains` `count` `endsWith` `find` `lower` `lstrip` `repeat` `replace` `rstrip`
`split` `startsWith` `strip` `substring` `toCharArray` `trim` `upper`

Note the mixed naming styles: some are camelCase (`startsWith`, `toCharArray`), some are
Python-style (`strip`, `lstrip`, `rstrip`, `find`). Memorize them from this list rather
than by guessing.

## Method Chaining

Methods can be chained as long as the previous result is still of a suitable type:

```jpx
global [word = "hello world"];

print word.upper();                          # HELLO WORLD
print word.replace("o", "0").upper();        # hell0 w0rld
print "  a,b  ".trim().split(",");           # ['a', 'b']
```

**Careful**: `.split()` produces a **list**, so string methods can't follow it directly:

```jpx
print word.split(" ").upper();               # ❌ error: 'upper' on a list
print word.split(" ")[0].upper();            # ✅ HELLO — take the element first
```

## Length and Indexing

String length uses `len()` — there is **no** `.length()` method:

```jpx
global [s = "abc"];
print len(s);            # 3
print s[1];              # b   (character index, starting at 0)
```

## Interpolation Inside Strings

Besides methods, strings support `$var` and `${expression}` interpolation — even chained
with methods:

```jpx
global [name = "jpx"];
print "Hello, ${name.upper()}!";      # Hello, JPX!
```

Details in [print-and-interpolation.md](print-and-interpolation.md).

## Escapes

The full list of escape sequences (`\n`, `\t`, `\$`, etc.) is explained in
[data-types.md](data-types.md).

## Companion Module

For broader string operations (e.g. `isDigit`, `isAlpha`, `starts_with`), import the
self-hosted `[jpx.string]` package — see [modules.md](modules.md).

## Related Pages

- [lists-dicts.md](lists-dicts.md) — the results of `.split()` and `.toCharArray()` are lists
- [built-in-functions.md](built-in-functions.md) — `len()`, `str()`, `ord()`, `chr()`
