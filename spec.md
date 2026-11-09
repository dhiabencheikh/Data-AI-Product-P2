# spec.md — executable spec · Ledgerly agent-assist copilot · skeleton v0

> Session 3 skeleton, completed in Session 4. Same content as `03_product_brief.md` v2, with nothing left vague: inputs, outputs, edge cases, fallbacks, done.

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
position : {stage: payer_bank | ledgerly | merchant_bank | paid_out, payout_id?, error_code?, next_step}
draft    : {text, references: [transaction_id, payout_id?], clause_id?, policy: pass | block, block_reason?}
log      : {ticket_id, match, draft, edits, sent_by, sent_at}
```

## edge_cases
- several payments fit (same amount, same payer name, "last week's payment" with three candidates) → `no_confident_match`, list the candidates, suggest the question to ask the merchant (`ask_merchant`), no draft
- open account flag (bank change in progress, contract ended, terms not accepted) → show the flag first; a bank change with money already sent → hand to a referent, no draft saying the money will arrive
- form fields missing or incomplete (they are optional), payment too recent to appear in the form, or free message → extract the clues from the text, then the same lookup; still no confident match → `ask_merchant`
- the fields the merchant typed do not match the ledger (wrong reference, different amount) → no exact match; rank on the other clues and show the agent which field does not match
- refund, chargeback or dispute → "human decision only" banner; the draft may ask for documents but promises no outcome
- non-EUR payment → show the converted amount and the rate
- personal data of the payer (decline reason, IBAN) → never quoted in the draft; IBANs masked
- data of another merchant → never retrieved: every query is filtered by `merchant_id` in the data layer
- out of scope ("how do I" questions, several merchant accounts, languages other than French and English) → no match, no draft; the ticket works as today

## fallbacks
- confidence below [threshold — set on the eval-set, not tuned on it] → `no_confident_match`; the ticket works as today
- policy block → show the reason to the agent, no draft
- the copilot or one data source is down → the panel says so; the ticket works as today
- the agent clicks "Not this one" → the draft is discarded; manual search
- hand to a referent or to legal → the pre-read goes with the ticket
- kill switch → the Head of Support turns drafts off for everyone

## done_criteria
- the success criterion from `03_product_brief.md` §7: on the 200-ticket eval-set, handling time falls by at least 38 % on tickets with a proposed match, and no more than 0.5 % of those end with a wrong transaction in the approved reply
- a proposed match on at least 70 % of tickets, with match precision of at least 98 % (hypothesis 1 of `01_problem_statement.md`)
- zero drafts that promise a refund, a chargeback or a dispute outcome on the adversarial cases
- zero cases where another merchant's data appears

## out_of_scope
The WON'T column of the MoSCoW board: auto-send · automatic refunds, chargebacks or fee waivers · any chat or bot that talks to merchants · tickets spanning several merchant accounts · fine-tuning on merchant or payer data · languages other than French and English · "how do I" questions answered from the documentation.

## eval_set
`evals/eval_set_v0.csv` — 20 invented cases now, 50 with Assignment 4, 200 by Session 5. Inputs generated with Claude; every label checked by hand by the team before any run.