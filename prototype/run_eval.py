import csv
import os
from router import TicketRouter
from routing_rule import apply_routing_rule
from drafter import retrieve_and_draft
from policy import check_policy

EVAL_PATH = os.path.join(os.path.dirname(__file__), "..", "evals", "eval_set_v0.csv")

def main():
    router = TicketRouter()
    total = 0
    drafts_produced = 0
    policy_blocks = 0
    human_only_total = 0
    drafts_on_human_only = 0
    escalated_correctly = 0
    misses = []

    with open(EVAL_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            tid = row["id"]
            text = row["input_the_agent_receives"]
            expected_handover = row["hand_over_to_a_person"].strip().lower().startswith("yes")

            if expected_handover:
                human_only_total += 1

            # Step 1: Route (Rung 2)
            route = router.predict(text)
            # Step 2: Routing Rule (Rung 1)
            gate = apply_routing_rule(route, text)

            if gate["action"] == "escalate":
                if expected_handover:
                    escalated_correctly += 1
                else:
                    misses.append((tid, "routing_rule", f"Over-escalated: {gate['reason']}"))
                continue

            # Step 3: Retrieve + Draft (Rung 3)
            draft_res = retrieve_and_draft(text, route["category"])
            if draft_res["status"] == "NO_DRAFT":
                if expected_handover:
                    escalated_correctly += 1
                else:
                    misses.append((tid, "drafter", f"Missed draft: {draft_res['reason']}"))
                continue

            # Step 4: Policy Check (Rung 1)
            pol = check_policy(draft_res)
            if pol["policy"] == "block":
                policy_blocks += 1
                misses.append((tid, "policy", f"Blocked: {pol['reason']}"))
                continue

            drafts_produced += 1
            if expected_handover:
                drafts_on_human_only += 1
                misses.append((tid, "routing_rule", "Drafted on a human-only ticket!"))

    print("=== LEDGERLY EVAL v0 SUMMARY ===")
    print(f"Total cases evaluated: {total}")
    print(f"Grounded + policy-passed drafts produced: {drafts_produced} / {total} ({drafts_produced/total:.1%})")
    print(f"Human-only tickets properly abstained/escalated: {escalated_correctly} / {human_only_total}")
    print(f"Drafts on human-only tickets (must be 0): {drafts_on_human_only}")
    print(f"Policy blocks triggered: {policy_blocks}")
    print("\n=== SAMPLE MISSES (FOR report_v0.md & spec.md v2) ===")
    for m in misses[:10]:
        print(f"- {m[0]} [{m[1]}]: {m[2]}")

if __name__ == "__main__":
    main()
