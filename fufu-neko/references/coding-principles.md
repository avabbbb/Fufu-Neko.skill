# Coding principles

Prefer code that is simple, direct, observable, testable, and maintainable. Choose the smallest design that fully satisfies the stated scope and its real failure modes.

## No speculative compatibility

Do not build adapters, aliases, shims, or dual paths for an old interface or an imagined future consumer. If compatibility is an explicit business, migration, or public API requirement, treat it as scope: define the supported versions, behavior, removal condition, and tests.

## No silent fallback

Do not hide a broken invariant with a default, fallback provider, swallowed exception, empty result, or fake success. Validate user input and external responses at system boundaries. Retries, degraded behavior, and safe defaults are valid only when they are intentional, observable, and part of the requirement.

## No patch-on-patch fixes

When the symptom comes from a bad abstraction, ownership boundary, state model, or contract, repair that cause. Do not add a second workaround to preserve an accidental behavior unless preserving it is an explicit requirement.

## Comments and changes

Use names and structure that explain ordinary code. Add a short comment only for a non-obvious invariant, external constraint, or deliberate trade-off that a future maintainer cannot infer from the code. Keep errors visible and avoid unrelated cleanup that expands scope.
