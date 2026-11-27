# Governance — our living file

> Created for Assignment 1, one line added every session. One question at the oral is drawn from this file.
> Answers are provisional: write what you know today, and mark what you still have to check.

## Session 1 — the six questions
| # | Question | Our answer (provisional) | To check with |
|---|---|---|---|
| 1 | **EU AI Act:** which risk tier is our agent in, and why? (minimal · limited — transparency: tell the user it is an AI · high-risk · prohibited) | Minimal, or limited at most. It assists an internal support agent; it does not decide on credit, access to a service or money, and the merchant never talks to it. The agent knows it is working with an AI. If drafts reach merchants largely as written, we still tell them AI helped write the reply (transparency, good practice). Agents get training on what the copilot can and cannot do (AI literacy, art. 4). **To check:** that no use slides into a high-risk case, e.g. creditworthiness or credit scoring of natural persons (Annex III). | Legal / DPO |
| 2 | **Data:** whose data does it use, and on what legal basis? (GDPR art. 6; what the B2B contract allows) | Merchants' account and transaction data, which includes personal data of their own payers (names, IBANs). Basis: the B2B contract with each merchant (GDPR art. 6). Whether Ledgerly is controller or processor for payer data is open: if processor, the data processing agreement (art. 28) must allow this use, and the LLM provider becomes a sub-processor the merchant has to accept. Only the fields needed for the match go to the model (IBANs masked). Hard rule: no cross-tenant leakage, so merchant A's transactions can never appear in merchant B's draft. **To check:** controller or processor; whether the contract allows an LLM provider; data residency and transfers outside the EU. | Legal, DPO, Security |
| 3 | **Accountability:** who is accountable when it is wrong — and where is the human? | Towards the merchant, Ledgerly is accountable for every reply, whatever the copilot suggested ("a separate legal entity" is not a defence, Moffatt v. Air Canada). Inside Ledgerly, the Head of Support owns the copilot, and the agent who approves a draft is responsible for checking it before sending. An override switch turns drafts off for everyone. **To check:** who can flip the switch outside office hours. | Head of Support |
| 4 | **Never:** what must it never do? | Never send to the merchant; never move money or promise a refund; never show a transaction match without its evidence, and abstain when unsure. | Product |
| 5 | **Explainability:** explainable to whom? (the customer, the support agent, the auditor) | Support agent: which transaction was matched and why (amount, date, counterparty). Merchant: the reply cites the transaction reference. Auditor: a log of the draft, the match, the edits and who sent it. | Support QA, Compliance |
| 6 | **The people it cannot serve:** what happens to them? | Tickets with no confident match, multi-account or non-payment questions get no draft and are handled fully by a human, as today. Counter-metric: handling time on these tickets must not get worse. | Product / Support |

## Session 2 — the cost of error
- Which cost-of-error line is a **legal or reputational** risk, not just money? A reply that confirms the wrong transaction (the merchant acts on it), or a draft that leaks another merchant's data. The second one is a personal-data breach that may have to be notified within 72 hours (GDPR art. 33), not just rework.
- Who in the company **owns** that risk? The Head of Support owns wrong replies. Data leakage is owned by the Head of Security (or CISO), with the DPO advising and checking compliance. **To check:** that Ledgerly has these roles.

## Session 3 — data and trust level

