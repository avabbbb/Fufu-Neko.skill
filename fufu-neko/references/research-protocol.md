# Reality sync protocol

Use this protocol whenever an answer depends on a current product, version, API, library, framework, model, price, license, standard, company, repository state, or ecosystem practice. Use a lighter pass for a small current fact and the full sequence for architecture, product direction, migration, purchase, or release decisions.

## Freshness and scope

1. Read the current date from the host session or environment. Do not turn a date in a prompt, example, or old document into a permanent rule.
2. State the research question and why freshness matters internally before searching.
3. Separate facts about the user's repository from facts about the outside world.
4. Treat model memory as a hypothesis. If current sources disagree with memory, current sources win.

## Source sequence

Follow the narrowest sequence that answers the question:

1. **Official truth:** current documentation, reference material, release notes, changelogs, official repositories, pricing, or license terms.
2. **Real code:** maintained repositories, examples, tests, adapters, and recent implementation patterns.
3. **Ecosystem signal:** issue activity, discussions, comparisons, and production reports that reveal operational pain or adoption. Use these as signals, not authority.
4. **Contradiction check:** compare dates, versions, claims, and implementation behavior. Do not call a single search result complete research.

For an important choice, corroborate the decisive claim with at least two independent sources, ideally an official source and a maintained implementation. Check a source's date and scope before using it.

## What to inspect

- Whether the project or product is active and what release line is current;
- the official recommendation and its migration or deprecation notes;
- real integration shape, tests, failure handling, and maintenance signals;
- licensing, commercial use, privacy, hosting, lock-in, cost, latency, and operational burden when relevant;
- the conditions under which the recommendation would change.

Do not copy long source passages into the response or into this skill. Extract the decision-relevant facts and cite the source near the claim when the host supports citations.

## Output labels

Use these labels when reporting research:

- **Verified:** directly supported by a current authoritative source or an executed local check.
- **Observed:** seen in a real repository, implementation, issue, or project artifact; scope it precisely.
- **Inferred:** a reasoned conclusion from verified or observed evidence.
- **Recommended:** Fufu's judgment, including the trade-off it accepts.
- **Unknown:** material information that remains unverified or unavailable.

Keep recommendation language separate from source language. State dates when they change the meaning of a fact. If browsing is unavailable, say current verification is blocked and mark the recommendation provisional; do not silently fall back to memory.
