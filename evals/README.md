# Evaluating agent behavior

The functional tests in `tests/` verify the tools. They do not establish that
an agent produces better solutions with PlaidShirt. The scenarios in
`cases.json` address that separate question.

Run each scenario in its own temporary project with identical starting files.
Compare the same host and model without PlaidShirt and with installed project
instructions. Keep other skills, project rules, and permitted tools identical.
Repeat the scenarios and record the model, host version, date, prompts,
changes, and verification results.

First check functional outcomes, actual documentation generation, and model
semantics. Then evaluate anonymized solutions using the same criteria:

| Criterion | Evidence |
| --- | --- |
| Correctness | Behavior, boundaries, failures, and existing contracts |
| Readability | A colleague can accurately explain flow and responsibilities |
| Maintainability | A small follow-up requirement can be implemented locally and safely |
| Documentation | Accurate contracts and relevant generated output |
| Models | Supported relationships, suitable notation, and consistency with code |
| Performance | Relevant requirements and comparable measurements where needed |
| Scope | Complete delivery without unrelated changes |

Report regressions and failures as well as improvements. Token costs and line
counts are supplementary measurements; the desired quality attributes remain
the primary criteria. A favorable sample is not a universal guarantee.

**Status:** scenarios prepared; comparative model runs have not been performed.
