# 04 · Architecture — Team Ledgerly · Ledgerly agent-assist copilot

> Session 4 deliverable. Describes the actual 4-step hybrid prototype committed in `/prototype`.

## 1. One-line description
A deterministic workflow copilot that pre-reads a merchant's isolated ledger and account flags when a payment ticket arrives, drafting grounded replies with citations for tier-1 support agents to approve, edit, or escalate—never sending or moving money automatically.

## 2. The diagram
ticket (merchant_id + text)
│
▼
[1. router.py]  ──(category, confidence)──▶  [2. routing_rule.py]
(Rung 2: ML)                                 (Rung 1: Rules & Gate)
│
┌─────────────────────────────┴─────────────────────────────┐
│ confidence < 0.70 OR human-only (refund/dispute/fee/OOS)  │ pass (status / account_flag, conf >= 0.70)
▼                                                           ▼
⊘ ABSTENTION: Escalate to Human                           [3. drafter.py] (Rung 3: Isolated Lookup + Draft)
(No draft; agent handles manually)                                    │
┌───────────┴───────────┐
│ no match / ambiguous  │ 1 confident match + citations
▼                       ▼
⊘ ABSTENTION: NO_DRAFT     [4. policy.py] (Rung 1: Policy Check)
(Agent searches ledger)           │
┌───────────┴───────────┐
│ policy block          │ policy pass
▼                       ▼
⊘ BLOCKED: Show reason    ⊘ APPROVAL: Tier-1 Agent UI
(Never approvable)        (Confirm / Edit / Send)
│
▼
[Audit Log (L4)]

⏻ Override Switch: Head of Support (and on-call Tech Lead) can flip COPILOT_DRAFTS_ENABLED=False in config/feature flag to drop the entire system to L1 (read-only / no drafts) for all agents immediately.

## 3. Component table
| # | Component | Rung (1 rules · 2 classical ML · 3 pretrained model · 4 custom) | Pattern (chaining · routing · parallelization · orchestrator-workers · evaluator-optimizer · agent) | Trust level (L1–L4) | Checkpoint ⊘ (approval · abstention · sampling · none) | Metric observed |
|---|---|---|---|---|---|---|
| 1 | `router.py` (Ticket classifier) | 2 (classical ML: TF-IDF + Logistic Regression) | Routing | L2 | None (feeds gate) | 86.0 % routing accuracy on 50 cases |
| 2 | `routing_rule.py` (Confidence & risk gate) | 1 (rules: threshold `>= 0.70` & keyword/category rules) | Routing (conditional gate) | L4 (enforced deterministic gate) | **⊘ Abstention** (routes refund, dispute, fee waiver, bank-change holds & `<0.70` to human) | 100 % human-only abstention (0 drafts on 17 human-only cases) |
| 3 | `drafter.py` (Isolated lookup & draft) | 3 (retrieval + grounded template/LLM drafter) | Prompt chaining | L2 | **⊘ Abstention** (`NO_DRAFT` on 0 or >1 TX candidates) | 100 % match precision (22/22); 0 cross-merchant leaks |
| 4 | `policy.py` (Compliance & PII guard) | 1 (rules: regex & citation check) | Evaluator / gate | L4 (hard block) | **⊘ Approval** (Tier-1 agent must review, edit, and click Send) | 0 policy violations passed; 20/33 eligible drafts sendable as-is |

## 4. Workflow or agent?
Team Ledgerly is built as a **deterministic workflow**, not an autonomous agent[cite: 30, 40]. Every ticket follows a fixed, pre-drawn four-step path (`router` → `routing_rule` → `drafter` → `policy`) with hard gates between steps[cite: 30, 40]. Because Ledgerly handles B2B payments, disputes, and sensitive banking data, giving an autonomous agent open-ended tool loops would create unacceptable financial and compliance risks (such as promising unauthorized refunds or leaking cross-merchant records)[cite: 30, 40]. Moving one step up (e.g., allowing an LLM router or multi-step query planner) would require an automated SQL/ledger sandbox verified at >99.9 % isolation accuracy on at least 200 eval cases plus real-time automated rollback triggers.

## 5. Fallbacks
- **retrieval finds nothing:** `drafter.py` returns `NO_DRAFT` with reason *"No matching transaction found in requesting merchant's ledger"*; ticket opens in standard manual agent view[cite: 40].
- **the model's confidence is below the threshold:** `routing_rule.py` (`confidence < 0.70`) blocks drafting and routes the ticket directly to the human agent queue[cite: 40].
- **the policy checker blocks the draft:** `policy.py` flags `policy: "block"` with the exact rule violated (e.g., bank code leak or refund promise); the draft is suppressed and never approvable[cite: 40].
- **the API is down:** Because Rung 1–2 run locally and Rung 3 degrades cleanly to `NO_DRAFT` on timeout/error, the copilot panel displays *"Pre-read unavailable"* and the agent works the ticket normally as before[cite: 40].

## 6. The override switch ⏻
- **Who can switch it off:** Head of Support (primary business owner) and On-Call Engineering Lead (technical owner)[cite: 40].
- **Scope:** Everyone (global feature flag `COPILOT_DRAFTS_ENABLED = False` disabling draft generation across all 800 merchant queues while preserving read-only ledger links)[cite: 40].
- **Tested on:** 15 November 2026, by Team Ledgerly during Session 4 prototype verification (verified setting threshold/flag to off routes 100 % of tickets to `escalate` with zero drafts emitted)[cite: 40].

## 7. Data
- **Training / demo data (`prototype/router.py`):** 24 synthetic, author-written ticket snippets across 5 categories (`status`, `refund`, `dispute`, `account_flag`, `out_of_scope`) used solely to fit the TF-IDF + Logistic Regression classifier[cite: 40].
- **Evaluation data (`evals/eval_set_v0.csv`):** 50 invented cases (`L-01` to `L-50`) created and hand-labelled by the team prior to running any evaluation; **never used for tuning**[cite: 39, 40].
- **Personal data present?** No real merchant or customer PII is stored[cite: 39, 40]. Synthetic names, masked IBANs (`•• 2210`), and invented `TX-`/`M-` IDs are stored in the private/course Git repository accessible only to Team Ledgerly and course instructors (see `governance.md`)[cite: 40].

## 8. Eval result v0
*"60.6 % of eligible status/account-flag tickets (20/33; 40.0 % of all 50 eval cases) got a draft two graders would send without editing, with 100 % match precision and 0 human-only or cross-merchant errors — criterion was 70 % match coverage and >= 98 % precision."*[cite: 40]

## 9. What you would build next (3 lines max)
1. Add `RF-\d+` refund ID extraction and payer-name/date disambiguation in `drafter.py` to recover missed approximate-amount tickets (`L-07`, `L-14`, `L-28`).
2. Connect `drafter.py` to structured JSON ledger fixtures (`data/ledger.json`) rather than inline ticket text so field mismatches (`L-32`) are highlighted explicitly.
3. Wrap the 4-step pipeline in a lightweight Streamlit demo surface (Inbox + Eval tab) and expand `eval_set_v0.csv` to 200 cases for Session 5[cite: 11, 36, 39].
