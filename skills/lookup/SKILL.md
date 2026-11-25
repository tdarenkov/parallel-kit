---
name: lookup
description: Search the web or read a web page with Parallel. Use it first for any fact from outside this repo: factual, current-information, research, comparison, documentation and troubleshooting questions, how others solve a problem like yours, APIs, papers, prices, versions and other people's code; and for every read of a known URL, from the main session or any subagent, instead of WebSearch, WebFetch, the web-fetch agent or curl. When you hand research to a subagent, tell it to use this skill. It runs as its own agent and returns the answer: in the args, describe the goal in a concise, standalone sentence that names the key topic, with any URLs. One question per call; for several questions, make several calls. Results are saved in /tmp/parallel-<name>.json. Read them before you search for the same thing again.
argument-hint: <query or URLs>
context: fork
agent: parallel-kit:lookup-agent
allowed-tools: Bash(parallel-cli:*)
---

# Web lookup

Look up: $ARGUMENTS

Search for each question. Extract each URL given, and a search result only when its excerpts are not enough: you need exact wording or quotes, full-page analysis, or the excerpts conflict.

Choose a short, descriptive filename for each call (e.g., `react-19-features`), lowercase with hyphens. Substitute it inline: `<name>`, `<keyword>` and `<url>` are placeholders, not shell variables.

## Search

```bash
parallel-cli search "<objective>" -q "<keyword1>" -q "<keyword2>" --max-results 10 --excerpt-max-chars-total 27000 -o "/tmp/parallel-<name>.json"
```

The first argument is the objective: a natural language description of what you're looking for. Add `-q` flags for specific keyword queries. Options if needed:

- `--after-date YYYY-MM-DD` for time-sensitive queries
- `--include-domains a.com,b.com` or `--exclude-domains c.com`
- `--mode advanced` for harder questions (multi-step, agentic search). Keep the default `basic` unless the request needs another mode.

## Extract

```bash
parallel-cli extract "<url1>" "<url2>" --objective "<focus>" -o "/tmp/parallel-<name>.json"
```

Each URL is its own quoted argument, up to 20 per call. For the whole page, extract one URL per call and add `--full-content --full-content-max-chars 100000`. If it is cut off, say so and give the file path.

## Read

Read the saved `-o` JSON file as the authoritative payload: the command prints only a short index. Read each file to its end before you answer, 20,000 characters at a time: start at offset 1 and add 20000 until a part comes back short.

```bash
jq -r '.results[] | "## " + .url, (.excerpts // [] | join("\n\n")), (.full_content // "")' "/tmp/parallel-<name>.json" | tail -c +<offset> | head -c 20000
```

## Response

Check the exit status, API error, `warnings` and per-URL `errors`. On an error or empty results, say what happened. Do not fabricate an answer. For sparse results, state the coverage limits; refine the objective or queries only when useful for the user's request.

- Search: lead with the answer. Cite every claim inline as [Title](URL), only from the saved results. Never invent URLs.
- Extract: keep content verbatim. Strip only menus, footers and ads. For long content, give a labelled preview.
- End with a Sources list, then the path of each saved file.

If `parallel-cli` is missing or not signed in, say so and point to `/parallel-kit:setup`.
