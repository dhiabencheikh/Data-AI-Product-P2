import re

# Step 2 · Routing rule (rung 1: deterministic rules from spec.md).
# Decides whether the copilot may go on to the lookup and the draft, or hands the ticket to a person.

CONFIDENCE_THRESHOLD = 0.70
# spec.md v2, CHANGE-3: a lower gate when the ticket carries a valid reference and no risky word.
CONFIDENCE_THRESHOLD_WITH_REFERENCE = 0.62
DRAFTABLE_CATEGORIES = {"status", "refund_status", "account"}
HIGH_RISK_WORDS = r"\b(refund|rembours\w*|dispute|chargeback|litige|contest\w*|waive|waiver|geste commercial)\b"

# Account situations where a person must act (spec.md edge cases, governance.md Session 4).
ACCOUNT_HOLDS = [
    (r"contract ended", "Contract ended: hand to a referent or to legal."),
    (r"bank details change in progress.*sent [^;]*to (?:the )?OLD account", "Bank change in progress and money already sent to the old account: hand to a referent."),
    (r"on hold[^;]*(?:reconciliation|rounding)", "Payout held by a cent-level reconciliation difference: payments operations must release it."),
]


def apply_routing_rule(route_result: dict, ticket: dict, clues: dict) -> dict:
    """
    Return {"action": "draft" | "escalate", "reason": str}.
    ticket and clues come from reader.split_ticket() and reader.extract_clues().
    """
    category = route_result["category"]
    confidence = route_result["confidence"]
    merchant_text = ticket["merchant_text"]
    account_context = ticket["account_context"]

    # 1. Several merchant accounts in one ticket are out of scope.
    merchant_ids = set(re.findall(r"\bM-\d{4}\b", merchant_text))
    if len(merchant_ids) > 1:
        return {"action": "escalate", "reason": f"Several merchant accounts in one ticket: {sorted(merchant_ids)}."}

    # 2. Without this merchant's account context there is nothing to look up.
    if not ticket["merchant_id"]:
        return {"action": "escalate", "reason": "No account context: nothing to look up (out of scope)."}

    # 3. Refund requests, disputes, fee waivers and out-of-scope questions are person only.
    if category not in DRAFTABLE_CATEGORIES:
        return {"action": "escalate", "reason": f"Category '{category}' is person only."}

    # 4. Account situations that need a person, whatever the merchant asked.
    for pattern, reason in ACCOUNT_HOLDS:
        if re.search(pattern, account_context, flags=re.IGNORECASE):
            return {"action": "escalate", "reason": reason}

    # 5. Confidence gate (lower when a valid reference is present and no risky word appears).
    has_reference = any(reference.startswith("TX-") for reference in clues["references"])
    # A refund-status question names the refund by design, so the word is not a risk signal there.
    risky = category != "refund_status" and bool(re.search(HIGH_RISK_WORDS, ticket["message"], flags=re.IGNORECASE))
    threshold = CONFIDENCE_THRESHOLD_WITH_REFERENCE if has_reference and not risky else CONFIDENCE_THRESHOLD
    if confidence < threshold:
        return {"action": "escalate", "reason": f"Routing confidence {confidence} below threshold {threshold}."}

    return {"action": "draft", "reason": f"Passed the routing gate ({category}, confidence {confidence})."}
