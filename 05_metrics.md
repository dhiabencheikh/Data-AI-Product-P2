# 05 · Metrics — Team Ledgerly · Ledgerly agent-assist copilot

> Session 5 deliverable. Five sections = the five moves of the session. Every number traces to a file already in the repo (`02_sizing.xlsx`, `evals/reports/report_v1.md`) — no new numbers appear here. Updated 27 November with the repaired prototype (`evals/reports/report_v1.md`; the first figures of `report_v0.md` were not reproducible).

## 1 · Place the number — the stack for your agent
| Level | Question | Your metric | Value today (or "not yet") | Produced by | Owner | Clock |
|---|---|---|---|---|---|---|
| 5 Business | does it move the P&L? | Cost per resolved ticket (`€10.00` base, `€5.63` agent time; `02_sizing.xlsx`) & wrong-answer error cost (`€25` status / `€200` refund) | Not yet (projected `€7.60` at the 80 % coverage of the `02_sizing.xlsx` base case; `€7.38` at the 87.5 % measured) | Finance & ticketing data (post-launch) | CFO / Head of Finance | Months |
| 4 Product | does the user adopt it and get the job done? | Handling time reduction on matched tickets (target ≥ 38 %; `02_sizing.xlsx` base 30 %) & 7-day reopen rate | Not yet (usability role-play only: 3–5 min vs 10–40 min) | Online A/B then production logs | Product Manager | Weeks |
| 3 Guardrails & responsible AI | does it stay inside the lines — for everyone? | Drafts on human-only tickets (`0`), cross-merchant leaks (`0`), unsupported evidence lines (`0`), parity across FR/EN & flagged accounts | `0 / 44` drafts on person-only tickets, `0 / 5` cross-merchant leaks, `0` money promises (`evals/reports/report_v1.md`) | Adversarial set offline + 5 % weekly QA audit | PM + DPO + Head of Security | Days |
| 2 AI system | does the workflow complete the task? | Drafts sendable without editing & proposed match coverage (`≥ 70 %` target) (`evals/reports/report_v1.md`) | `52.9 %` sendable as is on the golden 30 (`9 / 17`, human reference; the judge's `82.1 %` on 100 is an upper bound); `87.5 %` coverage (`49 / 56`) (`evals/reports/report_v1.md`) | Offline eval-set + rubric grading (two human graders to do) | AI Engineer | Hours |
| 1 Model | is the component right? | Draft / hand-over decision accuracy (router + routing rule) & ledger lookup match precision (`evals/reports/report_v1.md`) | `93 / 100` decisions right; `100 %` match precision (`47 / 47`) (`evals/reports/report_v1.md`) | Offline eval-set & deterministic assertions | ML / Backend Engineer | Seconds |

## 2 · Decide when to stop — the stop criterion
*"We stop improving **proposed-match coverage** at **87.5 %** (`evals/reports/report_v1.md`, above the 70 % criterion of `spec.md`) because **handling time saved** (Level 4) depends on coverage only up to the 80 % of the `02_sizing.xlsx` base case — beyond it the business case does not move — and the next point (the 7 remaining misses, all router confidence on informal phrasing) would cost **a new labelled phrase set and a re-evaluation** (`€5,000` per change in `02_sizing.xlsx`), while the risk sits elsewhere: the floors below."*

- **Component metric and value:** coverage `87.5 %` (`49 / 56`) and ledger lookup match precision `100 %` (`47 / 47`, criterion `≥ 98 %`), `evals/reports/report_v1.md`.
- **The level-above metric that stops responding (or the action threshold):** Level-4 agent handling time saved (`30 %` base in `02_sizing.xlsx`, `≥ 38 %` brief target), which assumes 80 % coverage in the base case: measured in the A/B, not offline.
- **Cost of the next point (weeks, tokens, labelling, latency):** `€5,000` per re-evaluation change (`02_sizing.xlsx` Inputs), `€30,000 / year` eval upkeep, plus engineering weeks that delay the next-best project (unified account view, `€180,000 / year` hurdle in `02_sizing.xlsx`).
- **What is a floor, not a stop (any miss blocks the release):** `0` drafts promising a refund, chargeback, or dispute outcome (`0 / 44` person-only tickets in `evals/reports/report_v1.md`); `0` cross-merchant data (`0 / 5` isolation traps); and `0` evidence lines or sentences unsupported by the ledger (`spec.md` / `03_user_research.md` T1 — 2 drafts fail this today, L-07 and L-61: a release blocker, fixed before step 1 of `08_launch_memo.md`). Any single miss blocks the release.

## 3 · Choose what to protect — the hierarchy, by segment
| Kind | Metric | Numerator / denominator | Level | Lag | Source & owner |
|---|---|---|---|---|---|
| Primary (1) | First-contact resolution rate without 7-day reopening on copilot-assisted tickets | Assisted tickets closed and not reopened within 7 days / Total tickets where copilot proposed a match and draft | Level 4 (Product) | 7 days | Ticketing logs · Product Manager |
| Guardrail (1) | Wrong-transaction match rate reaching the merchant | Approved replies citing a wrong `TX-` or `VO-` ID / Total approved copilot-assisted replies (target `≤ 0.5 %` status, `≤ 0.8 %` refunds in `02_sizing.xlsx`; `≥ 98 %` match precision in `spec.md`) | Level 3–4 (Guardrail / Product) | Weekly audit (days) | 5 % weekly QA audit + ledger logs · Support QA & Head of Support |
| Guardrail (2) | Zero unauthorized money promises & zero cross-merchant leaks | Drafts promising refund/dispute outcomes or leaking another `merchant_id` / Total generated drafts (must stay `0`: `0 / 44` person-only tickets and `0 / 5` isolation traps in `evals/reports/report_v1.md`) | Level 3 (Guardrail) | Pre-release + continuous | Policy filter & adversarial evals · PM + DPO + Security |
| Guardrail (3) | End-to-end copilot pre-read & draft latency (`p95`) | 95th percentile time from ticket arrival to draft panel render / All incoming tickets (must not slow down agent triage) | Level 2 (AI system) | Real-time (seconds) | Application logs · AI / Backend Engineer |
| Counter-metric (1) | 7-day ticket reopen rate (overall and on edited drafts) | Assisted tickets reopened by the merchant within 7 days / Total closed assisted tickets (catches agents rubber-stamping wrong drafts) | Level 4–5 (Product / Business) | 7 days | Ticketing logs · Product Manager |
| Counter-metric (2) | Handling time on `NO_DRAFT` / escalated human-only tickets | Median minutes spent by Tier-1 agents on tickets where copilot abstains / All unassisted tickets (from `governance.md` Session 1 Q6: must not degrade) | Level 4 (Product) | Weekly | Ticketing time-tracking · Head of Support |

- **Segments reported** (from the S3 audit in `governance.md` & `03_user_research.md`):
  1. **Ticket category:** `Transaction & payout status` (50 %), `Refunds, disputes & chargebacks` (30 %), `Account & other` (20 %) (`02_sizing.xlsx`).
  2. **Language:** `French` vs `English`.
  3. **Account flag status:** Accounts with open flags (`bank_change`, `contract`, `terms`, `fees`) vs `clean accounts`.
  4. **Payment complexity:** Standard single `EUR` payout vs `grouped transfers` (`VO-`), `cashback/offer cent-level differences`, and `non-EUR` conversions.
  5. **Merchant transaction volume:** Large merchants with frequent identical-amount payments vs standard merchants.
- **Fairness metric**, named: **Equalised error rates & selection-rate parity across segments** — specifically verifying that (a) `French` tickets receive confident drafts at a comparable rate to `English` tickets (selection-rate parity) and (b) the wrong-match and reopen rates on `French` tickets and `high-volume merchants` do not exceed `English` / `standard merchant` error rates (equalised odds).
- **Harm threshold** on the counter-metric, per segment, that stops the rollout — and its owner *(copied into `governance.md`)*:
  > *"If the 7-day reopen rate on French tickets, flagged accounts, or high-volume merchants exceeds **1.5×** the baseline segment rate for two consecutive weeks — OR if a single wrong transaction match causes a payout to an outdated bank account or any cross-merchant leak occurs — the Head of Support immediately moves `COPILOT_MODE` to `SUGGEST_ONLY` (L1: drafts visible, nothing can be sent) on that segment — `OFF` for a leak or a payout to an old account — until the DPO and Support QA verify the root cause. **Owner:** Head of Support (reviewed monthly with DPO and Support QA)."*
- **How it could be gamed → the repair:**
  - *Gaming risk:* Optimising **draft acceptance ("sendable as is")** alone (`52.9 %` human reference, `82.1 %` judge in `evals/reports/report_v1.md`) could cause the drafter to write generic, reassuring replies that agents accept quickly without checking the ledger, or cause agents to rubber-stamp drafts to hit their 32 tickets/day pace (`02_sizing.xlsx`).
  - *The repair:* We pair draft acceptance with **7-day reopen rate** (Counter-metric 1) and a mandatory **"Check in the ledger"** button (`03_user_research.md` T2) plus weekly 5 % human QA sampling of approved replies (`governance.md` Session 4).

## 4 · Derive the business metrics — three, with expected effects (the oral)
| Business metric | Baseline (from `02_sizing.xlsx`) | Expected effect (from `evals/reports/report_v1.md` × the cost line) | Lag | Read date | It is a hypothesis about… |
|---|---|---|---|---|---|
| 1. All-in cost per resolved `Transaction & payout status` ticket | `€10.00` all-in (`€5.63` direct agent time; `02_sizing.xlsx` Inputs) | `€10.00 → €7.60` at the `80 %` coverage of the `02_sizing.xlsx` base case × `30 %` time saved (`02_sizing.xlsx` base); `€7.38` at the `87.5 %` coverage measured (`evals/reports/report_v1.md`), plus `€0.072` AI token/retry cost per draft (`€0.06 × 1.20`) | 1 month (monthly finance & volume close) | End of Month 2 of the A/B rollout | Lookup coverage + draft acceptance → handling time saved → unit cost reduction (two arrows) |
| 2. Tier-1 agent handling time & monthly ticket capacity | `31.7` tickets/agent/day across `18` agents (`12,000` tickets/month, `40 %` spent reading; `02_sizing.xlsx` & `spec.md`) | `-30 %` handling time on covered tickets (`02_sizing.xlsx` base; target `-38 %` in `spec.md`), freeing `8,424` ticket-equivalents in Year 1 on status tickets (`13,689` across all categories in `02_sizing.xlsx` Upside) | 2 weeks (weekly ticketing cohorts) | Week 4 of the A/B rollout | Pre-read accuracy & ledger evidence clarity → reduced cross-tool search and manual verification time |
| 3. Wrong-answer error cost & 7-day reopen rate (non-effect guardrail) | `0.5 %` wrong-match rate on status tickets at `€25 / error` (`0.8 %` at `€200 / error` on refunds/disputes; `02_sizing.xlsx` Inputs) | **Unchanged (`≤ 0.5 %` wrong-match rate, reopen rate within `±1.5` pts of control)** — stated as an expected non-effect; exceeding `0.5 %` wrong matches or `1.5×` segment reopen rate stops the rollout | 2–4 weeks (7-day reopen window + weekly QA audit) | Week 4 of the A/B rollout | Grounded ledger citations + L2 human confirmation + open-flag warnings preventing anchor bias |

**The metrics tree (`component → product → business`):**
```text
[Component · Level 1]                  [Product · Level 4]                   [Business · Level 5]
Decisions right (93 / 100)       ──┐
                                   ├──► Proposed match coverage (87.5 %, base 80 %) ─┐
Lookup precision (100 % ≥ 98 %)  ─┘    & Sendable-as-is rate (52.9 %, humans)       │
                                                                                  ├──► Cost per resolved ticket (€10.00 → €7.60)
Groundedness (2 to fix)  ─────────────► Handling time saved (-30 % to -38 %) ─────┘    & Year-1 gross work avoided (€84,240 status / €136,890 total)
                                                                                  │
Policy & tenant isolation (0/44, 0/5) ─────► Wrong-match rate (≤ 0.5 %) & Reopens ────────► Error cost contained (€25–€200/error) & Zero GDPR breach
```

## 5 · Make the judge trustworthy — the evaluation plan
- **Eval-set v1**: `evals/eval_set_v1.csv`, 100 cases (200 in production), stratified by ticket category, language (FR / EN), open account flags, payment complexity, merchant size, isolation and adversarial traps; synthetic inputs tagged in `origin`, labels written by the team before any run; a golden set of 30 (L-01 to L-30) that never changes.
- **Grading guideline**: `evals/README.md` and `evals/judge_rubric.md` — five binary criteria with boundary examples. Two graders (Louise, Dhia) on the same 30 rows, independently: agreement = **90 %** (27 / 30); the 3 disagreements were on criterion 3 and settled as `needs_edit` (`evals/grading/agreement_v1.csv`). The figures written before 27 November could not have been measured and were withdrawn.
- **Judge**: prompt in `evals/judge_prompt.txt`. On 27 November the five criteria were applied to all 100 outputs by Claude (AI assistant): 46 sendable, 1 needs an edit, 2 fail criterion 1 (`evals/grading/grades_v1.csv`). Human–judge agreement on the same 30 = **86.7 %** (26 / 30) against the human reference; known bias: it over-accepts drafts that leave part of the question implicit (L-03, L-04, L-11, L-26), and the drafter's templates and the judge come from the same model family (Claude). Re-aligned on 27 November (criterion 3).
- **Cadence**: eval-set + judge on every change (prompt, model, rules, knowledge base) with `python prototype/run_eval.py` · human sample of 5 % of approved replies weekly (`governance.md` Session 4).
- *Optional, not graded* — red rows: the 18 adversarial rows of `eval_set_v1.csv` (prompt injection L-91, excessive agency L-92, hallucination trap L-93, payer personal data, cross-merchant lookups): 0 drafts on the person-only ones.
