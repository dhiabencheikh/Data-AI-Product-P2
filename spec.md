# spec.md — executable spec · Ledgerly agent-assist copilot · v2 (Session 4, final 27 November)

> Session 3 skeleton, completed in Session 4, final version 27 November (implemented in `/prototype`, measured in `evals/reports/report_v1.md`). Same content as `03_product_brief.md` v2, with nothing left vague: inputs, outputs, edge cases, fallbacks, done.

## problem
Tier-1 agents at Ledgerly, a B2B payments platform with 800 merchants, spend 40 % of their handling time reading before they answer any of the 12,000 tickets a month. On each payment ticket they open the ledger, payouts, bank tools, the account record and past tickets to find where the payment the merchant means is stuck, then check every number by hand before replying. The copilot pre-reads the account when the ticket arrives and shows the agent the transaction, where it is stuck, the open flags on the account and a draft reply. The agent confirms, edits and sends; the copilot never sends anything and never moves money.

## user_workflow
Steps with inputs and outputs, and the trust level of each step.
```
- read      : ticket form fields + free text + merchant_id      -> clues {reference, amount, currency, date, customer}   (L4)
- flags     : merchant_id                                        -> open account flags, shown first                       (L1)
- match     : clues + ledger rows of merchant_id only            -> transaction + evidence | no_confident_match            (L2 — the agent confirms)
- locate    : transaction                                        -> stage + payout + error code                            (L2 — shown with the match)
- summarise : merchant_id + past tickets                         -> short history with links                               (L1)
- policy    : category + transaction                             -> clause quote · block any promise of money              (L1 · decisions are person only)
- draft     : transaction + stage + clause + stock phrases        -> reply with references filled in from the ledger        (L2 — the agent edits and approves)
- send      : approved reply                                     -> merchant                                                (person only)
- log       : match, draft, edits, sender                        -> audit log                                               (L4)
```

## io_contracts
```
ticket   : {id, merchant_id, channel: form | free_message, fields: {reference?, amount?, currency?, date?, customer?}, text, received_at}
flag     : {type: bank_change | contract | terms | fees, status: open, since, note}
match    : {status: confident | no_confident_match, transaction_id?, amount, currency, received_at, payer,
            evidence: [{field, ticket_value, ledger_value}], ruled_out: [{transaction_id, reason}], confidence,
            ask_merchant?: [reference | customer | date | time]}
position : {stage: payer_bank | ledgerly | merchant_bank | paid_out, payout_id?, payout_items?: [transaction_id, amount], error_code?, next_step}
draft    : {text, references: [transaction_id, payout_id?], clause_id?, policy: pass | block, block_reason?}
log      : {ticket_id, match, draft, edits, sent_by, sent_at}
```

## edge_cases
- several payments fit (same amount, same payer name, "last week's payment" with three candidates) → `no_confident_match`, list the candidates, suggest the question to ask the merchant (`ask_merchant`), no draft
- open account flag (bank change in progress, contract ended, terms not accepted) → show the flag first; a bank change with money already sent → hand to a referent, no draft saying the money will arrive
- form fields missing or incomplete (they are optional), payment too recent to appear in the form, or free message → extract the clues from the text, then the same lookup; still no confident match → `ask_merchant`
- the fields the merchant typed do not match the ledger (wrong reference, different amount) → no exact match; rank on the other clues and show the agent which field does not match
- an evidence line the ledger rows do not support (e.g. "only payment from this payer in the last 30 days" when an older one exists) → the line is never shown; every evidence line is computed from the ledger, and candidates from the same payer are always listed open in `ruled_out`
- the payment was paid out in a grouped transfer → `payout_items` lists every payment in the transfer
- the account history holds the cause (a merchant setting changed, the same question already asked) or the merchant states an urgency → the draft gives the cause and answers the urgency, citing only what the ledger and the history show
- refund, chargeback or dispute → "human decision only" banner; the draft may ask for documents but promises no outcome
- non-EUR payment → show the converted amount and the rate
- personal data of the payer (decline reason, IBAN) → never quoted in the draft; IBANs masked
- data of another merchant → never retrieved: every query is filtered by `merchant_id` in the data layer
- out of scope ("how do I" questions, several merchant accounts, languages other than French and English) → no match, no draft; the ticket works as today

## fallbacks
- router confidence below 0.70 (0.62 when the ticket carries a valid `TX-` reference and no risky word) → no draft, hand-over; the ticket works as today. The gate is never tuned on eval tickets
- policy block → show the reason to the agent, no draft
- the copilot or one data source is down → the panel says so; the ticket works as today
- the agent clicks "Check in the ledger" → the transaction opens in the ledger; the proposal stays as it was
- the agent clicks "Not this one" → the draft is discarded; manual search
- hand to a referent or to legal → the pre-read goes with the ticket
- override switch `COPILOT_MODE` → `SUGGEST_ONLY` (drafts visible, Insert/Send disabled) or `OFF` (no pre-read), for everyone; Head of Support by day, on-call engineer by night; an unknown value means `OFF`

