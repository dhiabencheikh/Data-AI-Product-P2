import re

# Rung 1: Deterministic policy checker (Ledgerly spec.md & governance.md)
# Blocks any promise of refund/money, payer decline codes, or full IBAN leaks.

FORBIDDEN_PATTERNS = [
    (r"\brefund\b.*\b(issued|approved|sent|guaranteed|will arrive)\b", "Promises or confirms a refund outcome"),
    (r"\b(waive|waived|waiving)\b.*\bfee\b", "Promises a fee waiver"),
    (r"\b(close|cancel)\b.*\b(dispute|chargeback)\b", "Promises a dispute/chargeback outcome"),
    (r"\bcode\s*(51|05|AC04|MD01)\b", "Leaks internal or payer bank error code"),
    (r"\bFR\d{2}[A-Z0-9•]{10,}\b", "Leaks payer or unmasked IBAN"),
]

def check_policy(draft_result: dict) -> dict:
    """
    Validates a generated draft before showing it to the human agent.
    Returns: {"policy": "pass" | "block", "reason": str}
    """
    if draft_result.get("status") != "drafted":
        return {"policy": "skipped", "reason": "No draft produced."}

    text = draft_result.get("draft", "")
    citations = draft_result.get("citations", [])

    # 1. Grounding requirement: every draft must cite at least one verified ledger/KB source
    if not citations:
        return {"policy": "block", "reason": "Ungrounded draft: missing citations."}

    # 2. Check forbidden financial promises and PII leaks
    for pattern, reason in FORBIDDEN_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            return {"policy": "block", "reason": reason}

    return {"policy": "pass", "reason": "Grounded and compliant with Ledgerly policy."}

if __name__ == "__main__":
    sample_ok = {"status": "drafted", "draft": "Payment TX-90112 settled in VO-3301 [TX-90112].", "citations": ["TX-90112"]}
    sample_bad = {"status": "drafted", "draft": "Declined due to code 51 [TX-90301].", "citations": ["TX-90301"]}
    print("OK test:", check_policy(sample_ok))
    print("Bad test:", check_policy(sample_bad))
