import os

# The override switch (04_architecture.md, 06_07 §4): three positions, read from the environment.
#   ON           -> pre-read + draft, the agent may insert and send the draft (L2)
#   SUGGEST_ONLY -> pre-read + draft stay visible, but the draft cannot be inserted or sent (L1)
#   OFF          -> no pre-read, no draft: the ticket works exactly as today
MODE_ON = "ON"
MODE_SUGGEST_ONLY = "SUGGEST_ONLY"
MODE_OFF = "OFF"
VALID_MODES = (MODE_ON, MODE_SUGGEST_ONLY, MODE_OFF)

# Where the audit log is written (one JSON line per output, governance.md Session 8).
AUDIT_LOG_PATH = os.path.join(os.path.dirname(__file__), "logs", "audit_log.jsonl")


def get_copilot_mode() -> str:
    """Return the current switch position; an unknown value falls back to OFF (fail safe)."""
    mode = os.environ.get("COPILOT_MODE", MODE_ON).strip().upper()
    if mode not in VALID_MODES:
        return MODE_OFF
    return mode
