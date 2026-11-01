# JavaScript and TypeScript

## JavaScript: JSDoc

Place `/** ... */` directly before the documented element. Cover modules,
types, functions, methods, and relevant properties. Describe parameters
with `@param {Type} name`, results with `@returns {Type}`, and actual
failures with `@throws`. An ordinary `/* ... */` comment is not a JSDoc block.
[JSDoc introduction](https://jsdoc.app/about-getting-started) ·
[Parameter syntax](https://jsdoc.app/tags-param)

Document optional arguments and object properties where relevant. For
asynchronous operations, explain the resolved value, rejection conditions,
and side effects. A JavaScript result type can use `Promise<Result>`.

```javascript
/**
 * Checks whether inventory can fully cover another request.
 *
 * @param {number} availableCount - Available non-negative integer count.
 * @param {number} requestedCount - Requested positive integer count.
 * @returns {boolean} Whether both counts are valid and inventory is sufficient.
 */
function canFulfillRequest(availableCount, requestedCount) {
    if (!Number.isSafeInteger(availableCount) || availableCount < 0) {
        return false;
    }

    if (!Number.isSafeInteger(requestedCount) || requestedCount <= 0) {
        return false;
    }

    return availableCount >= requestedCount;
}
```

With local JSDoc installed, an example is `jsdoc -r src -d build/docs`.
Prefer the project's established package command.

## TypeScript: TSDoc and TypeDoc

TSDoc describes a comment format; TypeDoc is a possible generator.
TypeDoc also reads JSDoc tags, and its parser does not match every TSDoc
detail. Preserve a compatible project combination.
[TSDoc](https://tsdoc.org/) ·
[TypeDoc comments](https://typedoc.org/documents/Doc_Comments.html)

Use `@param name - meaning`, `@returns`, and relevant `@typeParam`,
`@remarks`, or `@example` sections. Types belong in TypeScript signatures.
Avoid a second contradictory type definition in comments; still document
the domain meaning.

```typescript
/**
 * Checks whether inventory can fully cover another request.
 *
 * @param availableCount - Available non-negative integer count.
 * @param requestedCount - Requested positive integer count.
 * @returns Whether both counts are valid and inventory is sufficient.
 */
export function canFulfillRequest(
    availableCount: number,
    requestedCount: number
): boolean {
    if (!Number.isSafeInteger(availableCount) || availableCount < 0) {
        return false;
    }

    if (!Number.isSafeInteger(requestedCount) || requestedCount <= 0) {
        return false;
    }

    return availableCount >= requestedCount;
}
```

Run the existing TypeDoc command and check entry points, export coverage,
visibility filters, and links. Enable `validation.notDocumented` when
missing-comment warnings are required; it is disabled by default.
[Validation options](https://typedoc.org/documents/Options.Validation.html).
