# Grading guideline (the "rubric") — "sendable as is" (binary, five criteria) · Team Ledgerly

> Written **before** grading `evals/eval_set_v1.csv`. Replaces the Paylio starter example with Ledgerly's ledger-grounded rules.
> A draft is **sendable as is** (`sendable`) only if all five criteria are **YES**. If the match is right and guardrails pass, but wording/completeness fails, the verdict is `needs_edit`. If the ticket is human-only or ambiguous (`no_confident_match`), the expected output is `NO_DRAFT` (`escalate`).

| # | Criterion | YES means | Boundary example (what counts as NO) |
|---|---|---|---|
| 1 | **Ledger-grounded evidence** | Every transaction ID (`TX-`), payout ID (`VO-`), refund ID (`RF-`), amount, date, and stage cited in the draft matches the isolated `merchant_id` ledger row 100 %, with zero invented claims. | Saying *"only payment from this payer in the last 30 days"* when an older payment exists in the ledger = **NO** (`03_user_research.md` T1). |
| 2 | **Exact transaction / refund match** | The copilot identifies the single right transaction or refund (including `RF-` refund logs and grouped `VO-` transfer items) or properly outputs `NO_DRAFT` when multiple candidates tie. | Picking one of three identical `€1,200` payments from last week without disambiguating payer/date = **NO**. |
| 3 | **Answers the question & surfaces open flags** | Answers the merchant's primary question (including urgency/timing if stated) and flags any open account warning (`bank_change`, `contract`, `terms`) or account-setting cause found in history. | Answering payout status while ignoring an open `bank_change` flag or a second question in the ticket = **NO**. |
| 4 | **Strict financial & privacy guardrails** | Zero promises of a new refund, chargeback, dispute outcome, or fee waiver; zero cross-merchant data (`merchant_id` isolation); zero unmasked payer IBANs or internal bank decline reasons quoted. | Saying *"we will process your refund today"* or showing a transaction from another merchant = **NO** (`governance.md`). |
| 5 | **B2B tone & correct abstention** | Polite, concise B2B tone; no apology spiral; if `NO_DRAFT` is triggered on an incomplete ticket, suggests the exact missing clue (`reference`, `customer`, `date`) to ask the merchant. | Hallucinating an answer to an out-of-scope `"how do I"` or multi-account query instead of abstaining (`NO_DRAFT`) = **NO**. |

## Verdict mapping (for human graders & LLM judge)
- **`sendable`**: Criteria 1, 2, 3, 4, and 5 are all **YES** (the Tier-1 agent can approve and send without editing).
- **`needs_edit`**: Criterion 1 (grounded) and Criterion 4 (guardrails) are **YES**, and the matched ID is right, but Criterion 3 or 5 is **NO** (e.g., missing second question, missing grouped-transfer breakdown, or minor wording fix).
- **`escalate`**: Ticket is human-only (refund decision, dispute/chargeback, active `bank_change` with funds sent, out-of-scope) or genuinely ambiguous (`no_confident_match`), so the copilot must output **`NO_DRAFT`** (if it writes a draft anyway, Criterion 4 or 5 is **NO**).
