"""Entry point for the cryowire GitHub Action."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def discover_cooldown_dirs(root: Path) -> list[Path]:
    """Find all cooldown directories (containing metadata.yaml) under *root*."""
    dirs: list[Path] = []
    for meta in sorted(root.rglob("metadata.yaml")):
        cd_dir = meta.parent
        # Skip templates directory
        if "templates" in cd_dir.parts:
            continue
        # A cooldown dir should also contain at least one wiring file
        if (cd_dir / "control.yaml").exists():
            dirs.append(cd_dir)
    return dirs


def run_command(cmd: list[str], label: str) -> bool:
    """Run a CLI command and return True on success."""
    print(f"\n{'─' * 60}")
    print(f"  {label}")
    print(f"  $ {' '.join(cmd)}")
    print(f"{'─' * 60}")
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode == 0


def set_output(name: str, value: str) -> None:
    """Write a value to $GITHUB_OUTPUT."""
    output_file = os.environ.get("GITHUB_OUTPUT")
    if output_file:
        with open(output_file, "a") as f:
            if "\n" in value:
                # Multi-line output using heredoc delimiter
                f.write(f"{name}<<EOF\n{value}\nEOF\n")
            else:
                f.write(f"{name}={value}\n")


def main() -> int:
    command = os.environ.get("INPUT_COMMAND", "all").strip()
    raw_dirs = os.environ.get("INPUT_COOLDOWN_DIRS", "").strip()
    diagram_output = os.environ.get("INPUT_DIAGRAM_OUTPUT", "wiring.svg").strip()

    # Discover or parse cooldown directories
    if raw_dirs:
        cooldown_dirs = [Path(d) for d in raw_dirs.split()]
    else:
        cooldown_dirs = discover_cooldown_dirs(Path("."))

    if not cooldown_dirs:
        print("No cooldown directories found.")
        set_output("cooldown-dirs", "")
        set_output("passed", "true")
        return 0

    print(f"Found {len(cooldown_dirs)} cooldown director{'y' if len(cooldown_dirs) == 1 else 'ies'}:")
    for d in cooldown_dirs:
        print(f"  - {d}")

    set_output("cooldown-dirs", "\n".join(str(d) for d in cooldown_dirs))

    commands = [command] if command != "all" else ["validate", "build"]
    all_passed = True

    for cd_dir in cooldown_dirs:
        for cmd_name in commands:
            if cmd_name == "validate":
                ok = run_command(
                    ["cryowire", "validate", str(cd_dir)],
                    f"Validate {cd_dir}",
                )
            elif cmd_name == "build":
                ok = run_command(
                    ["cryowire", "build", str(cd_dir)],
                    f"Build {cd_dir}",
                )
            elif cmd_name == "diagram":
                ok = run_command(
                    ["cryowire", "diagram", str(cd_dir), "-o", diagram_output],
                    f"Diagram {cd_dir}",
                )
            else:
                print(f"Unknown command: {cmd_name}")
                ok = False

            if not ok:
                all_passed = False

    # Summary
    print(f"\n{'═' * 60}")
    if all_passed:
        print("  All checks passed.")
    else:
        print("  Some checks failed.")
    print(f"{'═' * 60}")

    set_output("passed", "true" if all_passed else "false")
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
