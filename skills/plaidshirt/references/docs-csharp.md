# C#: XML documentation comments

Use `///` with well-formed XML before types and members. The compiler can
produce an XML documentation file; a generator such as DocFX turns it into
an HTML site.
[Microsoft: XML documentation](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/xmldoc/).

Describe purpose with `<summary>`, parameters with `<param name="...">`,
results with `<returns>`, and actual exceptions with
`<exception cref="...">`. Add relevant `<typeparam>`, `<value>` for
properties, `<remarks>`, `<example>`, and `<see cref="..."/>` elements.
Names and references must match signatures, and XML characters must be
escaped correctly. Javadoc-style `@param` is not an XML documentation tag.
[Recommended tags](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/xmldoc/recommended-tags).

For asynchronous methods, describe task completion, the awaited result,
and relevant cancellation or failure conditions. Explain a
`CancellationToken` and its effect on work in progress.

## Example

```csharp
/// <summary>
/// Checks available inventory for individual requests.
/// </summary>
public static class InventoryAvailability {
    /// <summary>
    /// Checks whether inventory can fully cover a request.
    /// </summary>
    /// <param name="availableCount">Available non-negative item count.</param>
    /// <param name="requestedCount">Requested positive item count.</param>
    /// <returns>
    /// Whether both counts are valid and inventory is sufficient.
    /// </returns>
    public static bool canFulfillRequest(int availableCount,
            int requestedCount) {
        if (availableCount < 0 || requestedCount <= 0) {
            return false;
        }

        return availableCount >= requestedCount;
    }
}
```

This example applies PlaidShirt's shared naming and brace style to C#.
Preserve required framework member names and existing API contracts.
Report any concrete conflict with a binding project `.editorconfig`.

## Build and verify

When establishing an SDK-style project, enable the property in an
appropriate existing property group:

```xml
<GenerateDocumentationFile>true</GenerateDocumentationFile>
```

Then `dotnet build` produces XML documentation. Inspect its contents,
missing or mismatched comments, and resolvable references. Do not suppress
documentation warnings merely to make the check pass.
[MSBuild property](https://learn.microsoft.com/en-us/dotnet/core/project-sdk/msbuild-props#generatedocumentationfile).

With an existing DocFX configuration, `docfx docfx.json` can build
metadata and HTML. Check inputs, visibility, and a rendered type page.
[DocFX: .NET API documentation](https://dotnet.github.io/docfx/docs/dotnet-api-docs.html).