### The six-question data audit
| # | Question | Our answer | Source type (measured / analogy / guess) | To check with |
|---|---|---|---|---|
| 1 | **Provenance** — where does each row come from, who collected it, when? | Production: Ledgerly's own systems, written while running the service — tickets and replies (ticketing tool), transactions (ledger), payouts, the CRM account record, the policy knowledge base. The MVP eval-set uses none of it: its 100 cases (`evals/eval_set_v1.csv`) are invented, generated with Claude and labelled by the team. | guess (Ledgerly's systems are assumed, not seen) | Engineering |
| 2 | **Volume & labels** — how many rows, labelled by whom, with which guideline? | 12,000 tickets a month; hundreds of transactions per merchant account. No ticket is linked to its transaction today, so there are no labels. Eval-set: 100 cases (`eval_set_v1.csv`; 200 is the production standard), labelled by hand by the team with one rule: "the transaction a careful agent would confirm from the ledger, or *no confident match*"; two human graders on the golden 30: 90 % agreement, 86.7 % with the judge (`evals/README.md`). | measured (tickets) · guess (transactions per account) | Support QA |
| 3 | **Coverage** — which languages, plans, regions vs the users we ship to? | Three ticket categories: status 50 %, refunds and disputes 30 %, account and other 20 %; French and English; EUR. The eval-set must cover each category, small and large merchants, and the trap case (several payments of the same amount). | guess (to measure on 12 months of ticket tags) | Support QA |
| 4 | **Rights** — legal basis (GDPR art. 6), what the customer contract allows, retention | Merchant data: the B2B contract (art. 6(1)(b)). Payers' names and IBANs: if Ledgerly is processor, the data processing agreement (art. 28) must allow this use, and the LLM provider becomes a sub-processor the merchant accepts; EU residency; no training on the data. Retention: traces and audit log kept 12 months, then deleted (one period for all, see Session 8). | guess | DPO, Legal |
| 5 | **Leakage** — can a row reappear in the test set, or in another customer's answer? | Test set: the eval cases are never used as prompt examples, and nobody tunes the prompt or the rules while looking at them. Other customers: every query is filtered by the ticket's merchant ID before retrieval, so another merchant's rows cannot reach the model. The eval-set includes two merchants with look-alike payer names to test it. | guess (design requirement) | Security |
| 6 | **Freshness** — how old is it, does that world still exist? | The ledger and payouts change by the minute: the copilot reads them live when the ticket arrives, never from a copy. Policy clauses (fees, dispute windows) change a few times a year: each carries its version and date. Past tickets older than 12 months weigh less in the summary. | guess | Engineering, Support |

- **Purpose limitation (GDPR art. 5):** the data is used only to answer the ticket it belongs to, by the agent who handles it. It is not used to train or fine-tune any model. Drafts, matches, edits and the name of the sender are kept 12 months in the audit log (`prototype/logs/audit_log.jsonl` in the prototype), for audit, then deleted.
- **Isolation between customers:** the copilot only queries data carrying the ticket's merchant ID; the filter sits in the data layer, not in the prompt. There is no shared index across merchants. Any draft showing another merchant's data is the rollback trigger, and may be a breach to notify within 72 hours (Session 2 line above).
- **Known gaps by segment** (language, plan, region): languages other than French and English (out of scope); large merchants with many payments of the same amount (harder matching); disputes and chargebacks (fewer cases, higher cost of error); accounts with an open flag (bank change in progress, contract, terms); payments touched by an offer or a cashback (cent-level differences); non-EUR payments; merchants with several accounts (out of scope). Results are reported for each of these segments.

### Trust level per step (same scale as Session 1)
| Step | L1 suggests · L2 drafts, a person approves · L3 acts on a scope, a person samples · L4 acts alone under a threshold · or person only | Why (cost of an error) |
|---|---|---|
| 1. Read the ticket, extract the clues | L4 | Read-only, nothing reaches the merchant; a wrong clue is caught at step 2 |
| 2. Find the transaction | L2 — shown with its evidence, the agent confirms; "no confident match" below the threshold | A wrong match costs €25 to €200 and is worse than no draft, because the agent anchors on it |
| 3. Summarise the account: open flags first, then past tickets | L1 | A missed past ticket costs a reopen (≈ €10); a missed bank-change flag sends money to the old bank. The summary links to each source |
| 4. Check the policy | L1 for the clause quote · person only for any refund, chargeback or fee decision | Wrong refund or chargeback advice: €200 to €400, and a legal and reputational risk |
| 5. Write the reply | L2 — the agent edits and approves every draft | A sent error reaches the merchant; a draft that a person reads does not |
| 6. Send, move money, log | Person only (send, refund, chargeback) · L4 for the log | Sending and money are the two things the copilot must never do |

## Session 4 — human-in-the-loop points and the override switch

