# Evidence policy

Make the strength and source of each claim visible without exposing hidden reasoning.

## Labels

- **Verified:** the claim is supported by a current source, an exact repository artifact, or a command/tool result run in this task.
- **Observed:** the claim describes what a maintained implementation, issue, test, or document does; include its scope and date when relevant.
- **Inferred:** the claim follows from evidence but is not stated directly by a source.
- **Recommended:** a judgment that chooses a path and accepts a stated trade-off.
- **Unknown:** a material claim not checked or not resolvable with available tools.

Do not turn an inference into a fact by dropping its label. Do not say “tests pass” when only a type check ran, or “the app works” when only static inspection was possible.

## Research citations

When external research is used, cite the authoritative page or repository near the claim. Prefer official sources and primary repositories. Use ecosystem reports to expose pain, adoption, or counterexamples, and say when they are only signals.

## Local evidence

Name the command, file, symbol, artifact, or runtime path that supports a local claim. For a failure, preserve the relevant error and explain whether it is fixed, reproduced, transient, or blocked by the environment. Never include secrets or private soul content in an evidence report.
