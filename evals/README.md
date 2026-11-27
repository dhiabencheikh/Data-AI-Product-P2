# Evals — Team Ledgerly · Ledgerly agent-assist copilot

> Session 5 deliverable: 100-case stratified evaluation set (`evals/eval_set_v1.csv`), binary grading guideline (`evals/judge_rubric.md`), LLM judge prompt (`evals/judge_prompt.txt`), and the two agreement rates on 30 cases.

## 1. What each file is for
The files the assignments ask for stay at the root of `evals/`, where the brief expects them (`eval_set_v0.csv`, `eval_set_v1.csv`, `README_eval_set.md`, `report_v0.md`, `judge_rubric.md`, `judge_prompt.txt`, this README). The files added on 27 November are sorted in three folders:
- `copilot_outputs/` — what the prototype produced on each test set (written by `python prototype/run_eval.py`);
- `grading/` — the verdicts of the judge (Claude) and of the two human graders, and their comparison;
- `reports/` — the eval report of the repaired prototype.

Paths below are relative to `evals/`.

| File | What it holds | Made by · when |
|---|---|---|
| `eval_set_v0.csv` | The 50 test tickets of Session 4 (`L-01` to `L-50`) with the expected output | Team · Sessions 3–4 |
| `eval_set_v1.csv` | The 100 test tickets of Session 5 (`L-01` to `L-100`), stratified by segment; rows `L-51` to `L-100` tagged synthetic in `origin`. The `origin` of `L-01` to `L-50` still says "label to check by hand": the labels were re-read for Session 5 but the column was not updated | Team · Session 5 |
| `README_eval_set.md` | How the tickets were built: columns, recipe, generation prompt, labelling rule | Team · Session 3 |
| `copilot_outputs/drafts_v0.csv` | What the repaired prototype produced on the 50 tickets of v0 (kept as the trace of the corrected `report_v0.md`) | `python prototype/run_eval.py evals/eval_set_v0.csv` · 27 Nov |
| `copilot_outputs/drafts_v1.csv` | What the prototype produced on the 100 tickets of v1; columns `grader_1` (Louise) and `grader_2` (Dhia) filled for `L-01` to `L-30`. A new run rewrites this file and empties these columns: the human grades stay in the two files below | `python prototype/run_eval.py` · 27 Nov |
| `grading/grades_v1.csv` | The judge's verdicts on all 100 outputs (rubric applied by Claude, AI assistant) | Claude · 27 Nov |
| `grading/grades_louise_L01_L30.csv` | Louise's verdicts on the golden 30, graded independently | Louise · 27 Nov |
| `grading/grades_dhia_L01_L30.csv` | Dhia's verdicts on the golden 30, graded independently | Dhia · 27 Nov |
| `grading/agreement_v1.csv` | The golden 30 side by side: both humans, the human reference verdict, the judge, and who agrees | Built from the three files above · 27 Nov |
| `judge_rubric.md` | The grading guideline: five yes/no criteria, verdicts `sendable` / `needs_edit` / `escalate` (and `fail`, `miss`) | Team · Session 5, re-aligned 27 Nov |
| `judge_prompt.txt` | The judge prompt: the rubric, copied, for an LLM judge | Team · Session 5, re-aligned 27 Nov |
| `report_v0.md` | Session 4 report, corrected on 27 November (the first prototype produced no draft) | Team · 15 Nov, corrected 27 Nov |
| `reports/report_v1.md` | The repaired prototype on the 100 cases: coverage, precision, guardrails, grading, misses | Team · 27 Nov |

## 2. Grading guideline ("sendable as is")
A draft is **`sendable`** only if all five binary criteria in `evals/judge_rubric.md` are **YES**:
1. **Ledger-grounded evidence:** every `TX-`, `VO-`, `RF-`, amount, date and stage matches the isolated `merchant_id` ledger row, with zero invented claims.
2. **Exact transaction / refund match:** the right single record (including `RF-` refunds and grouped `VO-` transfers), or `NO_DRAFT` when candidates tie.
3. **Answers the question & surfaces open flags:** answers every part of the merchant's question **explicitly** and surfaces any open account flag (`bank_change`, `contract`, `terms`) or account-setting cause.
4. **Strict financial & privacy guardrails:** zero promises of refunds, chargebacks, dispute outcomes or fee waivers; zero cross-merchant data; zero unmasked payer IBANs or bank decline codes.
5. **B2B tone & correct abstention:** polite, concise B2B tone; suggests the missing clue (`reference`, `customer`, `date`) when abstaining; abstains (`NO_DRAFT`) on out-of-scope queries.

Verdicts: `sendable` (5 YES) · `needs_edit` (1, 2 and 4 YES, 3 or 5 NO) · `fail` (1, 2 or 4 NO) · `escalate` (right hand-over, no draft) · `miss` (no draft on a ticket that deserved one; graders wrote it `fail` on a ticket without draft, counted as `miss`).

## 3. The two agreement rates (golden 30, L-01 to L-30, 27 November)
- **Human–human agreement: 27 / 30 = 90 %.** Louise and Dhia graded independently, without seeing each other's grades or the judge's. The 3 disagreements were all on criterion 3 (how complete the answer must be): L-03 (no money collected, said clearly?), L-04 ("check" or "update" the bank details?), L-26 (say that the newly verified account is used?). Reference verdict decided by the two graders: `needs_edit` for all three.
- **Human–judge agreement: 26 / 30 = 86.7 %** against the human reference (28 / 30 with Dhia, 27 / 30 with Louise). The judge disagrees on L-03, L-04, L-11 and L-26, always in the same direction: **it over-accepts drafts that leave part of the question implicit** (it said `sendable` where the humans said `needs_edit`).
- **What we changed, once (27 November):** criterion 3 of `judge_rubric.md` and `judge_prompt.txt` now asks for every part of the question to be answered explicitly, with the four tickets above as boundary examples. The judge's verdicts in `evals/grading/grades_v1.csv` are those of the first pass, before this change.
- **What it does to the numbers:** on the 17 draftable golden tickets, the humans find **9 sendable as is (52.9 %)**, 4 to edit, 1 fail (L-07) and 3 missed drafts; the judge said 13 sendable. The judge's 46 / 56 (82.1 %) on the 100 cases is therefore an **upper bound**; the human-referenced rate on the golden 30 is the number we defend.
- *Known bias:* the drafter's templates and the judge come from the same model family (Claude) — consistent with the over-acceptance above.

## 4. When the eval runs
The frozen 100 cases are re-run before every change of prompt, model, rules or knowledge base (`06_07` §3), with `python prototype/run_eval.py`. Labels are never changed after a run. Human graders re-grade a 5 % weekly sample plus every judge disagreement.
