import re

# Step 4 · Policy checker (rung 1: deterministic rules from spec.md and governance.md).
# Runs on every draft before the agent sees it. A blocked draft is never shown as a reply.

REFERENCE_PATTERN = r"\b(?:TX|VO|RF)-\d+\b"

FORBIDDEN_PATTERNS = [
    (r"\b(we will|we'll|we are going to|we have approved|we approve)\b[^.]*\b(refund|reimburse)", "Promises a refund"),
    (r"\brefund\b[^.]*\b(approved|guaranteed|will be (issued|sent))\b", "Promises a refund outcome"),
    (r"\b(nous allons|nous allons vous) rembourser\b|\bremboursement (sera|est) (accordé|validé)\b", "Promises a refund (FR)"),
    (r"\b(waive|waived|waiving)\b[^.]*\bfee", "Promises a fee waiver"),
    (r"\b(close|closed|cancel|cancelled)\b[^.]*\b(dispute|chargeback)\b", "Promises a dispute or chargeback outcome"),
    (r"\bcode\s*[A-Z]{0,2}\d{2}\b", "Quotes a bank error code (payer or merchant personal data)"),
    (r"\b[A-Z]{2}\d{2}[A-Z0-9•]{6,}", "Quotes an IBAN"),
]


def check_policy(draft_result: dict, account_context: str) -> dict:
    """
    Validate a draft before it is shown to the human agent.
    Returns {"policy": "pass" | "block" | "skipped", "reason": str}.
    """
    if draft_result.get("status") != "drafted":
        return {"policy": "skipped", "reason": "No draft produced."}

    text = draft_result.get("draft", "")
    citations = draft_result.get("citations", [])

    # 1. Grounding: every draft cites at least one ledger or Terms source.
    if not citations:
        return {"policy": "block", "reason": "Ungrounded draft: no citation."}

    # 2. Tenant isolation: every reference in the draft exists, whole, on this merchant's own account
    #    (compared as whole references, so TX-9011 never passes because TX-90112 exists).
    account_references = set(re.findall(REFERENCE_PATTERN, account_context))
    for reference in re.findall(REFERENCE_PATTERN, text):
        if reference not in account_references:
            return {"policy": "block", "reason": f"Reference {reference} is not on this merchant's account."}

    # 3. No promise of money, no personal data of the payer.
    for pattern, reason in FORBIDDEN_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            return {"policy": "block", "reason": reason}

    return {"policy": "pass", "reason": "Grounded and compliant with the Ledgerly policy."}
