import re

from reader import MONTH_PATTERN, parse_ledger_rows

# Step 3 · Lookup + draft (rung 3 in the architecture; here a mock drafter with templates,
# no API key needed, as allowed in Session 4). It only reads the ticket's own merchant account,
# matches one transaction with its evidence or abstains, then fills a reply from the ledger.

NAME_STOPWORDS = {"sarl", "sas", "and", "les", "des", "fils", "the", "client", "customer", "from"}
APPROXIMATE_TOLERANCE = 0.05
FRENCH_MARKERS = {"bonjour", "paiement", "virement", "règlement", "reçu", "remboursement", "compte", "est", "pas", "mon", "notre", "merci", "toujours"}

TEMPLATES = {
    "en": {
        "greeting": "Hello,",
        "grouped": "payment {tx} ({amount}) was paid out on {date} in grouped transfer {vo} of {total} ({count} payments){account}. On your bank statement you will see {total}, not {amount}.",
        "paid_out": "payment {tx} was paid out on {date} in transfer {vo}{account}.",
        "converted_paid": "payment {tx} was received and converted to {eur} (rate {rate}), then paid out on {date} in transfer {vo}{account}.",
        "converted_scheduled": "payment {tx} was received and converted to {eur} (rate {rate}). Your payout is scheduled for {date}.",
        "declined": "payment {tx} was not collected: it was declined by your customer's bank. Please ask your customer to contact their bank or to pay again.",
        "returned": "the payout {vo} for payment {tx} was returned by your bank on {date}. The funds are held at Ledgerly. Please check your bank details in your Ledgerly space so that we can send the transfer again.",
        "processing": "payment {tx} has been received and is being processed. Your payout is scheduled for {date}.",
        "scheduled": "payment {tx} has been received. Your payout is scheduled for {date}{account}.",
        "on_hold_iban": "payment {tx} has been received. Your payout is on hold until your new bank details are verified.",
        "refund": "refund {rf} of {amount} for payment {tx} was sent to your customer's bank on {date}. Banks usually take 3 to 5 working days to show it on the card or account.",
        "terms": "your payouts are paused because the new Terms of Service have not been accepted yet [Terms §1.4]. Once you accept them in your account settings, the pending payouts will be released.",
        "kyc": "your payouts are paused while your annual KYC/KYB documents are pending update [Terms §1.5]. Please upload them in your account settings to resume payouts.",
        "plan_change": "About the fee: your account moved from the Starter plan (1.5 %) to the Standard plan (1.9 %) on {date}.",
        "subscription": "About the deduction: the monthly subscription fee of {amount} of your Standard plan is deducted from the transfer.",
        "weekly": "Your payouts now follow a weekly cycle, which is why the date is later than usual.",
        "previous_ticket": "We have linked this reply to your earlier request {ticket}.",
        "received": "payment {tx} ({amount}) was received on {date}. It will be included in your next scheduled payout.",
        "closing": "Best regards,\nLedgerly Support",
    },
    "fr": {
        "greeting": "Bonjour,",
        "grouped": "le paiement {tx} ({amount}) a été versé le {date} dans le virement groupé {vo} de {total} ({count} paiements){account}. Sur votre relevé, vous verrez {total} et non {amount}.",
        "paid_out": "le paiement {tx} a été versé le {date} dans le virement {vo}{account}.",
        "converted_paid": "le paiement {tx} a été reçu et converti en {eur} (taux {rate}), puis versé le {date} dans le virement {vo}{account}.",
        "converted_scheduled": "le paiement {tx} a été reçu et converti en {eur} (taux {rate}). Votre versement est prévu le {date}.",
        "declined": "le paiement {tx} n'a pas été encaissé : il a été refusé par la banque de votre client. Merci de lui demander de contacter sa banque ou de payer à nouveau.",
        "returned": "le virement {vo} du paiement {tx} a été renvoyé par votre banque le {date}. Les fonds sont conservés chez Ledgerly. Merci de vérifier vos coordonnées bancaires dans votre espace Ledgerly pour que nous puissions relancer le virement.",
        "processing": "le paiement {tx} a bien été reçu et est en cours de traitement. Votre versement est prévu le {date}.",
        "scheduled": "le paiement {tx} a bien été reçu. Votre versement est prévu le {date}{account}.",
        "on_hold_iban": "le paiement {tx} a bien été reçu. Votre versement est suspendu jusqu'à la vérification de vos nouvelles coordonnées bancaires.",
        "refund": "le remboursement {rf} de {amount} pour le paiement {tx} a été envoyé à la banque de votre client le {date}. Les banques mettent en général 3 à 5 jours ouvrés à l'afficher.",
        "terms": "vos versements sont suspendus car les nouvelles conditions générales n'ont pas encore été acceptées [Terms §1.4]. Dès que vous les acceptez dans vos paramètres, les versements en attente seront libérés.",
        "kyc": "vos versements sont suspendus en attendant la mise à jour annuelle de vos documents KYC/KYB [Terms §1.5]. Merci de les déposer dans vos paramètres pour reprendre les versements.",
        "plan_change": "Concernant les frais : votre compte est passé de l'offre Starter (1,5 %) à l'offre Standard (1,9 %) le {date}.",
        "subscription": "Concernant la retenue : l'abonnement mensuel de {amount} de votre offre Standard est déduit du virement.",
        "weekly": "Vos versements suivent désormais un cycle hebdomadaire, d'où une date plus tardive que d'habitude.",
        "previous_ticket": "Nous avons rattaché cette réponse à votre demande précédente {ticket}.",
        "received": "le paiement {tx} ({amount}) a bien été reçu le {date}. Il sera inclus dans votre prochain versement programmé.",
        "closing": "Bien cordialement,\nLe support Ledgerly",
    },
}


