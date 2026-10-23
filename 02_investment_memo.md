# 02 — Investment memo (one page)

**Recommendation:** NO-GO on building the copilot this year. Build the unified account view first, and reopen the copilot only if the S4–S5 prototype shows it removes at least 38 % of handling time on the tickets it covers, with wrong matches reaching merchants on no more than 0.5 % of them.

> Line one is the decision. Everything below is evidence for that line. Same base case as `02_sizing.xlsx`.

| €/year, year 1 | Pessimistic | Base | Optimistic | Expected value |
|---|---|---|---|---|
| Net annual value | −€163.9k | −€36.6k | €101.3k | −€34.0k |
| Probability | 0.25 | 0.50 | 0.25 | — |
| Do-nothing (value of the current process improving on its own) | €45.0k | €72.0k | €100.8k | — |
| Next-best project: unified account view (the hurdle) | €180k | €180k | €180k | — |

## 1. How much?
The copilot never answers a merchant on its own, so we size it as time saved, not tickets deflected. On 144,000 tickets a year it drafts on 70 % and saves 19.5 % of all handling time (the 40 % → 20 % target). At €10 a ticket that is €280.8k a year at full adoption, and €136.9k in year 1 while adoption ramps from 20 % to 75 %. **Measured:** ticket volume and the 40 % of time spent reading (P2). **Analogy:** €10 per ticket (Paylio, S2 slide 37). **The guess that matters:** time saved per covered ticket (base 28 %).

## 2. How sure?
Weighted 0.25 / 0.50 / 0.25, the expected value is −€34.0k; only the optimistic case is positive. Time saved per covered ticket flips the decision. Year 1 cannot beat do-nothing: that would take 50 % saved, more than the 40 % agents spend reading. At full adoption the base case nets €77.3k, and clearing the hurdle takes 38 %, almost all of the reading. S4 measures coverage and match precision on 200 labelled tickets; S5 times the same agents with and without drafts.

## 3. What if we're wrong?
The model is not the cost: tokens are €3.5k a year, the fixed lines €145k, led by supervision (€55k) and evaluation (€30k). The tail is in refunds, disputes and chargebacks: a wrong match costs €200 (€400 pessimistic), and at full adoption errors eat 60 % of the value created on these tickets. Leaving disputes out of the first release cuts the pessimistic year-1 loss to −€124.8k for €11.7k less base value. **Governance line:** confirming the wrong transaction, or showing another merchant's data, is a legal and reputational risk. Owners: Head of Support for wrong replies, Head of Security for data leakage, with the DPO advising.

## 4. Compared to what?
Doing nothing is worth €72k a year (agents get ~5 % faster on their own); the copilot's expected value is €106.0k below it. The same team could build a unified account view instead, with no AI, valued at €180k a year (a guess); neither the expected value nor the pessimistic case clears it. If the view is worth less than €77k, the copilot at full adoption wins. Both need the same ledger, payout and ticket connectors, so building the view first is not wasted work.

## 5. Build, buy or orchestrate?
**We orchestrate because** the hard part is matching loose descriptions against our own ledger and payout data, which off-the-shelf bots do not read, and payer data must stay under our merchant contracts. Scores: Build 3.4 · Buy 3.0 · Orchestrate 4.0. **We would buy** a vendor copilot that reads our ledger, keeps data in the EU and costs under ~€324 per agent per month (our €70k a year of build-specific costs over 18 agents).
