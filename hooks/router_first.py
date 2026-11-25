"""PreToolUse (Skill): a lookup waits for the router once per subagent, and in the main session once, then again every 4 lookups."""
import json
import os
import re
import sys
import tempfile

LOOKUP = re.compile(r"^(parallel-kit:)?lookup$")
ROUTER = re.compile(r"^(parallel-kit:)?parallel$")
EVERY = 4
REASON = ("Before this lookup, invoke parallel-kit:parallel (Skill tool) with the question, "
          "then send the lookup again, written the way it says.")


def state_path(event):
    who = f"{event.get('session_id', '')}-{event.get('agent_id') or 'main'}"
    return os.path.join(tempfile.gettempdir(), "parallel-kit-router-" + re.sub(r"[^\w-]", "_", who))


def decide(event):
    """Return the deny reason, or None to let the call through."""
    skill = (event.get("tool_input") or {}).get("skill", "")
    path = state_path(event)
    if ROUTER.match(skill):
        open(path, "w").write("0")
        return None
    if not LOOKUP.match(skill):
        return None
    if not os.path.exists(path):
        return REASON
    count = int(open(path).read() or 0)
    if not event.get("agent_id") and count >= EVERY:
        return REASON
    open(path, "w").write(str(count + 1))
    return None


def main():
    try:
        event = json.load(sys.stdin)
    except ValueError:
        return
    reason = decide(event)
    if reason:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                                 "permissionDecision": "deny",
                                                 "permissionDecisionReason": reason}}))


if __name__ == "__main__":
    main()
