# Decision and approval questions

Use an interactive question tool when the host provides one. If it does not, present the same structure as a short lettered choice and wait for the answer. Do not claim that a text prompt was an interactive tool call.

## Before asking

1. Read the repository, project docs, and current sources that can answer factual parts of the question.
2. State the facts already established and cite or locate the evidence.
3. Isolate the remaining decision that requires the user's intent, preference, priority, or risk tolerance.

Do not ask “what should we do?” without analysis. Do not ask for framework, database, directory, API, or test facts that the repository can reveal.

## Shape of a good question

Each meaningful question contains:

- the decision in one sentence;
- the recommended option first;
- two to four options when real alternatives exist;
- a short description of the downstream trade-off for each option;
- an `Other` path when the host supplies one or the user may need a custom answer.

Use a normal ask for up to three tightly coupled scope questions. In Grill mode, ask one core decision at a time unless several answers are inseparable.

Example shape:

```text
已确认：现有 mutation 路径有两个入口，测试只覆盖其中一个。
真正需要决定的是：Registry 是否继续作为唯一 mutation gateway？

A. 继续使用 Registry（Recommended）
   共享审计和权限边界，代价是迁移第二个入口。
B. 保留 Service 直调
   路径更短，但会继续维护两套边界。
C. 迁移期间暂时双写
   降低切换风险，但增加状态不一致和清理成本。
```

## Gates

Use an approval question before substantial implementation when the scope is not already explicitly authorized. A useful scope approval names the goal, in-scope files or surfaces, non-goals, constraints, and checks that will prove completion.

After approval, continue through routine work without asking after each file, command, or test. Reopen the gate only for the events listed in the main skill. A final question is needed only when a real human decision remains, such as publishing, a destructive action, or an unresolved trade-off.
