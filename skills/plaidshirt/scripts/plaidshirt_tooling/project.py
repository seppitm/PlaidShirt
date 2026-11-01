"""Inspect a project without starting its application or build."""

import json
import os
from pathlib import Path
import re
import subprocess


SKIPPED_DIRECTORIES = {
    ".git", ".venv", ".tools", "node_modules", "vendor", "build", "dist",
    "target", "__pycache__", ".agents", ".claude", ".pytest_cache",
}
"""Directories containing dependencies, installed copies, or generated files."""

LANGUAGES = {
    ".java": "Java", ".js": "JavaScript", ".jsx": "JavaScript",
    ".ts": "TypeScript", ".tsx": "TypeScript", ".php": "PHP",
    ".cs": "C#", ".py": "Python", ".c": "C", ".h": "C/C++",
    ".cpp": "C++", ".hpp": "C++", ".rs": "Rust", ".go": "Go",
}
"""File extensions used for orientation rather than a full semantic analysis."""


def project_path(root: Path, relative: str) -> Path:
    """Resolve a path within the project.

    Args:
        root: Absolute project directory.
        relative: Path that must remain inside the project.

    Returns:
        The resolved project path.

    Raises:
        ValueError: If the resolved path leaves the project.
    """
    destination = (root / relative).resolve()
    if not destination.is_relative_to(root.resolve()):
        raise ValueError(f"Path is outside the project: {relative}")
    return destination


def project_files(root: Path) -> list[Path]:
    """List project files while respecting available Git exclusions.

    Args:
        root: Project directory to inspect.

    Returns:
        Sorted files excluding dependencies, installed skill copies, and symlinks.
    """
    try:
        result = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            cwd=root, capture_output=True, timeout=15, check=True,
        )
        names = result.stdout.decode("utf-8").split("\0")
        candidates = [root / name for name in names if name]
    except (OSError, UnicodeError, subprocess.SubprocessError):
        candidates = []
    if not candidates:
        # An explicitly selected project may be ignored by its parent repository.
        for directory, children, names in os.walk(root, followlinks=False):
            children[:] = [name for name in children
                           if name not in SKIPPED_DIRECTORIES]
            candidates.extend(Path(directory) / name for name in names)

    files = []
    for path in candidates:
        relative = path.relative_to(root)
        if any(part in SKIPPED_DIRECTORIES for part in relative.parts):
            continue
        if path.is_symlink() or not path.is_file():
            continue
        if not path.resolve().is_relative_to(root.resolve()):
            continue
        files.append(path)
    return sorted(set(files))


def inspect_project(root: Path) -> dict:
    """Inventory languages, build entry points, and existing models.

    Args:
        root: Project directory.

    Returns:
        A verifiable file inventory without invented class relationships.
    """
    languages = {}
    build_files = []
    diagram_sources = []
    instructions = []
    for path in project_files(root):
        relative = path.relative_to(root).as_posix()
        language = LANGUAGES.get(path.suffix)
        if language:
            languages[language] = languages.get(language, 0) + 1
        if path.name in {
            "pom.xml", "build.gradle", "build.gradle.kts", "package.json",
            "pyproject.toml", "conf.py", "phpdoc.xml", "phpdoc.dist.xml",
            "Doxyfile", "Cargo.toml", "go.mod", ".plaidshirt.json",
        } or path.suffix == ".csproj":
            build_files.append(relative)
        if path.suffix in {".puml", ".mmd", ".dot", ".drawio"}:
            diagram_sources.append(relative)
        if path.name in {"AGENTS.md", "AGENTS.override.md", "CLAUDE.md"}:
            instructions.append(relative)
    return {
        "project": str(root), "languages": languages,
        "build_files": build_files, "diagram_sources": diagram_sources,
        "instruction_files": instructions,
        "note": "File inventory only; verify UML and ER relationships against source.",
    }


def documentation_hints(root: Path) -> list[dict]:
    """Suggest discovered documentation entry points without running commands.

    Args:
        root: Project directory.

    Returns:
        Suggestions to review, each linked to its source file.
    """
    hints = []
    for path in project_files(root):
        relative = path.relative_to(root).as_posix()
        parent = path.parent.relative_to(root).as_posix()
        command = None
        if path.name == "pom.xml":
            command = ["mvn", "javadoc:javadoc"]
        elif path.name in {"build.gradle", "build.gradle.kts"}:
            command = ["gradle", "javadoc"]
        elif path.name in {"phpdoc.xml", "phpdoc.dist.xml"}:
            command = ["phpdoc"]
        elif path.name == "Doxyfile":
            command = ["doxygen", path.name]
        elif path.name == "Cargo.toml":
            command = ["cargo", "doc", "--no-deps", "--document-private-items"]
        elif path.name == "conf.py":
            command = ["sphinx-build", "-b", "html", "-W", ".", "build/docs"]
        elif path.suffix == ".csproj":
            command = ["dotnet", "build", path.name,
                       "-p:GenerateDocumentationFile=true"]
        elif path.name == "package.json":
            try:
                package = json.loads(path.read_text(encoding="utf-8-sig"))
                scripts = package.get("scripts", {})
                script = next((key for key in ("docs:build", "build:docs", "docs")
                               if key in scripts), None)
                if script:
                    command = ["npm", "run", script]
            except (ValueError, OSError):
                continue
        if command:
            hints.append({"source": relative, "cwd": parent, "command": command,
                          "note": "Check wrappers, package managers, and output paths."})
    return hints


def collect_debt(root: Path) -> list[dict]:
    """Collect recognizable debt markers from comment lines.

    Args:
        root: Project directory.

    Returns:
        Locations, contents, and any stated trigger for revisiting.
    """
    pattern = re.compile(
        r"^\s*(?:#|//|/\*+|\*|<!--)\s*"
        r"(DEBT|TODO|FIXME|shortcut):\s*(.*)", re.IGNORECASE,
    )
    findings = []
    for path in project_files(root):
        if path.suffix not in LANGUAGES:
            continue
        try:
            content = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError):
            continue
        for number, line in enumerate(content.splitlines(), 1):
            match = pattern.match(line)
            if not match:
                continue
            text = match.group(2).removesuffix("*/").strip()
            limitation, separator, trigger = text.partition("|")
            findings.append({
                "file": path.relative_to(root).as_posix(), "line": number,
                "marker": match.group(1), "limitation": limitation.strip(),
                "trigger": trigger.strip() if separator else None,
            })
    return findings
