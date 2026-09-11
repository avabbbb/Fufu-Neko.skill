# Changelog

## 2.1.1

- Added `VALIDATION.md`: a status vocabulary, a per-capability ledger separating runtime-validated behavior from packaging results, and the layering rule that the skill decides intent while the host decides permission.
- Added five boundary control suites to `evals/`: implicit activation without an explicit mention, ASK only when a human decision truly remains, external side effects as a matched pair, delegation with and without independent boundaries, and a private-soul tracer that must not escape.
- Registered the boundary suites in the validator's expected fixture list, so a missing or malformed control file now fails the package check.
- Added a README validation-status section so bundle generation is never described as runtime support, and separated host and harness failures from skill correctness.
- Documented a proposed `description` rewrite as a held-back change, to be applied after the implicit-trigger baseline is recorded.

## 2.1.0

- Replaced approval-before-implementation behavior with an agency protocol that acts on clear requests and asks only for unresolved human decisions.
- Added conditional delegation, parallel research, worktree guidance, response-style rules, and visible skill-conflict reporting.
- Added agency evaluation fixtures and updated existing execution, trigger, grilling, and question cases for continuous action.

## 2.0.0

- Rebuilt the skill as Fufu Neko with a codebase-first research and decision workflow.
- Split persona, research, questions, grilling, docs, execution, coding, evidence, and host guidance into focused references.
- Added public-safe context, ADR, and private soul templates.
- Added behavior-oriented evaluation suites and a repository validator.
- Added Codex metadata and deterministic WorkBuddy/TeleAgent bundle generation from the canonical skill.
- Protected local soul and machine context from the public package.
