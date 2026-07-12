# JPX Language Syntax Reference

Bahasa pemrograman JPX — sintaks, semantik, dan identitas.

## Identitas JPX

JPX adalah bahasa pemrograman dinamis yang:
- **Syntax mirip JavaScript/C** (curly braces, semicolons)
- **Keyword ringkas** (mirip Python — `print`, `function`, `if/elif/else`)
- **String interpolation** dengan `$var` (mirip PHP/bash)
- **Multi-paradigm**: procedural + functional + OOP
- **Self-hosting ready**: stdlib bisa ditulis dalam JPX sendiri

---

## 1. Comments

```jpx
# Single-line comment (Python style)

# Block comment dengan multiple #
# seperti ini.
```

> **Catatan**: `//` tadinya komentar, tapi sekarang jadi operator **integer division**.

---

## 2. Variables & Assignment

### Declaration
```jpx
# Single declaration (variable global)
global [x = 42];
global [name = "Alice"];

# Multiple declaration
global [a = 1, b = 2, c = 3];

# Local assignment (di dalam function)
local [tmp = compute()];

# Mutable assignment (tanpa global)
x = 10;
y = "hello";
```

### Multiple Assignment
```jpx
# Swap
x, y = y, x;

# Triple assign
a, b, c = 1, 2, 3;
```

### Index/Property Assignment
```jpx
# List element
arr[0] = 99;
arr[i + 1] = 42;

# Nested
matrix[0][1] = 7;

# Object/instance field
obj.field = "value";
self.count = 0;
```

---

## 3. Operators

### Arithmetic
| Operator | Description | Example | Result |
|----------|-------------|---------|--------|
| `+` | Add / String concat / List concat | `3 + 4` | `7` |
| `-` | Subtract | `10 - 3` | `7.0` |
| `*` | Multiply | `6 * 7` | `42.0` |
| `/` | Float divide | `10 / 4` | `2.5` |
| `//` | Integer divide | `10 // 4` | `2` |
| `%` | Modulo | `17 % 5` | `2` |
| `-x` | Unary minus | `-5` | `-5` |

### Comparison
| Operator | Example | Result |
|----------|---------|--------|
| `==` | `5 == 5` | `true` |
| `!=` | `5 != 6` | `true` |
| `<` | `3 < 5` | `true` |
| `>` | `5 > 3` | `true` |
| `<=` | `5 <= 5` | `true` |
| `>=` | `5 >= 5` | `true` |

### Logical
```jpx
if a and b { ... }
if a or b { ... }
if not a { ... }
# atau:
if a && b { ... }
if a || b { ... }
```

### Ternary
```jpx
result = cond ? "yes" : "no";
```

---

## 4. Control Flow

### if / elif / else
```jpx
if score >= 90 {
    print "A";
} elif score >= 80 {
    print "B";
} elif score >= 70 {
    print "C";
} else {
    print "F";
}
```

### while
```jpx
while i < 10 {
    print i;
    i = i + 1;
}

while true {
    if done { break; }
    if skip { continue; }
}
```

### for-to (numeric range)
```jpx
for i = 1 to 10 {
    print i;
}
```

### for-in (iterable)
```jpx
for item in [1, 2, 3, 4] {
    print item;
}

for ch in "hello" {
    print ch;
}
```

### try-catch
```jpx
try {
    risky_operation();
} catch (e) {
    print "Error: " + e;
}
```

---

## 5. Functions

### Named Function
```jpx
function add(a, b) {
    return a + b;
}

print add(3, 4);  # 7
```

### Function with Default Args (parser supports, runtime TODO)
```jpx
function greet(name, greeting = "Hello") {
    return greeting + ", " + name;
}
```

### Closures
```jpx
global [PI = 3.14];

function area(r) {
    return PI * r * r;  # captures PI from outer scope
}

# Function returning function
function makeMultiplier(factor) {
    function multiply(x) {
        return x * factor;
    }
    return multiply;
}

global [double = makeMultiplier(2);
print double(5);  # 10
```

---

## 6. Classes (NEW — Phase B)

```jpx
class Point {
    __init__(self, x, y) {
        self.x = x;
        self.y = y;
    }

    distance(self, other) {
        global [dx = self.x - other.x];
        global [dy = self.y - other.y];
        return (dx * dx + dy * dy) ** 0.5;
    }

    toString(self) {
        return "(" + self.x + ", " + self.y + ")";
    }
}

global [p1 = Point(0, 0);
global [p2 = Point(3, 4);
print p1.distance(p2);  # 5
print p2.toString();    # (3, 4)
```

