# PlaidShirt

**The German engineer in a flannel shirt.**

The variable has a name. The method has a contract. The coffee has gone cold.

You know the engineer. Flannel shirt. Proper vocational training. A deeply
personal objection to variables called `x`, `y`, or `z`.
He knows how to write a one-liner but he writes readable code and documents it
instead.

PlaidShirt brings that attitude to your coding agent.

## Readable code. Documented decisions.

PlaidShirt prefers clear responsibilities, readable control flow, meaningful
names, and documentation you can actually build.

He respects **KISS, DRY, YAGNI, and SOLID**.

PlaidShirt applies the style of the
[Java Code Conventions of September 12, 1997](https://www.oracle.com/technetwork/java/codeconventions-150003.pdf)
across all languages: consistent indentation, descriptive names, clear blocks,
readable line wrapping, and logically organized code. The same standard applies
to Java, Python, JavaScript, PHP, C#, and other languages, adapted to their syntax.
Affected code is documented, including private helpers, using each language's
documentation format and generator.

## What he brings to the project

| You ask for | PlaidShirt brings |
| --- | --- |
| A feature | Readable code, clear contracts, and appropriate checks |
| A refactor | Better structure with preserved behavior |
| Documentation | Native doc comments, including private helpers, and the right generator |
| A project overview | Useful UML, ER, sequence, activity, or flowchart views |
| A review | Concrete findings, locations, consequences, and fixes |
| A shortcut | A stated limit and a reason to revisit it |

JavaScript gets JSDoc. TypeScript gets suitable TSDoc/TypeDoc comments.
PHP gets PHPDoc. C# gets XML documentation. Python gets real docstrings.
C/C++, Rust, and Go have their own references too.

## Install

Give this repository to your LLM or coding agent and ask:

```text
Install PlaidShirt in this project. Follow its installation guide and use
the installer for this agent. Enable it through the project instructions
so it applies to all coding tasks and subdirectories without another
invocation. Preserve existing project rules and local edits.
```

The [installation guide](skills/plaidshirt/references/project-integration.md)
covers Codex, Claude Code, and other hosts that load project instructions.

## Diagrams

| Diagram | Purpose |
| --- | --- |
| Class | Types, responsibilities, and relationships |
| ER | Entities, keys, and cardinalities |
| Activity | Process steps, decisions, and parallel behavior |
| Sequence | Interactions between components |
| Flowchart | Algorithm steps and control flow |

Create or update diagrams when they clarify the affected structure or
behavior. Keep editable sources consistent with the implementation.

Use existing project tooling. PlantUML, Mermaid, Graphviz, or another
suitable renderer can be configured.

## Documentation

Use the documentation format and generator appropriate to each language.
Configure build commands and expected output files in `.plaidshirt.json`.

```sh
python skills/plaidshirt/scripts/plaidshirt.py overview
python skills/plaidshirt/scripts/plaidshirt.py discover
python skills/plaidshirt/scripts/plaidshirt.py docs
python skills/plaidshirt/scripts/plaidshirt.py docs --run
python skills/plaidshirt/scripts/plaidshirt.py diagrams --run
python skills/plaidshirt/scripts/plaidshirt.py debt
```

Without `--run`, build commands show their plan. With it, the helper runs
configured argument lists without a shell and checks their outputs.

Missing, empty, stale, malformed, or unexpected artifacts fail the configured
check. Generated content also requires inspection for accuracy and completeness.

[Documentation contract](skills/plaidshirt/references/documentation.md) ·
[Diagram guide](skills/plaidshirt/references/diagrams.md)
