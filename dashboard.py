
from pathlib import Path

import pandas as pd
import streamlit as st


# ---------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------

st.set_page_config(
    page_title="Clinic Support Dashboard",
    page_icon="🏥",
    layout="wide",
)

st.title("🏥 Clinic Support Operations Dashboard")
st.caption(
    "Healthcare SaaS support portfolio | "
    "Fictional clinic tickets and demonstration SLA policies"
)

BASE_DIR = Path(__file__).resolve().parent


# ---------------------------------------
# LOAD TICKETS
# ---------------------------------------

@st.cache_data
def load_tickets():
    try:
        tickets = pd.read_csv(BASE_DIR / "tickets.csv")
    except FileNotFoundError:
        st.error("tickets.csv was not found.")
        return pd.DataFrame()

    required_columns = {
        "ticket_id",
        "clinic",
        "issue_type",
        "priority",
        "status",
        "description",
    }

    missing = required_columns - set(tickets.columns)

    if missing:
        st.error(f"Missing columns: {sorted(missing)}")
        return pd.DataFrame()

    for column in ["clinic", "issue_type", "priority", "status"]:
        tickets[column] = (
            tickets[column].astype(str).str.strip().str.title()
        )

    return tickets


tickets = load_tickets()

if tickets.empty:
    st.warning("No valid ticket data available.")
    st.stop()


# ---------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------

st.sidebar.header("Support Filters")

selected_clinics = st.sidebar.multiselect(
    "Clinic",
    options=sorted(tickets["clinic"].unique()),
    default=sorted(tickets["clinic"].unique()),
)

selected_priorities = st.sidebar.multiselect(
    "Priority",
    options=sorted(tickets["priority"].unique()),
    default=sorted(tickets["priority"].unique()),
)

selected_statuses = st.sidebar.multiselect(
    "Status",
    options=sorted(tickets["status"].unique()),
    default=sorted(tickets["status"].unique()),
)

selected_issue_types = st.sidebar.multiselect(
    "Issue Type",
    options=sorted(tickets["issue_type"].unique()),
    default=sorted(tickets["issue_type"].unique()),
)

filtered_tickets = tickets[
    tickets["clinic"].isin(selected_clinics)
    & tickets["priority"].isin(selected_priorities)
    & tickets["status"].isin(selected_statuses)
    & tickets["issue_type"].isin(selected_issue_types)
].copy()


# ---------------------------------------
# SUPPORT OVERVIEW METRICS
# ---------------------------------------

st.subheader("Support Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Tickets", len(filtered_tickets))

col2.metric(
    "Urgent Tickets",
    int((filtered_tickets["priority"] == "Urgent").sum()),
)

col3.metric(
    "Open Tickets",
    int((filtered_tickets["status"] == "Open").sum()),
)

col4.metric(
    "High Priority",
    int(
        filtered_tickets["priority"]
        .isin(["High", "Urgent"])
        .sum()
    ),
)


# ---------------------------------------
# CREATE THREE TABS
# ---------------------------------------

overview_tab, queue_tab, sla_tab = st.tabs(
    ["Overview", "Ticket Queue", "SLA Monitoring"]
)


# ---------------------------------------
# TAB 1: OVERVIEW
# ---------------------------------------

with overview_tab:
    st.subheader("Support Ticket Analytics")

    left_col, right_col = st.columns(2)

    with left_col:
        st.write("Tickets by Priority")
        st.bar_chart(
            filtered_tickets["priority"].value_counts()
        )

    with right_col:
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


# ---------------------------------------
# TAB 2: TICKET QUEUE
# ---------------------------------------

with queue_tab:
    st.subheader("Support Ticket Queue")

    st.dataframe(
        filtered_tickets,
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        label="Download Filtered Tickets",
        data=filtered_tickets.to_csv(index=False),
        file_name="clinic_support_tickets.csv",
        mime="text/csv",
    )


# ---------------------------------------
# TAB 3: SLA MONITORING
# ---------------------------------------

