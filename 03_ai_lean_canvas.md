# 03 — AI Lean Canvas · Ledgerly agent-assist copilot

> One screen. Nine blocks from the classic Lean Canvas + five blocks that an AI product cannot skip. Short phrases, taken from 01, 02 and `03_product_brief.md`.

## The nine classic blocks
| Block | Our answer | Comes from |
|---|---|---|
| 1. Problem — top 3 pains | 40 % of handling time spent reading before answering · finding where a payment is stuck means opening tools that do not talk to each other · every number is checked by hand before sending | 01 · 03_user_research.md |
| 2. Users / customer segments | About 18 tier-1 agents like Inès (user) · Ledgerly's 800 merchants (who get the answer) | 01 (persona) |
| 3. Unique value proposition — one sentence | The account is already read when the agent opens the ticket: the payment the merchant means, with its evidence, and a draft the agent checks and sends | 01 (press release) |
| 4. Solution — the MUST features | The transaction and where it is stuck, with evidence, or "no confident match" · account summary, open flags first · draft reply with references filled in from the ledger · policy guard (never promise a refund or a chargeback) | 03 brief §3 |
| 5. Channels — where it lives | A side panel in the ticket view the agents already use, ready before they open the ticket | 03 brief §6 |
| 6. Value — what it is worth per year (base case, EV) | Base year 1: −€36.6k · expected value −€34.0k · €280.8k gross a year at full adoption · hurdle: unified account view, €180k a year | 02 |
| 7. Cost structure — the seven cost lines | Tokens ≈ €3.5k in year 1, with retries · integration €60k one-off (€20k a year) · evaluation €30k · supervision €55k (1 QA reviewer) · monitoring €20k · re-evaluation at model changes €20k · cost of wrong matches (€200 each on refunds and disputes) | 02 |
| 8. Key metric — the success criterion | Handling time −38 % on tickets with a proposed match, on the 200-ticket eval-set, with ≤ 0.5 % wrong transactions in approved replies | 03 brief §7 |
| 9. Unfair advantage — data or know-how nobody else has | Our own ledger, payout and ticket data, which off-the-shelf bots do not read and which must stay under our merchant contracts | 02 (build / buy) |

## The five AI blocks
| Block | Our answer | Comes from |
|---|---|---|
| 10. Data — sources, rights, gaps | Tickets, ledger, payouts, CRM, policy knowledge base · merchant contract (GDPR art. 6), payer data and LLM sub-processor to check with the DPO · gaps: disputes, large merchants, open account flags, offers and cashback, non-EUR, languages other than French and English | governance.md (Session 3 section) |
| 11. Model — rung per part | Exact lookup from the form's fields and the payment's position in the chain: rules · clue extraction from free text: pretrained model · ranking and abstention: classical ML · summary and draft: pretrained model with merchant-scoped retrieval · policy guard: rules · overall: hybrid | 03 brief §5 |
| 12. Evaluation — the eval-set and its size | `evals/eval_set_v0.csv`: 20 invented, hand-labelled cases now, 200 by Session 5; two graders per case | evals/ |
| 13. Human in the loop — trust level per step, way back to a person | L4 reading · L2 match and draft · L1 summary and clause · person only for send and money · way back: "no confident match" and "Not this one" open the ticket as today | 03 brief §2 |
| 14. Risks & governance — what it must never do, rollback trigger | Never sends to the merchant, never moves money or promises a refund, never shows a match without its evidence · rollback: > 0.5 % wrong transactions in sent replies in a week, or any cross-merchant data → drafts off for everyone the same day | governance.md |
