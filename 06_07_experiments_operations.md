# 06_07 — Experiments & operation · Team Ledgerly · Ledgerly agent-assist copilot

> Five sections = the five moves of Sessions 6 + 7. Every number traces to `02_sizing.xlsx`, `05_metrics.md`, or `evals/report_v0.md`. Every owner is a named role. Every threshold has a clock.

## §1 Prove the effect — hypothesis, unit, design (in words)

**Hypotheses** (one per business metric of `05_metrics.md §4` — each stated as a falsifiable outcome that exists with and without the copilot):

1. **All-in cost per resolved status ticket (`05_metrics.md §4` #1):**
   If we enable L2 copilot pre-reads and approval-gated drafts for Tier-1 agents on `Transaction & payout status` tickets (`6,000` tickets/month, `50 %` of volume in `02_sizing.xlsx`), then all-in cost per resolved status ticket moves from **`€10.00`** (`€5.63` direct agent time) to **`≤ €7.60`** at the `80 %` coverage of the `02_sizing.xlsx` base case (`87.5 %` measured offline in `evals/reports/report_v1.md`) by **end of Month 2** — without wrong-transaction matches exceeding **`0.5 %`** (`€25 / error`) and without the 7-day ticket reopen rate exceeding **`1.5×`** the control baseline on any pre-registered segment (`French`, `flagged accounts`, `high-volume merchants`).
2. **Tier-1 agent handling time & monthly ticket capacity (`05_metrics.md §4` #2):**
   If we show the grounded ledger pre-read and suggested draft in the agent sidebar on `Transaction & payout status` tickets, then median agent handling time on covered tickets drops by at least **`30 %`** (`02_sizing.xlsx` base; `38 %` brief target, vs today's `10–40 min` baseline where `40 %` of time is spent reading across tools) by **Week 4** — without handling time on `NO_DRAFT` / escalated human-only tickets increasing above control (`governance.md` Session 1 Q6).
3. **Wrong-answer error cost & 7-day reopen rate — non-effect guardrail (`05_metrics.md §4` #3):**
   If we require L2 human approval, ledger-cited evidence lines, and open-flag warnings (`bank_change`, `contract`, `terms`, `fees`) before sending any copilot-assisted reply, then the wrong-transaction match rate remains at or below **`0.5 %`** (`€25 / error` on status; `≤ 0.8 %` at `€200 / error` on refunds/disputes) and the 7-day reopen rate stays within **`±1.5` percentage points** of the control arm at **Week 4** — with **`0`** unauthorized refund/dispute promises and **`0`** cross-merchant data leaks (`0 / 44` person-only tickets and `0 / 5` isolation traps in `evals/reports/report_v1.md`).

**Unit of randomisation:** **The incoming ticket** (randomised 50 % treatment with copilot pre-read + draft vs 50 % control without copilot, stratified by language `FR`/`EN` and merchant account) — **because** `Transaction & payout status` tickets arrive at `~1,385` tickets/week (`6,000 / month` in `02_sizing.xlsx`), making ticket-level randomisation fast and high-powered, whereas randomising across only `18` Tier-1 agents (`9` per arm in `02_sizing.xlsx`) would leave too few clusters to detect a moderate gain.
- *Where treatment leaks:* Agents handling both arms can learn faster ledger-lookup habits or copy phrasing from treatment drafts onto control tickets (spillover), which slightly compresses the measured difference between arms (making our observed lift conservative). To monitor spillover, we track control-arm handling time week-over-week against pre-test baseline.

**Design & fallback plan:**
- **Primary design:** **50 / 50 randomised A/B test at the ticket level** on eligible `Transaction & payout status` tickets for **4 weeks** (after the offline eval of `evals/reports/report_v1.md` — `87.5 %` coverage, `100 %` match precision, `82.1 %` sendable as is — and two weeks of shadow mode on live tickets, step 0 of `08_launch_memo.md`), followed after full rollout by a **persistent 5 % holdout** (`governance.md`) to measure long-run drift.
- **What ticket-level A/B cannot see:** Agent-level learning spillover onto control tickets, multi-week fatigue or rubber-stamping after novelty wears off, and cross-ticket merchant satisfaction trends beyond the 7-day reopen window.
- **Fallback plan (if ticket-level randomisation cannot be wired in the ticketing UI):** Run **shadow mode** on 100 % of live status tickets for 2 weeks (logging copilot drafts without showing them to agents), followed by a **before/after rollout with a control group** (enabling the copilot on `English` status tickets first while keeping `French` status tickets as the concurrent control group, or alternating weeks).

## §2 Decide before — duration and decision rule

**Smallest improvement that still justifies the agent, and why:**
- **Minimum worthwhile lift:** **`−38 %` handling time saved** on covered status tickets — the flip point of `02_investment_memo.md` — with **`≥ 70 %` match coverage** (`87.5 %` offline in `evals/reports/report_v1.md`).
- **Why (`02_sizing.xlsx` and `02_investment_memo.md`):** at full adoption the base case (30 % saved) nets `€77.3k` a year, below the `€180k` a year of the next-best project (unified account view, the hurdle); clearing the hurdle takes 38 %. Between 25 % and 38 % the copilot beats doing nothing but not the alternative; below 15 % it does not pay for its `€30,000 / year` evaluation upkeep. The 02 memo wins over any other threshold (lower-numbered file).

**Slowest guardrail to read → how long we run:**
- **Duration: `4 weeks` (28 calendar days)** from test launch, fixed in advance (no peeking).
- **Why:** volume is not the constraint: `~1,385` status tickets arrive every week (`02_sizing.xlsx`), so each arm collects `~2,770` tickets in 4 weeks. The number of units per arm is not computed (optional in the brief: we did not use the `sample_size.xlsx` calculator). What fixes the duration is our slowest guardrail — **7-day ticket reopen rate** (plus the 5 % weekly human QA audit of wrong-transaction matches) — needs a full **7-day post-ticket window** after each weekly cohort closes plus two consecutive weekly reads (`Week 3` and `Week 4`) to rule out Week-1 novelty effects and catch Simpson's paradox on `French` and `flagged account` segments.

| Input (in words; the sample-size calculator of the course was not used — optional) | Value | Source |
|---|---|---|
| Baseline $p_0$ / mean (exists with and without agent) | `14 min` per payment ticket (`03_product_brief.md` §2, guess) (`10–40 min` range, `40 %` spent reading; `02_sizing.xlsx` / `05_metrics.md`) & `≤ 0.5 %` baseline wrong-match rate | `02_sizing.xlsx` & `05_metrics.md §1, §4` |
| Smallest rise / reduction worth acting on | `−5.3 min` (`−38 %`, the flip point); `−4.2 min` / `−30 %` is the base expectation in `02_sizing.xlsx` | `02_investment_memo.md` flip point |
| Two risks accepted (false win · missed win) | `1 in 20` (`α = 0.05`) · `1 in 5` (`power = 80 %`) | Course convention (Session 6) |
| **Units per group ($n$)** | Not computed (optional); the 4-week run gives `~2,770` status tickets per arm | `02_sizing.xlsx` volume × 4 weeks ÷ 2 arms |
| Volume per week | `~1,385` `Transaction & payout status` tickets/week (`6,000 / month` in `02_sizing.xlsx`) | `02_sizing.xlsx` Inputs |
| **Duration actually run** | **`4 weeks`** (`~2,770` status tickets per arm; 1-week post-close window so Week-3 reopens settle by end of Week 4) | Read date of slowest guardrail (`7-day reopen rate`) |

**Pre-registered segments** (exact list from `05_metrics.md §3` — reported separately on every read to prevent Simpson's paradox):
1. **Ticket category:** `Transaction & payout status` (primary test scope; `Refunds, disputes & chargebacks` and `Account & other` stay human-only / read-only in v1).
2. **Language:** `French` vs `English`.
3. **Account flag status:** Accounts with open flags (`bank_change`, `contract`, `terms`, `fees`) vs `clean accounts`.
4. **Payment complexity:** Standard single `EUR` payout vs `grouped transfers` (`VO-`), `cashback/offer cent-level differences`, and `non-EUR` conversions.
5. **Merchant transaction volume:** Large merchants with frequent identical-amount payments vs standard merchants.

**Decision rule, written on `2026-11-23` and aligned on the `02_investment_memo.md` flip point on `2026-11-27`, before the first unit (A/B from `2027-02-01`):**
- **Ship (100 % rollout on status tickets, keeping 5 % holdout) if:** At the Week-4 read date, median handling time on covered status tickets drops by **`≥ 38 %`** (`≥ 5.3 min` saved: the flip point of `02_investment_memo.md`), wrong-transaction match rate is **`≤ 0.5 %`**, 7-day reopen rate is within **`+1.5` pts** of control across every pre-registered segment, and **`0`** unauthorized money promises or cross-merchant leaks occurred.
- **Iterate (run one targeted 2-week cycle on prompt/lookup rules, same protocol) if:** Handling time drops by **`15 %–37 %`** (`−2.1` to `−5.2 min`; from 25 % it beats doing nothing but not the unified account view, which is re-compared before the cycle) with clean guardrails (`0` leaks/promises, wrong-match rate `≤ 0.5 %`), OR if overall metrics pass but one non-harmful segment (e.g., `non-EUR` or `grouped transfers`) shows elevated draft-edit rates (`> 50 %` edited) without breaching the reopen harm threshold.
- **Kill (revert to L1 read-only or turn off) if:** Handling time reduction is **`< 15 %`** at Week 4 (failing to cover `€30,000 / year` eval upkeep), OR `NO_DRAFT` handling time increases by **`> 15 %`** (slowing agents down on hard tickets), OR wrong-transaction match rate exceeds **`0.5 %`** without a single-rule fix.
- **Stop early ONLY if (`governance.md` harm threshold — never stop early on a good number):**
  1. **Immediate zero-tolerance stop (`< 15 min`):** Any single draft promises a refund/chargeback/dispute outcome, any cross-merchant `merchant_id` data is exposed, or a wrong transaction match causes a payout to an outdated bank account.
  2. **Segment circuit-breaker stop:** The 7-day reopen rate on `French` tickets, `flagged accounts`, or `high-volume merchants` exceeds **`1.5×`** the control segment baseline for **two consecutive weeks**.

## §3 Watch the four layers — monitoring and drift

| Layer | Metric (from `05_metrics.md`) | Threshold that pages someone | Clock | Owner | Tool — startup | Tool — large company |
|---|---|---|---|---|---|---|
| **Infrastructure** | `p95` end-to-end pre-read & draft latency; API error rate; ledger/KB no-hit rate; cost per draft (`€0.06` base) | `p95 > 4.0 s` OR API error rate `> 1.0 %` for `10 min` OR ledger lookup timeout `> 2 %` | Real time (1-min window) | On-call Backend / AI Engineer | Render metrics + Sentry + Grafana Cloud (free tier) | AWS CloudWatch / GCP Cloud Monitoring + Datadog |
| **Model quality** | Weekly 5 % human QA sample vs LLM judge agreement (`86.7 %` baseline on the golden 30, `evals/README.md`); human-graded `sendable` rate (`52.9 %` baseline on the golden 30, `evals/reports/report_v1.md`) | Human–judge agreement `< 80 %` OR `sendable` rate `< 45 %` for **2 consecutive weeks** | Weekly (Friday QA review) | Product Manager (PM) | Langfuse (Cloud free tier) / Arize Phoenix | LangSmith / Langfuse self-hosted / Datadog LLM Observability |
| **Product & guardrails** | Drafts generated on human-only tickets (`0`); cross-merchant leaks (`0`); wrong-match rate (`≤ 0.5 %`); 7-day reopen rate by segment (`FR` vs `EN`, flagged accounts) | **Any (`≥ 1`)** draft sent on human-only ticket or cross-merchant leak (immediate); OR segment 7-day reopen rate **`> 1.5×`** baseline for 2 weeks | Real time (policy alerts) & Daily (segment rollups) | Head of Support (+ DPO on privacy/leak alerts) | Postgres / SQLite event table + Metabase | BigQuery / Snowflake + Looker / Power BI |
| **Business** | All-in cost per resolved status ticket (`€10.00 → €8.00 / €7.60`); median handling time saved (`30 %` base / `38 %` target); wrong-answer error cost (`€25` / `€200`) | Handling time reduction `< 20 %` by Week 4 OR cost per resolved status ticket `> €8.50` at Month-2 close | Weekly (handling time) & Monthly (unit cost) | Head of Support + CFO / Head of Finance | Weekly SQL query + shared Google Sheet | Enterprise BI / Finance warehouse dashboard |
| **Paging** | Threshold breach routing across all four layers | Any red threshold above | Real time / Daily / Weekly | On-call Engineer (infra/outage) & Head of Support (guardrails) | Slack `#ledgerly-copilot-alerts` webhook | PagerDuty / Opsgenie on-call rota |

**Where our FastAPI runs:**
- **Demo (27 November oral):** the prototype runs on a laptop from the command line (`python prototype/run_eval.py`, `python prototype/test_switch.py`), on the invented eval-set: the laptop is our staging. No web service is deployed for the project (optional in the brief).
- **Pilot / Production (`€0` startup path from Slide 19):** **FastAPI service on Render** (or Hugging Face Spaces Docker container) behind `/draft` and `/health`, **Streamlit Community Cloud** for the agent UI tab, **Langfuse Cloud (free tier)** for OpenTelemetry traces, and **Supabase / Neon Postgres** for isolated merchant ledger & ticket logs. All LLM API keys and DB credentials live in environment variables (`.env` / platform secrets manager), never in Git.

**Release path and gates:**
1. **`dev` (laptop · every commit):** Deterministic unit tests on the 4 pipeline steps (router, isolated `merchant_id` ledger lookup, open-flag checker, policy guardrail filter) + `promptfoo` Level-1 assertions (`evals/promptfooconfig.yaml`) using mock responses (`€0` API cost).
   - **Gate 1 → `staging`:** `100 %` unit tests and Level-1 assertions green; `0` hardcoded secrets or cross-merchant query paths.
2. **`staging` (production-mirror schema · zero live merchants):** Full 100-case regression run (`evals/eval_set_v1.csv`) graded by `evals/judge_prompt.txt` + 2-week shadow mode on live incoming tickets (drafts logged to Langfuse, never shown to agents) + live rollback switch drill.
   - **Gate 2 → `production`:** Coverage `≥ 70 %` and human-graded sendable rate `≥ 50 %` on draftable tickets (`evals/reports/report_v1.md`: `87.5 %`, and `52.9 %` on the golden 30), lookup precision `≥ 98 %`, `0 / 100` policy/isolation misses, `p95 ≤ 4.0 s`, and rollback drill signed off with a real test date.
3. **`production` (phased rollout by steps):** `Internal QA agents (1 week)` → `5 % traffic canary (3 days)` → `50 % A/B experiment (4 weeks, §1–§2)` → `100 % rollout with persistent 5 % holdout`.
   - **Gate 3 → next step:** Every threshold in the four-layer monitoring table above stays green, and the Week-4 decision rule (`§2`) passes.

**First drift expected:**
- **Type:** **Knowledge & Concept drift** (followed closely by **Data drift** when Ledgerly launches new payment rails or promotional cashback campaigns).
- **Why it hits first:** Ledgerly's Terms of Service, fee schedules (e.g., Starter `1.5 %` vs Standard `1.9 %` in `L-11`), payout cut-off calendars (`Terms §2.1–§2.3`), and cashback/promo rules (`CB-11` in `L-06`) update more frequently than the underlying LLM weights—causing drafts that were `sendable` last month to cite outdated fee tiers or payout delays.
- **Signal that shows it:** A spike in **human edit rate** on `Account & fee` or `Cashback/offer` drafts (`> 45 %` edited), rising **retrieval age / version mismatch** flags on KB policy chunks, and a drop in weekly human–judge agreement below **`80 %`**.
- **What we re-run:** We update the affected policy chunk and golden labels, then re-run the **frozen 100-case eval-set (`evals/eval_set_v1.csv`)** + `evals/judge_prompt.txt` before every KB update, prompt edit, or model version bump (`€5,000 / change` budgeted in `02_sizing.xlsx`).

## §4 Contain the incident — trace, classes, rollback

**Trace — one OpenTelemetry trace per draft, one span per step** (emitted via OpenTelemetry / Langfuse `@observe()` SDK; stored in Langfuse + Postgres audit log):
1. **`POST /draft` (root span):** `trace_id`, `ticket_id`, `merchant_id` (tenant isolation key), `segment` (`category`, `language`, `has_open_flag`), `prompt_version`, `model_version`, `kb_version`, `total_latency_ms`, `token_cost_eur`, `switch_mode` (`ON` / `SUGGEST_ONLY` / `OFF`).
2. **`classify` (router span):** `predicted_intent` (`status` / `refund_dispute` / `account` / `out_of_scope`), `confidence_score`, `language_detected`, `in_scope_bool`.
3. **`retrieve` (isolated ledger & flag lookup span):** `merchant_id_filter_applied` (`true`), `matched_ids` (`TX-`, `VO-`, `RF-`), `candidate_count` (`0`, `1`, or `>1` tie), `open_account_flags` (`bank_change`, `contract`, `terms`, `fees`, or `none`), `kb_sources_cited`, `no_hit_bool`, `db_latency_ms`.
4. **`generate` (LLM drafter span — skipped if `NO_DRAFT`):** `model_name`, `tokens_in`, `tokens_out`, `llm_latency_ms`, `draft_generated_bool`.
5. **`guardrail` (policy & privacy check span):** `human_only_topic_blocked`, `money_promise_detected`, `unmasked_iban_or_decline_code_detected`, `cross_merchant_id_check` (`pass` / `block`), `final_action` (`show_draft` / `no_draft_escalate`).
6. **`human_decision` (agent & QA outcome span):** `agent_action` (`approved_as_is` / `edited` / `discarded` / `escalated`), `edit_distance_chars`, `reopened_within_7d_bool`, `llm_judge_score` (`sendable` / `needs_edit` / `escalate`), `weekly_human_qa_grade` (if sampled in 5 % audit).

**Our one-page dashboard — five panels and the question each answers** (built as a single-page Streamlit Ops tab backed by Langfuse & Postgres SQL views):
1. **Stat tiles + threshold badges (top row):** *"Am I paged right now?"* — Shows today's `drafts on human-only tickets` (`0`, threshold `0`), `cross-merchant leaks` (`0`, threshold `0`), `p95 latency` (`threshold 4.0 s`), `weekly sendable rate` (`threshold 45 %`), and `human–judge agreement` (`threshold 80 %`) in green/red.
2. **Time-series line chart with paging line (7-day & 30-day):** *"Are latency, cost per draft (`€0.06`), or API errors trending up or spiking?"* — Plots daily `p95` latency and error rate against the `4.0 s` and `1.0 %` paging lines.
3. **Distribution histogram (this week vs last week):** *"Is data or model drift shifting our confidence or edit distance?"* — Compares `classify.confidence_score` and `candidate_count` distributions week-over-week to catch new ticket phrasing before reopen rates rise.
4. **Grouped bar chart by pre-registered segment (4-week rolling):** *"Is any segment paying for the average (Simpson's paradox)?"* — Splits `7-day reopen rate` and `sendable-as-is rate` across `French vs English`, `Flagged vs Clean accounts`, and `High-volume vs Standard merchants` against the `1.5×` harm threshold line.
5. **Worst-cases triage table (bottom panel):** *"Which exact tickets should the PM and Support QA fix on Monday?"* — Lists every ticket from the past 7 days that triggered a `guardrail` block, a `7-day reopen`, or a `human ≠ LLM judge` disagreement, with clickable `trace_id`, `merchant_id`, `matched_ids`, and failure reason.

**Four incident classes, examples on Ledgerly agent-assist, and actions:**

| Class | Example on our agent | How we detect it (trace query) | Action |
|---|---|---|---|
| **Caught** | Policy filter blocks a draft that quoted payer bank decline code `51` (`L-03`) or promised a €100 partial refund (`L-35`); or agent edits an overly reassuring word (`"safely"` in `L-24`) before sending. | `guardrail.final_action = block` OR `human_decision.agent_action = edited` with `reopened_within_7d = false`. | Log and count in weekly review; if the same pattern repeats `≥ 3` times in a week, add a rule/example to `evals/judge_rubric.md` and prompt v2. |
| **Sent wrong** | Agent approves a draft citing the right `TX-` ID, but states a Saturday payout date (`7 Nov` in `L-02` / `L-26`) instead of Monday `9 Nov`, or omits that a `€0.01` cashback hold requires manual ops release (`L-06`), causing the merchant to reopen within 7 days. | `human_decision.agent_action ∈ {approved_as_is, edited}` AND `reopened_within_7d = true` (below the `1.5×` segment harm threshold, no money/privacy breach). | Agent sends a corrected follow-up citing the exact `VO-` / payout schedule; PM adds the case to `evals/eval_set_v1.csv` and updates the prompt/KB rule before the next release. |
| **Harmful** *(above `governance.md` harm threshold)* | A draft goes out on a human-only dispute/refund ticket promising a refund (`L-13`, `L-34`), fails to flag an open `bank_change` when payout already went to an old IBAN (`L-05`), exposes another `merchant_id`'s transaction (`L-20`, `L-44`), or pushes a segment's 7-day reopen rate above **`1.5×`** baseline for 2 weeks. | `guardrail` miss on human-only / PII / cross-merchant check, DPO/merchant escalation, OR segment `reopened_within_7d > 1.5×` control for 2 weeks. | **Immediate rollback (`< 15 min`)** to `SUGGEST_ONLY` or `OFF` on the affected segment; write incident post-mortem within 24 h; notify **DPO** immediately if any cross-merchant or payer PII data was exposed. |
| **Outage** | LLM provider API returns `5xx` timeouts (`error rate > 1 %` for `10 min`) or the isolated ledger lookup service returns `100 %` no-hits / timeouts. | `POST /draft` error rate `> 1.0 %` for `10 min` OR `retrieve` timeout/no-hit `= 100 %`. | **Automatic circuit-breaker fallback** switches `COPILOT_MODE = OFF` (humans-only mode); Tier-1 agents work directly in the ledger/ticketing UI as today until on-call Engineer restores service. |

**Rollback plan (the switch ⏻ from `04_architecture.md`)**

| Field | Ours |
|---|---|
| **1 · Trigger** | Any single (`≥ 1`) `Harmful` incident (draft sent promising money movement, cross-merchant leak, missed `bank_change` alert on sent funds), OR segment 7-day reopen rate `> 1.5×` baseline for 2 consecutive weeks, OR weekly human–judge agreement `< 80 %` / `sendable < 45 %` for 2 weeks, OR API error rate `> 1 %` for `10 min`. |
| **2 · Who decides (day / night)** | **Head of Support** during business hours (Mon–Fri `08:00–19:00` CET); **On-call Backend / AI Engineer** at night/weekends (acts immediately within `15 min`, then notifies Head of Support and PM). |
| **3 · The action (3 switch positions)** | Flip environment flag `COPILOT_MODE` in Render / feature-flag config: **(1) `SUGGEST_ONLY` (L1):** pre-read & draft remain visible for internal QA, "Insert / Send draft" button disabled (first move for quality/segment drift); **(2) `OFF` (L0):** full humans-only fallback (mandatory for `Harmful` privacy/isolation incidents or API outages); **(3)** redeploy previous Docker image / prompt tag if caused by a new release. |
| **4 · Time to execute** | **Under `15 minutes` (`~2 minutes` via feature flag toggle)** by one person, executable from a laptop or phone without needing the original code author. |
| **5 · What people see** | **Tier-1 agents:** Banner in sidebar *"Copilot drafts paused — handle ticket directly in ledger as usual"* (no broken UI or error stack); **Merchants:** No change (reply continues via normal Tier-1 agent workflow); **System:** OpenTelemetry traces continue logging `switch_mode` for audit. |
| **6 · Last tested (date · where · who)** | **Tested on `2026-11-27`** on the prototype on a laptop (our staging), with `python prototype/test_switch.py`, by **Team Ledgerly (AI Engineer & Product Manager roles)** — verified `ON` (draft, Send enabled) → `SUGGEST_ONLY` (draft visible, Send disabled) → `OFF` (no pre-read), and that an unknown value falls back to `OFF`: PASS on 4 checks, under 1 s once the variable is set; **next scheduled drill: `2027-02-27`** (quarterly). |

## §5 Own the system — the five owners

| Decision | Owner (named role) | Written where |
|---|---|---|
| **Run an experiment on real users** | **Head of Support** (signs protocol & business risk) + **Data Protection Officer (DPO)** (reviews tenant-isolation & GDPR compliance before launch) | `06_07_experiments_operations.md §1–§2` · `governance.md` |
| **Read the weekly numbers and act** | **Product Manager (PM)** (reviews four-layer dashboard & 5 % human QA sample every Monday; proposes prompt/KB iterations) | `06_07_experiments_operations.md §3` |
| **Press the switch (day / night)** | **Head of Support** (daytime `08:00–19:00` CET) · **On-call Backend / AI Engineer** (nights & weekends, `< 15 min` SLA) | `06_07_experiments_operations.md §4` · `governance.md` |
| **Approve a release (prompt, model, sources)** | **Product Manager (PM)** (approves only with green `evals/eval_set_v1.csv` 100-case regression report + `0` policy/isolation misses attached) | `evals/README.md` · `06_07_experiments_operations.md §3` |
| **Keep the trace; answer a customer or a regulator** | **Lead Backend / Platform Engineer** (maintains isolated OpenTelemetry/Langfuse trace retention) · **Legal Counsel & DPO** (answers merchant disputes, regulators, and EU AI Act Art. 26/50 inquiries — Ledgerly remains legally accountable for every sent reply, per *Moffatt v. Air Canada*, 2024 BCCRT 149) | `governance.md` · `06_07_experiments_operations.md §4–§5` |

*Copied into `governance.md` (Sessions 6 + 7 lines):*
- **Experiments on real users.** Any experiment on real Ledgerly merchants and Tier-1 agents is signed by the **Head of Support** and reviewed by the **Data Protection Officer (DPO)** before launch; the decision rule and harm threshold are written before the first ticket (`06_07_experiments_operations.md §1–§2`).
- **The switch.** The **Head of Support** (daytime) or **On-call Backend / AI Engineer** (night/weekends) can move `COPILOT_MODE` to `SUGGEST_ONLY` or `OFF` in under `15 minutes`. Last tested **`2026-11-27`** on the prototype (`python prototype/test_switch.py`); next scheduled test **`2027-02-27`** (`06_07_experiments_operations.md §4`).
- **The trace.** One OpenTelemetry trace per ticket (`request → classify → retrieve → generate → guardrail → human_decision`) is kept for **`12 months`** in **Langfuse + isolated Postgres audit storage** (`merchant_id`-scoped); **Legal Counsel & the DPO** answer any merchant complaint, audit, or regulator inquiry from it, and **Ledgerly remains fully responsible for all copilot-assisted communications** (*Moffatt v. Air Canada*, 2024 BCCRT 149; EU AI Act Art. 26 & 50).
