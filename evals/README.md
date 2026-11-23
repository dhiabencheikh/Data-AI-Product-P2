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
- **Golden subset:** 30 cases (`L-01` to `L-30`) stratified across normal status tickets, flagged accounts, refunds/disputes, and adversarial traps.
- **Human–human agreement (2 graders independent):** **`<xx> %`** (`<n> / 30` cases agreed before discussion; graded by `<Member 1>` and `<Member 2>`).
- **Human–judge agreement (on the same 30 cases):** **`<xx> %`** (`<n> / 30` cases agreed with the adjudicated human verdict; judge model: `<model name>`).
- **Disagreement analysis & re-alignment (`<date>`):** *<One sentence describing where the judge disagreed — e.g., "The judge initially over-accepted drafts that missed an open bank-change flag or quoted a bank decline code; we tightened Criterion 3 and Criterion 4 boundary examples in `judge_prompt.txt` on <date>." >*
- **Known bias note:** If the judge and drafter share the same model family, self-preference bias can slightly inflate `sendable` ratings; mitigated by requiring per-criterion ledger evidence quotes and weekly 5 % human QA sampling (`governance.md` Session 4).
