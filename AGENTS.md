# Developing PlaidShirt

The reusable skill source lives in `skills/plaidshirt`. Edit that source;
the installer updates project copies. Keep the Python helpers usable with
the standard library. Sphinx and PyYAML are development dependencies.
The optional DOT renderer uses Node.js and a local Graphviz library.

Write repository documentation, source comments, generated project rules,
examples, and user-facing tool messages in English. Keep the persona as a
German engineer in a flannel shirt. Describe capabilities directly;
do not include institutional references or the project's origin story.
Apply the selected 1997 code style across languages, using valid native syntax
and documentation formats. Preserve established APIs and report concrete
conflicts with binding project tooling.

Run from the repository root:

```text
python -m unittest discover -s tests -v
npm test
python skills/plaidshirt/scripts/plaidshirt.py docs --run
```

Use the configured development environment for documentation builds.
Keep diagrams and documentation consistent with the actual implementation.
Label illustrative examples and report verification limits accurately.

<!-- plaidshirt:start -->
## PlaidShirt: required project standard

Apply PlaidShirt to all coding, refactoring, review, and documentation tasks
throughout this repository and its subdirectories without requiring another
invocation. Read `skills/plaidshirt/SKILL.md` and the relevant references
before starting work.

Readable code, encapsulation, native doc comments, appropriate models,
tests, and configured documentation builds are part of the task.
Respect explicit user requests and other applicable project instructions.
When delegation is requested, pass along this skill path and the applicable
rules. This instruction does not request delegation or authorize extra actions.
<!-- plaidshirt:end -->
