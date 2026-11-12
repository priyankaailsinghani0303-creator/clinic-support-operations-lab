
from pathlib import Path

import pandas as pd
import streamlit as st

from ticket_router import route_ticket


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Clinic Support Dashboard",
    page_icon="🏥",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent

st.title("🏥 Clinic Support Operations Dashboard")
st.caption(
    "Healthcare SaaS support portfolio | "
    "Fictional clinic tickets and demonstration policies"
)


# ==========================================
# LOAD SUPPORT TICKETS
# ==========================================

@st.cache_data
def load_tickets():
    try:
        data = pd.read_csv(BASE_DIR / "tickets.csv")
    except FileNotFoundError:
        st.error("tickets.csv was not found.")
        return pd.DataFrame()

    required = {
        "ticket_id",
        "clinic",
        "issue_type",
        "priority",
        "status",
        "description",
    }

    missing = required - set(data.columns)

    if missing:
        st.error(f"Missing ticket columns: {sorted(missing)}")
        return pd.DataFrame()

    for column in ["clinic", "issue_type", "priority", "status"]:
        data[column] = (
            data[column].astype(str).str.strip().str.title()
        )

    return data


tickets = load_tickets()

if tickets.empty:
    st.warning("No valid ticket data available.")
    st.stop()


# ==========================================
# SIDEBAR FILTERS
# ==========================================

st.sidebar.header("Support Filters")


def make_filter(column, label):
    options = sorted(tickets[column].dropna().unique())

    return st.sidebar.multiselect(
        label,
        options=options,
        default=options,
    )


selected_clinics = make_filter("clinic", "Clinic")
selected_priorities = make_filter("priority", "Priority")
selected_statuses = make_filter("status", "Status")
selected_issue_types = make_filter("issue_type", "Issue Type")

filtered_tickets = tickets[
    tickets["clinic"].isin(selected_clinics)
    & tickets["priority"].isin(selected_priorities)
    & tickets["status"].isin(selected_statuses)
    & tickets["issue_type"].isin(selected_issue_types)
].copy()


# ==========================================
# SUPPORT OVERVIEW METRICS
# ==========================================

st.subheader("Support Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Tickets", len(filtered_tickets))

c2.metric(
    "Urgent Tickets",
    int((filtered_tickets["priority"] == "Urgent").sum()),
)

c3.metric(
    "Open Tickets",
    int((filtered_tickets["status"] == "Open").sum()),
)

c4.metric(
    "High Priority",
    int(
        filtered_tickets["priority"]
        .isin(["High", "Urgent"])
        .sum()
    ),
)


# ==========================================
# CREATE FOUR TABS
# ==========================================

overview_tab, queue_tab, sla_tab, routing_tab = st.tabs(
    [
        "Overview",
        "Ticket Queue",
        "SLA Monitoring",
        "Ticket Routing",
    ]
)


# ==========================================
# TAB 1 — OVERVIEW
# ==========================================

with overview_tab:

    st.subheader("Support Ticket Analytics")

    left, right = st.columns(2)

    with left:
        st.write("Tickets by Priority")
        st.bar_chart(
            filtered_tickets["priority"].value_counts()
        )

    with right:
        st.write("Tickets by Status")
        st.bar_chart(
            filtered_tickets["status"].value_counts()
        )

    st.write("Tickets by Clinic")
    st.bar_chart(
        filtered_tickets["clinic"].value_counts()
    )

    st.write("Tickets by Issue Type")
    st.bar_chart(
        filtered_tickets["issue_type"].value_counts()
    )


# ==========================================
# TAB 2 — TICKET QUEUE
# ==========================================

with queue_tab:

    st.subheader("Support Ticket Queue")

    st.dataframe(
        filtered_tickets,
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "Download Filtered Tickets",
        data=filtered_tickets.to_csv(index=False),
        file_name="clinic_support_tickets.csv",
        mime="text/csv",
    )


# ==========================================
# TAB 3 — SLA MONITORING
# ==========================================

