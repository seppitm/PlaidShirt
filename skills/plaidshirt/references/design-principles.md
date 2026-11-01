# Principles and design patterns

Use these principles together to make decisions about the current problem.

| Principle | Practical decision |
| --- | --- |
| KISS | Choose a flow and model a colleague can explain. Character count is not the measure. |
| DRY | Maintain the same business rule in one responsible place. Similar text alone does not prove a shared rule. |
| YAGNI | Implement required behavior. Clear names, encapsulation, doc comments, and understandable structure are current quality requirements. |
| Single Responsibility | Group work with the same reason to change. |
| Open/Closed | Introduce extension points for real variants required by the current design. |
| Liskov Substitution | Implementations preserve their abstraction's contracts, invariants, and expected failures. |
| Interface Segregation | Design focused interfaces around their consumers' needs. |
| Dependency Inversion | Decouple domain rules from replaceable technical details at useful boundaries. |
| Encapsulation | Manage state where its invariants can be protected; limit visibility and mutable access. |

## Complex problems

Describe the actual difficulty first: interchangeable calculation rules,
state-dependent behavior, an incompatible external interface, or independent
event consumers. Then assess whether an established pattern clarifies it.

| Observed problem | Pattern to assess |
| --- | --- |
| Multiple required strategies sharing a contract | Strategy |
| Domain state governs behavior and transitions | State |
| An external interface differs from the required one | Adapter |
| Additional responsibilities need deliberate composition | Decorator |
| Independent consumers react to events | Observer |
| Creating required product variants needs a common design | Factory Method or Abstract Factory |
| A subsystem needs a clear entry point | Facade |

Treat this table as guidance. Justify the chosen pattern using the concrete
problem and roles. Consider implementation effort, indirection, testability,
failure behavior, and relevant runtime costs. Keep a direct solution when
it already makes the complexity clear. A familiar pattern is not a reason
to introduce extra layers.

Document an applied pattern on its responsible type or module: the problem,
pattern name, participating roles, and main tradeoff. A separate design note
can help for decisions spanning modules; a local decision does not require
its own documentation system. Consult original pattern references or
official framework documentation when implementation details need checking.
