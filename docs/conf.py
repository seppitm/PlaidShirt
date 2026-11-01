"""Build the developer documentation from the tooling's Python docstrings."""

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
"""Repository root used to locate importable tooling modules."""
sys.path.insert(0, str(PROJECT_ROOT / "skills/plaidshirt/scripts"))

project = "PlaidShirt"
"""Title displayed in generated documentation."""
language = "en"
"""Language of generated navigation and interface text."""
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]
"""Read native docstrings, including Google-style sections."""
html_theme = "alabaster"
"""Bundled theme suitable for local documentation."""
exclude_patterns = ["_build"]
"""Output directories that should not be treated as input."""
autodoc_member_order = "bysource"
"""Present API members in their source-file order."""