def detect_language(message: str) -> str:
    """French when the merchant's own words contain French markers, English otherwise."""
    words = set(re.findall(r"[a-zà-ÿ']+", message.lower()))
    return "fr" if len(words & FRENCH_MARKERS) >= 2 else "en"


def name_tokens(text: str) -> set:
    """Lower-case name tokens of three letters or more, without legal-form words."""
    return {token for token in re.findall(r"[a-zà-ÿ]{3,}", text.lower()) if token not in NAME_STOPWORDS}


def amount_fits(row_amount, wanted, approximate: bool) -> bool:
    """Exact amount match, or within the tolerance when the merchant wrote 'around'."""
    if row_amount is None or wanted is None:
        return True
    if approximate:
        return abs(row_amount - wanted) <= wanted * APPROXIMATE_TOLERANCE
    return abs(row_amount - wanted) < 0.01


def find_match(ticket: dict, clues: dict) -> dict:
    """Match one transaction of this merchant, with its evidence, or say there is no confident match."""
    rows = parse_ledger_rows(ticket["account_context"])
    result = {"status": "no_confident_match", "row": None, "evidence": [], "ruled_out": [], "mismatch": None,
              "ask_merchant": []}

    # 1. A reference the merchant gave, found on this merchant's own account, decides.
    for reference in clues["references"]:
        for row in rows:
            if row["id"] == reference:
                result.update(status="confident", row=row, evidence=[f"reference {reference} given by the merchant"])
                result["ruled_out"] = [other["id"] for other in rows if other["id"] != reference]
                return result
        if reference.startswith("TX-"):
            result["mismatch"] = reference

    # 2. Otherwise rank on the other clues (spec.md v2, CHANGE-1 and CHANGE-3): payer, amount, weekday.
    wanted_names = name_tokens(clues["customer"]) or (clues["words"] - NAME_STOPWORDS)
    candidates = []
    for row in rows:
        if not (name_tokens(row["payer"]) & wanted_names):
            continue
        if not amount_fits(row["amount"], clues["amount"], clues["approximate"]):
            continue
        candidates.append(row)

    if len(candidates) > 1 and clues["weekday"] is not None:
        same_day = [row for row in candidates if row["date"] and row["date"].weekday() == clues["weekday"]]
        if same_day:
            candidates = same_day

    if len(candidates) == 1:
        chosen = candidates[0]
        # Every evidence line must be true for the ledger row (03_user_research.md T1): add a line only when it holds.
        evidence = [f"payer {chosen['payer']} named in the ticket"]
        if clues["amount"] is not None and chosen["amount"] is not None:
            evidence.append(f"amount {chosen['amount']:.2f} fits {clues['amount']:.2f}")
        if clues["weekday"] is not None and chosen["date"] and chosen["date"].weekday() == clues["weekday"]:
            evidence.append(f"date {chosen['date']} is the weekday the merchant gave")
        result.update(status="confident", row=chosen, evidence=evidence)
        result["ruled_out"] = [row["id"] for row in rows if row["id"] != chosen["id"]]
        return result

    result["ruled_out"] = [row["id"] for row in rows]
    result["ask_merchant"] = ["reference", "customer name", "date and time of the payment"]
    return result


