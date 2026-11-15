import re

# Rung 1: Deterministic routing rules (Ledgerly spec.md)
CONFIDENCE_THRESHOLD = 0.70
HUMAN_ONLY_CATEGORIES = {"refund", "dispute", "fee_waiver", "out_of_scope"}
HIGH_RISK_KEYWORDS = [
    r"bank details change in progress",
    r"contract ended",
    r"reconciliation difference",
    r"rounding mismatch",
    r"several merchant accounts",
]

def apply_routing_rule(route_result: dict, ticket_text: str) -> dict:
    """
    Decides whether the copilot proceeds to retrieval/drafting or hands over to a human.
    Returns: {"action": "draft" | "escalate", "reason": str}
    """
    category = route_result.get("category", "unknown")
    confidence = route_result.get("confidence", 0.0)
    text_lower = ticket_text.lower()

    # 1. Out-of-scope or human-only categories never auto-draft
    if category in HUMAN_ONLY_CATEGORIES:
        return {
            "action": "escalate",
            "reason": f"Category '{category}' is designated human-only / out-of-scope.",
        }

    # 2. High-risk account flags or operational holds require human referent
    for pattern in HIGH_RISK_KEYWORDS:
        if re.search(pattern, text_lower):
            return {
                "action": "escalate",
                "reason": f"High-risk flag or operational hold detected ({pattern}).",
            }

    # 3. Multiple merchant IDs in one ticket (out of scope per spec.md)
    merchant_ids = set(re.findall(r"\bM-\d{4}\b", ticket_text))
    if len(merchant_ids) > 1:
        return {
            "action": "escalate",
            "reason": f"Multiple merchant accounts referenced: {sorted(merchant_ids)}.",
        }

    # 4. Confidence threshold check
    if confidence < CONFIDENCE_THRESHOLD:
        return {
            "action": "escalate",
            "reason": f"Routing confidence {confidence} below threshold {CONFIDENCE_THRESHOLD}.",
        }

    return {
        "action": "draft",
        "reason": "Passed routing gate (confident status/account_flag lookup).",
    }

if __name__ == "__main__":
    print(apply_routing_rule({"category": "status", "confidence": 0.85}, "TX-90112 status"))
    print(apply_routing_rule({"category": "refund", "confidence": 0.91}, "Please refund €45"))
