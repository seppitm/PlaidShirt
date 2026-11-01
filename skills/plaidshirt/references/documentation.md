# Documentation contract

Deliver source code from which an appropriate tool can generate useful
documentation. This is part of affected implementation work even when the
user does not repeat the documentation requirement.

## Content and coverage

Document all new or behaviorally changed handwritten types, constructors,
functions, and methods, including private helpers. Document affected modules,
fields, properties, and constants through the language's supported mechanism.
Keep the entire affected contract accurate. Third-party code, generated files,
and untouched parts of the project do not automatically enter the task scope.

For each element, cover the applicable parts of its contract:

- A useful first sentence describing its purpose and domain behavior.
- Every parameter's meaning, units, valid range, and relevant rules for null,
  empty values, defaults, and optional arguments.
- The result's meaning, including absent results, ordering, or ownership
  where these matter.
- Actual failure conditions, exceptions, and behavior on failure.
- Relevant side effects, resource handling, mutation, concurrency, or
  asynchronous behavior.
- A short valid example and resolvable references for complex usage.

Use appropriate tags and sections. Do not invent constructor return values
or exceptions without a corresponding failure path. A trivial helper needs
a short but complete description of its real inputs and results; empty
boilerplate is not documentation. Preserve technical tag and section names.

Place contracts at the language's designated documentation location.
Implementation comments explain how or why a particular approach was chosen;
repeating the next statement does not replace a contract. Use supported
documentation inheritance where a contract is genuinely inherited, adding
any differences rather than duplicating long descriptions.

## Choose a language format and generator

Inspect project configuration, existing comments, generator version, and
documentation commands first. Preserve a compatible established format.
Otherwise use the appropriate language guide. Doxygen supports several
languages, but support and configuration must fit the actual project;
do not assume universal coverage.

For another language, consult official language or generator documentation
for syntax, tags, element association, visibility, and build commands.
Do not invent Javadoc-like tags. The included sources support detail checks;
routine work does not require fetching every source again.

## Verify generated output

Use `scripts/plaidshirt.py discover` to identify possible entry points.
Record reviewed commands and concrete artifacts in `.plaidshirt.json`,
then run `docs --run` through the loaded skill. This also builds configured
diagrams. A discovery suggestion is not a verified build configuration.

1. Use installed local tools and the project's command. Examples assume the
   required tools are available; checks do not silently install packages.
2. Verify that input paths, exports, and visibility filters include the
   desired elements. Documenting private helpers in source and publishing
   an API view are separate decisions. Include private elements when a
   complete internal developer view is requested.
3. Inspect missing-comment warnings, malformed tags, and broken references.
   Check at least one affected generated page and one complex contract
   where available. Ensure the result is not an empty documentation site.
4. Update examples after relevant signature changes and record a reproducible
   build command when establishing a documentation pipeline.
5. State whether verification covered syntax and contracts, the generator,
   and the generated content. Missing tools remain an open check; do not
   promise successful generation without evidence.