with sla_tab:
    st.subheader("First-Response SLA Monitoring")

    st.caption(
        "Historical first-response SLA calculations "
        "using fictional support tickets."
    )

    try:
        policy = pd.read_csv(
            BASE_DIR / "sla_policy.csv"
        )

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

    # Normalize priority values
    policy["priority"] = (
        policy["priority"].astype(str).str.strip().str.title()
    )

    # Check for duplicate keys before merging
    if policy["priority"].duplicated().any():
        st.error("Duplicate priorities found in sla_policy.csv.")
        st.stop()

    if timestamps["ticket_id"].duplicated().any():
        st.error("Duplicate ticket IDs found in ticket_timestamps.csv.")
        st.stop()

    # Merge tickets with SLA policies
    sla_data = filtered_tickets.merge(
        policy[
            ["priority", "first_response_minutes"]
        ],
        on="priority",
        how="left",
        validate="many_to_one",
    )

    # Merge response timestamps
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

    # Convert timestamps to datetime
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

    # Calculate first-response time
    sla_data["response_minutes"] = (
        responded - created
    ).dt.total_seconds() / 60

    sla_data["first_response_minutes"] = pd.to_numeric(
        sla_data["first_response_minutes"],
        errors="coerce",
    )

    # ---------------------------------------
    # SLA STATUS CLASSIFICATION
    # ---------------------------------------

    def calculate_sla_status(row):
        if pd.isna(row["first_response_minutes"]):
            return "Policy Missing"

        # No timestamp record or creation time
        if pd.isna(row["created_at"]):
            return "Response Not Recorded"

        # No first-response timestamp
        if pd.isna(row["first_responded_at"]):
            return "Response Not Recorded"

        # Invalid timestamp formatting
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

    # ---------------------------------------
    # SLA METRICS
    # ---------------------------------------

    met = int(
        (sla_data["SLA Status"] == "Met").sum()
    )

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

    c1, c2, c3 = st.columns(3)

    c1.metric("SLA Met", met)
    c2.metric("SLA Breached", breached)
    c3.metric("Response Not Recorded", missing)

    evaluated = met + breached

    if evaluated > 0:
        compliance = met / evaluated * 100

        st.metric(
            "First-Response SLA Compliance",
            f"{compliance:.1f}%",
        )
    else:
        st.info(
            "No completed responses available "
            "for SLA evaluation."
        )

    # ---------------------------------------
    # SLA DETAILS TABLE
    # ---------------------------------------

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

    # ---------------------------------------
    # SLA STATUS CHART
    # ---------------------------------------

    st.subheader("SLA Status Distribution")

    st.bar_chart(
        sla_data["SLA Status"].value_counts()
    )

    # ---------------------------------------
    # ESCALATION ALERTS
    # ---------------------------------------

    st.subheader("Support Escalation Alerts")

    if breached > 0:
        st.error(
            f"{breached} ticket(s) breached "
            "their first-response SLA. "
            "Review and escalate as needed."
        )

    if missing > 0:
        st.warning(
            f"{missing} ticket(s) have no recorded "
            "first response. Verify the response history."
        )

    if invalid > 0:
        st.warning(
            f"{invalid} ticket(s) contain "
            "invalid response timestamps."
        )

    policy_missing = int(
        (
            sla_data["SLA Status"]
            == "Policy Missing"
        ).sum()
    )

    if policy_missing > 0:
        st.warning(
            f"{policy_missing} ticket(s) have "
            "no matching SLA policy."
        )

    if (
        breached == 0
        and missing == 0
        and invalid == 0
        and policy_missing == 0
    ):
        st.success(
            "No SLA breaches or missing response "
            "records in the selected tickets."
        )

    # ---------------------------------------
    # DOWNLOAD SLA REPORT
    # ---------------------------------------

    st.download_button(
        label="Download SLA Report",
        data=sla_data.to_csv(index=False),
        file_name="clinic_sla_report.csv",
        mime="text/csv",
    )


# ---------------------------------------
# FOOTER
# ---------------------------------------

st.divider()

st.caption(
    "Clinic Support Operations Lab | "
    "Portfolio demonstration | "
    "All clinics, tickets, and SLA targets are fictional. "
    "Not connected to a live healthcare platform."
)
