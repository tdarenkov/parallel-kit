# Changelog

There are no version numbers: every push to main is an update. With auto-update on it arrives by itself; otherwise `claude plugin update parallel-kit@tdarenkov` takes the latest. Entries are by date.

## 2026-11-20

- `lookup` runs on `parallel-cli`, as Parallel's own search and extract skills do, and saves every result to `/tmp/parallel-<name>.json`, so a later question reads the file instead of searching again.
- The plugin no longer ships Parallel's MCP server; setup no longer signs in to it.
- `lookup` and the router say when to use the web: first, for most factual, current-information, research, comparison, documentation and troubleshooting questions.
- "go deep" is gone: the agent picks Parallel's search mode itself.
- The router no longer shows prices, which `$0` substitution garbled; they stay in `brief/references/pricing.md`.
- Setup offers to turn on auto-update.
- First public release: the router (`parallel`), `lookup` with its `lookup-agent`, `brief` for paid runs, `setup`, and the subagent guard.
