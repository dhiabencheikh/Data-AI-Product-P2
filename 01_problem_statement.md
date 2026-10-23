# 01 — Problem statement
**Team:** Team Ledgerly (Dhia Ben Cheikh, Saumya Joshi, Louise Caquelin, Santiago Pastrana) · **Agent:** P2 · **Last updated:** 23 October 2026

> Every number says where it comes from: **measured**, **analogy** (a comparable, with its source) or **guess** (and how we will test it).

## 1. The problem in one sentence
Tier-1 support agents at Ledgerly, a B2B payments platform with 800 merchants, spend 40 % of their handling time reading transaction history and past tickets before they can answer any of the 12,000 tickets a month, which costs about €48k a month (≈ €576k a year) of fully loaded support cost; today they search the account, ledger, payout and ticket tools by hand and rebuild the account story on every ticket. Success looks like reading time cut from 40 % to 20 % of handling time, with no increase in replies that cite the wrong transaction.

| Number in the sentence | Value | Measured / analogy / guess | Source or test |
|---|---|---|---|
| Merchants | 800 | measured | P2 proposal (`02_sizing.xlsx`, "How to fill it" tab) |
| Tickets per month | 12,000 | measured | P2 proposal |
| Share of handling time spent reading | 40 % | measured | P2 proposal |
| Cost of a human-handled ticket | ≈ €10 all-in | analogy | Paylio case, S2 slide 37 (agents + team leads, QA, tools); the sizing guide gives €5–15 as the usual range. To replace with Ledgerly's loaded cost |
| Reading cost | ≈ €48k / month, ≈ €576k / year | derived | 12,000 × €10 × 40 % = €48k; × 12 = €576k. It is all-in cost, not agent salary alone: in the Paylio case, agent time is ≈ €5.6 of the €10 |
| Target reading share | 20 % | guess | timed sample of tickets, with and without the copilot — S5 metrics |
| Replies citing the wrong transaction | no increase | guess (target) | today's rate is unknown: QA reviews a sample of sent replies before launch to set the baseline (S5), then the A/B test tracks it (S6) |

What the target is worth: going from 40 % to 20 % saves 20 % of handling time, i.e. 12,000 × €10 × 20 % ≈ €24k a month (≈ €288k a year) before AI and error costs. This is the same calculation as the P2 example in the sizing guide; the net figure is in `02_sizing.xlsx`.

## 2. Problem tree — from symptom to cause
- **Symptom** (what people complain about): merchants wait too long for answers on payment questions, and a large part of each ticket goes on looking things up rather than answering (40 % of handling time, measured).
- **Problem** (what is actually going wrong): on every ticket, the agent has to reconstruct the account context and find the transaction the merchant is talking about before writing a word.
- **Root cause** (5 Whys):
  1. Why are replies slow? — 40 % of handling time goes into reading before answering.
  2. Why? — the answer depends on finding the right transaction(s) among hundreds on the account.
  3. Why is that hard? — merchants describe payments loosely ("the €1,200 payment from client X last week"), and the data sits in separate tools: the account record in the CRM, the ledger, payouts and past tickets.
  4. Why separate? — support tooling was built around the ticket, not the account; nothing summarises an account's recent history.
  5. Why was it never fixed? — our hypothesis, to confirm with the Head of Support: reading time was never counted as a cost, and nobody owns the integration of the support tools.
- **What would fix the cause:** two parts.
  - A unified account view, with the merchant's transactions, payouts and past tickets on one screen. This is a **process / tooling fix, not AI**. It removes the time spent switching between tools.
  - Matching a loose description to the right transaction, summarising the history and drafting the reply. This is **GenAI**, and it removes the reading time.

  The unified view is not in the do-nothing baseline (section 7): someone has to build it. We treat it as the non-AI alternative and the likely next-best project in `02_investment_memo.md`.

