# Docs-anchored project memory

Use this protocol when the repository has project context, a glossary, architecture material, decision logs, ADRs, or terminology that may affect implementation.

## Read order

Start with the smallest relevant set:

1. `README.md` and contribution or development instructions;
2. `CONTEXT.md` or equivalent project brief;
3. `docs/`, architecture notes, glossary, and decision register;
4. `docs/adr/` or equivalent ADRs;
5. the code and tests that implement the relevant claim.

Use repository truth to check spoken assumptions. If a user says a mutation requires approval but a second code path bypasses it, report the contradiction as a system fact and identify the decision: fix the bypass or intentionally keep it.

## Durable records

Keep terminology, open questions, and decisions close to the repository only when another contributor will need them. Prefer updating an existing record to creating a parallel document.

Create an ADR only when all three conditions hold:

- the decision is hard to reverse;
- a future maintainer would reasonably ask why it exists;
- there was a real trade-off between viable alternatives.

Do not create an ADR for routine naming, formatting, a local bug fix, or a choice already dictated by the project.

Use [the ADR template](../assets/ADR.template.md) when a new ADR is warranted. Use [the context template](../assets/CONTEXT.template.md) only when the project has no suitable context document and the user wants one.

## Consistency check

Before handoff, check that new decisions, terminology, and claims agree across the affected docs, code, and tests. Mark unresolved disagreement as `Unknown` or an open decision; do not silently rewrite project history to make the documents look consistent.
