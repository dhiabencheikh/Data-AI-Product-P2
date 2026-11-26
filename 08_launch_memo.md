# Launch Memo — Ledgerly Agent-Assist Copilot

**Date:** November 26, 2026  
**Author(s):** Team Ledgerly  
**Status:** Conditional Go  

---

## 1. Executive Summary & Launch Decision
- **Decision:** **Conditional Go** — Ready for phased A/B rollout once the three pre-launch gates are closed: (1) audit log enabled for live tickets, (2) `RF-\d+` lookup & approximate-amount tie-breaking deployed to lift proposed match coverage from `66.7 %` to `≥ 70 %`, and (3) DPO sign-off on payer data & LLM sub-processor (`governance.md`).
- **Summary:** We are launching the **Ledgerly Agent-Assist Copilot** (L1/L2 hybrid side panel) for our 18 Tier-1 support agents handling ~12,000 tickets/month. It surfaces open account flags, identifies where a payment is stuck across the ledger/payouts/banks with computed evidence, and drafts grounded FR/EN replies—while keeping all money actions and final sends strictly human-only.

## 2. Target Users & Rollout Plan
- **Target Users:** Tier-1 support agents (approx. 32 tickets/day per agent), with highest expected impact for new agents.
- **In-Scope:** `Transaction & payout status` tickets (50 % of volume) and eligible FR/EN tickets with a single merchant account.
- **Out-of-Scope (Human-Only):** Refunds, chargebacks, fee waivers, "how do I" doc questions, multi-merchant tickets, non-FR/EN languages, and auto-send.
- **Rollout Phases:**
  - **Phase 1 (Weeks 1–2 — Pilot / 20 % A/B):** Enable for a subset of Tier-1 agents on `Transaction & payout status` tickets. Validate `p95` pre-read latency (`< 30 s`), 5 % weekly QA audit, and `0` policy/tenant leaks.
  - **Phase 2 (Weeks 3–4 — 50 % A/B Test):** Expand to 50 % of eligible tickets. Measure 7-day reopen rate, handling time reduction (target `-30 %` base / `-38 %` flip point), and segment parity (FR vs EN, flagged accounts, high-volume merchants).
  - **Phase 3 (Month 2+ — Full Rollout):** 100 % of eligible Tier-1 tickets if guardrails hold and unit cost tracks toward `€7.60–€8.00` per resolved status ticket (down from `€10.00`).

## 3. Success Metrics & Guardrails
*(Aligned with `03_product_brief.md` and `05_metrics.md`)*
- **Primary Product Metric:** First-contact resolution rate without 7-day reopening on copilot-assisted tickets; handling time reduction on matched tickets (`-30 %` base case to `≤ 9.8 min`; `-38 %` flip-point target to `≤ 8.7 min`).
- **Business Metric:** All-in cost per resolved status ticket (`€10.00` baseline → `€8.00` at `66.7 %` coverage, `€7.60` at `80 %` coverage).
- **AI / Model Targets:**
  - Match precision: `≥ 98 %` (currently `100.0 %`, `22/22`)
  - Proposed match coverage: `≥ 70 %` (currently `66.7 %`, `22/33`)
  - Router accuracy: `≥ 90 %` stop criterion (currently `86.0 %`, `43/50`)
- **Guardrail Metrics & Rollback Triggers (Owner: Head of Support):**
  - **Wrong-transaction match rate:** `> 0.5 %` of sent replies in a week (status) or `> 0.8 %` (refunds/disputes).
  - **Cross-merchant data leak:** Any single occurrence (`0` tolerance).
  - **Unauthorized money promise:** Any draft promising a refund, chargeback, or fee waiver (`0` tolerance).
  - **Segment harm / reopen rate:** 7-day reopen rate on French tickets, flagged accounts, or high-volume merchants exceeds **`1.5×`** the baseline segment rate for two consecutive weeks.
  - **Action:** Head of Support immediately flips `COPILOT_DRAFTS_ENABLED = False` (dropping to L1 read-only mode) the same day until DPO and Support QA verify the root cause.

## 4. Launch Readiness Checklist
- [x] **Product & Prototype:** Side-panel flow tested in usability sessions (`03_user_research.md`), including "Confirm", "Check in the ledger", and "Not this one" actions.
- [x] **Evaluations:** Baseline evals passing (`0 / 50` policy misses, `0` cross-merchant leaks, `100 %` match precision in `evals/report_v0.md`).
- [ ] **Coverage & Audit Log:** `RF-\d+` / approximate-amount tie-breaking deployed (`≥ 70 %` coverage) and audit log active for live tickets.
- [x] **Rollback Plan:** `COPILOT_DRAFTS_ENABLED` kill switch ready for same-day disablement by Head of Support.
- [ ] **Governance & Compliance:** DPO sign-off on payer data and LLM sub-processor in `governance.md`.

## 5. Known Risks & Mitigations
| Risk | Likelihood | Impact | Mitigation |
| :--- | :--- | :--- | :--- |
| Agent rubber-stamps a wrong match | Med | High | L2 human confirmation, "Check in the ledger" button, computed-only evidence lines, and 5 % weekly QA audit + 7-day reopen tracking. |
| Missed open account flag (e.g., bank change) | Low | High | Open flags pinned at the top of the side panel before the transaction card. |
| Cross-merchant data leak | Low | Critical | Strict `merchant_id` query filtering on all ledger/CRM reads; `0`-tolerance rollback trigger. |
| Handling time saved stays below 38 % flip point | Med | Med | Monitor A/B handling time in Weeks 3–4; if below 30 % base case, re-evaluate vs. non-AI unified account view (`€180k/yr`). |

## 6. Post-Launch Next Steps (First 30 Days)
- **Week 1–2:** Run 5 % weekly QA audit on approved replies and monitor `p95` latency and `NO_DRAFT` handling time.
- **Week 4:** Read A/B test results on handling time, 7-day reopen rate, and segment parity (FR/EN, flagged accounts, high-volume merchants).
- **End of Month 2:** Review unit cost per resolved ticket (`€10.00 → €7.60–€8.00`) with Finance to confirm business case.