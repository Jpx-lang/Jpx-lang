# CLI `jpx`

All interaction with JPX happens through the `jpx` command. This folder explains every
command, option, environment variable, exit code, and the `jpxkg` package manager.

## Command List

| Command | Purpose |
|---|---|
| `jpx <file.jpx>` | Run a JPX script |
| `jpx --version`, `-v` | Show version and library locations |
| `jpx --help`, `-h` | Show help |
| `jpx --info` | System information and installation folder status |
| `jpx --list-modules` | List all detected modules + search paths |
| `jpx --jpx-interpreter <file.jpx>` | Run with the self-hosted interpreter (experimental) |

Details for every option with real output examples:
[basic-commands.md](basic-commands.md).

## Environment Variables

| Variable | Purpose |
|---|---|
| `JPX_PATH` | Adds module search directories (`;`-separated on Windows, `:` on Linux) |

## Exit Codes

| Code | Meaning |
|---|---|
| `0` | Script finished normally |
| `1` | Runtime error / file not found |
| `130` | Execution interrupted (Ctrl+C) |

These exit codes are useful for scripting: `jpx job.jpx && echo "success"`.

## Package Manager

JPX packages are installed with `jpxkg install <package>` — installation is based on
`index.json`, with SHA256 verification. See [jpxkg.md](jpxkg.md).

## Installation Pages

Haven't installed JPX yet? Start from
[../installation/README.md](../installation/README.md).
