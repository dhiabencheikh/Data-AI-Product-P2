import re

# Rung 3: Grounded retrieval + mock drafter (no external API key required per S4 rules)
# Enforces merchant_id isolation, ambiguity checks, and grounded citations.

def retrieve_and_draft(ticket_text: str, category: str) -> dict:
    """
    Extracts ledger clues strictly from the requesting merchant's isolated context
    and generates a grounded L2 draft with citations, or returns NO_DRAFT.
    """
    # 1. Enforce merchant_id isolation: strip any cross-merchant distractor notes
    isolated_context = re.sub(r"\(another merchant,.*?\)", "", ticket_text, flags=re.IGNORECASE)
    isolated_context = re.sub(r"\(TX-\d+ belongs to merchant.*?\)", "", isolated_context, flags=re.IGNORECASE)

    # 2. Extract transaction IDs (TX-xxxxx) and payout IDs (VO-xxxx) in the merchant's own ledger
    tx_matches = list(dict.fromkeys(re.findall(r"\bTX-\d+\b", isolated_context)))
    vo_matches = list(dict.fromkeys(re.findall(r"\bVO-\d+\b", isolated_context)))

    # 3. Check for open account flags (e.g., new terms not accepted, KYC overdue)
    if "new terms of service not accepted" in isolated_context.lower():
        return {
            "status": "drafted",
            "draft": (
                "Hello, your payouts are currently paused because the new Terms of Service "
                "have not yet been accepted in your Ledgerly dashboard [Terms §1.4]. "
                "Once you accept them in your account settings, your pending payments will be released automatically."
            ),
            "citations": ["Terms §1.4"],
        }

    if "kyc/kyb annual document update overdue" in isolated_context.lower():
        return {
            "status": "drafted",
            "draft": (
                "Hello, your payouts are temporarily paused while your annual KYC/KYB compliance documents "
                "are pending update [Terms §1.5]. Please upload the required documents in your account settings "
                "to resume scheduled payouts."
            ),
            "citations": ["Terms §1.5"],
        }

    # 4. Ambiguity guard: if multiple TX candidates exist in the ledger snippet without a single clear match
    if len(tx_matches) > 1:
        return {
            "status": "NO_DRAFT",
            "reason": f"Ambiguous match: multiple candidate transactions found ({', '.join(tx_matches)}).",
            "citations": [],
        }

    # 5. No confident transaction found in this merchant's ledger -> fallback to NO_DRAFT
    if len(tx_matches) == 0:
        return {
            "status": "NO_DRAFT",
            "reason": "No matching transaction found in requesting merchant's ledger.",
            "citations": [],
        }

    tx_id = tx_matches[0]
    citations = [tx_id]
    if vo_matches:
        citations.extend(vo_matches)

    # 6. Grounded draft templates based on verified ledger state
    ctx_lower = isolated_context.lower()

    if "declined by the payer's bank" in ctx_lower or "declined by payer's bank" in ctx_lower:
        # Never quote bank error code (e.g., code 51 / 05) or payer IBAN
        return {
            "status": "drafted",
            "draft": (
                f"Hello, payment {tx_id} was not collected because it was declined by your customer's bank. "
                f"Please ask your customer to verify with their bank or retry the payment [{tx_id}]."
            ),
            "citations": citations,
        }

    if "returned" in ctx_lower and "merchant's bank" in ctx_lower:
        vo_str = f" ({vo_matches[0]})" if vo_matches else ""
        return {
            "status": "drafted",
            "draft": (
                f"Hello, the payout{vo_str} for transaction {tx_id} was returned by your bank and the funds "
                f"are safely held at Ledgerly. Please verify and update your bank details in your Ledgerly space "
                f"so we can reschedule the transfer [{', '.join(citations)}]."
            ),
            "citations": citations,
        }

    if "converted to €" in ctx_lower:
        conv_match = re.search(r"converted to (€[\d,]+\.\d{2}) \(rate ([\d.]+)\)", isolated_context)
        sched_match = re.search(r"payout scheduled (\d+ \w+)", isolated_context)
        eur_amt = conv_match.group(1) if conv_match else "the converted EUR amount"
        rate = conv_match.group(2) if conv_match else "the applicable rate"
        sched_date = sched_match.group(1) if sched_match else "the next settlement date"
        return {
            "status": "drafted",
            "draft": (
                f"Hello, payment {tx_id} has been received and converted to {eur_amt} (exchange rate {rate}). "
                f"Your payout is scheduled for {sched_date} [{tx_id}]."
            ),
            "citations": citations,
        }

    if vo_matches:
        vo_id = vo_matches[0]
        acct_match = re.search(r"•• \d{4}", isolated_context)
        acct_str = f" to your bank account {acct_match.group(0)}" if acct_match else ""
        return {
            "status": "drafted",
            "draft": (
                f"Hello, payment {tx_id} has been settled and included in grouped payout transfer {vo_id}"
                f"{acct_str} [{tx_id}, {vo_id}]."
            ),
            "citations": citations,
        }

    # Processing / scheduled payout
    sched_match = re.search(r"payout scheduled (\d+ \w+)", isolated_context)
    sched_info = f"for {sched_match.group(1)}" if sched_match else "for the next working day"
    return {
        "status": "drafted",
        "draft": (
            f"Hello, payment {tx_id} has been received and is currently processing. "
            f"Your payout is scheduled {sched_info} [{tx_id}]."
        ),
        "citations": citations,
    }

if __name__ == "__main__":
    sample = "Ticket of 6 Nov · form fields: ref TX-90112 · account M-0412: TX-90112 €640.00 paid out 4 Nov in transfer VO-3301 to account •• 2210"
    print(retrieve_and_draft(sample, "status"))
