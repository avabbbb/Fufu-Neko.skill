# Host bindings and portability

Keep the behavior protocol host-neutral. Use the host's actual tools and capabilities rather than assuming a particular product, shell, browser, or model.

## Generic Agent Skills host

- The skill directory is `fufu-neko/` and its entrypoint is `SKILL.md`.
- A host may auto-invoke the skill from its description or let the user invoke it by directory name.
- If no interactive question tool exists, render a structured decision with lettered options and wait for the user's answer.
- If web search, repository access, or a test runner is unavailable, label the missing evidence and continue only when the remaining uncertainty is safe to carry.
- Do not claim persistent state across turns unless the host actually preserves it. Restate the scope-lock state when a new turn or host session loses context.

## Claude Code

- A skill under the personal or project skills directory is invoked as `/fufu-neko`; the directory name supplies the command name.
- Claude Code can pass trailing invocation arguments. Interpret `research`, `grill`, `ship`, and `off` as mode hints when supplied. Keep the main frontmatter within the open standard; host-specific autocomplete or invocation metadata belongs in host configuration.
- Use the real `AskUserQuestion` tool when it is available. It supports one to four multiple-choice questions and an `Other` path; use it for decisions, not for facts the repository can answer.
- `/goal` is a host completion-condition command. Never redefine it as Fufu Neko's opt-out command. `/fufu-neko off` is the user-facing opt-out for this skill when the host supports session-level invocation state.
- Permission prompts and external side effects remain governed by the host. The skill cannot grant itself permission by describing a tool in prose.

For another host, map these behaviors to its equivalent tools and document the mapping outside the core protocol. If a capability is absent, use the explicit structured-text fallback and preserve the evidence boundary.
