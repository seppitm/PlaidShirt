# Project overviews and diagrams

A diagram answers a stated question. Use the necessary level of detail and
keep it consistent with the code or data model. Explicitly distinguish the
implemented system, a proposed design, and an illustrative example.

| Question | Suitable view | Content |
| --- | --- | --- |
| Who uses the system, and for what? | Use-case diagram | Actors, system boundary, use cases |
| Which domain types collaborate? | UML class diagram | Responsibilities, important members, visibility, supported relationships and multiplicities |
| How does a business process flow? | UML activity diagram | Actions, decisions, guards, parallelism, and relevant responsibilities |
| How does an algorithm work? | Algorithm flowchart (PAP) | Start/end, processing, input/output, decisions, loops |
| What data is stored? | ER diagram | Entities, keys, foreign keys, optionality, cardinalities |
| Who calls whom, and in what order? | UML sequence diagram | Participants, calls, responses, important alternatives |
| How do valid states change? | UML state diagram | States, events, transitions, guards |
| How is a larger system organized? | Component/package diagram | Module boundaries, interfaces, dependencies |
| Where do components run? | Deployment diagram | Processes, runtime nodes, connections, external systems |

ER diagrams and algorithm flowcharts are distinct notations. A Mermaid
`flowchart` is not automatically a UML activity diagram. Do not claim
DIN 66001 compliance without checking the applicable notation requirements.

## Select and maintain views

- Read existing architecture documentation, types, calls, and schemas first.
  File names alone do not establish relationships.
- Update affected models after structural changes. For a substantial new
  project, provide a small overview and views of its essential questions.
- Derive class relationships from real contracts. A reference alone does
  not establish composition or an exact multiplicity.
- Derive ER relationships from schemas, migrations, or a confirmed domain
  model. Do not invent storage for a project without persistence.
- Use activity diagrams for processes, flowcharts for algorithms, and
  sequence diagrams for collaboration. Do not generate every view routinely.
- Accompany each model with its purpose, scope, authoritative source files,
  and any important omissions.

## Editable sources and local rendering

Prefer existing project tools. Without a project preference, PlantUML can
cover UML/ER views and Mermaid can cover readable flowcharts and embedded
views. These are examples, not mandatory tools. Suitable libraries, editors,
and renderers are welcome regardless of the project's implementation language.

Choose accurate notation, readable sources, reproducible output, and
consistency with the system. Keep editable `.puml`, `.mmd`, `.dot`, or
other model sources alongside generated SVGs. Rendering does not verify
the model's meaning.

Official syntax:
[PlantUML classes](https://plantuml.com/class-diagram),
[activities](https://plantuml.com/activity-diagram-beta),
[ER/Information Engineering](https://plantuml.com/ie-diagram),
[Mermaid ER](https://mermaid.js.org/syntax/entityRelationshipDiagram.html),
[Mermaid flowcharts](https://mermaid.js.org/syntax/flowchart.html).

Example local commands with installed tools:
`java -jar plantuml.jar -tsvg model.puml` and
`mmdc -i flow.mmd -o flow.svg`. Check options against the installed version.
Configure repeatable jobs under `diagrams` in `.plaidshirt.json`; the helper
checks their expected artifacts. Use public rendering services for project
content only with appropriate authorization. Missing renderers are reported,
not installed automatically.

[PlantUML CLI](https://plantuml.com/command-line) ·
[Mermaid CLI](https://github.com/mermaid-js/mermaid-cli)

The optional `scripts/render_dot.mjs` helper renders DOT to SVG with the
locally installed `@viz-js/viz` library. It requires Node.js rather than a
Java runtime. [Official Viz.js API](https://viz-js.com/api/).
