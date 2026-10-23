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

## Session 3 — data (to come)
## Session 4 — human-in-the-loop points and the override switch (to come)
## Session 5 — counter-metrics and the segments we report (to come)
## Session 6 — protected segments and the harm threshold that stops an experiment (to come)
## Session 7 — accountable owner, rollback authority, incident path (to come)
