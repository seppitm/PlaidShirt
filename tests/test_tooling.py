"""Verify installation, project scope, and actual execution results."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SOURCE = Path(__file__).resolve().parents[1] / "skills/plaidshirt"
"""Skill source under test."""
sys.path.insert(0, str(SOURCE / "scripts"))

from plaidshirt_tooling.execution import load_tasks, run_documentation, run_tasks
from plaidshirt_tooling.installation import (
    END, START, install_project, managed_rules,
)
from plaidshirt_tooling.project import (
    collect_debt, documentation_hints, inspect_project, project_path,
)


class ToolingTests(unittest.TestCase):
    """Verify observable behavior in isolated temporary projects."""

    def setUp(self):
        """Create a separate project for each test case."""
        temporary_root = SOURCE.parents[1] / "tmp/tests"
        temporary_root.mkdir(parents=True, exist_ok=True)
        self.directory = tempfile.TemporaryDirectory(dir=temporary_root)
        self.root = Path(self.directory.name).resolve()
        if not self.root.is_relative_to(temporary_root.resolve()):
            raise ValueError("Temporary test project is outside the test area.")
        self.addCleanup(self.directory.cleanup)

    def write(self, name, content):
        """Write a UTF-8 fixture inside the isolated project."""
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def configure(self, command, artifacts=None, **extra):
        """Configure a single executable documentation check."""
        task = {
            "name": "Test generator", "command": command,
            "artifacts": artifacts or [{"path": "docs.html"}], **extra,
        }
        self.write(".plaidshirt.json", json.dumps({
            "version": 1, "documentation": [task],
        }))

    def test_installation_is_complete_and_idempotent(self):
        """A repeated install leaves identical files unchanged."""
        first = install_project(SOURCE, self.root, ["codex", "claude"])
        self.assertTrue(first["changed_files"])
        self.assertTrue((self.root / ".agents/skills/plaidshirt/SKILL.md").is_file())
        self.assertTrue((self.root / ".claude/skills/plaidshirt/scripts/plaidshirt.py").is_file())
        second = install_project(SOURCE, self.root, ["codex", "claude"])
        self.assertEqual([], second["changed_files"])

    def test_existing_project_rules_survive_byte_for_byte(self):
        """Preserve a BOM and CRLF instructions when adding a managed section."""
        original = b"\xef\xbb\xbf# Team\r\n\r\nExisting team rules.\r\n"
        path = self.root / "AGENTS.md"
        path.write_bytes(original)
        install_project(SOURCE, self.root, ["codex"])
        self.assertTrue(path.read_bytes().startswith(original))
        self.assertEqual(1, path.read_bytes().count(START.encode()))

    def test_user_edited_skill_is_not_overwritten(self):
        """Detect a file conflict before any planned destination changes."""
        install_project(SOURCE, self.root, ["codex"])
        target = self.root / ".agents/skills/plaidshirt/SKILL.md"
        target.write_text("Local edits", encoding="utf-8")
        previous_rules = (self.root / "AGENTS.md").read_bytes()
        with self.assertRaises(ValueError):
            install_project(SOURCE, self.root, ["claude", "codex"])
        self.assertEqual("Local edits", target.read_text(encoding="utf-8"))
        self.assertEqual(previous_rules, (self.root / "AGENTS.md").read_bytes())
        self.assertFalse((self.root / "CLAUDE.md").exists())

    def test_managed_section_preserves_text_on_both_sides(self):
        """Replace only the managed section during an update."""
        old = f"before\n{START}\nold\n{END}\nafter\n".encode()
        result = managed_rules(old, f"{START}\nnew\n{END}")
        self.assertEqual(f"before\n{START}\nnew\n{END}\nafter\n".encode(), result)

    def test_corrupt_rule_markers_are_rejected(self):
        """Reject incomplete, duplicated, or reversed markers."""
        for text in (START, f"{END}{START}", f"{START}{END}{START}{END}"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                managed_rules(text.encode(), f"{START}\nnew\n{END}")

    def test_path_outside_project_is_rejected(self):
        """Output paths cannot escape the project."""
        with self.assertRaises(ValueError):
            project_path(self.root, "../outside.txt")

    def test_overview_excludes_dependencies_and_outputs(self):
        """Inventory source files without counting dependencies or outputs."""
        self.write("src/Main.java", "class Main {}")
        self.write("node_modules/dependency/index.js", "function external() {}")
        self.write("build/generated.py", "pass")
        result = inspect_project(self.root)
        self.assertEqual({"Java": 1}, result["languages"])

    def test_debt_marker_is_not_a_string_literal(self):
        """Debt findings include their location and revisit trigger."""
        self.write("src/example.py", 'text = "TODO: literal"\n'
                   '# DEBT: At most 100 items | When the import grows\n')
        findings = collect_debt(self.root)
        self.assertEqual(1, len(findings))
        self.assertEqual(2, findings[0]["line"])
        self.assertEqual("When the import grows", findings[0]["trigger"])

    def test_discovery_reports_source_without_execution(self):
        """Record an existing package documentation command as a suggestion only."""
        self.write("frontend/package.json", '{"scripts":{"docs:build":"typedoc"}}')
        hints = documentation_hints(self.root)
        self.assertEqual("frontend/package.json", hints[0]["source"])
        self.assertEqual("frontend", hints[0]["cwd"])
        self.assertEqual(["npm", "run", "docs:build"], hints[0]["command"])

    def test_plan_does_not_execute_command(self):
        """Planning alone does not create output files."""
        self.configure(["{python}", "-c", "open('docs.html','w').write('docs')"])
        result = run_tasks(self.root, "documentation", False)
        self.assertTrue(result["success"])
        self.assertEqual("planned", result["tasks"][0]["status"])
        self.assertFalse((self.root / "docs.html").exists())

    def test_successful_generator_has_expected_output(self):
        """Success requires a newly generated artifact with the expected contents."""
        self.configure(
            ["{python}", "-c", "open('docs.html','w').write('<h1>API</h1>')"],
            [{"path": "docs.html", "contains": ["API"]}],
        )
        result = run_tasks(self.root, "documentation", True)
        self.assertTrue(result["success"])
        self.assertEqual("updated", result["tasks"][0]["artifacts"][0]["status"])

    def test_zero_exit_without_output_is_failure(self):
        """A successful process without documentation output still fails verification."""
        self.configure(["{python}", "-c", "pass"])
        self.assertFalse(run_tasks(self.root, "documentation", True)["success"])

    def test_stale_output_is_failure(self):
        """Stale output cannot make a no-op command pass."""
        self.write("docs.html", "old docs")
        self.configure(["{python}", "-c", "pass"])
        result = run_tasks(self.root, "documentation", True)
        self.assertFalse(result["success"])
        self.assertEqual("unchanged", result["tasks"][0]["artifacts"][0]["status"])

    def test_incremental_output_requires_explicit_setting(self):
        """An incremental build can explicitly allow unchanged artifacts."""
        self.write("docs.html", "existing docs")
        self.configure(["{python}", "-c", "pass"], allow_unchanged_artifacts=True)
        self.assertTrue(run_tasks(self.root, "documentation", True)["success"])

    def test_missing_symbol_is_failure(self):
        """An unrelated API page fails its required-content check."""
        self.configure(
            ["{python}", "-c", "open('docs.html','w').write('unrelated')"],
            [{"path": "docs.html", "contains": ["ExpectedMethod"]}],
        )
        self.assertFalse(run_tasks(self.root, "documentation", True)["success"])

    def test_failed_process_remains_failure_with_artifact(self):
        """An artifact does not cancel the generator's failure exit code."""
        self.configure(["{python}", "-c",
                        "open('docs.html','w').write('docs'); raise SystemExit(3)"])
        self.assertFalse(run_tasks(self.root, "documentation", True)["success"])

    def test_invalid_xml_is_failure(self):
        """Check that generated XML documentation is well formed."""
        self.configure(["{python}", "-c", "open('docs.xml','w').write('<broken>')"],
                       [{"path": "docs.xml"}])
        self.assertFalse(run_tasks(self.root, "documentation", True)["success"])

    def test_invalid_svg_is_failure(self):
        """Renaming a text file does not make it a rendered SVG."""
        self.configure(["{python}", "-c", "open('docs.svg','w').write('not SVG')"],
                       [{"path": "docs.svg"}])
        self.assertFalse(run_tasks(self.root, "documentation", True)["success"])

    def test_configuration_rejects_shell_string(self):
        """Reject a command string rather than interpreting it through a shell."""
        self.configure("echo docs > docs.html")
        with self.assertRaises(ValueError):
            load_tasks(self.root, "documentation")

    def test_svg_error_placeholder_is_failure(self):
        """Reject a renderer error placeholder even when its XML is well formed."""
        placeholder = '<svg xmlns="http://www.w3.org/2000/svg"><text>' \
                      'This feature has been suppressed</text></svg>'
        self.configure(["{python}", "-c",
                        f"open('docs.svg','w').write({placeholder!r})"],
                       [{"path": "docs.svg"}])
        result = run_tasks(self.root, "documentation", True)
        self.assertFalse(result["success"])
        self.assertEqual("renderer-error", result["tasks"][0]["artifacts"][0]["status"])

    def test_configuration_rejects_escaping_artifact(self):
        """Validate artifact paths before starting any program."""
        self.configure(["{python}", "-c", "pass"], [{"path": "../outside.html"}])
        with self.assertRaises(ValueError):
            run_tasks(self.root, "documentation", True)

    def test_diagram_failure_prevents_documentation_start(self):
        """A failed prerequisite prevents documentation from starting."""
        task = {"name": "failed diagram", "command": ["{python}", "-c", "pass"],
                "artifacts": [{"path": "missing.svg"}]}
        documentation = {"name": "docs", "command": ["{python}", "-c", "pass"],
                         "artifacts": [{"path": "docs.html"}]}
        self.write(".plaidshirt.json", json.dumps({
            "version": 1, "diagrams": [task], "documentation": [documentation],
        }))
        result = run_documentation(self.root, True)
        self.assertFalse(result["success"])
        self.assertEqual("not-started", result["documentation"])

    def test_cli_finds_project_from_nested_directory(self):
        """A subdirectory invocation uses its containing project's instructions."""
        install_project(SOURCE, self.root, ["codex", "claude"])
        nested = self.root / "src/deep/package"
        nested.mkdir(parents=True)
        self.write("src/deep/package/AGENTS.md", "Additional module rules.")
        result = subprocess.run(
            [sys.executable, str(SOURCE / "scripts/plaidshirt.py"), "status"],
            cwd=nested, capture_output=True, text=True, encoding="utf-8", check=True,
        )
        report = json.loads(result.stdout)
        self.assertTrue(report["hosts"]["codex"]["project_rule_present"])
        self.assertTrue(report["hosts"]["claude"]["skill_present"])
        self.assertIn("src/deep/package/AGENTS.md", report["additional_instruction_files"])


if __name__ == "__main__":
    unittest.main()
