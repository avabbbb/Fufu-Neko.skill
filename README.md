# Fufu Neko

> Your always-current, codebase-first neko engineering partner.

Fufu Neko reads the repository before asking you for facts, checks current sources before trusting a time-sensitive memory, and turns important ambiguity into a decision with a recommendation. When a requested action is clear, she starts the reversible work immediately and keeps working through implementation, tests, failures, and verification.

She is a catgirl in the conversation and a rigorous engineer in the work. The character adds warmth; it never changes a command, a citation, a code block, or the standard of evidence.

## Why it exists

Ordinary assistants often answer a current technical question from old memory, ask the user to repeat facts already present in the repository, or turn a design discussion into a pile of generic questions. Fufu Neko uses a different working habit:

```text
read the code → check current reality → identify the human decision
→ recommend a path when needed → execute and verify the requested outcome
```

The result is a partner that can be playful without being vague, skeptical without being obstructive, and autonomous without turning routine work into an approval ceremony.

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
5. **Act on clear requests.** A request to fix, implement, refactor, test, or connect something authorizes ordinary reversible work in that task's understood scope. Ask only for a human decision that inspection cannot resolve.
6. **Keep executing.** Implement, test, inspect failures, fix causes, regress, and verify until the requested outcome exists or a real blocker appears. Do not ask whether to continue after each file.
7. **Keep durable memory small.** Reconcile project terminology and decisions with the actual code. Create an ADR only for a hard-to-reverse, surprising, real trade-off.

## Agency and autonomy

Fufu first infers the expected outcome. “Help me fix this bug” means inspect, edit, test, and verify; “what do you think of this design?” means analyze and recommend without mutating the repository unless asked.

The user request authorizes ordinary reversible work in the understood task scope. It does not silently include an unrelated deployment, publication, public PR, data deletion, or credential use. A named external action is part of the outcome when the user explicitly requests it, subject to the host's own permissions and approval behavior.

Fufu asks only for unresolved human judgment, material ambiguity, destructive or irreversible targets that are unclear, unrequested external effects, missing credentials or permissions, or contradictions that inspection cannot resolve. She prepares the safe work first, then asks a concrete question with a recommended option and trade-offs.

Independent research or inspection may be delegated when parallel work has a material benefit. Tightly coupled work and shared-file edits stay with the main agent. The main agent cross-checks delegated results and owns the final decision.

The detailed behavior lives in [the agency protocol](fufu-neko/references/agency-protocol.md), [the collaboration protocol](fufu-neko/references/collaboration-protocol.md), [the response style](fufu-neko/references/response-style.md), and [the skill conflict protocol](fufu-neko/references/skill-conflict-protocol.md).

## Modes

The portable skill name is `fufu-neko`. Hosts expose the same modes through their own invocation syntax:

```text
/fufu-neko             normal mode for the current task
/fufu-neko research    research and synthesize current evidence
/fufu-neko grill       resolve a design or product decision tree
/fufu-neko ship        execute and verify a requested outcome
/fufu-neko off         stop applying this skill for the current task or session
```

In Codex, use `$fufu-neko` with the same mode words or choose it through `/skills`. WorkBuddy and TeleAgent use their installed skill name and native invocation UI.

`/goal` remains the host's completion-condition command. Fufu Neko does not assign it an opt-out meaning. Use the host command when you want a measurable condition to drive continued work.

## When it triggers

Use it for substantive work involving a repository, product, code, architecture, technical research, APIs, libraries, frameworks, models, system design, implementation plans, or decisions that may change with time.

It should stay out of the way for simple arithmetic, direct translation, light copyediting, ordinary conversation, and formatting-only transformations that need no project or current-world judgment.

## Soul customization

The public persona source lives in `fufu-neko/references/persona/`. It describes Fufu's character and voice without personal context. Keep personal preferences and machine notes in a local ignored `soul/` directory, or another private location, and start from [`private-soul.example.md`](fufu-neko/assets/private-soul.example.md).

Never place credentials, tokens, private addresses, personal memory, relationship details, or machine-specific paths in a public persona file. The repository validator checks that local `soul/` is ignored and that no private soul file is tracked.

## Use with Codex, WorkBuddy, and TeleAgent

The same canonical `fufu-neko/` directory is the source for all three hosts. It contains one standard `SKILL.md`; host-specific metadata is generated only when an importer needs it.

### Codex

Codex discovers repository skills from `.agents/skills` and user skills from `$HOME/.agents/skills`. Install the canonical directory with PowerShell:

```powershell
$codexSkill = Join-Path $HOME ".agents\skills\fufu-neko"
New-Item -ItemType Directory -Force (Split-Path $codexSkill) | Out-Null
Copy-Item -Recurse -Force .\fufu-neko $codexSkill
```

In Codex, use `/skills` to select it or mention `$fufu-neko`. If your Codex build exposes the installer, you can also ask `$skill-installer` to install `https://github.com/avabbbb/Fufu-Neko.skill/tree/main/fufu-neko`.

### WorkBuddy

WorkBuddy accepts a skill directory containing `SKILL.md`, references, and scripts. The Open Platform marketplace is the preferred import path. If its importer requires WorkBuddy-specific display and bilingual metadata, build an upload-ready bundle:

```bash
python fufu-neko/scripts/build_host_bundle.py --host workbuddy
```

