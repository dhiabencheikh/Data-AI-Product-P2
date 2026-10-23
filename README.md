# Team Ledgerly — Copilot that drafts, never sends

**Course:** Data & AI Product: From Diagnosis to Delivery (MSA-DAT07-04) · Albert School · shared project with Agentic Workflows
**Cohort:** M2-INTER-1

## Team
| Name | Git handle |
|---|---|
| Dhia Ben Cheikh | @dhiabencheikh |
| Saumya Joshi | @sjoshi-rgb |
| Louise Caquelin | _to be filled_ |
| Santiago Pastrana | _to be filled_ |

## Our agent
- **Starting point:** P2 — Agent-assist copilot, B2B payments fintech
- **The company:** Ledgerly (invented name), a B2B payments platform · 800 merchant customers (measured, P2) · 12,000 support tickets/month (measured, P2) · ~18 tier-1 agents (guess: 12,000 tickets ÷ 21 working days ÷ ~32 tickets per agent per day, the rate in the Paylio case, S2 slide 37)
- **The job, in one sentence:** When a merchant opens a support ticket, the copilot pre-reads the account, its transactions and past tickets, producing a draft reply and the matched transaction(s), with evidence, for the human agent to review.
- **Trust level per step:**
  - Read the account, transactions and past tickets (read-only): **L4** — automatic, no customer impact
  - Match the ticket to a transaction: **L2** — shown with its evidence; the agent confirms, or the copilot says "no confident match"
  - Draft the reply: **L2** — the agent edits and approves every draft
  - Send the reply, or any refund, chargeback or money movement: **L1** — human only
- **One thing it must never do:** send anything to the customer itself, or present a transaction match it is not confident about (it abstains instead).

## Repository structure
One numbered file per session. Every member authors commits in at least four of the numbered files.

| File | Session | Status |
|---|---|---|
| `00_pitch.md` | before S3 — only if you bring your own idea | not needed (we start from P2) |
| `01_problem_statement.md` | S1–S2 — Assignment 1 | v1 — Assignment 1 |
| `governance.md` | created for Assignment 1, one line added every session | v1 — Sessions 1–2 |
| `02_sizing.xlsx` | S2 — Assignment 2 | |
| `02_investment_memo.md` | S2 — Assignment 2 | |
| `03_product_brief.md` | S3 | |
| `04_architecture.md` | S4 | |
| `05_metrics.md` | S5 | |
| `06_ab_protocol.md` | S6 | |
| `07_operations.md` | S7 | |
| `08_launch_memo.md` | S8 | |
| `spec.md`, `product_brief.md` | final | |
| `/prototype`, `/evals` | from S4 | |

## Rules
- Commit with your own Git account: the individual question at the oral is about a commit you signed.
- Tag the final version `v1.0` before the first oral of your cohort. No commits after the first oral starts.
