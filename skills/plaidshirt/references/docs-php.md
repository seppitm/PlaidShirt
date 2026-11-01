# PHP: PHPDoc and phpDocumentor

Attach a `/** ... */` DocBlock to its element. Document files, classes,
interfaces, traits, functions, methods, properties, and constants; use other
structural elements where supported by the tool. One DocBlock is associated
with one structural element.
[DocBlock structure](https://docs.phpdoc.org/guide/guides/docblocks.html).

Use `@param Type $name`, `@return Type`, and `@throws ExceptionType`
for applicable contracts. Properties can use `@var`. Native PHP type
declarations remain authoritative. Doc types must agree with them and can
provide additional information such as collection element types.
Typed parameters still need meaningful descriptions.
[Parameters](https://docs.phpdoc.org/guide/references/phpdoc/tags/param.html) ·
[Return values](https://docs.phpdoc.org/guide/references/phpdoc/tags/return.html)

## Example

```php
<?php

/**
 * Checks whether inventory can fully cover another request.
 *
 * @param int $availableCount Available non-negative item count.
 * @param int $requestedCount Requested positive item count.
 * @return bool Whether both counts are valid and inventory is sufficient.
 */
function canFulfillRequest(int $availableCount, int $requestedCount): bool {
    if ($availableCount < 0 || $requestedCount <= 0) {
        return false;
    }

    return $availableCount >= $requestedCount;
}
```

This example assumes its declared integer contract. Preserve the project's
`strict_types` decision; a DocBlock does not change runtime coercion.

## Build and verify

Use the existing phpDocumentor task. With `phpdoc` installed, an example
is `phpdoc -d src -t build/docs`. Preserve configured input and output
paths in an existing `phpdoc.xml`.
[Official invocation and configuration](https://docs.phpdoc.org/guide/guides/running-phpdocumentor.html).

Inspect generated elements, PHPDoc types, links, and diagnostics.
phpDocumentor does not automatically compare doc types with native type
declarations; use existing static analysis or check the contracts directly.
A PHP syntax check does not verify DocBlock completeness.

Document private methods in source and include them in the generator's
selection when a complete internal developer view is required.
