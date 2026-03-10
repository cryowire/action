<p align="center"><a href="https://github.com/cryowire">
  <img src="https://raw.githubusercontent.com/cryowire/artwork/main/logo-type/logotype.png" alt="cryowire" width="600" />
</a></p>

<h1 align="center">cryowire/action</h1>
<p align="center">GitHub Action for validating and building <a href="https://github.com/cryowire">cryowire</a> configurations in CI.</p>
<p align="center">
  <a href="https://cryowire.github.io/"><img src="https://img.shields.io/badge/Website-cryowire.github.io-38bdf8?style=for-the-badge" alt="Website" /></a>
</p>

## Usage

### Basic (auto-discover all cooldowns)

```yaml
name: Validate
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: cryowire/action@v1
```

This automatically finds all cooldown directories (containing `metadata.yaml` + `control.yaml`) and runs `validate` + `build` on each.

### Validate only

```yaml
- uses: cryowire/action@v1
  with:
    command: validate
```

### Specific directories

```yaml
- uses: cryowire/action@v1
  with:
    cooldown-dirs: your-cryo/2026/cd001 your-cryo/2026/cd002
```

### Generate diagrams

```yaml
- uses: cryowire/action@v1
  with:
    command: diagram

- uses: actions/upload-artifact@v4
  with:
    name: diagrams
    path: "**/wiring.svg"
```

### Pin CLI version

```yaml
- uses: cryowire/action@v1
  with:
    cli-version: ">=0.1.0,<0.2.0"
```

## Inputs

| Input | Default | Description |
|---|---|---|
| `command` | `all` | `validate`, `build`, `diagram`, or `all` (validate + build) |
| `cooldown-dirs` | *(auto-discover)* | Space-separated cooldown directory paths |
| `diagram-output` | `wiring.svg` | Output filename for diagram command |
| `cli-version` | *(latest)* | Version constraint for cryowire |
| `python-version` | `3.11` | Python version |

## Outputs

| Output | Description |
|---|---|
| `cooldown-dirs` | Newline-separated list of processed directories |
| `passed` | `true` if all commands succeeded |

## How it works

1. Sets up Python and installs `cryowire` from PyPI
2. Discovers cooldown directories by searching for `metadata.yaml` files (or uses explicit paths)
3. Runs the specified command(s) on each directory
4. Reports results with exit code 0 (all passed) or 1 (any failed)

## Adding to your data repository

If you created your data repo from [cryowire/template](https://github.com/cryowire/template), add `.github/workflows/ci.yml`:

```yaml
name: CI
on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: cryowire/action@v1
```

This validates every cooldown on every push and pull request.
