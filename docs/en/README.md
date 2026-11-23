# JPX Documentation

Welcome to the official documentation of the **JPX** programming language, version **A2**.

JPX is a dynamic scripting language that blends traits of several popular languages:
curly-brace blocks and semicolons (C/JavaScript style), concise keywords (Python style),
`$var` string interpolation (PHP/bash style), the `|>` pipeline operator (Elixir style), and
`switch` without fall-through (Go style). JPX is designed for experimentation, light
automation, and exploring a minimalist runtime concept.

> **Important note**: JPX is **case-sensitive**. Every keyword is written in lowercase —
> `print`, not `Print`; `global`, not `Global`.

> 🌐 **Language**: this is the English edition of the documentation. The Indonesian edition
> lives one level up: [docs/README.md](../README.md).

---

## Documentation Map

| Folder / File | Contents |
|---|---|
| [`installation/`](installation/README.md) | How to install JPX: via the repository (binary release or source), via `shogun install`, and `choco install Jpx-cli` (coming soon) |
| [`syntax/`](syntax/README.md) | Complete syntax reference, split per topic: variables, data types, print & interpolation, operators, control flow, functions, class, strings, lists & dicts, modules, built-in functions, and limitations |
| [`cli/`](cli/README.md) | How to use the `jpx` CLI: running scripts, command-line options, environment variables, exit codes, and the `jpxkg` package manager |

---

## Quick Start

Once JPX is installed (see [installation/README.md](installation/README.md)), create a
file `hello.jpx`:

```jpx
global [name = "World"];
print "Hello, $name!";
print "Now: ${2025 + 1}";
```

Run it:

```bash
jpx hello.jpx
```

Output:

```text
Hello, World!
Now: 2026
```

---

## Version Status

This documentation was written for **JPX A2** ("A exclusive version"). Every syntax example
in the `syntax/` folder has been executed and verified against the A2 interpreter. Features
that are **not yet** supported are honestly collected in
[syntax/limitations.md](syntax/limitations.md) — read that page first so you don't run
into known limitations by surprise.

The legacy documentation (`docs.md` and the v1.0 `installation.md`) no longer reflects the
A2 syntax (it still uses capitalized `Global`/`Print`) and has been superseded by the
documents in this folder.

---

## Official Links

- Repository: <https://github.com/Jpx-lang/Jpx-lang>
- Releases page: <https://github.com/Jpx-lang/Jpx-lang/releases>
- Project website: <https://jpx-lang.netlify.app>
- Package download page (jpxkg): <https://jpxkg.netlify.app/>
