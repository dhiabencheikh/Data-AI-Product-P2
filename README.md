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

## How to run the prototype
Python 3.10 or later, from the repository root:
```
pip install -r requirements.txt
python prototype/run_eval.py                          # the 100-case eval-set → numbers of evals/reports/report_v1.md
python prototype/run_eval.py evals/eval_set_v0.csv    # the 50 cases of Session 4
python prototype/test_switch.py                       # rollback drill: ON → SUGGEST_ONLY → OFF
python prototype/pipeline.py                          # one invented ticket through the four steps
```
- The switch is the environment variable `COPILOT_MODE` (`ON` · `SUGGEST_ONLY` · `OFF`; anything else means `OFF`).
- No API key: the drafter fills templates from the ledger rows (mock drafter, as allowed in Session 4).
- Each run writes `evals/copilot_outputs/drafts_<set>.csv` (outputs, with empty `grader_1` / `grader_2` columns: a new run empties the human grades copied there, which are kept in `evals/grading/grades_louise_L01_L30.csv` and `evals/grading/grades_dhia_L01_L30.csv`) and a JSON-lines log in `prototype/logs/` (not in Git). What every file of `evals/` is for: `evals/README.md` §1.
- `prototype/data/make_router_training.py` rebuilds the router's training phrases (`prototype/data/router_training.csv`).

| File in `/prototype` | Step |
|---|---|
| `reader.py` | read: splits the merchant's words from this merchant's account rows, extracts the clues |
| `router.py` | 1 · router (rung 2: TF-IDF + logistic regression on the merchant's words) |
| `routing_rule.py` | 2 · routing rule (rung 1: person-only categories, account holds, confidence gate) |
| `drafter.py` | 3 · lookup in this merchant's ledger + draft (templates, FR / EN) |
| `policy.py` | 4 · policy check (no money promise, no bank code or IBAN, no reference from another account) |
| `pipeline.py` | the four steps behind the switch, plus the audit log |
| `config.py` | the switch `COPILOT_MODE` and the log path |
| `run_eval.py` · `test_switch.py` | the eval and the rollback drill |

## Repository structure
One numbered file per session. Every member authors commits in at least four of the numbered files.

| File | Session | Status |
|---|---|---|
| `01_problem_statement.md` | S1–S2 — Assignment 1 | v1 — Assignment 1 |
| `governance.md` | created for Assignment 1, one line added every session | final — Sessions 1 to 8 (Session 8: who signs the launch, the DPO's six conditions) |
| `02_sizing.xlsx` | S2 — Assignment 2 | v1 — Assignment 2 (base case: €10 per ticket) |
| `02_investment_memo.md` | S2 — Assignment 2 | v1 — Assignment 2 (no-go this year; flip point: 38 % of handling time saved) |
| `03_product_brief.md` | S3 — Assignment 3 | final v2 — after three interviews and one usability test |
| `03_ai_lean_canvas.md` | S3 — Assignment 3 | v1 — Assignment 3 |
| `03_user_research.md` | S3 — Assignment 3 | v1 — three interviews (role-play) and one usability test with A and B |
| `03_prototype_link.md` | S3 — Assignment 3 | v1 — link and prompt of the mockup v0.1 tested with A and B |
| `A3_interviews_transcripts/` | S3 — Assignment 3 | transcripts in English, French versions (PDF) |
| `04_architecture.md` | S4 — Assignment 4 | final — four steps, ⊘ checkpoints, three-position switch ⏻ tested on 27 Nov |
| `05_metrics.md` | S5 — Assignment 5 | final — five sections, numbers from `02_sizing.xlsx` and `evals/reports/report_v1.md` |
| `06_07_experiments_operations.md` | S6 + S7 — Assignment 6 + 7 (replaces `06_ab_protocol.md` and `07_operations.md`) | final — A/B protocol, monitoring, rollback, owners |
| `08_launch_memo.md` | S8 | final — Go to shadow mode and the A/B from 4 January 2027; full rollout only at −38 % |
| `spec.md` | S3 skeleton, S4 v2, final | final — v2 with CHANGE-1 to CHANGE-7 |
| `prototype/` | from S3 (mockup), S4 (code) | repaired and measured on 27 Nov (see above) |
| `evals/` | from S3 | 100 cases (`eval_set_v1.csv`), `report_v0.md` (corrected), `evals/reports/report_v1.md`, rubric, judge prompt, the judge's and the two human graders' verdicts (90 % / 86.7 % agreement) — file list in `evals/README.md` §1 |

The final product brief is `03_product_brief.md` (v2), as asked in Session 8; there is no separate `product_brief.md`.

## Rules
- Commit with your own Git account: the individual question at the oral is about a commit you signed.
- Tag the final version `v1.0` before the first oral of your cohort. No commits after the first oral starts.
