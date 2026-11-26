---
name: setup
description: Set up parallel-kit after install, or check it again. Removes Parallel's own plugin if it competes, gets parallel-cli installed and signed in, fixes named agents, offers to turn on auto-update, then runs one real search.
disable-model-invocation: true
allowed-tools: Bash(claude plugin list *), Bash(command -v *), Bash(uname *), Bash(parallel-cli auth *)
---

# Set up parallel-kit

Run the five steps in order, in this session. Each step checks first and acts only on a miss, after one yes from the user (`AskUserQuestion`, one question per change). Print each step's result as `✔ <step>` or `✘ <step>: <why>`. A rerun redoes only what failed. End with the summary: one line per step.

## 1. Parallel's own plugin

Its search and extract skills and its MCP server compete with this kit's `search` and `extract`. `claude plugin list --json`, every entry whose `id` starts with `parallel@`. Ask: uninstall (`claude plugin uninstall <id>`), disable (`claude plugin disable <id>`), or keep. Kept → ✘, "sessions may use Parallel's plugin instead of this kit's".

## 2. `parallel-cli` (required)

Every search, page read and paid run uses it.

- `command -v parallel-cli`. Missing: offer to install. On macOS (`uname -s` is `Darwin`): `brew install parallel-web/tap/parallel-cli`. On Linux: `pipx install "parallel-web-tools[cli]"`, then `pipx ensurepath` (if `pipx` is missing too, say to install it with the system's package manager).
- `parallel-cli auth --json`: the field `authenticated` must be `true`. If not: a user with no Parallel account signs up first at https://platform.parallel.ai. Then hand the user `! parallel-cli login` to type; it opens a browser for device sign-in. Check again.

**If the user declines the install or the sign-in, stop setup here** with ✘, and say to run `/parallel-kit:setup` again once `parallel-cli` is installed and signed in.

## 3. Named agents

A subagent with a fixed `tools:` list can use `search` and `extract` only if that list has `Skill`. Look at every `*.md` in `~/.claude/agents/` and in the current repo's `.claude/agents/` whose frontmatter has a `tools:` line without `Skill`.

For each, show the diff and, on a yes, edit its frontmatter:

- `tools:` gains `Skill`;
- `skills:` gains `parallel-kit:search` and `parallel-kit:extract` (add the line if there is none).

None found → ✔. Say that agents in other repos need `/parallel-kit:setup` run there too.

## 4. Auto-update

Already on → ✔: the entry `tdarenkov` has `"autoUpdate": true` in `~/.claude/plugins/known_marketplaces.json`, or under `extraKnownMarketplaces` in `~/.claude/settings.json`. Otherwise offer it. On a yes, add this under `extraKnownMarketplaces` in `~/.claude/settings.json` (show the diff first; leave the rest of the file alone):

```json
"tdarenkov": {"source": {"source": "github", "repo": "tdarenkov/claude-plugins"}, "autoUpdate": true}
```

Updates then arrive in the background; they load on `/reload-plugins` or the next session. Declined → ✘, "update by hand with `claude plugin update parallel-kit@tdarenkov`".

## 5. Working check

Call the Skill tool with `parallel-kit:search` and the argument: "What is the latest released version of Claude Code? I need the version number to check that this search works." ✔ if the answer cites a source link and names a `/tmp/parallel-*.json` file. ✘ otherwise: show its reply, and point to step 2 and the troubleshooting below.

## Troubleshooting

- **`parallel-cli login` hangs:** it waits on the browser's device sign-in. Open the URL it prints by hand, or run `parallel-cli login --no-browser`.
- **The plugin is disabled:** `claude plugin list --json` shows `"enabled": false`. `claude plugin enable parallel-kit@tdarenkov`, then `/reload-plugins`.
