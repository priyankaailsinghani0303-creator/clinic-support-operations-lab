"""Canonical portfolio SLA evaluation and initial routing. No operational commitments."""
import pandas as pd

PRIORITY_ORDER = {"Urgent": 1, "High": 2, "Medium": 3, "Low": 4}
EVALUATED_STATUSES = {"Met", "Breached"}
RISK_WARNING_FRACTION = 0.8

def parse_time(value):
    """Parse one timestamp; naive timestamps are treated as UTC."""
    if pd.isna(value) or not str(value).strip():
        return pd.NaT

    return pd.to_datetime(
        str(value).strip(),
        errors="coerce",
        utc=True,
    )


def calculate_sla(ticket_data, timestamp_data, policy_data):
    result = ticket_data.copy()
    result["priority"] = result["priority"].fillna("").astype(str).str.strip().str.title()
    if result["ticket_id"].fillna("").astype(str).str.strip().eq("").any():
        raise ValueError("Every ticket must have a ticket_id")
    result["ticket_id"] = result["ticket_id"].astype(str).str.strip()
    if result["ticket_id"].duplicated().any():
        raise ValueError("Duplicate ticket IDs")

    result["first_response_minutes"] = float("nan")
    result["response_minutes"] = float("nan")
    result["created_at"] = pd.NA
    result["first_responded_at"] = pd.NA
    result["SLA Status"] = "Policy Missing/Invalid"

    # Build a policy lookup. Ambiguous duplicate priorities
    # are excluded rather than silently choosing one.
    policy_map = {}

    if {"priority", "first_response_minutes"}.issubset(
        policy_data.columns
    ):
        policy_copy = policy_data.copy()
        policy_copy["priority"] = (
            policy_copy["priority"]
            .fillna("")
            .astype(str)
            .str.strip()
            .str.title()
        )

        duplicates = policy_copy["priority"].duplicated(
            keep=False
        )

        for _, row in policy_copy.loc[~duplicates].iterrows():
            policy_map[row["priority"]] = row[
                "first_response_minutes"
            ]

    # Build a timestamp lookup.
    timestamp_map = {}
    duplicate_timestamp_ids = set()

    if {
        "ticket_id",
        "created_at",
        "first_responded_at",
    }.issubset(timestamp_data.columns):
        timestamp_copy = timestamp_data.copy()
        timestamp_copy["ticket_id"] = (
            timestamp_copy["ticket_id"]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        duplicates = timestamp_copy["ticket_id"].duplicated(
            keep=False
        )

        duplicate_timestamp_ids = set(
            timestamp_copy.loc[duplicates, "ticket_id"]
        )

        timestamp_map = {
            row["ticket_id"]: row
            for _, row in timestamp_copy.loc[
                ~duplicates
            ].iterrows()
        }

    for index, ticket in result.iterrows():
        ticket_id = ticket["ticket_id"]

        target = pd.to_numeric(
            policy_map.get(ticket["priority"]),
            errors="coerce",
        )

        if ticket["priority"] not in PRIORITY_ORDER or pd.isna(target) or target <= 0 or target == float("inf"):
            continue

        result.at[index, "first_response_minutes"] = float(
            target
        )

        if ticket_id in duplicate_timestamp_ids:
            result.at[index, "SLA Status"] = (
                "Duplicate Timestamp Records"
            )
            continue

        record = timestamp_map.get(ticket_id)

        if record is None:
            result.at[index, "SLA Status"] = (
                "Creation Time Missing/Invalid"
            )
            continue

        raw_created = record["created_at"]
        raw_response = record["first_responded_at"]

        result.at[index, "created_at"] = raw_created
        result.at[index, "first_responded_at"] = raw_response

        created = parse_time(raw_created)

        if pd.isna(created):
            result.at[index, "SLA Status"] = (
                "Creation Time Missing/Invalid"
            )
            continue

        if pd.isna(raw_response) or not str(raw_response).strip():
            result.at[index, "SLA Status"] = (
                "Response Not Recorded"
            )
            continue

        responded = parse_time(raw_response)

        if pd.isna(responded) or responded < created:
            result.at[index, "SLA Status"] = (
                "Invalid Response Timestamp"
            )
            continue

        response_minutes = (
            responded - created
        ).total_seconds() / 60

        result.at[index, "response_minutes"] = response_minutes

        result.at[index, "SLA Status"] = (
            "Met"
            if response_minutes <= target
            else "Breached"
        )

    return result


ROUTING_RULES = {
    "Booking": (
        "Platform Support",
        "Review booking status, calendar filters and scope.",
    ),
    "Payments": (
        "Platform Support",
        "Check transaction status; escalate discrepancies "
        "to payments specialists or technical defects to engineering.",
    ),
    "Messaging": (
        "Platform Support",
        "Check reminder configuration and provider delivery evidence.",
    ),
    "Other": ("General Support", "Clarify the issue and confirm priority and owner."),
    "Account": (
        "Account Support",
        "Verify authorization and follow approved access procedures.",
    ),
}


def route_ticket(ticket):
    team, reason = ROUTING_RULES.get(
        str(ticket["issue_type"]).strip().title(),
        (
            "General Support",
            "Clarify the issue and identify the appropriate owner.",
        ),
    )

    return {
        "ticket_id": ticket["ticket_id"],
        "issue_type": str(ticket["issue_type"]).strip().title(),
        "priority": ticket["priority"],
        "suggested_initial_team": team,
        "routing_reason": reason,
    }


# --------------------------------------------------
# RISK SIMULATION
# --------------------------------------------------

def simulation_status(elapsed, target):
    if elapsed > target:
        return "BREACHED"

    if elapsed >= target * RISK_WARNING_FRACTION:
        return "AT RISK"

    return "ON TRACK"


def simulation_action(status):
    actions = {
        "BREACHED": (
            "Verify response history. If unanswered, respond promptly, "
            "notify the support lead and record the missed target."
        ),
        "AT RISK": (
            "Prioritize the response and confirm the assigned owner."
        ),
        "ON TRACK": (
            "Continue monitoring and respond within the target."
        ),
    }

    return actions[status]


