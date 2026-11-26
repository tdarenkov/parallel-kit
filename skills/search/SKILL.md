---
name: search
description: Search the web with Parallel. Use it first for any fact from outside this repo: factual, current-information, research, comparison, documentation and troubleshooting questions, how others solve a problem like yours, APIs, papers, prices, versions and other people's code, from the main session or any subagent, instead of WebSearch, the web-fetch agent or curl. When you hand research to a subagent, tell it to use this skill. It runs as its own agent and returns cited excerpts: in the args, describe the goal in a concise, standalone sentence that names the key topic. One question per call; for several questions, make several calls. To read a result in full, use parallel-kit:extract. Results are saved in /tmp/parallel-<name>.json. Read them before you search for the same thing again.
argument-hint: <goal>
context: fork
agent: parallel-kit:lookup-agent
allowed-tools: Bash(parallel-cli:*)
---

# Web Search

Search the web for: $ARGUMENTS

## Command

Choose a short, descriptive filename based on the query (e.g., `ai-chip-news`, `react-vs-vue`). Use lowercase with hyphens, no spaces. Substitute it into the command **inline**: `<name>` and `<keyword>` below are placeholders, not shell variables; do not copy them verbatim.

```bash
parallel-cli search "<objective>" -q "<keyword1>" -q "<keyword2>" --max-results 10 --excerpt-max-chars-total 27000 -o "/tmp/parallel-<name>.json"
```

The first argument is the **objective**: a natural language description of what you're looking for. Add `-q` flags for specific keyword queries to supplement the objective. The `-o` flag saves the full results to a JSON file for follow-up questions.

Options if needed:

- `--after-date YYYY-MM-DD` for time-sensitive queries
- `--include-domains domain1.com,domain2.com` to limit to specific sources
- `--exclude-domains domain.com` to filter out noisy sources
- `--mode advanced` for harder questions (multi-step, agentic search). Use the mode the request names; otherwise keep the default `basic`.

## Parsing results

**Read the saved `-o` JSON file as the authoritative payload**: the command prints only a short index. Read it to its end before you answer, 20,000 characters at a time: start at offset 1 and add 20000 until a part comes back short.

```bash
jq -r '.results[] | "## " + .url, (.excerpts // [] | join("\n\n"))' "/tmp/parallel-<name>.json" | tail -c +<offset> | head -c 20000
```

For each result, extract:

- title, url, and publish_date if provided; omit unknown dates
- Useful content from excerpts (skip navigation noise like menus, footers, "Skip to content")

Check the exit status, returned API error and `warnings` before presenting results. On an error or empty `results`, report what happened and do not fabricate an answer. For sparse results, state the coverage limits; refine the objective or queries only when useful for the user's request.

## Response format

**CRITICAL: Every claim must have an inline citation.** Use markdown links like [Title](URL) pulling only from the saved results. Never invent or guess URLs.

Synthesize a response that:

- Leads with the key answer/finding
- Includes specific facts, names, numbers, dates
- Cites every fact inline as [Source Title](url)
- Organizes by theme if multiple topics
- Says that it rests on search excerpts

**End with a Sources section** listing every URL referenced, then the output file path (`/tmp/parallel-<name>.json`).

If `parallel-cli` is missing or not signed in, say so and point to `/parallel-kit:setup`.
