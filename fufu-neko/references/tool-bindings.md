# Host bindings and portability

Keep the behavior protocol host-neutral. Use the host's actual tools and capabilities rather than assuming a particular product, shell, browser, or model.

## Generic Agent Skills host

- The canonical package is `fufu-neko/` and its entrypoint is `SKILL.md`.
- A host may auto-invoke the skill from its description or let the user invoke it by directory name.
- If no interactive question tool exists, render a structured decision with lettered options and wait for the answer.
- If web search, repository access, or a test runner is unavailable, label the missing evidence and continue only when the remaining uncertainty is safe to carry.
- Do not claim persistent state across turns unless the host actually preserves it. Re-inspect the task and restate the authorization scope when a new turn or host session loses context.

## Codex

- Codex can discover the canonical package from a repository `.agents/skills` directory or from the user-level `$HOME/.agents/skills` directory. Copy the whole `fufu-neko/` directory so `SKILL.md` remains at the skill root.
- Explicit invocation is `$fufu-neko` or selection through `/skills`. Implicit invocation depends on the frontmatter description.
- `agents/openai.yaml` is optional Codex metadata for display and invocation policy. It does not replace `SKILL.md` and does not contain the behavior protocol.
- Use Codex's available repository, shell, web, and interactive-question capabilities. If a capability is unavailable, use the generic structured-text fallback.
- `/goal` remains Codex's completion workflow. Do not reinterpret it as the skill's opt-out command.

## Claude Code

- A skill under the personal or project skills directory is invoked as `/fufu-neko`; the directory name supplies the command name.
- Claude Code can pass trailing invocation arguments. Interpret `research`, `grill`, `ship`, and `off` as mode hints when supplied. Keep the main frontmatter within the open standard; host-specific autocomplete or invocation metadata belongs in host configuration.
- Use the host's structured question tool when it is available. Use it for decisions, not for facts the repository can answer.
- `/goal` is a host completion-condition command. Never redefine it as Fufu Neko's opt-out command. `/fufu-neko off` is the user-facing opt-out for this skill when the host supports session-level invocation state.

## WorkBuddy

- WorkBuddy consumes a skill directory with a root `SKILL.md` and can load bundled `references/` and `scripts/` resources. Install through the WorkBuddy Skills marketplace or use the local skill directory supported by the installed WorkBuddy build.
- The Open Platform metadata surface may request display names, Chinese and English descriptions, a version, and an author. Generate the WorkBuddy bundle with `scripts/build_host_bundle.py --host workbuddy` when the importer requires those fields.
- WorkBuddy reference loading may use `@references/<file>.md`. The generated bundle includes a host loading map; preserve the bundled relative paths.
- Invoke the installed skill by its displayed name or allow WorkBuddy's description matcher to select it. Do not assume Claude-style slash commands.

## TeleAgent

- TeleAgent supports imported or private skills. Use its skill import UI when available, or copy the generated `dist/teleagent/fufu-neko/` bundle into the local skills directory configured by the desktop build.
- Public TeleAgent skill examples use `name`, `description`, Chinese metadata, `version`, and `author`. Generate the compatible bundle with `scripts/build_host_bundle.py --host teleagent` instead of editing the canonical frontmatter.
- Keep private soul and machine context outside the imported bundle. TeleAgent's local execution ability does not authorize the skill to expose secrets or bypass host permissions.
- Invoke by the installed skill name or let TeleAgent match the description. Use structured text when the host has no interactive decision tool.

## Permissions and side effects

Permission prompts, network access, file access, and external side effects remain governed by the host. The skill cannot grant itself permission by describing a tool in prose.
