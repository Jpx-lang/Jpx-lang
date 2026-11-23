# Installation Via the Repository

This is the most reliable method: getting JPX straight from the official GitHub repository
[Jpx-lang/Jpx-lang](https://github.com/Jpx-lang/Jpx-lang). There are two paths:

1. **Path A — download the release binary** (no Python). Recommended for general users.
2. **Path B — clone the source and run it with Python**. Best if you want to read, change,
   or contribute to JPX.

---

## Path A — Download the Release Binary (No Python)

The binary is built with PyInstaller 6.22.3 and bundles the Python runtime inside it, so
the target machine does not need Python installed.

### Steps

1. Open the releases page: <https://github.com/Jpx-lang/Jpx-lang/releases>
2. Pick the **A2** release.
3. Download the asset for your system:

   | Asset | For |
   |---|---|
   | `jpx.exe` | Windows x64 (executable only) |
   | `jpx-win64.zip` | Windows x64 (executable + `library/` + `bootstrap/` + docs) |
   | `jpx-x86-linux.zip` | Linux x86-64 (executable + `library/` + `bootstrap/` + docs) |

4. Extract the archive to a permanent folder, for example:
   - Windows: `C:\Tools\jpx\`
   - Linux: `~/.local/share/jpx/` or `/opt/jpx/`
5. Add that folder to `PATH` so the `jpx` command can be called from anywhere, or call it
   with the full path.

### Important: Do Not Separate the `library/` Folder

The interpreter looks for built-in modules relative to the location of the executable. The
`library/` folder (containing modules such as `fs`, `json`, `time`, `requests`) and
`bootstrap/` must stay next to `jpx`. If they are moved elsewhere, scripts that import
modules will fail with `Module not found` even though the binary itself runs fine.

### Verify

```bash
jpx --version
```

See the [installation README](README.md) for the full example output.

---

## Path B — Clone and Run From Source

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/Jpx-lang/Jpx-lang.git
   cd Jpx-lang
   ```

2. Enter the `jpx-lang/` folder — this is where the interpreter and libraries live:

   ```bash
   cd jpx-lang
   ```

3. Run JPX scripts directly with Python (no build step):

   ```bash
   python3 jpx.py some_file.jpx
   ```

4. (Optional) Make `jpx` callable directly by creating an alias or wrapper, for example
   on Linux:

   ```bash
   sudo ln -s "$(pwd)/jpx.py" /usr/local/bin/jpx
   ```

   Note: a symlink-based wrapper needs a correct shebang and executable permission
   (`chmod +x jpx.py`). If you don't want the hassle, always run with
   `python3 jpx.py <file.jpx>`.

### Verification and Tests

```bash
python3 jpx.py --version          # version and library locations
python3 jpx.py --list-modules     # module list + search paths
python3 tests/run_tests.py        # official test suite (almost all should pass)
```

Last verified: `run_tests.py` passed 25 of 26 tests, and `run_e2e.py` passed everything.

### Structure You Should Know

```text
jpx-lang/
├── jpx.py            # CLI entry point
├── interpreter/      # execution engine (interpreter, eval, parser, lexer, importer)
├── library/          # native built-in modules (.py) and self-hosted (.jpx)
├── bootstrap/        # experimental self-hosted interpreter (written in JPX)
├── tests/            # test suite (unit, e2e, bootstrap)
└── examples/         # example programs
```

---

## Common Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `Error: File 'x.jpx' not found` | Wrong path / not in the working folder | Run from the file's folder, or use the full path |
| `Module not found` on import | The `library/` folder was separated from the executable | Put `library/` back next to `jpx` |
| A specific module missing from `--list-modules` | Custom module folder not on the search path | Check the bottom of `--list-modules`; add the folder via `JPX_PATH` |
| `No module named 'colorama'` | The `[color]` module needs pip | `pip install colorama` |
| `No module named 'win32api'` | The `win32*` modules need pywin32 (Windows only) | `pip install pywin32` |

## Next Steps

- Install extra packages with `jpxkg`: [cli/jpxkg.md](../cli/jpxkg.md)
- All CLI options: [cli/basic-commands.md](../cli/basic-commands.md)