def format_money(amount, currency: str) -> str:
    """Write an amount in the currency of the ledger row: €640.00, £1,050.00, CHF 880.00."""
    if amount is None:
        return ""
    if currency == "CHF":
        return f"CHF {amount:,.2f}"
    return f"{currency}{amount:,.2f}"


def describe_row(row: dict, words: dict, language: str) -> str:
    """Pick the template that fits what the ledger says about this transaction."""
    segment = row["segment"]
    account_match = re.search(r"to (?:account |the )?(?:NEW account )?(•• \d{4})", segment)
    account = ""
    if account_match:
        account = f" to the account ending {account_match.group(1)}" if language == "en" else f" sur le compte se terminant par {account_match.group(1)}"
    values = {"tx": row["id"], "amount": format_money(row["amount"], row["currency"]), "account": account}

    vo_match = re.search(r"\b(VO-\d+)\b", segment)
    day_month = rf"\d{{1,2}} (?:{MONTH_PATTERN})"
    paid_match = re.search(rf"paid out ({day_month})", segment)
    scheduled_match = re.search(rf"(?:payout scheduled|scheduled) ({day_month})", segment)
    converted_match = re.search(r"converted to (€[\d,]+\.\d{2}) \(rate ([\d.]+)\)", segment)
    grouped_match = re.search(r"\((€[\d,]+\.\d{2}), (\d+) payments\)", segment)
    returned_match = re.search(rf"returned ({day_month})", segment)

    if "declined" in segment or "failed" in segment:
        return words["declined"].format(**values)
    if returned_match and vo_match:
        return words["returned"].format(vo=vo_match.group(1), date=returned_match.group(1), **values)
    if "pending IBAN verification" in segment:
        return words["on_hold_iban"].format(**values)
    if converted_match and paid_match and vo_match:
        return words["converted_paid"].format(eur=converted_match.group(1), rate=converted_match.group(2),
                                              date=paid_match.group(1), vo=vo_match.group(1), **values)
    if converted_match and scheduled_match:
        return words["converted_scheduled"].format(eur=converted_match.group(1), rate=converted_match.group(2),
                                                   date=scheduled_match.group(1), **values)
    if grouped_match and paid_match and vo_match:
        return words["grouped"].format(vo=vo_match.group(1), date=paid_match.group(1), total=grouped_match.group(1),
                                       count=grouped_match.group(2), **values)
    if paid_match and vo_match:
        return words["paid_out"].format(vo=vo_match.group(1), date=paid_match.group(1), **values)
    if "processing" in segment:
        date_text = scheduled_match.group(1) if scheduled_match else ("tomorrow" if language == "en" else "demain")
        return words["processing"].format(date=date_text, **values)
    if scheduled_match:
        return words["scheduled"].format(date=scheduled_match.group(1), **values)
    received_match = re.search(rf"({day_month})", segment)
    if received_match and row["amount"]:
        # The ledger only shows the payment itself: say it was received, promise no date.
        return words["received"].format(date=received_match.group(1), **values)
    return ""


