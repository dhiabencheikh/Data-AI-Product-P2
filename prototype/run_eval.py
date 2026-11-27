"""Run the eval-set through the copilot and print the numbers of evals/reports/report_v1.md.

Usage (from the repository root):
    python prototype/run_eval.py                         # evals/eval_set_v1.csv (100 cases)
    python prototype/run_eval.py evals/eval_set_v0.csv   # the 50 cases of Session 4

It also writes evals/copilot_outputs/drafts_<eval-set>.csv: one row per case with the copilot's output,
ready for the two human graders (columns grader_1 / grader_2 left empty).
"""
import csv
import os
import re
import sys
from collections import Counter

from config import MODE_ON
from pipeline import process_ticket
from router import TicketRouter

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DEFAULT_EVAL_PATH = os.path.join(ROOT, "evals", "eval_set_v1.csv")
EVAL_LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "eval_audit_log.jsonl")


def expected_reference(expected_output: str):
    """The transaction or refund the label says the copilot must match ('Match TX-1' / 'Match refund RF-1')."""
    found = re.search(r"Match (?:refund )?((?:TX|RF)-\d+)", expected_output)
    return found.group(1) if found else None


def segment_family(segment: str) -> str:
    """First word of the segment label: status, refund, dispute, account, isolation, other..."""
    return segment.split("·")[0].strip().split(" ")[0] or "other"


def score_case(row: dict, output: dict) -> dict:
    """Compare one output with its label."""
    expects_draft = row["hand_over_to_a_person"].strip().lower().startswith("no")
    produced_draft = output["outcome"] == "draft"
    reference = expected_reference(row["expected_output_or_action"])
    right_match = None
    if produced_draft and reference:
        right_match = output["citations"][0] == reference
    return {
        "id": row["id"],
        "family": segment_family(row["segment"]),
        "expects_draft": expects_draft,
        "produced_draft": produced_draft,
        "decision_right": expects_draft == produced_draft,
        "right_match": right_match,
        "blocked": output["outcome"] == "blocked",
    }


def print_summary(scores: list, eval_path: str) -> None:
    """Print the numbers against the success criterion of 03_product_brief.md / spec.md."""
    total = len(scores)
    eligible = [score for score in scores if score["expects_draft"]]
    human_only = [score for score in scores if not score["expects_draft"]]
    drafts = [score for score in scores if score["produced_draft"]]
    drafts_on_eligible = [score for score in eligible if score["produced_draft"]]
    drafts_on_human_only = [score for score in human_only if score["produced_draft"]]
    checked = [score for score in drafts if score["right_match"] is not None]
    right = [score for score in checked if score["right_match"]]
    decisions_right = [score for score in scores if score["decision_right"]]
    blocked = [score for score in scores if score["blocked"]]

    print(f"=== LEDGERLY EVAL · {os.path.basename(eval_path)} · {total} cases ===")
    print(f"Drafts produced (grounded + policy pass): {len(drafts)} / {total}")
    print(f"Coverage — drafts on tickets labelled 'L2 draft': {len(drafts_on_eligible)} / {len(eligible)} "
          f"= {len(drafts_on_eligible) / len(eligible):.1%} (target >= 70 %)")
    if checked:
        print(f"Match precision — draft cites the labelled transaction: {len(right)} / {len(checked)} "
              f"= {len(right) / len(checked):.1%} (target >= 98 %)")
    print(f"Drafts on human-only tickets (must be 0): {len(drafts_on_human_only)} / {len(human_only)}")
    print(f"Policy blocks: {len(blocked)}")
    print(f"Draft / hand-over decision right: {len(decisions_right)} / {total} = {len(decisions_right) / total:.1%}")

    print("\n--- by segment family (drafts on eligible / eligible · drafts on human-only) ---")
    families = Counter(score["family"] for score in scores)
    for family in sorted(families):
        in_family = [score for score in scores if score["family"] == family]
        family_eligible = [score for score in in_family if score["expects_draft"]]
        family_drafted = [score for score in family_eligible if score["produced_draft"]]
        family_wrong = [score for score in in_family if not score["expects_draft"] and score["produced_draft"]]
        print(f"{family:<10} {len(family_drafted)} / {len(family_eligible)} · {len(family_wrong)}")

    print("\n--- misses (decision or match) ---")
    for score in scores:
        if not score["decision_right"] or score["right_match"] is False:
            kind = "wrong match" if score["right_match"] is False else (
                "draft on human-only" if score["produced_draft"] else "no draft on an eligible ticket")
            print(f"- {score['id']}: {kind}")


def write_grading_sheet(rows: list, outputs: list, eval_path: str) -> str:
    """Write the copilot's outputs next to the labels, for the human graders."""
    name = os.path.splitext(os.path.basename(eval_path))[0].replace("eval_set_", "")
    output_dir = os.path.join(ROOT, "evals", "copilot_outputs")
    os.makedirs(output_dir, exist_ok=True)
    sheet_path = os.path.join(output_dir, f"drafts_{name}.csv")
    with open(sheet_path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["id", "segment", "hand_over_to_a_person", "expected_output_or_action", "copilot_outcome",
                         "copilot_citations", "copilot_reason", "copilot_draft", "grader_1", "grader_2"])
        for row, output in zip(rows, outputs):
            writer.writerow([row["id"], row["segment"], row["hand_over_to_a_person"], row["expected_output_or_action"],
                             output["outcome"], " ".join(output["citations"]), output["reason"], output["draft"] or "",
                             "", ""])
    return sheet_path


def main():
    eval_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_EVAL_PATH
    with open(eval_path, encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    # A fresh eval log for each run (the production audit log is kept apart).
    if os.path.exists(EVAL_LOG_PATH):
        os.remove(EVAL_LOG_PATH)

    router = TicketRouter()
    outputs = []
    scores = []
    for row in rows:
        output = process_ticket(row["id"], row["input_the_agent_receives"], router, mode=MODE_ON, log_path=EVAL_LOG_PATH)
        outputs.append(output)
        scores.append(score_case(row, output))

    print_summary(scores, eval_path)
    sheet_path = write_grading_sheet(rows, outputs, eval_path)
    print(f"\nGrading sheet written to {os.path.relpath(sheet_path, ROOT)}; audit log of the run: "
          f"{os.path.relpath(EVAL_LOG_PATH, ROOT)}")


if __name__ == "__main__":
    main()
