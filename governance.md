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
| 1 | **Provenance** — where does each row come from, who collected it, when? | Production: Ledgerly's own systems, written while running the service — tickets and replies (ticketing tool), transactions (ledger), payouts, the CRM account record, the policy knowledge base. The MVP eval-set uses none of it: its 20 cases are invented, generated with Claude and labelled by the team. | guess (Ledgerly's systems are assumed, not seen) | Engineering |
| 2 | **Volume & labels** — how many rows, labelled by whom, with which guideline? | 12,000 tickets a month; hundreds of transactions per merchant account. No ticket is linked to its transaction today, so there are no labels. Eval-set: 20 cases now, 200 by Session 5, labelled by hand by the team with one rule: "the transaction a careful agent would confirm from the ledger, or *no confident match*"; two graders per case. | measured (tickets) · guess (transactions per account) | Support QA |
| 3 | **Coverage** — which languages, plans, regions vs the users we ship to? | Three ticket categories: status 50 %, refunds and disputes 30 %, account and other 20 %; French and English; EUR. The eval-set must cover each category, small and large merchants, and the trap case (several payments of the same amount). | guess (to measure on 12 months of ticket tags) | Support QA |
| 4 | **Rights** — legal basis (GDPR art. 6), what the customer contract allows, retention | Merchant data: the B2B contract (art. 6(1)(b)). Payers' names and IBANs: if Ledgerly is processor, the data processing agreement (art. 28) must allow this use, and the LLM provider becomes a sub-processor the merchant accepts; EU residency; no training on the data. Retention: drafts and logs kept as long as the ticket itself, for audit. | guess | DPO, Legal |
| 5 | **Leakage** — can a row reappear in the test set, or in another customer's answer? | Test set: the eval cases are never used as prompt examples, and nobody tunes the prompt or the rules while looking at them. Other customers: every query is filtered by the ticket's merchant ID before retrieval, so another merchant's rows cannot reach the model. The eval-set includes two merchants with look-alike payer names to test it. | guess (design requirement) | Security |
| 6 | **Freshness** — how old is it, does that world still exist? | The ledger and payouts change by the minute: the copilot reads them live when the ticket arrives, never from a copy. Policy clauses (fees, dispute windows) change a few times a year: each carries its version and date. Past tickets older than 12 months weigh less in the summary. | guess | Engineering, Support |

- **Purpose limitation (GDPR art. 5):** the data is used only to answer the ticket it belongs to, by the agent who handles it. It is not used to train or fine-tune any model. Drafts, matches, edits and the name of the sender are kept as long as the ticket, for audit.
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
## Session 4 — human-in-the-loop points and the override switch (to come)
## Session 5 — counter-metrics and the segments we report (to come)
## Session 6 — protected segments and the harm threshold that stops an experiment (to come)
## Session 7 — accountable owner, rollback authority, incident path (to come)
