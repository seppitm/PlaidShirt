# Reviews and audits

## Establish scope

A **review** examines a named change: files, a working tree, commit, branch,
or pull request. Without a target, inspect local changes and state the scope.
An **audit** examines a named module or repository. Both initially produce
a report. A review-only request does not authorize code changes or installing
additional tools.

## Build findings from evidence

1. Read requirements, affected code, callers, tests, data models, and related
   documentation. Trace important inputs and outputs across real boundaries.
   For audits, map entry points and important data flows first, then state
   which areas were not examined.
2. Check domain errors, data loss, validation, error handling, resource use,
   and contracts first. Judge load and performance against actual requirements
   rather than hypothetical scale.
3. Check meaningful tests, clear responsibilities, encapsulation, duplicated
   business rules, and justified patterns. Use configured formatting and
   static-analysis tools where available.
4. Compare doc comments with signatures and actual behavior: parameters,
   results, failures, side effects, and private helpers. Run configured
   documentation checks and inspect generated content.
5. Compare relevant diagrams with code, calls, and schemas. Stale models and
   unsupported cardinalities are distinct documentation findings.
6. Confirm each finding with a concrete case. Separate demonstrated problems,
   open verification work, and optional design suggestions.

## Report

Start with scope and an overall assessment. Give each finding a priority,
location, trigger, consequence, and actionable correction. Prioritize
functional and security problems, followed by maintainability and
documentation. A style preference is not an invented bug.

State which checks ran and their limits. An audit is not a guarantee that
every defect or vulnerability has been found.

## Technical debt

Mark an actual accepted compromise with a short implementation comment such
as `DEBT: limitation | trigger for revisiting`. Existing `TODO`, `FIXME`,
and `shortcut:` conventions remain usable. A collected report is an inventory,
not an automatic evaluation or proof that unmarked code is debt-free.
