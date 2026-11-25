"""UserPromptSubmit: when a background parallel-kit:lookup reports back, ask the main session whether the report is enough before it answers."""
import json
import re
import sys

LOOKUP_REPORT = re.compile(r"<task-notification>.*?<summary>[^<]*parallel-kit:lookup", re.S)
NUDGE = (
    "Before you answer from this lookup: does it answer the question, or does your answer rest on pages "
    "it read only in excerpts? If so, send those URLs back to parallel-kit:lookup to read them in full."
)


def context_for(prompt):
    return NUDGE if LOOKUP_REPORT.search(prompt or "") else None


def main():
    try:
        prompt = json.load(sys.stdin).get("prompt", "")
    except ValueError:
        return
    text = context_for(prompt)
    if text:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": text}}))


if __name__ == "__main__":
    main()
