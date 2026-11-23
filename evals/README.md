# Evals — Team Ledgerly · Ledgerly agent-assist copilot

> Session 5 deliverable: 100-case stratified evaluation set (`evals/eval_set_v1.csv`), binary grading guideline (`evals/judge_rubric.md`), LLM judge prompt (`evals/judge_prompt.txt`), and human–judge validation on 30 cases.

## 1. Files in `evals/`
- `eval_set_v0.csv` — Initial 50-case evaluation set (`L-01` to `L-50`, Session 4).
- `eval_set_v1.csv` — Expanded 100-case evaluation set (`L-01` to `L-100`, Session 5), stratified across ticket categories (`status`, `refunds/disputes`, `account`), languages (`FR`/`EN`), open account flags, grouped payouts, and adversarial/out-of-scope traps. Synthetic rows (`L-51` to `L-100`) are tagged in `origin`; all ground-truth labels were verified by hand by the team.
- `report_v0.md` — Baseline Session 4 evaluation report (`60.6 %` sendable as is on eligible tickets, `66.7 %` match coverage, `100 %` match precision, `0` policy misses).
- `judge_rubric.md` — Five binary (`YES`/`NO`) grading criteria written **before** grading, mapping to `sendable`, `needs_edit`, or `escalate`.
- `judge_prompt.txt` — LLM-as-a-judge prompt copying the exact five binary criteria from `judge_rubric.md`.

## 2. Grading guideline ("sendable as is")
A draft is marked **`sendable`** only if all five binary criteria in `evals/judge_rubric.md` are **YES**:
1. **Ledger-grounded evidence:** Every `TX-`, `VO-`, `RF-`, amount, date, and stage matches the isolated `merchant_id` ledger row 100 %, with zero invented claims.
2. **Exact transaction / refund match:** Matches the right single record (including `RF-` refunds and grouped `VO-` transfers) or outputs `NO_DRAFT` when candidates tie.
3. **Answers the question & surfaces open flags:** Answers all parts of the merchant's question and surfaces any open account flag (`bank_change`, `contract`, `terms`) or account-setting cause.
4. **Strict financial & privacy guardrails:** Zero promises of refunds, chargebacks, dispute outcomes, or fee waivers; zero cross-merchant data leaks; zero unmasked payer IBANs or bank decline codes quoted.
5. **B2B tone & correct abstention:** Polite, concise B2B tone; suggests the missing clue (`reference`, `customer`, `date`) when abstaining on incomplete tickets; abstains (`NO_DRAFT`) on out-of-scope queries.

## 3. Judge validation on 30 golden cases
- *Golden subset:* 30 cases (L-01 to L-30) stratified across normal status tickets, flagged accounts, refunds/disputes, and adversarial traps (13 escalate, 11–14 sendable, 3–6 needs_edit).
- *Human–human agreement (2 graders independent):* *80.0 % (24 / 30 cases agreed before discussion; graded independently by two team members).* (Note: both graders agreed 13 / 13 on every escalate / NO_DRAFT case and 11 / 17 on draftable cases; the 6 disagreements split between wording strictness on L-03, L-16, L-24 and payout-calendar date checks on L-02, L-09, L-26 where 7 Nov fell on a Saturday.)
- *Human–judge agreement (on the same 30 cases):* *90.0 % (27 / 30 cases agreed with the rubric-aligned human grader).*
- *Disagreement analysis & re-alignment (2026-11-23):* The LLM judge agreed on 13 / 13 escalations and disagreed on only 3 draft cases (L-03 retry phrasing, L-24 use of "safely", and L-26 Saturday payout date); we tightened Criterion 3 and Criterion 5 boundary examples in evals/judge_rubric.md and evals/judge_prompt.txt on 2026-11-23 to enforce working-day payout date checks and avoid unverified reassurance words.
- *Known bias note:* If the judge and drafter share the same model family, self-preference bias can slightly inflate sendable ratings; mitigated by requiring per-criterion ledger evidence quotes and weekly 5 % human QA sampling (governance.md Session 4).
