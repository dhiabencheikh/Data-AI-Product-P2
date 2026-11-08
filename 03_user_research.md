# 03 — User research · Ledgerly agent-assist copilot

> Three conversations (about 20 min each), Mom Test rules: past behaviour, no pitching, never "would you use…?".
> All three are **role-played**: none of the three people works in payments support or for a payments platform. Each recording says so at the start. The conversations were held in French; quotes are translated from the transcripts. The scripts were done by an AI from MP3 files and can have some minor flaws in the transcripts.

## Who we talked to
| # | Who (role, company type — no personal data) | Real user or classmate in role? | Interviewer · note-taker |
|---|---|---|---|
| A | Tier-1 support agent at a B2B payments platform, experienced, trains new agents | Person in role (simulated, said at the start) | Team Ledgerly · transcript |
| B | Tier-1 support agent, 2–3 months in the job, just out of training | Person in role (simulated, said at the start) | Team Ledgerly · transcript |
| C | Merchant, customer of the platform for several years, has opened several tickets | Person in role (simulated, said at the start) | Team Ledgerly · transcript |

## Interview guide (as used — kept about the past)
**Support agents (A, B)**
1. Tell me about the last time a customer asked you about a payment. What happened, step by step?
2. How did you find the payment they meant? Which tools did you open, in which order?
3. How long did it take? Which part took the longest?
4. The last time you picked the wrong payment, what happened? How did you find out?
5. When you could not find it, what did you do? Who did you ask?
6. What have you already tried to go faster (notes, reply templates, shortcuts)?
7. If you could change one thing in that moment, what would it be?

**Merchant (C)**
1. Tell me about the last time you had a doubt about a payment. What did you do?
2. How did you describe that payment to support? (amount, date, customer name, reference?)
3. How long did you wait for the answer? How many exchanges did it take?
4. Was the answer right the first time?
5. If you could change one thing in that moment, what would it be?

*Avoided:* "Would you use an AI that…?" · "Do you like this idea?" · "How much would you pay?" — and we never showed or described the copilot.

## What we heard (facts, in their words)
| # | Quote or observed behaviour | Which part of our brief it confirms or contradicts |
|---|---|---|
| 1 | A: "the form already has fields with the information: the reference, when they have it, the amount, the customer" | **Contradicts** our guess that merchants describe payments loosely: the contact form already asks for the reference, the amount and the customer |
| 2 | C: the form has a drop-down list of his transactions (order reference, amount, date, customer name); "you can't send the ticket anymore if it's not all filled in"; very recent payments are not in the list and are typed by hand | **Contradicts** the same guess; free text remains for very recent payments and the free-message channel |
| 3 | B: "he gave us the amount, the transaction reference, and there you go, we more or less find it" | **Contradicts** step 2 as written: identifying the transaction is usually quick, so the exact-lookup rule should cover far more than 30–50 % of tickets |
| 4 | A: "we look at where in the flow the payment got stuck […] it means opening several tools. That, I'd say, is the longest part" | **Confirms** the pain at step 2, but moves it: the time goes into finding *where* the payment is stuck (payer's bank → platform → merchant's bank), across tools that "don't really talk to each other" |
| 5 | B: "searching for the information across all the tools is the longest. And second, it's checking" | **Confirms** the two pain steps: search across tools, then verify |
| 6 | A's last error: a merchant's bank change was in progress; the account record only had a note, "warning: information being updated"; she did not see it and the payment went to the old bank; money cannot be recalled, days of delay | **Adds** a risk we had not listed: a flag on the account record (bank change, contract, terms not accepted) that the agent misses. **Confirms** that a wrong answer costs more than time |
| 7 | B: "you mustn't copy the line below"; about 5 min per ticket checking "that I didn't get the number wrong" | **Confirms** the wrong-transaction risk and shows a verification cost we had not counted |
| 8 | A and B copy-paste stock phrases; B: "it's a shame it's so manual […] it doesn't write the reply for you" | **Confirms** the draft as a MUST; agents already "always write the same things" |
| 9 | A: "you must not tell the customer something wrong"; she escalates to a referent, and to the legal team for contract questions; B passes the ticket up when she cannot find the payment | **Confirms** the way back to a person; adds handing the ticket to a referent or to legal |
| 10 | A, the one thing she would change: the many small tickets, "where is my transaction, how long until I get the money", and the "how do I do this" questions | **Confirms** status tickets are a large share. The "how do I" questions are answered from the docs, not the ledger: outside our scope |
| 11 | B: her first ticket took about an hour, the same kind now takes 5 minutes; the manual is outdated. A: new agents get the simple tickets, and helping them takes "twice as long as doing it ourselves" | **Confirms** the problem and points to new agents as the users who lose the most time |
| 12 | B: on simple tickets, errors surface when the merchant writes again a week later: "well no, it still doesn't work" | **Confirms** reopened tickets as a counter-metric, and that nobody measures wrong replies today |
| 13 | A and B: replies stay generic and do not say when the platform made the mistake: "we won't necessarily tell them when we made a mistake" | **Question for governance**, not for users: what a draft may say about the cause of a delay |
| 14 | C: answer within 48 h, right the first time because the form had all the information; satisfied overall | **Confirms** the pain is on the agent's side (time), not the merchant's: we size the copilot on time saved, not satisfaction |
| 15 | C: problems came after big updates and commercial offers. A and B: cashback and discounts create cent-level differences that block payouts | **Adds** a segment for the eval-set: payments touched by an offer or a cashback |

## Usability test — one task, think aloud, don't help
**Prototype link:** see `03_prototype_link.md` · **Task given:** "Ticket T-48213: Studio Lune says it has not received Dupont's payment of about €1,200 from last week. Handle the ticket until the reply is sent."
**Testers:** A and B (the two support agents), same role-play.

| Tester | Finished without help? (yes / no) | Where they hesitated | What they expected instead |
|---|---|---|---|
| A | *(to run)* | | |
| B | *(to run)* | | |

## Desirability gate — do they want it?
- [ ] 2 of 2 finished the task without help
- [x] They told us what they did last time — not what they would do (A's last error, B's first ticket, C's last ticket)
- [ ] At least one said "I want this before…"
- [ ] Our out-of-scope list grew; our success criterion did not move

**Decision:** *(after the usability test)*
