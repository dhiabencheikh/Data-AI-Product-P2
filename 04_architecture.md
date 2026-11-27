# 04 · Architecture — Team Ledgerly · Ledgerly agent-assist copilot

> Session 4 deliverable, updated 27 November. Describes the 4-step hybrid prototype in `/prototype` (how to run it: `README.md`).

## 1. One-line description
A deterministic workflow copilot that pre-reads a merchant's isolated ledger and account flags when a payment ticket arrives, drafting grounded replies with citations for tier-1 support agents to approve, edit, or escalate — never sending or moving money automatically.

## 2. The diagram
```text
ticket (merchant_id + text)
│
▼  reader.py: splits the merchant's words from this merchant's account rows; other merchants' notes are dropped
[1. router.py]  ──(category, confidence)──▶  [2. routing_rule.py]
(Rung 2: ML, reads the merchant's words only)  (Rung 1: rules & gate)
                                  │
┌─────────────────────────────────┴───────────────────────────────┐
│ person-only category (refund request, dispute, fee waiver,      │ pass (status / refund status /
│ out of scope) · contract ended · bank change with money sent    │ account, confidence ≥ 0.70,
│ · cent-level hold · several accounts · confidence < 0.70        │ ≥ 0.62 with a valid reference)
▼                                                                 ▼
⊘ ABSTENTION: hand to a person                            [3. drafter.py] (lookup in this merchant's ledger + draft)
(no draft; the agent handles the ticket as today)                     │
                                                    ┌───────────────┴───────────────┐
                                                    │ 0 or several candidates        │ 1 confident match + evidence
                                                    ▼                                ▼
                                    ⊘ ABSTENTION: no confident match        [4. policy.py] (rung 1: policy check)
                                    (panel suggests the question                      │
                                     to ask the merchant)                ┌───────────┴───────────┐
                                                                         │ block                  │ pass
                                                                         ▼                        ▼
                                                         ⊘ BLOCKED: reason shown,       ⊘ APPROVAL: tier-1 agent
                                                           never approvable              (Confirm / Check in the ledger /
                                                                                          Not this one · edit · Send)
                                                                                                  │
                                                                                                  ▼
                                                                                   [audit log, L4: logs/audit_log.jsonl]
```

⏻ **Override switch `COPILOT_MODE`, three positions:** `ON` (drafts, the agent may insert and send) · `SUGGEST_ONLY` (pre-read and drafts stay visible, Insert/Send disabled: L1) · `OFF` (no pre-read: the ticket works exactly as today). Any unknown value falls back to `OFF`. Owners: Head of Support by day, on-call Backend / AI Engineer by night.

