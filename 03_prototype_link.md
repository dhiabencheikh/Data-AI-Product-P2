# 03 — Prototype link · Ledgerly agent-assist copilot

> One clickable prototype of the surface (the copilot side panel inside the agent's ticket view), then tried by two of our three users (A and B) on one task, thinking aloud. Results: `03_user_research.md`, usability test.

- **Link:** https://claude.ai/artifact/DPC2VoJNzroT5WhLmGREoK
- **Same file in the repo:** `prototype/mock_up_prototype/03_mockup_v0.1.html`
- **Made with:** Claude, in a conversation (first version on a Claude Design canvas, then rebuilt as one HTML page)
- **Version:** v0.1, the version tested with A and B
- **Data:** all invented. No model behind it: every screen is scripted.

![Ticket T-48213 with the copilot panel](prototype/mock_up_prototype/03_mockup_v0.1.png)

## The prompt
The brief in three paragraphs, as given to Claude:

```text
Paragraph 1 — who uses it and for what job:
Inès is a tier-1 support agent at Ledgerly, a B2B payments platform with 800 merchants. On every payment
ticket she spends about 40 % of her time searching the ledger, payouts and past tickets to find the payment
the merchant means ("the €1,200 from Dupont last week"). Build the screen she works in: her ticket queue,
the open ticket, and a copilot side panel that has already read the account when she opens the ticket.

Paragraph 2 — what is on the screen (panels, buttons, the one thing it must never do):
Left: the queue of three tickets. Centre: the merchant's message. Right: the copilot panel with (1) the
transaction it believes the merchant means, with its evidence (amount, date, payer, why it matches, the
candidates it rejected) and two buttons, "Confirm this transaction" and "Not this one"; (2) a short account
history with past tickets; (3) a draft reply that appears only once the agent has confirmed the match, with
"Edit" and "Send". The copilot never sends anything to the merchant and never moves money: only the agent
presses Send.

Paragraph 3 — the rules (routing, what is "human only", the trust level):
Matching and drafting are L2: the copilot proposes, the agent confirms and approves. When the copilot is not
sure (several payments of the same amount, no payer named), it says "no confident match", proposes no draft
and the ticket works exactly as today. Refunds, chargebacks and fee decisions are human only: on a
chargeback ticket, show a "human decision only" banner, quote the policy clause, and block any draft that
promises an outcome. Use invented data only, in French, as the agents and merchants write.
```

**What changed after this prompt, in the same conversation:** the mockup was rewritten in English, then rebuilt after the interviews with the changes of `03_product_brief.md` §9: where the payment is stuck (payer's bank → Ledgerly → merchant's bank), open account flags first, references filled in from the ledger, "Hand to a referent with this pre-read", and a fourth ticket (T-48230, bank change in progress). First version, on the Claude Design canvas: https://claude.ai/artifact/BZA1JfgujRri4LGxnRndMC

## What you can click
Four tickets in the queue, each one showing one part of `03_product_brief.md`:
- **T-48213 · Studio Lune** — free message, no form fields → confident match with "where it is" (grouped transfer), "why this one", candidates ruled out, account history, draft with references filled in from the ledger, Send and log. **This is the task of the usability test.**
- **T-48219 · Boulangerie Ferrand** — three payments of €480 → "no confident match", no draft, the question to ask the merchant.
- **T-48224 · Garage Auclair** — dispute → "human decision only", the policy clause, a draft that promises no outcome.
- **T-48230 · Menuiserie Vidal** — open flag first (bank change) → no draft, hand to a referent.

Ways back to a person: "Not this one" · "Hand to a referent with this pre-read" · nothing reaches the merchant until the agent presses "Send".

## Task given in the test
> "Ticket T-48213: Studio Lune says it has not received Dupont's payment of about €1,200 from last week. Handle the ticket until the reply is sent."

What the testers found and what changes in v0.2: `03_user_research.md` (T1–T8) and `03_product_brief.md` §9.
