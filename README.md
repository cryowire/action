# cryo-wiring/action

GitHub Action for validating and building [cryo-wiring](https://github.com/cryo-wiring) configurations in CI.

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
      - uses: cryo-wiring/action@v1
```

This automatically finds all cooldown directories (containing `metadata.yaml` + `control.yaml`) and runs `validate` + `build` on each.

### Validate only

```yaml
- uses: cryo-wiring/action@v1
  with:
    command: validate
```

### Specific directories

```yaml
- uses: cryo-wiring/action@v1
  with:
    cooldown-dirs: anemone/2026/cd001 anemone/2026/cd002
```

### Generate diagrams

```yaml
- uses: cryo-wiring/action@v1
  with:
    command: diagram

- uses: actions/upload-artifact@v4
  with:
    name: diagrams
    path: "**/wiring.svg"
```

### Pin CLI version

```yaml
- uses: cryo-wiring/action@v1
  with:
    cli-version: ">=0.1.0,<0.2.0"
```

## Inputs

| Input | Default | Description |
|---|---|---|
| `command` | `all` | `validate`, `build`, `diagram`, or `all` (validate + build) |
| `cooldown-dirs` | *(auto-discover)* | Space-separated cooldown directory paths |
| `diagram-output` | `wiring.svg` | Output filename for diagram command |
| `cli-version` | *(latest)* | Version constraint for cryo-wiring-cli |
| `python-version` | `3.11` | Python version |

## Outputs

| Output | Description |
|---|---|
| `cooldown-dirs` | Newline-separated list of processed directories |
| `passed` | `true` if all commands succeeded |

## How it works

1. Sets up Python and installs `cryo-wiring-cli` from PyPI
2. Discovers cooldown directories by searching for `metadata.yaml` files (or uses explicit paths)
3. Runs the specified command(s) on each directory
4. Reports results with exit code 0 (all passed) or 1 (any failed)

## Adding to your data repository

If you created your data repo from [cryo-wiring/template](https://github.com/cryo-wiring/template), add `.github/workflows/ci.yml`:

```yaml
name: CI
on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: cryo-wiring/action@v1
```

This validates every cooldown on every push and pull request.
