---
name: setup
description: Set up parallel-kit after install, or check it again. Removes competing Parallel servers, gets parallel-cli installed and signed in, signs in to the MCP server, fixes named agents, then runs one real lookup.
disable-model-invocation: true
allowed-tools: Bash(claude mcp list), Bash(claude mcp get *), Bash(claude plugin list *), Bash(command -v *), Bash(uname *), Bash(parallel-cli auth *)
---

# Set up parallel-kit

Run the five steps in order, in this session. Each step checks first and acts only on a miss, after one yes from the user (`AskUserQuestion`, one question per change). Print each step's result as `✔ <step>` or `✘ <step>: <why>`. A rerun redoes only what failed. End with the summary: one line per step.

## 1. Competing servers

The plugin's server is `plugin:parallel-kit:parallel`. Any other server on `mcp.parallel.ai` at user, local or project scope wins over it, and then the plugin's tools resolve to nothing.

- `claude mcp list`: every line whose URL contains `mcp.parallel.ai` and whose name is not `plugin:parallel-kit:parallel` is a competitor. `claude mcp get <name>` shows its scope. On a yes: `claude mcp remove <name> -s <scope>`.
- Project files: every `.mcp.json` from the current folder up to `/` that mentions `mcp.parallel.ai`. Claude Code reads them from parent folders too. On a yes, remove that entry from the file (show the diff first); leave its other servers alone.
- Parallel's own plugin: `claude plugin list --json`, every entry whose `id` starts with `parallel@`. Ask: uninstall (`claude plugin uninstall <id>`), disable (`claude plugin disable <id>`), or keep.

A competitor kept → ✘, "the plugin's tools won't resolve while it stays".

## 2. `parallel-cli` (required)

Paid runs (`/parallel-kit:brief`) use it.

- `command -v parallel-cli`. Missing: offer to install. On macOS (`uname -s` is `Darwin`): `brew install parallel-web/tap/parallel-cli`. On Linux: `pipx install "parallel-web-tools[cli]"`, then `pipx ensurepath` (if `pipx` is missing too, say to install it with the system's package manager).
- `parallel-cli auth --json`: the field `authenticated` must be `true`. If not: a user with no Parallel account signs up first at https://platform.parallel.ai. Then hand the user `! parallel-cli login` to type; it opens a browser for device sign-in. Check again.

**If the user declines the install or the sign-in, stop setup here** with ✘, and say to run `/parallel-kit:setup` again once `parallel-cli` is installed and signed in.

## 3. MCP sign-in

`claude mcp list`: the line for `plugin:parallel-kit:parallel` says `✔ Connected` → ✔. Otherwise tell the user to run `/mcp`, select `plugin:parallel-kit:parallel`, and sign in with their Parallel account in the browser (over SSH, see troubleshooting); then go on. Step 5 proves it.

## 4. Named agents

A subagent with a fixed `tools:` list can use the lookup only if that list has `Skill` and both plugin tools. Look at every `*.md` in `~/.claude/agents/` and in the current repo's `.claude/agents/` whose frontmatter has a `tools:` line without `mcp__plugin_parallel-kit_parallel__web_search`.

For each, show the diff and, on a yes, edit its frontmatter:

- `tools:` gains `Skill`, `mcp__plugin_parallel-kit_parallel__web_search` and `mcp__plugin_parallel-kit_parallel__web_fetch` (those it lacks);
- `skills:` gains `parallel-kit:lookup` (add the line if there is none).

None found → ✔. Say that agents in other repos need `/parallel-kit:setup` run there too.

## 5. Working check

Call the Skill tool with `parallel-kit:lookup` and the argument: "What is the latest released version of Claude Code? I need the version number to check that this lookup works." ✔ if the answer cites a source link. ✘ otherwise: show its reply, and point to `/mcp` (step 3) and the troubleshooting below.

## Troubleshooting

- **A duplicate `parallel` server:** a user, local or project server on `mcp.parallel.ai` hides the plugin's. Step 1 finds it; `claude mcp list` shows it.
- **`parallel-cli login` hangs:** it waits on the browser's device sign-in. Open the URL it prints by hand, or run `parallel-cli login --no-browser`.
- **The plugin is disabled:** `claude plugin list --json` shows `"enabled": false`. `claude plugin enable parallel-kit@tdarenkov`, then `/reload-plugins`.
- **The MCP sign-in can't reach the browser, or its redirect fails** (over SSH, or a callback error in the browser): run `! claude mcp login plugin:parallel-kit:parallel --no-browser`, open the URL it prints, and paste the redirect URL back when it asks.
