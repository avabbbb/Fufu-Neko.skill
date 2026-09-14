# Changelog

## 2.1.2

- Fixed the private-soul canary fixture: the concrete value is no longer committed, so the zero-hit condition is satisfiable. A fresh `FUFU_PRIVATE_CANARY_<UUID>` is minted per run.
- Widened the canary scan to the whole tree, not only git-tracked files, because a leaked generated artifact, an attached patch, or a staged file would all be invisible to a tracked-only scan.
- Added `scripts/boundary_run.py`: a neutral fixture repository, a decoy skill inventory that pressures the Codex initial-skills budget, the runtime canary, and the run ledger.
- Added `evals/BOUNDARY-RUNBOOK.md`: phase order, repetition counts, scoring, and the rule that one observation is one piece of evidence.
- Extended the run metadata to include repository SHA, Codex version, model, reasoning effort, approval mode, sandbox mode, OS, CWD, installed skill count and inventory, inventory variant, session mode, exact prompt, repetition, transcript reference, and raw outcome.
- Restated `VALIDATION.md` around the boundary program. No capability was upgraded in this release; it adds the ability to measure, not measurements.
- Behavior changed: none. This release touches validation infrastructure, harness tooling, and documentation only.

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