## 3. Is AI the right tool?
| Question | Our answer |
|---|---|
| Is there a rule that solves 80 % of it? | No, but a rule solves part of it. When the merchant gives a transaction ID, or an exact amount and date, a simple lookup finds the transaction (share of tickets: guess 30–50 %, to measure on 200 tickets). Free-text descriptions, summarising history and drafting can't be done with rules. So the rule runs first and AI handles the rest. |
| Is it a prediction / generation problem, or an organisational decision? | Generation (summary + draft) with retrieval (transaction matching). Refunds, disputes and fee waivers are organisational policies: the copilot can quote the policy but never decides. The human agent does. |
| Do we have the data — which, how much, who owns it? | Ticket history (12,000/month), the transaction ledger, payouts, past replies and the policy knowledge base, all held by Ledgerly. Merchant data is used under the B2B contract (still to check, see `governance.md`). Missing: a labelled set of ticket → correct transaction; we build 200 for S4. |
| What does one error cost — and who pays it? | A wrong match makes the agent tell the merchant the wrong status or amount, or advise the wrong refund or chargeback. The merchant pays first (wrong decision, lost time), then Ledgerly (rework, trust, churn, possible financial loss). It is worse than no draft, because the agent anchors on it. |

**Level chosen:** GenAI copilot at L2, not an agent. **Why not the level below:** rules and classical ML can match exact identifiers and rank candidate transactions, and we use them inside the matching step, but they cannot read a free-text ticket, summarise an account or draft a reply. **Why not an agent:** it reads several sources but takes no action; one input (ticket + account), one output (a draft for a human). An agent is only needed "where several systems and steps must chain" (S2 slide 10), and nothing here touches money.

## 4. Why this agent — the four selection questions
| Criterion | Our answer, one line |
|---|---|
| High frequency — is the work done every day or every hour? | 12,000 tickets a month, about 570 per working day (12,000 ÷ 21): every agent would use it on every ticket. |
| Bounded decision space — can we list its tools and outcomes on one slide? | Five read-only sources (account record, ledger, payouts, past tickets, policy knowledge base) and three outputs: summary, proposed match with evidence (or "no confident match"), draft reply. |
| Measurable success — can we say in one sentence whether it succeeded on one ticket? | Was the matched transaction correct, and was the draft sent with minor edits only? |
| Recoverable failure — if it is wrong, is the damage limited and reversible? | Mostly: a human reviews every draft before sending. The remaining risk is an agent trusting a wrong match, so the match must show its evidence and abstain when unsure. |

## 5. Press release (Working Backwards)
*Paris, 1 June 2027* — Ledgerly today announced that its support agents now answer merchant payment questions with the account already read for them. When a merchant opens a ticket, a copilot pulls the relevant transactions and past tickets, shows the transaction it believes the merchant means along with the evidence, and drafts a reply that the agent checks and sends. Agents now spend 20 % of their handling time reading instead of 40 %, and no reply leaves without a human approving it. "They found the payment I meant before I had to explain it twice," says the finance manager of one of Ledgerly's 800 merchants.

## 6. What would have to be true?
| # | Hypothesis | Measured / analogy / guess | How we will test it | Session |
|---|---|---|---|---|
| 1 | When the copilot proposes a transaction match, it is right ≥ 98 % of the time, and it still proposes one on ≥ 70 % of tickets (it says "no confident match" on the rest instead of guessing) | guess (both thresholds) | 200 labelled tickets run through the prototype: precision of proposed matches + share of tickets with a proposal. 98 % because a wrong match is worse than no draft (section 3); 70 % so that abstaining on everything cannot pass | S4 prototype |
| 2 | With the copilot, reading time falls from 40 % to ≤ 20 % of handling time | measured (40 %) / guess (20 %) | timed sample: the same agents on comparable tickets, with and without drafts | S5 metrics |
| 3 | Agents catch wrong drafts: replies citing the wrong transaction and reopened tickets do not increase, and CSAT is unchanged | guess | A/B by agent group, with the wrong-transaction rate as the counter-metric, against the QA baseline from section 1 | S6 A/B |

## 7. Do-nothing baseline
In 12 months, with nothing built:
- Ticket volume grows with the merchant base (guess: +20 %, to check against Ledgerly's merchant growth).
- Agents get somewhat faster with experience and better internal docs (analogy: the current process improves ~5 % a year, S2 slides 31 and 37). In the sizing sheet this is worth 5 % × 144,000 tickets × €10 ≈ €72k a year, the do-nothing value the copilot is compared with.
- No unified account view either: building it is a project in its own right, so we compare against it as an alternative (section 2), not count it here.

Reading cost goes from ≈ €576k to ≈ €657k a year (€576k × 1.20 × 0.95): cheaper per ticket, more expensive in total. The copilot has to beat this trajectory, not zero.
