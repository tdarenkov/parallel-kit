---
name: parallel
description: Decide which Parallel tool a web question needs, and what it costs. Use the web first for most factual, current-information, research, comparison, documentation, and troubleshooting questions: a search through parallel-kit:search, a page read through parallel-kit:extract, or a paid run (deep research, FindAll, enrichment) through /parallel-kit:brief.
argument-hint: <question>
---

# Parallel: which way to the web

Question: $ARGUMENTS

| Need | Use |
| --- | --- |
| Current facts, versions, prices, docs, how others do something | `parallel-kit:search` (Skill tool), one call per question |
| A page's content: a known URL, or a search result whose excerpts are not enough | `parallel-kit:extract` (Skill tool), with the URLs and what you need from them |
| A cited report on a broad question | Deep research: `/parallel-kit:brief` |
| Every entity matching a description (all X that Y) | FindAll: `/parallel-kit:brief` |
| Web-sourced columns added to rows you have | Enrichment: `/parallel-kit:brief` |

Costs: `../brief/references/pricing.md`; `/parallel-kit:brief` shows the exact estimate before it runs anything.

- **Searches:** one goal per call, a concise, standalone sentence that names the key topic. Shape it by the question:
  - A fact about a named thing: ask it as it is, in `basic` mode.
  - Several things at once: split them into questions that can each be answered alone.
  - How to solve your problem: step back to the general problem it is a case of, and ask that too. Ask for `advanced` mode: Parallel's mode for harder, multi-step questions.
- **After a search:** its answer rests on excerpts. Send the pages your answer or decision rests on to `parallel-kit:extract`, then search again with what they turned up.
- **Paid run:** do not start `parallel-cli research`, `findall` or `enrich` yourself. Say which of the three the question needs and run `/parallel-kit:brief`, which writes the brief, shows the cost and asks before it runs.
