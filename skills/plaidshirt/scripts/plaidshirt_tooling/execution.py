"""Plan and explicitly run project checks without a shell."""

import json
import os
from pathlib import Path
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

from .project import project_path


def load_tasks(root: Path, category: str) -> list[dict]:
    """Read and validate project documentation or diagram jobs.

    Args:
        root: Project directory.
        category: Either documentation or diagrams.

    Returns:
        Validated jobs with argument lists and verifiable artifacts.

    Raises:
        ValueError: If configuration is missing or invalid.
    """
    config_path = root / ".plaidshirt.json"
    if not config_path.is_file():
        raise ValueError(".plaidshirt.json is missing. Run discover and configure the documentation build.")
    config = json.loads(config_path.read_text(encoding="utf-8-sig"))
    if config.get("version") != 1:
        raise ValueError("Configuration requires version: 1.")
    tasks = config.get(category, [])
    if not isinstance(tasks, list) or not tasks:
        raise ValueError(f"No jobs configured under {category}.")
    for task in tasks:
        if not isinstance(task, dict):
            raise ValueError("Each job must be an object.")
        command = task.get("command")
        if (not isinstance(command, list) or not command
                or not all(isinstance(part, str) and part for part in command)):
            raise ValueError("command must be a non-empty argument list.")
        if not isinstance(task.get("name"), str) or not task["name"]:
            raise ValueError("Each job requires a name.")
        project_path(root, task.get("cwd", "."))
        artifacts = task.get("artifacts")
        if not isinstance(artifacts, list) or not artifacts:
            raise ValueError("Each job requires verifiable artifacts.")
        for artifact in artifacts:
            if not isinstance(artifact, dict) or not isinstance(artifact.get("path"), str):
                raise ValueError("Each artifact requires a file path.")
            project_path(root, artifact["path"])
            contains = artifact.get("contains", [])
            if not isinstance(contains, list) or not all(isinstance(item, str) for item in contains):
                raise ValueError("contains must be a list of strings.")
        timeout = task.get("timeout", 120)
        if not isinstance(timeout, int) or not 1 <= timeout <= 3600:
            raise ValueError("timeout must be between 1 and 3600 seconds.")
        if not isinstance(task.get("allow_unchanged_artifacts", False), bool):
            raise ValueError("allow_unchanged_artifacts must be a boolean.")
    return tasks


def artifact_state(root: Path, artifact: dict, before: int | None) -> dict:
    """Check the existence, contents, and freshness of an expected output.

    Args:
        root: Project directory.
        artifact: Relative path and any required text contents.
        before: Previous modification time, or None for a new file.

    Returns:
        An artifact status without a claim of semantic completeness.
    """
    path = project_path(root, artifact["path"])
    result = {"path": artifact["path"], "status": "missing"}
    if not path.is_file() or path.stat().st_size == 0:
        return result
    content = path.read_text(encoding="utf-8", errors="replace")
    if any(text not in content for text in artifact.get("contains", [])):
        return {**result, "status": "expected-content-missing"}
    if path.suffix == ".xml":
        try:
            ET.fromstring(content)
        except ET.ParseError:
            return {**result, "status": "invalid-xml"}
    if path.suffix == ".svg":
        try:
            element = ET.fromstring(content)
            if element.tag.rsplit("}", 1)[-1] != "svg":
                return {**result, "status": "invalid-svg"}
        except ET.ParseError:
            return {**result, "status": "invalid-svg"}
        error_markers = ("syntax error", "this feature has been suppressed")
        if any(marker in content.lower() for marker in error_markers):
            return {**result, "status": "renderer-error"}
    updated = before is None or path.stat().st_mtime_ns != before
    return {**result, "status": "updated" if updated else "unchanged"}


def run_tasks(root: Path, category: str, execute: bool) -> dict:
    """Show configured commands or run them with artifact checks.

    Args:
        root: Project directory.
        category: Either documentation or diagrams.
        execute: Only True starts programs configured by the project.

    Returns:
        Per-job results and an overall success status.
    """
    tasks = load_tasks(root, category)
    results = []
    for task in tasks:
        command = [part.replace("{python}", sys.executable)
                   .replace("{project}", str(root)) for part in task["command"]]
        cwd = project_path(root, task.get("cwd", "."))
        item = {"name": task["name"], "command": command, "cwd": str(cwd)}
        if not execute:
            results.append({**item, "status": "planned"})
            continue
        timestamps = {}
        for artifact in task["artifacts"]:
            path = project_path(root, artifact["path"])
            timestamps[artifact["path"]] = path.stat().st_mtime_ns if path.is_file() else None
        started = time.monotonic()
        try:
            process = subprocess.run(
                command, cwd=cwd, capture_output=True, text=True,
                encoding="utf-8", errors="replace", timeout=task.get("timeout", 120),
                shell=False, env={**os.environ, "PYTHONUTF8": "1"},
            )
            artifacts = [artifact_state(root, artifact, timestamps[artifact["path"]])
                         for artifact in task["artifacts"]]
            allowed_states = {"updated"}
            if task.get("allow_unchanged_artifacts", False):
                allowed_states.add("unchanged")
            success = process.returncode == 0 and all(
                artifact["status"] in allowed_states for artifact in artifacts)
            results.append({
                **item, "status": "passed" if success else "failed",
                "exit_code": process.returncode, "artifacts": artifacts,
                "stdout": process.stdout, "stderr": process.stderr,
                "duration_seconds": round(time.monotonic() - started, 3),
            })
        except (OSError, subprocess.TimeoutExpired) as error:
            results.append({**item, "status": "failed", "error": str(error)})
    success = all(item["status"] in {"passed", "planned"} for item in results)
    return {"category": category, "executed": execute, "success": success,
            "tasks": results,
            "note": "Also inspect semantic completeness and rendered content."}


def run_documentation(root: Path, execute: bool) -> dict:
    """Build configured diagrams before their associated documentation.

    Args:
        root: Project directory containing .plaidshirt.json.
        execute: True runs configured programs; False shows their plan.

    Returns:
        The documentation report with an optional diagram prerequisite report.
    """
    load_tasks(root, "documentation")
    config_path = root / ".plaidshirt.json"
    prerequisites = None
    if config_path.is_file():
        config = json.loads(config_path.read_text(encoding="utf-8-sig"))
        if config.get("diagrams"):
            prerequisites = run_tasks(root, "diagrams", execute)
            if not prerequisites["success"]:
                return {"success": False, "executed": execute,
                        "diagrams": prerequisites, "documentation": "not-started"}
    result = run_tasks(root, "documentation", execute)
    if prerequisites is not None:
        result["diagrams"] = prerequisites
    return result