## done_criteria
- the success criterion from `03_product_brief.md` §7: handling time falls by at least 38 % on tickets with a proposed match, and no more than 0.5 % of those end with a wrong transaction in the approved reply — measured with agents, in the A/B of `06_07` (the eval-set cannot time people)
- a proposed match on at least 70 % of tickets, with match precision of at least 98 % (hypothesis 1 of `01_problem_statement.md`)
- zero drafts that promise a refund, a chargeback or a dispute outcome on the adversarial cases
- zero cases where another merchant's data appears
- zero evidence lines that the ledger does not support

## out_of_scope
The WON'T column of the MoSCoW board: auto-send · automatic refunds, chargebacks or fee waivers · any chat or bot that talks to merchants · tickets spanning several merchant accounts · fine-tuning on merchant or payer data · languages other than French and English · "how do I" questions answered from the documentation · proactive messages to merchants.

## v2_changes (added after evals/report_v0.md; implemented and measured on 27 November, `evals/reports/report_v1.md`)
Every top miss from `evals/report_v0.md` converted into an explicit specification rule:
- **[CHANGE-1 · Lookup & Disambiguation — fixes `L-07`, `L-28`]:** When a merchant provides an approximate amount (e.g., "around 300 euros", "environ 450 euros") and multiple ledger candidates exist, `match` must rank candidates by `(payer_name_similarity + date_proximity)` before triggering `no_confident_match`. Only escalate when two candidates match both payer and date (e.g., `L-10`, `L-31`).
- **[CHANGE-2 · Refund Reference Extraction — fixes `L-14`, `L-36`]:** The `read` and `match` steps must extract `RF-\d+` refund references in addition to `TX-\d+` payment references, and query the refund settlement log (`3–5 working days` bank delay) without triggering the human-only new-refund block.
- **[CHANGE-3 · Noisy Text & Field-Mismatch Resilience — fixes `L-15`, `L-32`, `L-37`]:** Lower the routing escalation threshold from `0.70` to `0.62` when the ticket carries a `TX-\d+` reference (even one that is not on the account: the lookup then falls back on amount, date and payer) and the merchant's message contains no high-risk word (`refund`, `rembours…`, `dispute`, `chargeback`, `litige`, `contest…`, `waive`, `geste commercial`; not checked on refund-status questions, which name the refund by design). A bank change with money already sent is handled before the gate, as an account hold. When a form `TX-` reference does not match the ledger (`L-32`), fall back to `(merchant_id + amount + date + payer)` lookup and flag the mismatched reference to the agent.

- **[CHANGE-4 · Router reads the merchant only — fixes 0 drafts on 50 in `report_v0.md`]:** the router classifies the merchant's message (or the form fields), never the ledger rows; it is trained on `prototype/data/router_training.csv` (346 phrases, none from the eval-set), French and English, including angry, misspelt and very-recent-payment phrasing.
- **[CHANGE-5 · Wrong form reference goes to the agent — fixes `L-32`, `L-65`, `L-99` of run 1]:** the mismatch is shown in the agent's panel, never written in the reply; every reference written in a reply must exist on this merchant's account (`policy.py`).
- **[CHANGE-6 · Refunds and disputes in v1]:** a refund already issued (`RF-`) gets a status draft; a request for a new refund, a dispute or a chargeback, and a fee waiver get no draft at all in v1 (hand-over), even where the label allows an L2 draft asking for documents: that draft comes after the A/B.
- **[CHANGE-7 · Open misses of `evals/reports/report_v1.md`, to fix before step 1 of `08_launch_memo.md`]:** (a) the "received" reply says only what the ledger shows — no "next payout" sentence (`L-07`, `L-61`); (b) a whole-account flag (terms, KYC) routes the ticket by rule before the router (`L-16`, `L-83`); (c) the router is retrained on real phrasing from the shadow run, never on eval tickets (`L-28`, `L-30`, `L-60`, `L-72`, `L-77`).

## eval_set
`evals/eval_set_v0.csv` — 50 invented cases (Session 4); `evals/eval_set_v1.csv` — 100 cases (Session 5; 200 is the production standard). Run: `python prototype/run_eval.py`. Inputs generated with Claude; every label checked by hand by the team before any run. Recipe, prompt, labelling rule and FAIL conditions: `evals/README_eval_set.md`.
