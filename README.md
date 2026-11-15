# Team Ledgerly — Copilot that drafts, never sends

**Course:** Data & AI Product: From Diagnosis to Delivery (MSA-DAT07-04) · Albert School · shared project with Agentic Workflows
**Cohort:** M2-INTER-1

## Team
| Name | Git handle |
|---|---|
| Dhia Ben Cheikh | @dhiabencheikh |
| Saumya Joshi | @sjoshi-rgb |
| Louise Caquelin | @lcaquelin |
| Santiago Pastrana | _to be filled_ |

## Our agent
- **Starting point:** P2 — Agent-assist copilot, B2B payments fintech
- **The company:** Ledgerly (invented name), a B2B payments platform · 800 merchant customers (measured, P2) · 12,000 support tickets/month (measured, P2) · ~18 tier-1 agents (guess: 12,000 tickets ÷ 21 working days ÷ ~32 tickets per agent per day, the rate in the Paylio case, S2 slide 37)
- **The job, in one sentence:** When a merchant opens a support ticket, the copilot pre-reads the account, its transactions and past tickets, producing a draft reply and the matched transaction(s), with evidence, for the human agent to review.
- **Trust level per step** (same as `03_product_brief.md` §2):
  - Read the ticket and extract the clues (amount, date, payer, reference): **L4** — read-only, no customer impact
  - Find the transaction and where it is stuck: **L2** — shown with its evidence; the agent confirms, or the copilot says "no confident match"
  - Summarise the account (open flags first) and past tickets: **L1** — a summary with a link to each source
  - Check the policy: **L1** for the clause quote · **person only** for any refund, chargeback or fee decision
  - Draft the reply: **L2** — the agent edits and approves every draft
  - Send the reply, or any refund, chargeback or money movement: **person only** — the copilot never sends and never moves money · the log is written automatically (**L4**)
- **One thing it must never do:** send anything to the customer itself, or present a transaction match it is not confident about (it abstains instead).

## Repository structure
One numbered file per session. Every member authors commits in at least four of the numbered files.

| File | Session | Status |
|---|---|---|
| `00_pitch.md` | before S3 — only if you bring your own idea | not needed (we start from P2) |
| `01_problem_statement.md` | S1–S2 — Assignment 1 | v1 — Assignment 1 |
| `governance.md` | created for Assignment 1, one line added every session | v3 — Sessions 1–3 (Session 3: data audit, purpose, isolation, gaps, trust level per step) |
| `02_sizing.xlsx` | S2 — Assignment 2 | v1 — Assignment 2 (base case: €10 per ticket) |
| `02_investment_memo.md` | S2 — Assignment 2 | v1 — Assignment 2 (no-go this year; flip point: 38 % of handling time saved) |
| `03_product_brief.md` | S3 — Assignment 3 | v2 — after three interviews and one usability test |
| `03_ai_lean_canvas.md` | S3 — Assignment 3 | v1 — Assignment 3 |
| `03_user_research.md` | S3 — Assignment 3 | v1 — three interviews (role-play) and one usability test with A and B |
| `03_prototype_link.md` | S3 — Assignment 3 | v1 — link and prompt of the mockup v0.1 tested with A and B |
| `A3_interviews_transcripts/` | S3 — Assignment 3 | transcripts in English, French originals (PDF) |
| `spec.md` | S3 skeleton, completed in S4 and final | skeleton v0 — Assignment 3 |
| `evals/eval_set_v0.csv`, `evals/README_eval_set.md` | from S3 | v0 — 20 invented cases, labels to be checked by hand by two people |
| `prototype/mock_up_prototype/` | from S3 | mockup v0.1 (HTML and screenshot), the version tested with A and B |
| `04_architecture.md` | S4 | |
| `05_metrics.md` | S5 | |
| `06_ab_protocol.md` | S6 | |
| `07_operations.md` | S7 | |
| `08_launch_memo.md` | S8 | |
| `product_brief.md` | final | |

## Rules
- Commit with your own Git account: the individual question at the oral is about a commit you signed.
- Tag the final version `v1.0` before the first oral of your cohort. No commits after the first oral starts.
