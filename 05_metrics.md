# 05 · Metrics — Team Ledgerly · Ledgerly agent-assist copilot

> Session 5 deliverable. Five sections = the five moves of the session. Every number traces to a file already in the repo (`02_sizing.xlsx`, `evals/report_v0.md`) — no new numbers appear here.

## 1 · Place the number — the stack for your agent
| Level | Question | Your metric | Value today (or "not yet") | Produced by | Owner | Clock |
|---|---|---|---|---|---|---|
| 5 Business | does it move the P&L? | Cost per resolved ticket (`€10.00` base, `€5.63` agent time; `02_sizing.xlsx`) & wrong-answer error cost (`€25` status / `€200` refund) | Not yet (projected `€8.00` at 66.7 % coverage / `€7.60` at 80 % coverage) | Finance & ticketing data (post-launch) | CFO / Head of Finance | Months |
| 4 Product | does the user adopt it and get the job done? | Handling time reduction on matched tickets (target ≥ 38 %; `02_sizing.xlsx` base 30 %) & 7-day reopen rate | Not yet (usability role-play only: 3–5 min vs 10–40 min) | Online A/B then production logs | Product Manager | Weeks |
| 3 Guardrails & responsible AI | does it stay inside the lines — for everyone? | Drafts on human-only tickets (`0`), cross-merchant leaks (`0`), unsupported evidence lines (`0`), parity across FR/EN & flagged accounts | `0 / 50` policy misses & `0` cross-merchant leaks (`evals/report_v0.md`) | Adversarial set offline + 5 % weekly QA audit | PM + DPO + Head of Security | Days |
| 2 AI system | does the workflow complete the task? | Drafts sendable without editing (`40.0 %` overall; `60.6 %` on eligible tickets) & proposed match coverage (`66.7 %` vs `70 %` target) (`evals/report_v0.md`) | `60.6 %` sendable as is (`20 / 33` eligible); `66.7 %` match coverage (`22 / 33`) (`evals/report_v0.md`) | Offline eval-set + two human graders | AI Engineer | Hours |
| 1 Model | is the component right? | Router accuracy (`86.0 %`, `43 / 50`) & ledger lookup match precision (`100.0 %`, `22 / 22`) (`evals/report_v0.md`) | `86.0 %` routing accuracy; `100.0 %` match precision (`evals/report_v0.md`) | Offline eval-set & deterministic assertions | ML / Backend Engineer | Seconds |

## 2 · Decide when to stop — the stop criterion
*"We stop improving **router accuracy** at **90 %** (up from 86.0 % in `report_v0.md`) because **proposed match coverage** (Level 2, target ≥ 70 %) stops responding once `RF-\d+` lookup and approximate-amount tie-breaking are added, and the next point of router tuning would cost **two engineering weeks of manual phrase labelling** while `02_sizing.xlsx` shows the business case depends on coverage and time saved rather than routing edge cases."*

- **Component metric and value:** Router accuracy at `90 %` (currently `86.0 %` in `evals/report_v0.md`); ledger lookup match precision at `≥ 98 %` (`spec.md` done criterion; currently `100.0 %` in `evals/report_v0.md`).
- **The level-above metric that stops responding (or the action threshold):** Level-2 proposed match coverage (`≥ 70 %` criterion in `spec.md`, currently `66.7 %` in `evals/report_v0.md`) and Level-4 agent handling time saved (`30 %` base in `02_sizing.xlsx`, `≥ 38 %` brief target).
- **Cost of the next point (weeks, tokens, labelling, latency):** `€5,000` per model re-evaluation change (`02_sizing.xlsx` Inputs), `€30,000 / year` eval upkeep, plus engineering sprint weeks that delay the next-best project (unified account view, `€180,000 / year` hurdle in `02_sizing.xlsx`).
- **What is a floor, not a stop (any miss blocks the release):** `0` drafts promising a refund, chargeback, or dispute outcome (`0 / 50` in `evals/report_v0.md`); `0` cross-merchant data leaks (`governance.md`); and `0` evidence lines unsupported by the ledger (`spec.md` / `03_user_research.md` T1). Any single miss blocks the release.

