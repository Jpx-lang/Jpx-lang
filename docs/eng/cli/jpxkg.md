# `jpxkg` — The JPX Package Manager

`jpxkg` is the JPX package manager (version 1.0). Packages are fetched from an
`index.json`-based catalog, downloaded, verified with SHA256, then installed into the
`lib/` folder, which also becomes a JPX module search path. The catalog is also
accessible via the web at <https://jpxkg.netlify.app/>.

## Commands

```bash
jpxkg install <package>   # install a package from the catalog
jpxkg -v                  # show the jpxkg version
```

Without arguments, `jpxkg` prints a short help summary.

### Example

```bash
jpxkg install samplepackage
```

Typical installation output:

```text
📦 Downloading samplepackage...
  Progress: 100%
  Verifying SHA256...
✅ SHA256 OK
✅ Installed samplepackage to lib/samplepackage.py (12.3 KB)
```

## How Installation Works

1. `jpxkg` reads `index.json` in the JPX installation folder.
2. The package is looked up by `name`; if it's not there, the list of available packages
   is displayed to make searching easy.
3. The file is downloaded from the package's `download_url`.
4. When `sha256` is available in the catalog, the file is verified; a **checksum
   mismatch** raises a warning and a confirmation — it's best to answer `n` when unsure.
5. The file is installed to `install_path` (usually `lib/<name>.py`). When the file
   already exists, `jpxkg` asks for confirmation before overwriting.
6. When the package has `dependencies` (Python dependencies), `jpxkg` lists them for
   manual installation via pip:

   ```text
   ⚠️ Dependencies:
     • colorama (pip install colorama)
   ```

## The `index.json` Format

`jpxkg` reads the following structure from `index.json`:

```json
{
  "modules": [
    {
      "name": "samplepackage",
      "download_url": "https://example.example/samplepackage.py",
      "sha256": "64-character-hex-hash",
      "install_path": "lib/samplepackage.py",
      "dependencies": ["colorama"]
    }
  ]
}
```

All keys are optional except `name` and `download_url`. Once `index.json` exists in the
installation folder, `[samplepackage];` can be imported directly from JPX scripts
because the `lib/` folder is on the search path (priority order: script folder → `lib/`
→ `JPX_PATH` → built-in `library/` — see [../syntax/modules.md](../syntax/modules.md)).

## Security Notes

- Packages from the catalog are Python code that executes on import — install only from
  sources you trust.
- Always let the SHA256 verification run; if the checksum doesn't match, stop the
  installation and report it to the catalog owner.
- `jpxkg` currently only provides the `install` command (no `search`, `update`, or
  `uninstall` yet). Removing a package is done manually by deleting its file in the
  `lib/` folder.

## Related Pages

- [basic-commands.md](basic-commands.md) — the `jpx` CLI options and `--list-modules`
- [../syntax/modules.md](../syntax/modules.md) — search paths and custom modules
- Web catalog: <https://jpxkg.netlify.app/>
