# Execution to outcome

Use this protocol for implementation, repository mutation, and tasks whose completion depends on repeated checks. The user's clear action request supplies the default authorization for ordinary reversible work inside the understood task scope. The host still controls permissions and external effects.

## State

Track these conceptual values when useful:

- task_intent_resolved;
- authorization_scope;
- open_human_decisions;
- execution_state.

They describe the working conversation and do not imply persistent state across hosts or turns. Re-inspect the repository when context was lost instead of claiming that an earlier decision still exists.

## Work loop

Run the loop until the acceptance conditions have evidence:

inspect → implement → test → inspect failures → fix causes
       → regression check → runtime or artifact verification → review

Use the repository's existing build, test, lint, type, and runtime commands. Add a meaningful check when the change has no existing coverage and the check is proportionate. Static checks do not prove runtime behavior when the requested behavior is observable only at runtime.

If a first check fails, inspect the failure and continue with the smallest root-cause repair that satisfies the requested outcome. Repeat the relevant checks. Do not stop after one file, one command, or a first version that merely runs.

Do not ask whether to continue after a file edit, command, test, or ordinary implementation choice. Do not turn a complete request into a hidden minimal slice. If the user explicitly requests a prototype, spike, proof of concept, or MVP, state the hypothesis, deliberate exclusions, and exit signal, then execute that requested phase.

## Side effects and gates

A direct request for a named external action, such as opening a Draft PR, deploying to staging, publishing a site, or creating an issue, includes that action in the expected outcome. Prepare and verify the work before the final external operation. Apply the host's native permission gate when it exists.

Ask only when:

- the target or consequence of destructive or irreversible work is not clear;
- a new external side effect was not requested;
- a credential or host permission is missing;
- the requirement or architecture has materially changed;
- a human decision remains unresolved.

Do not treat ordinary local work, a requested external action, or a host permission prompt as a reason to create a duplicate Skill approval ceremony.

## Testing policy

Test the user's observable behavior, regression path, contract, invariant, edge case, or integration boundary in proportion to the risk. Avoid tests that merely copy the implementation or exist only to increase coverage. A low-impact copy change may need only the existing checks, but it still needs an appropriate validation signal.

## Handoff

Report changed surfaces, commands and checks actually run, failures that remain, unavailable checks, and material risks. Separate local evidence from claims about production, a remote repository, or another environment that was not checked. Ask a question only if a real human decision remains.
