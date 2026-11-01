# Engineering workflow

Use a workflow proportionate to the task. A small correction may need only a
few checks; a larger feature benefits from explicit requirements and models.

1. **Understand the request.** Establish requirements, domain terms, inputs,
   outputs, failures, and observable acceptance cases.
2. **Design.** Identify responsibilities, data, and important control flow.
   Add a diagram when it answers a concrete question.
3. **Implement.** Use descriptive names, encapsulation, suitable data structures,
   and justified patterns.
4. **Verify.** Check normal, boundary, and failure cases. Use configured
   formatting, type, and static-analysis tools.
5. **Document and build.** Update native contracts, generate the relevant
   documentation, and synchronize affected diagrams.
6. **Hand off.** Explain the result, checks, remaining limits, and consequential
   design decisions.

Repeat earlier steps when new evidence changes the design. This workflow
does not require a waterfall process or extensive paperwork for trivial work.

## Definition of done

The requested behavior works, affected contracts remain consistent, meaningful
checks pass, and relevant configured documentation builds produce the expected
content. A changed diagram agrees with the implementation or is explicitly
labeled as a proposed design. Material unverified work is stated clearly.
