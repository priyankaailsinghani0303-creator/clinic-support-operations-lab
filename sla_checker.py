from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def load_csv(filename: str):
    with (BASE_DIR / filename).open(newline="") as file:
        return list(csv.DictReader(file))


def parse_timestamp(value: str) -> datetime:
    if not value:
        raise ValueError("Timestamp is missing")

    formats = (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S.%f",
    )

    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue

    try:
        return datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"Unsupported timestamp format: {value!r}") from exc


def get_policy_for_ticket(ticket: dict, policy_map: dict[str, dict]) -> dict | None:
    return policy_map.get(ticket.get("priority"))


def response_minutes(record: dict) -> float:
    created = parse_timestamp(record["created_at"])
    responded = parse_timestamp(record["first_responded_at"])
    return (responded - created).total_seconds() / 60


def build_queue(tickets, timestamps, policy_map):
    queue = []
    timestamp_map = {record["ticket_id"]: record for record in timestamps if record.get("ticket_id")}

    for ticket in tickets:
        ticket_id = ticket.get("ticket_id")
        record = timestamp_map.get(ticket_id)

        if record is None:
            alert = "RESPONSE NOT RECORDED"
        else:
            policy = get_policy_for_ticket(ticket, policy_map)
            if policy is None:
                alert = "SLA POLICY MISSING"
            else:
                try:
                    minutes = response_minutes(record)
                    target = int(policy["first_response_minutes"])
                    alert = "SLA MET" if 0 <= minutes <= target else "SLA BREACHED"
                except ValueError:
                    alert = "INVALID TIMESTAMP"

        queue.append((ticket, alert))

    return queue


sla_policy = load_csv("sla_policy.csv")
tickets = load_csv("tickets.csv")
timestamps = load_csv("ticket_timestamps.csv")

policy_map = {policy["priority"]: policy for policy in sla_policy if policy.get("priority")}
ticket_map = {ticket["ticket_id"]: ticket for ticket in tickets if ticket.get("ticket_id")}
timestamp_map = {record["ticket_id"]: record for record in timestamps if record.get("ticket_id")}
priority_order = {"Urgent": 1, "High": 2, "Medium": 3, "Low": 4}
alert_order = {
    "SLA BREACHED": 1,
    "RESPONSE NOT RECORDED": 2,
    "SLA MET": 3,
    "SLA POLICY MISSING": 4,
    "INVALID TIMESTAMP": 5,
}

print("Ticket ID | Priority | First Response (min) | Resolution (min)")
for ticket in tickets:
    policy = get_policy_for_ticket(ticket, policy_map)
    if policy is None:
        continue
    print(" | ".join([
        ticket["ticket_id"],
        ticket["priority"],
        policy["first_response_minutes"],
        policy["resolution_minutes"],
    ]))

print("\nActual first response by ticket")
for record in timestamps:
    ticket_id = record.get("ticket_id")
    if not ticket_id:
        continue
    try:
        minutes = response_minutes(record)
    except ValueError:
        print(f"{ticket_id} | INVALID TIMESTAMP")
        continue
    print(f"{ticket_id} | Actual first response: {minutes:.0f} minutes")

print("\nFIRST-RESPONSE SLA COMPLIANCE")
met = 0
breached = 0
for record in timestamps:
    ticket_id = record.get("ticket_id")
    ticket = ticket_map.get(ticket_id)
    if ticket is None:
        continue

    policy = get_policy_for_ticket(ticket, policy_map)
    if policy is None:
        continue

    try:
        actual_minutes = response_minutes(record)
        target_minutes = int(policy["first_response_minutes"])
    except ValueError:
        print(f"{ticket_id} | INVALID TIMESTAMP | SKIPPED")
        continue

    status = "MET" if 0 <= actual_minutes <= target_minutes else "BREACHED"
    if status == "MET":
        met += 1
    else:
        breached += 1

    print(f"{ticket_id} | {actual_minutes:.0f}/{target_minutes} min | {status}")

print("\nNEEDS ATTENTION")
for record in timestamps:
    ticket_id = record.get("ticket_id")
    ticket = ticket_map.get(ticket_id)
    if ticket is None:
        continue

    policy = get_policy_for_ticket(ticket, policy_map)
    if policy is None:
        continue

    try:
        actual = response_minutes(record)
        target = int(policy["first_response_minutes"])
    except ValueError:
        continue

    if actual > target:
        print(f"{ticket['ticket_id']} | {ticket['clinic']} | {ticket['issue_type']} | SLA BREACHED")

print("\nSLA PERFORMANCE SUMMARY")
print(f"Tickets evaluated: {met + breached}")
print(f"SLA met: {met}")
print(f"SLA breached: {breached}")
if met + breached:
    print(f"SLA compliance rate: {met / (met + breached) * 100:.1f}%")
else:
    print("No tickets evaluated")

print("\nTICKETS WITHOUT FIRST-RESPONSE RECORDS")
recorded_ids = set(timestamp_map)
for ticket in tickets:
    ticket_id = ticket.get("ticket_id")
    if ticket_id not in recorded_ids:
        print(f"{ticket_id} | {ticket['clinic']} | {ticket['issue_type']} | {ticket['priority']} | RESPONSE NOT RECORDED")

print("\nTICKET PRIORITY SUMMARY")
for priority in ["Urgent", "High", "Medium", "Low"]:
    count = sum(1 for ticket in tickets if ticket.get("priority") == priority)
    print(f"{priority}: {count}")

print("\nSUPPORT TICKET TRIAGE QUEUE")
sorted_tickets = sorted(tickets, key=lambda ticket: priority_order.get(ticket.get("priority"), 5))
for ticket in sorted_tickets:
    print(f"{ticket['ticket_id']} | {ticket['priority']} | {ticket['issue_type']} | {ticket['clinic']}")

print("\nTICKET QUEUE WITH SLA ALERTS")
for ticket in sorted_tickets:
    record = timestamp_map.get(ticket.get("ticket_id"))
    if record is None:
        alert = "RESPONSE NOT RECORDED"
    else:
        policy = get_policy_for_ticket(ticket, policy_map)
        if policy is None:
            alert = "SLA POLICY MISSING"
        else:
            try:
                minutes = response_minutes(record)
                target = int(policy["first_response_minutes"])
                alert = "SLA MET" if 0 <= minutes <= target else "SLA BREACHED"
            except ValueError:
                alert = "INVALID TIMESTAMP"

    print(f"{ticket['ticket_id']} | {ticket['priority']} | {ticket['issue_type']} | {alert}")

print("\nACTION-PRIORITY TICKET QUEUE")
queue = build_queue(tickets, timestamps, policy_map)
queue.sort(key=lambda item: (alert_order.get(item[1], 99), priority_order.get(item[0].get("priority"), 5)))
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
    elif alert == "INVALID TIMESTAMP":
        action = "Fix timestamp formatting before SLA review"
    else:
        action = "Continue normal ticket follow-up"

    print(f"{ticket['ticket_id']} | {action}")
