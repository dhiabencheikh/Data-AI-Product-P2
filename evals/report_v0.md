# Eval report v0 — Team Ledgerly · Ledgerly agent-assist copilot

**Date:** 15 November 2026, corrected 27 November 2026   **Eval-set:** `evals/eval_set_v0.csv`, 50 cases   **Prototype commit:** `eval-v0`

> **Correction of 27 November.** The figures first written here (22 / 50 drafts, 86 % routing, 60.6 % sendable) were not produced by the committed code: run again, the `eval-v0` prototype gives **0 drafts on 50**. Its router read the whole ticket, ledger rows included, after training on 24 phrases, and stayed under the 0.70 gate on every ticket. The prototype was repaired; the full account, with the 100-case run, is `evals/reports/report_v1.md`. The table below gives both runs on these same 50 cases.

## 1. The number against the criterion
| | `eval-v0` prototype (15 Nov) | Repaired prototype (27 Nov) |
|---|---|---|
| Success criterion (brief, Session 3) | *"Handling time falls by at least 38 % on tickets with a proposed match; a proposed match on at least 70 % of tickets, ≥ 98 % match precision, 0 drafts promising refunds or leaking another merchant's data."* | same |
| Drafts produced (grounded + policy pass) | 0 / 50 | 24 / 50 |
| Coverage — drafts on the 27 tickets labelled "L2 draft" | 0 / 27 = 0 % | 24 / 27 = 88.9 % |
| Match precision | — (no draft) | 23 / 23 = 100 % |
| Drafts on the 23 person-only tickets (should be 0) | 0 | 0 |
| Policy blocks | 0 | 0 |

**Verdict:** the `eval-v0` prototype failed the criterion (no draft at all) while staying safe. The repaired prototype meets coverage and precision on these 50 cases; see `evals/reports/report_v1.md` for the 100 cases, the tickets we looked at, and the limits. The time saved is not measured by the eval-set: the A/B test does it.

## 2. The three most frequent misses (Session 4 analysis → `spec.md` v2)
Written in Session 4 from the design of the drafter; they became CHANGE-1 to CHANGE-3 of `spec.md` v2, now implemented.

| # | What went wrong (one line) | Example ticket id | Which component | What it becomes in `spec.md` v2 |
|---|---|---|---|---|
| 1 | Approximate-amount free-text tickets with several ledger candidates got no draft instead of a payer-name + date tie-break | `L-07`, `L-28` | `drafter.py` (lookup) | CHANGE-1: payer-name + weekday tie-break before `no_confident_match` |
| 2 | Tickets naming a refund (`RF-1201`, `RF-1244`) or an account setting were not looked up: only `TX-` ids were read | `L-14`, `L-36`, `L-47` | `drafter.py` & `router.py` | CHANGE-2: read `RF-` refund ids and account-setting events |
| 3 | Non-standard phrasing (typos, capitals, a wrong form reference `TX-99999`) over-escalated valid status tickets | `L-15`, `L-32`, `L-37` | `router.py` & `routing_rule.py` | CHANGE-3: lower gate with a valid reference and no risky word; fall back on amount + date + payer when the form reference is wrong |

## 3. Who graded, and how
In Session 4 no draft existed, so no draft could be graded. The rubric grading of the repaired prototype's drafts and the two human graders (90 % agreement) are in `evals/reports/report_v1.md` §3.

## 4. What is demo data and what is eval data
- **Demo data:** the 24 phrases of the `eval-v0` router (`TRAINING_DATA`), at least two of which were copied word for word from the eval-set (L-13, L-42): a leak, removed in the repaired prototype (`prototype/data/router_training.csv`, 346 phrases, none from `evals/`).
- **Evaluation data:** `evals/eval_set_v0.csv`, 50 cases (`L-01` to `L-50`), labelled before any run; no label changed since.

## 5. Next step (one line)
Grow to 100 cases (`eval_set_v1.csv`) and report the repaired prototype on them: `evals/reports/report_v1.md`.
