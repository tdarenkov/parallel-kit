# Changelog

There are no version numbers: every push to main is an update. With auto-update on it arrives by itself; otherwise `claude plugin update parallel-kit@tdarenkov` takes the latest. Entries are by date.

## 2026-11-26

- `lookup` is now two skills, `search` and `extract`, as Parallel ships them. A search answers from excerpts, and your session decides which pages to read in full with `extract`, instead of the agent deciding for it.
- The router has your session pick the search mode: `basic` for a fact about a named thing, `advanced` for how to solve a problem like yours.
- The question a session gets when a search or page read reports back now also follows one that ran in the foreground, because an earlier call was still running.
- Named agents set up before this need `/parallel-kit:setup` run again, so their `skills:` list names `search` and `extract`.

## 2026-11-25

- Before a session's first lookup, and every few lookups after, a hook has it read the router, which now says how to shape a question: a fact about a named thing as it is, several things split apart, and how to solve a problem stepped back to the general problem as well.
- `lookup` asks for the goal the way Parallel's docs do: a concise, standalone sentence that names the key topic.
- When a lookup reports back, a hook asks the session whether the report answers the question or rests on pages read only in excerpts, so it sends those pages back to be read in full before answering.
- Sessions and subagents reach for `lookup` for any fact from outside the repo, including how others solve a problem like yours, instead of WebSearch, WebFetch, the web-fetch agent or curl. Each call carries one question and its URLs.
- `lookup` reads its saved results to the end instead of a cut-off printout, and reads whole pages up to 100,000 characters.

## 2026-11-21

- The router's pointer to the price list resolves, and it no longer repeats `lookup`'s answer rules.

## 2026-11-20

- `lookup` runs on `parallel-cli`, as Parallel's own search and extract skills do, and saves every result to `/tmp/parallel-<name>.json`, so a later question reads the file instead of searching again.
- The plugin no longer ships Parallel's MCP server; setup no longer signs in to it.
- `lookup` and the router say when to use the web: first, for most factual, current-information, research, comparison, documentation and troubleshooting questions.
- "go deep" is gone: the agent picks Parallel's search mode itself.
- The router no longer shows prices, which `$0` substitution garbled; they stay in `brief/references/pricing.md`.
- Setup offers to turn on auto-update.
- First public release: the router (`parallel`), `lookup` with its `lookup-agent`, `brief` for paid runs, `setup`, and the subagent guard.
