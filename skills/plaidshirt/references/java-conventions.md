# Shared code style: the 1997 conventions

Use the **Java Code Conventions of September 12, 1997**, originally published
by Sun Microsystems and [hosted by Oracle](https://www.oracle.com/technetwork/java/codeconventions-150003.pdf).
Apply their style as PlaidShirt's baseline across all programming languages.
This does not require an old Java runtime or permit invalid syntax, changed
language semantics, or broken project contracts.

## Apply the same style across languages

Use four-space indentation, descriptive names, clear multi-line control flow,
consistent block layout, readable wrapping, logical organization, encapsulation,
and complete documentation in every language.

Use `PascalCase` for custom types, `lowerCamelCase` for custom functions,
methods, variables, and parameters, and `UPPER_SNAKE_CASE` for constants
where language semantics allow it. This naming policy is a deliberate house
style, including in languages whose usual style guide prefers another spelling.

Use same-line opening braces in brace-based languages. In languages such as
Python, express the same structure through valid native syntax and indentation.
Use native documentation formats and generators; do not put Javadoc delimiters
or tags into a language that does not recognize them.

| Language | Translation of the shared style |
| --- | --- |
| JavaScript, TypeScript, PHP, C# | Four spaces, descriptive Java-style names, same-line opening braces, and native doc comments |
| Python | Four spaces, descriptive Java-style names, explicit control flow, native colons and docstrings |
| C and C++ | Apply the same naming and layout to custom code; preserve external ABI names and native constructs |
| Rust and Go | Apply the shared rules while preserving language-defined visibility, required names, and unavoidable formatter constraints |

Keep established public APIs, overrides, protocol methods, and external names
unless the task includes changing them. For example, Go capitalization can
determine visibility and Python special methods have prescribed names.
Describe concrete conflicts with binding project formatters or lint rules;
do not silently fall back to another style. A focused change does not authorize
a repository-wide rename or reformat.

## Formatting and organization

- Indent by four positions per block. PlaidShirt uses spaces; the original
  leaves the implementation of indentation open.
- Aim for at most 80 characters per line and about 70 in documentation
  examples. Do not damage an indivisible URL to force a wrap.
- Put an opening brace at the end of its introducing line and the closing
  brace on its own line. Keep `} else {` and `} catch (...) {` together.
- Give single-statement control branches braces. Use one statement and one
  variable declaration per line; a `for` header remains a logical unit.
- Add spaces after commas, around binary operators, and between a control
  keyword and its parenthesis. Do not separate a method name from `(`.
- Wrap after commas or before operators. Align continuations, or indent
  eight positions when alignment would make the code hard to read.
- Separate methods and logical steps with blank lines. Avoid decorative
  comment frames and commented-out alternative implementations.
- Source order: an existing appropriate header, package, imports, then types.
  Translate these sections into the language's supported module structure.
  In Java, a public top-level type matches its file name.
- Type order: static fields, instance fields, constructors, methods.
  Group methods by responsibility rather than visibility alone.
- In Java, the historical convention places local declarations at the
  beginning of a block, except for loop indices in a `for` header. Other
  languages keep the same logical grouping using their own declaration and
  initialization syntax. Preserve scope and evaluation order.

## Naming and access

Use `PascalCase` for classes and interfaces, `lowerCamelCase` for methods
and variables, and `UPPER_SNAKE_CASE` for constants. Prefer complete,
meaningful words. Established domain abbreviations and simple loop indices
are acceptable when their meaning is immediately clear.

Access static members through their type. Encapsulate state, avoid hidden
multiple assignments, and name domain-significant numeric values.
Do not invent authors, dates, version histories, or license text for a header.

## PlaidShirt additions

The historical guide includes concise conditional expressions and wrapping
rules for them. PlaidShirt expands nested decisions into clearly named steps
and branches. An immediately understandable boolean return still does not
need an artificial `if` statement.

Complete doc comments for private helpers and affected elements are an
explicit PlaidShirt requirement. Use the appropriate language documentation guide.
Historical examples do not require copying obsolete APIs, build systems,
or legal notices.
