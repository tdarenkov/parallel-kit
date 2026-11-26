---
name: extract
description: Read web pages in full with Parallel. Use it for every read of a known URL, and for a search result when its excerpts are not enough: you need exact wording or quotes, the whole page, or the excerpts conflict or leave the question open. From the main session or any subagent, instead of WebFetch, the web-fetch agent or curl. It runs as its own agent: in the args, give the URLs and what you need from them. Results are saved in /tmp/parallel-<name>.json.
argument-hint: <url> [url2] [url3] <what you need>
context: fork
agent: parallel-kit:lookup-agent
allowed-tools: Bash(parallel-cli:*)
---

# URL Extraction

Extract content from: $ARGUMENTS

## Command

Choose a short, descriptive filename based on the URL or content (e.g., `vespa-docs`, `react-hooks-api`). Use lowercase with hyphens, no spaces. Substitute it into the command **inline**: `<name>` is a placeholder, not a shell variable.

Pass each requested URL as a separate quoted positional argument, up to 20 per call. For the whole page, extract one URL per call and add `--full-content --full-content-max-chars 100000`:

```bash
parallel-cli extract "<url>" --objective "<what is needed>" --full-content --full-content-max-chars 100000 -o "/tmp/parallel-<name>.json"
```

Options if needed:

- `--objective "focus area"` to focus extraction on a specific goal
- `-q "keyword"` (repeatable) to prioritize keywords in excerpts
- `--no-excerpts` to strip excerpts when you only want full content

## Read

**Read the saved `-o` JSON file as the authoritative payload**: the command prints only a short index. Read it to its end before you answer, 20,000 characters at a time: start at offset 1 and add 20000 until a part comes back short.

```bash
jq -r '.results[] | "## " + .url, (.excerpts // [] | join("\n\n")), (.full_content // "")' "/tmp/parallel-<name>.json" | tail -c +<offset> | head -c 20000
```

## Handling failed extractions

Inspect the exit status, API error, `results`, per-URL `errors` and any warnings. `errors: []` is normal success. Nonempty errors can coexist with successful results: present the successful content, then name each failed URL and its returned reason. Empty results or missing content are not a successful extraction. Do not fabricate content. If a page is cut off at the cap, say so.

## Response format

Return content as **[Page Title](URL)**, answering what was asked from the full page. Quote exact wording where it matters, and keep facts, names, numbers, dates and quotes as the page has them. Strip only obvious noise: nav menus, footers, ads.

After the response, mention the output file path (`/tmp/parallel-<name>.json`).

If `parallel-cli` is missing or not signed in, say so and point to `/parallel-kit:setup`.
