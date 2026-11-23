# Installation Via Shogun

If you already use **shogun** as your package manager/CLI tool, JPX can be installed
straight from the shogun catalog without manually downloading a release.

## Steps

1. Make sure shogun is installed and callable:

   ```bash
   shogun --version
   ```

2. Install JPX:

   ```bash
   shogun install jpx-cli
   ```

3. Verify the installation:

   ```bash
   jpx --version
   ```

   The expected output starts with:

   ```text
   JPX A2 - A exclusive version
   ```

## Updating and Uninstalling

Use shogun's built-in commands to manage the package, depending on your shogun version:

```bash
shogun update jpx-cli     # update to the latest version (if supported)
shogun uninstall jpx-cli  # remove the installation (if supported)
```

## Important Notes

- **Package name**: the commands on this page use the package name `jpx-cli`. The exact
  name follows the shogun catalog you are using — if `shogun install jpx-cli` is not
  found, look through the package list with shogun's search command (e.g.
  `shogun search jpx`) and adjust the package name.
- **File layout**: whatever the installation method, the `library/` folder must stay next
  to the `jpx` binary (see [via-repository.md](via-repository.md)). If shogun places files
  in a custom location, make sure that layout stays intact.
- **Alternative**: if this method gives you trouble, use the
  [via repository](via-repository.md) method, which always uses the latest official
  release.

## Next Steps

- Run your first script: [cli/basic-commands.md](../cli/basic-commands.md)