def account_notes(account_context: str, words: dict) -> list:
    """Extra sentences when the account history holds the cause (spec.md edge cases)."""
    notes = []
    plan_match = re.search(r"Starter \(1\.5 %\) to Standard(?: plan)? \(1\.9 %\) on (\d{1,2} \w+)", account_context)
    if plan_match:
        notes.append(words["plan_change"].format(date=plan_match.group(1)))
    subscription_match = re.search(r"subscription fee (€[\d,]+\.\d{2})", account_context)
    if subscription_match:
        notes.append(words["subscription"].format(amount=subscription_match.group(1)))
    if re.search(r"weekly (?:payout )?cycle", account_context):
        notes.append(words["weekly"])
    ticket_match = re.search(r"(#T-\d+)", account_context)
    if ticket_match:
        notes.append(words["previous_ticket"].format(ticket=ticket_match.group(1)))
    return notes


def open_flags(account_context: str) -> list:
    """Open account flags, always shown first to the agent."""
    return re.findall(r'flag(?: OPEN)? "([^"]+)"', account_context)


def draft_refund_status(ticket: dict, clues: dict, words: dict) -> dict:
    """A refund that already exists: say where it is, never promise a new one (spec.md v2, CHANGE-2)."""
    refunds = re.findall(r"refund (RF-\d+) (€[\d,]+\.\d{2}) issued [^,;]* for (TX-\d+), sent to (?:the )?payer's bank (\d{1,2} \w+)",
                         ticket["account_context"])
    if len(refunds) != 1:
        return {"status": "NO_DRAFT", "reason": "No single refund found on this account.", "citations": []}
    refund_id, amount, tx_id, sent_date = refunds[0]
    body = words["refund"].format(rf=refund_id, amount=amount, tx=tx_id, date=sent_date)
    return {"status": "drafted", "citations": [refund_id, tx_id], "body": body,
            "evidence": [f"only refund on the account: {refund_id}"]}


def draft_account(ticket: dict, words: dict) -> dict:
    """Whole-account blocks that the Terms explain (terms not accepted, KYC overdue)."""
    context = ticket["account_context"].lower()
    if "new terms of service not accepted" in context:
        return {"status": "drafted", "citations": ["Terms §1.4"], "body": words["terms"], "evidence": ["open flag: terms not accepted"]}
    if "kyc/kyb annual document update overdue" in context:
        return {"status": "drafted", "citations": ["Terms §1.5"], "body": words["kyc"], "evidence": ["open flag: KYC/KYB overdue"]}
    return {"status": "NO_DRAFT", "reason": "No account flag that the Terms explain.", "citations": []}


def retrieve_and_draft(ticket: dict, clues: dict, category: str) -> dict:
    """Return a grounded draft {status: drafted, draft, citations, match, flags} or {status: NO_DRAFT, reason}."""
    language = detect_language(ticket["message"])
    words = TEMPLATES[language]
    flags = open_flags(ticket["account_context"])

    if category == "refund_status":
        result = draft_refund_status(ticket, clues, words)
    elif not parse_ledger_rows(ticket["account_context"]):
        # No transaction on this account: only a whole-account flag can be explained.
        result = draft_account(ticket, words)
    else:
        match = find_match(ticket, clues)
        if match["status"] != "confident":
            return {"status": "NO_DRAFT", "reason": "No confident match in this merchant's ledger.",
                    "citations": [], "match": match, "flags": flags}
        body = describe_row(match["row"], words, language)
        if not body:
            return {"status": "NO_DRAFT", "reason": f"No template for the ledger state of {match['row']['id']}.",
                    "citations": [], "match": match, "flags": flags}
        sentences = [body] + account_notes(ticket["account_context"], words)
        citations = [match["row"]["id"]] + re.findall(r"\bVO-\d+\b", match["row"]["segment"])
        result = {"status": "drafted", "citations": citations, "body": " ".join(sentences), "evidence": match["evidence"],
                  "match": match, "agent_notes": []}
        if match["mismatch"]:
            # spec.md v2, CHANGE-3: the wrong reference is flagged to the agent, never written in the reply.
            result["agent_notes"].append(f"The form reference {match['mismatch']} is not on this account; "
                                         f"matched {match['row']['id']} from amount, date and payer.")

    if result["status"] != "drafted":
        result["flags"] = flags
        return result

    body = result.pop("body")
    result["draft"] = f"{words['greeting']}\n\n{body[0].upper() + body[1:]}\n\n{words['closing']}"
    result["flags"] = flags
    result["language"] = language
    return result