### 1. Human Checkpoints (⊘)
Every point in the Ledgerly copilot workflow where human oversight is enforced by design (never left to model self-confidence):
- **Checkpoint 1 — Routing & Risk Abstention (`⊘ Abstention` in `routing_rule.py`):** Mandatory hand-off to a human specialist or referent whenever a ticket involves a refund request, chargeback/dispute, fee waiver, ended contract, cent-level reconciliation hold, bank-details change with funds already sent, multi-account query, or routing confidence `< 0.70`. *Owner:* Tier-1 Support Queue Lead (SLA: standard queue priority, < 4 business hours).
- **Checkpoint 2 — Ambiguity / Missing-Match Abstention (`⊘ Abstention` in `drafter.py`):** When 0 or >1 transactions match within the merchant's isolated ledger, the system outputs `NO_DRAFT` and leaves investigation to the human agent. *Owner:* Assigned Tier-1 Support Agent (SLA: immediate at ticket open).
- **Checkpoint 3 — Pre-Send Draft Review (`⊘ Approval` in Agent UI):** Every generated draft is strictly L2 ("copilot that drafts, never sends"). A Tier-1 agent must verify the cited `TX-`/`VO-` references against the ledger panel, edit if needed, and click Approve & Send. *Owner:* Assigned Tier-1 Support Agent (SLA: before any external merchant communication).
- **Checkpoint 4 — Post-Launch Quality & Isolation Audit (`⊘ Sampling`):** Weekly manual audit of 5 % of approved replies and 100 % of policy-blocked drafts to verify zero cross-merchant data leakage and zero unauthorized financial promises. *Owner:* Support QA Lead & Data Protection Officer (SLA: weekly review every Friday).

### 2. Override Switch (⏻)
- **Owner:** Head of Support (operational authority, by day) and the on-call Backend / AI Engineer (technical execution, by night).
- **Mechanism & Scope:** one environment variable, `COPILOT_MODE`, read at every ticket across all 800 merchant queues, with three positions: `ON` (drafts the agent may send) · `SUGGEST_ONLY` (drafts visible, Insert/Send disabled: L1) · `OFF` (no pre-read: agents handle tickets as before). An unknown value falls back to `OFF`.
- **Verification:** tested on 27 November 2026 on the prototype (`python prototype/test_switch.py`): the three positions give what they must, and an unknown value falls back to `OFF` — PASS. (The test written here for 15 November could not have run: the switch was not in the code then.)

### 3. Evaluation Data Storage & Access Control
- **Location:** `evals/eval_set_v0.csv` (50 cases, Session 4) and `evals/eval_set_v1.csv` (100 cases, Session 5), labelled before any run, in the team Git repository (`Data-AI-Product-P2`); the outputs of each run in `evals/copilot_outputs/drafts_v1.csv`.
- **Privacy & Anonymisation:** Contains 100 % synthetic/invented merchant IDs (`M-xxxx`), transaction IDs (`TX-xxxxx`), and masked IBANs (`•• xxxx`); zero real production customer or payer PII is present.
- **Access & Anti-Contamination Rule:** Visible to Team Ledgerly members and course evaluators. Strictly separated from the router's training phrases (`prototype/data/router_training.csv`, none taken from the eval-set); team members are prohibited from tuning prompts or thresholds against individual eval rows.

## Session 5 — counter-metrics and the segments we report
- **Segments reported:** (1) Ticket category (`Transaction & payout status` 50 %, `Refunds, disputes & chargebacks` 30 %, `Account & other` 20 % — from `02_sizing.xlsx`), (2) Language (`French` vs `English`), (3) Account state (`open flag: bank_change / contract / terms` vs `clean account`), (4) Payment complexity (`standard EUR` vs `grouped transfer / cashback cent-difference / non-EUR`), and (5) Merchant size (`high-volume merchants with duplicate amounts` vs `standard merchants`).
- **Counter-metrics watched:** (1) **7-day ticket reopen rate** (catches wrong matches or incomplete drafts closed too fast) and (2) **Human-only handling time & escalation queue delay** (catches slowdowns on tickets where the copilot abstains with `NO_DRAFT`).
- **Harm threshold that stops the rollout (and owner):** *"If the 7-day reopen rate on French tickets, flagged accounts, or high-volume merchants exceeds **1.5×** the baseline segment rate for two consecutive weeks — OR if a single wrong transaction match causes a payout to an outdated bank account or any cross-merchant leak occurs — the Head of Support immediately moves `COPILOT_MODE` to `SUGGEST_ONLY` (L1: drafts visible, nothing can be sent) on that segment — `OFF` for a leak or a payout to an old account — until the DPO and Support QA verify the root cause. **Owner:** Head of Support (reviewed monthly with DPO and Support QA)."*

