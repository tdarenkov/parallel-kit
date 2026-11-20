---
name: brief
description: Write a brief for a paid Parallel run (deep research, FindAll or enrichment), show its cost, then run it after your yes.
disable-model-invocation: true
argument-hint: <research topic, entities to find, or rows to enrich>
allowed-tools: Bash(parallel-cli:*)
---

# Parallel brief

Request: $ARGUMENTS

Pick the product and say in one line why it fits: deep research (one question, a cited report), FindAll (a list of entities the user doesn't have yet) or enrichment (columns added to rows the user has). Then follow Parallel's own text for it, read in full, with the three changes below.

- `references/parallel-deep-research.md`, `references/parallel-findall.md`, `references/parallel-data-enrichment.md`: the product's steps.
- `references/task-specify-a-task.md`, `references/task-best-practices.md`, `references/task-choose-a-processor.md`: how to write the input and pick the processor.
- `references/pricing.md`: prices, from a saved copy that may be stale.
- `references/status.md`, `references/result.md`: checking on or fetching a run later.
- **Follow-ups:** when the request builds on an earlier run, find its `interaction_id` or, for FindAll, its `findall_id` (in this conversation, or in its file in `parallel-results/`) and follow the product's reference: `--previous-interaction-id` for deep research and enrichment, `findall extend` for more FindAll matches. A follow-up is a new paid run, so it gets its own brief and the user's yes.

## Changes to Parallel's texts

1. **Show the brief, then wait.** Before any paid call, reply with the exact input Parallel will receive, the tier and its cost from `references/pricing.md`. Make the paid call only after the user says yes.
2. **Results go to `parallel-results/`** at the root of the current repo, in place of `/tmp` or `reports/` in every command.
3. **Poll in the background.** Run the poll as one Bash command with `run_in_background: true` and without `--timeout 60`; Claude Code's completion notice brings the session back to report.
