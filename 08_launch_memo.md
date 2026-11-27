# Launch memo — Ledgerly agent-assist copilot — 27 November 2026

> One page. The decision on line one. Numbers, names, dates. Every number comes from `02_sizing.xlsx`, `evals/reports/report_v1.md`, `05_metrics.md` or `06_07_experiments_operations.md`.

## 1 · Decision
**Go** — to step 0 (shadow mode on live status tickets, 2 weeks), then step 1 (internal agents, then 5 % of status tickets) and step 2 (A/B on 50 % of `Transaction & payout status` tickets, 4 weeks), from **4 January 2027**. The next decision — ship, iterate or kill — is read on **1 March 2027** by the **Head of Support** and the **Product Manager**. Full rollout only if the A/B shows the **38 %** flip point of `02_investment_memo.md`.

**Why a go when 02 said no-go this year:** the 02 no-go was conditional — reopen the copilot if the prototype covers enough tickets, matches the right transaction and never touches money. The offline part is now met (87.5 % coverage, 100 % match precision, 0 forbidden outputs). The time saved can only be measured with agents on real tickets: the A/B is that measurement, and its kill rule protects the hurdle. The pilot's ledger, payout and ticket connectors are the ones the unified account view needs (02 §4), so the experiment does not delay the next-best project.

**Budget we ask for:** **€145k a year**, the fixed costs of `02_sizing.xlsx` (+ ≈ €3.5k of tokens). It pays for the QA reviewer who supervises (€55k), the integration (€20k amortised), the evaluation and graders (€30k), monitoring and on-call (€20k) and re-evaluation at model changes (€20k).

## 2 · Evidence
- **Eval v1** (100 cases; two graders on the golden 30, judge validated — agreement **90 %** human–human / **86.7 %** human–judge): coverage **49 / 56 = 87.5 %**, match precision **47 / 47 = 100 %**, **9 / 17** golden drafts sendable as is for the humans (52.9 %; the judge, which over-accepts, says 46 / 56 on all 100), against the criterion **"a proposed match on ≥ 70 % of draftable tickets with ≥ 98 % precision, and 0 drafts that promise money or show another merchant's data"** (`spec.md`, `evals/reports/report_v1.md`). French and English: 87.5 % coverage each.
- **Guardrails:** **0** drafts on the 44 person-only tickets, **0 / 5** cross-merchant isolation traps, **0** bank codes or IBANs; checked at every change (eval re-run) and on a 5 % weekly sample of approved replies. 2 drafts add a sentence the ledger does not support (L-07, L-61): fixed and re-run before step 1.
- **What the A/B will prove:** handling time on covered status tickets from **14 min** to **≤ 8.7 min (−38 %)**, without the 7-day reopen rate leaving ±1.5 pts of control in any pre-registered segment; ≈ **2,770 status tickets per arm** in 4 weeks (`~1,385` a week, `02_sizing.xlsx`; the per-arm minimum was not computed, optional); **4 weeks** because the 7-day reopen rate is the slowest guardrail (`06_07` §2).
- **Sizing:** base year 1 **−€36.6k** vs hurdle **€180k** (unified account view); EV **−€34.0k**; do-nothing trajectory **€72k** a year. At full adoption, 38 % saved clears the hurdle (`02_investment_memo.md`).

## 3 · Rollout steps
| Step | Scope | Duration | Gate (metric · threshold · read date) | Signs the next step |
|---|---|---|---|---|
| 0a | offline eval + rollback drill, laptop staging | done (27 Nov 2026) | coverage 87.5 % ≥ 70 % · precision 100 % ≥ 98 % · 0 forbidden output · switch drill PASS | Product Manager |
| 0b | shadow mode on live status tickets (drafts logged, never shown) | 4–15 Jan 2027 | two human graders on 30 live drafts · coverage ≥ 70 % · precision ≥ 98 % · 0 forbidden output · L-07 / L-61 fix re-run · DPO conditions closed (§5) — read 15 Jan | Product Manager + DPO |
| 1 | internal QA agents, then 5 % of status tickets | 18–22 Jan, then 25–27 Jan 2027 | 0 forbidden outputs · human-graded sendable ≥ 50 % on the weekly sample · p95 ≤ 4 s — read 29 Jan | Head of Support |
| 2 | the A/B, 50 % of status tickets | 1–28 Feb 2027 (4 weeks) | time saved ≥ 38 % → ship · 15–37 % → iterate · < 15 % → kill · guardrails green in every segment — decided 1 Mar 2027 | Head of Support + Product Manager |
| 3 | 100 % with a 5 % holdout | 6 months from March 2027 | monthly: four monitoring layers green, drift review | Head of Support |

## 4 · Rollback & the switch
Trigger: any draft promising money, any cross-merchant data, a missed bank-change flag on sent funds; a segment's 7-day reopen rate > 1.5× control for 2 weeks; human–judge agreement < 80 % or sendable < 45 % for 2 weeks; API errors > 1 % for 10 min · Who decides: **Head of Support** (at night: **on-call Backend / AI Engineer**) · Action: `COPILOT_MODE` → `SUGGEST_ONLY` (drafts visible, nothing can be sent) → `OFF` (no pre-read) · Time to execute: < 15 min · What people see: agents get "Copilot drafts paused — handle the ticket as usual"; merchants see no change · **Last tested: 27 November 2026, on the prototype (laptop staging, `python prototype/test_switch.py`, PASS), with Team Ledgerly. Next drill: 27 February 2027.**

## 5 · Owners — and who signs
| Decision | Owner | Written where |
|---|---|---|
| run an experiment on real users | Head of Support signs; the DPO reads | 06_07 §1–§2 · governance.md |
| read the weekly numbers and act | Product Manager | 06_07 §3 |
| press the switch | Head of Support; at night the on-call Backend / AI Engineer | 06_07 §4 · governance.md |
| approve a release (prompt, model, KB) | Product Manager, with the eval re-run | evals/README.md |
| keep the trace, answer a customer or a regulator | Lead Backend / Platform Engineer keeps it; Legal Counsel & DPO answer | governance.md |

**The DPO has read the protocol (27 November 2026) and validates it under six conditions** (`governance.md`, Session 8): controller / processor role and DPA clause for the LLM sub-processor · EU processing, zero retention and no training at the provider · data minimisation (masked IBANs, no decline codes) · merchant isolation in the data layer · one retention period (12 months) for traces and logs · a short DPIA and agents trained before step 0b.

**This launch is signed by the Head of Support and the Product Manager.**

## 6 · What we do not know yet
- **The time saved** (−38 % needed) — next experiment: the A/B of step 2, read on 1 March 2027.
- **How the router copes with real merchant phrasing** — 7 misses on informal or very recent messages (`evals/reports/report_v1.md` §4); next experiment: the shadow run of step 0b, a test set nobody has seen.
- **How many drafts agents will send without editing** — humans find 52.9 % sendable as is on the golden 30, mostly because answers leave part of the question implicit; next experiment: the re-aligned rubric on 30 shadow drafts (step 0b), then the edit rate in step 1.
