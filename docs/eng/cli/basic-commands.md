# Basic `jpx` CLI Commands

Every output on this page is real output from the A2 CLI (the Python version in the
examples depends on your system).

## Running a Script

```bash
jpx file_name.jpx
```

Example — a file `hello.jpx`:

```jpx
global [name = "World"];
print "Hello, $name!";
```

Produces:

```text
Hello, World!
```

Important details when running:

- The folder containing the `.jpx` file is automatically added to the **module search
  path**, so `[module];` can import `.jpx`/`.py` files in the same folder (relative
  imports).
- Runtime errors are displayed as `Runtime Error: <message>` and the program exits with
  exit code `1`. Use `try/catch` to catch them inside the script.
- Press Ctrl+C to interrupt; it exits with exit code `130`.

## `jpx --version` / `-v`

```bash
jpx --version
```

```text
JPX A2 - A exclusive version
Python: 3.12.16
Root: /installation/location/jpx
Library: /installation/location/jpx/library
User lib: /installation/location/jpx/lib
```

Useful to confirm the CLI you called really is version A2, and to see where `library/`
and `lib/` are searched.

## `jpx --help` / `-h`

```text
JPX Programming Language
Version: JPX A2 - A exclusive version

Usage:
  jpx <file.jpx>              Run a JPX script
  jpx --version, -v            Show version information
  jpx --help, -h               Show this help message
  jpx --info                    Show system information

Examples:
  jpx script.jpx
  jpx examples/hello.jpx

Environment:
  JPX_PATH                      Additional library paths

More info: https://github.com/alzzmetth/Jpx-lang
```

> **Note**: `--list-modules` and `--jpx-interpreter` **work** but are not yet listed in
> the `--help` text. This document is the complete reference.

## `jpx --info`

System information, more complete than `--version`: root/library paths, the existence
status of each folder (`✓`/`✗`), platform, Python version, and the contents of `JPX_PATH`
when set.

```bash
jpx --info
```

Use this command right after installing to confirm the folder structure is correct
(remember: `library/` must be next to the executable).

## `jpx --list-modules`

Shows all modules detected across all search paths, tagged `[PY]` (Python implementation)
or `[JPX]` (written in JPX itself), followed by the total and the search path order:

```text
Available JPX modules:
=================================================
  [PY] json            (library/json.py)
  [PY] math            (library/math.py)
  [JPX] array          (library/array.jpx)
  [JPX] mathx          (library/mathx.jpx)
  ...

Total: 27 modules

Search paths (priority order):
  1. ✗ /working/folder/lib
  2. ✓ /installation/location/jpx/library
```

If a module you wrote doesn't appear here, your script won't be able to import it either
— fix the file location or add its folder to `JPX_PATH`. The complete priority order is
explained in [../syntax/modules.md](../syntax/modules.md).

## `jpx --jpx-interpreter <file.jpx>`

Runs the script through the **self-hosted interpreter** (lexer, parser, AST, and
evaluator written in JPX itself, in the `bootstrap/` folder). This is an **experimental**
feature demonstrating self-hosting progress — its output starts with a banner:

```text
[JPX-Interpreter] Running hello.jpx with self-hosted interpreter
[JPX-Interpreter] (experimental — subset features only)
```

Officially stated limitations:

- Module imports are not supported (the evaluator has no module loader yet).
- Class instantiation is minimal only.
- Try-catch is not fully supported.
- Native string methods are not supported.

**Warning**: on this path, failures can happen **without any message** — statements that
fail to execute may silently disappear from the output. Use the main interpreter
(`jpx file.jpx`) for real work; use `--jpx-interpreter` only for demos and testing the
bootstrap components.

## The `JPX_PATH` Environment Variable

Adds module search directories. Example:

```bash
# Linux / macOS
export JPX_PATH="/home/me/jpx-modules:/opt/jpx-modules"
jpx app.jpx

# Windows (PowerShell)
$env:JPX_PATH = "C:\jpx-modules;C:\opt\jpx-modules"
jpx app.jpx
```

Check the effect via the `Search paths` section of `jpx --list-modules`.

## Running Without Installation (From Source)

If you cloned the repository, all the commands above can be called directly through
Python:

```bash
python3 jpx.py script.jpx
python3 tests/run_tests.py     # official test suite
```

## Related Pages

- [jpxkg.md](jpxkg.md) — installing packages with the package manager
- [../syntax/modules.md](../syntax/modules.md) — search path order and writing modules
- [../installation/via-repository.md](../installation/via-repository.md) — installation
