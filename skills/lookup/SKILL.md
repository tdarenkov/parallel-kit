---
name: lookup
description: Every web search and every read of a known URL, from the main session or any subagent, instead of WebSearch and WebFetch. Pass every question and URL you need in one call, each with what you need to know and why; say "go deep" when a question is hard or needs many sources. Runs in its own agent with Parallel's MCP tools and returns a short cited answer, so the excerpts stay out of your context. If it reports the MCP tools unavailable, use WebSearch/WebFetch and say why.
argument-hint: <questions and URLs>
context: fork
agent: parallel-kit:lookup-agent
---

# Web lookups through Parallel

The lookups: $ARGUMENTS

1. **Paid run?** If a question needs deep research (a cited report), FindAll (every entity matching a description) or enrichment (web-sourced columns added to rows), do not attempt it: name which one, and say the main session runs `/parallel-kit:brief`.
2. **Search.** Each question: `web_search` with an `objective` (one goal, in words) and 2–3 `search_queries` of 3–6 keywords each. Never the raw question as the only query. Start all independent searches in one turn. Default: leave `mode` and `advanced_settings` out (`fast`, 10 results, $0.001 a search).
3. **Go deeper only when needed.** When the caller said "go deep", or a `fast` search came back thin or off target: search again with `mode: "advanced"` ($0.005) and, if you need more sources, `advanced_settings: {"max_results": 20}` (+$0.001 a result past 10). Rewrite the objective and queries first; a better query beats a bigger one.
4. **Read the excerpts;** they are often enough. When they are not (you need a page's argument, a table, exact text), `web_fetch` the few results worth reading, with the same `objective` and `search_queries` ($0.001 a URL). `full_content: true` only when you need the whole page.
5. **Each URL given:** `web_fetch` it, with an objective from the question.
6. **Answer** per question in a few lines. Cite every claim with a link the results returned, never one they did not. Say what you could not find and which mode you ended on. No raw excerpts. If the MCP tools are missing or a call errors, say exactly that and stop.
