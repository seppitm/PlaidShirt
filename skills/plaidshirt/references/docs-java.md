# Java: Javadoc

Use traditional `/** ... */` comments directly before a declaration,
including its annotations. Document types, constructors, methods, fields,
and constants; use `package-info.java` for a package description where
appropriate. PlaidShirt includes private helpers.
[Official syntax and association rules](https://docs.oracle.com/en/java/javase/25/docs/specs/javadoc/doc-comment-spec.html).

Use `@param` for parameters and type parameters, `@return` for actual
results, and `@throws` for relevant failures. Describe boundaries, units,
and null handling. Link symbols with `{@link ...}` and format code with
`{@code ...}`. Use `{@inheritDoc}` only where a contract is genuinely
inherited. Additional tags must fit the project's JDK version.

## Example

```java
/**
 * Calculates the remaining number of inventory items.
 */
public final class InventoryCounter {

    /**
     * Prevents instances of this stateless utility class.
     */
    private InventoryCounter() {
    }

    /**
     * Returns the number of items not yet processed.
     *
     * @param totalCount total item count, at least 0
     * @param processedCount processed count between 0 and the total,
     *        inclusive
     * @return the non-negative remaining count
     * @throws IllegalArgumentException if either count is negative
     *         or the processed count exceeds the total
     */
    public static int countRemainingItems(int totalCount,
            int processedCount) {
        if (totalCount < 0) {
            throw new IllegalArgumentException(
                    "The total count must not be negative.");
        }

        if (processedCount < 0 || processedCount > totalCount) {
            throw new IllegalArgumentException(
                    "The processed count is outside the inventory.");
        }

        return totalCount - processedCount;
    }
}
```

## Build and verify

Prefer the project's Maven or Gradle documentation task. For a suitable
standalone source file, an example local JDK invocation is:

```text
javadoc -private -Xdoclint:all -encoding UTF-8 -d build/docs InventoryCounter.java
```

`-private` includes internal elements. Inspect generated class and method
views. A published API build may deliberately use different visibility.
The linked specification describes JDK 25 without prescribing a target
version; check supported tags and options for other JDKs.
