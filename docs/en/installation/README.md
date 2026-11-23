# Installing JPX

This page summarizes all official ways to install JPX A2. Pick one method that suits
your needs — all of them produce the same `jpx` CLI.

## Method Overview

| Method | Command / Steps | Best for | Status |
|---|---|---|---|
| [Via repository](via-repository.md) | Download the binary release, or `git clone` + Python | All users; the most reliable way | ✅ Available |
| [Via shogun](via-shogun.md) | `shogun install` from the shogun catalog | Users who already use shogun | ✅ Available |
| [Via Chocolatey](via-choco.md) | `choco install Jpx-cli` | Windows users who use Chocolatey | ⏳ **Coming soon** |

## Requirements

**Using the release binary** (recommended):

- Windows x64 or Linux x86-64.
- No Python needed — the binary is built with PyInstaller and bundles the Python runtime
  inside it.
- Follow the important rule: the `library/` folder must stay **next to** the executable,
  because the interpreter looks for built-in modules relative to its own location.

**Running from source:**

- Python 3.x (used and tested on Python 3.12).
- Git (to clone the repository).
- Most JPX built-in modules only use the Python standard library. Two exceptions:
  `[color]` requires the pip package `colorama`, and the Windows modules (`win32sys`,
  `win32ui`) require `pywin32` and only run on Windows.

## Verify After Installing

Whichever method you used, verify with:

```bash
jpx --version
```

Expected output (the Python version on the second line depends on your system):

```text
JPX A2 - A exclusive version
Python: 3.12.16
Root: <JPX installation location>
Library: <JPX installation location>/library
User lib: <JPX installation location>/lib
```

If the `jpx` command is not recognized yet, add the installation folder to your system
`PATH`, or run it with the full path (e.g. `./jpx` on Linux, `jpx.exe` on Windows).

## Next Steps

- Run your first script: [cli/basic-commands.md](../cli/basic-commands.md)
- Learn the syntax: [syntax/README.md](../syntax/README.md)