## 3. Component table
| # | Component | Rung (1 rules · 2 classical ML · 3 pretrained model · 4 custom) | Pattern (chaining · routing · parallelization · orchestrator-workers · evaluator-optimizer · agent) | Trust level (L1–L4) | Checkpoint ⊘ (approval · abstention · sampling · none) | Metric observed (`evals/reports/report_v1.md`, 100 cases) |
|---|---|---|---|---|---|---|
| 0 | `reader.py` (split the ticket, extract clues) | 1 (rules: patterns) | Chaining | L4 (read-only) | None | Feeds steps 1–3; no merchant's data crosses to another (0 / 5 isolation traps) |
| 1 | `router.py` (ticket classifier) | 2 (TF-IDF character n-grams + logistic regression, 346 training phrases) | Routing | L4 (internal, read-only) | None (feeds the gate) | Draft / hand-over decision right on 93 / 100 tickets (with step 2) |
| 2 | `routing_rule.py` (confidence & risk gate) | 1 (rules: threshold 0.70, 0.62 with a valid reference; person-only categories; account holds) | Routing (conditional gate) | L4 (deterministic gate) | **⊘ Abstention** (refund requests, disputes, fee waivers, bank change with money sent, contract ended, cent-level holds, several accounts, confidence below the gate) | 0 drafts on 44 person-only tickets |
| 3 | `drafter.py` (isolated lookup & draft) | 3 in the target design (pretrained model + retrieval); in the prototype, templates filled from the ledger (mock drafter, no API key) | Prompt chaining | L2 | **⊘ Abstention** (`NO_DRAFT` on 0 or several candidates) | Coverage 49 / 56 = 87.5 %; match precision 47 / 47 = 100 % |
| 4 | `policy.py` (compliance & PII guard) | 1 (rules: patterns + every cited reference must be on this merchant's account) | Evaluator / gate | L4 (hard block) | **⊘ Approval** (the tier-1 agent reviews, edits, and clicks Send) | 0 money promises, 0 bank codes or IBANs, 0 foreign references passed |

## 4. Workflow or agent?
Team Ledgerly built a **deterministic workflow**, not an autonomous agent. Every ticket follows a fixed, pre-drawn path (`reader` → `router` → `routing_rule` → `drafter` → `policy`) with hard gates between steps. Because Ledgerly handles B2B payments, disputes and banking data, an autonomous agent with open-ended tool loops would create unacceptable financial and compliance risks (promising unauthorised refunds, leaking another merchant's records). Moving one step up (an LLM router or a multi-step query planner) would need a sandboxed ledger access verified at > 99.9 % isolation on at least 200 eval cases, plus automated rollback triggers.

## 5. Fallbacks
- **retrieval finds nothing:** `drafter.py` returns `NO_DRAFT` ("No confident match in this merchant's ledger"); the panel suggests the question to ask the merchant (reference, customer name, date and time); the ticket opens in the standard view.
- **the model's confidence is below the threshold:** `routing_rule.py` (`confidence < 0.70`, or `< 0.62` with a valid reference and no risky word) blocks drafting and hands the ticket to the agent.
- **the policy checker blocks the draft:** `policy.py` returns `block` with the rule violated (refund promise, bank code, IBAN, reference not on this account); the draft is suppressed and never approvable.
- **the API is down:** steps 0–2 and 4 run locally; step 3 degrades to `NO_DRAFT` on a timeout or an error, the panel says "Pre-read unavailable" and the agent works the ticket as before. A sustained outage moves the switch to `OFF` (`06_07` §4).

## 6. The override switch ⏻
- **Who can switch it off:** Head of Support (business owner, by day) and the on-call Backend / AI Engineer (by night).
- **Scope:** everyone (one environment variable, `COPILOT_MODE`, read at every ticket), three positions: `ON` · `SUGGEST_ONLY` · `OFF`. `SUGGEST_ONLY` is the first move on a quality alert; `OFF` on a harmful incident or an outage.
- **Tested on:** 27 November 2026, on the prototype (laptop as staging), with `python prototype/test_switch.py`: `ON` gives a draft that may be sent, `SUGGEST_ONLY` a draft that cannot be sent, `OFF` no pre-read; an unknown value falls back to `OFF`. PASS on all four checks. Next drill: 27 February 2027.

## 7. Data
- **Training data (`prototype/data/router_training.csv`):** 346 synthetic phrases in French and English across 7 categories (`status`, `refund_status`, `refund_request`, `dispute`, `fee_waiver`, `account`, `out_of_scope`), built by `prototype/data/make_router_training.py` from fragments written by the team. None comes from the eval-set.
- **Evaluation data (`evals/eval_set_v1.csv`):** 100 invented cases (`L-01` to `L-100`), labelled by the team before any run; labels never changed after a run. `eval_set_v0.csv` keeps the 50 cases of Session 4.
- **Audit and eval logs:** `prototype/logs/` (not in Git): one JSON line per output — ticket, merchant, switch position, route, outcome, match (transaction, evidence, candidates ruled out), citations, flags, the draft shown or the blocked draft (kept for the weekly review, never shown), and the fields the ticket tool fills when a person acts: edits, sender, time sent (`spec.md` io_contracts).
- **Personal data present?** No real merchant or payer data. Synthetic names, masked accounts (`•• 2210`) and invented `TX-`/`M-` ids, in the course Git repository, visible to Team Ledgerly and the course instructors (see `governance.md`).

## 8. Eval result
*"On the 100-case eval-set, 49 of the 56 draftable tickets got a draft (87.5 %, criterion ≥ 70 %), every draft cites the right transaction (47 / 47, criterion ≥ 98 %), and none of the 44 person-only tickets got a draft. Two human graders agree at 90 % on the golden 30 and find 9 of its 17 draftable tickets sendable as is; the judge agrees with them at 86.7 %."* — `evals/reports/report_v1.md`. The first prototype (`eval-v0`) produced no draft at all: `evals/report_v0.md`.

## 9. What you would build next (3 lines max)
1. Let an open account flag route the ticket by rule (terms, KYC) and retrain the router on real phrasing from the shadow run (misses L-16, L-28, L-30, L-60, L-72, L-77, L-83).
2. Remove the unsupported "next payout" sentence of the "received" template (L-07, L-61) and list the candidates and the question to ask in the panel's no-match view.
3. Replace the template drafter by a pretrained model behind the same policy check, and expose `/draft` and `/health` through FastAPI (`06_07` §3).