**Catatan**: 
- Method parameter pertama harus `self` (mirip Python)
- Field diakses via `self.field_name`
- Constructor namanya `__init__`

---

## 7. Strings

### String Literals
```jpx
"double quote string"
'single quote string'
"""triple-quoted string"""
```

### String Interpolation
```jpx
global [name = "Alice";
global [age = 30;
print "Hello, $name! You are $age years old.";
# Output: Hello, Alice! You are 30 years old.
```

### Escape Sequences
| Escape | Meaning |
|--------|---------|
| `\n` | Newline |
| `\t` | Tab |
| `\r` | Carriage return |
| `\\` | Backslash |
| `\"` | Double quote |
| `\'` | Single quote |
| `\0` | Null byte |

### String Indexing & Slicing
```jpx
global [s = "hello";
s[0]        # "h"
s[-1]       # "o"
s[1:4]      # "ell"
s[:3]       # "hel"
s[2:]       # "llo"
```

### String Methods (Native)
```jpx
s.split(",")          # split ke list
s.strip()             # trim whitespace
s.replace("a", "b")   # replace all
s.upper()             # uppercase
s.lower()             # lowercase
s.contains("sub")     # bool
s.startsWith("pre")   # bool
s.endsWith("suf")     # bool
s.find("sub")         # index or -1
s.count("sub")        # int
s.repeat(n)           # string repeated n times
s.substring(start, end)  # slice
s.toCharArray()       # list of chars
```

---

## 8. Lists

### List Literal
```jpx
global [nums = [1, 2, 3, 4, 5];
global [mixed = [1, "two", true, null];
global [nested = [[1, 2], [3, 4]];
```

### List Operations
```jpx
nums[0]            # akses index
nums[-1]           # index negatif (dari belakang)
nums[1:3]          # slice
len(nums)          # panjang (3)
nums + [6, 7]      # concat list
nums[0] = 99       # mutable assignment
```

### List Library (`[array]`)
```jpx
[array];
array.sort([3,1,4,1,5])        # [1,1,3,4,5]
array.reverse([1,2,3])         # [3,2,1]
array.sum([1,2,3,4])           # 10
array.max([3,7,2])             # 7
array.min([3,7,2])             # 2
array.contains([1,2,3], 2)     # true
array.indexOf([1,2,3], 2)      # 1
array.join([1,2,3], ",")       # "1,2,3"
array.push([1,2], 3)           # [1,2,3]
array.pop([1,2,3])             # [1,2]
```

---

## 9. Objects (Dicts)

### Object Literal
```jpx
global [person = {
    "name": "Alice",
    "age": 30,
    "active": true
};
```

### Access
```jpx
person["name"]     # "Alice"
person.name        # "Alice" (sugar)
person["age"] = 31 # mutable
```

---

## 10. Imports

### Single Module
```jpx
[string];      # import module
[mathx];       # bisa .py atau .jpx
```

### Multi-Module
```jpx
[math, time, json];
```

### Single Attribute
```jpx
[utils.formatNumber];
```

### Multi-Attribute
```jpx
[validator.isEmail, validator.isAlpha];
```

### Search Path Priority
1. Script directory (relative import)
2. `lib/` di current working directory
3. `JPX_PATH` env variable
4. `stdlib/` built-in library

---

## 11. Built-in Functions

```jpx
print(x)              # output ke stdout
int(x)                # convert ke int
float(x)              # convert ke float
str(x)                # convert ke string
bool(x)               # convert ke bool
len(x)                # panjang string/list/dict
ord(s)                # char code dari first char
chr(n)                # char dari code
type(x)               # nama tipe ("int", "str", "list", dll)
```

### Constants
```jpx
true                  # boolean true
false                 # boolean false
null                  # null/None
```

---

## 12. Reserved Keywords

```
function  return  if  elif  else  while  for  in  to
break  continue  try  catch  global  import
class  self  __init__
true  false  null  and  or  not
```

---

## 13. JPX Identity (Filosofi)

1. **Semicolons required** — setiap statement diakhiri `;`
2. **Curly braces required** — untuk semua block (`if`, `while`, `for`, `function`, `class`)
3. **`global [name = value]`** — declaration explicit, bukan implicit assignment
4. **String interpolation `$var`** — built-in, no f-string needed
5. **`self` explicit** — mirip Python, bukan implicit `this`
6. **`//` integer division** — bukan komentar (komentar pakai `#`)
7. **Hybrid modules** — `.py` (native) + `.jpx` (self-hosted) hidup berdampingan
