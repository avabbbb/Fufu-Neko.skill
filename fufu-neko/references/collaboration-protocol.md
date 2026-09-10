# Collaboration and delegation

Use delegation to improve independent investigation or verification. More agents are not a quality signal by themselves. The main agent remains responsible for the final synthesis, decision, and handoff.

## Delegate when independence creates value

Delegate work that has a clean boundary and can proceed without frequent shared context:

- independent official-document and ecosystem research;
- separate module or subsystem inspection;
- large log or repository searches;
- security, performance, or test reviews;
- independent hypotheses about a failure;
- modules that can be implemented without editing the same files.

For independent research, a useful split is official current behavior, maintained real implementations, and failure or ecosystem signals. The main agent must cross-check contradictions and synthesize the result; it must not concatenate summaries and call that a conclusion.

The parent flow is:

DECOMPOSE → DELEGATE → COLLECT → CROSS-CHECK → SYNTHESIZE → DECIDE

## Keep coupled work in the main agent

Do not delegate a small change, a tightly ordered multi-stage task, dense edits to one core file, work that needs continuous user interaction, or work where setup and merge cost exceed the likely benefit. Keep one owner for shared state and sequential architecture decisions.

Do not delegate the final architecture choice. A delegate can provide evidence or a bounded implementation; the main agent checks it against the user's goal, repository facts, and other results.

## Isolate parallel edits

When parallel workers need to modify files and their edits could interfere, use a temporary isolated worktree or branch if the host supports it. Compare the results, keep the compatible change, and integrate it deliberately. Ordinary temporary isolation is part of implementing an already requested task and does not require a second skill-level confirmation.

Do not create a worktree for a simple single-threaded change or use isolation as a substitute for understanding ownership.

## Host portability

Use the host's native subagent, worktree, and parallel-task capabilities when available. If they are unavailable, perform the same decomposition in the main agent or use the host's equivalent. The protocol does not require a particular agent-team product, nested-agent feature, or vendor-specific command.
