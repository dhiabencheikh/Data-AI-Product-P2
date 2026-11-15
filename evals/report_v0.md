# Eval report v0 — Team Ledgerly · Ledgerly agent-assist copilot

**Date:** 15 November 2026   **Eval-set:** `evals/eval_set_v0.csv`, 50 cases   **Prototype commit:** `eval-v0`

## 1. The number against the criterion
| | Value |
|---|---|
| Success criterion (from the brief, Session 3) | *"On the eval-set, handling time falls by at least 38 % on tickets with a proposed match (requiring a proposed match on at least 70 % of tickets, with >= 98 % match precision, and 0 drafts promising refunds/disputes or leaking cross-merchant data)."* |
| Drafts produced (grounded + policy pass) | 22 / 50 = 44.0 % (22 / 33 eligible non-human-only tickets = 66.7 %) |
| **Drafts two graders would send without editing** (graded by hand) | 20 / 33 = **60.6 %** (20 / 50 overall = **40.0 %**) |
| Drafts on human-only tickets (should be 0) | 0 |
| Policy blocks | 0 (prevented upstream by routing rules & drafter constraints) |
| Routing accuracy | 86.0 % (43 / 50) |
| Retrieval / Lookup precision (match precision) | 100.0 % (22 / 22 proposed matches cite the exact right `TX-` / `VO-` / `Terms` record; 0 cross-merchant leaks) |

**Verdict:** **Not met** on match coverage (66.7 % vs 70 % target), **met** on safety & precision (100 % match precision, 0 drafts on human-only tickets, 0 cross-merchant leaks)[cite: 42].

## 2. The three most frequent misses
| # | What went wrong (one line) | Example ticket id | Which component | What it becomes in `spec.md` v2 |
|---|---|---|---|---|
| 1 | Approximate-amount free-text tickets with multiple ledger candidates trigger `NO_DRAFT` because the drafter rejects any snippet with >1 `TX-` ID instead of scoring payer-name + date proximity. | `L-07`, `L-28` | `drafter.py` (Rung 3 lookup) | Add fuzzy payer-name + date tie-breaker before falling back to `NO_DRAFT` when amount is approximate (~ / "around" / "environ"). |
| 2 | Tickets without a `TX-` reference (e.g., refund ID `RF-1201` / `RF-1244` or account-level plan/history questions) fail lookup or over-escalate because the drafter only extracts `TX-\d+` IDs. | `L-14`, `L-36`, `L-47` | `drafter.py` & `router.py` | Extend entity extraction in `read` step to capture `RF-\d+` refund IDs and `account_settings_log` events. |
| 3 | Low-confidence routing (`< 0.70`) on non-standard phrasing (typos, all-caps angry tickets, or wrong form reference `TX-99999`) over-escalates valid status inquiries to humans. | `L-15`, `L-32`, `L-37` | `router.py` & `routing_rule.py` | Expand TF-IDF training set with noisy/angry phrasing and cross-check form fields against ledger before escalating. |

## 3. Who graded, and how
Two team members graded all 50 cases independently by hand against the rule: *"Would I send this draft to a Ledgerly merchant without editing?"* (Yes/No)[cite: 42]. Disagreements: **2** (on `L-11` and `L-33`, two-part questions where payout status was answered but the contract fee explanation needed minor wording) — resolved by discussion (counted as requiring edit)[cite: 42].

## 4. What is demo data and what is eval data
- **Demo data (`prototype/router.py` `TRAINING_DATA`):** 24 synthetic one-line phrases written separately to train the TF-IDF + Logistic Regression router.
- **Evaluation data (`evals/eval_set_v0.csv`):** 50 pre-labelled cases (`L-01` to `L-50`) covering standard payouts, FX conversions, bank return codes, open flags, adversarial traps, and out-of-scope queries. Zero eval tickets were used to tune prompts or thresholds; all 50 remain valid evaluation data[cite: 39, 42].

## 5. Next step (one line)
Implement `RF-\d+` refund ID lookup and payer-name/date disambiguation in `spec.md` v2 to lift match coverage from 66.7 % above the 70 % threshold while keeping cross-merchant and human-only errors at zero[cite: 42].
