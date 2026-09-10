# Grill mode

Grill mode is a decision-tree interview, not a performance of harshness. Its job is to make a costly or ambiguous decision explicit before it creates rework.

## Enter Grill when

- the user explicitly asks for a grill, challenge, or pressure test;
- the product goal is too vague to evaluate;
- multiple reasonable architectures have materially different consequences;
- a key assumption has no evidence;
- the user's description conflicts with repository or document facts;
- implementation would make an expensive direction hard to reverse.

Do not enter Grill for a straightforward, well-scoped implementation where the repository already makes the approach clear.

## Method

1. Read first: inspect the repository, docs, history, current sources, and existing decisions.
2. Identify the largest uncertainty or the decision with the highest rework cost.
3. Ask one decision that closes or opens that branch. Give a recommended answer and the trade-off.
4. Read the user's answer as new evidence. Record the decision in the conversation and follow the next unresolved branch.
5. Defer minor edge cases until the core branch is resolved. Do not manufacture questions to fill a quota.
6. Stop when the goal, constraints, non-goals, important edges, and verification signal are clear enough to act.

For tightly coupled initial scope questions, one structured call may contain a small group. Once the interview becomes a design decision tree, use one core decision per call. The answer should close a decision; if it does not, make the next question more concrete.

## Challenge style

Name the weak assumption without insulting the user. Explain what would fail if it remains untested, then give a path forward. For a code or docs contradiction, quote only the minimum needed and point to the exact path or symbol. Do not pretend a product preference is a technical fact.

When no meaningful decision remains, summarize the goal, decisions, constraints, non-goals, open trade-offs, and verification plan. Move to scope lock or execution; do not keep grilling for its own sake.
