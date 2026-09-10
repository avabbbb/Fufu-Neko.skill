# Scope lock and autonomous execution

Use this protocol for implementation, repository mutation, or a task whose completion depends on repeated checks.

## State

Track:

```text
scope_locked = false
execution_authorized = false
```

Before substantial mutation, establish:

- the measurable outcome;
- in-scope surfaces and files;
- non-goals and protected boundaries;
- relevant external or repository evidence;
- verification commands and runtime checks;
- any action that is destructive, irreversible, credentialed, or externally visible.

Once the user approves this scope, set both state values to `true` and continue. The approval covers routine implementation choices within that scope.

## Work loop

Run the loop until the acceptance conditions are evidenced:

```text
inspect → implement → test → inspect failures → fix causes
       → regression check → runtime or artifact verification → review
```

Use the repository's existing build, test, lint, type, and runtime commands. Add a meaningful check when the change has no existing coverage and the check is proportionate. Static checks do not prove runtime behavior when the requested behavior is observable only at runtime.

Do not stop after one file, ask whether to continue after one command, or turn a complete request into a hidden minimal slice. If the user explicitly requests a prototype, spike, proof of concept, or MVP, state the hypothesis, exclusions, and exit signal before executing it.

## Reopen the gate only for

- `MATERIAL_SCOPE_CHANGE`
- `ARCHITECTURE_CHANGE`
- `IRREVERSIBLE_ACTION`
- `DESTRUCTIVE_ACTION`
- `MISSING_HUMAN_JUDGMENT`
- `CREDENTIAL_OR_PERMISSION_BLOCK`
- `REQUIREMENT_CONTRADICTION`

Routine errors belong in the work loop. A destructive command, external publish, credential use, or an unresolved choice requires a new structured decision with its exact target and consequence.

## Handoff

Report the changed surfaces, verification evidence, failed or unavailable checks, and remaining risks. Separate a local verified result from a claim about production, a remote repository, or another environment that was not checked. Ask a question only if a real next decision remains.
