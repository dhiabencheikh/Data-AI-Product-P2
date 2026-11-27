import json
import os
from datetime import datetime, timezone

from config import AUDIT_LOG_PATH, MODE_OFF, MODE_ON, VALID_MODES, get_copilot_mode
from drafter import retrieve_and_draft
from policy import check_policy
from reader import extract_clues, split_ticket
from routing_rule import apply_routing_rule

# The four steps of 04_architecture.md, chained, behind the override switch:
#   router -> routing rule -> lookup + draft -> policy check -> shown to the agent (who alone sends)


def write_audit_line(record: dict, log_path: str = AUDIT_LOG_PATH) -> None:
    """Append one JSON line per output to the audit log (who, what, when, which switch position)."""
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")


def summarise_match(match) -> dict:
    """The part of a lookup kept in the log: status, transaction, evidence, candidates ruled out."""
    if not match:
        return None
    row = match.get("row") or {}
    return {
        "status": match.get("status"),
        "transaction_id": row.get("id"),
        "evidence": match.get("evidence", []),
        "ruled_out": match.get("ruled_out", []),
    }


def process_ticket(ticket_id: str, ticket_text: str, router, mode: str = None, log_path: str = AUDIT_LOG_PATH) -> dict:
    """
    Run one ticket through the copilot and return what the agent's panel would show:
      outcome      : "draft" | "no_draft" | "blocked" (the policy check stopped the draft) | "copilot_off"
      send_enabled : True only in ON mode, and only when a policy-checked draft exists
    The copilot never sends: send_enabled only means the agent may insert the draft and send it.
    """
    mode = mode or get_copilot_mode()
    if mode not in VALID_MODES:
        # Fail safe, as in config.get_copilot_mode(): an unknown switch position means OFF.
        mode = MODE_OFF
    result = {"ticket_id": ticket_id, "mode": mode, "outcome": "no_draft", "send_enabled": False,
              "draft": None, "blocked_draft": None, "match": None, "citations": [], "flags": [], "reason": "",
              "route": None}

    if mode == MODE_OFF:
        result.update(outcome="copilot_off", reason="Switch OFF: no pre-read, the ticket works as today.")
        write_audit_line(build_audit_record(result), log_path)
        return result

    ticket = split_ticket(ticket_text)
    clues = extract_clues(ticket)
    # The router reads only what the merchant wrote, never the ledger rows (spec.md v2, CHANGE-4).
    merchant_words = ticket["message"] or ticket["form_fields"] or ticket["merchant_text"]

    # Step 1 · router, then Step 2 · routing rule
    route = router.predict(merchant_words)
    gate = apply_routing_rule(route, ticket, clues)
    result["route"] = route
    result["merchant_id"] = ticket["merchant_id"]

    if gate["action"] == "escalate":
        result["reason"] = gate["reason"]
        write_audit_line(build_audit_record(result), log_path)
        return result

    # Step 3 · lookup + draft, on this merchant's account only
    draft_result = retrieve_and_draft(ticket, clues, route["category"])
    result["flags"] = draft_result.get("flags", [])
    result["match"] = summarise_match(draft_result.get("match"))
    if draft_result["status"] != "drafted":
        result["reason"] = draft_result["reason"]
        write_audit_line(build_audit_record(result), log_path)
        return result

    # Step 4 · policy check
    verdict = check_policy(draft_result, ticket["account_context"])
    if verdict["policy"] == "block":
        # Never shown to the agent, but kept in the log for the weekly review of blocked drafts (governance.md).
        result.update(outcome="blocked", reason=verdict["reason"], blocked_draft=draft_result["draft"])
        write_audit_line(build_audit_record(result), log_path)
        return result

    result.update(outcome="draft", draft=draft_result["draft"], citations=draft_result["citations"],
                  evidence=draft_result.get("evidence", []), agent_notes=draft_result.get("agent_notes", []),
                  reason=verdict["reason"],
                  send_enabled=(mode == MODE_ON))
    write_audit_line(build_audit_record(result), log_path)
    return result


def build_audit_record(result: dict) -> dict:
    """The fields kept in the audit log (spec.md io_contracts: log), plus the switch position and the route."""
    return {
        "logged_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "ticket_id": result["ticket_id"],
        "merchant_id": result.get("merchant_id"),
        "mode": result["mode"],
        "route": result["route"],
        "outcome": result["outcome"],
        "match": result["match"],
        "citations": result["citations"],
        "flags": result["flags"],
        "reason": result["reason"],
        "send_enabled": result["send_enabled"],
        "draft": result["draft"],
        "blocked_draft": result["blocked_draft"],
        # Filled by the agent's ticket tool once a person acts on the draft:
        "edits": None,
        "sent_by": None,
        "sent_at": None,
    }


if __name__ == "__main__":
    from router import TicketRouter

    sample = ('Ticket of 6 Nov · form fields: ref TX-10001, amount €500.00, date 2 Nov · message: "Where is this payment?" · '
              'account M-0001: TX-10001 €500.00 received 2 Nov, paid out 4 Nov in transfer VO-1001 to account •• 1234 · no open flag')
    outcome = process_ticket("DEMO-1", sample, TicketRouter(), mode=MODE_ON)
    print(json.dumps(outcome, ensure_ascii=False, indent=2, default=str))