## Sessions 6 + 7 — Experiment signature, rollback switch & trace retention
- **Experiments on real users.** Any experiment on real Ledgerly merchants and Tier-1 agents is signed by the **Head of Support** and reviewed by the **Data Protection Officer (DPO)** before it starts; the decision rule and the harm threshold are written before the first unit (`06_07_experiments_operations.md §1–§2`).
- **The switch.** The **Head of Support** can move `COPILOT_MODE` to `SUGGEST_ONLY` or `OFF` by day; the **On-call Backend / AI Engineer** by night (under `15 minutes`). Last tested **`2026-11-27`** on the prototype (`python prototype/test_switch.py`); next test **`2027-02-27`** (`06_07_experiments_operations.md §4`).
- **The trace.** One OpenTelemetry trace per output (`POST /draft` spans), kept **`12 months`** in **Langfuse + isolated Postgres audit storage**; **Legal Counsel & the Data Protection Officer (DPO)** answer a customer or a regulator from it, and **Ledgerly answers for what the system says** (*Moffatt v. Air Canada*, 2024 BCCRT 149; EU AI Act Art. 26 & 50).


## Session 8 — who signs the launch
- This launch (step 0b shadow mode from 4 January 2027, then step 1 internal agents and 5 % of status tickets, then step 2 the A/B on 50 % of `Transaction & payout status` tickets, 1–28 February 2027) is signed by the **Head of Support** and the **Product Manager**; the **DPO** has read the protocol on 27 November 2026 and validates it under the six conditions below (`08_launch_memo.md`).
- Not applicable: a person approves and sends every answer (EU AI Act art. 50 — the merchant never talks to the AI). Agents are told and trained on what the copilot can and cannot do (art. 4, AI literacy) before step 0b.
- The rollback plan (`06_07` §4) was last tested on 27 November 2026 by Team Ledgerly, on the prototype (`python prototype/test_switch.py`, PASS); next test: 27 February 2027.

### The DPO's six conditions (why the DPO could say no, and what closes it)
| # | Why the DPO could say no | Condition | Status |
|---|---|---|---|
| 1 | Ledgerly's role for payer data (controller or processor) is still open (Session 1, Q2) | Legal confirms the role; the data processing agreement (GDPR art. 28) names the LLM provider as a sub-processor, and merchants get 30 days to object | To close before step 0b — Legal + DPO |
| 2 | Payer data could leave the EU or train the provider's model | EU processing (or standard contractual clauses), zero retention and no training written in the provider contract | To close before step 0b — Security + Legal |
| 3 | More data than needed could reach the model | Only the fields needed for the match; IBANs masked, decline codes never quoted — enforced by `policy.py` (0 leaks in `evals/reports/report_v1.md`) | Met in the prototype; re-checked in shadow mode |
| 4 | One merchant's data could appear in another's reply (a breach to notify within 72 h, art. 33) | The `merchant_id` filter sits in the data layer; 0 / 5 isolation traps passed; any leak moves the switch to `OFF` and opens the breach procedure | Met in the prototype; weekly 5 % audit from step 1 |
| 5 | Two different retention periods were written (as long as the ticket / 12 months) | One period: traces and audit log 12 months, then deleted — at least the 6 months the AI Act asks of deployers' logs (art. 26(6)) | Met (written in Sessions 3, 6 + 7 and here) |
| 6 | An experiment on agents and merchants' data without an impact assessment | A short DPIA (GDPR art. 35) and the agents informed and trained before the first live ticket | To close before step 0b — DPO + Head of Support |
