
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

ROUTING_RULES = {
    "Booking": "Platform Support",
    "Payments": "Billing Support",
    "Messaging": "Technical Support",
    "Account": "Account Support",
}

def route_ticket(ticket):
    issue_type = ticket["issue_type"].strip().title()

    assigned_team = ROUTING_RULES.get(
        issue_type,
        "General Support"
    )

    return {
        "ticket_id": ticket["ticket_id"],
        "issue_type": issue_type,
        "priority": ticket["priority"],
        "assigned_team": assigned_team,
    }

with open(BASE_DIR / "tickets.csv", newline="") as file:
    tickets = list(csv.DictReader(file))

print("AUTOMATED SUPPORT TICKET ROUTING")
print("-" * 55)

for ticket in tickets:
    result = route_ticket(ticket)

    print(
        f"{result['ticket_id']} | "
        f"{result['issue_type']} | "
        f"{result['priority']} | "
        f"{result['assigned_team']}"
    )
