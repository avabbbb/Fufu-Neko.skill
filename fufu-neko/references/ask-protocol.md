# Decision questions

Use the host's interactive question tool when one exists. If it does not, render the same structure as a short lettered choice and wait for the user's answer. Do not claim that a text prompt was an interactive tool call.

ASK resolves human judgment. It is not a ritual approval step for work the user already requested.

## Before asking

1. Read the repository, project docs, conversation context, and current sources that can answer factual parts of the question.
2. State the facts already established and identify the exact evidence.
3. Isolate the remaining decision that requires the user's intent, preference, priority, risk tolerance, or business meaning.
4. Complete all safe preparation that does not depend on the answer, including impact analysis, affected-file identification, and rollback assessment when relevant.

Do not ask for framework, database, directory, API, test, or configuration facts that the repository can reveal. Do not ask whether to start, continue, or perform a clearly requested local fix.

## Shape of a good question

Each meaningful question contains:

- the decision in one sentence;
- the recommended option first;
- two to four options when real alternatives exist;
- a short description of the downstream trade-off for each option;
- an Other path when the host supplies one or the user may need a custom answer.

Example:

已确认：现有 mutation 路径有两个入口，测试只覆盖其中一个。

真正需要决定的是：Registry 是否继续作为唯一 mutation gateway？

A. 继续使用 Registry（Recommended）
   共享审计和权限边界，代价是迁移第二个入口。
B. 保留 Service 直调
   路径更短，但会继续维护两套边界。
C. 迁移期间暂时双写
   降低切换风险，但增加状态不一致和清理成本。

Prefer a concrete decision over an open prompt such as “接下来怎么办？” or “你想怎么做？”.

## When ASK is allowed

Ask for:

- a missing product or business decision;
- material scope ambiguity;
- multiple valid directions with a real trade-off;
- a destructive or irreversible action when the exact target or consequence is unclear;
- an external side effect the user has not requested;
- missing credentials or host permissions;
- a contradiction that inspection cannot resolve.

An explicit user instruction for a concrete side effect is already an instruction to perform that side effect. Do not ask a second Skill-level confirmation. Respect the host's own permission or approval behavior.

## When ASK is not needed

Do not ask for:

- reading or searching code and documents;
- current research;
- running tests, builds, lint, or type checks;
- fixing a requested bug;
- reversible local refactoring within the requested outcome;
- following an architecture the user has already selected;
- regression checks or result review;
- temporary local branches or worktrees used to complete the task.

For the detailed authorization envelope and completion loop, read agency-protocol.md.
