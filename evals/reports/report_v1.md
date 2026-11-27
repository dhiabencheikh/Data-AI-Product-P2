# Eval report v1 — Team Ledgerly · Ledgerly agent-assist copilot

**Date:** 27 November 2026   **Eval-set:** `evals/eval_set_v1.csv`, 100 cases (56 labelled "L2 draft", 44 person only)   **Prototype:** `/prototype`, mock drafter (no API key), switch `COPILOT_MODE=ON`
**Reproduce:** `python prototype/run_eval.py` (numbers below) · outputs in `evals/copilot_outputs/drafts_v1.csv` · grades in `evals/grading/grades_v1.csv`

## 1. The numbers against the criterion
The eval-set measures the part of the success criterion it can measure: coverage, match precision and the guardrails (`spec.md` done criteria). The time saved (−38 %, `03_product_brief.md` §7) needs people timed on real tickets: the A/B test measures it (`06_07` §1–§2).

| | Run 1 (prototype repaired, before the fixes below) | **Run 3 (final)** | Target (`spec.md`) |
|---|---|---|---|
| Coverage — drafts on the 56 tickets labelled "L2 draft" | 31 / 56 = 55.4 % | **49 / 56 = 87.5 %** | ≥ 70 % |
| Match precision — the draft cites the labelled transaction | 29 / 29 = 100 % | **47 / 47 = 100 %** | ≥ 98 % |
| Drafts on the 44 person-only tickets (refund, dispute, fee waiver, bank change with money sent, out of scope, isolation traps) | 0 / 44 | **0 / 44** | 0 |
| Drafts showing another merchant's data (5 isolation traps) | 0 / 5 | **0 / 5** | 0 |
| Draft or hand-over decision right | 75 / 100 | **93 / 100** | — |
| Sendable as is — human reference, golden 30 (two graders, see §3) | — | **9 / 17 = 52.9 %** of draftable golden tickets · 4 need an edit · 1 fail · 3 without a draft | — |
| Sendable as is — judge (Claude), all 100 (upper bound: the judge over-accepts) | — | 46 / 56 = 82.1 % | — |

**Verdict:** met on coverage (87.5 % vs 70 %), precision (100 % vs 98 %) and every floor (0 drafts on person-only tickets, 0 cross-merchant data, 0 money promises). By segment: French 7 / 8 and English 42 / 48 draftable tickets get a draft (87.5 % each, no gap); open-flag accounts 6 / 8.

## 2. What we changed between run 1 and run 3, and why
The prototype committed for Session 4 never drafted: the router read the whole ticket, ledger rows included, after training on 24 phrases (at least two of them copied from the eval-set), and stayed under the 0.70 gate on every ticket — 0 drafts on 50. The Session 4 figures (22 / 50 drafts, 86 % routing) were not produced by that code; this report replaces them.

| Cause found in run 1 | Component | Fix (each one is a line of `spec.md` v2) |
|---|---|---|
| Router trained on 24 phrases, reading the ledger rows, 2 phrases copied from the eval-set | `router.py` | Reads only the merchant's words; 346 training phrases in `prototype/data/router_training.csv`, none from the eval-set; C chosen by cross-validation on the training phrases only |
| The amount reader took the number of a reference (TX-90501) for an amount | `reader.py` | A number counts as an amount only if it is not part of a reference |
| No phrase with an angry tone, typos, "paid 20 minutes ago", follow-ups or informal French in the training phrases | `router.py` training data | Fragments of each kind added (cause-level, not copied from tickets) |
| The wrong form reference was written in the reply, and the policy check blocked it | `drafter.py` | The mismatch goes to the agent's panel, never into the reply (CHANGE-3) |
| No reply template when the ledger only says "failed" or "received" | `drafter.py` | Two templates added |

**Which tickets we looked at:** to write the parser we read the format of the inputs (not the outputs) of the 100 cases, and to find the causes above we read the reasons of the 25 misses of run 1 (L-07, L-09, L-15, L-16, L-23, L-28, L-30, L-32, L-36, L-37, L-45, L-51, L-58, L-60, L-61, L-64, L-65, L-67, L-70, L-72, L-76, L-77, L-83, L-96, L-99). The fixes are made by cause and no label was changed, but these tickets are now partly demo data: run 3 is not a clean test. The clean test is the shadow run on live tickets, gate of step 0 in `08_launch_memo.md`.

## 3. Who graded, and how
- **Automatic checks** (`run_eval.py`): draft or hand-over against the label, the cited transaction against the "Match TX-…" of the label, policy blocks.
- **Rubric grading** (`evals/grading/grades_v1.csv`): each of the 49 drafts graded on the five criteria of `evals/judge_rubric.md` by **Claude (AI assistant)**, on 27 November. 46 sendable, 1 needs an edit (L-96 links one of the two earlier tickets), 2 fail criterion 1 (L-07 and L-61 add "included in your next payout", which the ledger does not say). On the golden 30 (L-01 to L-30): 13 sendable, 1 fails (L-07), 3 without a draft, 13 right hand-overs.
- **Two human graders** (Louise and Dhia, independently, golden 30, 27 November — `evals/grading/grades_louise_L01_L30.csv`, `evals/grading/grades_dhia_L01_L30.csv`, side by side in `evals/grading/agreement_v1.csv`): **human–human agreement 27 / 30 = 90 %**; **human–judge agreement 26 / 30 = 86.7 %** against the human reference. The judge over-accepts drafts that leave part of the question implicit (L-03, L-04, L-11, L-26: `sendable` for the judge, `needs_edit` for the humans); criterion 3 of the rubric and the judge prompt were re-aligned once. The drafter and the judge come from the same model family, a known bias.

## 4. The three most frequent misses of run 3
| # | What went wrong | Tickets | Component | What it becomes in `spec.md` |
|---|---|---|---|---|
| 1 | Router below the 0.70 gate on informal or very recent payment messages | L-28, L-30, L-60, L-72 | `router.py` | Collect real merchant phrasing in the shadow run and retrain; never lower the gate on eval tickets |
| 2 | Whole-account blocks (terms, KYC) and refund-status questions below the gate | L-16, L-77, L-83 | `router.py` | Same; the account flag itself could route the ticket (rule) before the router |
| 3 | A reply that adds a sentence the ledger does not support | L-07, L-61 | `drafter.py` template "received" | The template says only what the ledger shows: remove "next payout" |

## 5. What is demo data and what is eval data
- **Training data:** `prototype/data/router_training.csv` (346 synthetic phrases, rebuilt by `make_router_training.py`). None comes from `evals/`.
- **Eval data:** `evals/eval_set_v1.csv` — 100 invented cases, labelled before the run; no label was changed after a run. The tickets listed in §2 have been looked at.

## 6. Next step (one line)
Run step 0 of `08_launch_memo.md`: two weeks of shadow mode on live tickets (a test set nobody has seen), two human graders on 30 live drafts with the re-aligned rubric, then the A/B.
