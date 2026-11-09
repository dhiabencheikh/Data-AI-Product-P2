# 03 — Product brief · Ledgerly agent-assist copilot · v2

**Team:** Team Ledgerly · **Starting point:** P2 — agent-assist copilot, B2B payments fintech · **Version:** v2 — v1 plus the changes from three user conversations (sections 9–10)

> Every number says where it comes from: *(m)* measured · *(a)* analogy · *(g)* guess. Most of them come from `01_problem_statement.md` and `02_sizing.xlsx`.

## 1. Problem, user, do-nothing  *(from 01)*
- **Problem in one sentence (with a number):** tier-1 agents spend 40 % *(m)* of their handling time reading transaction history and past tickets before they can answer any of the 12,000 tickets a month *(m)*, about €576k a year of support cost *(derived)*.
- **User (persona):** Inès, tier-1 support agent at Ledgerly (invented persona), about 32 tickets a day *(a)* — goal: answer each merchant right the first time — pain: on every ticket she rebuilds the account story by hand across four tools (CRM, ledger, payouts, past tickets) to work out which payment the merchant means (the contact form's fields are optional and often incomplete) and where it is stuck. New agents lose the most: high turnover, an outdated manual, and experienced agents who spend time helping them.
- **Do-nothing baseline:** volume grows about 20 % *(g)*, agents get about 5 % faster on their own *(a)*: the reading cost goes from €576k to about €657k a year. The copilot must beat that trajectory, and the unified account view (non-AI, €180k a year *(g)*), not zero.

## 2. The process — as-is and to-be
One ticket about a payment, handled by Inès today: 14 min *(g: 32 tickets a day over about 7.5 h of handling)*.

| # | Step | Who today | Minutes | Error rate | Cost of an error | Automate / augment / keep human (test it fails) | Trust level (L1–L4 or person) | Minutes after | Metric for this step |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Read the ticket, spot what the merchant refers to (amount, date, client, reference) | Tier-1 agent | 1 *(g)* | 2 % *(g)* | Merchant asked to repeat: one more exchange, ≈ €5 *(g)* | **Automate** — passes the eight tests; errors are cheap because step 2 shows its evidence | L4 (read-only, no customer impact) | 0.5 | Clue extraction accuracy (amount, date, counterparty, reference) |
| 2 | Find the transaction and where it is stuck (payer's bank → Ledgerly → merchant's bank), across the ledger, payouts and bank tools | Tier-1 agent | 4 *(g)* | 3 % wrong transaction *(g)* | €25 on a status ticket, €200 on a refund or dispute *(g, 02)* | **Augment** — fails "errors are cheap" (a wrong match is worse than no draft) and "no need to explain" (the agent must see why) | L2 — one match with its evidence, the agent confirms; below the threshold: "no confident match" | 1.8 | Match precision on proposed matches (≥ 98 %) and coverage (≥ 70 %) |
| 3 | Read the account record (flags: bank change, contract, terms) and past tickets | Tier-1 agent | 1.5 *(g)* | 5 % miss a relevant flag or past ticket *(g)* | Reopened ticket ≈ €10 *(a)*; a missed bank change sends money to the old bank (user A's last error) | **Augment** — fails "no need to explain" (each point must link to its source) | L1 — suggests a summary, open flags first, with links | 0.8 | Share of summaries that miss an open flag or a relevant past ticket (graders) |
| 4 | Check the policy (payout delays, refund and dispute windows, fees) | Tier-1 agent | 2 *(g)* | 4 % *(g)* | Wrong refund or chargeback advice, €200 *(g, 02)* | **Keep human** for the decision — fails "errors are cheap"; the copilot only quotes the clause | Person only (refund, chargeback, fee decision) · L1 for the clause quote | 1.8 | Policy catches: drafts blocked for promising money (target: all) |
| 5 | Write the reply | Tier-1 agent | 4 *(g)* | 1 % *(g)* | Wrong wording, rework ≈ €5 *(g)* | **Augment** — a sent error is not cheap; a draft read by the agent is | L2 — draft citing the transaction reference, the agent edits and approves | 3.4 | Share of drafts sent with minor edits only |
| 6 | Send the reply, take any money action, log the ticket | Tier-1 agent | 1.5 *(g)* | 1 % *(g)* | Missing log: no audit trail; double refund *(g)* | **Keep human** for sending and money; **automate** the log | Person only (send, refund, chargeback) · L4 for the log | 1.5 | Share of sent replies with the matched transaction logged |
| | **Total** | | **14** | | | | | **9.8** | **−30 %** = the 02 base case. The flip point (−38 %) needs ≤ 8.7 min |

Steps 2 + 3 = 5.5 of 14 min = the 40 % of reading time *(m)*. The split by step and every error rate are guesses: today nobody measures the wrong-transaction rate, so QA reviews a sample of sent replies to set the baseline.

**Where the pain sits (the two steps):** step 2 (find the transaction) and step 3 (read the history): 5.5 min a ticket, and step 2 carries the costly error.
**The way back to a person (designed first):** below the confidence threshold the copilot says "no confident match" and the ticket opens exactly as today; on any proposed match the agent can click "Not this one" and search by hand; the agent can hand the ticket to a referent or to the legal team with the pre-read attached; nothing reaches the merchant unless the agent presses Send; the Head of Support can turn drafts off for everyone in one switch.
**Where the governance line sits:** anything that moves money (refund, chargeback, fee waiver) or reaches the merchant is person only; a merchant's data never appears in another merchant's ticket.

*Trust levels: L1 suggests · L2 drafts, a person approves · L3 acts on a scope, a person samples · L4 acts alone under a threshold.*

## 3. Features — RICE and MoSCoW
Reach from `02_sizing.xlsx`: 12,000 tickets a month; 8,400 where the copilot proposes a match (70 %); 3,600 refunds, disputes and chargebacks.

| Feature | Reach / month (from 02_sizing.xlsx) | Impact (0.25–3) | Confidence (50/80/100 %) | Effort (person-weeks) | RICE | MoSCoW |
|---|---|---|---|---|---|---|
| Policy guard: quote the clause, block any draft that promises a refund or a chargeback (step 4) | 3,600 | 2 | 80 % | 1 | 5,760 | MUST |
| Audit log: match, draft, edits, who sent (step 6) | 8,400 | 0.5 | 100 % | 1 | 4,200 | SHOULD |
| Account summary: open flags first (bank change, contract, terms), then past tickets, with links (step 3) | 8,400 | 1 | 80 % | 2 | 3,360 | MUST |
| Transaction and where it is stuck, with evidence, or "no confident match" (step 2) | 8,400 | 3 | 50 % | 4 | 3,150 | MUST |
| Auto-send the reply when confidence is high (what a flawed brief promises) | 8,400 | 3 | 50 % | 5 | 2,520 | WON'T |
| Ticket category tag: status / dispute / other (step 1) | 12,000 | 0.25 | 80 % | 1 | 2,400 | COULD |
| Draft reply from the team's stock phrases, references filled in from the transaction (step 5) | 8,400 | 1 | 50 % | 2 | 2,100 | MUST |
| Automatic refunds and chargebacks (what a flawed brief promises) | 3,600 | 2 | 50 % | 6 | 600 | WON'T |

- **MUST (≤ 4):** transaction and where it is stuck, with evidence, or "no confident match" · account summary, open flags first · draft reply with references filled in · policy guard.
- **SHOULD:** audit log.
- **COULD:** ticket category tag.
- **WON'T this time (≥ 5) — this is the out-of-scope list, decided 8 November 2026:** (1) auto-send, even when confident · (2) automatic refunds, chargebacks or fee waivers · (3) any chat or bot that talks to merchants · (4) tickets that span several merchant accounts · (5) fine-tuning a model on merchant or payer data · (6) tickets in languages other than French and English · (7) "how do I" questions answered from the documentation, with no payment to look up (added after the users).
- **The feature that tests our flip assumption, and why it is a MUST:** the transaction and where it is stuck. The flip assumption is the share of handling time saved on covered tickets (38 %), and almost all of it comes from not searching the ledger, payout and bank tools. It is only fourth in RICE because its confidence is 50 %: it is our riskiest assumption, so we build it first, to learn.
- **The cut that hurt the most:** the audit log. We promised it to the auditor in `governance.md`, but the eval-set test does not need it; it becomes a MUST before the first live ticket.

## 4. Data  *(from the six-question audit — details in governance.md)*
Ledgerly's own systems: tickets and replies, the ledger, payouts, the CRM account record, the policy knowledge base. 12,000 tickets a month *(m)*; no ticket is labelled with its transaction today, so the eval-set is invented and labelled by hand (20 cases now, 200 by Session 5). Coverage gaps to check: disputes, large merchants with many similar amounts, non-EUR payments, languages other than French and English. Legal basis: the merchant contract (GDPR art. 6); payer names and IBANs make the processor question and the LLM sub-processor open points for the DPO. Leakage: every query is filtered by the ticket's merchant ID. Freshness: the ledger changes by the minute, so the copilot reads live data, never a copy.

## 5. Model — one rung per part
| Part | Rung (1 rules · 2 classical ML · 3 pretrained model · 4 hybrid) | Why the rung below fails |
|---|---|---|
| Lookup from the contact form's fields (reference, amount, date, customer) — only when the merchant filled them in: the fields are optional and often incomplete, according to the users; share to measure on 200 tickets | 1 · rules | Bottom rung: when the fields are complete, an exact lookup is enough, and it is explainable |
| Read where the payment is stuck: payer's bank → Ledgerly → merchant's bank, with the error code if any | 1 · rules | Bottom rung: each system reports a status or an error code; the rule reads them in order |
| Extract the clues from free text (incomplete forms, free-message channel, very recent payments typed by hand: "twelve hundred", "last Tuesday", "last week's payment") | 3 · pretrained model | Rules catch IDs and formatted amounts, not loose wording; classical ML would need labelled tickets we do not have |
| Rank the candidate transactions and decide to abstain | 2 · classical ML (score on amount, date and name gaps, with a threshold) | Rules can filter candidates but cannot rank near-ties or give a confidence to abstain on |
| Summarise the account history and past tickets | 3 · pretrained model + retrieval, scoped to the merchant | Rules can list the last tickets, not say which ones matter for this question |
| Draft the reply | 3 · pretrained model, starting from the team's stock phrases, grounded on the matched transaction and the policy clause; references filled in from the ledger, never retyped | One template per status covers a single question; merchants mix questions and write loosely. The templates stay as the fallback |
| Policy guard: never promise a refund or a chargeback | 1 · rules (block list + clause lookup) | Bottom rung: the model is not trusted with money |
| **The MVP** | **4 · hybrid** | Each part sits on its own rung |

## 6. Where it lives (integration surface)
A side panel inside the ticket view the agents already use, filled when the ticket arrives so it is ready before the agent opens it (under 30 s *(g)*). Format: open account flags first (bank change in progress, contract, terms), then the matched transaction card (amount, date, counterparty, where it is stuck, why it matches), the account summary, the draft. Fallback: no confident match, or the copilot is down → the panel says so and the ticket works exactly as today. Log: seen by the agent, the QA reviewer and the Head of Support.

## 7. Success criterion — one sentence
> By Session 5, on our 200-ticket eval-set, handling time falls by at least 38 % on the tickets where the copilot proposes a match (two graders handle each ticket, timed, with and without the copilot) — and no more than 0.5 % of those tickets end with a wrong transaction in the approved reply.

The 38 % and the 0.5 % are the flip point of `02_investment_memo.md`. It assumes the copilot proposes a match on at least 70 % of tickets, as in the 02 base case.

## 8. Risks and rollback trigger
- Top risks: the agent trusts a wrong match and tells the merchant the wrong status or amount · a flag on the account record is missed (bank change in progress) and money goes to the old bank · a merchant's data appears in another merchant's ticket · a draft promises a refund or a chargeback · the copilot abstains too often and saves no time · time saved stays near the 30 % base case, below the flip point.
- **Rollback trigger (one line):** more than 0.5 % of sent replies citing the wrong transaction in a week, or any draft showing another merchant's data → the Head of Support turns drafts off for everyone the same day.

---
*v2 only — after the users. Evidence numbers (#) refer to the "What we heard" table in `03_user_research.md`. The usability test on the prototype is still to run.*

## 9. What the users changed
| Change | Evidence (who said / did what) |
|---|---|
| Step 2 is about **where the payment is stuck**, not only which payment it is: the panel shows the payment's position from the payer's bank to the merchant's bank, with the error code if any | A: the longest part is finding "where in the flow the payment got stuck", across tools that "don't really talk to each other" (#4); B: searching across the tools is the longest part (#5) |
| The **exact-lookup rule runs first, but it is not the main path**: the contact form's fields are optional and often incomplete, so clue extraction, ranking and "no confident match" stay at the core. On "no confident match", the panel suggests the question to ask the merchant (reference, customer name, time of payment) | The fields exist but are often incomplete, and agents contact the merchant again (A, #1); C can send a ticket without them, and a missing field means one more exchange and a restart (#2); B: "the customer talks about last week's transaction, and he has three" (#3); the company keeps the fields optional on purpose (B, #16) |
| The account summary shows **open flags first** (bank change in progress, contract not renewed, terms not accepted) | A's last error: she missed a "warning: information being updated" note on a bank change and the payment went to the old bank (#6) |
| The draft **fills in references from the ledger**, never retyped, and starts from the team's stock phrases | B checks for about 5 min per ticket that she "didn't get the number wrong" and must not "copy the line below" (#7); A and B copy-paste the same phrases (#8) |
| The way back gains **"hand to a referent or to legal, with the pre-read attached"** | A escalates to a referent and to legal for contract questions; B passes the ticket up when she cannot find the payment (#9) |
| The out-of-scope list grew: **"how do I" questions** answered from the documentation are a WON'T | A's one change: the many "how do I do this" tickets, answered from the docs, not the ledger (#10) |
| The users who gain the most are **new agents**, named in the persona | B: first ticket about an hour, now 5 minutes; A: helping new agents takes "twice as long" (#11) |
| The eval-set gains two segments: **open account flags** and **payments touched by an offer or a cashback** | A's bank-change error (#6); cashback and discounts create cent-level differences that block payouts (A, B), and problems came after commercial offers (C) (#15) |

The success criterion did not move: users do not set the threshold.

## 10. What they could not decide
- **The threshold** (38 % of handling time saved, ≤ 0.5 % wrong transactions): it is the flip point of `02_investment_memo.md`; the timed test on the eval-set decides it.
- **Whether the copilot is right often enough** (match precision, coverage): the 200-ticket eval-set decides, not opinions.
- **How many tickets carry an exact reference**, so how far the rule goes before the model is needed: the users only say "not always" (#1, #3); measured on 200 real ticket forms, not asked.
- **What a reply may say about Ledgerly's own mistakes**: agents keep replies generic and do not admit errors (#13). The Head of Support decides with Legal; until then the draft states only what the ledger shows and never invents a cause.
- **The legal basis for payer data and the LLM sub-processor**: the DPO decides (governance.md).