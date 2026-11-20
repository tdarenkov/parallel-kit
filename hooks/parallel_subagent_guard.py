"""PreToolUse guard for Bash: a subagent may search and extract with Parallel, nothing that spends.

`parallel-cli` is logged in machine-wide, so any subagent could start a paid run (research, findall, enrich, monitor).
A hook input that carries agent_id is a subagent; the main session is never blocked. In command position a subagent
may run only: search (any mode), extract, fetch, auth, --help, --version. Everything else, including any subcommand
Parallel adds later, is refused. Quoted text (a grep, a commit message) is not a call; `bash -c '...'` scripts are
checked. Shell keywords and wrappers (then, do, time, nohup, env, sudo, {) before the CLI count as command position.
Best effort, not airtight: `xargs`, `eval` and variables get past it.
"""
from __future__ import annotations

import json
import re
import sys

ALLOWED = {"search", "extract", "fetch", "auth", "--help", "--version"}
# Command position: line start, after ; | & ( ` { or `--`, then any shell keyword or wrapper (then, do, time, sudo -u x)
# and VAR=x assignments; the CLI may be a path.
WRAP = r"(?:(?:then|do|else|elif|time|nohup|env|sudo|command|exec|builtin)\s+(?:-\S+\s+(?:\w+\s+)?)*)"
CALL = re.compile(
    r"(?m)(?:^\s*|[;|&(`{]\s*|\s--\s+)(?:" + WRAP + r"|\w+=\S*\s+)*"
    r"(?:[\w./~-]*/)?parallel-cli(?=$|[\s;|&)])(?:\s+([^\s;|&)]*))?"
)
QUOTED = re.compile(r"'([^']*)'|\"([^\"]*)\"")
SCRIPT = re.compile(r"\s-c\s+(?:'([^']*)'|\"([^\"]*)\")")   # bash -c '...': the script is commands too


def refused_subcommand(text: str) -> str | None:
    """The first parallel-cli subcommand in `text` not on the allow-list ('' when none is given), else None."""
    for m in CALL.finditer(QUOTED.sub(" ", text)):
        sub = m.group(1) or ""
        if sub not in ALLOWED:
            return sub
    return None


def decide(payload: dict) -> str | None:
    """The deny reason, or None to allow."""
    if not payload.get("agent_id") or payload.get("tool_name") != "Bash":
        return None
    raw = str((payload.get("tool_input") or {}).get("command") or "")
    hit = refused_subcommand(raw)
    for a, b in SCRIPT.findall(raw):
        if hit is None:
            hit = refused_subcommand(a or b)
    if hit is None:
        return None
    what = f"`parallel-cli {hit}`" if hit else "bare `parallel-cli`"
    return (f"{what} is refused for subagents: it can spend. A subagent may run only "
            f"{', '.join(sorted(ALLOWED))}; ask the main session for anything else.")


def main() -> None:
    reason = decide(json.load(sys.stdin))
    if reason:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse", "permissionDecision": "deny",
            "permissionDecisionReason": f"[parallel_subagent_guard] {reason}"}}))


if __name__ == "__main__":
    main()
