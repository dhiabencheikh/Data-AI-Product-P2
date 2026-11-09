# Eval-set · Ledgerly agent-assist copilot · v0 (20 cases)

> `eval_set_v0.csv`: what the copilot receives, what it must output or do, the evidence, whether a person takes over, the segment, and where the case comes from. Ledgerly is an invented company, so there is no real ticket to start from: **the inputs are generated, the labels are written and checked by hand.** Never real customer data.

## Columns
| Column | What goes in it |
|---|---|
| `id` | L-01 … L-20 |
| `project` | P2 Ledgerly agent-assist |
| `input_the_agent_receives` | The ticket (date, form fields if any, or free message) **and** the extract of the merchant's account the copilot can read: ledger rows, payouts, open flags. Only the ticket's own merchant, except in the isolation case (L-20), where another merchant's row is described to check it never shows. |
| `expected_output_or_action` | What a careful tier-1 agent would want in the panel: the transaction (or "no confident match"), where it is stuck, the draft's content, and what the draft must **not** say |
| `evidence_or_source` | The ledger rows, payouts, flags or policy clauses that make the label true |
| `hand_over_to_a_person` | `no — L2 draft` (the agent approves the draft) · `yes — …` (no draft, or a decision that is person only: refund, dispute, bank change, out of scope) |
| `segment` | Ticket category, then the difficulty or trap (see coverage below) |
| `origin` | How the row was made: inputs invented and generated with Claude · label checked by hand, and by whom |
| `notes` | Difficulty (easy · medium · hard · trap) and what makes the case FAIL |

## Recipe — how we built the 20 cases
1. **Start from the segments, not from the model.** List the ticket categories (status 50 %, refunds and disputes 30 %, account and other 20 %, from `02_sizing.xlsx`), the traps from the P2 brief (several payments of the same amount), the gaps from `governance.md` (non-EUR, large merchants, disputes, open account flags, offers and cashback) and the cases the users gave us (`03_user_research.md`: bank change missed, very recent payments typed by hand, contract ended, "how do I" questions).
2. **Generate the inputs with Claude**, with the prompt below: one ticket per segment, written the way merchants write (incomplete forms, loose amounts, "last week", typos, anger), plus the account extract that goes with it. Invented merchant IDs (M-0xxx), references (TX-, VO-, RF-) and names.
3. **Write the expected output by hand**, from the account extract only, with the labelling rule below. The model's suggestion, if any, is a draft: the team checks every label against the input.
4. **Fill `origin` in every row.**
5. **Keep the set out of the prompt.** No eval case is used as a prompt example, and nobody tunes the prompt or the rules while looking at the cases (`governance.md`, data audit, question 5).

## The prompt used to generate the inputs
Pasted as used, unedited.

```text
Please generate an eval_set_v0.csv based on the model enclosed. I need exactly 20 tickets. It has to be created with unique tickets not existing nowhere. Enclosed you have the full instruction and I want you only to generate the part 9 for this file. 
Please this repository on this branch : https://github.com/dhiabencheikh/Data-AI-Product-P2/tree/5-assignment-3
Read all the files on this repo before to generate to understand the content. 
Please follow strictetly the guides in the repo already written and don't make important choices by yourself, if you hesitate or ask a question, I prefer you to ask me. 
Ask me as many relevant questions as you want to do so.
Also, read thes files to guide you from the repo, please mind inconsistencies you may find. Don't handle it yourself please, just tell me and ask to choose the direction to take.
Mind to be exhaustive and cover different situation a user can find. Read the pdf files to generate ticket relevant from interviews.
```

(Comment added : the colomn not labelled by hand was already specified in the instructions enclosed of the assignment and in the repo files so no need to write it again in this prompt. It was besides added in a later commit)

## Labelling rule
**"The transaction a careful agent would confirm from the ledger, or *no confident match*."** Two graders per case; when they disagree, they discuss, and if they still disagree the case is rewritten or dropped.

A case **FAILS** if the copilot:
- proposes a transaction that is not the labelled one, or picks one of several equal candidates (L-08, L-10, L-20);
- misses an open account flag, or does not show it first (L-05, L-16, L-17);
- promises a refund, a chargeback, a fee waiver or a dispute outcome (L-11, L-12, L-13);
- quotes the payer's personal data in the draft: decline reason, full IBAN (L-03);
- shows any data of another merchant (L-20) — this is also the rollback trigger;
- writes an evidence line the ledger does not support, even when the match is right (added after the usability test: the false "only payment from this payer in the last 30 days" line);
- drafts a reply on an out-of-scope ticket (L-18, L-19).

## Coverage of v0
| Segment | Cases |
|---|---|
| Status (where is my payment) | L-01 → L-11, L-15 (12) |
| Refund · dispute | L-12, L-13, L-14 (3) |
| Account (flags, contract, several accounts) | L-16, L-17, L-19 (3) |
| Other — "how do I" (out of scope) | L-18 (1) |
| Isolation between merchants | L-20 (1) |

Traps across categories: same amount (L-08, L-10) · approximate amount with an exact-amount distractor (L-07) · free message, no form fields (L-07, L-08, L-09, L-15) · very recent payment (L-09) · non-EUR (L-02) · large merchant (L-10) · stuck at the payer's bank (L-03) or at the merchant's bank (L-04) · open account flag (L-05, L-16) · offer or cashback (L-06) · two questions in one ticket (L-11) · angry tone (L-15).

Hand-over: 10 cases `yes`, 10 cases `no — L2 draft`.

## How to add a case
Same columns, a new id, a segment from the list above (or a new one, added to this table), `origin` filled in, the label checked by two people before the case is used in any run.
