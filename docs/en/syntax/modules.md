# Modules & Import

## How to Import

Put imports at the top of the script. The syntax is the `module_name` inside square
brackets, ending with `;`:

```jpx
[string];
[array];
[math];
```

The result is available as an object named after the module: `string.upper("hi")`,
`array.sum([1, 2])`, and so on.

## Built-in Native Modules (`.py`)

The following modules ship with JPX (Python implementations, standard library except
where noted):

`array` `beuty` `color` `env` `fs` `hash` `JpXhash` `JpXUi` `json` `math` `mem`
`notification` `print` `random` `ReGx` `requests` `scanner` `speedreq` `string`
`subnotif` `system` `time` `win32sys` `win32ui`

Special dependencies:

| Module | Requirement |
|---|---|
| `[color]` | the pip package `colorama` — `pip install colorama`; without it the import fails |
| `[win32sys]`, `[win32ui]` | the pip package `pywin32`, **Windows only** |
| others | Python standard library — no extra installation |

When you see `No module named '...'`, it means the module uses a third-party library
that is not installed yet — install it via pip.

## Self-Hosted Packages (`library/jpx/*.jpx`)

Part of the library is written in JPX's own syntax and imported using a dot:

```jpx
[jpx.string];
[jpx.io];
[jpx.types];
[jpx.functional];
[jpx.choose];
```

Modules inside a package are exported under their **last name**:

```jpx
[jpx.string];
print string.isDigit("5");      # True
print string.isAlpha("B");      # True
```

> `[io]` alone **won't** work — the `io` module lives inside the `jpx` package, so write
> `[jpx.io]`.

## Module Usage Example

```jpx
[string];
[array];
[mathx];
[json];
[time];

print string.upper("hi");               # HI
print string.starts_with("abc", "a");   # True

print array.sum([1, 2, 3]);             # 6
print array.sort([3, 1, 2]);            # [1, 2, 3]

print mathx.fib(10);                    # 55
print mathx.isPrime(17);                # True
print mathx.gcd(12, 8);                 # 4
print mathx.lcm(4, 6);                  # 12
print mathx.power(2, 8);                # 256
print mathx.mean([1, 2, 3]);            # 2.0

print json.encode({"a": 1});            # {"a": 1}
print time.now();                       # 2026-11-22 10:39:39
```

Available `mathx` functions:
`fib` `factorial` `isPrime` `gcd` `lcm` `power` `isqrt` `mean` `median`

See the list of modules detected on your system:

```bash
jpx --list-modules
```

## Module Search Order

When a script calls `[module];`, the interpreter looks for a `module.jpx` or `module.py`
file (or a package folder containing `_jpx_.jpx`) in this priority order:

1. **The script's folder** — the directory of the running `.jpx` file
   (supports relative imports).
2. **`lib/` in the working directory** — where `jpxkg` installs packages.
3. **`JPX_PATH`** — extra directories from the environment variable (`;`-separated on
   Windows or `:` on Linux).
4. **The built-in `library/`** — the last fallback.

Set `JPX_PATH` to add custom module locations:

```bash
# Linux / macOS
export JPX_PATH="/home/me/jpx-modules:/opt/jpx-modules"

# Windows PowerShell
$env:JPX_PATH = "C:\jpx-modules;C:\opt\jpx-modules"
```

## Writing Your Own Module

1. Put a `mymodule.jpx` file (or `mymodule.py` for a Python implementation) in your
   script's folder, or in a folder listed on the search path above.
2. Import it with `[mymodule];`.
3. Confirm it's detected with `jpx --list-modules`.

Third-party packages can be installed with `jpxkg` — see
[../cli/jpxkg.md](../cli/jpxkg.md).

## Security Notes

Importing a `.py` module means executing Python code from that file. Only import modules
from sources you trust (built-ins, `lib/` from `jpxkg`, or your own files).

## Related Pages

- [../cli/jpxkg.md](../cli/jpxkg.md) — installing packages with the package manager
- [../cli/basic-commands.md](../cli/basic-commands.md) — `--list-modules` and `JPX_PATH`
- [lists-dicts.md](lists-dicts.md) — the `array` module for lists
