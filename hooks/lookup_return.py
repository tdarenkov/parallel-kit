"""When a parallel-kit search or extract reports back, ask the main session whether the report is enough before it answers.

A background call reports as a task notification (UserPromptSubmit). One that runs in the
foreground, because an earlier one is still running, returns as the Skill tool's result (PostToolUse).
"""
import json
import re
import sys

LOOKUP_REPORT = re.compile(r"<task-notification>.*?<summary>[^<]*parallel-kit:(search|extract)", re.S)
LOOKUP = re.compile(r"^(parallel-kit:)?(search|extract)$")
NUDGE = (
    "Before you answer from this: does it answer the question, or does your answer rest on pages read "
    "only in excerpts? If so, send those URLs to parallel-kit:extract to read them in full."
)


def context_for(event):
    """The question to add, or None."""
    if event.get("hook_event_name") == "PostToolUse":
        skill = (event.get("tool_input") or {}).get("skill", "")
        response = event.get("tool_response")
        launched = isinstance(response, dict) and response.get("background") is True
        return NUDGE if LOOKUP.match(skill) and not launched else None
    return NUDGE if LOOKUP_REPORT.search(event.get("prompt") or "") else None


def main():
    try:
        event = json.load(sys.stdin)
    except ValueError:
        return
    text = context_for(event)
    if text:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": event.get("hook_event_name", "UserPromptSubmit"),
                                                 "additionalContext": text}}))


if __name__ == "__main__":
    main()
