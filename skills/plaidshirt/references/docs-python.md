# Python: docstrings and Sphinx

Use `"""..."""` as the first statement of a module, class, function,
or method. A preceding `#` comment does not become its `__doc__`.
Begin with a short summary; separate additional detail with a blank line.
PlaidShirt also documents private helpers.
[PEP 257](https://peps.python.org/pep-0257/).

Apply PlaidShirt's shared naming and layout rules to custom Python code.
The example deliberately uses `lowerCamelCase`; Python's colons, indentation,
special method names, and docstring syntax remain valid and unchanged.

Preserve an established reStructuredText, Google, or NumPy format. Without
a project decision, use Google-style docstrings with Sphinx and Napoleon.
Keep technical section names such as `Args`, `Returns`, `Raises`, and
`Yields`. Describe parameters, results, actual failures, and generated
values where applicable.
[Sphinx Napoleon](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html).

Prefer native type hints. Keep any additional documented types consistent
and explain meaning even when hints are complete. For async functions,
describe the awaited result, failures, cancellation, and side effects
where they belong to the contract.

## Example

```python
"""Check inventory availability for individual requests."""


def canFulfillRequest(availableCount: int, requestedCount: int) -> bool:
    """Check whether inventory can fully cover a request.

    Args:
        availableCount: Available non-negative integer count.
        requestedCount: Requested positive integer count.

    Returns:
        Whether both counts are valid and inventory is sufficient.
    """
    if type(availableCount) is not int or availableCount < 0:
        return False

    if type(requestedCount) is not int or requestedCount <= 0:
        return False

    return availableCount >= requestedCount
```

The explicit type check also rejects booleans as item counts.
Type hints alone do not perform runtime validation.

## Build and verify

Sphinx `autodoc` reads documentation from importable modules.
Google/NumPy docstrings also need `sphinx.ext.napoleon` in the relevant
configuration. Documentation pages must actually include affected modules
through `automodule`, `autoclass`, or related directives.
[Sphinx autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html).

Use the existing documentation task. With Sphinx installed and configured,
an example is `sphinx-build -b html -W --keep-going docs build/docs`.
Inspect generated module and function pages; account for private-member
settings when an internal view is needed.

`autodoc` imports project modules and can trigger import side effects.
Use the intended development environment. Importing must not accidentally
start the application or make production requests.
