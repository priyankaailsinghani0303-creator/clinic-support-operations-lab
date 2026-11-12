import csv
from datetime import datetime

with open("sla_policy.csv", newline="") as file:
    sla_policy = list(csv.DictReader(file))

with open("tickets.csv", newline="") as file:
    tickets = list(csv.DictReader(file))

print("Ticket ID | Priority | First Response (min) | Resolution (min)")
for ticket in tickets:
    for policy in sla_policy:
        if ticket["priority"] == policy["priority"]:
            print(" | ".join([ticket["ticket_id"], ticket["priority"], policy["first_response_minutes"], policy["resolution_minutes"]]))

with open("ticket_timestamps.csv", newline="") as file:
    timestamps = list(csv.DictReader(file))

for record in timestamps:
    created = datetime.strptime(record["created_at"], "%Y-%m-%d %H:%M:%S")
    responded = datetime.strptime(record["first_responded_at"], "%Y-%m-%d %H:%M:%S")
    minutes = (responded - created).total_seconds() / 60
    print(f"{record['ticket_id']} | Actual first response: {minutes:.0f} minutes")

print("\nFIRST-RESPONSE SLA COMPLIANCE")

for record in timestamps:
    ticket = next((t for t in tickets if t["ticket_id"] == record["ticket_id"]), None)
    if ticket is None:
        continue

    policy = next((p for p in sla_policy if p["priority"] == ticket["priority"]), None)
    if policy is None:
        continue

    created = datetime.strptime(record["created_at"], "%Y-%m-%d %H:%M:%S")
    responded = datetime.strptime(record["first_responded_at"], "%Y-%m-%d %H:%M:%S")

    actual_minutes = (responded - created).total_seconds() / 60
    target_minutes = int(policy["first_response_minutes"])

    status = "MET" if 0 <= actual_minutes <= target_minutes else "BREACHED"

    print(f"{record['ticket_id']} | {actual_minutes:.0f}/{target_minutes} min | {status}")

print("\nNEEDS ATTENTION")

for record in timestamps:
    ticket = next((t for t in tickets if t["ticket_id"] == record["ticket_id"]), None)
    if ticket is None:
        continue

    policy = next((p for p in sla_policy if p["priority"] == ticket["priority"]), None)
    if policy is None:
        continue

    created = datetime.strptime(record["created_at"], "%Y-%m-%d %H:%M:%S")
    responded = datetime.strptime(record["first_responded_at"], "%Y-%m-%d %H:%M:%S")

    actual = (responded - created).total_seconds() / 60
    target = int(policy["first_response_minutes"])

    if actual > target:
        print(f"{ticket['ticket_id']} | {ticket['clinic']} | {ticket['issue_type']} | SLA BREACHED")

print("\nSLA PERFORMANCE SUMMARY")

met = 0
breached = 0

for record in timestamps:
    ticket = next((t for t in tickets if t["ticket_id"] == record["ticket_id"]), None)
    if ticket is None:
        continue

    policy = next((p for p in sla_policy if p["priority"] == ticket["priority"]), None)
    if policy is None:
        continue

    created = datetime.strptime(record["created_at"], "%Y-%m-%d %H:%M:%S")
    responded = datetime.strptime(record["first_responded_at"], "%Y-%m-%d %H:%M:%S")

    actual = (responded - created).total_seconds() / 60
    target = int(policy["first_response_minutes"])

    if 0 <= actual <= target:
        met += 1
    else:
        breached += 1

total = met + breached

print(f"Tickets evaluated: {total}")
print(f"SLA met: {met}")
print(f"SLA breached: {breached}")
print(f"SLA compliance rate: {met / total * 100:.1f}%" if total else "No tickets evaluated")

print("\nTICKETS WITHOUT FIRST-RESPONSE RECORDS")

recorded_ids = {record["ticket_id"] for record in timestamps}

for ticket in tickets:
    if ticket["ticket_id"] not in recorded_ids:
        print(f"{ticket['ticket_id']} | {ticket['clinic']} | {ticket['issue_type']} | {ticket['priority']} | RESPONSE NOT RECORDED")

print("\nTICKET PRIORITY SUMMARY")

for priority in ["Urgent", "High", "Medium", "Low"]:
    count = sum(1 for ticket in tickets if ticket["priority"] == priority)
    print(f"{priority}: {count}")

print("\nSUPPORT TICKET TRIAGE QUEUE")

priority_order = {
    "Urgent": 1,
    "High": 2,
    "Medium": 3,
    "Low": 4
}

sorted_tickets = sorted(
    tickets,
    key=lambda ticket: priority_order.get(ticket["priority"], 5)
)

for ticket in sorted_tickets:
    print(f"{ticket['ticket_id']} | {ticket['priority']} | {ticket['issue_type']} | {ticket['clinic']}")

print("\nTICKET QUEUE WITH SLA ALERTS")

for ticket in sorted_tickets:
    record = next(
        (r for r in timestamps if r["ticket_id"] == ticket["ticket_id"]),
        None
    )

    if record is None:
        alert = "RESPONSE NOT RECORDED"
    else:
        policy = next(
            (p for p in sla_policy if p["priority"] == ticket["priority"]),
            None
        )

        if policy is None:
            alert = "SLA POLICY MISSING"
        else:
            created = datetime.strptime(record["created_at"], "%Y-%m-%d %H:%M:%S")
            responded = datetime.strptime(record["first_responded_at"], "%Y-%m-%d %H:%M:%S")
            minutes = (responded - created).total_seconds() / 60
            target = int(policy["first_response_minutes"])

            alert = "SLA MET" if 0 <= minutes <= target else "SLA BREACHED"

    print(f"{ticket['ticket_id']} | {ticket['priority']} | {ticket['issue_type']} | {alert}")

print("\nACTION-PRIORITY TICKET QUEUE")

alert_order = {
    "SLA BREACHED": 1,
    "RESPONSE NOT RECORDED": 2,
    "SLA MET": 3,
    "SLA POLICY MISSING": 4
}

queue = []

for ticket in tickets:
    record = next(
        (r for r in timestamps if r["ticket_id"] == ticket["ticket_id"]),
        None
    )

    if record is None:
        alert = "RESPONSE NOT RECORDED"
    else:
        policy = next(
            (p for p in sla_policy if p["priority"] == ticket["priority"]),
            None
        )

        if policy is None:
            alert = "SLA POLICY MISSING"
        else:
            created = datetime.fromisoformat(record["created_at"])
            responded = datetime.fromisoformat(record["first_responded_at"])
            minutes = (responded - created).total_seconds() / 60
            target = int(policy["first_response_minutes"])
            alert = "SLA MET" if 0 <= minutes <= target else "SLA BREACHED"

    queue.append((ticket, alert))

queue.sort(
    key=lambda item: (
        alert_order.get(item[1], 5),
        priority_order.get(item[0]["priority"], 5)
    )
)

for ticket, alert in queue:
    print(f"{ticket['ticket_id']} | {ticket['priority']} | {alert}")

print("\nSUPPORT ESCALATION RECOMMENDATIONS")

for ticket, alert in queue:
    if alert == "SLA BREACHED":
        action = "Review breach, update clinic, notify support lead"
    elif alert == "RESPONSE NOT RECORDED":
        action = "Verify response history and contact clinic if needed"
    elif alert == "SLA POLICY MISSING":
        action = "Ask support lead to verify SLA configuration"
    else:
        action = "Continue normal ticket follow-up"

    print(f"{ticket['ticket_id']} | {action}")