## 3 · Choose what to protect — the hierarchy, by segment
| Kind | Metric | Numerator / denominator | Level | Lag | Source & owner |
|---|---|---|---|---|---|
| Primary (1) | First-contact resolution rate without 7-day reopening on copilot-assisted tickets | Assisted tickets closed and not reopened within 7 days / Total tickets where copilot proposed a match and draft | Level 4 (Product) | 7 days | Ticketing logs · Product Manager |
| Guardrail (1) | Wrong-transaction match rate reaching the merchant | Approved replies citing a wrong `TX-` or `VO-` ID / Total approved copilot-assisted replies (target `≤ 0.5 %` status, `≤ 0.8 %` refunds in `02_sizing.xlsx`; `≥ 98 %` match precision in `spec.md`) | Level 3–4 (Guardrail / Product) | Weekly audit (days) | 5 % weekly QA audit + ledger logs · Support QA & Head of Support |
| Guardrail (2) | Zero unauthorized money promises & zero cross-merchant leaks | Drafts promising refund/dispute outcomes or leaking another `merchant_id` / Total generated drafts (must stay `0 / 50` as in `evals/report_v0.md`) | Level 3 (Guardrail) | Pre-release + continuous | Policy filter & adversarial evals · PM + DPO + Security |
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
  > *"If the 7-day reopen rate on French tickets, flagged accounts, or high-volume merchants exceeds **1.5×** the baseline segment rate for two consecutive weeks — OR if a single wrong transaction match causes a payout to an outdated bank account or any cross-merchant leak occurs — the Head of Support immediately flips `COPILOT_DRAFTS_ENABLED = False` (dropping to L1 read-only mode) on that segment until the DPO and Support QA verify the root cause. **Owner:** Head of Support (reviewed monthly with DPO and Support QA)."*
- **How it could be gamed → the repair:**
  - *Gaming risk:* Optimising **draft acceptance ("sendable as is")** alone (`60.6 %` in `report_v0.md`) could cause the drafter to write generic, reassuring replies that agents accept quickly without checking the ledger, or cause agents to rubber-stamp drafts to hit their 32 tickets/day pace (`02_sizing.xlsx`).
  - *The repair:* We pair draft acceptance with **7-day reopen rate** (Counter-metric 1) and a mandatory **"Check in the ledger"** button (`03_user_research.md` T2) plus weekly 5 % human QA sampling of approved replies (`governance.md` Session 4).

## 4 · Derive the business metrics — three, with expected effects (the oral)
| Business metric | Baseline (from `02_sizing.xlsx`) | Expected effect (from `evals/report_v0.md` × the cost line) | Lag | Read date | It is a hypothesis about… |
|---|---|---|---|---|---|
| 1. All-in cost per resolved `Transaction & payout status` ticket | `€10.00` all-in (`€5.63` direct agent time; `02_sizing.xlsx` Inputs) | `€10.00 → €8.00` at current `66.7 %` match coverage (`evals/report_v0.md`) × `30 %` time saved (`02_sizing.xlsx` base); `€10.00 → €7.60` once `v2_changes` lift coverage to `80 %` (`02_sizing.xlsx` base), plus `€0.072` AI token/retry cost per draft (`€0.06 × 1.20`) | 1 month (monthly finance & volume close) | End of Month 2 of the A/B rollout | Lookup coverage + draft acceptance → handling time saved → unit cost reduction (two arrows) |
| 2. Tier-1 agent handling time & monthly ticket capacity | `31.7` tickets/agent/day across `18` agents (`12,000` tickets/month, `40 %` spent reading; `02_sizing.xlsx` & `spec.md`) | `-30 %` handling time on covered tickets (`02_sizing.xlsx` base; target `-38 %` in `spec.md`), freeing `8,424` ticket-equivalents in Year 1 on status tickets (`13,689` across all categories in `02_sizing.xlsx` Upside) | 2 weeks (weekly ticketing cohorts) | Week 4 of the A/B rollout | Pre-read accuracy & ledger evidence clarity → reduced cross-tool search and manual verification time |
| 3. Wrong-answer error cost & 7-day reopen rate (non-effect guardrail) | `0.5 %` wrong-match rate on status tickets at `€25 / error` (`0.8 %` at `€200 / error` on refunds/disputes; `02_sizing.xlsx` Inputs) | **Unchanged (`≤ 0.5 %` wrong-match rate, reopen rate within `±1.5` pts of control)** — stated as an expected non-effect; exceeding `0.5 %` wrong matches or `1.5×` segment reopen rate stops the rollout | 2–4 weeks (7-day reopen window + weekly QA audit) | Week 4 of the A/B rollout | Grounded ledger citations + L2 human confirmation + open-flag warnings preventing anchor bias |

**The metrics tree (`component → product → business`):**
```text
[Component · Level 1]                  [Product · Level 4]                   [Business · Level 5]
Router accuracy (86.0 % → 90 %)  ──┐
                                   ├──► Proposed match coverage (66.7 % → 80 %) ──┐
Lookup precision (100.0 % ≥ 98 %) ─┘    & Sendable-as-is rate (60.6 %)            │
                                                                                  ├──► Cost per resolved ticket (€10.00 → €7.60)
Evidence groundedness (0 false)  ─────► Handling time saved (-30 % to -38 %) ─────┘    & Year-1 gross work avoided (€84,240 status / €136,890 total)
                                                                                  │
Policy & tenant isolation (0/50) ─────► Wrong-match rate (≤ 0.5 %) & Reopens ────────► Error cost contained (€25–€200/error) & Zero GDPR breach
