# Apply PlaidShirt throughout a project

A skill is initially selectable guidance. To make it a project standard,
also install persistent project instructions. Configuration outside the target
project is not changed.

## Install

When given this repository, identify the current agent host and use the
installer from the checkout. For Codex use `--host codex`, for Claude Code
use `--host claude`, or use `--host generic` for a host reading `AGENTS.md`.
Several `--host` options can be combined when appropriate.

```text
python skills/plaidshirt/scripts/plaidshirt.py install --project /path/project --host codex --host claude
```

The installer copies the skill, references, and scripts into
`.agents/skills/plaidshirt` and/or `.claude/skills/plaidshirt`. It adds a
managed section to `AGENTS.md` and `CLAUDE.md`. Existing instructions outside
that section remain intact. Local edits to installed skill files are not
overwritten.

`AGENTS.md` requires the standard for relevant work throughout the project
and subdirectories. `CLAUDE.md` additionally imports the installed `SKILL.md`
using Claude's `@` syntax. Start a new session if needed after installation.
The user does not need to invoke the skill for each coding task.
Unrelated conversation does not initiate project work.

## Verify

```text
python /path/plaidshirt/scripts/plaidshirt.py status --project /path/project
```

Status checks saved instructions and skill files and lists additional
instruction files. It does not prove what a running agent has loaded.
Verify separately in a session started from a subdirectory: the agent
should be able to identify its active project rules and the PlaidShirt source.

Codex reads instructions along the project hierarchy. More specific rules
and `AGENTS.override.md` can supersede earlier guidance; host configuration
and context limits also matter.
[Official OpenAI documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

Claude can load hierarchical `CLAUDE.md` files and imports. Project rules
are instructions rather than a guarantee of every model decision. Inspect
the host's context view to confirm loading.
[Official Claude documentation](https://code.claude.com/docs/en/memory).

For other hosts, including those using DeepSeek, `--host generic` installs
`AGENTS.md` and the shared skill path. Automatic application requires the
host to load those instructions. When delegation is requested, pass along
the project rules and skill path; this requirement does not request delegation.