with sla_tab:

    st.subheader("First-Response SLA Monitoring")

    st.caption(
        "Historical SLA calculations using "
        "fictional clinic support tickets."
    )

    try:
        policy = pd.read_csv(BASE_DIR / "sla_policy.csv")
        timestamps = pd.read_csv(
            BASE_DIR / "ticket_timestamps.csv"
        )
    except FileNotFoundError as error:
        st.error(f"Required SLA file missing: {error}")
        st.stop()

    required_policy = {
        "priority",
        "first_response_minutes",
    }

    required_timestamps = {
        "ticket_id",
        "created_at",
        "first_responded_at",
    }

    if not required_policy.issubset(policy.columns):
        st.error("SLA policy file has missing columns.")
        st.stop()

    if not required_timestamps.issubset(timestamps.columns):
        st.error("Timestamp file has missing columns.")
        st.stop()

    policy["priority"] = (
        policy["priority"].astype(str).str.strip().str.title()
    )

    if policy["priority"].duplicated().any():
        st.error("Duplicate SLA priorities found.")
        st.stop()

    if timestamps["ticket_id"].duplicated().any():
        st.error("Duplicate timestamp ticket IDs found.")
        st.stop()

    sla_data = filtered_tickets.merge(
        policy[
            ["priority", "first_response_minutes"]
        ],
        on="priority",
        how="left",
        validate="many_to_one",
    )

    sla_data = sla_data.merge(
        timestamps[
            [
                "ticket_id",
                "created_at",
                "first_responded_at",
            ]
        ],
        on="ticket_id",
        how="left",
        validate="one_to_one",
    )

    created = pd.to_datetime(
        sla_data["created_at"],
        errors="coerce",
        utc=True,
    )

    responded = pd.to_datetime(
        sla_data["first_responded_at"],
        errors="coerce",
        utc=True,
    )

    sla_data["response_minutes"] = (
        responded - created
    ).dt.total_seconds() / 60

    sla_data["first_response_minutes"] = pd.to_numeric(
        sla_data["first_response_minutes"],
        errors="coerce",
    )

    # SLA classification

    def calculate_sla_status(row):

        if pd.isna(row["first_response_minutes"]):
            return "Policy Missing"

        if pd.isna(row["created_at"]):
            return "Response Not Recorded"

        if pd.isna(row["first_responded_at"]):
            return "Response Not Recorded"

        if pd.isna(row["response_minutes"]):
            return "Invalid Timestamp"

        if row["response_minutes"] < 0:
            return "Invalid Timestamp"

        if row["response_minutes"] <= row["first_response_minutes"]:
            return "Met"

        return "Breached"

    sla_data["SLA Status"] = sla_data.apply(
        calculate_sla_status,
        axis=1,
    )

    met = int((sla_data["SLA Status"] == "Met").sum())
    breached = int(
        (sla_data["SLA Status"] == "Breached").sum()
    )
    missing = int(
        (
            sla_data["SLA Status"]
            == "Response Not Recorded"
        ).sum()
    )
    invalid = int(
        (
            sla_data["SLA Status"]
            == "Invalid Timestamp"
        ).sum()
    )

    a, b, c = st.columns(3)

    a.metric("SLA Met", met)
    b.metric("SLA Breached", breached)
    c.metric("Response Not Recorded", missing)

    evaluated = met + breached

    if evaluated:
        st.metric(
            "First-Response SLA Compliance",
            f"{met / evaluated:.1%}",
        )
    else:
        st.info("No completed responses to evaluate.")

    st.subheader("Ticket SLA Details")

    st.dataframe(
        sla_data[
            [
                "ticket_id",
                "clinic",
                "issue_type",
                "priority",
                "first_response_minutes",
                "response_minutes",
                "SLA Status",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("SLA Status Distribution")

    st.bar_chart(
        sla_data["SLA Status"].value_counts()
    )

    st.subheader("Support Escalation Alerts")

    if breached:
        st.error(
            f"{breached} ticket(s) breached their "
            "first-response SLA. Review and escalate."
        )

    if missing:
        st.warning(
            f"{missing} ticket(s) have no recorded "
            "first response. Verify response history."
        )

    if invalid:
        st.warning(
            f"{invalid} ticket(s) contain "
            "invalid response timestamps."
        )

    policy_missing = int(
        (sla_data["SLA Status"] == "Policy Missing").sum()
    )

    if policy_missing:
        st.warning(
            f"{policy_missing} ticket(s) have "
            "no matching SLA policy."
        )

    if not any(
        [breached, missing, invalid, policy_missing]
    ):
        st.success(
            "No SLA breaches or missing response records "
            "in the selected tickets."
        )

    st.download_button(
        "Download SLA Report",
        data=sla_data.to_csv(index=False),
        file_name="clinic_sla_report.csv",
        mime="text/csv",
    )


# ==========================================
# TAB 4 — AUTOMATED TICKET ROUTING
# ==========================================

with routing_tab:

    st.subheader("Automated Ticket Routing")

    st.caption(
        "Rule-based ticket assignment using fictional "
        "healthcare SaaS support team structures."
    )

    if filtered_tickets.empty:
        st.info("No tickets match the selected filters.")

    else:
        # Use the existing ticket_router.py rules
        routing_results = [
            route_ticket(ticket)
            for ticket in filtered_tickets.to_dict(
                orient="records"
            )
        ]

        routing_df = pd.DataFrame(routing_results)

        # Routing summary metrics
        r1, r2, r3 = st.columns(3)

        r1.metric(
            "Tickets Routed",
            len(routing_df),
        )

        r2.metric(
            "Support Teams",
            routing_df["assigned_team"].nunique(),
        )

        r3.metric(
            "Urgent Tickets",
            int(
                (routing_df["priority"] == "Urgent").sum()
            ),
        )

        st.subheader("Ticket Assignment Queue")

        st.dataframe(
            routing_df,
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("Tickets by Assigned Team")

        st.bar_chart(
            routing_df["assigned_team"].value_counts()
        )

        st.subheader("Routing Decisions")

        for _, ticket in routing_df.iterrows():

            st.info(
                f"{ticket['ticket_id']} | "
                f"{ticket['issue_type']} | "
                f"Assigned to {ticket['assigned_team']}"
            )

        st.download_button(
            "Download Routing Report",
            data=routing_df.to_csv(index=False),
            file_name="clinic_ticket_routing.csv",
            mime="text/csv",
        )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "Clinic Support Operations Lab | "
    "Portfolio demonstration | "
    "All clinics, tickets, team assignments, "
    "and SLA targets are fictional. "
    "Not connected to a live healthcare platform."
)
