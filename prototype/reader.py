import re
from datetime import date

# Step "read" of spec.md: split a ticket into what the merchant wrote and what the
# merchant's own account shows, then extract the clues used by the lookup.
# A ticket in the eval-set looks like:
#   Ticket of 6 Nov · form fields: ref TX-1, amount €640.00 · message: "..." · account M-0412: <ledger rows>

# Ticket dates carry no year ("6 Nov"): YEAR is the year of the eval-set. It must be set to the
# current year (or read from the ticket's timestamp) before running on live tickets, because the
# weekday tie-break of drafter.find_match depends on it.
YEAR = 2026
MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}
# Month abbreviations as written in the ledger rows ("4 Nov"), shared with drafter.py.
MONTH_PATTERN = "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec"
WEEKDAYS = {
    "monday": 0, "lundi": 0,
    "tuesday": 1, "mardi": 1,
    "wednesday": 2, "mercredi": 2,
    "thursday": 3, "jeudi": 3,
    "friday": 4, "vendredi": 4,
    "saturday": 5, "samedi": 5,
    "sunday": 6, "dimanche": 6,
}
APPROXIMATE_WORDS = ("around", "about", "approximately", "environ", "d'environ", "~")

# A number written before "€" or "euros" counts only if it is not the end of a reference such as TX-90501.
AMOUNT_PATTERN = r"(?:€|£|CHF\s?)\s?(\d[\d,.]*\d|\d)|(?<![\w-])(\d[\d,.]*\d|\d)\s?(?:€|eur\b|euros\b)"
DATE_PATTERN = rf"\b(\d{{1,2}}) ({MONTH_PATTERN})\b"

# Notes about other merchants are never part of this merchant's context (tenant isolation).
OTHER_MERCHANT_NOTES = [
    r"\(another merchant,.*?\)",
    r"\([A-Z]{2}-\d+ belongs to merchant.*?\)",
]


def parse_amount(raw: str) -> float:
    """Turn '1,560.00' or the European '1.200' into a float."""
    cleaned = raw.strip(".,")
    if re.fullmatch(r"\d{1,3}(\.\d{3})+", cleaned):
        # European thousands separator, e.g. "1.200"
        cleaned = cleaned.replace(".", "")
    cleaned = cleaned.replace(",", "")
    return float(cleaned)


def find_amounts(text: str) -> list:
    """Return every money amount written in a piece of text."""
    amounts = []
    for symbol_amount, word_amount in re.findall(AMOUNT_PATTERN, text, flags=re.IGNORECASE):
        raw = symbol_amount or word_amount
        try:
            amounts.append(parse_amount(raw))
        except ValueError:
            continue
    return amounts


def find_currency(text: str) -> str:
    """Currency of the first amount of a text: £, CHF, or € (euros by default)."""
    found = re.search(AMOUNT_PATTERN, text, flags=re.IGNORECASE)
    if found and found.group(0).startswith("£"):
        return "£"
    if found and found.group(0).upper().startswith("CHF"):
        return "CHF"
    return "€"


def find_date(text: str):
    """Return the first 'day Month' date of a text as a date object, or None."""
    found = re.search(DATE_PATTERN, text)
    if not found:
        return None
    return date(YEAR, MONTHS[found.group(2).lower()], int(found.group(1)))


def split_ticket(ticket_text: str) -> dict:
    """Separate the merchant's own words from the account context."""
    merchant_id = None
    account_context = ""
    account_match = re.search(r"account (M-\d{4})[^:]*:(.*)$", ticket_text)
    if account_match:
        merchant_id = account_match.group(1)
        account_context = account_match.group(2)
        merchant_part = ticket_text[: account_match.start()]
    else:
        merchant_part = ticket_text

    for pattern in OTHER_MERCHANT_NOTES:
        account_context = re.sub(pattern, "", account_context, flags=re.IGNORECASE)

    message_match = re.search(r'message[^:]*: "(.*?)"', merchant_part)
    message = message_match.group(1) if message_match else ""

    form_match = re.search(r"form fields: (.*?)(?: · message|$)", merchant_part)
    form_fields = form_match.group(1) if form_match else ""

    return {
        "merchant_id": merchant_id,
        "message": message,
        "form_fields": form_fields,
        "merchant_text": merchant_part,
        "account_context": account_context.strip(),
    }


def extract_clues(ticket: dict) -> dict:
    """Extract the clues a careful agent would use: references, amount, date, names, weekday."""
    merchant_text = ticket["merchant_text"]
    form_fields = ticket["form_fields"]
    lowered = merchant_text.lower()

    customer_match = re.search(r"customer ([^,·(]+)", form_fields)
    weekday = None
    for word, index in WEEKDAYS.items():
        if re.search(rf"\b{word}\b", lowered):
            weekday = index
            break

    amounts = find_amounts(merchant_text)
    return {
        "references": list(dict.fromkeys(re.findall(r"\b(?:TX|RF|VO)-\d+\b", merchant_text))),
        "amount": amounts[0] if amounts else None,
        "approximate": any(word in lowered for word in APPROXIMATE_WORDS),
        "date": find_date(form_fields),
        "customer": customer_match.group(1).strip() if customer_match else "",
        "weekday": weekday,
        "words": set(re.findall(r"[a-zà-ÿ]{3,}", lowered)),
    }


def parse_ledger_rows(account_context: str) -> list:
    """Cut the account context into one row per transaction that exists on this account."""
    rows_by_id = {}
    positions = [found.start() for found in re.finditer(r"\bTX-\d+\b", account_context)]
    for index, start in enumerate(positions):
        end = positions[index + 1] if index + 1 < len(positions) else len(account_context)
        segment = account_context[start:end].strip(" ;,·")
        tx_id = re.match(r"TX-\d+", segment).group(0)
        if "does not exist" in segment:
            continue
        # The same transaction can be named twice (e.g. a past ticket, then the ledger row): merge.
        row = rows_by_id.setdefault(tx_id, {"id": tx_id, "segment": "", "amount": None, "currency": "€", "date": None,
                                            "payer": ""})
        row["segment"] = f"{row['segment']} {segment}".strip()
        payer_match = re.search(r"payer ([A-Z][A-Z&.' ]+[A-Z])", segment)
        if not payer_match:
            payer_match = re.search(rf"\d (?:{MONTH_PATTERN}) ([A-Z][A-Z&.' ]+[A-Z])", segment)
        amounts = find_amounts(segment)
        if row["amount"] is None and amounts:
            row["amount"] = amounts[0]
            row["currency"] = find_currency(segment)
        if row["date"] is None:
            row["date"] = find_date(segment)
        if not row["payer"] and payer_match:
            row["payer"] = payer_match.group(1).strip()
    return list(rows_by_id.values())
