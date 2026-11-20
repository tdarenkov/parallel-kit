---
name: parallel
description: Decide how to get something from the web, and what it costs, before you do it. Use when it is unclear whether a question needs the web, a quick lookup, or a paid Parallel run (deep research, FindAll, enrichment). For a plain lookup you already know you need, call parallel-kit:lookup directly.
argument-hint: <question>
---

# Parallel: which way to the web

Question: $ARGUMENTS

| Need | Use | Cost |
| --- | --- | --- |
| Your own knowledge or the repo answers it | Nothing: answer | free |
| Current facts, versions, prices, docs, a page's content | `parallel-kit:lookup` (Skill tool), every question and URL in one call | about $0.001–0.05 a call |
| A cited report on a broad question | Deep research: `/parallel-kit:brief` | $0.005–2.40 a run, by processor |
| Every entity matching a description (all X that Y) | FindAll: `/parallel-kit:brief` | by generator and matches |
| Web-sourced columns added to rows you have | Enrichment: `/parallel-kit:brief` | per row, by processor |

Costs are from `brief/references/pricing.md` in this plugin; `/parallel-kit:brief` shows the exact estimate before it runs anything.

- **Lookup:** write each question as what you need to know and why. Say "go deep" when it is hard or needs many sources; the lookup agent then searches in `advanced` mode and with more results.
- **Paid run:** do not start `parallel-cli research`, `findall` or `enrich` yourself. Say which of the three the question needs and run `/parallel-kit:brief`, which writes the brief, shows the cost and asks before it runs.
- **Built-ins:** WebSearch and WebFetch only when `parallel-kit:lookup` reports Parallel's MCP tools unavailable, or the user names a built-in tool. Say which case applies.

Answer from the results: lead with the answer, cite every claim with a link the results returned, never one they did not.
