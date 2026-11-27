"""Rollback drill: move the override switch ON -> SUGGEST_ONLY -> OFF and check what the agent sees.

Usage (from the repository root):  python prototype/test_switch.py
The drill uses an invented ticket (not from the eval-set) and prints a dated PASS/FAIL line
that goes into 06_07 §4 and governance.md ("last tested").
"""
import os
import sys
import time
from datetime import date

from config import MODE_OFF, MODE_ON, MODE_SUGGEST_ONLY, get_copilot_mode
from pipeline import process_ticket
from router import TicketRouter

DRILL_LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "switch_drill_log.jsonl")
DRILL_TICKET = ('Ticket of 9 Nov · form fields: ref TX-10001, amount €500.00, date 2 Nov · message: "Where is this payment?" · '
                'account M-0001: TX-10001 €500.00 received 2 Nov, paid out 4 Nov in transfer VO-1001 to account •• 1234 · no open flag')

# What each switch position must give the agent.
EXPECTED = {
    MODE_ON: {"outcome": "draft", "send_enabled": True},
    MODE_SUGGEST_ONLY: {"outcome": "draft", "send_enabled": False},
    MODE_OFF: {"outcome": "copilot_off", "send_enabled": False},
}


def check_position(mode: str, router) -> bool:
    """Set the switch through the environment, as the on-call person would, and check the panel."""
    os.environ["COPILOT_MODE"] = mode
    result = process_ticket("DRILL-1", DRILL_TICKET, router, mode=get_copilot_mode(), log_path=DRILL_LOG_PATH)
    expected = EXPECTED[mode]
    passed = result["outcome"] == expected["outcome"] and result["send_enabled"] == expected["send_enabled"]
    status = "PASS" if passed else "FAIL"
    print(f"{status}  COPILOT_MODE={mode:<13} outcome={result['outcome']:<12} send_enabled={result['send_enabled']}")
    return passed


def main():
    router = TicketRouter()
    started = time.perf_counter()
    results = [check_position(mode, router) for mode in (MODE_ON, MODE_SUGGEST_ONLY, MODE_OFF)]
    # An unknown value must fail safe to OFF, whether it comes from the environment or is passed directly.
    os.environ["COPILOT_MODE"] = "typo"
    from_environment = get_copilot_mode() == MODE_OFF
    passed_directly = process_ticket("DRILL-2", DRILL_TICKET, router, mode="typo",
                                     log_path=DRILL_LOG_PATH)["outcome"] == "copilot_off"
    fail_safe = from_environment and passed_directly
    print(f"{'PASS' if fail_safe else 'FAIL'}  unknown value 'typo' falls back to OFF (environment and direct call)")
    elapsed = time.perf_counter() - started
    all_passed = all(results) and fail_safe
    print(f"\nRollback drill {date.today().isoformat()}: {'PASS' if all_passed else 'FAIL'} "
          f"in {elapsed:.1f} s (ON -> SUGGEST_ONLY -> OFF)")
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
