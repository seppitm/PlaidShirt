# Other language-native documentation formats

Read only the section relevant to the task. These rules supplement the
shared documentation contract with language syntax and tool choices.

## C and C++: Doxygen

Use, for example, `/** ... */` with `@brief`, `@param[in]`,
`@param[out]`, `@return`, and applicable `@throws`. Document
preconditions, null pointers, buffer lengths, ownership, and lifetimes
where they govern the contract. Keep declarations and definitions
consistent. Private functions receive documentation too.
[Official comment forms](https://www.doxygen.nl/manual/docblocks.html).

An existing project can run `doxygen Doxyfile`. Check `INPUT`,
`FILE_PATTERNS`, recursion, and warnings. An internal view may require
`EXTRACT_PRIVATE = YES` and `EXTRACT_STATIC = YES`. File-level elements
may also need file documentation such as `@file`.
`EXTRACT_ALL = YES` can disable undocumented-element warnings and is
not proof of complete documentation.
[Configuration reference](https://www.doxygen.nl/manual/config.html).

## Rust: rustdoc

Use `///` for the following item and `//!` for its enclosing module
or crate. Describe the contract in Markdown. Add appropriate
`# Examples`, `# Errors`, `# Panics`, and `# Safety` sections.
Where possible, examples should run as documentation tests.
[Official rustdoc book](https://doc.rust-lang.org/rustdoc/how-to-write-documentation.html).

In a Cargo project, use `cargo doc --no-deps`, adding
`--document-private-items` for an internal view.
Check examples with `cargo test --doc`. Inspect generated item pages
and links; passing doc tests alone do not prove a complete contract.

## Go: doc comments

Place `//` comment blocks directly before declarations without a
separating blank line. Descriptions of named elements normally begin
with the element's name. Cover packages, types, functions, methods,
fields, and constants; PlaidShirt also includes unexported helpers.
Describe parameters and failures in prose rather than invented
`@param` tags.
[Official Go doc comments](https://go.dev/doc/comment).

Inspect an API with `go doc ./path/to/package`, using `-u` where
unexported elements should be included. This is a text view; a requested
HTML site needs an additional suitable tool. Preserve visibility and required
API names. When binding project tooling requires `gofmt`, report any resulting
differences from the shared layout rules.
