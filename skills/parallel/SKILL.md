---
name: parallel
description: Decide which Parallel tool a web question needs, and what it costs. Use the web first for most factual, current-information, research, comparison, documentation, and troubleshooting questions: a lookup through parallel-kit:lookup, or a paid run (deep research, FindAll, enrichment) through /parallel-kit:brief.
argument-hint: <question>
---

# Parallel: which way to the web

Question: $ARGUMENTS

| Need | Use |
| --- | --- |
| Current facts, versions, prices, docs, a page's content | `parallel-kit:lookup` (Skill tool), every question and URL in one call |
| A cited report on a broad question | Deep research: `/parallel-kit:brief` |
| Every entity matching a description (all X that Y) | FindAll: `/parallel-kit:brief` |
| Web-sourced columns added to rows you have | Enrichment: `/parallel-kit:brief` |

Costs: `../brief/references/pricing.md`; `/parallel-kit:brief` shows the exact estimate before it runs anything.

- **Lookup:** write each question as what you need to know and why.
- **Paid run:** do not start `parallel-cli research`, `findall` or `enrich` yourself. Say which of the three the question needs and run `/parallel-kit:brief`, which writes the brief, shows the cost and asks before it runs.