Zip `dist/workbuddy/fufu-neko/` with `SKILL.md` at the archive's skill root, then import it through WorkBuddy's Skills interface. A local WorkBuddy-compatible runner may instead use `~/.workbuddy/skills/fufu-neko/`. Invoke it by the displayed skill name or let the description matcher select it.

### TeleAgent

TeleAgent supports imported and private skills. Build the bundle with the Chinese metadata fields used by TeleAgent skill packages:

```bash
python fufu-neko/scripts/build_host_bundle.py --host teleagent
```

Import or copy `dist/teleagent/fufu-neko/` through the TeleAgent skill interface. Some desktop builds expose a local skills directory such as `~/.config/TeleAgent/skills/`; use the path configured by the installed build. Keep private soul files outside the bundle.

The host-specific bundle generator copies the canonical references and adds loading hints; it does not maintain a second behavior implementation.

The host details follow the [Codex skill documentation](https://developers.openai.com/codex/skills/), [WorkBuddy Skill documentation](https://open.workbuddy.cn/en/docs/skill), and [TeleAgent's official product documentation](https://www.teleai.com.cn/product/teleagent). Host UI labels and local paths can change independently of the skill format. The Codex page is currently served under the title "Build skills"; the discovery paths and invocation rules described here are unchanged.

## Validation status

This project separates a well-formed package from a demonstrated behavior. Codex is the host with recorded sessions; the other hosts are not yet. Read the claim, not the impression:

```text
Codex
  Skill discovery:          Runtime validated
  Agency behavior:          Runtime validated
  Repository-first:         Runtime validated
  Side-effect boundary:     Sample validated, needs explicit-authorization control
  Persona vs execution:     Sample validated, needs regression

Claude Code
  Structure / permission:   Spec aligned
  Runtime behavior:         Pending / partial

WorkBuddy
  Bundle generation:        Validated
  Runtime session:          Unverified

TeleAgent
  Bundle generation:        Validated
  Runtime session:          Unverified
```

A passing repository validator and a successful bundle build are packaging results. Neither is a behavior verdict, and neither is described here as runtime support.

Failures that belong to the harness rather than to the skill are tracked separately and are not treated as skill defects: a Windows sandbox helper environment failure, an incomplete orchestrator helper, and temporary fixture cleanup. The skill decides what the agent intends to do; the host decides what is allowed. When a run stops at a host gate, the correct report is the gate.

The full ledger, the evidence behind each row, and the next round of boundary controls live in [`VALIDATION.md`](VALIDATION.md).

## Install

The portable skill directory is [`fufu-neko/`](fufu-neko/), whose entrypoint is [`fufu-neko/SKILL.md`](fufu-neko/SKILL.md). Use that directory with any Agent Skills-compatible host.

Clone the repository:

```bash
git clone https://github.com/avabbbb/Fufu-Neko.skill.git
cd Fufu-Neko.skill
```

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
├── VALIDATION.md
├── LICENSE
├── CHANGELOG.md
├── .gitignore
├── fufu-neko/
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   ├── references/
│   │   ├── persona/
│   │   │   ├── core.md
│   │   │   └── voice.md
│   │   ├── research-protocol.md
│   │   ├── ask-protocol.md
│   │   ├── agency-protocol.md
│   │   ├── collaboration-protocol.md
│   │   ├── grilling.md
│   │   ├── docs-protocol.md
│   │   ├── execution-protocol.md
│   │   ├── coding-principles.md
│   │   ├── evidence-policy.md
│   │   ├── response-style.md
│   │   ├── skill-conflict-protocol.md
│   │   └── tool-bindings.md
│   ├── assets/
│   │   ├── CONTEXT.template.md
│   │   ├── ADR.template.md
│   │   └── private-soul.example.md
│   └── scripts/
│       ├── build_host_bundle.py
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
    ├── regression.json
    ├── host-compatibility.json
    ├── agency.json
    ├── boundary-trigger.json
    ├── boundary-ask.json
    ├── boundary-side-effect.json
    ├── boundary-delegation.json
    └── boundary-soul-leak.json
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

Build a standalone WorkBuddy or TeleAgent upload bundle when the host requires extra frontmatter:

```bash
python fufu-neko/scripts/build_host_bundle.py --host workbuddy
python fufu-neko/scripts/build_host_bundle.py --host teleagent
```

The files under `evals/` are behavior fixtures. They describe observable passes and failures for trigger accuracy, reality sync, question quality, decision-tree grilling, agency, collaboration, docs consistency, persona boundaries, private-soul safety, and regression behavior. Run each case in a fresh host session when measuring actual model behavior; a passing structure check alone is not a behavior verdict.

The `boundary-*.json` suites are controls rather than feature tests. They probe where the behavior should stop: implicit activation without an explicit mention, ASK only when a human decision truly remains, external side effects as a matched pair, delegation with and without independent boundaries, and a tracer that must never escape the private soul file. [`VALIDATION.md`](VALIDATION.md) defines the status vocabulary, the per-capability ledger, and how to record a run.

## Design principles

- Memory is a hypothesis, not evidence.
- The repository is the first source for repository facts.
- Questions resolve decisions; they do not decorate the workflow.
- Recommendations expose trade-offs.
- Clear action requests authorize ordinary reversible work; unresolved human decisions open a question.
- Errors stay visible until their cause is understood.
- Public persona and private memory have different boundaries.
- A verified result matters more than a confident-sounding answer.

## License

MIT. See [`LICENSE`](LICENSE).
