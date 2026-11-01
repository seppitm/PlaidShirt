Implementation status
=========================

Implemented
---------------

* Persistent project rules and repeatable installation for Codex, Claude Code,
  and hosts that read AGENTS.md.
* Dedicated review, audit, diagram-selection, and debt-inventory workflows.
* Local project inventory, documentation discovery, and configurable
  documentation/diagram builds with artifact checks and a plan-only mode.
* Debt-marker collection with locations and optional revisit triggers.
* Sphinx and JSDoc developer documentation with editable diagram sources.
* Functional tooling tests and realistic agent-evaluation scenarios.

Pending verification and optional features
---------------------------------------------

* Run the prepared scenarios with actual coding agents and evaluate
  anonymized outcomes against the same criteria.
* Verify native sessions started in subdirectories actually load PlaidShirt.
  File checks alone do not establish this.
* Integrate additional native language generators in real target projects.
* Select marketplace packaging, optional lifecycle hooks, and a status
  interface based on practical use.
* Add cost/token views and a task board if they prove useful.

The quality standard stays the same across workflows. Review, documentation,
and modeling are task types; a mode with reduced documentation requirements
is not planned.
