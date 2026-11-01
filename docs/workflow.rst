Workflow and project integration
====================================

Project-wide standard
-------------------------

The installer copies the complete skill into the appropriate project
locations and adds persistent rules to AGENTS.md and CLAUDE.md.
It preserves existing instructions outside its managed section and refuses
to overwrite local edits to installed skill files.

.. code-block:: text

   python skills/plaidshirt/scripts/plaidshirt.py install --project TARGET --host codex --host claude
   python skills/plaidshirt/scripts/plaidshirt.py status --project TARGET

The standard applies to relevant work throughout the target project.
Commands started in a subdirectory can find its project root.
Host instruction ordering, more specific rules, and context limits still
apply. The status report checks files rather than the model's actual context.

From requirements to handoff
-------------------------------

1. Establish requirements, domain terms, and observable acceptance cases.
2. Model responsibilities, data, and important behavior where useful.
3. Develop readable code and native documentation comments together.
4. Verify behavior, failures, formatting, and relevant runtime properties.
5. Generate affected diagrams and API documentation locally, then inspect them.
6. Explain the result, checks, limits, and consequential decisions.

Executable checks
---------------------

The project file ``.plaidshirt.json`` defines documentation and diagram
commands as argument lists. Without ``--run``, commands only show their
plan. With it, reviewed jobs run without a shell. Missing tools are not installed.

.. code-block:: text

   python skills/plaidshirt/scripts/plaidshirt.py discover
   python skills/plaidshirt/scripts/plaidshirt.py overview
   python skills/plaidshirt/scripts/plaidshirt.py docs
   python skills/plaidshirt/scripts/plaidshirt.py docs --run
   python skills/plaidshirt/scripts/plaidshirt.py diagrams --run
   python skills/plaidshirt/scripts/plaidshirt.py debt

Documentation builds run configured diagram jobs first. Missing, empty,
stale, malformed, or unexpected artifacts fail the check. A genuinely
incremental generator can explicitly enable ``allow_unchanged_artifacts``;
its output freshness then needs separate verification. A passing check
does not replace inspecting contracts and rendered content.

Building this repository
---------------------------

Use a development environment with Sphinx and the example renderers.
For example, on Windows:

.. code-block:: text

   python -m venv .venv
   .venv\Scripts\python -m pip install -r requirements-dev.txt
   npm ci --ignore-scripts
   .venv\Scripts\python skills/plaidshirt/scripts/plaidshirt.py docs --run

Provide the example PlantUML renderer at ``.tools/plantuml.jar`` and a
working Java executable on the process path. The flowchart uses a JavaScript
Graphviz library; JSDoc builds its API documentation. Dependencies are not
bundled with the skill. Target projects configure their own native tools,
such as Javadoc, TypeDoc, phpDocumentor, or compiler XML followed by DocFX.
