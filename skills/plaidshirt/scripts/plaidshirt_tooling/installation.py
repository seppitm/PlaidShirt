"""Install project instructions and portable skill files without global changes."""

import hashlib
import json
from pathlib import Path

from .project import inspect_project, project_path


START = "<!-- plaidshirt:start -->"
"""Start of the instruction section managed by the installer."""
END = "<!-- plaidshirt:end -->"
"""End of the instruction section managed by the installer."""
MANIFEST = ".plaidshirt-install.json"
"""Manifest containing hashes of the last installed skill files."""


def digest(content: bytes) -> str:
    """Return the SHA-256 digest of file contents."""
    return hashlib.sha256(content).hexdigest()


def managed_rules(existing: bytes, block: str) -> bytes:
    """Update one managed section while preserving all other text.

    Args:
        existing: Previous UTF-8 contents, possibly including a BOM.
        block: Complete replacement PlaidShirt section.

    Returns:
        Contents preserving other instructions and their line-ending style.

    Raises:
        ValueError: If management markers are duplicated or incomplete.
    """
    text = existing.decode("utf-8")
    newline = "\r\n" if "\r\n" in text else "\n"
    replacement = block.replace("\n", newline)
    if text.count(START) != text.count(END) or text.count(START) > 1:
        raise ValueError("Invalid PlaidShirt markers in existing project instructions.")
    if START not in text:
        separator = "" if not text else newline * (1 if text.endswith(newline) else 2)
        return (text + separator + replacement + newline).encode("utf-8")
    start = text.index(START)
    end_start = text.index(END)
    if end_start < start:
        raise ValueError("PlaidShirt markers are out of order.")
    end = end_start + len(END)
    return (text[:start] + replacement + text[end:]).encode("utf-8")


def instruction_block(skill_path: str, host: str) -> str:
    """Generate concrete project-wide instructions for an agent host.

    Args:
        skill_path: Relative path to the installed SKILL.md.
        host: Target host: codex, claude, or generic.

    Returns:
        A managed instruction block granting no additional execution permissions.
    """
    reference = f"@{skill_path}" if host == "claude" else f"`{skill_path}`"
    return (
        f"{START}\n"
        "## PlaidShirt: required project standard\n\n"
        "Apply PlaidShirt to all coding, refactoring, review, and\n"
        "documentation tasks throughout this project and its subdirectories\n"
        "without requiring another invocation. Before starting, read:\n\n"
        f"{reference}\n\n"
        "Load only the references relevant to the task. Preserve\n"
        "readability, encapsulation, complete native doc comments, and\n"
        "relevant diagrams. Run configured tests and documentation builds.\n"
        "Respect explicit user requests and additional project instructions;\n"
        "identify actual conflicts. When delegation is requested, pass along\n"
        "these instructions and the skill path. This rule does not authorize\n"
        "additional actions or request delegation.\n"
        f"{END}"
    )


def skill_payload(source: Path) -> dict[str, bytes]:
    """Read installable skill files, excluding temporary Python files.

    Args:
        source: Source directory containing the complete skill.

    Returns:
        Relative file paths and their contents.
    """
    payload = {}
    for path in source.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"Skill symlinks are not copied: {path}")
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        if path.suffix in {".pyc", ".pyo"} or path.name == MANIFEST:
            continue
        payload[path.relative_to(source).as_posix()] = path.read_bytes()
    if "SKILL.md" not in payload:
        raise ValueError("The skill source contains no SKILL.md.")
    return payload


def install_project(source: Path, root: Path, hosts: list[str]) -> dict:
    """Install selected host copies and persistent project instructions.

    Args:
        source: Directory of the skill to install.
        root: Existing target project.
        hosts: Selected hosts: codex, claude, or generic.

    Returns:
        Changed files and installed hosts.

    Raises:
        ValueError: For path conflicts or local edits at the destination.
    """
    payload = skill_payload(source)
    changes = {}
    for host in dict.fromkeys(hosts):
        if host not in {"codex", "claude", "generic"}:
            raise ValueError(f"Unknown host: {host}")
        directory = ".claude" if host == "claude" else ".agents"
        target = project_path(root, f"{directory}/skills/plaidshirt")
        manifest_path = target / MANIFEST
        previous = {}
        if manifest_path.is_file():
            previous = json.loads(manifest_path.read_text(encoding="utf-8"))["files"]
        for relative, content in payload.items():
            destination = project_path(root, str(target / relative))
            if destination.exists():
                current = destination.read_bytes()
                if current != content and previous.get(relative) != digest(current):
                    raise ValueError(f"Local destination edit preserved: {destination}")
            changes[destination] = content
        manifest = {"version": 1, "files": {
            relative: digest(content) for relative, content in payload.items()}}
        changes[manifest_path] = (json.dumps(manifest, indent=2) + "\n").encode()
        rules_name = "CLAUDE.md" if host == "claude" else "AGENTS.md"
        rules_path = project_path(root, rules_name)
        existing = changes.get(rules_path, rules_path.read_bytes()
                               if rules_path.exists() else b"")
        skill_path = f"{directory}/skills/plaidshirt/SKILL.md"
        changes[rules_path] = managed_rules(
            existing, instruction_block(skill_path, host))

    # Complete conflict checking before changing any files.
    written = []
    for destination, content in changes.items():
        if destination.is_file() and destination.read_bytes() == content:
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)
        written.append(destination.relative_to(root).as_posix())
    return {"hosts": sorted(set(hosts)), "changed_files": written}


def installation_status(root: Path) -> dict:
    """Inspect saved project integration and additional local instructions.

    Args:
        root: Project directory.

    Returns:
        Saved host copies and rules, not proof of the model's actual context.
    """
    hosts = {}
    for host, directory, rules_name in (
        ("codex", ".agents", "AGENTS.md"),
        ("claude", ".claude", "CLAUDE.md"),
    ):
        rules = root / rules_name
        content = rules.read_text(encoding="utf-8-sig") if rules.is_file() else ""
        standard_path = f"{directory}/skills/plaidshirt/SKILL.md"
        source_path = "skills/plaidshirt/SKILL.md"
        in_place = source_path in content and (root / source_path).is_file()
        hosts[host] = {
            "skill_present": (root / standard_path).is_file() or in_place,
            "source_in_place": in_place,
            "project_rule_present": START in content and END in content,
        }
    nested = [path for path in inspect_project(root)["instruction_files"]
              if "/" in path or path == "AGENTS.override.md"]
    return {"hosts": hosts, "additional_instruction_files": nested,
            "note": "Saved instructions checked; verify loaded context in the host."}
