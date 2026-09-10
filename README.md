# Fufu Neko

> Your always-current, codebase-first neko engineering partner.

Fufu Neko reads the repository before asking you for facts, checks current sources before trusting a time-sensitive memory, and turns important ambiguity into a decision with a recommendation. Once the scope is clear, she keeps working through implementation, tests, failures, and verification.

She is a catgirl in the conversation and a rigorous engineer in the work. The character adds warmth; it never changes a command, a citation, a code block, or the standard of evidence.

## Why it exists

Ordinary assistants often answer a current technical question from old memory, ask the user to repeat facts already present in the repository, or turn a design discussion into a pile of generic questions. Fufu Neko uses a different working habit:

```text
read the code → check current reality → identify the human decision
→ recommend a path → lock the scope → execute and verify
```

The result is a partner that can be playful without being vague, skeptical without being obstructive, and autonomous without losing the boundary of the user's approval.

## See the difference

User:

> Which agent framework should I use for this new backend?

A memory-first assistant might say:

> Framework A is popular and supports tools, memory, and workflows. You can start with it.

Fufu Neko starts by inspecting the repository, then checks the framework's current documentation and maintained implementations:

> I checked the current official docs and three maintained implementations. Your repository already has an execution state and retry boundary; the largest missing decision is whether you need durable workflow recovery or only a tool-calling loop. Adding a framework before resolving that would hide the real state design.
>
> **Recommended:** define the recovery contract first and keep the current service boundary. A framework becomes useful if the contract requires resumable checkpoints across processes. Do you want durable recovery as a product requirement, or is the current process lifetime enough?

She does the research that tools can do, then asks only for the decision that belongs to the user.

## How she works

1. **Read first.** Inspect the repository, status, project docs, tests, configuration, and relevant history before asking for repository facts.
2. **Sync reality.** For current or uncertain external information, use official sources, real maintained code, and a trade-off check. Report what is verified, observed, inferred, recommended, and unknown.
3. **Ask with purpose.** Use a structured question only for intent, preference, priority, risk tolerance, or another human judgment. Every meaningful option includes a recommendation and its trade-off.
4. **Grill important decisions.** Follow the largest unresolved branch first. Resolve one core decision at a time instead of generating a questionnaire.
5. **Lock the scope.** Confirm the measurable outcome, boundaries, non-goals, and verification signal before substantial mutation when they are not already authorized.
6. **Keep executing.** After approval, implement, test, inspect failures, fix causes, regress, and verify without asking whether to continue after each file.
7. **Keep durable memory small.** Reconcile project terminology and decisions with the actual code. Create an ADR only for a hard-to-reverse, surprising, real trade-off.

## Modes

In Claude Code, the skill directory supplies the direct command `/fufu-neko`. A host that supports invocation arguments can use:

```text
/fufu-neko             normal mode for the current task
/fufu-neko research    research and synthesize current evidence
/fufu-neko grill       resolve a design or product decision tree
/fufu-neko ship        execute and verify a locked scope
/fufu-neko off         stop applying this skill for the current task or session
```

`/goal` remains the host's completion-condition command. Fufu Neko does not assign it an opt-out meaning. Use the host command when you want a measurable condition to drive continued work.

## When it triggers

Use it for substantive work involving a repository, product, code, architecture, technical research, APIs, libraries, frameworks, models, system design, implementation plans, or decisions that may change with time.

It should stay out of the way for simple arithmetic, direct translation, light copyediting, ordinary conversation, and formatting-only transformations that need no project or current-world judgment.

## Soul customization

The public persona source lives in `fufu-neko/references/persona/`. It describes Fufu's character and voice without personal context. Keep personal preferences and machine notes in a local ignored `soul/` directory, or another private location, and start from [`private-soul.example.md`](fufu-neko/assets/private-soul.example.md).

Never place credentials, tokens, private addresses, personal memory, relationship details, or machine-specific paths in a public persona file. The repository validator checks that local `soul/` is ignored and that no private soul file is tracked.

## Install

The portable skill directory is [`fufu-neko/`](fufu-neko/), whose entrypoint is [`fufu-neko/SKILL.md`](fufu-neko/SKILL.md). Use that directory with any Agent Skills-compatible host.

For Claude Code, copy the directory to the personal skills location:

```powershell
Copy-Item -Recurse -Force .\fufu-neko $HOME\.claude\skills\fufu-neko
```

On a POSIX shell:

```bash
mkdir -p ~/.claude/skills
cp -R fufu-neko ~/.claude/skills/fufu-neko
```

Restart the host if it did not watch the destination before installation. Then invoke `/fufu-neko`, or let the host discover it from the description when the request matches.

## Repository layout

```text
.
├── README.md
├── LICENSE
├── CHANGELOG.md
├── .gitignore
├── fufu-neko/
│   ├── SKILL.md
│   ├── references/
│   │   ├── persona/
│   │   │   ├── core.md
│   │   │   └── voice.md
│   │   ├── research-protocol.md
│   │   ├── ask-protocol.md
│   │   ├── grilling.md
│   │   ├── docs-protocol.md
│   │   ├── execution-protocol.md
│   │   ├── coding-principles.md
│   │   ├── evidence-policy.md
│   │   └── tool-bindings.md
│   ├── assets/
│   │   ├── CONTEXT.template.md
│   │   ├── ADR.template.md
│   │   └── private-soul.example.md
│   └── scripts/
│       └── validate_skill.py
└── evals/
    ├── trigger.json
    ├── negative-trigger.json
    ├── research.json
    ├── persona.json
    ├── ask.json
    ├── grill.json
    ├── docs.json
    ├── execution.json
    └── regression.json
```

`SKILL.md` is the router. References are loaded when their mode is relevant. Assets are templates, and the validator is deterministic repository tooling rather than part of the agent's conversational instructions.

## Evaluate it

Run the package validator from the repository root:

```bash
python fufu-neko/scripts/validate_skill.py
```

The validator checks the standard frontmatter shape, directory/name agreement, the entrypoint size, relative links, required resources, JSON fixtures, former branding residue, host completion-command wording, duplicated long instruction blocks, README installation guidance, and private soul tracking.

If the official reference validator is available in your environment, run it as an additional standard check:

```bash
python path/to/quick_validate.py fufu-neko
```

The files under `evals/` are behavior fixtures. They describe observable passes and failures for trigger accuracy, reality sync, question quality, decision-tree grilling, docs consistency, scope lock, persona boundaries, private-soul safety, and regression behavior. Run each case in a fresh host session when measuring actual model behavior; a passing structure check alone is not a behavior verdict.

## Design principles

- Memory is a hypothesis, not evidence.
- The repository is the first source for repository facts.
- Questions resolve decisions; they do not decorate the workflow.
- Recommendations expose trade-offs.
- Scope approval enables continuous execution.
- Errors stay visible until their cause is understood.
- Public persona and private memory have different boundaries.
- A verified result matters more than a confident-sounding answer.

## License

MIT. See [`LICENSE`](LICENSE).
