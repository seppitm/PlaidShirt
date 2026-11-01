"""Use PlaidShirt's local project, installation, and documentation tools."""

import argparse
import json
from pathlib import Path
import sys

from plaidshirt_tooling.execution import run_documentation, run_tasks
from plaidshirt_tooling.installation import install_project, installation_status
from plaidshirt_tooling.project import (
    collect_debt, documentation_hints, inspect_project,
)


def find_project(explicit: str | None) -> Path:
    """Locate the target project, including calls from a subdirectory.

    Args:
        explicit: Explicit project path, or None to search parent directories.

    Returns:
        The resolved existing project directory.

    Raises:
        ValueError: If an explicit project directory does not exist.
    """
    current = Path(explicit).resolve() if explicit else Path.cwd().resolve()
    if not current.is_dir():
        raise ValueError(f"Project directory does not exist: {current}")
    if explicit:
        return current
    candidates = (current, *current.parents)
    for candidate in candidates:
        if any((candidate / marker).exists() for marker in (
            ".plaidshirt.json", ".git", ".agents/skills/plaidshirt/SKILL.md",
            ".claude/skills/plaidshirt/SKILL.md")):
            return candidate
    for candidate in candidates:
        if any((candidate / marker).exists() for marker in ("AGENTS.md", "CLAUDE.md")):
            return candidate
    return current


def argument_parser() -> argparse.ArgumentParser:
    """Describe supported project commands and their arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="action", required=True)
    descriptions = {
        "install": "Install the skill and persistent project instructions",
        "status": "Check saved project integration",
        "overview": "Inventory files, languages, and existing diagrams",
        "discover": "Suggest documentation commands from existing entry points",
        "docs": "Plan or run configured documentation builds",
        "diagrams": "Plan or run configured diagram builds",
        "debt": "Collect technical-debt comment markers",
    }
    for name, description in descriptions.items():
        command = commands.add_parser(name, help=description)
        command.add_argument("--project", help="Project path; otherwise search parent directories")
        if name == "install":
            command.add_argument("--host", action="append", required=True,
                                 choices=["codex", "claude", "generic"])
        if name in {"docs", "diagrams"}:
            command.add_argument("--run", action="store_true",
                                 help="Execute the displayed project commands")
    return parser


def main(arguments: list[str] | None = None) -> int:
    """Run a command and print a machine-readable result.

    Args:
        arguments: Optional argument list for embedded calls and tests.

    Returns:
        0 on success, 1 for failed checks, or 2 for an invalid invocation.
    """
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    options = argument_parser().parse_args(arguments)
    try:
        root = find_project(options.project)
        if options.action == "install":
            result = install_project(Path(__file__).resolve().parents[1], root, options.host)
        elif options.action == "status":
            result = installation_status(root)
        elif options.action == "overview":
            result = inspect_project(root)
        elif options.action == "discover":
            result = {"suggestions": documentation_hints(root),
                      "note": "Review suggestions and configure them in .plaidshirt.json."}
        elif options.action == "debt":
            result = {"findings": collect_debt(root),
                      "note": "Recognizable comment markers, not a complete debt analysis."}
        elif options.action == "docs":
            result = run_documentation(root, options.run)
        else:
            result = run_tasks(root, "diagrams", options.run)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("success", True) else 1
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
