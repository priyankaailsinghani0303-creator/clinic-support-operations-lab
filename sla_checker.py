"""Print the same historical SLA results used by the dashboard."""
from pathlib import Path
import pandas as pd
from support_rules import calculate_sla, EVALUATED_STATUSES, PRIORITY_ORDER

BASE_DIR = Path(__file__).resolve().parent


def main():
    sla = calculate_sla(
        pd.read_csv(BASE_DIR / "tickets.csv"),
        pd.read_csv(BASE_DIR / "ticket_timestamps.csv"),
        pd.read_csv(BASE_DIR / "sla_policy.csv"),
    )
    met = int(sla["SLA Status"].eq("Met").sum())
    breached = int(sla["SLA Status"].eq("Breached").sum())
    evaluated = met + breached
    print(sla.to_string(index=False))
    print(f"\nTickets evaluated: {evaluated}")
    print(f"SLA met: {met}")
    print(f"SLA breached: {breached}")
    print(f"Cannot evaluate SLA: {len(sla) - evaluated}")
    print(f"SLA compliance: {met / evaluated:.1%}" if evaluated else "SLA compliance: N/A")
    print("\nTRIAGE QUEUE — PRIORITY ORDER")
    queue = sla.assign(priority_order=sla["priority"].map(PRIORITY_ORDER).fillna(99))
    print(queue.sort_values("priority_order", kind="stable").drop(columns="priority_order").to_string(index=False))
    print("\nRECORDS REQUIRING REVIEW")
    print(sla.loc[~sla["SLA Status"].eq("Met")].to_string(index=False))
    print("\nResolution targets are reference values; resolution compliance is not calculated.")


if __name__ == "__main__":
    main()
