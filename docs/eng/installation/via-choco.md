# Installation Via Chocolatey — Coming Soon

> ⏳ **Status: NOT AVAILABLE YET.**
> The `Jpx-cli` package is being prepared for Chocolatey and **cannot** be installed at
> the time this document was written. This page is published early so the documentation
> structure is complete; the commands below will become active once the package ships.

## Planned Commands

Once the package is published, Windows users with Chocolatey will install JPX with:

```powershell
choco install Jpx-cli
```

Verify:

```powershell
jpx --version
```

Update and uninstall:

```powershell
choco upgrade Jpx-cli
choco uninstall Jpx-cli
```

## Preparation (Once the Package Is Released)

1. Install [Chocolatey](https://chocolatey.org/install) if you don't have it yet.
2. Run `choco install Jpx-cli` from a terminal with administrator privileges.
3. Chocolatey places `jpx.exe` plus the `library/` folder in the package location and
   adds them to `PATH`, so `jpx` becomes immediately callable.

## Interim Alternatives

While waiting for the Chocolatey package, use one of the methods that already work:

- [Via repository](via-repository.md) — download `jpx.exe` / `jpx-win64.zip` from the
  GitHub releases page (no Python needed), or clone the source and run it with Python.
- [Via shogun](via-shogun.md) — if you use shogun.
