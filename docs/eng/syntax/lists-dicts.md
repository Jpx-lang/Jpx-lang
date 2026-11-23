# Lists and Dicts

## Lists

Lists are written with square brackets, elements separated by commas, indexes starting
at 0:

```jpx
global [l = [10, 20, 30]];

print l;                 # [10, 20, 30]
print l[0];              # 10
print len(l);            # 3
```

Elements can be of mixed types: `[1, "two", true, [3]]`.

### The `push` Method

`push` appends an element to the end of the list **directly on the original list**:

```jpx
global [l = [3, 1, 2]];

l.push(4);
print l;                 # [3, 1, 2, 4]
```

### Indexing Inside Interpolation

Accessing elements inside `${...}` works too:

```jpx
global [nums = [3, 1, 4]];
print "first element: ${nums[0]}";     # first element: 3
```

### The `array` Module

Richer list operations live in the built-in `[array]` module:

```jpx
[array];

global [nums = [3, 1, 4, 1, 5]];

print array.sum(nums);       # 14
print array.max(nums);       # 5
print array.min(nums);       # 1
print array.first(nums);     # 3
print array.last(nums);      # 5
print array.sort(nums);      # [1, 1, 3, 4, 5]
print array.reverse(nums);   # [5, 1, 4, 1, 3]
print array.contains(nums, 4);   # True
print array.join(nums, "-");     # 3-1-4-1-5
```

Available `array` functions:
`push` `pop` `first` `last` `contains` `indexOf` `count` `reverse` `sort` `sum` `max`
`min` `join` `slice`

## Dicts

Dicts are written with curly braces, `"key": value` pairs:

```jpx
global [d = {"name": "JPX", "ver": "A2"}];

print d["name"];         # JPX
print "ver" in d;        # True
```

- Key access uses square brackets: `d["name"]`.
- Key existence is tested with the `in` operator.
- When printed, dicts appear Python repr style: `{'name': 'JPX', 'ver': 'A2'}`
  (single quotes).

### Rewriting Dict Values

```jpx
global [d = {"count": 1}];
d["count"] = d["count"] + 1;
print d["count"];          # 2
```

## Iteration

`for ... in` iterates over lists; for dicts, iteration happens over the list of keys:

```jpx
global [d = {"a": 1, "b": 2}];
for k in ["a", "b"] {
    print k + " = " + str(d[k]);
}
```

## Related Pages

- [modules.md](modules.md) — how to import `[array]` and other modules
- [strings.md](strings.md) — `split()` and `toCharArray()` produce lists
- [control-flow.md](control-flow.md) — `for ... in` and `break`/`continue`
